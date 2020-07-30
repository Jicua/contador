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
			'fecha_inicio': DateTimePicker(
					options={
						'format': "DD/MM/YYYY H:mm",
						'stepping': 5,
					}
				),
			'duracion': TimePicker(
					options={
						'format': "H:mm",
						'stepping': 5,
					}
				),
			'descripcion': forms.Textarea(
					attrs={
					'rows': 3,
					'cols': 21
					}
				),
		}