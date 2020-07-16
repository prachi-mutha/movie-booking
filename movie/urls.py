from . import views
from django.urls import path
from django.views.generic import TemplateView 
urlpatterns=[
path("",views.movie1,name="movie1"),
path("movieSynopsis",views.movieSynopsis,name="movieSynopsis"),
path("signin",views.signin,name="signin"),
path("search",views.search,name="search"),
path("login_auth",views.login_auth,name='login_auth'),
path("signup",views.signup,name="signup"),
path("register",views.register,name="register"),
path("after_login",views.after_login,name="after_login"),
path("after_login1",views.after_login1,name="after_login1"),
path("location",views.location,name="location"),
path("moviesp",views.moviesp,name="moviesp"),
path("movieDetails",views.movieDetails,name="movieDetails"),
path("book",views.book,name="book"),
path("detail",views.detail,name="detail"),
path("now",views.now,name="now"),
path("upComing",views.upComing,name="upComing"),
path("review",views.review,name="review"),
path("pay",views.pay,name="pay"),
path("seat",views.seat,name="seat"),
path("signedout",views.signedout,name="signedout")
#path("movie1",TemplateView.as_view(template_name="movie1.html"),name="movie1"),

]