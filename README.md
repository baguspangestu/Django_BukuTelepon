# ☎️Buku Telepon

Applikasi Web Buku Telepon sebagai tugas kuliah S1 Sistem Informasi ITBA DCC dengan Bahasa Pemrograman Python dan Framework Django.

### Software yang dibutuhkan

- [Python v3.7.0](https://www.python.org/downloads/release/python-370)
- [Poetry v1.2.2](https://python-poetry.org)

#### Framework

- Django v3.2.16

#### Dependencies

| Nama       | Deskripsi                               |
| ---------- | --------------------------------------- |
| whitenoise | Membuka akses static file di server     |
| xlsxwriter | Membuat & export file xlsx              |
| pandas     | Membaca data import file                |
| xlrd       | Engine untuk membaca file xls           |
| openpyxl   | Engine untuk membaca file xlsx dan xlsm |
| pyxlsb     | Engine untuk membaca file xlsb          |

### Inisialisasi

```
poetry install
```

### Run Server

```
poetry run python manage.py runserver
```

### Sudah disetting untuk di deploy ke [render.com](https://render.com)
