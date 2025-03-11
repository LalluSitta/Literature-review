from django import forms
from .models import Articoli

# Definisce un modulo di input basato sul modello "Articoli",
# che consente di gestire i campi del modello nel form di input dell'utente

class ArticoloForm(forms.ModelForm):
    class Meta:
        model = Articoli
        fields = ["titolo", "autore", "anno", "citazioni", "fonte", "lingua", "tipo_documento", "text","status"]
        widgets = {
            "anno": forms.NumberInput(attrs={"placeholder": "Anno di pubblicazione"}),
            "citazioni": forms.NumberInput(attrs={"placeholder": "Numero di citazioni"}),
            "lingua": forms.Select(choices=Articoli.LINGUA_CHOICES),
            "status": forms.Select(choices=Articoli.STATUS_CHOICES),
            "text": forms.Textarea(attrs={"rows": 4, "placeholder": "Testo della ricerca"}),
            
        }
