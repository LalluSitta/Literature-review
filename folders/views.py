from django.shortcuts import render, get_object_or_404, redirect
from .models import Folder
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Homepage 
def home(request):
    return render(request, 'homepage/index.html')

#Lista delle cartelle dell'utente autenticato
@login_required  # Assicura che solo gli utenti loggati possano accedere
def lista_cartelle(request):
    cartelle = Folder.objects.filter(utente=request.user)  # Filtra per utente loggato
    return render(request, "folders/folders.html", {"cartelle": cartelle})

# Dettaglio di una cartella con le ricerche al suo interno
def dettaglio_cartella(request, cartella_id):
    # Recupera la cartella, assicurandosi che appartenga all'utente attuale
    cartella = get_object_or_404(Folder, id=cartella_id, utente=request.user)
    researches = cartella.researches.all()  # Prende tutti i documenti della cartella
    return render(request, 'research_list.html', {'cartella': cartella, 'researches': researches})    

# Creazione di una nuova cartella
@login_required
def crea_cartella_ajax(request):
    if request.method == "POST":
        nome_cartella = request.POST.get("nome").strip()

         # Controlla se l'utente ha già una cartella con lo stesso nome
        if Folder.objects.filter(nome=nome_cartella, utente=request.user).exists():
            return JsonResponse({"success": False, "error": "Hai già una cartella con questo nome!"})

        # Crea la cartella per l'utente autenticato
        cartella = Folder.objects.create(nome=nome_cartella, utente=request.user)
        return JsonResponse({"success": True, "id": cartella.id, "nome": cartella.nome})

    return JsonResponse({"success": False, "error": "Errore durante la creazione"})

# Modifica il nome di una cartella
@csrf_exempt
def modifica_cartella(request, cartella_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cartella = get_object_or_404(Folder, id=cartella_id)
            cartella.nome = data.get("nome", cartella.nome)
            cartella.save()
            return JsonResponse({"success": True, "nome": cartella.nome})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Invalid request"})

# Eliminazione di una cartella 
@csrf_exempt
def elimina_cartella(request, cartella_id):
    if request.method == "POST":
        cartella = get_object_or_404(Folder, id=cartella_id)
        cartella.delete()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "error": "Invalid request"})