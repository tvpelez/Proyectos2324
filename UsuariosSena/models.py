from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from .choices import (
    roles,
    cuentadantes,
    estado,
    categoriaElemento,
    tipoId,
    tipoContratos,
)
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import User


# Create your models here.


class UsuariosSenaManager(BaseUserManager):
    def create_user(self, numeroIdentificacion, email, password=None, **extra_fields):
        user = self.model(
            numeroIdentificacion=numeroIdentificacion,
            email=self.normalize_email(email),
            **extra_fields,
        )
        user = self.model(
            numeroIdentificacion=numeroIdentificacion,
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, numeroIdentificacion, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault(
            "cuentadante", "superAdmin"
        )  # Predeterminamos el tipo cuentadante al crear super User que quede como SuperAdmin en el aplicativo

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(numeroIdentificacion, email, password, **extra_fields)


class UsuariosSena(AbstractUser):
    nombres = models.CharField(max_length=25)
    apellidos = models.CharField(max_length=25)
    tipoIdentificacion = models.CharField(max_length=25, choices=tipoId, default="CC")
    numeroIdentificacion = models.CharField(
        max_length=25, unique=True, primary_key=True
    )
    email = models.EmailField(max_length=35)
    celular = models.CharField(max_length=10)
    rol = models.CharField(max_length=25, choices=roles, default="I")
    cuentadante = models.CharField(
        max_length=25, choices=cuentadantes, default="adminD"
    )
    tipoContrato = models.CharField(max_length=25, choices=tipoContratos, default="P")
    is_active = models.BooleanField(default=1)
    duracionContrato = models.CharField(max_length=25)
    password = models.CharField(max_length=100, default="")
    recovery_token = models.CharField(max_length=30, blank=True, null=True)
    fotoUsuario = models.ImageField(
        upload_to="usuarioFoto/", blank=True, null=True
    )  # Campo para la foto

    objects = UsuariosSenaManager()

    username = None
    last_name = None
    first_name = None

    # Set the node for log in
    USERNAME_FIELD = "numeroIdentificacion"


# ----Informacion General Producto (Repetitiva + Sumatoria Productos)---------------------------------------------------------------------------
class ProductosInventarioDevolutivo(models.Model):
    nombre = models.CharField(max_length=75)
    categoria = models.CharField(max_length=25, choices=categoriaElemento, default="C")
    estado = models.CharField(max_length=25, choices=estado, default="D")
    descripcion = models.CharField(max_length=255)
    valor_unidad = models.IntegerField()
    disponibles = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


# ----Informacion única Para El Inventario De Cada Unidad
class InventarioDevolutivo(models.Model):
    producto = models.ForeignKey(
        "ProductosInventarioDevolutivo", on_delete=models.CASCADE
    )
    fecha_Registro = models.DateField(auto_now_add=True)
    observacion = models.TextField()
    serial = models.CharField(max_length=25, primary_key=True)
    factura = models.ImageField(upload_to="facturaElemento/", blank=True, null=True)

    def __str__(self):
        return f"{self.serial}"


# -------------------------NORMALIZACION TABLA (ElementosConsumible)------------------------------------------------------
class ProductosInventarioConsumible(models.Model):
    nombreElemento = models.CharField(max_length=25)
    categoriaElemento = models.CharField(
        max_length=25,
        choices=[("Devolutivo", "Devolutivo"), ("Consumible", "Consumible")],
    )
    estadoElemento = models.CharField(
        max_length=25,
        choices=[
            ("Garantia", "Garantia"),
            ("Baja", "Baja"),
            ("Disponible", "Disponible"),
            ("Prestamo", "Prestamo"),
        ],
        default="Disponible",
    )
    descripcionElemento = models.CharField(max_length=25)
    costoUnidadElemento = models.IntegerField()
    disponible = models.IntegerField(default=0)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.nombreElemento



class InventarioConsumible(models.Model):
    productoConsumible = models.ForeignKey(
        ProductosInventarioConsumible, on_delete=models.CASCADE
    )
    fechaAdquisicion = models.DateField(auto_now_add=True)
    cantidadElemento = models.IntegerField()
    costoTotalElemento = models.IntegerField(blank=True, null=True)
    observacionElemento = models.CharField(max_length=25)
    facturaElemento = models.ImageField(
        upload_to="facturaElemento/", blank=True, null=True
    )
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return f"Detalle de {self.productoConsumible.nombreElemento}, Fecha de Adquisición: {self.fechaAdquisicion}"


# --------------------------------------------------------------------------------------------------------------------------------
class Prestamo(models.Model):
    fechaEntrega = models.DateField()
    fechaDevolucion = models.DateField()
    # SE PODRIA HACER FILTRADO Y BUSCAR EN ESTE CAMPO YA SEA POR ID O NAME - IT'S OK
    nombreEntrega = models.ForeignKey(
        "UsuariosSena",
        related_name="prestamos_entregados",
        on_delete=models.SET_NULL,
        null=True,
        to_field="numeroIdentificacion",
    )
    nombreRecibe = models.ForeignKey(
        "UsuariosSena",
        related_name="prestamos_recibidos",
        on_delete=models.SET_NULL,
        null=True,
        to_field="numeroIdentificacion",
    )

    serialSenaElemento = models.ForeignKey(
        "InventarioDevolutivo", on_delete=models.CASCADE, related_name="prestamos"
    )
    serialSenaElemento = models.ForeignKey(
        "InventarioDevolutivo", on_delete=models.CASCADE, related_name="prestamos"
    )

    # Método para finalizar préstamo y actualizar inventario
    def finalizar_prestamo(self):
        self.estadoPrestamo = "FINALIZADO"
        producto = self.serialSenaElemento.producto
        producto.disponibles += 1
        producto.save()
        self.save()

    estado_actualizado = models.BooleanField(default=False)
    estadoPrestamo = models.CharField(max_length=25, default="ACTIVO")
    valorUnidadElemento = models.IntegerField()
    firmaDigital = models.ImageField(upload_to="firmaDigital/", blank=True, null=True)
    observacionesPrestamo = models.TextField()
    observacionesEntrega = models.TextField(blank=True, null=False)

    def __str__(self):
        return f"Prestamo devolutivo del producto {self.serialSenaElemento.producto.nombre}"

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"



class EntregaConsumible(models.Model):
    fecha_entrega = models.DateField()
    responsable_Entrega = models.ForeignKey(
        "UsuariosSena",
        related_name="entregas_realizadas",
        on_delete=models.SET_NULL,
        null=True,
        to_field="numeroIdentificacion",
    )
    nombre_solicitante = models.ForeignKey(
        "UsuariosSena",
        related_name="solicitudes_recibidas",
        on_delete=models.SET_NULL,
        null=True,
        to_field="numeroIdentificacion",
    )

    idC = models.ForeignKey(
        "InventarioConsumible", on_delete=models.CASCADE, related_name="entregas"
    )

    cantidad_prestada = models.PositiveIntegerField()
    observaciones_prestamo = models.TextField()
    firmaDigital = models.ImageField(upload_to="firmaDigital/", blank=True, null=True)

    def __str__(self):
        return self.nombreElemento
