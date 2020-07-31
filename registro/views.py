from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Cliente, Tipo, Trabajo
from .forms import ClienteForm, TipoForm, TrabajoForm, SignUpForm
from datetime import datetime, timedelta
from django.db.models import Sum


from django.contrib.auth.models import User


# Create your views here.

@login_required()
def inicio(request):
	contador = request.user
	queryset = Trabajo.objects.all().filter(contador=contador, fecha_inicio__gt=datetime.today()-timedelta(days=2)).order_by('fecha_inicio').reverse()
	context = {
		"trabajos": queryset,
	}
	return render(request, 'registro/inicio.html', context)



################ CONTADORES ################

@login_required()
def contador_create_view(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
	else:
		form = SignUpForm()
	context = {
		'form': form,
	}
	return render(request, 'registro/contador/create.html', context)

@login_required()
def contador_list_view(request):
	queryset = User.objects.all()
	context = {
		"contadores": queryset,
	}
	return render(request, "registro/contador/list.html", context)

@login_required()
def contador_detail_view(request, id):
	obj = get_object_or_404(User, id=id)
	duracion = Trabajo.objects.values_list('duracion', flat=True).filter(contador=id)
	i = horas = minutos = 0
	for d in duracion:
		horas += d.hour
		minutos += d.minute
	i = minutos // 60
	horas += i
	minutos -= i*60
	context = {
		"contador": obj,
		"horas": horas,
		"minutos": minutos,
	}
	return render(request, "registro/contador/detail.html", context)
################ CLIENTE ################

@login_required()
def cliente_create_view(request):
	form = ClienteForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/registro/clientes')
	context = {
		'form': form,
	}
	return render(request, 'registro/cliente/create.html', context)

@login_required()
def cliente_list_view(request):
	queryset = Cliente.objects.all()
	context = {
		"clientes": queryset,
	}
	return render(request, "registro/cliente/list.html", context)

@login_required()
def cliente_detail_view(request, id):
	obj = get_object_or_404(Cliente, id=id)
	context = {
		"cliente": obj,
	}
	return render(request, "registro/cliente/detail.html", context)

################ TIPO ################

@login_required()
def tipo_create_view(request):
	form = TipoForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/registro/tipos')
	context = {
		'form': form,
	}
	return render(request, 'registro/tipo/create.html', context)

@login_required()
def tipo_list_view(request):
	queryset = Tipo.objects.all()
	context = {
		"tipos": queryset
	}
	return render(request, "registro/tipo/list.html", context)

@login_required()
def tipo_detail_view(request, id):
	obj = get_object_or_404(Tipo, id=id)
	context = {
		"tipo": obj,
	}
	return render(request, "registro/tipo/detail.html", context)

################ TRABAJO ################

@login_required()
def trabajo_create_view(request):
	form = TrabajoForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/registro/')
	context = {
		'form': form,
	}
	print(form.errors)
	return render(request, 'registro/trabajo/create.html', context)

@login_required()
def trabajo_list_view(request):
	contador = request.user
	queryset = Trabajo.objects.all().filter(contador=contador).order_by('fecha_inicio').reverse()
	context = {
		'trabajos': queryset,
	}
	return render(request, "registro/trabajo/list.html", context)

@login_required()
def trabajo_detail_view(request, id):
	obj = get_object_or_404(Trabajo, id=id)
	context = {
		"trabajo": obj,
	}
	return render(request, "registro/trabajo/detail.html", context)