from django.shortcuts import render, redirect, get_object_or_404
from nails_app.models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
import json
# Create your views here.

def home(request):
    return render(request, 'home.html')

# Redireccion de usuario según su rol
@login_required
def redireccionar_usuario(request):
    usuario = request.user

    if usuario.rol.codigo == 'ADMIN':  # Administrador
        return render(request, 'admin.html', {'usuario': usuario})
    
    elif usuario.rol.codigo == 'MAN':  # Manicurista
        return render(request, 'manicurista.html', {'usuario': usuario})
    
    elif usuario.rol.codigo == 'PEL':  # Peluquer@
        return render(request, 'peluquero.html', {'usuario': usuario})
    
    elif usuario.rol.codigo == 'EST':  # Estilista
        return render(request, 'estilista.html', {'usuario': usuario})
    else:
        return render(request, 'home.html', {'usuario': usuario})  # Para roles no definidos
    
# Actualizar el orden de los roles
@csrf_exempt
def update_rol_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        for index, rol_id in enumerate(data['order']):
            Rol.objects.filter(id=rol_id).update(order=index + 1)

        return JsonResponse({'status': 'ok'})
    
# Funciones para ingresar un usuario
    
def insert_user(request):
    if request.method == 'POST':
        if (request.POST.get('tipo_doc')
        and request.POST.get('document')
        and request.POST.get('first_name')
        and request.POST.get('last_name')
        and request.POST.get('username')
        and request.POST.get('email')
        and request.POST.get('password')
        and request.POST.get('phone')
        and request.POST.get('rol_id')):
            
            usuario = Usuario.objects.create_user(
            
                tipo_doc = request.POST.get('tipo_doc'),
                document = request.POST.get('document'),
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                username = request.POST.get('username'),
                email = request.POST.get('email'),
                password = request.POST.get('password'),
                phone = request.POST.get('phone'),
                
                rol=Rol.objects.get(id=request.POST.get('rol_id'))
            )
            return redirect('list_user')
            
    else:
        roles = Rol.objects.all()
        return render(request, "user/register.html", {'roles': roles})
    
#Listar todos los usuarios    
def list_user(request):
    usuarios = Usuario.objects.all()
    return render(request, "user/list.html", {'usuarios': usuarios})

# Eliminar un usuario
def delete_user(request, id):
    usuario=get_object_or_404(Usuario,id=id)
    usuario.delete()
    return redirect("list_user")

# Actualizar un usuario
def update_user(request, id):
    usuario=get_object_or_404(Usuario,id=id)
    roles = Rol.objects.all()
    if request.method == 'POST': 
        usuario.tipo_doc = request.POST.get('tipo_doc')
        usuario.document = request.POST.get('document')
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.set_password(request.POST.get('password'))
        usuario.phone = request.POST.get('phone')
        usuario.rol_id = request.POST.get('rol_id')
            
        usuario.save()
        return redirect("list_user")
    
    else:
        return render(request, 'user/update.html', {'usuario': usuario, 'roles': roles})


# Función para iniciar sesión

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('redireccion_usuario')  # Redirige según el rol
        else:
            messages.error(request, 'Credenciales incorrectas, intente de nuevo')

    return render(request, 'user/login.html')

#Funcion para cerrar sesion
def logout_user(request): 
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


 #Funcion para insertar un rol
def insert_rol(request):
    if request.method == 'POST':
        try:
            last_order = Rol.objects.aggregate(
                max_order=models.Max('order')
            )['max_order'] or 0

            Rol.objects.create(
                name=request.POST.get('name'),
                code=request.POST.get('code'),
                order=last_order + 1
            )

            return redirect('list_rol')

        except IntegrityError:
            messages.error(request, '❌ El código o nombre ya existe')

    return render(request, 'rol/insert.html')

# Listar todos los roles
def list_rol(request):
    roles = Rol.objects.all().order_by('order')
    return render(request, 'rol/list.html', {'roles': roles})

# Reordenar roles
def reorder_roles():
    roles = Rol.objects.all().order_by('order', 'id')
    for index, rol in enumerate(roles, start=1):
        if rol.order != index:
            rol.order = index
            rol.save(update_fields=['order'])


# Eliminar un rol
def delete_rol(request, id):
    rol=get_object_or_404(Rol,id=id)
    rol.delete()
    reorder_roles()
    return redirect("list_rol")

# Actualizar un rol
def update_rol(request, id):
    rol = get_object_or_404(Rol, id=id)

    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('code'):
            rol.name = request.POST.get('name')
            rol.code = request.POST.get('code')
            rol.save()
            return redirect('list_rol')

    return render(request, 'rol/update.html', {'rol': rol})
        
def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        MensajeContacto.objects.create(
            nombre=nombre,
            correo=correo,
            asunto=asunto,
            mensaje=mensaje
        )

        return redirect('contacto')  

    return render(request, 'contactanos.html')

