from django.db import models
from peminjaman.models import Peminjaman
from datetime import date

class Log(models.Model):
    peminjaman = models.ForeignKey(Peminjaman, blank=True, null=True, on_delete=models.SET_NULL)
    peminjaman_str = models.CharField(blank=True, max_length=500)
    tanggal = models.DateField(auto_now_add=True, db_index=True)
    deskripsi = models.CharField(blank=True, max_length=1000) #Bernilai deskripsi yang akan ditunjukan apabila object peminjaman sudah dihapus

    CREATE = 'Buat'
    UPDATE = 'Ubah'
    DELETE = 'Hapus'
    PILIHAN_TIPE_AKSI = (
        (CREATE, 'Buat'),
        (UPDATE, 'Ubah'),
        (DELETE, 'Hapus'),
    )
    aksi = models.CharField(max_length=50, choices=PILIHAN_TIPE_AKSI, default=UPDATE)



