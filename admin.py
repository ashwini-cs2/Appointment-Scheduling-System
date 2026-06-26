from django.contrib import admin
from .models import Department, StaffProfile, Service

admin.site.register(Department)
admin.site.register(StaffProfile)
admin.site.register(Service)