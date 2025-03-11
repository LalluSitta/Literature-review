from django.urls import path
from .views import articoli_per_cartella, importa_articoli, ricerca_articoli, aggiungi_articolo,modifica_stato_articolo, salva_ricerche, ricerche_salvate, elimina_articolo

app_name = "articoli"


urlpatterns = [

    # Visualizza tutti gli rticoli
    path('cartella/<int:folder_id>/articoli/', articoli_per_cartella, name='articoli_per_cartella'),
    
    # Importa articoli in una cartella specifica
    path("articoli/importa-articoli/<str:folder_id>/", importa_articoli, name="importa_articoli"),
    
    # Effettua una ricerca di articoli all'interno di una cartella
    path("ricerca/<int:folder_id>/", ricerca_articoli, name="ricerca_articoli"),

    #Aggiunta di un articolo
    path('articoli/aggiungi/<int:folder_id>/', aggiungi_articolo, name="aggiungi_articolo"),

    # Modifica lo stato di un articolo
    path("modifica-stato/", modifica_stato_articolo, name="modifica_stato_articolo"),


    #Salvataggio ricerche con stato "Preso"
    path("cartella/<int:folder_id>/salva-ricerche/", salva_ricerche, name="salva_ricerche"),
    
    # Recupera le ricerche salvate di una cartella
    path("cartella/<int:folder_id>/ricerche-salvate/", ricerche_salvate, name="ricerche_salvate"),

    # Elimina un articolo
    path("articoli/elimina-articolo/", elimina_articolo, name="elimina_articolo"),

    
]