# Panduan Penambahan Gambar Gejala

Folder ini berisi gambar untuk setiap gejala dalam sistem pakar penyakit jagung.

## Struktur Folder

```
static/images/
├── daun/           # Gambar gejala pada daun
├── pertumbuhan/    # Gambar gejala pada pertumbuhan tanaman
├── batang/         # Gambar gejala pada batang
└── tongkol/        # Gambar gejala pada tongkol
```

## Penamaan File Gambar

Setiap gambar harus dinamai sesuai dengan kode gejala dengan ekstensi `.jpg`:

### Gejala pada Daun (`daun/`)
- `G1.jpg` - Daun menguning pucat
- `G3.jpg` - Muncul bercak coklat kemerahan pada daun seperti karat
- `G4.jpg` - Terdapat bercak titik-titik memanjang sempit berwarna coklat tua hingga coklat kekuningan
- `G5.jpg` - Daun menguning dimulai dari ujung daun
- `G6.jpg` - Daun mengering sebelum waktunya
- `G7.jpg` - Muncul bercak memanjang berwarna coklat keabu-abuan pada daun
- `G14.jpg` - Daun tanaman berlubang
- `G15.jpg` - Terdapat kotoran hama yang menyerupai serbuk pada daun
- `G16.jpg` - Terdapat lapisan tepung putih/abu-abu di bawah permukaan daun pada pagi hari
- `G17.jpg` - Bercak pada daun terasa kasar atau timbul jika diraba (seperti amplas halus)
- `G18.jpg` - Terdapat kerusakan pada pucuk/titik tumbuh daun muda (pupus)

### Gejala pada Pertumbuhan Tanaman (`pertumbuhan/`)
- `G2.jpg` - Pertumbuhan tanaman menjadi kerdil

### Gejala pada Batang (`batang/`)
- `G8.jpg` - Batang tanaman menjadi lunak dan berair
- `G9.jpg` - Bagian dalam batang berwarna coklat
- `G10.jpg` - Tanaman mudah roboh
- `G19.jpg` - Terdapat lendir atau bau busuk menyengat pada pangkal batang

### Gejala pada Tongkol (`tongkol/`)
- `G11.jpg` - Tongkol jagung berjamur
- `G12.jpg` - Tongkol mengeluarkan bau tidak sedap
- `G13.jpg` - Tongkol mengalami pembusukan

## Spesifikasi Gambar

- **Format**: JPG/JPEG (atau PNG jika ingin mengubah ekstensi di mapping)
- **Ukuran Rekomendasi**: Minimum 300x300px, maksimal 2000x2000px
- **Ukuran File**: Maksimal 500KB per gambar (untuk performa)
- **Rasio Aspek**: Persegi (1:1) atau landscape (4:3) akan ditampilkan dengan `object-fit: cover`

## Cara Menambahkan Gambar

1. Siapkan gambar gejala dalam format JPG
2. Letakkan di folder yang sesuai (daun, pertumbuhan, batang, atau tongkol)
3. Beri nama sesuai kode gejala (G1.jpg, G2.jpg, dst.)
4. Refresh halaman browser, gambar akan otomatis tampil

## Jika Gambar Tidak Muncul

- Periksa apakah nama file sudah sesuai dengan kode gejala
- Pastikan file ada di folder yang benar
- Cek browser console (F12 → Console) untuk error message
- Jika gambar corrupt, try re-upload dengan format yang berbeda (PNG, WebP, dst.)

## Mengubah Format Gambar

Jika ingin menggunakan format selain JPG, ubah ekstensi di `pakar.py`:

```python
GEJALA_IMAGES = {
    'G1':  'G1.png',   # Untuk PNG
    'G2':  'G2.webp',  # Untuk WebP
    ...
}
```

---

**Last Updated**: 2026-05-18
