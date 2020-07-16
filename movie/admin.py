from django.contrib import admin

# Register your models here.
from .models import Location,Movies,Moviedetail
admin.site.register(Location)
admin.site.register(Movies)
admin.site.register(Moviedetail)