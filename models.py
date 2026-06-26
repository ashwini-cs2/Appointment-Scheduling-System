from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    specialization = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)
    experience = models.IntegerField(default=0)
    qualifications = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    room_number = models.CharField(max_length=20, blank=True)
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)

    @property
    def name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def email(self):
        return self.user.email

    @property
    def phone(self):
        try:
            return self.user.student.phone_number
        except:
            return ''

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return f"{self.name} - {self.specialization}"


class Service(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.IntegerField(default=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name