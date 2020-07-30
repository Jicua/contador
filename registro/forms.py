from django import forms
from .models import Cliente, Tipo, Trabajo
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

class ClienteForm(forms.ModelForm):
	class Meta:
		model = Cliente
		fields = [
			'rut',
			'nombre',
		]

class TipoForm(forms.ModelForm):
	class Meta:
		model = Tipo
		fields = [
			'nombre',
		]

class TrabajoForm(forms.ModelForm):
	class Meta:
		model = Trabajo
		fields = [
			'contador',
			'cliente',
			'tipo',
			'fecha_inicio',
			'duracion',
			'descripcion',
		]
		widgets = {
			'fecha_inicio': DateTimePicker(),
			'duracion': TimePicker(
					options={
						'format': "LT"
					}
				),
		}