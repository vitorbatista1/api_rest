from django.contrib import admin

from .models import User, MyUser

admin.site.register(User)

admin.site.register(MyUser)