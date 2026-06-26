from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Department


@receiver(post_migrate)
def create_default_departments(sender, **kwargs):
    departments = [
        "CSE",
        "IT",
        "ECE",
        "EEE",
        "MECH",
        "CIVIL",
        "AI & DS"
    ]

    for dept in departments:
        Department.objects.get_or_create(name=dept)