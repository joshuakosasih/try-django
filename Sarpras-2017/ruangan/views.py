from django.shortcuts import render, redirect
from .models import Ruangan
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Ruangan index view, mostly for debugging purpose
@login_required
def index(request):
    all_ruangan = Ruangan.objects.all()
    return render(request, 'ruangan/index.html', {
        'all_ruangan': all_ruangan
    })


# Return a form which'll be used to add new Ruangan object to model
@login_required
def formadd(request):

	# Inisiasi variabel berdasarkan post jika ada
    new_nama = request.POST.get("nama",'')
    new_harga = request.POST.get("harga",0)
    new_deskripsi = request.POST.get("deskripsi", '')
    new_tipe = request.POST.get("tipe",'Selasar')
    new_warna = request.POST.get('warna', '#000000')
    if request.POST.get('restrict', False):
        new_restricted = True
    else:
        new_restricted = False

    error = []
    message = []

    # Jika ada data post yang diberikan,
    if request.method == 'POST':

        # Mengecek apakah ada nama valid yang diberikan
        if new_nama == '':
            error += ["Nama ruangan tidak boleh kosong", ]

        # Mengecek apakah tipe ruangan yg diberikan valid
        if (new_tipe != 'Selasar' and new_tipe != 'Lapangan' and new_tipe != 'Ruang'):
            error += ["Pilihan tipe tidak valid", ]

        # Mengecek apakah ada object dengan nama yang sama
        if (Ruangan.objects.filter(nama=new_nama)):
            error += ["Sudah ada data ruangan dengan nama yang sama", ]

        # Berusaha memasukan object ke database jika tidak ada error
        if not error:
            new_ruangan = Ruangan(
                nama = new_nama,
				harga = new_harga,
                deskripsi = new_deskripsi,
				tipe = new_tipe,
                warna = new_warna,
                restricted = new_restricted
            )
            if len(request.FILES) != 0:
                new_ruangan.foto = request.FILES['foto']
            else:
                new_ruangan.foto = None

            # Berusaha menyimpan perubahan dan redirect ke Index jika berhasil
            try:
                new_ruangan.save()
            except Exception as e:
                message += ["Unhandled Exception", ]
            else:
                return redirect(reverse('ruangan:index'))

    # Mengembalikan form yang sama
    return render(request, 'ruangan/add.html', {
        'error': error,
        'message': message,
        'nama': new_nama,
		'harga': new_harga,
        'deskripsi': new_deskripsi,
		'tipe': new_tipe,
        'warna': new_warna,
        'restrict' : new_restricted
    })


# Return a form which'll be used to edit Ruangan object to model
@login_required
def formedit(request, ruangan_id = 0):
	
	# Berusaha mendapat model ruangan yang ingin diubah
    try:
        selected_ruangan = Ruangan.objects.get(id=ruangan_id)
    except Exception as e:
        return redirect(reverse('ruangan:index'))

    # Inisiasi variabel berdasarkan post jika ada
    new_nama = request.POST.get("nama", '')
    new_harga = request.POST.get("harga", 0)
    new_deskripsi = request.POST.get("deskripsi", '')
    new_tipe = request.POST.get("tipe", 'Selasar')
    new_warna = request.POST.get('warna', '#000000')
    if request.POST.get('restrict', False):
        new_restricted = True
    else:
        new_restricted = False

    error = []
    message = []

    # Jika ada data post yang diberikan,
    if request.method == 'POST':

        # Mengecek apakah ada nama valid yang diberikan
        if new_nama == '':
            error += ["Nama ruangan tidak boleh kosong", ]

        # Mengecek apakah tipe ruangan yg diberikan valid
        if (new_tipe != 'Selasar' and new_tipe != 'Lapangan' and new_tipe != 'Ruang'):
            error += ["Pilihan tipe tidak valid", ]

        # Mengecek apakah ada object dengan nama yang sama
        if (Ruangan.objects.filter(nama=new_nama) and (not(selected_ruangan.nama == new_nama))):
            error += ["Sudah ada data peminjam dengan nama yang sama", ]

        # Berusaha mengubah informasi object jika tidak ada error
        if not error:
            selected_ruangan.nama = new_nama
            selected_ruangan.harga = new_harga
            selected_ruangan.deskripsi = new_deskripsi
            selected_ruangan.tipe = new_tipe
            selected_ruangan.warna = new_warna
            selected_ruangan.restricted = new_restricted
            if len(request.FILES) != 0:
                selected_ruangan.foto.delete()
                selected_ruangan.foto = request.FILES['foto']
			
            # Berusaha menyimpan perubahan dan redirect ke Index jika berhasil
            try:
                selected_ruangan.save()
            except Exception as e:
                message += ["Unhandled Exception", ]
                print(e)
            else:
                return redirect(reverse('ruangan:index'))


    # Mengembalikan form yang sama
    return render(request, 'ruangan/edit.html', {
        'selected_ruangan': selected_ruangan,
        'error': error,
        'message': message,
    })


# Return a form which'll be used to delete Ruangan object to model
@login_required
def formdelete(request, ruangan_id = 0):
    
	# Berusaha mendapat model peminjam yang ingin diubah
    try:
        selected_ruangan = Ruangan.objects.get(id=ruangan_id)
    except Exception as e:
        return redirect(reverse('ruangan:index'))

    # Inisiasi variabel berdasarkan post jika ada
    new_nama = request.POST.get("nama",'')
    error = []
    message = []

    # Jika ada data post yang diberikan,
    if(new_nama):

        # Mengecek apakah ada object dengan nama yang sama
        if (not(selected_ruangan.nama == new_nama)):
            error += ["Nama ruangan tidak sama", ]

        # Berusaha mengubah informasi object jika tidak ada error
        if not error:

            # Berusaha menyimpan perubahan dan redirect ke Index jika berhasil
            try:
                if selected_ruangan.foto:
                    selected_ruangan.foto.delete()
                selected_ruangan.delete()
            except Exception as e:
                message += ["Unhandled Exception", ]
            else:
                return redirect(reverse('ruangan:index'))

    # Mengembalikan form yang sama
    return render(request, 'ruangan/delete.html', {
        'selected_ruangan': selected_ruangan,
        'error': error,
        'message': message,
    })


@login_required
def fetchrecord(request):
    all_ruangan = Ruangan.objects.all().values()
    return JsonResponse({'results': list(all_ruangan)})


def fetchrecord_umum(request):
    all_ruangan = Ruangan.objects.filter(restricted=False).values()
    return JsonResponse({'results': list(all_ruangan)})