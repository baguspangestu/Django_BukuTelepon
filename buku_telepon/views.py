import xlwt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import BukuTelepon
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError


def validator(data: BukuTelepon):
    if not data.nama:
        msg = 'Nama Lengkap wajib diisi'
    elif not data.no_telepon:
        msg = 'Nomor Telepon wajib diisi'
    elif not data.alamat:
        msg = 'Alamat wajib diisi'
    else:
        msg = ''
    return msg


def index(request):
    list = BukuTelepon.objects.all().order_by('-id')

    search = request.GET.get('search')
    if search:
        search = search.strip()
        list = BukuTelepon.objects.filter(
            Q(nama__icontains=search) | Q(no_telepon__icontains=search) |
            Q(alamat__icontains=search) | Q(perusahaan__icontains=search)
        ).distinct().order_by('-id')

    limit = 10
    paginator = Paginator(list, limit)
    page = request.GET.get('page')

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    count = paginator.count
    lastCounter = limit * (data.number - 1)

    pageRange = []
    for num in paginator.page_range:
        if data.number == 1 and num < data.number + 3 or num > data.number - 2 and num < data.number + 2 or data.number == paginator.num_pages and num > data.number - 3:
            pageRange.append(num)

    isAdded = request.session.get('isAdded')
    updatedId = request.session.get('updatedId')

    if isAdded:
        request.session['isAdded'] = None
    if updatedId:
        request.session['updatedId'] = None

    context = {
        'data': data,
        'count': count,
        'lastCounter': lastCounter,
        'pageRange': pageRange,
        'isAdded': isAdded,
        'updatedId': updatedId,
    }

    return render(request, 'index.html', context)


def add(request):
    data = BukuTelepon()

    if request.method == 'POST':
        data.nama = request.POST['nama']
        data.no_telepon = request.POST['no_telepon']
        data.alamat = request.POST['alamat']
        data.perusahaan = request.POST['perusahaan']

        alert = validator(data)

        if not alert:
            try:
                data.save()
                messages.success(request, 'Data berhasil ditambahkan.')
                request.session['isAdded'] = True
                return redirect('/')
            except IntegrityError as _:
                messages.error(request, 'Terjadi kesalahan!')
        else:
            messages.error(request, alert)

    context = {
        'data': data,
    }

    return render(request, 'add.html', context)


def update(request, id):
    data = BukuTelepon.objects.get(id=id)

    if request.method == 'POST':
        data.nama = request.POST['nama']
        data.no_telepon = request.POST['no_telepon']
        data.alamat = request.POST['alamat']
        data.perusahaan = request.POST['perusahaan']

        alert = validator(data)

        if not alert:
            try:
                data.save()
                messages.success(request, 'Data berhasil diperbarui.')
                request.session['updatedId'] = id
                return redirect('/')
            except IntegrityError as _:
                messages.error(request, 'Terjadi kesalahan!')
        else:
            messages.error(request, alert)

    context = {
        'data': data,
    }

    return render(request, 'update.html', context)


def delete(request, id):
    BukuTelepon.objects.get(id=id).delete()

    messages.success(request, 'Data berhasil dihapus.')

    return redirect('/')


def export(_):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="buku_telepon.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Buku Telepon')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['no', 'nama', 'no_telepon', 'alamat', 'perusahaan', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = BukuTelepon.objects.all().values_list(
        'nama', 'no_telepon', 'alamat', 'perusahaan')
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row_num, font_style)
        for col_num in range(len(row)):
            ws.write(row_num, col_num + 1, row[col_num], font_style)

    wb.save(response)

    return response
