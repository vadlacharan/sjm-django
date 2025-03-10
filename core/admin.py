from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Publication)
admin.site.register(models.Likes)
admin.site.register(models.Saved)
admin.site.register(models.News)

admin.site.site_header = "SJMedSpace Admin Panel"   # Title in navbar
admin.site.site_title = "SJMedSpace Admin"          # Title in browser tab
admin.site.index_title = "Welcome to SJMedSpace Admin Dashboard"  # Title on the main page