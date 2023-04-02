from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re, qrcode
from django.db.models import Q
from .models import Staff, Roles, Patient, Invoices, Logs, WardsBeds, Doctor
from django.contrib.auth.hashers import make_password, check_password
import datetime
import random
import requests

# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    if 'login' in request.session.keys():
        if request.session['login']==True:
            return redirect('/dashboard')
    return render(request, 'login.html')

def register(request): 
    if 'login' in request.session.keys():
        if request.session['login']==True:
            return redirect('/dashboard')   
    return render(request, "register.html")

def dashboard(request):
    if 'login' in request.session.keys():
        if request.session['login']==True:
            return render(request, 'index.html')
    else:
        return redirect('/')

def login(request):
    request.session['err'] = False
    request.session['succ'] = False
    if request.method=="POST":
        keys = request.POST.keys()
        if ('staffid' in keys) and ('pass' in keys):
            staffid = str(request.POST['staffid']).strip()
            password = str(request.POST['pass']).strip()
            if staffid!="" and password!="":
                staff = Staff.objects.filter(staffId=staffid).first()
                if staff != None:
                    if check_password(password,staff.password):
                        if int(staff.isverifed)==1:
                            name = staff.fullname.split(' ')
                            if 'err' in request.session.keys():
                                request.session.pop('err')
                                # request.session.pop('err_msg')
                            if 'succ' in request.session.keys():
                                request.session.pop('succ')
                                # request.session.pop('succ_msg')
                                # pass
                            request.session['login']=True
                            request.session['email']=staff.email
                            request.session['fname']=name[0]
                            request.session['lname']=name[1]
                            request.session['fullname']=staff.fullname
                            request.session['address']=staff.address
                            request.session['phone']=staff.phone
                            request.session['staffid']=staffid
                            request.session['gender']=staff.gender
                            request.session['role']=staff.role
                            request.session['position'] = staff.position
                            log = Logs(user=staff.fullname, position=staff.position, description=f"{staff.fullname} with id ({staff.staffId}) logged in", ip=f"{get_client_ip(request)}")
                            log.save()
                            return redirect('/dashboard')
                        else:
                            request.session['err']=True
                            request.session['err_msg']="Your account has not been verified yet, Please check back later."
                    else:
                        request.session['err']=True
                        request.session['err_msg']="Incorrect password. Try again or reset your password."
                else:
                    request.session['err']=True
                    request.session['err_msg']="Staff Id not found. Check your ID and try again."
            else:
                request.session['err']=True
                request.session['err_msg']="Staff Id and password are required."
        else:
            request.session['err']=True
            request.session['err_msg']="Please provide staff id and password to log in."
    return redirect('/')

def logout(request):
    try:
        log = Logs(user=request.session['fullname'], position=request.session['position'], description=f"{request.session['fullname']} with id ({request.session['staffid']}) logged out", ip=f"{get_client_ip(request)}")
        log.save()
        request.session.pop('login')
        request.session.pop('email')
        request.session.pop('fname')
        request.session.pop('lname')
        request.session.pop('fullname')
        request.session.pop('address')
        request.session.pop('phone')
        request.session.pop('staffid')
        request.session.pop('gender')
        request.session.pop('role')
    except Exception as e:
        print(e)
    finally:
        return redirect('/')


def signup(request):
    request.session['err']=False
    request.session['succ'] = False
    request.session['err_msg'] = ""
    if request.method=="POST":
        keys = request.POST.keys()
        if ('fname' in keys) and ('lname' in keys) and ('email' in keys) and ('pass' in keys) and ('cpass' in keys) and ('address' in keys) and ('pincode' in keys) and ('phone' in keys) and ('staffid' in keys) and ('gender' in keys):
            fname = str(request.POST['fname']).strip().title()
            lname = str(request.POST['lname']).strip().title()
            email = str(request.POST['email']).strip()
            password = str(request.POST['pass']).strip()
            cpass = str(request.POST['cpass']).strip()
            address = str(request.POST['address']).strip()
            pincode = str(request.POST['pincode']).strip()
            phone = str(request.POST['phone']).strip()
            staffid = str(request.POST['staffid']).strip()
            gender = str(request.POST['gender']).strip()
            if (fname != "") and (lname != "") and (email != "") and (password != "") and (cpass != "") and (address != "") and (pincode != "") and (phone != "") and (staffid != "") and (gender != ""):
                # print(fname, lname, email, password, cpass, address, pincode, phone, staffid, gender)
                if password == cpass:
                    if len(password) > 8 and len(password) < 15:
                        if re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",email):
                            if len(phone) == 10:
                                if len(pincode) == 6:
                                    if len(staffid) == 6:
                                        if gender == 'Male' or gender == 'Female':
                                            staff1 = Staff.objects.filter(email=email).first()
                                            staff2 = Staff.objects.filter(staffId=staffid).first()
                                            # print(staff1, staff2)
                                            if staff1 == None and staff2 == None:
                                                fullname = f"{fname} {lname}"
                                                password = make_password(password=password)
                                                user = Staff(fullname=fullname,email=email,password=password,address=f"{address}, {pincode}",phone=phone,staffId=staffid,gender=gender,isverifed=0,role='minimal')
                                                user.save()
                                                request.session['err']=False
                                                request.session['err_msg'] = ""
                                                request.session['succ']=True
                                                request.session['succ_msg']="Your account has been created, but is under review. You can Login to your account once verified"
                                                log = Logs(user=user.fullname, position=user.position, description=f"{user.fullname} with id ({user.staffId}) created an account", ip=f"{get_client_ip(request)}")
                                                log.save()
                                                return redirect('/')
                                            else:
                                                request.session['err']=True
                                                request.session['err_msg']="Staff Id or Email already registered"
                                        else:
                                            request.session['err']=True
                                            request.session['err_msg']="There is some error while storing gender data."
                                    else:
                                        request.session['err']=True
                                        request.session['err_msg']="Please enter a valid Staff ID."
                                else:
                                    request.session['err']=True
                                    request.session['err_msg']="Please enter a valid pincode."
                            else:
                                request.session['err']=True
                                request.session['err_msg']="Please enter only 10 digit Mobile number."
                        else:
                            request.session['err']=True
                            request.session['err_msg']="Please enter a valid email address."
                    else:
                        request.session['err']=True
                        request.session['err_msg']="Password should be of 8-15 characters only."
                else:
                    request.session['err']=True
                    request.session['err_msg']="Oops! Password mismatch. Please choose a strong password."
            else:
                request.session['err']=True
                request.session['err_msg']="Some fields are missing! Please fill in all the details."
        else:
            request.session['err']=True
            request.session['err_msg']="Some fields are missing, please fill all the details"
    
    return redirect('register/')

def allPatients(request):
    pat = Patient.objects.all().order_by('-dateofadm').values()
    return render(request, 'patient-list.html',{'patients':pat})

def ipd_patients(request):
    ipd = Patient.objects.filter(ptype="IPD").all()
    return render(request, 'patient-list.html',{'patients':ipd})

def opd_patients(request):
    opd = Patient.objects.filter(ptype="OPD").all()
    return render(request, 'patient-list.html',{'patients':opd,'result':'OPD'})

def roles(request):
    role = Roles.objects.all().values()
    # print(role)
    return render(request, 'roles.html', {'roles':role})

def newrole(request):
    if request.method=="POST":
        # print(request.POST['role'])
        # print(request.POST['desc'])
        # role = Roles(role=)
        if 'role' in request.POST.keys() and 'desc' in request.POST.keys():
            role = str(request.POST['role']).strip().title()
            desc = str(request.POST['desc']).strip().title()
            if role != "" and desc != "":   
                dbrole = Roles(role=role, description=desc, permissions="")
                dbrole.save()
    return redirect('/roles')

def newPatient(request):
    try:
        if request.session["login"] == True and request.method == "POST":
            pname = str(request.POST['pname']).strip()
            phone = str(request.POST['phone']).strip()
            addr = str(request.POST['address']).strip()
            age = str(request.POST['age']).strip()
            sex = str(request.POST['gender']).strip()
            guardian = str(request.POST.get('guardian',"")).strip()
            ptype= str(request.POST['ptype']).strip()
            # dateadmissn = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            doctor = str(request.POST['doctor']).strip()
            caseid = str(request.POST['caseid']).strip()
            ward = str(request.POST.get('ward',"")).strip()
            bed = str(request.POST.get('bed',"")).strip()
            status = "admitted"
            if ptype == "OPD":
                ward = ""
                bed = ""
                status = "Ongoing Treatment"
            patient = Patient(pname, phone, addr, age, sex, guardian, ptype, doctor, caseid, ward,status, bed, request.session['fullname'])
            patient.save()
            log = Logs(user=request.session['fullname'], position=request.session['position'], description=f"New patient {pname} (CaseId: {caseid}) added by {request.session['fullname']} (stffId: {request.session['staffid']})", ip=f"{get_client_ip(request)}")
            log.save()
    except Exception as e:
        print("-->",e)
    finally:
        return redirect("/all-patients")
def patientDetails(request, slug):
    patient = Patient.objects.get(caseid=slug)
    print(patient)
    return render(request, "patient-details.html", {'patient': patient})

def patientInvoice(request, slug):
    mon = ['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    patient = Patient.objects.get(caseid=slug)
    if patient is not None:
        invoice = Invoices.objects.filter(caseid=patient.caseid).count()
        # print(invoice)
        if invoice == 0:
            invoice = Invoices(caseid=patient.caseid,path="")
            invoice.save()
            invoice = Invoices.objects.filter(caseid=patient.caseid).values()
            Invoices.objects.filter(caseid=patient.caseid).update(path=f"/hospital/static/invoices/{invoice[0]['invoiceid']}.pdf")
        invoice = Invoices.objects.filter(caseid=patient.caseid).values()
        invdate = str(invoice[0]['date']).split("-")
        invdate = mon[int(invdate[1])-1]+" "+invdate[2]+", "+invdate[0]
        print(patient)
        admdate = str(patient.dateofadm).split(" ")[0].split("-")
        admdate = mon[int(admdate[1])-1]+" "+admdate[2]+", "+admdate[0]
        print(admdate)

    return render(request,'patient-info.html',{'patient':patient,'invoice':invoice,"invdate":invdate, "admdate":admdate})

@csrf_exempt
def geninvoice(request):
    mon = ['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    if request.method=="POST":
        print(request.POST)
        datakeys = request.POST.keys()
        data = {'inv':[]}
        i=1
        invdata = {}
        dd = []
        print(datakeys)
        for key in datakeys:
            # print(key)
            if 'itemName' in key:
                invdata['itemName'] = request.POST[key]
                invdata['n'] = i
                i+=1
            if 'itemRate' in key:
                invdata['itemRate'] = float("{:.2f}".format(float(request.POST[key])))
            if 'quantity' in key:
                invdata['quantity'] = request.POST[key]
            if 'totalAmount' in key:
                invdata['totalAmount'] = float("{:.2f}".format(float(request.POST[key])))
                print(invdata)
                dd.append(invdata.copy())
                print(dd)
            if 'subtotal' in key:
                data['subtotal'] = float(request.POST[key])
            if 'discount' in key:
                if request.POST[key] == '':
                    data['discount'] = 0
                else:
                    data['discount'] = float(request.POST[key])
                    data['dp'] = float("{:.2f}".format((data['discount']*100)/data['subtotal']))
            if 'paid' in key:
                if request.POST[key] == '':
                    data['paid'] = 0
                else:
                    data['paid'] = float(request.POST[key])
            if 'caseid' in key:
                caseid = request.POST[key]
            if 'pmethod' in key:
                pmethod = request.POST[key]
                if pmethod == "Cash":
                     data['pmethod']= "Cash"
                else:
                     data['pmethod']= "Bank Transfer"
        data['inv'] = dd
        data['amount'] = data['subtotal'] - data['discount']
        data['due'] = data['amount'] - data['paid']
        print(data)
        patient = Patient.objects.get(caseid=caseid)
        admdate = str(patient.dateofadm).split(" ")[0].split("-")
        admdate = mon[int(admdate[1])-1]+" "+admdate[2]+", "+admdate[0]
        invoiced = datetime.datetime.today().strftime("%Y-%m-%d")
        invdate = invoiced.split("-")
        invdate = mon[int(invdate[1])-1]+" "+invdate[2]+", "+invdate[0]
        # uri = "https://api.qr-code-generator.com/v1/create?access-token=pNJC2w3jR552LVQi5LQRBkzI1LHTTeQhE2P22GleZ0ouqmj7GXmVsWwJr7Sq_Eti"
        # jsondata = {
        #         "frame_name": "no-frame",
        #         "qr_code_text": f"upi://pay?pa=875626098048@paytm&am={data['due']}&pn=PaytmUser&mc=0000&mode=02&purpose=00&orgid=159761",
        #         "image_format": "JPG",
        #         "qr_code_logo": "scan-me",
        #         "image_width": 400,
        #         "download": 1
        #     }
        # x = requests.post(uri, json=jsondata)
        # print(x.text)
        img = qrcode.make(f"upi://pay?pa=875626098048@paytm&am={data['due']}&pn=PaytmUser&mc=0000&mode=02&purpose=00&orgid=159761")
        img.save("hospital/static/qr.png")
        # f = open("hospital/static/qr.jpg", mode="wb")
        # f.write(x.content)
        # f.close()
    return render(request, 'invoice.html',{"patient":patient,'data':data, 'admdate':admdate, 'invdate':invdate})

def getlogs(request):
    try:
        if request.session["login"] == True:
            logs = Logs.objects.order_by("datetime")[:200]
            return render(request, "logs.html", {"logs":logs})
        else:
            return redirect("/")
    except Exception as e:
        return redirect("/")


def addbeds(request):
    if request.method == "POST":
        ward = request.POST.get('wardname','')
        floor = request.POST.get('floorname', '')
        beds = request.POST.get('nofbeds', '')
        if ward != "" and floor != "" and beds != "":
            wardbed = WardsBeds(ward=ward, floor=floor, beds=beds, addedby=request.session['staffid'])
            wardbed.save()
            log = Logs(user=request.session['fullname'], position=request.session['position'], description=f"{request.session['fullname']} with id ({request.session['staffid']}) added a ward {ward} with {beds} bed(s) on floor {floor}", ip=f"{get_client_ip(request)}")
            log.save()
    
    beds = WardsBeds.objects.all()
    return render(request,"addbeds.html",{"beds":beds})

def getwards(request):
    if 'w' in request.GET.keys():
        beds = WardsBeds.objects.filter(ward=request.GET['w'])
        return HttpResponse(beds[0].beds)
    wards = WardsBeds.objects.all()
    s = ""
    for ward in wards:
        s = s+ f"<option value='{ward.ward}'>{ward.ward}</option>"
    return HttpResponse(s)


def toipd(request):
    if request.method == "POST":
        caseid = request.POST.get('caseoid', '').strip()
        ward = request.POST.get('wardd', '').strip()
        bed = request.POST.get('bedd', '').strip()
        if caseid != "" and ward != "" and bed != "":
            cases = "OPD-"+caseid.split("-")[1]
            Patient.objects.filter(caseid=cases).update(caseid=caseid, ptype="IPD", ward=ward, bed=bed)
            log = Logs(user=request.session['fullname'], position=request.session['position'], description=f"{request.session['fullname']} with id ({request.session['staffid']}) converted OPD patient with case id{cases} to IPD (new caseID: {caseid})", ip=f"{get_client_ip(request)}")
            log.save()
    return redirect("/ipd-patients")

def adddoctor(request):
    if request.method == "POST":
        print("form recieved")
        dname = request.POST.get('docname',"").strip().upper()
        qual = request.POST.get('qualification',"").strip().upper()
        spec = request.POST.get('specialization',"").strip().upper()
        exp = request.POST.get('exp',"").strip()
        email = request.POST.get('docemail',"").strip().lower()
        docpass = request.POST.get('docpass',"").strip()
        phone = request.POST.get('phone',"").strip()
        fee = request.POST.get('fee',"").strip()
        # print(dname, qual, spec, exp, email, docpass,)
        if dname != "" and qual != "" and spec != "" and exp != "" and email != "" and docpass != "" and phone != "" and fee != "":
            print("form valid")
            p = make_password(docpass)
            n = dname.split(" ")
            did = ""
            for i in n:
                did += i[0]
            did += f"{exp}"
            did += f"{random.randint(235738,923829)}"
            # print(did)
            doctor = Doctor(name=dname, qual=qual, spec=spec, exp=exp, email=email, password=p, status='active', phone=phone, fee=fee, did=did)
            doctor.save()
            log = Logs(user=request.session['fullname'], position=request.session['position'], description=f"{request.session['fullname']} with id ({request.session['staffid']}) added a new doctor {dname} ({qual} - {spec}) Doctor ID: {did}", ip=f"{get_client_ip(request)}")
            log.save()
    doctors = Doctor.objects.all()
    return render(request, 'add-doctor.html', {"doctors":doctors})

def getdocname(request):
    doctors = Doctor.objects.all()
    s = "<option selected disabled>Choose doctor... </option>"
    for doc in doctors:
        s += f"<option value='{doc.did}'>{doc.name.title()} ({doc.qual}) - {doc.spec.capitalize()} </option>"
    return HttpResponse(s)

def alldoctors(request):
    doctors = Doctor.objects.filter(status="active")
    return render(request, 'all-doctors.html', {"doctors":doctors})

def doctordetail(request, slug):
    if slug != "":
        doctor = Doctor.objects.filter(did=slug)
        # print(len(doctor))
        if len(doctor) > 0:
            # print(doctor)
            return render(request, "doctor-detail.html",{"doctor":doctor[0]})

    return redirect("/")

def stafflist(request):
    stf = Staff.objects.filter(~Q(role='su'))
    return render(request,'all-staff.html',{"staffs":stf})

def getstaff(request,slug):
    sid = str(slug).strip()
    try:
        if sid != "":
            stf = Staff.objects.get(staffId=sid)
            # print("-->",stf)
            return render(request,'staff-detail.html',{"staff":stf})
    except Exception as e:
        print(e)
        return redirect('/staff-list')