import os
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Exists, OuterRef
from .forms import (
    UserLoginForm,
)
from django.db.models import Exists, OuterRef
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .models import (
    UsuariosSena,
    Prestamo,
    InventarioDevolutivo,
    ProductosInventarioDevolutivo,
    ProductosInventarioConsumible,
    InventarioConsumible,
    EntregaConsumible,
    InventarioDevolutivo,
)
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Exists, OuterRef
from .forms import (
    UserLoginForm,
)
from django.db.models import Exists, OuterRef
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .models import (
    UsuariosSena,
    Prestamo,
    InventarioDevolutivo,
    ProductosInventarioDevolutivo,
    ProductosInventarioConsumible,
    InventarioConsumible,
    EntregaConsumible,
    InventarioDevolutivo,
)
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# decoradores para uso de Permisos en las visats de usuario y de inicia de sesion
from django.contrib.auth.decorators import login_required
from .decorators import verificar_cuentadante, verificar_superadmin

from django.contrib.auth import login, authenticate, logout
from datetime import timedelta, datetime, date
from django.core.exceptions import ValidationError
from django.urls import reverse

# Limpiar Cache
from django.core.cache import cache

# Importar biblioteca reportlab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
from svglib.svglib import svg2rlg
from django.http import HttpResponse
import os



# Librería excel
import xlsxwriter

# Create your views here.
from django.contrib.auth.views import PasswordResetConfirmView


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def post(self, request, *args, **kwargs):
        # Aquí puedes agregar mensajes de depuración
        print("Protocol:", request.scheme)
        print("Domain:", request.META["HTTP_HOST"])
        print("uid:", kwargs["uidb64"])
        print("token:", kwargs["token"])

        # También puedes registrar mensajes en los registros
        import logging

        logger = logging.getLogger(__name__)
        logger.debug(f"Protocol: {request.scheme}")
        logger.debug(f"Domain: {request.META['HTTP_HOST']}")
        logger.debug(f"uid: {kwargs['uidb64']}")
        logger.debug(f"token: {kwargs['token']}")

        # Tu lógica existente aquí
        return super().post(request, *args, **kwargs)


# Create your views here.
def login_view(request):
    if request.method == "POST":
        loginForm = UserLoginForm(request.POST)
        if loginForm.is_valid():
            numeroIdentificacion = loginForm.cleaned_data.get("numeroIdentificacion")
            password = loginForm.cleaned_data.get("password")
            user = authenticate(
                request, username=numeroIdentificacion, password=password
            )

            if user is not None:
                login(request, user)
                return redirect("homedash")

            else:
                loginForm.add_error(None, "Invalid username or password")
    else:
        loginForm = UserLoginForm()

    return render(request, "indexLogin.html", {"form": loginForm})


@login_required
def homedash(request):
    prestamos = Prestamo.objects.all().order_by("fechaDevolucion")
    entregas = EntregaConsumible.objects.all()
    usuarios = UsuariosSena.objects.all()  # Consulta todos los usuarios
    opcion_seleccionada = request.GET.get("opcion", None)
    data = {
        "opcion_seleccionada": opcion_seleccionada,
        "Prestamos": prestamos,
        "Entregas": entregas,
        "usuarios": usuarios,
    }

    return render(request, "superAdmin/basedashboard.html", data)


@login_required
def elementosdash(request):
    return render(request, "superAdmin/elementosdash.html")


@login_required
def usuariodash(request):
    return render(request, "superAdmin/usuariodash.html")


@login_required
def inventariodash(request):
    return render(request, "superAdmin/inventariodash.html")


@login_required
def transacciondash(request):
    return render(request, "superAdmin/transaccionesdash.html")


def logout(request):
    return render(request, "indexLogin.html")


@login_required
def consultarUsuario_view(request):
    usuarios = UsuariosSena.objects.all()  # Consulta todos los usuarios
    return render(request, "superAdmin/consultarUsuario.html", {"usuarios": usuarios})


@login_required
@verificar_superadmin
def registroUsuario_view(request):
    if request.method == "POST":
        nombresVar = request.POST.get("nombres")
        apellidosVar = request.POST.get("apellidos")
        tipoIdentificacionVar = request.POST.get("tipoIdentificacion")
        numeroIdentificacionVar = request.POST.get("numeroIdentificacion")
        emailVar = request.POST.get("email")
        celularVar = request.POST.get("celular")
        rolVar = request.POST.get("rol")
        cuentadanteVar = request.POST.get("cuentadante")
        tipoContratoVar = request.POST.get("tipoContrato")
        is_activeVar = request.POST.get("is_active")
        duracionContratoVar = request.POST.get("duracionContrato")
        passwordVar = request.POST.get("password")
        fotoUsuarioVar = request.FILES.get(
            "fotoUsuario", None
        )  # Ajustado para manejar casos en los que no se suba una foto

        # Validar si el número de identificación ya está registrado
        if UsuariosSena.objects.filter(
            numeroIdentificacion=numeroIdentificacionVar
        ).exists():
            messages.error(request, "El número de identificación ya está registrado.")
        else:
            emailVar = request.POST.get("email")

            # Validar si el correo electrónico ya está registrado
            if UsuariosSena.objects.filter(email=emailVar).exists():
                messages.error(request, "El correo electrónico ya está registrado.")
            else:
                celularVar = request.POST.get("celular")
                rolVar = request.POST.get("rol")
                cuentadanteVar = request.POST.get("cuentadante")
                tipoContratoVar = request.POST.get("tipoContrato")
                is_activeVar = request.POST.get("is_active")
                duracionContratoVar = request.POST.get("duracionContrato")
                passwordVar = request.POST.get("password")
                fotoUsuarioVar = request.POST.get("fotoUsuario")

                # Cifrar la contraseña
                password_cifrada = make_password(passwordVar)

                # Crear el objeto de usuario y guardarlo en la base de datos
                user = UsuariosSena(
                    nombres=nombresVar,
                    apellidos=apellidosVar,
                    tipoIdentificacion=tipoIdentificacionVar,
                    numeroIdentificacion=numeroIdentificacionVar,
                    email=emailVar,
                    celular=celularVar,
                    rol=rolVar,
                    cuentadante=cuentadanteVar,
                    tipoContrato=tipoContratoVar,
                    is_active=is_activeVar,
                    # is_staff=True, #Permitiru ingreso al admin, creados por la aplicacion
                    duracionContrato=duracionContratoVar,
                    password=password_cifrada,
                    fotoUsuario=fotoUsuarioVar,
                )
                user.save()

                messages.success(request, "Usuario Registrado con Éxito")

    return render(request, "superAdmin/registroUsuario.html")


@login_required
@verificar_superadmin
def editarUsuario_view(request, numeroIdentificacion):
    try:
        user = UsuariosSena.objects.get(numeroIdentificacion=numeroIdentificacion)
        datos = {"user": user}
        # Redirigir a la vista consultarUsuario_view para recargar los datos
        return render(request, "superAdmin/editarUsuario.html", datos)
    except UsuariosSena.DoesNotExist:
        messages.warning(request, "No existe registro")
        return redirect("consultarUsuario_view")


@login_required
@verificar_superadmin
def editarElementosconsu_view(request, id):
    # Obtener el objeto ElementosConsumible por su ID
    elemento = get_object_or_404(InventarioConsumible, id=id)

    if request.method == "POST":
        try:
            # Obtener datos del formulario
            fecha_adquisicion = request.POST.get("txt_fechaadquisicion")
            nombre_elemento = request.POST.get("txt_nombreElemento")
            categoria_elemento = request.POST.get("txt_categoriaElemento")
            estado_elemento = request.POST.get("txt_estadoElemento")
            descripcion_elemento = request.POST.get("txt_descripcionElemento")
            observacion_elemento = request.POST.get("txt_observacionElemento")
            cantidad_elemento = request.POST.get("txt_cantidadElemento")
            costo_unidad_elemento = request.POST.get("txt_costoUnidadElemento")
            costo_total_elemento = request.POST.get("txt_costoTotalElemento")
            factura_elemento = request.FILES.get("txt_facturaElemento")

            # Actualizar los campos del objeto ElementosConsumible con los datos del formulario
            elemento.fechaAdquisicion = fecha_adquisicion
            elemento.productoConsumible.nombreElemento = nombre_elemento
            elemento.categoriaElemento = categoria_elemento
            elemento.productoConsumible.estadoElemento = estado_elemento
            elemento.productoConsumible.descripcionElemento = descripcion_elemento
            elemento.observacionElemento = observacion_elemento
            elemento.cantidadElemento = cantidad_elemento
            elemento.productoConsumible.costoUnidadElemento = costo_unidad_elemento
            elemento.costoTotalElemento = costo_total_elemento
            elemento.facturaElemento = factura_elemento

            # Guardar el modelo ProductosInventarioConsumible
            elemento.productoConsumible.save()

            # Guardar el modelo InventarioConsumible
            elemento.save()

            messages.success(request, "Elemento consumible actualizado con éxito")
            consultar_elementosconsu_url = reverse("consultarElementos")
            return redirect(
                f"{consultar_elementosconsu_url}?opcion=elemento_consumible"
            )

        except InventarioConsumible.DoesNotExist as e:
            # Manejar la excepción y mostrar un mensaje de error
            error_message = f"Elemento consumible no encontrado. Detalles: {e}"
            print(error_message)  # Imprimir mensaje de error en la consola
            return render(
                request,
                "superAdmin/editarElementoconsu.html",
                {"elemento": elemento, "error_message": error_message},
            )

    # Si la solicitud no es POST, enviar el objeto ElementosConsumible a la plantilla
    return render(
        request, "superAdmin/editarElementoconsu.html", {"elemento": elemento}
    )


@login_required
@verificar_superadmin
def editarElementosdevo_view(request, serial):
    # Obtener el objeto InventarioDevolutivo por su serial
    try:
        inventario_elemento = InventarioDevolutivo.objects.select_related(
            "producto"
        ).get(serial=serial)

        datos = {"inventario_elemento": inventario_elemento}
        # Redirigir a la vista consultarUsuario_view para recargar los datos
        return render(request, "superAdmin/editarElementodevo.html", datos)

    except InventarioDevolutivo.DoesNotExist as e:
        messages.warning(request, "No existe registro")
        return redirect("consultarElementos")


@login_required
@verificar_superadmin
def actualizarElementoDevolutivo(request, serial):
    try:
        inventario_elemento = InventarioDevolutivo.objects.select_related(
            "producto"
        ).get(serial=serial)

        if request.method == "POST":
            # Obtener datos del formulario
            serial_elemento = request.POST.get("txt_serial")
            fecha_Registro = request.POST.get("txt_fechaAdquisicion")
            nombre_elemento = request.POST.get("txt_nombreElemento")
            categoria_elemento = request.POST.get("txt_categoriaElemento")
            estado_elemento = request.POST.get("txt_estadoElemento")
            descripcion_elemento = request.POST.get("txt_descripcionElemento")
            observacion_elemento = request.POST.get("txt_observacionElemento")
            cantidad_elemento = request.POST.get("txt_cantidadElemento")
            factura_elemento = request.FILES.get("txt_facturaElemento")
            valor_nidad = request.POST.get("txt_valorUnidadElemento")

            # Actualizar campos del modelo ProductosInventarioDevolutivo
            inventario_elemento.producto.nombre = nombre_elemento
            inventario_elemento.producto.categoria = categoria_elemento
            inventario_elemento.producto.estado = estado_elemento
            inventario_elemento.producto.descripcion = descripcion_elemento
            inventario_elemento.producto.valor_unidad = valor_nidad
            # Actualizar campos del modelo InventarioDevolutivo
            inventario_elemento.fecha_Registro = fecha_Registro
            inventario_elemento.observacion = observacion_elemento
            inventario_elemento.factura = factura_elemento
            print(
                "actualizarElementoDevolutivo ",
                categoria_elemento,
                observacion_elemento,
            )
            inventario_elemento.producto.save()

            inventario_elemento.save()
            messages.success(request, "Elemento Consumible Editado con Éxito")

            consultar_elementodevo_url = reverse("consultarElementos")
            return redirect(f"{consultar_elementodevo_url}?opcion=elemento_devolutivo")

    except InventarioDevolutivo.DoesNotExist as e:
        messages.warning(request, "No existe registro")
        return redirect("consultarElementos")

    return render(
        request,
        "superAdmin/editarElementodevo.html",
        {"inventario_elemento": inventario_elemento},
    )


@login_required
@verificar_superadmin
def actualizarUsuario_view(request, numeroIdentificacion):
    if request.method == "POST":
        nombreVar = request.POST.get("nombre")
        apellidoVar = request.POST.get("Apellidos")
        tipoIdentificacionVar = request.POST.get("tipoIdentificacion")
        numeroIdentificacionVar = request.POST.get("numeroIdentificacion")
        correoSenaVar = request.POST.get("correoSena")
        celularVar = request.POST.get("celular")
        rolVar = request.POST.get("rol")
        cuentadanteVar = request.POST.get("cuentadante")
        tipoContratoVar = request.POST.get("tipoContrato")
        duracionContratoVar = request.POST.get("duracionContrato")
        estadoUsuariovar = request.POST.get("estadoUsuario")
        passwordVar = request.POST.get("contraSena")
        validacionContraSenaVar = request.POST.get("validacionContraSena")
        fotoUsuarioVar = request.FILES.get("fotoUsuario")

        user = UsuariosSena.objects.get(numeroIdentificacion=numeroIdentificacion)
        if passwordVar != validacionContraSenaVar:
            messages.warning(request, "La contraseña no coincide")
            return redirect("consultarUsuario_view")
        password_cifrada = make_password(passwordVar)
        user.nombres = nombreVar
        user.apellidos = apellidoVar
        user.tipoIdentificacion = tipoIdentificacionVar
        user.numeroIdentificacion = numeroIdentificacionVar
        user.email = correoSenaVar
        user.celular = celularVar
        user.rol = rolVar
        user.cuentadante = cuentadanteVar
        user.tipoContrato = tipoContratoVar
        user.duracionContrato = duracionContratoVar
        user.is_active = estadoUsuariovar == "A"  # 'A' para activo, 'I' para inactivo
        user.password = password_cifrada
        user.fotoUsuario = fotoUsuarioVar
        user.save()
        messages.success(request, "Usuario actualizado con Exito")  # mensaje de alerta

        # Redirigir a la vista consultarUsuario_view para recargar los datos
        return redirect("consultarUsuario_view")
    else:
        messages.warning(request, "No existe registro")
        return redirect("consultarUsuario_view")


@login_required
@verificar_superadmin
def eliminarUsuario_view(request, numeroIdentificacion):
    try:
        # Busca el usuario por ID
        user = UsuariosSena.objects.get(numeroIdentificacion=numeroIdentificacion)
        # Desactiva el usuario
        user.is_active = False
        user.save()

        # Cierra la sesión del usuario
        logout(request)

        # Mensaje de éxito
        messages.success(request, "Perfil descativado exitosamente.")

        # Redirige a la página de inicio (ajusta la URL según tu configuración)
        return redirect("consultarUsuario_view")

    except UsuariosSena.DoesNotExist:
        # Maneja el caso en el que el usuario no existe
        messages.error(request, "Usuario no encontrado.")
        return redirect("index")


@login_required
@verificar_cuentadante
def inhabilitar_elemento_consumible(request, id):
    consumible = get_object_or_404(ProductosInventarioConsumible, id=id)
    # Cambiar el estado a "Baja"
    consumible.estadoElemento = "Baja"
    consumible.save()
    messages.success(request, "Elemento inhabilitado Correctamente")
    # Puedes agregar más lógica o mensajes según sea necesario
    return redirect("consultarElementos")

@login_required
@verificar_cuentadante
def inhabilitar_elemento_devo(request, serial):
    devolutivo = get_object_or_404(InventarioDevolutivo, serial=serial)
    # Cambiar el estado a "Baja"
    devolutivo.producto.estado = 'Baja'
    devolutivo.producto.save()
    messages.success(request, "Elemento inhabilitado Correctamente")
    # Puedes agregar más lógica o mensajes según sea necesario
    return redirect("consultarElementos")



# def inhabilitar_elemento_devolutivo(request, id):
#     devolutivo = get_object_or_404(ProductosInventarioDevolutivo, id=id)
#     # Cambiar el estado a "Baja"
#     devolutivo.estadoElemento = 'Baja'
#     devolutivo.save()
#     messages.success(request, "Elemento inhabilitado Correctamente")
#     # Puedes agregar más lógica o mensajes según sea necesario
#     return redirect("consultarElementos")







@login_required
@verificar_cuentadante
def formPrestamosDevolutivos_view(request):
    # Obtiene todos los usuarios excepto el que esta fijado de primero
    usuarios = UsuariosSena.objects.exclude(numeroIdentificacion="12345")
    # usuario específico que se quiere fijar
    try:
        usuario_pinned = UsuariosSena.objects.get(numeroIdentificacion="12345")
    except UsuariosSena.DoesNotExist:
        usuario_pinned = None

    # Obtiene el nombre del producto, el serial del inventario y los disponibles
    prestamos_activos_o_vencidos = Prestamo.objects.filter(
        serialSenaElemento=OuterRef("pk"),
        estadoPrestamo__in=["ACTIVO", "VENCIDO"],
    )

    # Anotar la disponibilidad de los elementos basándote en la existencia de préstamos activos o vencidos
    elementos = (
        InventarioDevolutivo.objects.annotate(
            prestado=Exists(prestamos_activos_o_vencidos)
        )
        .select_related("producto")
        .values_list("producto__nombre", "serial", "producto__descripcion", "prestado")
    )
    form_data = {}
    if request.method == "POST":
        fechaDevolucionVar = request.POST.get("fechaDevolucion")
        fechaDevolucion = date.fromisoformat(
            fechaDevolucionVar
        )  # Convierte la fecha a objeto date
        fechaEntregaVar = date.today()
        nombreEntregavar = request.POST.get("nombreEntrega")
        nombreRecibevar = request.POST.get("nombreRecibe")
        nombreElementovar = request.POST.get("nombreElemento")
        serialSenaElementovar = request.POST.get("serialSenaElemento")
        # cantidadElementoVar = int(request.POST.get("cantidadElemento"))
        valorUnidadElementoVar = int(request.POST.get("valorUnidadElemento"))
        disponiblesVar = request.POST.get("disponibles", "")

        observacionesPrestamovar = request.POST.get("observacionesPrestamo")
        form_data = {
            "fechaDevolucion": fechaDevolucionVar,
            "nombreEntrega": nombreEntregavar,
            "nombreRecibe": nombreRecibevar,
            "nombreElemento": nombreElementovar,
            "disponibles": disponiblesVar,
            "valorUnidadElemento": valorUnidadElementoVar,
            "serialSenaElemento": serialSenaElementovar,
            "observacionesPrestamo": observacionesPrestamovar,
        }
        # Dividir el nombre y apellido para nombreEntrega
        partes_nombre_entrega = nombreEntregavar.split(maxsplit=1)
        if len(partes_nombre_entrega) == 2:
            nombre_entrega, apellido_entrega = partes_nombre_entrega
        else:
            messages.error(
                request,
                "Formato inválido para el nombre del instructor que entrega. Por favor, ingrese nombre y apellido.",
            )
            return render(
                request,
                "superAdmin/formPrestamosDevolutivos.html",
                {"elementos": elementos, "usuarios": usuarios},
            )

        # Dividir el nombre y apellido para nombreRecibe
        partes_nombre_recibe = nombreRecibevar.split(maxsplit=1)
        if len(partes_nombre_recibe) == 2:
            nombre_recibe, apellido_recibe = partes_nombre_recibe
        else:
            messages.error(
                request,
                "Formato inválido para el nombre del instructor que recibe. Por favor, ingrese nombre y apellido.",
            )
            return render(
                request,
                "superAdmin/formPrestamosDevolutivos.html",
                {"elementos": elementos, "usuarios": usuarios},
            )
        try:
            nombreEntregaUsuario = UsuariosSena.objects.get(
                nombres=nombre_entrega, apellidos=apellido_entrega
            )
        except UsuariosSena.DoesNotExist:
            messages.error(request, "Usuario de entrega no encontrado.")
            return render(
                request,
                "superAdmin/formPrestamosDevolutivos.html",
                {
                    "elementos": elementos,
                    "usuarios": usuarios,
                    "form_data": form_data,
                },
            )

        # Obtener la instancia del usuario para el campo nombreRecibe
        try:
            nombreRecibeUsuario = UsuariosSena.objects.get(
                nombres=nombre_recibe, apellidos=apellido_recibe
            )
        except UsuariosSena.DoesNotExist:
            messages.error(request, "Usuario receptor no encontrado.")
            return render(
                request,
                "superAdmin/formPrestamosDevolutivos.html",
                {
                    "elementos": elementos,
                    "usuarios": usuarios,
                    "form_data": form_data,
                },
            )
        try:
            # Obtiene el inventario correspondiente al nombre del producto y serial
            inventario = InventarioDevolutivo.objects.select_related("producto").get(
                producto__nombre=nombreElementovar, serial=serialSenaElementovar
            )

            # Validaciones
            if fechaDevolucion < date.today():
                messages.error(
                    request,
                    "La fecha de devolución no puede ser anterior a la fecha actual.",
                )
                return render(
                    request,
                    "superAdmin/formPrestamosDevolutivos.html",
                    {
                        "elementos": elementos,
                        "usuarios": usuarios,
                        "form_data": form_data,
                    },
                )

            # Crea el objeto Prestamo
            prestamo = Prestamo(
                fechaEntrega=fechaEntregaVar,
                fechaDevolucion=fechaDevolucionVar,
                nombreEntrega=nombreEntregaUsuario,  # Esto es una instancia de UsuariosSena
                nombreRecibe=nombreRecibeUsuario,  # Esto tambien es una instancia de UsuariosSena
                serialSenaElemento=inventario,  # Esto es una instancia de InventarioDevolutivo
                # disponibles=disponiblesVar,
                valorUnidadElemento=valorUnidadElementoVar,
                # valorTotalElemento=valorTotalElementoVar,
                observacionesPrestamo=observacionesPrestamovar,
            )
            prestamo.save()

            prestamo_id = prestamo.id

            # Enviar Correo De Notificacion a la hora de Realizar el prestamo

            enviar_correo_notificacion(request, prestamo_id)

            # Disminuir la cantidad de elementos disponibles
            if inventario.producto.categoria == "D":
                inventario.producto.disponibles = max(
                    inventario.producto.disponibles - 1, 0
                )
                inventario.producto.save()
            messages.success(request, "Elemento Guardado Exitosamente")
            return redirect("formPrestamosDevolutivos_view")

        except InventarioDevolutivo.DoesNotExist:
            messages.error(request, "El elemento con el serial dado no existe.")
            # Renderiza de nuevo el formulario con el mensaje de error
            return render(
                request,
                "superAdmin/formPrestamosDevolutivos.html",
                {
                    "elementos": elementos,
                    "usuarios": usuarios,
                    "form_data": form_data,
                },
            )
        except ValidationError as e:
            return HttpResponse(str(e), status=400)

    return render(
        request,
        "superAdmin/formPrestamosDevolutivos.html",
        {
            "elementos": elementos,
            "usuario_pinned": usuario_pinned,
            "usuarios": usuarios,
            "form_data": form_data,
        },
    )


@login_required
def get_element_name_by_serial(request):
    serial_number = request.GET.get("serialNumber", None)
    if serial_number:
        try:
            inventario_item = InventarioDevolutivo.objects.get(serial=serial_number)
            element_name = inventario_item.producto.nombre
            valor_unidad = inventario_item.producto.valor_unidad
            stock_disponible = inventario_item.producto.disponibles

            # Verificar si el elemento ha sido prestado y obtener el estado del préstamo
            prestamo_activo = (
                Prestamo.objects.filter(
                    serialSenaElemento=serial_number,
                    fechaDevolucion__gte=timezone.now().date(),
                )
                .order_by("-fechaDevolucion")
                .first()
            )

            estado_prestamo = "DISPONIBLE"
            if prestamo_activo:
                if prestamo_activo.fechaDevolucion < timezone.now().date():
                    estado_prestamo = "VENCIDO"
                else:
                    estado_prestamo = prestamo_activo.estadoPrestamo

            return JsonResponse(
                {
                    "elementName": element_name,
                    "valorUnidad": valor_unidad,
                    "esPrestado": estado_prestamo in ["ACTIVO", "VENCIDO"],
                    "estadoPrestamo": estado_prestamo,
                    "Stock": stock_disponible,
                }
            )
        except InventarioDevolutivo.DoesNotExist:
            return JsonResponse({"error": "Serial number not found"}, status=404)
    else:
        return JsonResponse({"error": "No serial number provided"}, status=400)


@login_required
@verificar_cuentadante
def formEntregasConsumibles_view(request):
    # Obtiene todos los usuarios excepto el que esta fijado de primero
    usuarios = UsuariosSena.objects.exclude(numeroIdentificacion="12345")
    # usuario específico que se quiere fijar
    try:
        usuario_pinned = UsuariosSena.objects.get(numeroIdentificacion="12345")
    except UsuariosSena.DoesNotExist:
        usuario_pinned = None
    elementos = (
        ProductosInventarioConsumible.objects.all()
    )  # Obtiene todos los elementos

    if request.method == "POST":
        responsable_Entrega_nombre = request.POST.get("responsable_Entrega")
        nombre_solicitante_nombre = request.POST.get("nombre_solicitante")
        idC_id = request.POST.get("idC")  # Este es el ID del InventarioConsumible

        cantidad_prestada = request.POST.get("cantidadElemento")
        observaciones_prestamo = request.POST.get("observaciones_prestamo")
        firmaDigital = (
            request.FILES.get("firmaDigital")
            if "firmaDigital" in request.FILES
            else None
        )

        # Dividir el nombre y apellido para responsable_Entrega
        partes_nombre_responsable = responsable_Entrega_nombre.split(maxsplit=1)
        if len(partes_nombre_responsable) == 2:
            nombre_responsable, apellido_responsable = partes_nombre_responsable
        else:
            messages.error(
                request,
                "Debe ingresar tanto el nombre como el apellido del responsable de la entrega.",
            )
            return render(
                request,
                "superAdmin/formEntregasConsumibles.html",
                {"usuarios": usuarios, "elementos": elementos},
            )

        # Dividir el nombre y apellido para nombre_solicitante
        partes_nombre_solicitante = nombre_solicitante_nombre.split(maxsplit=1)
        if len(partes_nombre_solicitante) == 2:
            nombre_solicitante, apellido_solicitante = partes_nombre_solicitante
        else:
            messages.error(
                request,
                "Debe ingresar tanto el nombre como el apellido del solicitante.",
            )
            return render(
                request,
                "superAdmin/formEntregasConsumibles.html",
                {"usuarios": usuarios, "elementos": elementos},
            )
        try:
            responsable_Entrega = UsuariosSena.objects.get(
                nombres=nombre_responsable, apellidos=apellido_responsable
            )
            nombre_solicitante = UsuariosSena.objects.get(
                nombres=nombre_solicitante, apellidos=apellido_solicitante
            )
            inventarioConsumible = InventarioConsumible.objects.get(id=idC_id)

            # Obtener el producto consumible y verificar la cantidad disponible
            producto_consumible = ProductosInventarioConsumible.objects.get(id=idC_id)
            cantidad_solicitada = int(cantidad_prestada)

            if producto_consumible.disponible >= cantidad_solicitada:
                # Actualizar la cantidad disponible y crear la entrega
                producto_consumible.disponible -= cantidad_solicitada
                producto_consumible.save()

                entrega_consumible = EntregaConsumible(
                    fecha_entrega=timezone.now(),
                    responsable_Entrega=responsable_Entrega,
                    nombre_solicitante=nombre_solicitante,
                    idC=inventarioConsumible,
                    cantidad_prestada=cantidad_solicitada,
                    observaciones_prestamo=observaciones_prestamo,
                    firmaDigital=firmaDigital,
                )
                entrega_consumible.save()
                messages.success(request, "Entrega de consumible guardada exitosamente")
                return redirect("formEntregasConsumibles_view")
            else:
                messages.error(request, "Cantidad no disponible.")

        except UsuariosSena.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
        except InventarioConsumible.DoesNotExist:
            messages.error(request, "Elemento consumible no encontrado.")
        except Exception as e:
            messages.error(request, f"Error al procesar la solicitud: {str(e)}")
        # En caso de cualquier otro error, también debes manejarlo.

    return render(
        request,
        "superAdmin/formEntregasConsumibles.html",
        {
            "usuarios": usuarios,
            "elementos": elementos,
            "usuario_pinned": usuario_pinned,
            "form_data": request.POST,
        },
    )


# Rellenar info del elemento consumible seleccionado
@login_required
def get_element_consum_info(request):
    consumible_id = request.GET.get("consumibleId", None)
    element_id = request.GET.get("id", None)

    if consumible_id:
        try:
            consumible_item = ProductosInventarioConsumible.objects.get(
                id=consumible_id
            )
            nombre_elemento = consumible_item.nombreElemento
            stock_disponible = consumible_item.disponible
            return JsonResponse(
                {"nombreElemento": nombre_elemento, "disponible": stock_disponible}
            )
        except ProductosInventarioConsumible.DoesNotExist:
            return JsonResponse({"error": "ID de consumible no encontrado"}, status=404)
    elif element_id:
        try:
            elemento = ProductosInventarioConsumible.objects.get(id=element_id)
            return JsonResponse(
                {"nombre": elemento.nombreElemento, "disponible": elemento.disponible}
            )
        except ProductosInventarioConsumible.DoesNotExist:
            return JsonResponse(
                {"error": "Elemento con el ID proporcionado no encontrado"}, status=404
            )
    else:
        return JsonResponse(
            {"error": "No se proporcionó ID o nombre de consumible"}, status=400
        )


@login_required
def calendario(request):
    prestamos = Prestamo.objects.select_related(
        "nombreRecibe", "serialSenaElemento__producto"
    ).all()
    eventos = []

    for prestamo in prestamos:
        nombre_usuario = (
            f"{prestamo.nombreRecibe.nombres} {prestamo.nombreRecibe.apellidos}"
        )
        nombre_producto = prestamo.serialSenaElemento.producto.nombre
        titulo_evento = f"{nombre_usuario} - {nombre_producto}"

        evento = {
            "title": titulo_evento,
            "start": prestamo.fechaEntrega.isoformat(),
            "end": (prestamo.fechaDevolucion + timedelta(days=1)).isoformat(),
        }
        eventos.append(evento)

    return render(request, "superAdmin/calendario.html", {"eventos": eventos})


@login_required
@verificar_cuentadante
def formElementos_view(request):
    form_data = {}
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        categoria = request.POST.get("categoria")
        estado = request.POST.get("estado")
        descripcion = request.POST.get("descripcion")
        valor_unidad = int(request.POST.get("valor_unidad"))
        serial = request.POST.get("serial")
        observacion = request.POST.get("observacion")
        factura = request.FILES.get("factura")
        form_data = {
            "nombre": nombre,
            "valor_unidad": valor_unidad,
            "serial": serial,
            "descripcion": descripcion,
            "observacion": observacion,
        }
        if categoria == "D":  # Devolutivo
            if InventarioDevolutivo.objects.filter(serial=serial).exists():
                messages.error(
                    request,
                    "El número de serial ya está registrado para un elemento devolutivo.",
                )
                return render(
                    request, "superAdmin/formElementos.html", {"form_data": form_data}
                )
            # Verificar si el producto ya existe
            producto, created = ProductosInventarioDevolutivo.objects.get_or_create(
                nombre=nombre,
                categoria=categoria,
                estado=estado,
                descripcion=descripcion,
                valor_unidad=valor_unidad,
            )

            # Crear una nueva entrada en el Inventario Devolutivo
            InventarioDevolutivo.objects.create(
                producto=producto,
                serial=serial,
                observacion=observacion,
                factura=factura,
            )

            # Actualizar el contador de elementos disponibles
            producto.disponibles += 1
            producto.save()

            messages.success(request, "Elemento Devolutivo Guardado Exitosamente")

        elif categoria == "C":  # Consumible
            cantidad = int(request.POST.get("cantidadElemento"))
            costo_total = cantidad * valor_unidad

            producto, created = ProductosInventarioConsumible.objects.get_or_create(
                nombreElemento=nombre,
                categoriaElemento=categoria,
                estadoElemento=estado,
                descripcionElemento=descripcion,
                costoUnidadElemento=valor_unidad,
            )

            InventarioConsumible.objects.create(
                productoConsumible=producto,
                cantidadElemento=cantidad,
                costoTotalElemento=costo_total,
                observacionElemento=observacion,
                facturaElemento=factura,
            )

            producto.disponible += cantidad
            producto.save()

            messages.success(request, "Elemento Consumible Guardado Exitosamente")

        else:
            messages.error(request, "Categoría de elemento no válida.")

        return redirect("formElementos_view")

    return render(request, "superAdmin/formElementos.html")


@login_required
def consultarElementos(request):
    opcion_seleccionada = request.GET.get("opcion", None)
    elementosconsu = InventarioConsumible.objects.select_related(
        "productoConsumible"
    ).all()
    elementos_devolutivos = InventarioDevolutivo.objects.all()

    for elemento in elementos_devolutivos:
        elemento.esta_en_prestamo = Prestamo.objects.filter(
            serialSenaElemento=elemento, estadoPrestamo__in=["ACTIVO", "VENCIDO"]
        ).exists()

    data = {
        "opcion_seleccionada": opcion_seleccionada,
        "ElementosConsumibles": elementosconsu,
        "ElementosDevolutivos": elementos_devolutivos,
    }

    return render(request, "superAdmin/consultarElementos.html", data)


@login_required
def consultarTransacciones_view(request):
    prestamos = Prestamo.objects.select_related("nombreRecibe", "nombreEntrega").all()

    for prestamo in prestamos:
        prestamo.nombre_del_producto = prestamo.serialSenaElemento.producto.nombre

        # Comprobación de la fecha de devolución y si el estado ya ha sido actualizado
        if (
            prestamo.fechaDevolucion < timezone.now().date()
            and not prestamo.estado_actualizado  # estado_actualizado variable de comprobación
        ):
            prestamo.estadoPrestamo = "VENCIDO"
            prestamo.estado_actualizado = True
            prestamo.save()

    entregas = EntregaConsumible.objects.all()
    usuarios = UsuariosSena.objects.all()  # Consulta todos los usuarios
    opcion_seleccionada = request.GET.get("opcion", None)
    data = {
        "opcion_seleccionada": opcion_seleccionada,
        "Prestamos": prestamos,
        "Entregas": entregas,
        "usuarios": usuarios,
    }

    return render(request, "superAdmin/consultarTransacciones.html", data)


@login_required
@verificar_cuentadante
def finalizarPrestamo_view(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)

    if request.method == "POST":
        try:
            prestamo.finalizar_prestamo()
            messages.success(request, "Préstamo finalizado correctamente!!")
            return redirect(f"{reverse('consultarTransacciones')}?opcion=prestamo")
        except Exception as e:
            messages.error(request, f"Error al finalizar el préstamo: {e}")

    return render(
        request, "superAdmin/consultarTransacciones.html", {"prestamo": prestamo}
    )

def generar_pdf_devolutivos(request):

    buffer = BytesIO()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="lista_elementos_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf"'

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        pagesize=letter,
    )

    elementos = []

    logo_path = 'UsuariosSena/static/img/logo-sena-negro-png-2022.png'

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=0.5 * inch, height=0.5 * inch)
        logo.hAlign = 'LEFT'
        elementos.append(logo)
    else:
        return HttpResponse("Error: El archivo de imagen no existe.")

    estilo_titulo = ParagraphStyle(
        'Title',
        parent=getSampleStyleSheet()['Title'],
        spaceAfter=6,
        fontSize=16,
    )
    titulo_para = Paragraph("Elementos del Inventario devolutivo", estilo_titulo)
    elementos.append(titulo_para)

    data = [
        [
            "F. Registro",
            "Producto",
            "Categoría",
            "Estado",
            "Descripción",
            "Valor Unidad",
            "Serial",
            "Observación",
            "Factura",
        ]
    ]
    
    

    # Agrega datos al arreglo 'data' según la selección
    for inventario in InventarioDevolutivo.objects.select_related("producto").all():
            producto = inventario.producto
            data.append(
                [
                    inventario.fecha_Registro.strftime("%Y-%m-%d"),
                    producto.nombre,
                    producto.categoria,
                    producto.estado,
                    producto.descripcion,
                    producto.valor_unidad,
                    inventario.serial,
                    inventario.observacion,
                    "Factura",
                ]
            )
    
    table = Table(data, colWidths=[0.9 * inch] * 9)
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.green),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )
    table.setStyle(table_style)
    elementos.append(table)

    doc.build(elementos)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response




def generar_pdf_consumibles(request):
    
    buffer = BytesIO()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="lista_elementos_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf"'

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        pagesize=letter,
    )

    elementos = []

    logo_path = 'UsuariosSena/static/img/logo-sena-negro-png-2022.png'

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=0.5 * inch, height=0.5 * inch)
        logo.hAlign = 'LEFT'
        elementos.append(logo)
    else:
        return HttpResponse("Error: El archivo de imagen no existe.")

    estilo_titulo = ParagraphStyle(
        'Title',
        parent=getSampleStyleSheet()['Title'],
        spaceAfter=6,
        fontSize=16,
    )
    titulo_para = Paragraph("Elementos del Inventario consumible", estilo_titulo)
    elementos.append(titulo_para)

    data = [
        [
            "F. Registro",
            "Producto",
            "Categoría",
            "Estado",
            "Descripción",
            "Observación",
            "Factura",
        ]
    ]
    
    # Agrega datos al arreglo 'data' según la selección
    for inventario1 in InventarioConsumible.objects.select_related("productoConsumible").all():
        producto1 = inventario1.productoConsumible
        data.append(
            [
                inventario1.fechaAdquisicion.strftime("%Y-%m-%d"),
                producto1.nombreElemento,
                producto1.categoriaElemento,
                producto1.estadoElemento,
                producto1.descripcionElemento,
                inventario1.observacionElemento,
                "Factura",
            ]
        )
    
    table = Table(data, colWidths=[0.9 * inch] * 7)  # Ajusta el número de columnas según tus datos
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.green),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )
    table.setStyle(table_style)
    elementos.append(table)

    doc.build(elementos)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def generar_excel(request):
    opcion_seleccionada = request.GET.get("opcion", None)

    buffer = BytesIO()
    workbook = xlsxwriter.Workbook(buffer, {"in_memory": True})
    worksheet = workbook.add_worksheet()

    # Define the formats here
    header_format = workbook.add_format(
        {
            "bold": True,
            "align": "center",
            "valign": "vcenter",
            "bg_color": "#4CAF50",
            "font_color": "white",
            "border": 1,
        }
    )

    # Determine which data set to use
    if opcion_seleccionada == "elementosconsu":
        queryset = InventarioConsumible.objects.select_related(
            "productoConsumible"
        ).all()
        headers = [
            "Fecha Adquisición",
            "Nombre Elemento",
            "Categoría",
            "Estado",
            "Cantidad",
            "Costo Unitario",
            "Costo Total",
            "Descripción",
            "Observación",
        ]
    elif opcion_seleccionada == "elementosdevo":
        queryset = InventarioDevolutivo.objects.select_related("producto").all()
        headers = [
            "Fecha Registro",
            "Nombre Producto",
            "Categoría",
            "Estado",
            "Valor Unidad",
            "Descripción",
            "Serial",
            "Observación",
        ]
    else:
        # Handle unexpected cases or set a default
        queryset = None
        headers = []

    # Write the headers
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, header_format)

    # Write the data
    for row_num, item in enumerate(queryset, start=1):
        # This will vary depending on the structure of your models and what data you want to write
        if opcion_seleccionada == "elementosconsu":
            worksheet.write(row_num, 0, str(item.fechaAdquisicion))
            worksheet.write(row_num, 1, item.productoConsumible.nombreElemento)
            worksheet.write(
                row_num, 2, item.productoConsumible.get_categoriaElemento_display()
            )
            worksheet.write(
                row_num, 3, item.productoConsumible.get_estadoElemento_display()
            )
            worksheet.write(row_num, 4, item.cantidadElemento)
            worksheet.write(row_num, 5, item.productoConsumible.costoUnidadElemento)
            worksheet.write(row_num, 6, item.costoTotalElemento)
            worksheet.write(row_num, 7, item.productoConsumible.descripcionElemento)
            worksheet.write(row_num, 8, item.observacionElemento)
        elif opcion_seleccionada == "elementosdevo":
            worksheet.write(row_num, 0, str(item.fecha_Registro))
            worksheet.write(row_num, 1, item.producto.nombre)
            worksheet.write(row_num, 2, item.producto.get_categoria_display())
            worksheet.write(row_num, 3, item.producto.get_estado_display())
            worksheet.write(row_num, 4, item.producto.valor_unidad)
            worksheet.write(row_num, 5, item.producto.descripcion)
            worksheet.write(row_num, 6, item.serial)
            worksheet.write(row_num, 7, item.observacion)

    # Close the workbook
    workbook.close()

    # Prepare the response, setting the content type and headers
    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response[
        "Content-Disposition"
    ] = f'attachment; filename="Elementos_{opcion_seleccionada}_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx"'

    # Close the buffer
    buffer.close()

    return response

def user_logout(request):
    logout(request)
    return redirect("login_view")


@login_required
def consultarTransacciones_view(request):
    prestamos = Prestamo.objects.select_related("nombreRecibe", "nombreEntrega").all()
    for prestamo in prestamos:
        prestamo.nombre_del_producto = prestamo.serialSenaElemento.producto.nombre
        # Comprobación de la fecha de devolución PERO VA DE LA MANO CON LA LOGICA CUANDO SE FINALICE EL PRODUCTO
        if prestamo.fechaDevolucion < timezone.now().date():
            prestamo.estado = "FINALIZADO"
        else:
            prestamo.estado = "ACTIVO"

    entregas = EntregaConsumible.objects.all()
    usuarios = UsuariosSena.objects.all()  # Consulta todos los usuarios
    opcion_seleccionada = request.GET.get("opcion", None)
    data = {
        "opcion_seleccionada": opcion_seleccionada,
        "Prestamos": prestamos,
        "Entregas": entregas,
        "usuarios": usuarios,
    }

    return render(request, "superAdmin/consultarTransacciones.html", data)



@login_required
@verificar_cuentadante
def editarPrestamo_view(request, id):
    # Obtener el objeto Prestamo por su ID
    prestamo = get_object_or_404(Prestamo, id=id)
    elemento = None  # Inicializar la variable fuera del bloque try

    if request.method == "POST":
        # Obtener datos del formulario
        fecha_entrega = request.POST.get("txt_fechaentrega")
        fecha_devolucion = request.POST.get("txt_fechaDevolucion")
        nombre_entrega = request.POST.get("txt_nombreEntrega")
        nombre_recibe = request.POST.get("txt_nombreRecibe")
        nombre_elemento = request.POST.get("txt_nombreElemento")
        valor_unidad = request.POST.get("txt_valorUnidadElemento")
        observaciones_prestamo = request.POST.get("txt_observacionesPrestamo")
        estado_prestamo = request.POST.get("txt_estado_prestamo")

        try:
            # Actualizar los campos del objeto Prestamo con los datos del formulario
            prestamo.fechaEntrega = fecha_entrega
            prestamo.fechaDevolucion = fecha_devolucion
            prestamo.nombreEntrega.numeroIdentificacion = nombre_entrega
            prestamo.nombreRecibe.numeroIdentificacion = nombre_recibe
            prestamo.nombreElemento = nombre_elemento
            prestamo.valorUnidadElemento = valor_unidad
            prestamo.observacionesPrestamo = observaciones_prestamo
            prestamo.estadoPrestamo = estado_prestamo
            # Resto de la lógica de actualización

            prestamo.save()

            messages.success(request, "El prestamo se ha editado exitosamente")

            consultar_transacciones_url = reverse("consultarTransacciones")
            return redirect(f"{consultar_transacciones_url}?opcion=prestamo")

        except InventarioDevolutivo.DoesNotExist as e:
            # Manejar la excepción y mostrar un mensaje de error
            error_message = f"Elemento no encontrado. Por favor, asegúrate de que el serial sea correcto. Detalles: {e}"
            print(error_message)  # Imprimir mensaje de error en la consola
            return render(
                request,
                "superAdmin/editarPrestamo.html",
                {
                    "prestamo": prestamo,
                    "elemento": elemento,
                    "error_message": error_message,
                },
            )

    # Si la solicitud no es POST, enviar el objeto Prestamo y Elementos a la plantilla
    return render(
        request,
        "superAdmin/editarPrestamo.html",
        {"prestamo": prestamo, "elemento": elemento},
    )


@login_required
@verificar_cuentadante
def editarEntrega_view(request, id):
    # Obtener el objeto Prestamo por su ID
    entrega = get_object_or_404(EntregaConsumible, id=id)
    elemento = None  # Inicializar la variable fuera del bloque try

    if request.method == "POST":
        # Obtener datos del formulario
        cantidad_elemento = request.POST.get("txt_cantidad_prestada")
        observaciones_prestamo = request.POST.get("txt_observaciones_prestamo")

        try:
            # Actualizar los campos del objeto Prestamo con los datos del formulario
            entrega.cantidad_prestada = cantidad_elemento
            entrega.observaciones_prestamo = observaciones_prestamo
            # Resto de la lógica de actualización

            entrega.save()

            messages.success(request, "La Entrega se ha editado exitosamente")

            consultar_transacciones_url = reverse("consultarTransacciones")
            return redirect(f"{consultar_transacciones_url}?opcion=entregas")

        except InventarioConsumible.DoesNotExist as e:
            # Manejar la excepción y mostrar un mensaje de error
            error_message = f"Elemento no encontrado. Por favor, asegúrate de que el serial sea correcto. Detalles: {e}"
            print(error_message)  # Imprimir mensaje de error en la consola
            return render(
                request,
                "superAdmin/editarEntrega.html",
                {
                    "entrega": entrega,
                    "elemento": elemento,
                    "error_message": error_message,
                },
            )

    # Si la solicitud no es POST, enviar el objeto Prestamo y Elementos a la plantilla
    return render(
        request,
        "superAdmin/editarEntrega.html",
        {"entrega": entrega, "elemento": elemento},
    )
    
@login_required
@verificar_cuentadante   
def almacenar_observaciones_view(request, id):
    if request.method == "POST":
        observaciones = request.POST.get('observacionesEntrega', '')

        try:
            prestamo = Prestamo.objects.get(id=id)
            prestamo.observacionesEntrega = observaciones
            prestamo.save()
            
            # Puedes redirigir o devolver un JsonResponse según tus necesidades
            return render(request,"superAdmin/consultarTransacciones.html",)
        except Prestamo.DoesNotExist:
            return render({'success': False, 'error': 'El préstamo no existe'})

    return render(request,"superAdmin/consultarTransacciones.html",)


@login_required
@verificar_cuentadante
def finalizarPrestamo_view(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)

    if request.method == "POST":
        nuevo_estado = request.POST.get("txt_nuevo_estado")
        observaciones = request.POST.get("observacionesEntrega")

        try:
            # Almacena las observaciones
            prestamo.observacionesEntrega = observaciones
            prestamo.save()

            # Cambia el estado del préstamo
            prestamo.estadoPrestamo = nuevo_estado
            prestamo.save()

            # Agrega una variable de contexto para indicar que el préstamo se ha finalizado
            return render(
                request,
                "superAdmin/consultarTransacciones.html",
            )

        except Exception as e:
            messages.error(request, f"Error al actualizar el estado del préstamo: {e}")

    return render(
        request, "superAdmin/consultarTransacciones.html", {"prestamo": prestamo}
    )

@login_required
@verificar_cuentadante
# def finalizarPrestamo_view(request, id):
#     prestamo = get_object_or_404(Prestamo, id=id)

#     if request.method == "POST":
#         nuevo_estado = request.POST.get("txt_nuevo_estado")
#         try:
#             prestamo.estadoPrestamo = nuevo_estado
#             prestamo.save()

#             # Agrega una variable de contexto para indicar que el préstamo se ha finalizado
#             return render(
#                 request,
#                 "superAdmin/consultarTransacciones.html",
#                 {"prestamo": prestamo, "prestamo_finalizado": True},
#             )

#         except Exception as e:
#             messages.error(request, f"Error al actualizar el estado del préstamo: {e}")

#     return render(
#         request, "superAdmin/consultarTransacciones.html", {"prestamo": prestamo}
#     )

@login_required
def reporteelementosactivos(request):
    fecha_inicio = request.GET.get("fecha_inicio", None)
    fecha_fin = request.GET.get("fecha_fin", None)

    if fecha_inicio is None or fecha_fin is None:
        elementosconsu = InventarioConsumible.objects.select_related(
            "productoConsumible"
        ).all()
        elementosdevo = InventarioDevolutivo.objects.select_related("producto").all()
        data = {
            "ElementosConsumibles": elementosconsu,
            "ElementosDevolutivos": elementosdevo,
        }

        return render(request, "superAdmin/reporteelementosactivos.html", data)

    if request.method == "GET":
        elementosconsu = InventarioConsumible.objects.select_related(
            "productoConsumible"
        ).filter(fechaAdquisicion__range=[fecha_inicio, fecha_fin])
        elementosdevo = InventarioDevolutivo.objects.select_related("producto").filter(
            fecha_Registro__range=[fecha_inicio, fecha_fin]
        )
        if not elementosconsu.exists() and not elementosdevo.exists():
            messages.error(request, "No se encontraron elementos para las fechas especificadas.")
            return redirect("reporteelementosactivos")
        data = {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "ElementosConsumibles": elementosconsu,
            "ElementosDevolutivos": elementosdevo,
        }

        return render(request, "superAdmin/reporteelementosactivos.html", data)


@login_required
def reporteelementosprestamo(request):
    fecha_inicio = request.GET.get("fecha_inicio", None)
    fecha_fin = request.GET.get("fecha_fin", None)

    if fecha_inicio is None or fecha_fin is None:
        prestamos = Prestamo.objects.all()

        data = {"prestamos": prestamos}
        return render(request, "superAdmin/reporteelementosprestamo.html", data)

    if request.method == "GET":
        prestamos = Prestamo.objects.filter(
            fechaEntrega__range=[fecha_inicio, fecha_fin]
        )
        if not prestamos.exists():
            messages.error(request, "No se encontraron prestamo para las fechas especificadas.")
            return redirect("reporteelementosprestamos")
        data = {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "prestamos": prestamos,
        }

        return render(request, "superAdmin/reporteelementosprestamo.html", data)


@login_required
def reporteelementosbajas(request):
    fecha_inicio = request.GET.get("fecha_inicio", None)
    fecha_fin = request.GET.get("fecha_fin", None)

    if fecha_inicio is None or fecha_fin is None:
        elementosconsu = InventarioConsumible.objects.select_related(
            "productoConsumible"
        ).all()
        elementosdevo = InventarioDevolutivo.objects.select_related("producto").all()
        data = {
            "ElementosConsumibles": elementosconsu,
            "ElementosDevolutivos": elementosdevo,
        }
        return render(request, "superAdmin/reporteelementosbajas.html", data)

    if request.method == "GET":
        elementosconsu = InventarioConsumible.objects.select_related(
            "productoConsumible"
        ).filter(fechaAdquisicion__range=[fecha_inicio, fecha_fin])
        elementosdevo = InventarioDevolutivo.objects.select_related("producto").filter(
            fecha_Registro__range=[fecha_inicio, fecha_fin]
        )
        data = {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "ElementosConsumibles": elementosconsu,
            "ElementosDevolutivos": elementosdevo,
        }

        if not elementosconsu.exists() and not elementosdevo.exists():
            messages.error(request, "No se encontraron elementos para las fechas especificadas.")
            return redirect("reporteelementosbajas")

        return render(request, "superAdmin/reporteelementosbajas.html", data)


def enviar_correo_notificacion(request, id):
    # Obtener el objeto de la base de datos usando el ID
    prestamo = Prestamo.objects.get(id=id)

    nombre_recibe = prestamo.nombreRecibe.nombres
    apelido_recibe = prestamo.nombreRecibe.apellidos
    nombreCompleto = nombre_recibe + apelido_recibe
    fecha_entrega = prestamo.fechaEntrega
    fecha_devolucion = prestamo.fechaDevolucion
    nombre_producto = prestamo.serialSenaElemento.producto.nombre
    serial_sena = prestamo.serialSenaElemento.serial

    # Lógica para determinar el asunto y el cuerpo del correo usando datos del objeto
    asunto = f"Notificacion Prestamo Elemento Sena CDITI Area de Software"
    cuerpo = (
        f"Hola {nombreCompleto},\n\n"
        f"Notificacion del Prestamo Adquirido:\n"
        f"Fecha de entrega: {fecha_entrega}\n"
        f"Fecha de devolución: {fecha_devolucion}\n"
        f"Nombre del Elemento: {nombre_producto}\n"
        f"Serial Sena: {serial_sena}"
    )

    # Utilizar el campo 'mail' del objeto como destinatario
    destinatario = [prestamo.nombreRecibe.email]

    # Puedes personalizar estos valores según tus necesidades
    remitente = "alertasinventariosena@gmail.com"

    # Enviar el correo
    send_mail(asunto, cuerpo, remitente, destinatario, fail_silently=False)
    messages.success(request, "Notificacion de Prestamo enviada al correo")
    # Mostrar alerta SweetAlert después de enviar el correo directamente en la misma vista
    return "Notificacion de Prestamo Enviada al Correo"


def enviar_correo_desde_boton(request, id):
    prestamo = Prestamo.objects.get(id=id)

    nombre_recibe = prestamo.nombreRecibe.nombres
    apelido_recibe = prestamo.nombreRecibe.apellidos
    nombreCompleto = nombre_recibe + apelido_recibe
    fecha_entrega = prestamo.fechaEntrega
    fecha_devolucion = prestamo.fechaDevolucion
    nombre_producto = prestamo.serialSenaElemento.producto.nombre
    serial_sena = prestamo.serialSenaElemento.serial

    # Lógica para determinar el asunto y el cuerpo del correo usando datos del objeto
    asunto = f"***Recordatorio Devolucion Elemento Sena CDITI Area de Software***"
    cuerpo = (
        f"Hola {nombreCompleto},\n\n"
        f"**** Recordatorio de la Devolucion del elemento Adquirido:*****\n"
        f"Fecha de entrega: {fecha_entrega}\n"
        f"Fecha de devolución: {fecha_devolucion}\n"
        f"Nombre del Elemento: {nombre_producto}\n"
        f"Serial Sena: {serial_sena}"
    )

    # Utilizar el campo 'mail' del objeto como destinatario
    destinatario = [prestamo.nombreRecibe.email]

    # Puedes personalizar estos valores según tus necesidades
    remitente = "alertasinventariosena@gmail.com"

    # Enviar el correo
    send_mail(asunto, cuerpo, remitente, destinatario, fail_silently=False)

    # Mostrar alerta SweetAlert después de enviar el correo directamente en la misma vista
    return redirect("homedash")
