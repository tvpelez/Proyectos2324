from django.contrib import admin
from .models import (
    UsuariosSena,
    ProductosInventarioDevolutivo,
    InventarioDevolutivo,
    ProductosInventarioConsumible,
    InventarioConsumible,
    Prestamo,
    EntregaConsumible,
)
from .choices import roles, cuentadantes


class ServicioAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "update")


class InventarioDevolutivoInline(admin.TabularInline):
    model = InventarioDevolutivo
    extra = 1


class ProductosInventarioDevolutivoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "categoria", "estado", "disponibles"]
    inlines = [InventarioDevolutivoInline]


class InventarioConsumibleInline(admin.TabularInline):
    model = InventarioConsumible
    extra = 1


class ProductosInventarioConsumibleAdmin(admin.ModelAdmin):
    list_display = [
        "nombreElemento",
        "categoriaElemento",
        "estadoElemento",
        "disponible",
    ]
    inlines = [InventarioConsumibleInline]


class UsuariosSenaAdmin(admin.ModelAdmin):
    list_display = [
        "nombres",
        "apellidos",
        "tipoIdentificacion",
        "numeroIdentificacion",
        "email",
    ]
    search_fields = ["nombres", "apellidos", "numeroIdentificacion"]
    list_filter = ["rol", "cuentadante", "tipoContrato"]


# Registrar los modelos con su personalización
admin.site.register(UsuariosSena, UsuariosSenaAdmin)
admin.site.register(ProductosInventarioDevolutivo, ProductosInventarioDevolutivoAdmin)
admin.site.register(ProductosInventarioConsumible, ProductosInventarioConsumibleAdmin)
admin.site.register(Prestamo)
admin.site.register(EntregaConsumible)
