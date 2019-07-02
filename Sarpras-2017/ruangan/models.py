from django.db import models
from datetime import datetime
import os

def ruangan_foto_dir(instance, filename):
    if instance.id is None:
        try:
            nextid = (Ruangan.objects.latest('id')).id + 1
        except(Ruangan.DoesNotExist):
            nextid = 0
    else:
        nextid = instance.id

    fname, file_extension = os.path.splitext(filename)
    return 'ruangan/{0}_{1}{2}'.format(nextid, instance.nama, file_extension)

class Ruangan(models.Model):

    nama = models.CharField(max_length=250, unique=True, db_index=True)
    harga = models.BigIntegerField(default=0)
    deskripsi = models.CharField(max_length=1000, blank=True)

    RUANG = 'Ruang'
    SELASAR = 'Selasar'
    LAPANGAN = 'Lapangan'
    PILIHAN_TIPE_RUANG = (
        (RUANG, 'Ruang'),
        (SELASAR, 'Selasar'),
        (LAPANGAN, 'Lapangan'),
    )
    tipe = models.CharField(max_length=50, choices=PILIHAN_TIPE_RUANG, default=SELASAR)

    foto = models.ImageField(upload_to=ruangan_foto_dir, max_length=500, blank=True)
    restricted = models.BooleanField(default=False, db_index=True)

    warna = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nama + ' - ' + self.tipe