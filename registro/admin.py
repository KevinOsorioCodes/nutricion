from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Profile

admin.site.register(Permission)

class ProfileAdmin(admin.ModelAdmin):
    list_display =("foto_perfil",)

admin.site.register(Profile,ProfileAdmin)
