from django import forms
from django.contrib.auth.models import User
from .models import StaffProfile, Department, Service
from accounts.models import Student


class StaffCreationForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = StaffProfile
        fields = [
            'department',
            'specialization',
            'designation',
            'experience',
            'qualifications',
            'bio',
            'room_number',
            'is_available'
        ]

        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'qualifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Validate username
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose another.")

        return username

    # Validate email
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")

        return email

    def save(self, commit=True):

        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )

        Student.objects.create(
            user=user,
            user_type='staff',
            phone_number=self.cleaned_data['phone_number']
        )

        staff = super().save(commit=False)
        staff.user = user

        if commit:
            staff.save()

        return staff


class StaffProfileForm(forms.ModelForm):

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = StaffProfile
        fields = [
            'department',
            'specialization',
            'designation',
            'experience',
            'qualifications',
            'bio',
            'room_number',
            'is_available'
        ]

        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'qualifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ['name', 'description', 'duration', 'price', 'is_active']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }