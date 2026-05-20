# Panduan Flask Configuration

Flask secara otomatis melayani file statis dari folder `static/`.

## Struktur yang Didukung

- `static/css/` → untuk stylesheet
- `static/js/` → untuk JavaScript
- `static/images/` → untuk gambar
- `static/fonts/` → untuk font custom
- dll.

## Contoh Penggunaan di Template

```html
<!-- Gambar -->
<img src="{{ url_for('static', filename='images/daun/G1.jpg') }}" alt="Gejala G1">

<!-- CSS -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

<!-- JavaScript -->
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
```

## Menjalankan Flask

```bash
# Development mode
python pakar.py

# Atau dengan Flask CLI
flask run
```

Aplikasi akan berjalan di `http://localhost:5000`

---

Jika gambar tidak muncul, pastikan:
1. Flask sedang berjalan
2. Nama file sudah sesuai (case-sensitive di Linux/Mac)
3. File berada di lokasi yang benar
4. Tidak ada cache browser (Ctrl+F5 untuk hard refresh)
