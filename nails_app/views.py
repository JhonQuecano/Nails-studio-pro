from django.shortcuts import render, redirect

from .models import MensajeContacto
# Create your views here.

def home(request):
    return render(request, 'home.html')

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