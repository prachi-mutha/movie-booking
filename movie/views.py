from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
import MySQLdb as mdb
import datetime
import time
from django.utils.datastructures import MultiValueDictKeyError
import smtplib
# Create your views here.
city=""
display="" #theater name
name="" #movie name
date=""
time=""
price=""
email=""
seat=[]
total=0  #total payment
user=''
authan=''

def signedout(req):
	globals()['authan']=''
	globals()['city']=''
	globals()['display']=''
	globals()['date']=''
	globals()['name']=''
	globals()['email']=''
	globals()['user']=''
	
	con=mdb.connect("localhost","root","","movie")
	cur=con.cursor()
	q="SELECT movieName from moviedetail"
	cur.execute(q)
	rows=cur.fetchall()
	movieName=[]
	for movie in rows:
		movie=''.join(movie)
		movieName.append(movie)
	cur.close()
	con.close()
	return render(req,"movie1.html",{'movieName':movieName})

def movie1(req):
	con=mdb.connect("localhost","root","","movie")
	cur=con.cursor()
	q="SELECT movieName from moviedetail"
	cur.execute(q)
	rows=cur.fetchall()
	movieName=[]
	for movie in rows:
		movie=''.join(movie)
		movieName.append(movie)
	cur.close()
	con.close()
	return render(req,"movie1.html",{'movieName':movieName,'authan':authan,'user':user,'email':email})
def search(req):
	movie=req.GET['searched']
	m=movie.lower()
	m=m.replace(" ","")
	con=mdb.connect("localhost","root","","movie")
	cur=con.cursor()
	q="SELECT movieName from moviedetail"
	cur.execute(q)
	rows=cur.fetchall()
	moviename=''
	for movienm in rows:
		movienm=''.join(movienm)
		mn= movienm.lower()
		mn=mn.replace(" ","")
		if mn.__contains__(m):
			for i in m:
				if i in mn:
					moviename=movienm
					print(moviename)
				else:
					return redirect("/")
			cur.close()
			con.close()

			con=mdb.connect("localhost","root","","movie")
			cur=con.cursor()
			q="SELECT synopsis from moviedetail where movieName='%s'"%moviename
			cur.execute(q)
			rows=cur.fetchone()
			synopsis=''
			for syn in rows:
				syn=''.join(syn)
				synopsis+=syn
			cur.close()
			con.close()

			con=mdb.connect("localhost","root","","movie")
			cur=con.cursor()
			q=f"SELECT email,review,rating from userreview where movieName LIKE '%{movie}%'"
			cur.execute(q)
			rows=cur.fetchall()
			review=[]
			em=[]
			rate=0
			c=0
			for e,rev,rat in rows:
				e=''.join(e)
				rev=''.join(rev)
				rate+=rat
				review.append(rev)
				em.append(e)
				c+=1
			try:
				rating=int((rate/(c*5))*100)
			except:
				rating=0
			comb=[]
			for e,rev in zip(em,review):
				comb.append((e,rev))
			cur.close()
			con.close()
			context={'synopsis':synopsis,'video':'samp','movie':moviename,'review':comb,'rating':rating,'authan':authan,'user':user,'email':email}
			return render(req,"syn_detail.html",context)
	return redirect("/")

def movieSynopsis(req):
	movie=req.GET['movieName']
	con=mdb.connect("localhost","root","","movie")
	cur=con.cursor()
	q="SELECT synopsis from moviedetail where movieName='%s'"%movie
	cur.execute(q)
	rows=cur.fetchone()
	synopsis=''
	for syn in rows:
		syn=''.join(syn)
		synopsis+=syn
	cur.close()
	con.close()
	con=mdb.connect("localhost","root","","movie")
	cur=con.cursor()
	q="SELECT email,review,rating from userreview where movieName='%s'"%movie
	cur.execute(q)
	rows=cur.fetchall()
	review=[]
	em=[]
	rate=0
	c=0
	for e,rev,rat in rows:
		e=''.join(e)
		rev=''.join(rev)
		rate+=rat
		review.append(rev)
		em.append(e)
		c+=1
	try:
		rating=int((rate/(c*5))*100)
	except:
		rating=0
	comb=[]
	for e,rev in zip(em,review):
		comb.append((e,rev))
	cur.close()
	con.close()
	
	return render(req,"syn_detail.html",{'synopsis':synopsis,'video':'samp','movie':movie,'review':comb,'rating':rating,'authan':authan,'user':user})

def signin(req):
	return render(req,"signin.html")

def login_auth(req):
	con=mdb.connect("localhost","root","","movie")
	cur=con.cursor()
	q="SELECT city from location"
	cur.execute(q)
	rows=cur.fetchall()
	cities=[]
	for ct in rows:
		ct=''.join(ct)
		cities.append(ct)
	cities=set(cities)
	cur.close()
	con.close()
	if req.method=='POST' and authan!='true':
		email=req.POST['email']
		passwrd=req.POST['password']
		con=mdb.connect("localhost","root","","movie")
		cur=con.cursor()
		q="SELECT password,name from register where email='%s'"%email
		cur.execute(q)
		rows=cur.fetchall()
		for password,name in rows:
			row = ''.join(password) #tuple to string 
			print(row)
			if row==passwrd:
				globals()['user']=name
				globals()['email']=email
				#req.session['email']=email
				globals()['authan']='true'
				return render(req,'after_login1.html',{'user':user,'cities':sorted(cities),'c':' Choose Your City','authan':authan})
				break
		else:
			messages.info(req,"Invalid Credentials")
			return redirect('signin')
		cur.close()
		con.close()
	else:
		return render(req,'after_login1.html',{'user':user,'cities':sorted(cities),'c':' Choose Your City','authan':authan})

def signup(req):
	return render(req,"signup.html")
def register(req):
	if req.method=='POST':
		user_name=req.POST['user_name']
		email=req.POST['email']
		passwrd=req.POST['password']
		cpass=req.POST['pass']
		con=mdb.connect("localhost","root","","movie")
		cur=con.cursor()
		q="SELECT email from register where email='%s'"%email
		result=cur.execute(q)
		if result:
			messages.info(req,"email already exists")
		elif passwrd==cpass:
			con=mdb.connect("localhost","root","","movie")
			cur=con.cursor()
			q="INSERT into register(name,email,password) values('%s' ,'%s','%s')"%(user_name,email,passwrd)
			out=cur.execute(q)
			if out:
				messages.info(req,"created")
			else:
				messages.info(req,"try again")
			con.commit()
			con.close()
	return render(req,'signin.html')
	    
def after_login(req):
	
	return render(req,"after_login.html",{'user':user})
def after_login1(req):
	
	return render(req,"after_login1.html",{'city':cities,'authan':authan})
def movieDetails(req):
	
 	return render(req,"movieDetails.html",{'authan':authan})
def now(req):
	return render(req,"now.html")
def upComing(req):
	return render(req,"upComing.html")
def location(req):
	if req.method=='GET':
		l=req.GET['location']
		city=''.join(l)
		globals()['city']=city
		#s=req.GET['s'] 
		con=mdb.connect("localhost","root","","movie")
		cur=con.cursor()
		q="SELECT m.m_name from movies m ,location l where l.theater=m.theater and l.city='%s'"%city
		cur.execute(q)
		rows=cur.fetchall()
		nm=[]
		
		d=[]
		for m_name in rows:
			m=''.join(m_name)
			nm.append(m)
			
		movies=set(nm)
		return render(req,"movieDetails.html",{'city':city,'movies':movies,'user':user,'authan':authan})
def detail(req):
	return redirect(req,"detail.html",{'authan':authan})

def moviesp(req):
	globals()['name']=req.GET['movies']
	con=mdb.connect("localhost","root","","movie")
	cur=con.cursor()
	q="SELECT l.theater ,m.m_time from location l,movies m where l.theater=m.theater and l.city='%s'and  m.m_name='%s'"%(city,name)
	cur.execute(q)
	rows=cur.fetchall()
	cinemas=[]
	mtime=[]
	movietimes=[]
	d=[]
	for theater,m_time in rows:
		theater=''.join(theater)
		mtimes=str(m_time)
		mtime.append(mtimes)
		cinemas.append(theater)
	print(mtime)
	for theater,m_time in zip(cinemas,mtime):
		d.append((theater,m_time))
	print(d)
	mtimes=dict()
	for cinema,mt in d:
		movietimes=[]
		format = '%H:%M:%S' 
		datetime_str = datetime.datetime.strptime(mt, format).time()
		plus=datetime_str
		for n in range(10):  #no. of movie time 
			plus = (datetime.datetime.combine(datetime.date(1, 1, 1), plus) + datetime.timedelta(minutes=45)).time()
			t=str(plus.strftime("%H:%M %p"))
			movietimes.append(t)
			mtimes[cinema]=movietimes
	print(mtimes)
	print(movietimes)
	today = datetime.datetime.today() 
	d2 = today.strftime("%B %d-%A")
	d3=today+datetime.timedelta(1)
	d3=d3.strftime("%B %d-%A")
	globals()['name']=name
	
	ctime=datetime.datetime.today()
	ctime=ctime.strftime("%H:%M %p")
	ctime=str(ctime)
	context={'theater':cinemas,'video':'samp.mp4','today':d2,'tomorrow':d3,'range':range(1,7),'name':name,'ctime':ctime,'r':range(1,12),'user':user,'authan':authan,'mtimes':mtimes}
	return render(req,"detail.html",context)


	# for theater,m_name in rows:
	# 	nm.append(m_name)
	# 	cinemas.append(theater)
	# for theater,m_name in zip(cinemas,nm):
	# 	d.append((theater,m_name))
	# y=dict()
	# for li in d:
	# 	if li[0] in y:
	# 		y[li[0]].append(li[1])
	# 	else:
	# 		y[li[0]]=[li[1]]
	# print(y)
def review(req):
	rev=req.GET['review']
	rat=req.GET['rate']
	rating=int(rat)
	con=mdb.connect("localhost","root","","movie")
	cur=con.cursor()
	q="INSERT into userreview(email,movieName,review,rating) values('%s','%s' ,'%s','%d')"%(email,name,rev,rating)
	cur.execute(q)
	con.commit()
	con.close()
	
	return HttpResponse("<center><h2>FEEDBACK SUCCESSFULLY SUBMITTED</h2><a href='/'>Return to home page</a></center>")

	# return redirect("login_auth")

def book(req):

	display=req.GET['display']
	display=''.join(display)
	globals()['display']=display
	if req.method=='GET':
		try:
			date=req.GET['date']
			time=req.GET['booktime']
			globals()['date']=''.join(date)
			globals()['time']=''.join(time)
		except:
			return render(req,"movieDetails.html",{'authan':authan})


	day=['Friday','Saturday','Sunday']
	price_time=['10.00 AM','11.30 AM','12.15 PM']

	con=mdb.connect("localhost","root","","movie")
	cur=con.cursor()

	for i in day:
		if i in date:
			print(i)
			price="SELECT fss from movies where theater='%s' and m_name='%s'"%(display,name)
			cur.execute(price)
			price=cur.fetchone()
			for price in price:
				globals()['price']=price
			break
	
	else:
		price="SELECT mtwt from movies where theater='%s' and m_name='%s'"%(display,name)
		cur.execute(price)
		price=cur.fetchone()
		for price in price:
			globals()['price']=price


	con=mdb.connect("localhost","root","","movie")
	cur=con.cursor()
	q="SELECT seat from booking where movie='%s' and location='%s'and theater='%s' and time='%s' and date='%s'"%(name,city,display,time,date)
	cur.execute(q)
	rows=cur.fetchall()
	s=[]
	for seat in rows:
		s.append(''.join(seat))
	return render(req,"seat.html",{'seat':s,'range':range(1,7),'movie':name,'price':price,'display':display,'user':user,'authan':authan})

def seat(req):
	count=0
	A=[]
	seat=[]
	for r in range(65,71):
		for c in range(1,7):
			A.append(str(c)+chr(r))
	print(A)
	
	for a in A:
		c=req.GET.get(a,'off')
		if c=='on':
			count+=1
			seat.append(a)
			continue
	globals()['price']=int(price)
	globals()['total']=price*count
	globals()['seat']=seat

	context={'movie':name,'date':date,'time':time,'seat':seat,'theater':display,'price':total,'count':count,'user':user,'authan':authan}
	return render(req,"payment.html",context)
def pay(req):
	paid=req.GET['pay']
	p=int(paid)	
	con=mdb.connect("localhost","root","","movie")
	cur=con.cursor()
	for sit in seat:
		q="INSERT into booking(email,location,theater,movie,date,time,seat,payment,status) values('%s','%s' ,'%s','%s','%s','%s','%s','%d','%s')"%(email,city,display,name,date,time,sit,price,'booked')
		cur.execute(q)
	con.commit()
	con.close()
	try:
		server=smtplib.SMTP('smtp.gmail.com',587)
		server.ehlo() #identify comp
		server.starttls() #transport tlayer security
		content=f"Payment of {total} for {name}  is successfull.Selected seats are {seat} ,at {display} on {date} {time}  .Enjoy!!"
		f=open('movie/data.txt','r')
		p=f.readline()
		server.login('pracheejain1398@gmail.com',p)
		server.sendmail('pracheejain1398@gmail.com',email,content)
		server.close()
	except:
		return render(req,"review.html",{'user':user,'authan':authan})
	return render(req,"review.html",{'user':user,'authan':authan})