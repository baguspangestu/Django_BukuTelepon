import io
import xlsxwriter
import pandas as pd
import pathlib
from .models import BukuTelepon
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
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


def import_data(request):
    if request.method == 'POST' and request.FILES['file']:
        ext = ['.csv', '.xls', '.xlsx', '.xlsm', '.xlsb']
        file = request.FILES['file']
        file_ext = pathlib.Path(file.name).suffix

        if file_ext in ext:
            try:
                if file_ext == '.csv':
                    dfs = pd.read_csv(file, dtype=str)
                else:
                    if file_ext == ext[1]:
                        engine = 'xlrd'
                    elif file_ext in ext[2:4]:
                        engine = 'openpyxl'
                    else:
                        engine = 'pyxlsb'

                    read = pd.read_excel(
                        file, engine=engine, dtype=str
                    )
                    dfs = pd.DataFrame(read)

                dfs = dfs.fillna('')
            except:
                messages.error(
                    request, 'Terjadi kesalahan saat membaca data!'
                )
                return False

            s_count = 0
            e_count = 0

            ouaId = []

            for df in dfs.itertuples():
                data = BukuTelepon()

                try:
                    data.nama = df.nama
                except:
                    data.nama = ''

                try:
                    data.no_telepon = df.no_telepon
                except:
                    data.no_telepon = ''

                try:
                    data.alamat = df.alamat
                except:
                    data.alamat = ''

                try:
                    data.perusahaan = df.perusahaan
                except:
                    data.perusahaan = ''

                try:
                    data.save()
                    s_count += 1
                    ouaId.append(data.id)
                except:
                    e_count += 1

            request.session['uoaId'] = ouaId

            if s_count > 0:
                msg = f'{s_count} data berhasil ditambahkan'
                if e_count > 0:
                    msg += f'& {e_count} data error.'
                else:
                    msg += '.'

                messages.success(request, msg)
            else:
                messages.error(
                    request, 'Terjadi kesalahan saat mengimport data!'
                )

        else:
            messages.error(
                request, 'Format file tidak sesuai!')

        return True

    return False


def index(request):
    if import_data(request):
        return redirect('/')

    list = BukuTelepon.objects.all().order_by('-id')

    search = request.GET.get('search')
    if search:
        search = search.strip()
        list = BukuTelepon.objects.filter(
            Q(nama__icontains=search) | Q(no_telepon__icontains=search) |
            Q(alamat__icontains=search) | Q(perusahaan__icontains=search)
        ).distinct().order_by('-id')

    limit = 5
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

    uoaId = request.session.get('uoaId')

    if uoaId:
        request.session['uoaId'] = None

    context = {
        'data': data,
        'count': count,
        'lastCounter': lastCounter,
        'pageRange': pageRange,
        'uoaId': uoaId,
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
                request.session['uoaId'] = [data.id]
                messages.success(request, 'Data berhasil ditambahkan.')
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
                request.session['uoaId'] = [data.id]
                messages.success(request, 'Data berhasil diperbarui.')
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
    buffer = io.BytesIO()
    wb = xlsxwriter.Workbook(buffer)
    ws = wb.add_worksheet()

    row_num = 0

    columns = ['no', 'nama', 'no_telepon', 'alamat', 'perusahaan', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num])

    rows = BukuTelepon.objects.all().values_list(
        'nama', 'no_telepon', 'alamat', 'perusahaan'
    )

    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row_num)
        for col_num in range(len(row)):
            ws.write(row_num, col_num + 1, row[col_num])

    wb.close()

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="buku_telepon.xlsx"'

    response.write(buffer.getvalue())

    return response
