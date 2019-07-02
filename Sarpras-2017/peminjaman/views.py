import calendar

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q

from .models import Peminjaman
from ruangan.models import Ruangan
from peminjam.models import Peminjam
from log.models import Log

from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import json
import re

# Peminjaman index view, mostly for debugging purpose
@login_required
def index(request, errormsg=''):
    all_peminjaman = Peminjaman.objects.all()
    all_ruangan = Ruangan.objects.all()
    all_peminjam = Peminjam.objects.all()
    return render(request, 'peminjaman/index.html', {
        'all_peminjaman' : all_peminjaman,
        'all_ruangan' : all_ruangan,
        'all_peminjam' : all_peminjam,
        'error' : errormsg
    })


@login_required
def kalender(request, errormsg=''):
    return render(request, 'peminjaman/kalender_admin.html', {})

def kalender_umum(request, errormsg=''):
    return render(request, 'peminjaman/kalender_umum.html', {})


# Return a form which'll be used to add new Peminjaman object to model
@login_required
def formadd(request):

    input_peminjam = ''
    input_ruangan = ''
    tanggal_awal = request.POST.get('waktu_awal_0', datetime.now().strftime("%Y-%m-%d")) # format tanggal : %Y-%m-%d
    tanggal_akhir = request.POST.get('waktu_akhir_0', datetime.now().strftime("%Y-%m-%d")) # format tanggal : %Y-%m-%d
    pukul_awal = request.POST.get('waktu_awal_1', '00:00') # format waktu : %H:%M
    pukul_akhir = request.POST.get('waktu_akhir_1', '00:00') # format waktu : %H:%M
    input_deskripsi = request.POST.get('deskripsi', '')
    input_tagihan = request.POST.get('harga', 0.00)
    input_tagihan = float(input_tagihan)
    waktu_bayar_t = None
    if input_tagihan == 0:
        waktu_bayar_t = date.today()
    input_nomor_surat = request.POST.get('nomor_surat', '')
    input_diskon = request.POST.get('discount', 0) # only for minus of input_tagihan

    errormsg = []
    messages = []
    obj_ruangan = None
    if request.method == 'POST':

        # Ambil input tagihan dan Olah tagihan setelah dikurangi diskon
        input_tagihan = request.POST['harga']
        input_diskon = request.POST['discount']

        if float(input_tagihan) > 0:
            input_tagihan = float(input_tagihan)
            decimal_diskon = float(input_diskon) / float(100)
            input_tagihan = (1-decimal_diskon) * input_tagihan
            if input_tagihan <= 0:
                input_tagihan = 0
                waktu_bayar_t = date.today()
            else:
                waktu_bayar_t = None
        else:
            waktu_bayar_t = date.today()

        # Ambil data hasil input dari user
        input_peminjam = request.POST['peminjam']
        input_ruangan = request.POST['ruangan']

        # Ambil dan parsing tanggal-jam mulai pinjam dari form
        tanggal_mulai_pinjam = datetime.strptime(tanggal_awal, "%Y-%m-%d")
        mulai_pinjam = datetime.strptime(pukul_awal, "%H:%M")
        tanggal_mulai_pinjam = tanggal_mulai_pinjam.replace(hour=mulai_pinjam.hour, minute=mulai_pinjam.minute)

        # Ambil dan parsing tanggal-jam selesai pinjam dari form
        tanggal_selesai_pinjam = datetime.strptime(tanggal_akhir, "%Y-%m-%d")
        akhir_pinjam = datetime.strptime(pukul_akhir, "%H:%M")
        tanggal_selesai_pinjam = tanggal_selesai_pinjam.replace(hour=akhir_pinjam.hour, minute=akhir_pinjam.minute)

        # Mengecek tanggal mulai kurang dari tanggal selesai
        temp_mulai = tanggal_mulai_pinjam.replace(tzinfo=None)
        temp_selesai = tanggal_selesai_pinjam.replace(tzinfo=None)
        if temp_mulai >= temp_selesai:
            errormsg += ['Waktu mulai harus kurang dari waktu selesai']

        if not input_peminjam:
            errormsg += ['Harap pilih peminjam yang valid']
        if not input_ruangan:
            errormsg += ['Harap pilih ruangan yang valid']

        # Jika belum ditemukan error
        if not errormsg:

            # Ambil objek Peminjam dan Ruangan
            obj_peminjam = Peminjam.objects.get(id=input_peminjam)
            obj_ruangan = Ruangan.objects.get(id=input_ruangan)

            # Membuat object peminjaman yang sesuai, BELUM DI-SAVE
            new_peminjaman = Peminjaman(no_laporan=input_nomor_surat,
                                        peminjam=obj_peminjam,
                                        ruangan=obj_ruangan,
                                        jumlah_tagihan=input_tagihan,
                                        waktu_bayar = waktu_bayar_t,
                                        waktu_awal=tanggal_mulai_pinjam,
                                        waktu_akhir=tanggal_selesai_pinjam,
                                        deskripsi=input_deskripsi)

            # Mengecek apakah ada peminjaman yang bentrok,
            collision = new_peminjaman.get_all_conflicted_set()

            # Apabila ada bentrok, print semua jadwal yang bentrok, dan kembalikan form
            if(collision):
                errormsg += ['Terdapat jadwal yang bentrok :']
                for peminjaman in collision:
                    errormsg += [peminjaman.__str__(), ]

            # Jika tidak, maka simpan peminjaman, dan kembali ke index
            else:
                if int(input_diskon) > 0:
                    input_deskripsi = input_deskripsi + '\nDiskon : ' + input_diskon + ' %'
                    new_peminjaman.deskripsi = input_deskripsi

                    if len(request.FILES) != 0:
                        new_peminjaman.foto = request.FILES['foto']
                    else:
                        new_peminjaman.foto = None
                try:
                    new_peminjaman.save()
                    new_log = Log(peminjaman=new_peminjaman,
                                  peminjaman_str=new_peminjaman.__str__(),
                                  tanggal=date.today(),
                                  deskripsi="",
                                  aksi="Buat")
                    new_log.save()
                except Exception as e:
                    messages += ["Unhandled Exception", ]
                else:
                    if request.POST['save'] == "Save":
                        return redirect(reverse('peminjaman:index'))
                    else:
                        all_peminjam = Peminjam.objects.all()
                        all_ruangan = Ruangan.objects.all()
                        errormsg = []
                        messages = []
                        if obj_ruangan: input_tipe = obj_ruangan.tipe
                        else: input_tipe = ""

                        return render(request, 'peminjaman/add.html', {
                            'all_peminjam': all_peminjam,
                            'all_ruangan': all_ruangan,
                            'error': errormsg,
                            'message': messages,
                            'input_peminjam': input_peminjam,
                            'input_tipe': input_tipe,
                            'input_ruangan': input_ruangan,
                            'input_deskripsi': '',
                            'tanggal_awal': datetime.now().strftime("%Y-%m-%d"),
                            'pukul_awal': '00:00',
                            'tanggal_akhir': datetime.now().strftime("%Y-%m-%d"),
                            'pukul_akhir': '00:00',
                            'harga': 0.00,
                            'diskon': 0,
                            'nomor_surat': input_nomor_surat,
                            'waktu_bayar': date.today(),
                        })

    # Apabila tidak redirect ke index, maka kirim form
    all_peminjam = Peminjam.objects.all()
    all_ruangan = Ruangan.objects.all()
    if obj_ruangan: input_tipe = obj_ruangan.tipe
    else: input_tipe = ""

    return render(request, 'peminjaman/add.html', {
        'all_peminjam': all_peminjam,
        'all_ruangan': all_ruangan,
        'error': errormsg,
        'message': messages,
        'input_peminjam': input_peminjam,
        'input_tipe': input_tipe,
        'input_ruangan': input_ruangan,
        'input_deskripsi': input_deskripsi,
        'tanggal_awal': tanggal_awal,
        'pukul_awal': pukul_awal,
        'tanggal_akhir': tanggal_akhir,
        'pukul_akhir': pukul_akhir,
        'harga': input_tagihan.__str__(),
        'diskon': input_diskon,
        'nomor_surat': input_nomor_surat,
        'waktu_bayar': waktu_bayar_t,
    })


# Return a form which'll be used to edit peminjaman object to model
@login_required
def formedit(request, peminjaman_id = 0):

    # Berusaha mendapat model peminjam yang ingin diubah
    try:
        selected_peminjaman = Peminjaman.objects.get(id=peminjaman_id)
    except Exception as e:
        return redirect(reverse('peminjaman:index'))

    input_peminjam = selected_peminjaman.peminjam.id
    input_ruangan = selected_peminjaman.ruangan.id
    tanggal_awal = request.POST.get('waktu_awal_0', selected_peminjaman.waktu_awal.date().isoformat())  # format tanggal : %Y-%m-%d
    tanggal_akhir = request.POST.get('waktu_akhir_0', selected_peminjaman.waktu_akhir.date().isoformat())  # format tanggal : %Y-%m-%d
    pukul_awal = request.POST.get('waktu_awal_1', selected_peminjaman.waktu_awal.time().strftime("%H:%M"))  # format waktu : %H:%M
    pukul_akhir = request.POST.get('waktu_akhir_1', selected_peminjaman.waktu_akhir.time().strftime("%H:%M"))  # format waktu : %H:%M
    input_deskripsi = request.POST.get('deskripsi', selected_peminjaman.deskripsi)
    input_tagihan = request.POST.get('harga', selected_peminjaman.jumlah_tagihan)
    input_nomor_surat = request.POST.get('nomor_surat', selected_peminjaman.no_laporan)
    input_tanggal_lunas = request.POST.get('tanggal_bayar', selected_peminjaman.waktu_bayar)

    input_lunas = ''

    if input_tanggal_lunas != None:
        input_lunas = 'already'
    else:
        input_tanggal_lunas = date.today().strftime("%Y-%m-%d")

    errormsg = []
    messages = []

    if request.method == 'POST':

        try:
            input_lunas = request.POST['lunas']
        except Exception:
            input_lunas = ''

        if input_tanggal_lunas == None:
            try:
                input_tanggal_lunas = request.POST['tanggal_bayar']
            except Exception:
                input_tanggal_lunas = input_tanggal_lunas
        if input_lunas == 'already' and input_tanggal_lunas != '':
            waktu_bayar_t = input_tanggal_lunas
        elif input_lunas == 'already' and input_tanggal_lunas == '':
            waktu_bayar_t = date.today()
        else:
            waktu_bayar_t = None

        # Ambil data pascaedit
        if input_tagihan == '':
            input_tagihan = request.POST['harga']
            input_tagihan = float(input_tagihan)
        if input_tagihan <= 0 and waktu_bayar_t == None:
            waktu_bayar_t = date.today()

        if waktu_bayar_t != None:
            try:
                waktu_bayar_t = datetime.strptime(waktu_bayar_t, "%d %B %Y")
                waktu_bayar_t = waktu_bayar_t.strftime("%Y-%m-%d")
            except Exception as e:
                # Nothing's need to be changed
                pass


        # Ambil data hasil input dari user
        input_peminjam = request.POST['peminjam']
        input_ruangan = request.POST['ruangan']

        # Ambil dan parsing tanggal-jam mulai pinjam dari form
        tanggal_mulai_pinjam = datetime.strptime(tanggal_awal, "%Y-%m-%d")
        mulai_pinjam = datetime.strptime(pukul_awal, "%H:%M")
        tanggal_mulai_pinjam = tanggal_mulai_pinjam.replace(hour=mulai_pinjam.hour, minute=mulai_pinjam.minute)

        # Ambil dan parsing tanggal-jam selesai pinjam dari form
        tanggal_selesai_pinjam = datetime.strptime(tanggal_akhir, "%Y-%m-%d")
        akhir_pinjam = datetime.strptime(pukul_akhir, "%H:%M")
        tanggal_selesai_pinjam = tanggal_selesai_pinjam.replace(hour=akhir_pinjam.hour, minute=akhir_pinjam.minute)

        # Ambil objek Peminjam dan Ruangan
        obj_peminjam = Peminjam.objects.get(id=input_peminjam)
        obj_ruangan = Ruangan.objects.get(id=input_ruangan)

        # Mengecek tanggal mulai kurang dari tanggal selesai
        temp_mulai = tanggal_mulai_pinjam.replace(tzinfo=None)
        temp_selesai = tanggal_selesai_pinjam.replace(tzinfo=None)
        if temp_mulai >= temp_selesai:
            errormsg += ['Waktu mulai harus kurang dari waktu selesai']

        if not input_peminjam:
            errormsg += ['Harap pilih peminjam yang valid']
        if not input_ruangan:
            errormsg += ['Harap pilih ruangan yang valid']

        # Jika belum ditemukan error
        if not errormsg:

            # Ambil objek Peminjam dan Ruangan
            obj_peminjam = Peminjam.objects.get(id=input_peminjam)
            obj_ruangan = Ruangan.objects.get(id=input_ruangan)

            # Membuat object peminjaman yang sesuai, TIDAK AKAN DI-SAVE
            new_peminjaman = Peminjaman(peminjam=obj_peminjam,
                                        ruangan=obj_ruangan,
                                        waktu_awal=tanggal_mulai_pinjam,
                                        waktu_akhir=tanggal_selesai_pinjam,
                                        waktu_bayar=waktu_bayar_t,
                                        deskripsi=input_deskripsi,
                                        jumlah_tagihan=input_tagihan,
                                        no_laporan=input_nomor_surat)

            # Mengecek apakah ada peminjaman yang bentrok,
            collision = new_peminjaman.get_all_conflicted_set()
            collisionset = []
            for peminjaman in collision:
                if not (peminjaman == selected_peminjaman):
                    collisionset += [peminjaman.__str__(), ]

            # Apabila ada bentrok, print semua jadwal yang bentrok, dan kembalikan form
            if (collisionset):
                errormsg += ['Terdapat jadwal yang bentrok :']
                for error in collisionset:
                    errormsg += [error, ]

            # Jika tidak, maka simpan peminjaman, dan kembali ke index
            else:

                # Mencatat perubahan yang dilakukan ke log
                logmsg = ""
                if selected_peminjaman.no_laporan != input_nomor_surat:
                    logmsg += "Ubah no laporan dari " + selected_peminjaman.no_laporan.__str__() + " ke " + input_nomor_surat.__str__() + "\n"
                if selected_peminjaman.peminjam != obj_peminjam:
                    logmsg += "Ubah peminjam dari " + selected_peminjaman.peminjam.__str__() + " ke " + obj_peminjam.__str__() + "\n"
                if selected_peminjaman.ruangan != obj_ruangan:
                    logmsg += "Ubah ruangan dari " + selected_peminjaman.ruangan.__str__() + " ke " + obj_ruangan.__str__() + "\n"
                if selected_peminjaman.waktu_awal != tanggal_mulai_pinjam:
                    logmsg += "Ubah waktu mulai dari " + selected_peminjaman.waktu_awal.__str__() + " ke " + tanggal_mulai_pinjam.__str__() + "\n"
                if selected_peminjaman.waktu_akhir != tanggal_selesai_pinjam:
                    logmsg += "Ubah waktu akhir dari " + selected_peminjaman.waktu_akhir.__str__() + " ke " + tanggal_selesai_pinjam.__str__() + "\n"
                if selected_peminjaman.deskripsi != input_deskripsi:
                    logmsg += "Ubah isi deskripsi\n"
                if str(selected_peminjaman.jumlah_tagihan) != input_tagihan:
                    logmsg += "Ubah jumlah tagihan dari " + selected_peminjaman.jumlah_tagihan.__str__() + " ke " + input_tagihan.__str__() + "\n"

                try:
                    selected_peminjaman.peminjam = obj_peminjam
                    selected_peminjaman.ruangan = obj_ruangan
                    selected_peminjaman.waktu_awal = tanggal_mulai_pinjam
                    selected_peminjaman.waktu_akhir = tanggal_selesai_pinjam
                    selected_peminjaman.waktu_bayar = waktu_bayar_t
                    selected_peminjaman.deskripsi = input_deskripsi
                    selected_peminjaman.jumlah_tagihan = input_tagihan
                    selected_peminjaman.no_laporan = input_nomor_surat
                    if len(request.FILES) != 0:
                        selected_peminjaman.foto.delete()
                        selected_peminjaman.foto = request.FILES['foto']
                    selected_peminjaman.save()
                    new_log = Log(peminjaman=selected_peminjaman,
                                  peminjaman_str=selected_peminjaman.__str__(),
                                  tanggal=date.today(),
                                  deskripsi=logmsg,
                                  aksi="Ubah")
                    new_log.save()
                except Exception as e:
                    messages += ["Unhandled Exception", ]
                else:
                    return redirect(reverse('peminjaman:index'))

    # Mengembalikan form yang sama
    all_peminjam = Peminjam.objects.all()
    all_ruangan = Ruangan.objects.all()
    return render(request, 'peminjaman/edit.html', {
        'all_peminjam': all_peminjam,
        'all_ruangan': all_ruangan,
        'selected_peminjaman' : selected_peminjaman,
        'error': errormsg,
        'message': messages,
        'input_peminjam': input_peminjam,
        'input_ruangan': input_ruangan,
        'input_deskripsi': input_deskripsi,
        'tanggal_awal': tanggal_awal,
        'pukul_awal': pukul_awal,
        'tanggal_akhir': tanggal_akhir,
        'pukul_akhir': pukul_akhir,
        'harga': input_tagihan.__str__(),
        'nomor_surat': input_nomor_surat,
        'input_lunas': input_lunas,
        'waktu_bayar': input_tanggal_lunas,
    })



# Return a form which'll be used to delete peminjaman object to model
@login_required
def formdelete(request, peminjaman_id = 0, errormsg=''):
    try:
        object_peminjaman = Peminjaman.objects.get(id=peminjaman_id)
        new_log = Log(peminjaman=None,
                      peminjaman_str=object_peminjaman.__str__(),
                      tanggal=date.today(),
                      deskripsi="",
                      aksi="Hapus")
        new_log.save()
        if object_peminjaman.foto:
            object_peminjaman.foto.delete()
        object_peminjaman.delete()
    except Peminjaman.DoesNotExist:
        pass

    return redirect(reverse('peminjaman:index'))


# AJAX Service to toggle pembayaran status
@login_required
@csrf_exempt
def togglepembayaran(request, peminjaman_id = 0):
    if request.method == 'POST':
        # Berusaha mendapat model peminjam yang ingin diubah data pembayarannya
        try:
            selected_peminjaman = Peminjaman.objects.get(id=peminjaman_id)
        except Exception as e:
            return JsonResponse({'result': ""})

        if selected_peminjaman.jumlah_tagihan > 0:
            if selected_peminjaman.waktu_bayar:
                selected_peminjaman.waktu_bayar = None
                selected_peminjaman.save()

                new_log = Log(peminjaman=selected_peminjaman,
                              peminjaman_str=selected_peminjaman.__str__(),
                              tanggal=date.today(),
                              deskripsi="Ubah status pembayaran ke 'Belum Lunas'",
                              aksi="Ubah")
                new_log.save()
                return JsonResponse({'result': "Belum Lunas"})

            else:
                selected_peminjaman.waktu_bayar = date.today().strftime("%Y-%m-%d")
                selected_peminjaman.save()

                new_log = Log(peminjaman=selected_peminjaman,
                              peminjaman_str=selected_peminjaman.__str__(),
                              tanggal=date.today(),
                              deskripsi="Ubah status pembayaran ke 'Lunas pada " + selected_peminjaman.waktu_bayar.__str__() + "'",
                              aksi="Ubah")
                new_log.save()
                return JsonResponse({'result': selected_peminjaman.waktu_bayar})
        else:
            return JsonResponse({'result': selected_peminjaman.waktu_bayar})

    return JsonResponse({'result': 'Nope'})


@login_required
@csrf_exempt
def filter(request, year):
    selected_peminjaman = Peminjaman.objects.filter(waktu_awal__year = year).values()
    return JsonResponse({'results': list(selected_peminjaman)})


def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    day = calendar.monthrange(year,month)[1]
    return date(year,month,day)
def diff_months(sourcedate,months):
    year = sourcedate.year
    month = sourcedate.month
    if (sourcedate.month < months) :
        year=year-1
        month=month+12-months
    else :
        month = month - months
    return date(year, month, 1)

@login_required
def fetchrecord(request, d = date.today()):
    selected_peminjaman = Peminjaman.objects.filter(waktu_awal__range = [diff_months(d,6).strftime('%Y-%m-%d'),add_months(d,6).strftime('%Y-%m-%d')]).values()
    return JsonResponse({'results': list(selected_peminjaman)})


def fetchrecord_umum(request, d = date.today()):
    selected_peminjaman = Peminjaman.objects.filter(waktu_awal__range = [diff_months(d,6).strftime('%Y-%m-%d'),add_months(d,6).strftime('%Y-%m-%d')]).filter(ruangan__restricted = False).values()
    return JsonResponse({'results': list(selected_peminjaman)})