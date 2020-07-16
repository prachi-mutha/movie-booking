from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class Booking(models.Model):
    email = models.CharField(max_length=30)
    location = models.CharField(max_length=20)
    theater = models.CharField(max_length=20)
    movie = models.CharField(max_length=20)
    date = models.CharField(max_length=30)
    time = models.CharField(max_length=20)
    seat = models.CharField(max_length=20)
    payment = models.IntegerField()
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'booking'
        unique_together = (('location', 'theater', 'movie', 'time', 'seat'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=20)
    theater = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'location'
        unique_together = (('city', 'theater'),)


class Moviedetail(models.Model):
    moviename = models.CharField(db_column='movieName', primary_key=True, max_length=30)  # Field name made lowercase.
    synopsis = models.TextField()
    avgrating = models.IntegerField(db_column='avgRating' ,blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'moviedetail'


class Movies(models.Model):
    id = models.AutoField(primary_key=True)
    theater = models.CharField(max_length=20)
    m_name = models.CharField(max_length=20)
    mtwt = models.IntegerField()
    fss = models.IntegerField()
    m_time = models.TimeField()

    class Meta:
        managed = False
        db_table = 'movies'
        unique_together = (('theater', 'm_name'),)


class Register(models.Model):
    name = models.TextField()
    email = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'register'


class Userreview(models.Model):
    email = models.CharField(max_length=30)
    moviename = models.CharField(db_column='movieName', max_length=30)  # Field name made lowercase.
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userreview'

		

