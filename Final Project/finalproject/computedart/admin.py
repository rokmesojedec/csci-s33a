from django.contrib import admin
from .models import User, Configuration, Color

# Register your models here.
admin.site.register(Configuration)
admin.site.register(Color)
admin.site.register(User)