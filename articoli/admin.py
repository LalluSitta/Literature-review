from django.contrib import admin
from .models import Articoli

class ArticoliAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'autore', 'anno', 'fonte', 'citazioni', 'tipo_documento', 'lingua', 'folder', 'status')  # Campi visibili nella lista admin
    list_filter = ('anno', 'fonte', 'tipo_documento', 'lingua', 'folder', 'status')  # Filtri laterali
    search_fields = ('titolo', 'autore', 'fonte', 'folder__nome')  # Permette la ricerca per titolo, autore e cartella
    ordering = ('-anno', 'titolo')  # Ordina gli articoli per anno decrescente e titolo
    list_editable = ('status','tipo_documento')  # Permette di modificare lo stato direttamente nella lista
    readonly_fields = ('id',)  # Il campo ID non deve essere modificabile

    fieldsets = (
        ('Informazioni Generali', {
            'fields': ('titolo', 'autore', 'anno', 'fonte', 'citazioni', 'tipo_documento', 'lingua','status','folder')
        }),
        ('Testo della Ricerca', {
            'fields': ('text',),
            'classes': ('collapse',),  # Rende il campo "text" collassabile
        }),
    )


admin.site.register(Articoli, ArticoliAdmin)
