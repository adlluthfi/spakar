# Penjelasan Sistem Pakar Jagung (Backward Chaining)

## 1. Gambaran Umum
Aplikasi pada `pakar.py` adalah sistem pakar berbasis web (Flask) untuk mendiagnosis penyakit/hama tanaman jagung.
Alur utama sistem:
1. Pengguna memilih gejala pada form konsultasi.
2. Gejala diperlakukan sebagai fakta awal.
3. Sistem menguji hipotesis penyakit menggunakan backward chaining.
4. Sistem memberi status hipotesis (Terbukti/Belum Terbukti), skor kecocokan, dan rekomendasi penanganan.

## 2. Struktur Kode Utama
Komponen utama file `pakar.py`:
1. Inisialisasi Flask.
2. Basis pengetahuan: gejala, kelompok gejala, penyakit, dan rule IF-THEN.
3. Mesin inferensi backward chaining.
4. Route untuk halaman beranda, konsultasi, diagnosa, dan basis pengetahuan.
5. Menjalankan server lokal.

## 3. Basis Pengetahuan
### 3.1 GEJALA
`GEJALA` adalah kamus kode gejala ke deskripsi.
Contoh: `G1 -> Daun menguning pucat`.
Fungsi:
1. Menjadi fakta observasi yang dipilih pengguna.
2. Menjadi elemen prasyarat pada rule.

### 3.2 KELOMPOK_GEJALA
`KELOMPOK_GEJALA` dipakai untuk pengelompokan tampilan di form.
Fungsi:
1. Meningkatkan keterbacaan input pengguna.
2. Tidak mempengaruhi logika inferensi secara langsung.

### 3.3 PENYAKIT
`PENYAKIT` menyimpan pengetahuan hasil diagnosa:
1. Identitas penyakit/hama (`nama`, `penyebab`, `deskripsi`).
2. Rentang umur tanaman rentan (`umur_tanaman` dalam HST).
3. Rekomendasi kuratif (`pengobatan`).
4. Rekomendasi preventif (`pencegahan`).
5. Atribut tampilan (`warna`, `ikon`).

### 3.4 RULES
`RULES` adalah representasi pengetahuan IF-THEN.
Struktur:
- `conditions`: daftar kode gejala yang harus terpenuhi.
- `result`: kode penyakit yang disimpulkan.

Contoh:
`IF G1 AND G2 AND G16 THEN P1`

## 4. Mesin Inferensi Backward Chaining
### 4.1 Fungsi _confidence_label
Fungsi ini mengubah persentase kecocokan ke label:
1. 100% -> Terdiagnosis
2. >= 66% -> Kemungkinan Besar
3. >= 50% -> Kemungkinan
4. < 50% -> Kemungkinan Kecil

Fungsi ini bersifat pelaporan hasil, bukan inti penalaran backward chaining.

### 4.2 Fungsi _prove_goal (inti backward chaining)
Input:
1. `goal`: target yang ingin dibuktikan (umumnya kode penyakit, misalnya `P1`).
2. `facts`: himpunan gejala yang dipilih pengguna.
3. `visited`: penanda untuk mencegah loop rekursi.

Langkah kerja:
1. Jika `goal` ada dalam fakta, langsung terbukti (`True`).
2. Jika `goal` adalah gejala terminal tetapi tidak ada di fakta, gagal (`False`).
3. Cek `visited` untuk mencegah siklus pembuktian.
4. Cari semua rule dengan `result == goal`.
5. Untuk setiap rule kandidat, buktikan semua prasyarat (`conditions`) secara rekursif.
6. Jika ada satu rule yang semua prasyaratnya terbukti, maka `goal` terbukti (`True`).
7. Jika tidak ada rule sukses, `goal` tidak terbukti (`False`).

Inti paradigma:
- Backward chaining bergerak dari tujuan (penyakit) ke kebutuhan bukti (gejala).
- Bukan dari fakta ke kesimpulan seperti forward chaining.

### 4.3 Fungsi backward_chaining
Fungsi ini menjalankan inferensi untuk seluruh hipotesis penyakit.

Tahapan:
1. Konversi gejala pilihan menjadi `set` (`fakta`) agar pencarian cepat.
2. Iterasi setiap rule pada `RULES`.
3. Hitung:
   - `gejala_cocok`
   - `gejala_kurang`
   - `matched` dan `total`
4. Jika tidak ada gejala yang cocok (`matched == 0`), hipotesis dilewati.
5. Uji pembuktian formal via `_prove_goal(rule['result'], fakta)`.
6. Hitung persentase kecocokan: `persen = round((matched/total)*100)`.
7. Tetapkan label:
   - Jika terbukti penuh -> `Terdiagnosis`.
   - Jika belum terbukti -> pakai `_confidence_label(persen)`.
8. Validasi umur tanaman (`umur_hst`) terhadap rentang penyakit.
   - Jika di luar rentang, sistem membuat `umur_warning`.
9. Gabungkan data inferensi dengan data penyakit ke dalam list hasil.
10. Urutkan hasil dengan prioritas:
   - Hipotesis terbukti (`is_terbukti=True`) di atas.
   - Persentase kecocokan terbesar berikutnya.

Output:
List hasil diagnosis yang siap ditampilkan di template.

## 5. Alur Route Flask
### 5.1 Route '/'
Menampilkan ringkasan total penyakit, gejala, dan rule.

### 5.2 Route '/konsultasi'
Mengirim data gejala dan pengelompokan ke halaman form.

### 5.3 Route '/diagnosa' (POST)
Tahapan proses:
1. Ambil gejala dari form (`request.form.getlist('gejala')`).
2. Jika kosong, kembali ke halaman konsultasi.
3. Ambil umur tanaman opsional (`umur_hst`) dan validasi integer (1 sampai 365).
4. Jalankan `backward_chaining(gejala_dipilih, umur_hst)`.
5. Bentuk data gejala terpilih untuk ditampilkan ulang.
6. Render halaman hasil dengan data inferensi.

### 5.4 Route '/basis-pengetahuan'
Menampilkan gejala, penyakit, dan rules sebagai transparansi basis pengetahuan.

## 6. Sistematis Metodologi (untuk penjelasan akademik)
1. Akuisisi pengetahuan domain pertanian jagung.
2. Representasi pengetahuan dalam bentuk rule IF-THEN.
3. Pengumpulan fakta observasi dari pengguna (gejala).
4. Penalaran backward chaining untuk pembuktian hipotesis.
5. Kuantifikasi dukungan hipotesis (persentase kecocokan).
6. Validasi konteks umur tanaman sebagai penguat interpretasi.
7. Penyajian keputusan dan rekomendasi tindakan.

## 7. Contoh Jejak Inferensi
Contoh input:
- Gejala: `G1, G2, G16`
- Umur: 21 HST

Proses:
1. Sistem uji hipotesis `P1`.
2. Rule `P1` mensyaratkan `G1, G2, G16`.
3. Semua prasyarat ada di fakta, maka `_prove_goal('P1') = True`.
4. Skor 100%, status `Terbukti`, label `Terdiagnosis`.
5. Umur 21 HST masuk rentang P1 (0-30), jadi tanpa peringatan umur.

## 8. Kelebihan dan Batasan
### Kelebihan
1. Sesuai prinsip backward chaining.
2. Transparan: gejala cocok dan gejala kurang ditampilkan.
3. Praktis: hipotesis parsial tetap ditampilkan sebagai referensi lapangan.

### Batasan
1. Rule saat ini belum bertingkat (masih langsung gejala -> penyakit).
2. Bobot gejala belum dibedakan (semua gejala dianggap setara).
3. Belum ada mekanisme conflict resolution kompleks jika rule diperbanyak.

## 9. Ringkasan Singkat
Sistem ini adalah sistem pakar berbasis aturan yang menggunakan backward chaining untuk membuktikan hipotesis penyakit dari fakta gejala, lalu menyajikan hasil diagnosis secara terurut beserta rekomendasi tindakan kuratif dan preventif.
