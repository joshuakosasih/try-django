from django.shortcuts import render
from django.http import JsonResponse
from .models import Log
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Log index view
@login_required
def index(request):
    all_log = Log.objects.all()
    return render(request, 'log/index.html', {
        'all_log': all_log,
    })

#Ajax Bulan dan tahun
@login_required
@csrf_exempt
def filter(request, select_year,select_month):
    if select_year == "1971" and select_month == "0":
        selected_log = Log.objects.values()
    elif select_month == "0":
        selected_log = Log.objects.filter(tanggal__year=select_year).values()
    else:
        selected_log = Log.objects.filter(tanggal__year=select_year, tanggal__month=select_month).values()
    return JsonResponse({'results': list(selected_log)})

@login_required
def fetchrecord(request, start_year = 2017):
    selected_log = Log.objects.filter(tanggal__year = start_year).values()
    return JsonResponse({'results': list(selected_log)})

