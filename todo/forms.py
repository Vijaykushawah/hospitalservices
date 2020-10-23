from django.forms import ModelForm
from .models import Todo,Contact,MyProfile,SendMultiMail,MyBiodata,BiodataPrivacy,BiodataHelp,RequestsForApproval
from django.contrib.auth.models import User
from django import forms
from . import models


class TodoForm(ModelForm):
    class Meta:
        model=Todo
        fields=['title','memo','important']

class ContactForm(ModelForm):
    class Meta:
        model=Contact
        fields = '__all__'

class MyProfileForm(ModelForm):
    class Meta:
        model=MyProfile
        fields = {'user'}
class SendMultiMailForm(ModelForm):
    class Meta:
        model=SendMultiMail
        fields = {'receivers','subject','sender','body'}
class MyBiodataForm(ModelForm):
    class Meta:
        model=MyBiodata
        fields = {'name','age','gender','height','body_Weight','body_Type','complexion','mother_Toung',
        'social','religion','diet','cast','manglik','hobbies','education','profession','profession_type','job_location','annual_Income',
        'father_name','father_occupation','mother_name','mother_occupation','family_details','about',
        'contact_number','contact_privacy','email_ID','place','created_by','photo'}
    field_order=['name','age','gender','height','body_Weight','body_Type','complexion','mother_Toung',
        'social','religion','diet','cast','manglik','hobbies','education','profession','profession_type','job_location','annual_Income',
        'father_name','father_occupation','mother_name','mother_occupation','family_details','about',
        'contact_number','contact_privacy','email_ID','place','created_by','photo']

class BiodataPrivacyForm(ModelForm):
    class Meta:
        model=BiodataPrivacy
        fields = {'biodataid','contact_visibility','email_visibility','education_detail_visibility','address_detail_visibility',
        'hide_profile'}
    field_order=['biodataid','contact_visibility','email_visibility','education_detail_visibility','address_detail_visibility',
    'hide_profile']

class BiodataHelpForm(ModelForm):
    class Meta:
        model=BiodataHelp
        fields = '__all__'
class RequestsForApprovalForm(ModelForm):
    class Meta:
        model=RequestsForApproval
        fields = '__all__'

#hospitalservices
#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
#for doctor SignUp
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Patient
        fields=['address','mobile','status','symptoms','profile_pic']

class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']
