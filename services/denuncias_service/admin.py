from django.contrib import admin
from .models import Denuncia, DenunciaEvidencia

class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_type_display', 'status', 'region', 'district', 'created_at')
    list_filter = ('status', '_type', 'region', 'created_at')
    search_fields = ('description', 'user__email', 'user__dni', 'district', 'region')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user',)
        }),
        ('Detalles de la Denuncia', {
            'fields': ('_type', 'description', 'status')
        }),
        ('Ubicación', {
            'fields': ('region', 'district', 'lat', 'lon')
        }),
        ('Fechas', {
            'fields': ('created_at',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def get_type_display(self, obj):
        return obj.get__type_display()
    get_type_display.short_description = 'Tipo'


admin.site.register(Denuncia, DenunciaAdmin)
admin.site.register(DenunciaEvidencia)