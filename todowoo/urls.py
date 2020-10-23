"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from todo import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [

    path('accounts/', include('allauth.urls')),
    #path('',TemplateView.as_view(template_name='todo/loginuser.html')),

    path('admin/', admin.site.urls),
    #Auth
    path('signup/',views.signupuser,name='signupuser'),
    #Signup
    #Logout
    path('logout/',views.logoutuser,name='logoutuser'),
    path('login/',views.loginuser,name='loginuser'),
    #Todo
    path('',views.home,name='home'),
    path('create/',views.createtodo,name='createtodo'),
    path('current/',views.currenttodos,name='currenttodos'),
    path('completed/',views.completedtodos,name='completedtodos'),
    path('todo/<int:todo_pk>',views.viewtodo,name='viewtodo'),
    path('todo/<int:todo_pk>/complete',views.completetodo,name='completetodo'),
    path('todo/<int:todo_pk>/delete',views.deletetodo,name='deletetodo'),
    path('about/',views.abouttodo,name='abouttodo'),
    path('portfolio/',views.portfoliotodo,name='portfoliotodo'),
    path('contact/',views.contacttodo,name='contacttodo'),
    path('myprofile/',views.myprofiletodo,name='myprofiletodo'),
    path('removeassociate/',views.removeassociatetodo,name='removeassociatetodo'),
    path('getassociatestatus/<str:associateusername>',views.getassociatestatustodo,name='getassociatestatustodo'),
    path('exportdata/',views.exportdatatodo,name='exportdatatodo'),
    path('exportexceldata/',views.exportexceldatatodo,name='exportexceldatatodo'),
    path('exportcompledata/',views.exportcompledatatodo,name='exportcompledatatodo'),
    path('exportexcelcompledata/',views.exportexcelcompledatatodo,name='exportexcelcompledatatodo'),
    path('exportassociatedata/',views.exportassociatedatatodo,name='exportassociatedatatodo'),
    path('translator/',views.translatortodo,name='translatortodo'),
    path('translate/',views.translatetodo,name='translatetodo'),
    path('sendmail/',views.sendmailtodo,name='sendmailtodo'),
    path('passwordgenerator/',views.passwordgeneratortodo,name='passwordgeneratortodo'),
    path('createbiodata/',views.createbiodatatodo,name='createbiodatatodo'),
    path('mybiodata/',views.mybiodatatodo,name='mybiodatatodo'),
    path('mybiodata/<int:todo_pk>',views.viewmybiodatatodo,name='viewmybiodatatodo'),
    path('mybiodata/<int:todo_pk>/delete',views.mybiodatadeletetodo,name='mybiodatadeletetodo'),
    path('mybiodataprivacy/',views.mybiodataprivacytodo,name='mybiodataprivacytodo'),
    path('mybiodatadownload/',views.mybiodatadownloadtodo,name='mybiodatadownloadtodo'),
    path('mybiodatahome/',views.mybiodatahometodo,name='mybiodatahometodo'),
    path('viewcontact/',views.viewcontacttodo,name='viewcontacttodo'),
    path('biodatachats/',views.biodatachatstodo,name='biodatachatstodo'),
    path('biodatahelp/',views.biodatahelptodo,name='biodatahelptodo'),

    # Hosptal services urls
    # user clicked view
    path('userclick<int:todo_pk>', views.userclick_view,name='userclick_view'),
    path('userlogin', LoginView.as_view(template_name='todo/userlogin.html'),name='userlogin'),
    path('crosslogintodo', views.crosslogintodo,name='crosslogintodo'),



    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='todo/home.html'),name='logout'),

    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),



    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),

    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),


]
urlpatterns +=[
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),
    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
     path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
     path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
     path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
