from django.db import models
import shortuuid
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from folders.models import Folder


class Articoli(models.Model):
        
    id = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    titolo = models.CharField(max_length=255, verbose_name="Title")  # Titolo dell'articolo
    autore = models.CharField(max_length=255, verbose_name="Author")  # Autori dell'articolo
    anno = models.PositiveIntegerField(null=True, blank=True, verbose_name="Year")  # Anno di pubblicazione
    fonte = models.CharField(max_length=255, verbose_name="Source Title")  # Fonte della pubblicazione
    citazioni = models.PositiveIntegerField(default=0, verbose_name="Cited by")  # Numero di citazioni ricevute
    tipo_documento = models.CharField(max_length=50, verbose_name="Document Type")  # Tipo di documento (es. articolo, review, conferenza)
    folder = models.ForeignKey("folders.Folder", on_delete=models.CASCADE, related_name="articoli")
    
    # Nuovo campo per il testo della ricerca
    text = models.TextField(verbose_name="Testo della Ricerca", blank=True, null=True)
    
    
    
    STATUS_CHOICES = [
        ('Preso', 'Preso'),
        ('Scartato', 'Scartato'),
    ]

    # Stato dell'articolo, con valore predefinito "Scartato"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Scartato")

    def save(self, *args, **kwargs):
        """Garantisce che lo status sia solo 'Preso' o 'Scartato'."""
        if self.status not in dict(self.STATUS_CHOICES):
            self.status = "Scartato"  # Imposta un valore di default valido
        super().save(*args, **kwargs)


    # Scelte per la lingua dell'articolo
    LINGUA_CHOICES = [
        ("IT", "Italian"),
        ("EN", "English"),
        ("FR", "French"),
        ("ES", "Spanish"),
        ("DE", "German"),
        ("LT", "Lituan"),
        ("JP", "Japanese"),
        ("CH", "Chinese"),
        ("RU", "Russian"),
    ]

    #Articoli in base alla lingua
    lingua = models.CharField(max_length=2, choices=LINGUA_CHOICES, default='EN', verbose_name="Lingua")

    # Vincolo di unicità: titolo presente solo una volta per ogni cartella
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['titolo', 'folder'], name="unique_research_per_folder")
        ]

    def __str__(self):
        return f"{self.titolo} ({self.anno}) - {self.folder.nome} [{self.get_lingua_display()}]"
    

# Associa un articolo a una cartella specifica, salvando la ricerca
class RicercaSalvata(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    articolo = models.ForeignKey(Articoli, on_delete=models.CASCADE)
    salvato_il = models.DateTimeField(auto_now_add=True)

    # Vincolo di unicità per evitare duplicati 
    class Meta:
        unique_together = ("folder", "articolo") 