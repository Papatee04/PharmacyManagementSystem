from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import  UserCreationForm
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .utils import *
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.utils.timezone import datetime 
from django.http import JsonResponse


@login_required
@user_passes_test(is_pharmacist, login_url='denied')
def pharmacistHome(request):
    patients_total=Patients.objects.all().count()
    today = datetime.today()
    expired_drugs = Inventory.objects.filter(valid_to__lt=today)
    expired_count = expired_drugs.count()
    distribted_drugs = Dispense.objects.count()
 
    out_of_inventory=Inventory.objects.filter(quantity__lte=0).count()
    total_inventory=Inventory.objects.all().count()

    context={
"patients_total":patients_total,
        "expired_total":expired_count,
        "out_of_inventory":out_of_inventory,
        "total_drugs":total_inventory,
        "distribted_drugs":distribted_drugs
    }
    return render(request,'pharmacist_templates/pharmacist_home.html',context)

@login_required
@user_passes_test(is_pharmacist, login_url='denied')
def userProfile(request):
    staff=Pharmacist.objects.all()
    form=CustomerForm()
    if request.method == "POST":
       

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

      
        customuser = CustomUser.objects.get(id=request.user.id)
        customuser.first_name = first_name
        customuser.last_name = last_name
        
        customuser.save()
        staff = Pharmacist.objects.get(admin=customuser.id)
        form=CustomerForm(request.POST,request.FILES,instance=staff)

        staff.address = address
        if form.is_valid():
            form.save()
        staff.save()
        
        messages.success(request, "Profile Updated Successfully")
        return redirect('pharmacist_profile')

    context={
        "staff":staff,
        "form":form
    }
      

    return render(request,'pharmacist_templates/staff_profile.html',context)

@login_required
@user_passes_test(is_pharmacist, login_url='denied')
def managePatientsPharmacist(request):
   
    patient=Patients.objects.all()
    context={
        "patients":patient
    }
    return render(request,'pharmacist_templates/manage_patients.html',context)



@login_required
@user_passes_test(is_pharmacist, login_url='denied')
def managePrescription(request):
    precrip=Dispense.objects.all()

    context={
        "prescrips":precrip,
    }
    return render(request,'pharmacist_templates/patient_prescrip.html',context)


    
@login_required
@user_passes_test(is_pharmacist, login_url='denied')
def manageInventory(request):
    inventorys = Inventory.objects.all()
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

    }
    return render(request,'pharmacist_templates/manage_stock.html',context)


@login_required
@user_passes_test(is_pharmacist, login_url='denied')
def manageDispense(request, pk):
    queryset = Patients.objects.get(id=pk)

    # Retrieve all prescriptions related to the selected patient
    prescrips = Prescription.objects.filter(patient_id=queryset)

    form = DispenseForm(request.POST, initial={'patient_id': queryset}) if request.method == 'POST' else DispenseForm(initial={'patient_id': queryset})

    if request.method == 'POST':
        print('POST')
        print(request.POST)

        if form.is_valid():
            dispense_quantity = form.cleaned_data['dispense_quantity']
            drug = form.cleaned_data['drug']
            prescription = request.POST['prescription']
            form.instance.prescription = prescription

            # Check if there's enough quantity in the selected drug's inventory
            if drug.inventory.quantity >= dispense_quantity:
                # Subtract the dispensed quantity from inventory
                drug.inventory.quantity -= dispense_quantity
                drug.inventory.save()

                # Save the dispense record
                instance = form.save()
                instance.save()
                messages.success(request, "Drug Has been Successfully Distributed")
            else:
                messages.error(request, "Not enough quantity in inventory to dispense")
        else:
            print("Validity Error") 
            messages.error(request, "Validity Error")

    # Filter drugs to show only those that are not expired
    drugs = Inventory.objects.filter(
        valid_to__gt=timezone.now(),
        expired=False
    )

    ex = Inventory.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True)
    eo = Inventory.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=False)

    context = {
        "patients": queryset,
        "form": form,
        "drugs": drugs,
        "prescrips": prescrips,
        "expired": ex,
        "expa": eo,
    }

    return render(request, 'pharmacist_templates/manage_dispense.html', context)





@login_required
@user_passes_test(is_pharmacist, login_url='denied')
def drugDetails(request,pk):
    inventorys=Inventory.objects.get(id=pk)
    context={
        "inventorys":inventorys,
       

    }
    return render(request,'pharmacist_templates/view_drug.html',context)



@login_required
@user_passes_test(is_pharmacist, login_url='denied')
def deleteDispense4(request,pk):
    try:
        fed=Dispense.objects.get(id=pk)
        if request.method == 'POST':
            fed.delete()
            messages.success(request, "Dispense  deleted successfully")
            return redirect('pharmacist_prescription')

    except:
        messages.error(request, "Delete Error, Please Check again")
        return redirect('pharmacist_prescription')


   
    return render(request,'pharmacist_templates/sure_delete.html')
    




@login_required
@user_passes_test(is_pharmacist, login_url='denied')
def dispenseDrug(request,pk):
     queryset=Patients.objects.get(id=pk)
     form=DispenseForm(initial={'patient_id':queryset})
     if request.method == 'POST':
         form=DispenseForm(request.POST or None)
         if form.is_valid():
             form.save()
            
    
     context={
         # "title":' Issue' + str(queryset.item_name),
         "queryset":queryset,
         "form":form,
         # "username":" Issue By" + str(request.user),
     }
     return render(request,"pharmacist_templates/dispense_drug.html",context)

#def manageDispense(request):
     #disp=De.objects.all()
     #context={
         #"prescrips":disp,
     
     #return render(request,'pharmacist_templates/manage_dispense.html',context)




@login_required
@user_passes_test(is_pharmacist, login_url='denied')
def dispense(request, pk):
    queryset = Inventory.objects.get(id=pk)
    form = DispenseForm2(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.dispense_quantity
        print(instance.drug.quantity)
        print(instance.dispense_quantity)
        instance.save()

        return redirect('pharmacist_disp')

    context = {
        "queryset": queryset,
        "form": form,
    }
    return render(request, 'pharmacist_templates/dispense_form.html', context)

