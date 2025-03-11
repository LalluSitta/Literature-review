from django.contrib import admin
from .models import Folder

# Configura l'interfaccia di amministrazione per il modello Folder
class FolderAdmin(admin.ModelAdmin):
    list_display = ('nome', 'utente', 'data_creazione', 'num_ricerche')  # Mostra il numero di ricerche
    search_fields = ('nome', 'utente__username')
    list_filter = ('data_creazione', 'utente')
    ordering = ('-data_creazione',)

    # Metodo per visualizzare il numero di ricerche associate alla cartella
    def num_ricerche(self, obj):
        return obj.num_ricerche
    num_ricerche.short_description = "Numero di Ricerche"

# Registra il modello Folder nell'admin di Django
admin.site.register(Folder, FolderAdmin)
