from django.db import models
from django.contrib.auth.models import AbstractUser
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    asunto = models.CharField(max_length=150, blank=True)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"

class Rol(models.Model):
    code = models.CharField(max_length=10, unique=True,null=False, default= 'ADMIN') 
    name = models.CharField(max_length=50, unique=True,null=False, default= 'ADMINISTRADOR')
    order = models.PositiveIntegerField(default=0)
    
class Usuario(AbstractUser):
    TIPO_DOC = [
        ('TI','Tarjeta de identidad'),
        ('CC','Cedula de ciudadania'),
        ('CE', 'Cedula de extranjeria'),
        ('OT', 'Otro'),
    ]
    tipo_doc = models.CharField(max_length=2, choices=TIPO_DOC, default='CC')
    document = models.CharField(max_length=15, unique=True, default="")
    phone = models.CharField(max_length=10, blank=True, null=True)
    rol = models.ForeignKey('Rol', on_delete= models.PROTECT )
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        
    def __str__(self):
        return self.username
    


