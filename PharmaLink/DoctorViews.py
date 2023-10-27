from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import  UserCreationForm
from .decorators import *
from django.contrib.auth.decorators import login_required
from .utils import *
from django.contrib.auth.decorators import user_passes_test
from .forms import *
from .models import *

@login_required
@user_passes_test(is_doctor, login_url='denied')
def doctorHome(request): 
    prescip = Prescription.objects.all().count()

    context={
        "Prescription_total":prescip

    }
    return render(request,'doctor_templates/doctor_home.html',context)

@login_required
@user_passes_test(is_doctor, login_url='denied')
def doctorProfile(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    staff=Doctor.objects.get(admin=customuser.id)

    form=DoctorForm()
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')


        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name=last_name
        customuser.save()

        staff=Doctor.objects.get(admin=customuser.id)
        form =DoctorForm(request.POST,request.FILES,instance=staff)

        staff.save()

        if form.is_valid():
            form.save()

    context={
        "form":form,
        "staff":staff,
        "user":customuser
    }

    return render(request,'doctor_templates/doctor_profile.html',context)

@login_required
@user_passes_test(is_doctor, login_url='denied')
def managePatients(request):
    patients=Patients.objects.all()

    context={
        "patients":patients,

    }
    return render(request,'doctor_templates/manage_patients.html',context)

@login_required
@user_passes_test(is_doctor, login_url='denied')
def addPrescription(request, pk):
    patient = Patients.objects.get(id=pk)
    
    if request.method == 'POST':
        try:
            form = PrescriptionForm(request.POST)
            
            # Assign the patient to the form instance
            form.instance.patient_id = patient
            
            if form.is_valid():
                # Get the logged-in doctor
                doctor = request.user.doctor  # Moved this line here

                # Associate the logged-in doctor with the doctor_issued field
                form.instance.doctor_issued = doctor

                form.save()
                messages.success(request, 'Prescription added successfully')
                return redirect('manage_precrip_doctor')
        except:
            messages.error(request, 'Prescription Not Added')
            return redirect('manage_patient-doctor')
    else:
        # Get the logged-in doctor and set it as the initial value for the field
        doctor = request.user.doctor
        form = PrescriptionForm(initial={'patient_id': patient, 'doctor_issued': doctor})
    
    context = {
        'form': form,
    }
    return render(request, 'doctor_templates/prescribe_form.html', context)




@login_required
@user_passes_test(is_doctor, login_url='denied')
def patient_personalDetails(request,pk):
    patient=Patients.objects.get(id=pk)
    prescrip=patient.prescription_set.all()

    context={
        "patient":patient,
        "prescription":prescrip

    }
    return render(request,'doctor_templates/patient_personalRecords.html',context)

@login_required
@user_passes_test(is_doctor, login_url='denied')
def deletePrescription(request,pk):
    prescribe=Prescription.objects.get(id=pk)

    if request.method == 'POST':
        try:
            prescribe.delete()
            messages.success(request,'Prescription Deleted successfully')
            return redirect('manage_precrip_doctor')
        except:
            messages.error(request,'Prescription Not Deleted successfully')
            return redirect('manage_precrip_doctor')




    context={
        "patient":prescribe
    }

    return render(request,'doctor_templates/sure_delete.html',context)
    
@login_required
@user_passes_test(is_doctor, login_url='denied')
def managePrescription(request):
    precrip=Prescription.objects.all()

    patient = Patients.objects.all()
    
       
    context={
        "prescrips":precrip,
        "patient":patient
    }
    return render(request,'doctor_templates/manage_prescription.html' ,context)

@login_required
@user_passes_test(is_doctor, login_url='denied')
def editPrescription(request,pk):
    prescribe=Prescription.objects.get(id=pk)
    form=PrescriptionForm(instance=prescribe)

    
    if request.method == 'POST':
        form=PrescriptionForm(request.POST ,instance=prescribe)

        try:
            if form.is_valid():
                form.save()

                messages.success(request,'Prescription Updated successfully')
                return redirect('manage_precrip_doctor')
        except:
            messages.error(request,' Error!! Prescription Not Updated')
            return redirect('manage_precrip_doctor')




    context={
        "patient":prescribe,
        "form":form
    }

    return render(request,'doctor_templates/edit_prescription.html',context)
    