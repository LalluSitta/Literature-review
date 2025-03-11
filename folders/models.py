from django.db import models
import os
from userauths.models import User



def file_upload_path(instance, filename):
    """Genera un percorso di upload unico per ogni cartella."""
    return os.path.join(f'cartelle/{instance.id}/', filename)

class Folder(models.Model):
    nome = models.CharField(max_length=255) 
    data_creazione = models.DateTimeField(auto_now_add=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders")

    # Assicura che un utente non possa avere due cartelle con lo stesso nome
    class Meta:
        unique_together = ('nome', 'utente')  


    def __str__(self):
        """Restituisce una rappresentazione leggibile della cartella."""
        return f"{self.nome} ({self.utente.username})"
    
    @property
    def num_ricerche(self):
        """Restituisce il numero di ricerche associate a questa cartella."""
        return self.articoli.count()
