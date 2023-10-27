from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class PatientsAdmin(admin.ModelAdmin):
    #list_display = ('admin','sex','age','mobile','address','profile_pic')
    search_fields = ["admin__username"]
class UserModel(UserAdmin):
    pass
admin.site.register(CustomUser, UserModel)
admin.site.register(Patients,PatientsAdmin)
admin.site.register(Pharmacist)
admin.site.register(AdminHOD)
admin.site.register(Inventory)
admin.site.register(Category)
admin.site.register(Doctor)
admin.site.register(Prescription)
admin.site.register(Dispense)
admin.site.register(Drug)



   



 



