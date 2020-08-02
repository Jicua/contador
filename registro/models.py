from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Cliente(models.Model):
	rut		= models.CharField(max_length=10, blank=False, null=False)
	nombre	= models.CharField(max_length=255, blank=False, null=False)

	def __str__(self):
		return self.nombre

	def get_absolute_url(self):
		return reverse("cliente-detalle", kwargs={"id": self.id})

	def get_edit_url(self):
		return reverse("cliente-editar", kwargs={"id": self.id})

class Tipo(models.Model):
	nombre	= models.CharField(max_length=40, blank=False, null=False)

	def __str__(self):
		return self.nombre
		
	def get_absolute_url(self):
		return reverse("tipo-detalle", kwargs={"id": self.id})

	def get_edit_url(self):
		return reverse("tipo-editar", kwargs={"id": self.id})

class Trabajo(models.Model):
	contador		= models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=True, on_delete=models.SET_NULL)
	cliente			= models.ForeignKey(Cliente, blank=False, null=True, on_delete=models.SET_NULL)
	tipo			= models.ForeignKey(Tipo, blank=False, null=True, on_delete=models.SET_NULL)
	fecha_inicio	= models.DateTimeField(blank=False, null=False)
	duracion		= models.TimeField(blank=True, null=True)
	descripcion		= models.TextField(blank=True, null=True)

	def get_absolute_url(self):
		return reverse("trabajo-detalle", kwargs={"id": self.id})

	def get_edit_url(self):
		return reverse("trabajo-editar", kwargs={"id": self.id})
		