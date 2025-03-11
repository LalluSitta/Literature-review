from django.urls import path
from . import views
from articoli.views import salva_ricerche, ricerche_salvate

# Definisce il namespace per evitare conflitti con altre app Django
app_name = "folders"

urlpatterns = [
    # Homepage dell'app folders
    path("", views.home, name='home'),

    # Gestione cartelle
    path('folders', views.lista_cartelle, name='lista_cartelle'), # Mostra l'elenco delle cartelle dell'utente
    path('cartella/<int:cartella_id>/', views.dettaglio_cartella, name='dettaglio_cartella'), # Dettagli di una cartella specifica
    path('cartella/crea/ajax/', views.crea_cartella_ajax, name='crea_cartella_ajax'), # Creazione di una cartella via AJAX
    path('cartella/<int:cartella_id>/modifica/', views.modifica_cartella, name='modifica_cartella'), # Modifica di una cartella
    path('cartella/<int:cartella_id>/elimina/', views.elimina_cartella, name='elimina_cartella'), # Eliminazione di una cartella

    # Salvataggio e recupero delle ricerche associate a una cartella
    path("cartella/<int:folder_id>/salva-ricerche/", salva_ricerche, name="salva_ricerche"),
    path("cartella/<int:folder_id>/ricerche-salvate/", ricerche_salvate, name="ricerche_salvate"),

    
]