from django.contrib import admin
from .models import Cliente, Tipo, Trabajo
# Register your models here.

admin.site.register(Cliente)
admin.site.register(Tipo)
admin.site.register(Trabajo)