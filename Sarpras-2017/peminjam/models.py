from django.db import models

class Peminjam(models.Model):
    nama = models.CharField(max_length=250, unique=True, db_index=True)
    deskripsi = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.nama
