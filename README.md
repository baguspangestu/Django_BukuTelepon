# irvanudin-buku_telepon

### Software yang dibutuhkan

- [Python v3.7.0](https://www.python.org/downloads/release/python-370)
- [Poetry (versi terbaru)](https://python-poetry.org)

#### Framework

- DJango v3.2.16

#### Dependencies

- whitenoise (Membuka akses static file di server)
- xlsxwriter (Membuat & export file xlsx)
- pandas (Membaca data import file)
- xlrd (Engine untuk membaca file xls)
- openpyxl (Engine untuk membaca file xlsx dan xlsm)
- pyxlsb (Engine untuk membaca file xlsb)

### Inisialisasi

```
poetry install
```

### Run Server

```
poetry run python manage.py runserver
```

### Sudah disetting untuk di deploy ke [render.com](https://render.com)
