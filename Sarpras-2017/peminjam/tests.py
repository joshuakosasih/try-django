from django.test import TestCase


class PeminjamTest(TestCase):
# # Peminjam index view, mostly for debugging purpose
# def index(request, message='', error=''):
#     all_peminjam = Peminjam.objects.all()
#     return render(request, 'peminjam/index.html', {
#         'error': error,
#         'message': message,
#         'all_peminjam': all_peminjam
#     })
    def test_peminjam_index(self):
        pass
        respond  = self.client.get('/peminjam/')
        self.assertEqual(respond.status_code, 200)

#
#
# # Return a form which'll be used to add new Peminjam object to model
# def formadd(request):
#
#     # Inisiasi variabel berdasarkan post jika ada
#     new_nama = request.POST.get("nama",'')
#     new_deskripsi = request.POST.get("deskripsi",'')
#     error = []
#     message = []
#
#     # Jika ada data post yang diberikan,
#     if request.method == 'POST':
#
#         # Mengecek apakah ada nama valid yang diberikan
#         if new_nama == '':
#             error += ["Nama organisasi tidak boleh kosong", ]
#
#         # Mengecek apakah ada object dengan nama yang sama
#         if (Peminjam.objects.filter(nama=new_nama)):
#             error += ["Sudah ada data peminjam dengan nama yang sama", ]
#
#         # Berusaha memasukan object ke database jika tidak ada error
#         if not error:
#             new_peminjam = Peminjam(
#                 nama=new_nama,
#                 deskripsi=new_deskripsi
#             )
#
#             # Berusaha menyimpan perubahan dan redirect ke Index jika berhasil
#             try:
#                 new_peminjam.save()
#             except Exception as e:
#                 message += ["Unhandled Exception", ]
#             else:
#                 return redirect(reverse('peminjam:index'))
#
#     # Mengembalikan form yang sama
#     return render(request, 'peminjam/add.html', {
#         'error': error,
#         'message': message,
#         'nama': new_nama,
#         'deskripsi': new_deskripsi
#     })
#
    def peminjam_add_test():
        pass


#
# # Return a form which'll be used to edit Peminjam object to model
# def formedit(request, peminjam_id = 0):
#
#     # Berusaha mendapat model peminjam yang ingin diubah
#     try:
#         selected_peminjam = Peminjam.objects.get(id=peminjam_id)
#     except Exception as e:
#         return redirect(reverse('peminjam:index'))
#
#     # Inisiasi variabel berdasarkan post jika ada
#     new_nama = request.POST.get("nama",selected_peminjam.nama)
#     new_deskripsi = request.POST.get("deskripsi",selected_peminjam.deskripsi)
#     error = []
#     message = []
#
#     # Jika ada data post yang diberikan,
#     if request.method == 'POST':
#
#         # Mengecek apakah ada nama valid yang diberikan
#         if new_nama == '':
#             error += ["Nama organisasi tidak boleh kosong", ]
#
#         # Mengecek apakah ada object dengan nama yang sama
#         if (Peminjam.objects.filter(nama=new_nama) and (not(selected_peminjam.nama == new_nama))):
#             error += ["Sudah ada data peminjam dengan nama yang sama", ]
#
#         # Berusaha mengubah informasi object jika tidak ada error
#         if not error:
#             selected_peminjam.nama = new_nama
#             selected_peminjam.deskripsi = new_deskripsi
#
#             # Berusaha menyimpan perubahan dan redirect ke Index jika berhasil
#             try:
#                 selected_peminjam.save()
#             except Exception as e:
#                 message += ["Unhandled Exception", ]
#             else:
#                 return redirect(reverse('peminjam:index'))
#
#
#     # Mengembalikan form yang sama
#     return render(request, 'peminjam/edit.html', {
#         'selected_peminjam': selected_peminjam,
#         'error': error,
#         'message': message,
#     })
#
    def peminjam_edit_test():
        pass
#
# # Return a form which'll be used to delete Peminjam object to model
# def formdelete(request, peminjam_id = 0):
#
#     # Berusaha mendapat model peminjam yang ingin diubah
#     try:
#         selected_peminjam = Peminjam.objects.get(id=peminjam_id)
#     except Exception as e:
#         return redirect(reverse('peminjam:index'))
#
#     # Inisiasi variabel berdasarkan post jika ada
#     new_nama = request.POST.get("nama",'')
#     error = []
#     message = []
#
#     # Jika ada data post yang diberikan,
#     if(new_nama):
#
#         # Mengecek apakah ada object dengan nama yang sama
#         if (not(selected_peminjam.nama == new_nama)):
#             error += ["Nama peminjam tidak sama", ]
#
#         # Berusaha mengubah informasi object jika tidak ada error
#         if not error:
#
#             # Berusaha menyimpan perubahan dan redirect ke Index jika berhasil
#             try:
#                 selected_peminjam.delete()
#             except Exception as e:
#                 message += ["Unhandled Exception", ]
#             else:
#                 return redirect(reverse('peminjam:index'))
#
#     # Mengembalikan form yang sama
#     return render(request, 'peminjam/delete.html', {
#         'selected_peminjam': selected_peminjam,
#         'error': error,
#         'message': message,
#     })
#
    def peminjam_delete_test():
        pass
#
# def fetchrecord(request):
#     all_peminjam = Peminjam.objects.all().values()
#     return JsonResponse({'results': list(all_peminjam)})

    def peminjam_fetchrecord_test():
        pass