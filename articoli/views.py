from django.shortcuts import render, get_object_or_404, redirect
from .models import Articoli, RicercaSalvata
from folders.models import Folder
from django.http import JsonResponse
import csv
import io
from django.db.models import Q
from .forms import ArticoloForm
from django.contrib import messages
from django.db import IntegrityError
import traceback  # Importa per il debug
import json
from django.views.decorators.csrf import csrf_exempt # Necessario per richieste AJAX senza token CSRF

# Recupera gli articoli di una cartella specifica e li visualizza nella lista
def articoli_per_cartella(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    articoli = Articoli.objects.filter(folder=folder)

    context = {
        'folder': folder,
        'articoli': articoli
    }
    return render(request, 'articoli/lista_articoli.html', context)


# Importa articoli da un file CSV in una cartella specifica
def importa_articoli(request, folder_id):
    try:
        if request.method == "POST" and request.FILES.get("csv_file"):
            csv_file = request.FILES["csv_file"]

            if not csv_file.name.endswith(".csv"):
                return JsonResponse({"success": False, "error": "⚠️ Il file deve essere un CSV!"})

            data_set = csv_file.read().decode("utf-8", errors="replace")
            io_string = io.StringIO(data_set)
            reader = csv.reader(io_string, delimiter=",")

            # Definisci i nomi delle colonne richieste
            colonne_richieste = ["Title", "Author", "Year", "Source title", "Cited by", "Document Type", "Language","Testo della Ricerca"]
            
            header = next(reader)
            if header != colonne_richieste:
                return JsonResponse({"success": False, "error": "⚠️ Il file CSV non ha le colonne corrette!"})

            folder = get_object_or_404(Folder, id=folder_id)

            articoli_importati = []
            articoli_duplicati = 0  # Contatore degli articoli ignorati perché già presenti


            for row in reader:
                titolo = str(row[0]).strip("(),'\"")  # Rimuove parentesi, virgole e virgolette
                autore = str(row[1]).strip("(),'\"")
                anno = int(row[2]) if row[2].isdigit() else None
                fonte = str(row[3]).strip("(),'\"")
                citazioni = int(row[4]) if row[4].isdigit() else 0
                tipo_documento = str(row[5]).strip("(),'\"")
                lingua = str(row[6]).strip("(),'\"")
                text = str(row[7]).strip("(),'\"") if len(row) > 7 else ""
                folder=folder

                
                # Verifica se l'articolo è già presente nella cartella
                if Articoli.objects.filter(titolo=titolo, anno=anno, folder=folder).exists():
                    articoli_duplicati += 1
                    continue  # Salta l'aggiunta dell'articolo

                # Crea e salva l'articolo
                articolo = Articoli.objects.create(
                    titolo=titolo,
                    autore=autore,
                    anno=anno,
                    fonte=fonte,
                    citazioni = citazioni,
                    tipo_documento=tipo_documento,
                    lingua=lingua,
                    text=text,
                    status="Scartato",
                    folder=folder
                )

                articoli_importati.append({
                    "titolo": articolo.titolo,
                    "autore": articolo.autore,
                    "anno": articolo.anno,
                    "fonte": articolo.fonte,
                    "citazioni": articolo.citazioni,
                    "tipo_documento": articolo.tipo_documento,
                    "lingua": articolo.lingua,
                    "text": articolo.text,
                })
            
            
            total_articoli= Articoli.objects.filter(folder=folder).count()
            
            # **Costruisce il messaggio finale**
            if not articoli_importati and articoli_duplicati > 0:
                return JsonResponse({"success": False, "error": f"⚠️ {articoli_duplicati} articoli erano già presenti e non sono stati importati!", "total_articoli": total_articoli})
            
            
            return JsonResponse({
                "success": True,
                "message": f"✅ {len(articoli_importati)} articoli importati con successo! {articoli_duplicati} duplicati ignorati.",
                "articoli": articoli_importati,
                "total_articoli": total_articoli
            })

        return JsonResponse({"success": False, "error": "❌ Errore nell'importazione del file."})
    
    except Exception as e:
        print("🔥 ERRORE GENERALE:", e)
        print(traceback.format_exc())  # Stampa il traceback completo per il debug
        return JsonResponse({"success": False, "error": "❌ Errore interno del server. Controlla la console Django."})

# Effettua la ricerca di articoli in base a titolo, autore, stato e lingua
def ricerca_articoli(request, folder_id):
    """View per la ricerca di articoli in base ai parametri scelti"""
    
    # Recupera i parametri della ricerca
    query = request.GET.get("q", "").strip()
    stato = request.GET.get("stato", "")
    lingua = request.GET.get("lingua", "")

    # Filtra gli articoli per la cartella selezionata
    articoli = Articoli.objects.filter(folder_id=folder_id)

    # Se è presente una query di ricerca (per titolo, autore, anno o tipo)
    if query:
        articoli = articoli.filter(
            Q(titolo__icontains=query) |
            Q(autore__icontains=query) |
            Q(anno__icontains=query) |
            Q(tipo_documento__icontains=query)
        )

    # Se l'utente ha selezionato uno stato (Preso/Scartato)
    if stato:
        articoli = articoli.filter(status=stato)

    # Se l'utente ha selezionato una lingua specifica
    if lingua:
        articoli = articoli.filter(lingua=lingua)
        print(f"Lingua ricevuta: '{lingua}'")

    # Converti gli articoli in JSON per restituirli in risposta AJAX
    articoli_data = list(articoli.values(
        "id", "titolo", "autore", "anno", "citazioni", "fonte", "lingua",
        "tipo_documento", "text", "status"
    ))

    return JsonResponse({"articoli": articoli_data})

# Aggiunge manualmente un articolo a una cartella
def aggiungi_articolo(request, folder_id):
    folder = Folder.objects.get(id=folder_id)  # Trova la cartella corrente
    form = ArticoloForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            try:
                articolo = form.save(commit=False)
                articolo.folder = folder  # Assegna l'articolo alla cartella corrente
                articolo.save()
                messages.success(request, "Articolo aggiunto con successo!")
                return redirect("articoli:articoli_per_cartella", folder_id=folder.id)  # Se hai un namespace

            except IntegrityError:
                messages.error(request, "Esiste già un articolo con questo titolo in questa cartella.")
    
    return render(request, "articoli/aggiungi_articolo.html", {"form": form, "folder": folder})


# Modifica lo stato di un articolo (da "Preso" a "Scartato" e viceversa)
def modifica_stato_articolo(request):
    if request.method == "POST":
        data = json.loads(request.body)
        articolo_id = data.get("id")  # Usa l'ID anziché il titolo
        nuovo_stato = data.get("nuovo_stato")

        try:
            articolo = Articoli.objects.get(id=articolo_id)  # Usa il filtro corretto
            articolo.status = nuovo_stato
            articolo.save()
            return JsonResponse({"success": True})
        except Articoli.DoesNotExist:
            return JsonResponse({"success": False, "error": "❌ Errore: Articolo non trovato nel database."})

    return JsonResponse({"success": False, "error": "❌ Errore nella richiesta."})


# Salva gli articoli con stato "Preso" in una cartella
def salva_ricerche(request, folder_id):
    if request.method == "POST":
        folder = get_object_or_404(Folder, id=folder_id)
        articoli_presi = Articoli.objects.filter(folder=folder, status="Preso")

        if articoli_presi.exists():
            for articolo in articoli_presi:

                articolo.status = "Preso"
                articolo.save()

                RicercaSalvata.objects.get_or_create(
                    folder=folder,
                    articolo=articolo,
                )

            return JsonResponse({"success": True, "message": "Ricerche salvate con successo!"})
        else:
            return JsonResponse({"success": False, "message": "Nessun articolo selezionato per il salvataggio!"})

    return JsonResponse({"success": False, "message": "Metodo non consentito!"})

# Recupera gli articoli salvati con stato "Preso"
def ricerche_salvate(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    ricerche = RicercaSalvata.objects.filter(folder=folder, articolo__status="Preso").select_related("articolo")

    return render(request, "articoli/ricerche_salvate.html", {"folder": folder, "ricerche": ricerche},)



# Elimina un articolo cambiandone lo stato in "Scartato"
@csrf_exempt  # Se usi fetch POST senza form Django, serve per evitare errori CSRF
def elimina_articolo(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Leggi il corpo della richiesta JSON
            article_id = data.get("id")  # Prendi l'ID dell'articolo

            if not article_id:
                return JsonResponse({"success": False, "error": "ID articolo mancante"}, status=400)

            articolo = Articoli.objects.get(id=article_id)  # Trova l'articolo nel DB
            articolo.status = "Scartato"  # Imposta lo stato a "Scartato"
            articolo.save()  # Salva la modifica

            return JsonResponse({"success": True, "message": "Articolo eliminato e stato aggiornato"})

        except Articoli.DoesNotExist:
            return JsonResponse({"success": False, "error": "Articolo non trovato"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Errore nel parsing JSON"}, status=400)

    return JsonResponse({"success": False, "error": "Metodo non consentito"}, status=405)


