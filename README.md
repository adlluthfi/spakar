# Sistem Pakar Diagnosa Penyakit Tanaman Jagung dengan Integrasi NLP

Project ini merupakan aplikasi berbasis web untuk mata kuliah **Sistem Pakar dan Bahasa Alamiah**. Aplikasi dibuat untuk membantu pengguna melakukan diagnosa awal terhadap penyakit atau hama tanaman jagung berdasarkan gejala yang muncul, serta memberikan rekomendasi perawatan yang sesuai.

Pengembangan terbaru pada project ini adalah penambahan fitur **chatbot berbasis Natural Language Processing (NLP)**, sehingga pengguna tidak hanya dapat memilih gejala melalui form konsultasi, tetapi juga dapat menuliskan keluhan menggunakan kalimat bebas.

---

## 1. Deskripsi Project

Aplikasi ini menggabungkan dua pendekatan utama:

### Sistem Pakar

Sistem pakar digunakan untuk mendiagnosis penyakit tanaman jagung berdasarkan gejala yang dipilih pengguna. Sistem menggunakan basis pengetahuan berupa data penyakit, gejala, dan rule IF–THEN.

Metode utama yang digunakan:

- Rule IF–THEN
- Backward Chaining
- Partial Matching
- Validasi umur tanaman / HST
- Pemilihan satu diagnosis terbaik

### Natural Language Processing / Bahasa Alamiah

NLP digunakan pada fitur chatbot agar pengguna dapat bertanya menggunakan kalimat bebas.

Contoh input user:

```text
Daun jagung saya menguning dan tanamannya kerdil, terkena penyakit apa?
```

Sistem akan membaca kalimat tersebut, mengenali gejalanya, lalu mencocokkannya dengan rule sistem pakar.

---

## 2. Latar Belakang

Tanaman jagung merupakan salah satu komoditas penting dalam sektor pertanian. Dalam proses budidayanya, tanaman jagung dapat terserang berbagai penyakit dan hama, seperti bulai, karat daun, hawar daun, busuk batang, busuk tongkol, dan ulat grayak.

Sistem pakar dibuat untuk membantu pengguna, khususnya petani atau masyarakat umum, dalam mengenali penyakit tanaman jagung berdasarkan gejala yang muncul. Agar interaksi dengan sistem lebih mudah, ditambahkan fitur chatbot berbasis NLP sehingga pengguna dapat menyampaikan keluhan dengan bahasa sehari-hari.

---

## 3. Fitur Utama

1. **Halaman Beranda**  
   Menampilkan informasi awal mengenai sistem pakar.

2. **Halaman Konsultasi**  
   Pengguna dapat memilih gejala tanaman jagung melalui form.

3. **Validasi Input Gejala**  
   Jika pengguna menekan tombol diagnosa tanpa memilih gejala, sistem menampilkan pop-up peringatan yang menarik.

4. **Hasil Diagnosis**  
   Sistem menampilkan satu hasil diagnosis terbaik berdasarkan gejala yang dipilih.

5. **Basis Pengetahuan**  
   Menampilkan data penyakit, gejala, dan rule yang digunakan sistem.

6. **Chatbot NLP**  
   Pengguna dapat menulis pertanyaan atau keluhan tanaman jagung dengan kalimat bebas.

7. **Pencarian Knowledge Base**  
   Chatbot dapat mencari jawaban umum dari file `knowledge.txt` menggunakan TF-IDF dan Cosine Similarity.

---

## 4. Penyakit dan Hama yang Didukung

| Kode | Penyakit / Hama | Contoh Gejala |
|---|---|---|
| P1 | Penyakit Bulai | Daun menguning pucat, tanaman kerdil |
| P2 | Penyakit Karat Daun | Bercak coklat kemerahan seperti karat |
| P3 | Penyakit Hawar Daun | Daun menguning dari ujung, daun mengering |
| P4 | Penyakit Busuk Batang | Batang lunak, berair, tanaman mudah roboh |
| P5 | Penyakit Busuk Tongkol | Tongkol berjamur, bau tidak sedap, membusuk |
| P6 | Hama Ulat Grayak | Daun berlubang, terdapat kotoran seperti serbuk |

---

## 5. Metode Sistem Pakar

### 5.1 Rule IF–THEN

Sistem menggunakan representasi pengetahuan berbasis rule IF–THEN.

Contoh:

```text
IF G1 AND G2 AND G16
THEN P1
```

Artinya, jika tanaman memiliki gejala daun menguning pucat, pertumbuhan kerdil, dan terdapat lapisan putih/abu-abu di bawah daun, maka tanaman kemungkinan mengalami Penyakit Bulai.

### 5.2 Backward Chaining

Backward Chaining digunakan untuk menguji hipotesis penyakit berdasarkan gejala yang dipilih pengguna. Sistem akan memeriksa apakah gejala yang menjadi syarat suatu penyakit dapat dibuktikan dari fakta yang diberikan pengguna.

### 5.3 Partial Matching

Partial Matching digunakan agar sistem tetap dapat memberikan hasil diagnosis meskipun gejala yang diberikan pengguna belum lengkap.

Rumus:

```text
Persentase = jumlah gejala cocok / total gejala pada rule x 100%
```

Kategori hasil:

| Persentase | Label |
|---|---|
| 100% | Terdiagnosis |
| ≥ 66% | Kemungkinan Besar |
| ≥ 50% | Kemungkinan |
| < 50% | Kemungkinan Kecil |

### 5.4 Pemilihan Satu Diagnosis Terbaik

Sebelumnya sistem menampilkan beberapa kemungkinan penyakit. Setelah diperbaiki, sistem hanya menampilkan satu penyakit terbaik agar hasil lebih jelas dan tidak membingungkan pengguna.

Prioritas pemilihan diagnosis:

1. Rule yang terbukti lengkap.
2. Persentase kecocokan tertinggi.
3. Kesesuaian umur tanaman / HST.
4. Jumlah gejala cocok terbanyak.

---

## 6. Metode NLP / Bahasa Alamiah

Fitur NLP diterapkan pada chatbot agar sistem dapat memahami input berupa kalimat bebas.

### 6.1 Alur NLP

```text
Input Kalimat User
↓
Text Preprocessing
↓
Deteksi Sapaan / Intent Sederhana
↓
Deteksi Nama Penyakit
↓
Deteksi Gejala dari Kalimat
↓
Pencocokan Gejala dengan Rule Sistem Pakar
↓
Pemilihan Satu Diagnosis Terbaik
↓
Output Jawaban Chatbot
```

### 6.2 Text Preprocessing

Tahapan preprocessing yang digunakan:

| Tahapan | Penjelasan |
|---|---|
| Case Folding | Mengubah teks menjadi huruf kecil |
| Punctuation Removal | Menghapus tanda baca |
| Normalization | Membersihkan teks agar format seragam |
| Tokenization | Memecah kalimat menjadi kata penting |
| Stopword Removal | Menghapus kata umum yang tidak terlalu bermakna |

Contoh:

```text
Input:
Daun jagungku menguning dan pertumbuhannya kerdil, terkena apa?

Hasil preprocessing:
daun jagungku menguning dan pertumbuhannya kerdil terkena apa

Token penting:
menguning, kerdil
```

### 6.3 Keyword Matching

Sistem menggunakan kamus kata kunci untuk mengenali variasi bahasa pengguna.

| Kode Gejala | Gejala Sistem | Contoh Kata User |
|---|---|---|
| G1 | Daun menguning pucat | daun kuning, daun menguning, pucat |
| G2 | Pertumbuhan tanaman kerdil | kerdil, pendek, tumbuh lambat |
| G14 | Daun berlubang | bolong, berlubang |
| G15 | Kotoran hama seperti serbuk | serbuk, kotoran hama |

### 6.4 Token Matching

Selain keyword matching, sistem juga membandingkan kata penting dari input user dengan deskripsi gejala yang tersedia pada basis pengetahuan.

### 6.5 TF-IDF dan Cosine Similarity

TF-IDF digunakan untuk mencari jawaban umum dari file `knowledge.txt`. Cosine Similarity digunakan untuk menghitung kemiripan antara pertanyaan pengguna dan paragraf yang ada di knowledge base.

---

## 7. Contoh Alur Chatbot

### Contoh 1

Input user:

```text
Daun jagung saya menguning dan tanamannya kerdil.
```

Hasil deteksi gejala:

```text
G1 = Daun menguning pucat
G2 = Pertumbuhan tanaman menjadi kerdil
```

Rule yang cocok:

```text
IF G1 AND G2 AND G16 THEN Penyakit Bulai
```

Output chatbot:

```text
Tanaman jagung kemungkinan mengalami Penyakit Bulai.
Tingkat kecocokan: 67%.
```

### Contoh 2

Input user:

```text
Daun jagung berlubang dan ada kotoran seperti serbuk.
```

Hasil deteksi gejala:

```text
G14 = Daun tanaman berlubang
G15 = Terdapat kotoran hama yang menyerupai serbuk pada daun
```

Output chatbot:

```text
Tanaman jagung kemungkinan mengalami Hama Ulat Grayak.
```

---

## 8. Struktur Folder Project

```text
E:.
|   chatbot.py
|   knowledge.txt
|   pakar.py
|   README.md
|   requirements.txt
|
+---static
|   +---images
|       +---batang
|       +---daun
|       +---pertumbuhan
|       +---tongkol
|
+---templates
|       base.html
|       basis_pengetahuan.html
|       chatbot.html
|       hasil.html
|       index.html
|       konsultasi.html
```

---

## 9. Penjelasan File Penting

| File / Folder | Fungsi |
|---|---|
| `pakar.py` | File utama aplikasi Flask, berisi data gejala, penyakit, rule, route, dan fungsi inferensi |
| `chatbot.py` | Modul chatbot NLP untuk memproses pertanyaan pengguna |
| `knowledge.txt` | Sumber pengetahuan umum untuk pertanyaan non-diagnosis |
| `requirements.txt` | Daftar library Python yang dibutuhkan |
| `templates/` | Folder tampilan HTML |
| `static/images/` | Folder gambar gejala tanaman jagung |
| `templates/konsultasi.html` | Halaman input gejala |
| `templates/hasil.html` | Halaman hasil diagnosis |
| `templates/chatbot.html` | Halaman chatbot |

---

## 10. Teknologi yang Digunakan

| Teknologi | Fungsi |
|---|---|
| Python | Bahasa pemrograman utama |
| Flask | Framework web |
| HTML, CSS, JavaScript | Tampilan antarmuka |
| Bootstrap | Styling dan komponen UI |
| scikit-learn | TF-IDF dan Cosine Similarity |
| NumPy | Pengolahan array dan perhitungan |
| Jinja2 | Template engine Flask |

---

## 11. Instalasi dan Cara Menjalankan Project

### 11.1 Buka Folder Project

```bash
cd nama-folder-project
```

### 11.2 Buat Virtual Environment

```bash
python -m venv venv
```

### 11.3 Aktifkan Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### 11.4 Install Dependency

```bash
pip install -r requirements.txt
```

Jika `requirements.txt` belum lengkap, install manual:

```bash
pip install flask numpy scikit-learn
```

### 11.5 Jalankan Aplikasi

```bash
python pakar.py
```

### 11.6 Buka di Browser

```text
http://127.0.0.1:5000
```

---

## 12. Endpoint Aplikasi

| Endpoint | Fungsi |
|---|---|
| `/` | Halaman utama |
| `/konsultasi` | Halaman input gejala |
| `/diagnosa` | Proses diagnosis dari form |
| `/basis-pengetahuan` | Halaman basis pengetahuan |
| `/chatbot` | Halaman chatbot |
| `/api/chat` | API untuk memproses pesan chatbot |

---

## 13. Perbaikan yang Telah Dilakukan

### 13.1 Hasil Diagnosis Menjadi Satu Penyakit

Sebelumnya sistem menampilkan semua kemungkinan penyakit dengan persentase kecocokan. Setelah diperbaiki, sistem hanya menampilkan satu diagnosis terbaik.

### 13.2 Validasi Gejala Kosong

Sebelumnya jika user tidak memilih gejala lalu menekan tombol diagnosis, sistem hanya redirect atau menampilkan alert biasa. Setelah diperbaiki, sistem menampilkan pop-up validasi yang lebih menarik dan informatif.

Pesan validasi:

```text
Tolong inputkan gejala-gejala yang terlihat pada tanaman jagung Anda
agar sistem dapat melakukan proses diagnosa penyakit dengan benar.
```

### 13.3 Chatbot NLP

Chatbot diperbaiki agar dapat membaca gejala dari kalimat pengguna, misalnya:

```text
daun kuning
tanaman kerdil
daun bolong
ada serbuk
batang lunak
mudah roboh
```

Kalimat tersebut kemudian diubah menjadi kode gejala seperti G1, G2, G14, G15, dan seterusnya.

### 13.4 Integrasi Rule ke Chatbot

Chatbot sekarang menerima data:

```python
penyakit_data=PENYAKIT
gejala_data=GEJALA
rules_data=RULES
```

Dengan begitu hasil NLP dapat langsung dicocokkan dengan rule sistem pakar.

---

## 14. Catatan Penting Integrasi Chatbot

Pastikan inisialisasi chatbot di `pakar.py` diletakkan setelah `RULES`.

Contoh:

```python
RULES = [
    {'conditions': ['G1', 'G2', 'G16'], 'result': 'P1'},
    {'conditions': ['G3', 'G4', 'G17'], 'result': 'P2'},
    {'conditions': ['G5', 'G6', 'G7'],  'result': 'P3'},
    {'conditions': ['G8', 'G9', 'G10', 'G19'], 'result': 'P4'},
    {'conditions': ['G11', 'G12', 'G13'],       'result': 'P5'},
    {'conditions': ['G14', 'G15', 'G18'],       'result': 'P6'},
]

kb = JaguKnowledgeBase(
    penyakit_data=PENYAKIT,
    gejala_data=GEJALA,
    rules_data=RULES
)
```

Jika `kb = JaguKnowledgeBase(...)` ditulis sebelum `RULES`, chatbot belum bisa memakai rule diagnosis.

---

## 15. Skenario Pengujian

| No | Input | Hasil yang Diharapkan | Status |
|---|---|---|---|
| 1 | Pilih G1, G2, G16 | Penyakit Bulai | Berhasil |
| 2 | Pilih G3, G4, G17 | Penyakit Karat Daun | Berhasil |
| 3 | Pilih G8, G9, G10, G19 | Penyakit Busuk Batang | Berhasil |
| 4 | Tidak memilih gejala | Muncul pop-up validasi | Berhasil |
| 5 | Chatbot: daun menguning dan kerdil | Penyakit Bulai | Berhasil |
| 6 | Chatbot: daun bolong dan ada serbuk | Hama Ulat Grayak | Berhasil |
| 7 | Chatbot: apa itu karat daun? | Penjelasan Karat Daun | Berhasil |
| 8 | Chatbot: halo | Sapaan chatbot | Berhasil |

---

## 16. Kelebihan Sistem

1. Sistem dapat digunakan melalui form konsultasi dan chatbot.
2. Diagnosis berbasis rule lebih mudah dijelaskan dalam laporan.
3. Chatbot dapat memahami beberapa variasi kalimat pengguna.
4. Sistem hanya menampilkan satu diagnosis terbaik.
5. Fitur NLP membantu mengubah bahasa bebas menjadi kode gejala.
6. Tersedia rekomendasi pengobatan dan pencegahan.

---

## 17. Keterbatasan Sistem

1. NLP masih berbasis keyword matching dan token matching sederhana.
2. Sistem belum menggunakan stemming bahasa Indonesia.
3. Sistem belum menggunakan lemmatization.
4. Sistem belum dapat memahami konteks percakapan panjang.
5. Jika user memakai istilah yang tidak ada pada kamus keyword, gejala bisa tidak terdeteksi.
6. Chatbot belum menanyakan gejala lanjutan secara otomatis.

---

## 18. Rencana Pengembangan

1. Menambahkan stemming bahasa Indonesia.
2. Menambahkan lebih banyak sinonim gejala dari bahasa petani sehari-hari.
3. Membuat chatbot dapat bertanya balik jika gejala belum lengkap.
4. Menambahkan dataset percakapan untuk evaluasi chatbot.
5. Menambahkan fitur export hasil diagnosis.
6. Menambahkan halaman riwayat konsultasi.
7. Menambahkan login admin untuk mengelola data penyakit, gejala, dan rule.

---

## 19. Pembuat

Nama: **Daniel Febrian Sijabat**  
Mata Kuliah: **Sistem Pakar dan Bahasa Alamiah**  
Program Studi: **Informatika**  
Project: **Sistem Pakar Diagnosa Penyakit Tanaman Jagung dengan Integrasi NLP**

---

## 20. Ringkasan

Project ini merupakan sistem pakar berbasis web untuk mendiagnosis penyakit tanaman jagung. Sistem menggunakan rule IF–THEN, backward chaining, partial matching, validasi umur tanaman, dan chatbot berbasis NLP. Dengan integrasi chatbot, pengguna dapat berkonsultasi menggunakan bahasa alami sehingga sistem menjadi lebih mudah digunakan dan lebih komunikatif.
