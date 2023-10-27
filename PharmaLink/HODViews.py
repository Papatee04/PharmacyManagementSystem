from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import  UserCreationForm
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone, dateformat
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import datetime 
from .forms import *
from .models import *
from .utils import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


@login_required
@user_passes_test(is_admin, login_url='denied')
def adminDashboard(request):
    patients_total=Patients.objects.all().count()
    
    doctors=Doctor.objects.all().count()
    pharmacist=Pharmacist.objects.all().count() 
    out_of_inventory=Inventory.objects.filter(quantity__lte=0).count()
    total_inventory=Inventory.objects.all().count()


    today = datetime.today()
    expired_drugs = Inventory.objects.filter(valid_to__lt=today)
    expired_count = expired_drugs.count()
     


    context={
        "patients_total":patients_total,
        "expired_total":expired_count,
        "out_of_inventory":out_of_inventory,
        "total_drugs":total_inventory,
        "all_doctors":doctors,
        "all_pharmacists":pharmacist,

        

    }
    return render(request,'hod_templates/admin_dashboard.html',context)



@login_required
@user_passes_test(is_admin, login_url='denied')
def createPatient(request):
    form=PatientForm()

 
    if request.method == "POST":
        form=PatientForm(request.POST, request.FILES)

        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']
            reg_no = form.cleaned_data['reg_no']



            user = CustomUser.objects.create_user(username=username, email=email,password=password, last_name=last_name,user_type=5)
            user.patients.address = address
            user.patients.phone_number = phone_number
            user.patients.dob=dob
            user.patients.reg_no=reg_no
            user.patients.first_name=first_name
            user.patients.last_name=last_name
            user.patients.gender=gender

            user.save()
            messages.success(request, username +' was Successfully Added')

            return redirect('patient_form')

          
   

    context={
        "form":form,
        "title":"Add Patient"
    }
       
    return render(request,'hod_templates/patient_form.html',context)



@login_required
@user_passes_test(is_admin, login_url='denied')
def allPatients(request):
    form=PatientSearchForm1(request.POST or None)
    patients=Patients.objects.all()
    context={
        "patients":patients,
        "form":form,
        "title":"Admitted Patients"
    }
    if request.method == 'POST':
        # admin=form['first_name'].value()
        name = request.POST.get('search')
        patients=Patients.objects.filter(first_name__icontains=name) 
       
        context={
            "patients":patients,
            form:form
        }
    return render(request,'hod_templates/admited_patients.html',context)

@login_required
@user_passes_test(is_admin, login_url='denied')
def confirmDelete(request,pk):
    try:
        patient=Patients.objects.get(id=pk)
        if request.method == 'POST':
            patient.delete()
            return redirect('all_patients')
    except:
        messages.error(request, "Patient Cannot be deleted  deleted , Patient is still on medication or an error occured")
        return redirect('all_patients')

    context={
        "patient":patient,

    }
    
    return render(request,'hod_templates/sure_delete.html',context)





    
@login_required
@user_passes_test(is_admin, login_url='denied')
def createPharmacist(request):

    if request.method == "POST":
           
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
           
        
        user = CustomUser.objects.create_user(username=username, email=email,password=password, first_name=first_name, last_name=last_name,user_type=2)
        user.first_name=first_name
        user.last_name=last_name
        user.pharmacist.address = address
        user.pharmacist.mobile = mobile

        user.save()
        messages.success(request, "Staff Added Successfully!")
        return redirect('add_pharmacist')
       

    context={
    "title":"Add Pharmacist"

    }
    

    return render(request,'hod_templates/pharmacist_form.html',context)

@login_required
@user_passes_test(is_admin, login_url='denied')
def managePharmacist(request):
    staffs = Pharmacist.objects.all()
    context = {
        "staffs": staffs,
        "title":"Manage Pharmacist"
    }

    return render(request,'hod_templates/all_pharmacist.html',context)


@login_required
@user_passes_test(is_admin, login_url='denied')
def createDoctor(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        emp_no = request.POST.get('emp_no')
        specialisation = request.POST.get('specialisation')  # Corrected variable name

        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, user_type=3)
            user.doctor.address = address
            user.doctor.mobile = mobile
            user.doctor.emp_no = emp_no
            user.doctor.specialisation = specialisation  # Corrected variable name

            user.save()
            messages.success(request, "Doctor Added Successfully!")
            return redirect('add_doctor')
        except:
            messages.error(request, "Failed to Add Doctor!")
            return redirect('add_doctor')

    context = {
        "title": "Add Doctor",
    }

    return render(request, 'hod_templates/add_doctor.html', context)


@login_required
@user_passes_test(is_admin, login_url='denied')
def manageDoctor(request):
    staffs = Doctor.objects.all()

    context = {
        "staffs": staffs,
        "title":"Dotors Details"

    }

    return render(request,'hod_templates/manage_doctor.html',context)



@login_required
@user_passes_test(is_admin, login_url='denied')
def addInventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Drug Added Successfully!")
            return redirect('add_inventory')
        # The 'else' block is not needed here; messages will be set automatically for form errors
    else:
        form = InventoryForm()

    context = {
        "form": form,
        "title": "Add New Drug"
    }
    return render(request, 'hod_templates/add_inventory.html', context)


    
@login_required
@user_passes_test(is_admin, login_url='denied')
def manageInventory(request):
    inventorys = Inventory.objects.all().order_by("-id")
    ex=Inventory.objects.annotate(
    expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True)
    eo=Inventory.objects.annotate(
    expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=False)
    

    context = {
        "inventorys": inventorys,
        "expired":ex,
        "expa":eo,
        "title":"Manage Inventoryed Drugs"
    }

    return render(request,'hod_templates/manage_inventory.html',context)


@login_required
@user_passes_test(is_admin, login_url='denied')
def addCategory(request):
    try:
        form=CategoryForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Category added Successfully!")

                return redirect('add_category')
    except:
        messages.error(request, "Category Not added! Try again")

        return redirect('add_category')

    
    context={
        "form":form,
        "title":"Add a New Drug Category"
    }
    return render(request,'hod_templates/add_category.html',context)

@login_required
@user_passes_test(is_admin, login_url='denied')
def addPrescription(request):
    form=PrescriptionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('prescribe')
    
    context={
        "form":form,
        "title":"Prescribe Drug"
    }
    return render(request,'hod_templates/prescribe.html',context)



    
@login_required
@user_passes_test(is_admin, login_url='denied')
def editPatient(request,patient_id):
    # adds patient id into session variable
    request.session['patient_id'] = patient_id

    patient = Patients.objects.get(admin=patient_id)

    form = EditPatientForm()
    

    # filling the form with data from the database
    form.fields['email'].initial = patient.admin.email
    form.fields['username'].initial = patient.admin.username
    form.fields['first_name'].initial = patient.first_name
    form.fields['last_name'].initial = patient.last_name
    form.fields['address'].initial = patient.address
    form.fields['gender'].initial = patient.gender
    form.fields['phone_number'].initial = patient.phone_number
    form.fields['dob'].initial = patient.dob
    if request.method == "POST":
        if patient_id == None:
            return redirect('all_patients')
        form = EditPatientForm( request.POST)

        if form.is_valid():
            
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            gender = form.cleaned_data['gender']
            dob=form.cleaned_data['dob']
            phone_number = form.cleaned_data['phone_number']


            try:
            # First Update into Custom User Model
                user = CustomUser.objects.get(id=patient_id)
                user.username = username

                user.email = email
                user.save()

                # Then Update Students Table
                patients_edit = Patients.objects.get(admin=patient_id)
                patients_edit.address = address
                patients_edit.gender = gender
                patients_edit.dob=dob
                patients_edit.phone_number=phone_number
                patients_edit.first_name = first_name
                patients_edit.last_name = last_name


                
                patients_edit.save()
                messages.success(request, "Patient Updated Successfully!")
                return redirect('all_patients')
            except:
                messages.success(request, "Failed to Update Patient.")
                return redirect('all_patients')


    context = {
        "id": patient_id,
        # "username": patient.admin.username,
        "form": form,
        "title":"Edit Patient"
    }
    return render(request, "hod_templates/edit_patient.html", context)


       

    
@login_required
@user_passes_test(is_admin, login_url='denied')
def patient_personalRecords(request,pk):
    patient=Patients.objects.get(id=pk)
    prescrip=patient.prescription_set.all()
    inventorys=patient.dispense_set.all()

    context={
        "patient":patient,
        "prescription":prescrip,
        "inventorys":inventorys

    }
    return render(request,'hod_templates/patient_personalRecords.html',context)

@login_required
@user_passes_test(is_admin, login_url='denied')
def deletePrescription(request,pk):
    prescribe=Prescription.objects.get(id=pk)
    if request.method == 'POST':
        prescribe.delete()
        return redirect('all_patients')

    context={
        "patient":prescribe
    }

    return render(request,'hod_templates/sure_delete.html',context)


@login_required
@user_passes_test(is_admin, login_url='denied')
def hodProfile(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    staff=AdminHOD.objects.get(admin=customuser.id)


    form=HodForm()
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
       
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name=last_name
        customuser.save()

        staff=AdminHOD.objects.get(admin=customuser.id)
        form =HodForm(request.POST,request.FILES,instance=staff)
        staff.address = address
       
        staff.mobile=mobile
        staff.save()

        if form.is_valid():
            form.save()

    context={
        "form":form,
        "staff":staff,
        "user":customuser
    }

    return render(request,'hod_templates/hod_profile.html',context)

@login_required
@user_passes_test(is_admin, login_url='denied')
def deleteDoctor(request,pk):
    try:
        doctor=Doctor.objects.get(id=pk)
        if request.method == 'POST':
            doctor.delete()
            messages.success(request, "Doctor  deleted successfully")

            return redirect('manage_doctor')

    except:
        messages.error(request, "Doctor aready deleted")
        return redirect('manage_doctor')


   
    return render(request,'hod_templates/sure_delete.html')
    
@login_required
@user_passes_test(is_admin, login_url='denied')
def deletePharmacist(request,pk):
    try:
        pharmacist=Pharmacist.objects.get(id=pk)
        if request.method == 'POST':
            pharmacist.delete()
            messages.success(request, "Pharmacist  deleted successfully")
                
            return redirect('manage_pharmacist')

    except:
        messages.error(request, "Pharmacist aready deleted")
        return redirect('manage_pharmacist')


   
    return render(request,'hod_templates/sure_delete.html')


@login_required
@user_passes_test(is_admin, login_url='denied')
def editPharmacist(request,staff_id):
    staff = Pharmacist.objects.get(admin=staff_id)
    if request.method == "POST":
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

            # INSERTING into Customuser Model
        user = CustomUser.objects.get(id=staff_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()
        
        # INSERTING into Staff Model
        staff = Pharmacist.objects.get(admin=staff_id)
        staff.address = address
        staff.save()

        messages.success(request, "Staff Updated Successfully.")
        return redirect('manage_pharmacist')
    context = {
        "staff": staff,
        "id": staff_id,
        'title':"Edit Pharmacist "

    }
    return render(request, "hod_templates/edit_pharmacist.html", context)


@login_required
@user_passes_test(is_admin, login_url='denied')
def editDoctor(request,doctor_id):
    staff = Doctor.objects.get(admin=doctor_id)
    if request.method == "POST":
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

            # INSERTING into Customuser Model
        user = CustomUser.objects.get(id=doctor_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()
        
        # INSERTING into Staff Model
        staff = Doctor.objects.get(admin=doctor_id)
        staff.address = address
        staff.save()

        messages.success(request, "Staff Updated Successfully.")

    context = {
        "staff": staff,
        "title":"Edit Doctor"
    }
    return render(request, "hod_templates/edit_doctor.html", context)


@login_required
@user_passes_test(is_admin, login_url='denied')
def editAdmin(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    staff=AdminHOD.objects.get(admin=customuser.id)


    form=HodForm()
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
       
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name=last_name
        customuser.save()

        staff=AdminHOD.objects.get(admin=customuser.id)
        form =HodForm(request.POST,request.FILES,instance=staff)
        staff.address = address
       
        staff.mobile=mobile
        staff.save()

        if form.is_valid():
            form.save()

    context={
        "form":form,
        "staff":staff,
        "user":customuser
    }

    return render(request,'hod_templates/edit-profile.html',context)


@login_required
@user_passes_test(is_admin, login_url='denied')
def editInventory(request,pk):
    drugs=Inventory.objects.get(id=pk)
    form=InventoryForm(request.POST or None,instance=drugs)

    if request.method == "POST":
        if form.is_valid():
            form=InventoryForm(request.POST or None ,instance=drugs)

            category=request.POST.get('category')
            drug_name=request.POST.get('drug_name')
            quantity=request.POST.get('quantity')
            # email=request.POST.get('email')

            try:
                drugs =Inventory.objects.get(id=pk)
                drugs.drug_name=drug_name
                drugs.quantity=quantity
                drugs.save()
                form.save()
                messages.success(request,'Receptionist Updated Succefully')
            except:
                messages.error(request,'An Error Was Encounterd Receptionist Not Updated')


        
    context={
        "drugs":drugs,
         "form":form,
         "title":"Edit Inventory"

    }
    return render(request,'hod_templates/edit_drug.html',context)


@login_required
@user_passes_test(is_admin, login_url='denied')
def deleteDrug(request,pk):
    try:
    
        drugs=Inventory.objects.get(id=pk)
        if request.method == 'POST':
        
            drugs.delete()
            messages.success(request, "Pharmacist  deleted successfully")
                
            return redirect('manage_inventory')

    except:
        messages.error(request, "Pharmacist aready deleted")
        return redirect('manage_inventory')



    return render(request,'hod_templates/sure_delete.html')

@login_required
@user_passes_test(is_admin, login_url='denied')
def receiveDrug(request,pk):
    receive=Inventory.objects.get(id=pk)
    form=ReceiveInventoryForm()
    try:
        form=ReceiveInventoryForm(request.POST or None )

        if form.is_valid():
            form=ReceiveInventoryForm(request.POST or None ,instance=receive)

            instance=form.save(commit=False) 
            instance.quantity+=instance.receive_quantity
            instance.save()
            form=ReceiveInventoryForm()

            messages.success(request, str(instance.receive_quantity) + " " + instance.drug_name +" "+ "drugs added successfully")

            return redirect('manage_inventory')

      
    except:
        messages.error(request,"An Error occured, Drug quantity Not added")
                
        return redirect('manage_inventory')
    context={
            "form":form,
            "title":"Add Drug"
            
        }
    return render(request,'hod_templates/modal_form.html',context)



@login_required
@user_passes_test(is_admin, login_url='denied')
def drugDetails(request,pk):
    inventorys=Inventory.objects.get(id=pk)
    # prescrip=inventorys.prescription_set.all()
    # inventorys=inventorys.dispense_set.all()

    context={
        "inventorys":inventorys,
        # "prescription":prescrip,
        # "inventorys":inventorys

    }
    return render(request,'hod_templates/view_drug.html',context)
