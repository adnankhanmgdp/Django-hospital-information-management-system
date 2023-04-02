from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.logout, name="logout"),
    path('opd-patients', views.opd_patients, name="OPD patients"),
    path('ipd-patients', views.ipd_patients, name="IPD patients"),
    path('roles', views.roles, name="roles"),
    path('newrole', views.newrole, name="New role"),
    path('add-patient', views.newPatient, name="add patient"),
    path('all-patients', views.allPatients, name="All Patients"),
    path('patient/<slug:slug>', views.patientDetails, name="Patient Details"),
    path('patientinv/<slug:slug>', views.patientInvoice, name="Patient Invoice"),
    path('geninvoice',views.geninvoice, name="generate invoice"),
    path('logs', views.getlogs, name='system logs'),
    path('addbeds', views.addbeds, name= "Add beds view"), 
    path('getwards', views.getwards, name="GET beds"),
    path('toipd', views.toipd, name = "Change OPD to IPD"),
    path('add-doctor', views.adddoctor, name="Add new Doctor"),
    path('getdocname',views.getdocname, name=" GET doctors list"),
    path('all-doctors', views.alldoctors, name="List Doctors"),
    path('doctor/<slug:slug>', views.doctordetail, name="Doctor Details"),
    path('staff-list',views.stafflist, name="List of Staff"),
    path('staff/<slug:slug>', views.getstaff, name="Staff Details")
]