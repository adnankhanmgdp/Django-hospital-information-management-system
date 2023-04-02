from django.db import models

# Create your models here.
class Staff(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.BigIntegerField()
    staffId = models.CharField(max_length=10, primary_key=True)
    gender = models.CharField(max_length=6)
    isverifed = models.BooleanField()
    position = models.CharField(max_length= 255, default="Other")
    role=models.CharField(max_length=20)


class Roles(models.Model):
    role = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    permissions = models.CharField(max_length=11250)


class Patient(models.Model):
    pname = models.CharField(max_length=255)
    phone = models.BigIntegerField()
    address = models.CharField(max_length=500)
    age = models.SmallIntegerField()
    sex = models.CharField(max_length=10)
    guardian = models.CharField(max_length=255)
    ptype = models.CharField(max_length=3)
    doctor = models.CharField(max_length=255)
    caseid = models.CharField(max_length=255,primary_key=True)
    ward = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default="Admitted")
    bed = models.CharField(max_length=10)
    entryBy = models.CharField(max_length=255)
    dateofadm = models.DateTimeField(auto_now_add=True)

class Invoices(models.Model):
    caseid = models.CharField(max_length=255)
    invoiceid = models.AutoField(primary_key=True)
    path = models.CharField(max_length=300)
    date = models.DateField(auto_now_add=True)

class Logs(models.Model):
    datetime = models.DateTimeField( auto_now_add=True, primary_key=True)
    user = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    description  = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)

class WardsBeds(models.Model):
    ward = models.CharField(max_length=255)
    floor = models.CharField(max_length=255)
    beds = models.CharField(max_length=10)
    addedby = models.CharField(max_length=255)

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    qual = models.CharField(max_length=255)
    spec = models.CharField(max_length=255)
    exp = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, default="+919876543210")
    fee = models.CharField(max_length=255)
    did = models.CharField(max_length=255, primary_key=True)
    joindate = models.DateField(auto_now_add=True)
# class InvoiceData(models.Model):
    # caseid = models.CharField(max_length=255)
    
