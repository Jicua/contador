from django import forms
from .models import Cliente, Tipo, Trabajo
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2', )

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
						'stepping': 1,
					},
					attrs={
						'append': 'fa fa-calendar',
						'icon_toggle': True,
					}
				),
			'duracion': TimePicker(
					options={
						'format': "H:mm",
						'stepping': 5,
						'defaultDate': '1970-01-01T00:00:00'
					},
					attrs={
						'required': True,
						'append': 'fa fa-clock-o',
					},	
				),
			'descripcion': forms.Textarea(
					attrs={
						'rows': 3,
						'cols': 21
					}
				),

		}