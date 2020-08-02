from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from datetime import datetime, timedelta

from .models import Cliente, Tipo, Trabajo
from .forms import ClienteForm, TipoForm, TrabajoForm, SignUpForm

import xlwt

# Create your views here.

@login_required
def inicio(request):
	contador = request.user
	queryset = Trabajo.objects.all().filter(contador=contador, fecha_inicio__gt=datetime.today()-timedelta(days=2)).order_by('fecha_inicio').reverse()
	today = datetime.today()
	trabajosHoy = Trabajo.objects.all().filter(contador=contador, fecha_inicio__year=today.year, fecha_inicio__month=today.month, fecha_inicio__day=today.day).order_by('fecha_inicio')
	
	context = {
		"trabajos": queryset,
		"trabajosHoy": trabajosHoy,
		"title": "Inicio",
	}
	return render(request, 'registro/inicio.html', context)

################ CONTADORES ################

@staff_member_required
def contador_create_view(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/registro/contadores/')
	else:
		form = SignUpForm()
	context = {
		'form': form,
		"title": "Nuevo contador"
	}
	return render(request, 'registro/contador/create.html', context)

@staff_member_required
def contador_update_view(request, id):
	obj = get_object_or_404(User, id=id)
	if request.method == "POST":
		form = UserChangeForm(request.POST, instance=obj)
		if form.is_valid():
			form.save()
			return redirect('registro/contador/' + obj.id)
	else:
		form = UserChangeForm(instance=obj)
		context = {
			"form": form,
			"title": "Editar contador"
		}
		return render(request, "registro/contador/edit.html", context)

@staff_member_required
def contador_list_view(request):
	queryset = User.objects.all()
	horas = []
	for contador in queryset:
		horas.append(contar_horas(contador))
	context = {
		"contadores": queryset,
		"horas": horas,
		"title": "Contadores",
	}
	return render(request, "registro/contador/list.html", context)

def contar_horas(contador):
	duracion = Trabajo.objects.values_list('duracion', flat=True).filter(contador=contador)
	i = horas = minutos = 0
	for d in duracion:
		horas += d.hour
		minutos += d.minute
	i = minutos // 60
	horas += i
	minutos -= i*60
	final = (str(horas) + ":" + str(minutos))
	return final

def contar_horas_cliente(cliente, contador):
	duracion = Trabajo.objects.values_list('duracion', flat=True).filter(cliente=cliente, contador=contador)
	i = horas = minutos = 0
	for d in duracion:
		horas += d.hour
		minutos += d.minute
	i = minutos // 60
	horas += i
	minutos -= i*60
	final = (str(horas) + ":" + str(minutos))
	return final

def contar_horas_tipo(tipo, contador):
	duracion = Trabajo.objects.values_list('duracion', flat=True).filter(tipo=tipo, contador=contador)
	i = horas = minutos = 0
	for d in duracion:
		horas += d.hour
		minutos += d.minute
	i = minutos // 60
	horas += i
	minutos -= i*60
	final = (str(horas) + ":" + str(minutos))
	return final

def contar_horas_tipo_cliente(tipo, cliente):
	duracion = Trabajo.objects.values_list('duracion', flat=True).filter(tipo=tipo, cliente=cliente)
	i = horas = minutos = 0
	for d in duracion:
		horas += d.hour
		minutos += d.minute
	i = minutos // 60
	horas += i
	minutos -= i*60
	final = (str(horas) + ":" + str(minutos))
	return final

@staff_member_required
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

	queryset = Trabajo.objects.all().filter(contador=id).order_by('fecha_inicio').reverse()
	clientes = Cliente.objects.all()
	tipos = Tipo.objects.all()

	buscaCliente = None
	horasCliente = "";
	if request.GET.get('cliente'):
		buscaCliente = request.GET.get('cliente')
		cliente = Cliente.objects.filter(nombre=buscaCliente).first()
		horasCliente = contar_horas_cliente(cliente, id)

	buscaTipo = None
	horasTipo = "";
	if request.GET.get('tipo'):
		buscaTipo = request.GET.get('tipo')
		tipo = Tipo.objects.filter(nombre=buscaTipo).first()
		horasTipo = contar_horas_tipo(tipo, id)

	context = {
		"contador": obj,
		"horas": horas,
		"minutos": minutos,
		"trabajos": queryset,
		"clientes": clientes,
		"tipos": tipos,
		"horasCliente": horasCliente,
		"cliente": buscaCliente,
		"horasTipo": horasTipo,
		"tipo": buscaTipo,
		"title": obj.first_name,
	}
	return render(request, "registro/contador/detail.html", context)
################ CLIENTE ################

@login_required
def cliente_create_view(request):
	form = ClienteForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/registro/clientes')
	context = {
		'form': form,
		"title": "Nuevo cliente",
	}
	return render(request, 'registro/cliente/create.html', context)

@login_required
def cliente_list_view(request):
	queryset = Cliente.objects.all()
	context = {
		"clientes": queryset,
		"title": "Clientes",
	}
	return render(request, "registro/cliente/list.html", context)

@login_required
def cliente_detail_view(request, id):
	obj = get_object_or_404(Cliente, id=id)
	queryset = Trabajo.objects.all().filter(cliente=id).order_by('fecha_inicio').reverse()
	contadores = User.objects.all()
	tipos = Tipo.objects.all()

	buscaContador = None
	horasContador = ""
	if request.GET.get('contador'):
		buscaContador = request.GET.get('contador')
		contador = User.objects.filter(first_name=buscaContador).first()
		horasContador = contar_horas_cliente(id, contador)

	buscaTipo = None
	horasTipo = "";
	if request.GET.get('tipo'):
		buscaTipo = request.GET.get('tipo')
		tipo = Tipo.objects.filter(nombre=buscaTipo).first()
		horasTipo = contar_horas_tipo_cliente(tipo, id)

	context = {
		"cliente": obj,
		"trabajos": queryset,
		"contadores": contadores,
		"tipos": tipos,
		"horasContador": horasContador,
		"contador": buscaContador,
		"horasTipo": horasTipo,
		"tipo": buscaTipo,
		"title": obj.nombre,
	}
	return render(request, "registro/cliente/detail.html", context)

@login_required
def cliente_update_view(request, id):
	obj = get_object_or_404(Cliente, id=id)
	form = ClienteForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
		return redirect('/registro/clientes/')
	context = {
		"form": form,
		"title": "Editar cliente",
	}
	return render(request, "registro/cliente/create.html", context)

################ TIPO ################

@login_required
def tipo_create_view(request):
	form = TipoForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/registro/tipos')
	context = {
		'form': form,
		"title": "Nuevo tipo de trabajo",
	}
	return render(request, 'registro/tipo/create.html', context)

@login_required
def tipo_update_view(request, id):
	obj = get_object_or_404(Tipo, id=id)
	form = TipoForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
		return redirect('/registro/tipos/')
	context = {
		"form": form,
		"title": "Editar tipo de trabajo",
	}
	return render(request, "registro/tipo/create.html", context)

@login_required
def tipo_list_view(request):
	queryset = Tipo.objects.all()
	context = {
		"tipos": queryset,
		"title": "Tipos de trabajo",
	}
	return render(request, "registro/tipo/list.html", context)

@login_required
def tipo_detail_view(request, id):
	obj = get_object_or_404(Tipo, id=id)
	context = {
		"tipo": obj,
	}
	return render(request, "registro/tipo/detail.html", context)

################ TRABAJO ################

@login_required
def trabajo_create_view(request):
	form = TrabajoForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/registro/')
	context = {
		'form': form,
		"title": "Nuevo trabajo"
	}
	print(form.errors)
	return render(request, 'registro/trabajo/create.html', context)

@login_required
def trabajo_update_view(request, id):
	obj = get_object_or_404(Trabajo, id=id)
	form = TrabajoForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
		return redirect(obj.get_absolute_url())
	context = {
		"form": form,
		"title": "Editar trabajo"
	}
	return render(request, "registro/trabajo/create.html", context)

@login_required
def trabajo_list_view(request):
	contador = request.user
	queryset = Trabajo.objects.all().filter(contador=contador).order_by('fecha_inicio').reverse()
	context = {
		'trabajos': queryset,
		"title": "Mis trabajos",
	}
	return render(request, "registro/trabajo/list.html", context)

@login_required
def trabajo_detail_view(request, id):
	obj = get_object_or_404(Trabajo, id=id)
	context = {
		"trabajo": obj,
	}
	return render(request, "registro/trabajo/detail.html", context)

@staff_member_required
def trabajo_todos_view(request):
	queryset = Trabajo.objects.all().order_by('fecha_inicio').reverse()
	context = {
		"trabajos": queryset,
		"title": "Trabajos",
	}
	return render(request, "registro/trabajo/todos.html", context)

def trabajo_to_excel(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="trabajos.xls"'
	wb = xlwt.Workbook(encoding="utf-8")
	ws = wb.add_sheet('Trabajos')
	# Sheet header, first row
	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True
	columns = ['Fecha de inicio', 'Duración', 'Contador', 'Cliente', 'Tipo', 'Descripcion']
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
	# Sheet body, remaining rows
	font_style = fecha_style = duracion_style = xlwt.XFStyle()
	rows = Trabajo.objects.all().values_list('fecha_inicio', 'duracion', 'contador__first_name', 'cliente__nombre', 'tipo__nombre', 'descripcion')
	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			if col_num == 0:
				fecha_style.num_format_str = 'dd/mm/yyyy hh:mm'
				ws.write(row_num, col_num, row[col_num], fecha_style)
			elif col_num == 1:
				duracion_style.num_format_str = 'hh:mm'
				ws.write(row_num, col_num, row[col_num], duracion_style)
			else:
				ws.write(row_num, col_num, row[col_num], font_style)
	wb.save(response)
	return response
