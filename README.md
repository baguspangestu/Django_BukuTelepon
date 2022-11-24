# ☎️ Buku Telepon

Aplikasi Web Buku Telepon sebagai tugas kuliah S1 Sistem Informasi ITBA DCC Pringsewu 2022 dengan Bahasa Pemrograman Python dan Framework Django.

![Screenshot](application/static/images/screenshot.png)

> [Live Demo](https://kelompok1-bukutelepon.onrender.com)

### Software

[![Python](https://img.shields.io/badge/Python-^3.7-blue)](https://www.python.org/downloads)
[![Poetry](https://img.shields.io/badge/Poetry-^1.2-orange)](https://python-poetry.org/docs/#installation)

#### Framework

- Django v3.2.16

#### Database

- SQLite 3

#### Dependencies

| Nama       | Deskripsi                               |
| ---------- | --------------------------------------- |
| whitenoise | Membuka akses static file di server     |
| xlsxwriter | Membuat & export file xlsx              |
| pandas     | Membaca data import file                |
| xlrd       | Engine untuk membaca file xls           |
| openpyxl   | Engine untuk membaca file xlsx dan xlsm |
| pyxlsb     | Engine untuk membaca file xlsb          |

### Download

```
git clone https://github.com/baguspangestu/buku_telepon.git
```

### Inisialisasi

```
poetry install
```

### Run Server

```
poetry run python manage.py runserver
```

### Sudah disetting untuk di deploy ke [render.com](https://render.com)

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE.md)

@ 2022 Irvanudin X Bagus Pangestu <<baguspangestu@yandex.com>>
