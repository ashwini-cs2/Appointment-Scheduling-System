from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import StaffProfile, Department, Service
from .forms import StaffCreationForm, StaffProfileForm, ServiceForm


def is_admin(user):
    if user.is_superuser:
        return True
    try:
        return user.student.user_type == 'admin'
    except Exception:
        return False


@login_required
def add_staff(request):
    """Only admin can add staff members."""
    if not is_admin(request.user):
        messages.error(request, 'Only administrators can add staff members.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = StaffCreationForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save()
            messages.success(request, f'Staff member {staff.name} added successfully!')
            return redirect('staff_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StaffCreationForm()

    departments = Department.objects.all()
    context = {
        'form': form,
        'departments': departments,
        'title': 'Add New Staff Member'
    }
    return render(request, 'staff_management/add_staff.html', context)


@login_required
def staff_list(request):
    """All logged-in users can view staff list."""
    staff_members = StaffProfile.objects.all().select_related('user', 'department')

    department_id = request.GET.get('department')
    if department_id:
        staff_members = staff_members.filter(department_id=department_id)

    availability = request.GET.get('availability')
    if availability == 'available':
        staff_members = staff_members.filter(is_available=True)
    elif availability == 'unavailable':
        staff_members = staff_members.filter(is_available=False)

    search_query = request.GET.get('search')
    if search_query:
        staff_members = staff_members.filter(
            Q(specialization__icontains=search_query) |
            Q(designation__icontains=search_query)
        )

    departments = Department.objects.all()
    context = {
        'staff_members': staff_members,
        'departments': departments,
        'title': 'Staff Directory',
        'is_admin': is_admin(request.user),
    }
    return render(request, 'staff_management/staff_list.html', context)


@login_required
def staff_detail(request, pk):
    staff = get_object_or_404(
        StaffProfile.objects.select_related('user', 'department'),
        pk=pk
    )
    services = Service.objects.filter(staff=staff)
    context = {
        'staff': staff,
        'services': services,
        'title': f'Staff Details - {staff.name}',
        'is_admin': is_admin(request.user),
    }
    return render(request, 'staff_management/staff_details.html', context)


@login_required
def edit_staff(request, pk):
    """Only admin can edit staff."""
    if not is_admin(request.user):
        messages.error(request, 'Only administrators can edit staff.')
        return redirect('dashboard')

    staff = get_object_or_404(StaffProfile, pk=pk)
    if request.method == 'POST':
        form = StaffProfileForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff details updated successfully!')
            return redirect('staff_detail', pk=staff.pk)
    else:
        form = StaffProfileForm(instance=staff)

    departments = Department.objects.all()
    context = {
        'form': form,
        'staff': staff,
        'departments': departments,
        'title': f'Edit Staff - {staff.name}'
    }
    return render(request, 'staff_management/edit_staff.html', context)


@login_required
def delete_staff(request, pk):
    """Only admin can delete staff."""
    if not is_admin(request.user):
        messages.error(request, 'Only administrators can delete staff.')
        return redirect('dashboard')

    staff = get_object_or_404(StaffProfile, pk=pk)
    if request.method == 'POST':
        staff_name = staff.name
        user = staff.user
        staff.delete()
        if user:
            user.delete()
        messages.success(request, f'Staff member {staff_name} deleted successfully!')
        return redirect('staff_list')

    context = {
        'staff': staff,
        'title': f'Delete Staff - {staff.name}'
    }
    return render(request, 'staff_management/delete_staff.html', context)


@login_required
def manage_services(request, staff_pk):
    """Only admin can manage services."""
    if not is_admin(request.user):
        messages.error(request, 'Only administrators can manage services.')
        return redirect('dashboard')

    staff = get_object_or_404(StaffProfile, pk=staff_pk)
    services = Service.objects.filter(staff=staff)

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.staff = staff
            service.save()
            messages.success(request, 'Service added successfully!')
            return redirect('manage_services', staff_pk=staff.pk)
    else:
        form = ServiceForm()

    context = {
        'staff': staff,
        'services': services,
        'form': form,
        'title': f'Manage Services - {staff.name}'
    }
    return render(request, 'staff_management/manage_services.html', context)


@login_required
def delete_service(request, staff_pk, service_pk):
    """Only admin can delete services."""
    if not is_admin(request.user):
        messages.error(request, 'Only administrators can delete services.')
        return redirect('dashboard')

    service = get_object_or_404(Service, pk=service_pk, staff_id=staff_pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully!')

    return redirect('manage_services', staff_pk=staff_pk)
