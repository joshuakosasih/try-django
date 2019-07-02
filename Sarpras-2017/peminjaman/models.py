from django.db import models
from ruangan.models import Ruangan
from peminjam.models import Peminjam
from datetime import datetime
import os

def peminjaman_foto_dir(instance, filename):
    now = datetime.now().date()
    if instance.id is None:
        try:
            nextid = (Ruangan.objects.latest('id')).id + 1
        except(Ruangan.DoesNotExist):
            nextid = 0
    else:
        nextid = instance.id

    fname, file_extension = os.path.splitext(filename)
    return 'peminjaman/{0}/{1}_{2}{3}'.format(now.year, nextid, instance.no_laporan, file_extension)

class Peminjaman(models.Model):
    no_laporan = models.CharField(blank=True, max_length=500, db_index=True)

    peminjam = models.ForeignKey(Peminjam,on_delete=models.CASCADE, db_index=True)
    ruangan = models.ForeignKey(Ruangan, on_delete=models.CASCADE, db_index=True)

    waktu_awal = models.DateTimeField(auto_now=False, auto_now_add=False, db_index=True)
    waktu_akhir = models.DateTimeField(auto_now=False, auto_now_add=False, db_index=True)

    jumlah_tagihan = models.DecimalField(max_digits=65, decimal_places=2, default=0)
    waktu_bayar = models.DateField(blank=True, null=True) # Apabila bernilai null maka berarti belum dibayar

    deskripsi = models.CharField(max_length=1000, blank=True)

    foto = models.ImageField(upload_to=peminjaman_foto_dir, max_length=500, blank=True)

    def __str__(self):
        return (self.peminjam.__str__() +' : '+ self.ruangan.__str__() +' ( '+ self.waktu_awal.__str__() +' - '+ self.waktu_akhir.__str__()+ ' )')

    def is_collision(self, Peminjaman_new):
        new_time_start = Peminjaman_new.waktu_awal.replace(tzinfo=None)
        new_time_finish = Peminjaman_new.waktu_akhir.replace(tzinfo=None)
        old_time_start = self.waktu_awal.replace(tzinfo=None)
        old_time_finish = self.waktu_akhir.replace(tzinfo=None)
        return (new_time_start <= old_time_start <= new_time_finish) or (old_time_start <= new_time_start <= old_time_finish)

    def get_all_conflicted_set(self):
        if(self.waktu_akhir.year == self.waktu_awal.year):
            conflicted_candidates = Peminjaman.objects.filter(ruangan = self.ruangan).filter(waktu_awal__year = self.waktu_awal.year)
        else:
            conflicted_candidates = Peminjaman.objects.filter(ruangan = self.ruangan).filter(waktu_awal__year = self.waktu_awal.year) | \
                                    Peminjaman.objects.filter(ruangan = self.ruangan).filter(waktu_awal__year = self.waktu_akhir.year)
        conflicteds = []

        for candidate in conflicted_candidates:
            if self.is_collision(candidate):
                conflicteds.append(candidate)

        return conflicteds

