from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Cliente, Tipo, Trabajo
from .forms import ClienteForm, TipoForm, TrabajoForm
from datetime import datetime


# Create your views here.

@login_required()
def inicio(request):
	user = request.user
	queryset = Trabajo.objects.filter(contador=user)
	context = {
		"trabajos": queryset,
	}
	return render(request, 'registro/inicio.html')

@login_required()
def crearUsuario(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
	else:
		form = UserCreationForm()
	context = {
		'form': form,
	}
	return render(request, 'registro/crear-usuario.html', context)

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
		"clientes": queryset
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
def tipo_list_view(request):
	queryset = Tipo.objects.all()
	context = {
		"tipos": queryset
	}
	return render(request, "registro/tipo/list.html", context)

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

################ TRABAJO ################

@login_required()
def trabajo_create_view(request):
	initial_data = {
		'fecha_inicio': datetime.now().strftime("%d-%m-%Y"),
	}
	form = TrabajoForm(request.POST or None, initial_data)
	form.initial['contador'] = request.user
	if form.is_valid():
		form.save()
	context = {
		'form': form,
	}
	print(form.errors)
	return render(request, 'registro/trabajo/create.html', context)

