import re
import string
from html import unescape
from typing import Dict, List, Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class JaguKnowledgeBase:
    """
    Class utama untuk membuat knowledge base chatbot tanaman jagung.

    Fungsi utama class ini:
    1. Membaca file knowledge.txt sebagai sumber pengetahuan umum.
    2. Membaca data penyakit, gejala, dan rule dari file pakar.py.
    3. Mendeteksi pertanyaan user, apakah berupa:
       - Sapaan
       - Pertanyaan nama penyakit
       - Cerita gejala tanaman
       - Pertanyaan umum tentang jagung
    4. Jika user menceritakan gejala, sistem akan mencocokkan gejala tersebut
       dengan RULES sistem pakar dan hanya memberi 1 diagnosis terbaik.
    """

    # ============================================================
    # PESAN SAPAAN DASAR
    # ============================================================
    # Dictionary ini menyimpan jawaban otomatis untuk sapaan, ucapan terima kasih,
    # dan perpisahan. Tujuannya agar chatbot terasa lebih interaktif.
    GREETINGS = {
        "salam": "Halo! 👋 Saya siap membantu menjawab pertanyaan tentang tanaman jagung.",
        "thank": "Sama-sama! 😊 Semoga tanaman jagungnya sehat dan hasil panennya bagus.",
        "bye": "Sampai jumpa! 👋 Semoga tanaman jagungnya tumbuh subur.",
    }

    # ============================================================
    # KAMUS KATA KUNCI GEJALA
    # ============================================================
    # Bagian ini digunakan untuk membaca kalimat bebas dari user.
    # Contoh:
    # User menulis: "daun jagungku kuning dan tanamannya pendek"
    # Sistem akan mengenali:
    # - "daun kuning" / "kuning" sebagai G1
    # - "pendek" sebagai G2
    #
    # Jadi user tidak harus menulis persis sama dengan teks gejala di sistem.
    GEJALA_KEYWORDS = {
        "G1": [
            "daun menguning", "daun kuning", "menguning pucat", "pucat",
            "daun pucat", "warna daun kuning", "daunnya menguning",
            "daunnya kuning",
        ],
        "G2": [
            "kerdil", "tanaman kerdil", "pertumbuhan kerdil",
            "pertumbuhan lambat", "tidak tumbuh", "tumbuh lambat",
            "pendek", "tanaman pendek",
        ],
        "G3": [
            "bercak coklat kemerahan", "seperti karat", "karat",
            "bercak karat", "daun berkarat",
        ],
        "G4": [
            "titik memanjang", "bercak memanjang sempit", "coklat tua",
            "coklat kekuningan", "bercak memanjang", "bercak coklat tua",
        ],
        "G5": [
            "ujung daun menguning", "menguning dari ujung",
            "kuning dari ujung", "daun kuning dari ujung",
        ],
        "G6": [
            "daun mengering", "kering sebelum waktunya", "daun kering",
            "mengering sebelum waktunya",
        ],
        "G7": [
            "bercak coklat keabu", "coklat keabu-abuan",
            "bercak memanjang", "bercak abu",
        ],
        "G8": [
            "batang lunak", "batang berair", "batangnya lunak",
            "batangnya berair",
        ],
        "G9": [
            "dalam batang coklat", "bagian dalam batang coklat",
            "isi batang coklat",
        ],
        "G10": [
            "mudah roboh", "tanaman roboh", "batang roboh",
            "rebah", "tanaman rebah",
        ],
        "G11": [
            "tongkol berjamur", "jagung berjamur", "jamur pada tongkol",
            "tongkol jamuran",
        ],
        "G12": [
            "bau tidak sedap", "bau busuk", "tongkol bau",
            "berbau busuk",
        ],
        "G13": [
            "tongkol membusuk", "pembusukan tongkol", "tongkol busuk",
            "jagung busuk",
        ],
        "G14": [
            "daun berlubang", "daunnya berlubang", "lubang pada daun",
            "daun bolong", "bolong", "berlubang",
        ],
        "G15": [
            "kotoran hama", "serbuk pada daun", "kotoran seperti serbuk",
            "ada serbuk",
        ],
        "G16": [
            "tepung putih", "lapisan putih", "abu abu di bawah daun",
            "bawah daun putih", "bulu putih",
        ],
        "G17": [
            "bercak terasa kasar", "bercak timbul", "seperti amplas",
            "kasar saat diraba",
        ],
        "G18": [
            "pucuk rusak", "titik tumbuh rusak", "pupus rusak",
            "daun muda rusak", "pucuk daun rusak",
        ],
        "G19": [
            "lendir", "pangkal batang bau", "bau busuk menyengat",
            "lendir pada batang", "pangkal batang busuk",
        ],
    }

    def __init__(
        self,
        knowledge_file: str = "knowledge.txt",
        penyakit_data: Optional[Dict] = None,
        gejala_data: Optional[Dict] = None,
        rules_data: Optional[List[Dict]] = None,
    ):
        """
        Constructor class JaguKnowledgeBase.
        Fungsi:
        Method ini otomatis dijalankan ketika object JaguKnowledgeBase dibuat
        di file pakar.py.
        Parameter:
        - knowledge_file:
          Nama file pengetahuan umum chatbot. Default-nya adalah knowledge.txt.
        - penyakit_data:
          Data penyakit dari dictionary PENYAKIT di file pakar.py.
        - gejala_data:
          Data gejala dari dictionary GEJALA di file pakar.py.
        - rules_data:
          Data rule dari list RULES di file pakar.py.
        Alur kerja:
        1. Simpan semua data ke dalam property class.
        2. Siapkan TF-IDF Vectorizer untuk pencarian jawaban umum.
        3. Baca isi knowledge.txt.
        4. Buat index TF-IDF dari isi knowledge.txt.
        """

        # Menyimpan lokasi file knowledge.txt.
        self.knowledge_file = knowledge_file

        # Menyimpan data penyakit dari pakar.py.
        # Jika data tidak dikirim, gunakan dictionary kosong agar tidak error.
        self.penyakit_data = penyakit_data or {}

        # Menyimpan data gejala dari pakar.py.
        self.gejala_data = gejala_data or {}

        # Menyimpan data rule dari pakar.py.
        # Rule digunakan untuk mencocokkan gejala dengan penyakit.
        self.rules_data = rules_data or []

        # Variabel untuk menyimpan isi mentah knowledge.txt.
        self.content = ""

        # Variabel untuk menyimpan knowledge.txt yang sudah dipotong menjadi paragraf.
        self.paragraphs: List[str] = []

        # Membuat object TF-IDF Vectorizer.
        # TF-IDF digunakan untuk mencari paragraf di knowledge.txt yang paling mirip
        # dengan pertanyaan user.
        self.vectorizer = TfidfVectorizer(
            lowercase=True,                 # Semua teks dibuat huruf kecil.
            stop_words=self._get_stopwords(),  # Kata umum diabaikan.
            token_pattern=r"\b[a-zA-Z]{2,}\b", # Ambil token minimal 2 huruf.
            max_features=2000,               # Maksimal 800 kata penting.
        )

        # Variabel untuk menyimpan hasil representasi TF-IDF dari paragraf knowledge.txt.
        self.tfidf_matrix = None

        # Membaca file knowledge.txt.
        self._load_knowledge()

        # Membuat index TF-IDF dari knowledge.txt.
        self._build_tfidf_index()

    def _get_stopwords(self) -> List[str]:
        """
        Mengembalikan daftar stopwords bahasa Indonesia sederhana.
        Stopwords adalah kata-kata umum yang biasanya tidak terlalu penting
        untuk proses pencarian makna, misalnya:
        - dan
        - atau
        - yang
        - di
        - ke
        Dalam project ini, beberapa kata seperti "jagung", "tanaman",
        "daun", "batang", dan "tongkol" juga dimasukkan sebagai stopwords
        agar sistem lebih fokus pada ciri gejala, bukan objek umumnya.
        Return:
        - List berisi kata-kata yang akan diabaikan saat proses tokenisasi.
        """
        return [
            "dan", "atau", "yang", "di", "ke", "dari", "pada", "untuk", "adalah",
            "ini", "itu", "dengan", "oleh", "dalam", "jika", "maka", "dapat", "akan",
            "telah", "sudah", "juga", "saja", "saat", "karena", "sebab", "namun",
            "tetapi", "tapi", "lalu", "kemudian", "sering", "tidak", "belum", "ada",
            "terdapat", "tanaman", "jagung", "jagungku", "kira", "solusi", "solusinya",
            "terkena", "kena", "apa", "bagaimana", "cara", "mohon", "tolong",
            "daun", "batang", "tongkol", "seperti", "obat", "obatnya", "solusnya",
        ]

    def _load_knowledge(self):
        """
        Membaca file knowledge.txt dan memecahnya menjadi beberapa paragraf.

        Fungsi:
        - Membuka file knowledge.txt.
        - Membaca seluruh isinya.
        - Memisahkan isi file berdasarkan baris kosong.
        - Hanya menyimpan paragraf yang panjangnya lebih dari 30 karakter.

        Kenapa dipotong menjadi paragraf?
        Karena saat user bertanya, chatbot akan mencari paragraf paling relevan
        dari knowledge.txt, bukan membaca seluruh file sekaligus.
        """

        try:
            # Membuka dan membaca file knowledge.txt.
            with open(self.knowledge_file, "r", encoding="utf-8") as file:
                self.content = file.read()

            # Memecah isi file berdasarkan dua enter/baris kosong.
            self.paragraphs = [
                paragraph.strip()
                for paragraph in self.content.split("\n\n")
                if paragraph.strip() and len(paragraph.strip()) > 30
            ]

        except FileNotFoundError:
            # Jika knowledge.txt tidak ditemukan, chatbot tetap berjalan,
            # tetapi tidak bisa menjawab pertanyaan umum dari knowledge.txt.
            self.paragraphs = []

        except Exception as error:
            # Jika ada error lain, tampilkan error di terminal.
            print(f"[Chatbot] Gagal membaca knowledge.txt: {error}")
            self.paragraphs = []

    def _build_tfidf_index(self):
        """
        Membuat index TF-IDF dari paragraf knowledge.txt.
        Fungsi:
        - Mengubah kumpulan paragraf menjadi bentuk numerik.
        - Bentuk numerik ini dipakai untuk menghitung kemiripan
          antara pertanyaan user dan isi knowledge.txt.

        Penjelasan sederhana:
        TF-IDF akan memberi bobot tinggi pada kata yang penting,
        dan bobot rendah pada kata yang terlalu umum.
        """

        # Jika tidak ada paragraf, proses TF-IDF tidak dijalankan.
        if not self.paragraphs:
            return

        try:
            # Membentuk matrix TF-IDF dari semua paragraf.
            self.tfidf_matrix = self.vectorizer.fit_transform(self.paragraphs)

        except Exception as error:
            # Jika gagal, chatbot tetap bisa menggunakan fallback search.
            print(f"[Chatbot] Gagal membuat indeks TF-IDF: {error}")
            self.tfidf_matrix = None

    def _normalize_text(self, text: str) -> str:
        """
        Membersihkan dan menormalkan teks.

        Fungsi:
        - Mengubah teks menjadi huruf kecil.
        - Menghapus simbol HTML.
        - Mengubah tanda hubung menjadi spasi.
        - Menghapus tanda baca.
        - Menghapus spasi berlebih.

        Contoh:
        Input:
        "Daun Jagung-ku Menguning!!!"

        Output:
        "daun jagungku menguning"

        Parameter:
        - text: teks yang akan dibersihkan.

        Return:
        - Teks yang sudah bersih dan seragam.
        """

        # Mengubah HTML entity dan huruf menjadi kecil.
        text = unescape(text.lower())

        # Mengganti tanda hubung dengan spasi.
        text = text.replace("-", " ")

        # Menghapus tanda baca.
        text = text.translate(str.maketrans("", "", string.punctuation))

        # Menghapus spasi berlebih.
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _tokenize(self, text: str) -> List[str]:
        """
        Mengubah teks menjadi kumpulan token/kata penting.
        Fungsi:
        - Membersihkan teks dengan _normalize_text().
        - Memecah teks menjadi kata-kata.
        - Menghapus stopwords.
        - Menghapus kata yang terlalu pendek.
        Contoh:
        Input:
        "daun jagung saya menguning dan tanaman menjadi kerdil"
        Output:
        ["menguning", "kerdil"]
        Parameter:
        - text: teks yang akan diubah menjadi token.
        Return:
        - List berisi kata-kata penting.
        """

        # Bersihkan teks terlebih dahulu.
        text = self._normalize_text(text)

        # Ambil kata yang bukan stopwords dan panjangnya lebih dari 2 huruf.
        return [
            token for token in text.split()
            if token not in self._get_stopwords() and len(token) > 2
        ]

    def _clean_html(self, text: str) -> str:
        """
        Menghapus tag HTML dari teks.
        Fungsi ini dipakai karena beberapa data pengobatan/pencegahan di pakar.py
        memakai tag HTML seperti:
        - <strong>
        - <em>
        Saat ditampilkan di chatbot, tag tersebut dibersihkan agar teks jawaban
        terlihat rapi.
        Parameter:
        - text: teks yang mungkin mengandung tag HTML.
        Return:
        - Teks tanpa tag HTML.
        """

        # Menghapus tag HTML.
        text = re.sub(r"<[^>]+>", "", text)

        # Mengubah HTML entity menjadi karakter biasa.
        text = unescape(text)

        # Merapikan spasi.
        return re.sub(r"\s+", " ", text).strip()

    def get_response(self, query: str) -> Dict:
        """
        Fungsi utama untuk memproses pertanyaan user.
        Fungsi ini dipanggil dari route /api/chat di file pakar.py.
        Alur kerja:
        1. Cek apakah pertanyaan kosong.
        2. Bersihkan pertanyaan user.
        3. Cek apakah pertanyaan berupa sapaan.
        4. Cek apakah pertanyaan menyebut nama penyakit atau gejala.
        5. Jika bukan, cari jawaban umum dari knowledge.txt memakai TF-IDF.
        6. Jika tetap tidak ditemukan, tampilkan pesan bantuan.
        Parameter:
        - query: pertanyaan user.

        Return:
        - Dictionary berisi:
          success: True/False
          message: jawaban chatbot
          type: jenis respon
        """

        # Menghapus spasi di awal dan akhir pertanyaan.
        query = query.strip()

        # Jika pertanyaan kosong, langsung kembalikan pesan error.
        if not query:
            return {
                "success": False,
                "message": "Silakan masukkan pertanyaan tentang tanaman jagung terlebih dahulu.",
                "type": "error",
            }

        # Membersihkan teks pertanyaan agar mudah diproses.
        query_lower = self._normalize_text(query)

        # Mengecek apakah user hanya menyapa, mengucapkan terima kasih, atau pamit.
        greeting_response = self._detect_greeting_farewell(query_lower)
        if greeting_response:
            return greeting_response

        # Mengecek apakah user bertanya tentang penyakit atau menyebut gejala.
        disease_response = self._answer_disease_or_symptom_question(query_lower)
        if disease_response:
            return disease_response

        # Jika bukan pertanyaan penyakit/gejala, cari jawaban umum di knowledge.txt.
        results = self._search_with_tfidf(query)
        if results:
            best_result = results[0]
            return {
                "success": True,
                "message": self._format_general_response(best_result["snippet"]),
                "type": "success",
            }

        # Jika tidak ada jawaban yang cocok, tampilkan contoh pertanyaan.
        return {
            "success": False,
            "message": (
                "Maaf, saya belum menemukan informasi yang sesuai.\n\n"
                "Coba tuliskan pertanyaan dengan menyebutkan gejalanya, misalnya:\n"
                "• Daun jagung menguning dan tanaman kerdil\n"
                "• Daun berlubang dan ada kotoran seperti serbuk\n"
                "• Batang lunak, berair, dan tanaman mudah roboh"
            ),
            "type": "not_found",
        }

    def _detect_greeting_farewell(self, query_lower: str) -> Optional[Dict]:
        """
        Mendeteksi apakah input user adalah sapaan, terima kasih, atau perpisahan.
        Kenapa dibatasi kalimat pendek?
        Agar kata seperti "pagi" dalam kalimat panjang tidak langsung dianggap
        sebagai sapaan. Contoh:
        "pada pagi hari ada lapisan putih di bawah daun"
        Kalimat itu adalah gejala G16, bukan sapaan.
        Parameter:
        - query_lower: pertanyaan user yang sudah dibersihkan.
        Return:
        - Dictionary respon jika terdeteksi sapaan.
        - None jika bukan sapaan.
        """

        # Memecah kalimat menjadi kata.
        words = query_lower.split()

        # Deteksi sapaan hanya jika kalimat pendek.
        if len(words) <= 4 and any(word in query_lower for word in ["halo", "hai", "pagi", "siang", "sore", "malam"]):
            return {
                "success": True,
                "message": self.GREETINGS["salam"],
                "type": "greeting",
            }

        # Deteksi ucapan terima kasih.
        if any(word in query_lower for word in ["terima kasih", "makasih", "thanks", "thank you"]):
            return {
                "success": True,
                "message": self.GREETINGS["thank"],
                "type": "thank",
            }

        # Deteksi perpisahan hanya jika kalimat pendek.
        if len(words) <= 4 and any(word in query_lower for word in ["bye", "dadah", "sampai jumpa"]):
            return {
                "success": True,
                "message": self.GREETINGS["bye"],
                "type": "farewell",
            }

        # Jika tidak cocok, kembalikan None.
        return None

    def _answer_disease_or_symptom_question(self, query_lower: str) -> Optional[Dict]:
        """
        Menentukan apakah pertanyaan user berkaitan dengan penyakit atau gejala.
        Alur kerja:
        1. Cek apakah user menyebut nama penyakit langsung.
           Contoh:
           "Apa itu penyakit bulai?"
        2. Jika tidak menyebut nama penyakit, cek apakah user menceritakan gejala.
           Contoh:
           "Daun menguning dan tanaman kerdil."
        3. Jika ditemukan gejala, sistem melakukan diagnosis berdasarkan rule.
        4. Jika tidak ada penyakit/gejala yang cocok, return None.
        Parameter:
        - query_lower: pertanyaan user yang sudah dibersihkan.
        Return:
        - Dictionary respon jika pertanyaan penyakit/gejala dikenali.
        - None jika tidak dikenali.
        """

        # 1. Cek nama penyakit secara langsung.
        direct_disease = self._find_disease_by_name(query_lower)
        if direct_disease:
            disease_code, disease_info = direct_disease
            return {
                "success": True,
                "message": self._format_disease_detail(disease_info),
                "type": "disease",
                "disease_code": disease_code,
            }

        # 2. Cek gejala dari kalimat user.
        detected_symptoms = self._detect_symptoms_from_query(query_lower)

        # Jika ada gejala yang terdeteksi, lakukan diagnosis.
        if detected_symptoms:
            diagnosis = self._diagnose_from_symptoms(detected_symptoms)

            # Jika diagnosis berhasil ditemukan, format jawabannya.
            if diagnosis:
                return {
                    "success": True,
                    "message": self._format_symptom_diagnosis(diagnosis, detected_symptoms),
                    "type": "disease",
                    "disease_code": diagnosis["kode"],
                }

        # Jika tidak ada yang cocok, return None agar diproses oleh TF-IDF.
        return None

    def _find_disease_by_name(self, query_lower: str) -> Optional[tuple]:
        """
        Mengecek apakah user menyebut nama penyakit secara langsung.
        Contoh input user:
        - "Apa itu penyakit bulai?"
        - "Bagaimana cara mengatasi karat daun?"
        - "Busuk batang itu penyebabnya apa?"
        Fungsi ini akan mencocokkan kata tersebut dengan:
        1. Nama penyakit dari dictionary PENYAKIT.
        2. Alias/sinonim penyakit yang ditulis manual.
        Parameter:
        - query_lower: pertanyaan user yang sudah dibersihkan.
        Return:
        - Tuple berisi (kode_penyakit, data_penyakit) jika ditemukan.
        - None jika tidak ditemukan.
        """

        # Alias digunakan agar user tidak harus menulis nama penyakit secara persis.
        aliases = {
            "P1": ["bulai", "penyakit bulai"],
            "P2": ["karat daun", "penyakit karat", "daun karat"],
            "P3": ["hawar daun", "penyakit hawar"],
            "P4": ["busuk batang", "penyakit busuk batang"],
            "P5": ["busuk tongkol", "penyakit busuk tongkol"],
            "P6": ["ulat grayak", "hama ulat", "grayak"],
        }

        # Loop semua penyakit dari pakar.py.
        for disease_code, disease_info in self.penyakit_data.items():
            # Ambil nama penyakit, lalu normalisasi.
            disease_name = self._normalize_text(disease_info.get("nama", ""))

            # Jika nama penyakit ditemukan dalam pertanyaan user.
            if disease_name and disease_name in query_lower:
                return disease_code, disease_info

            # Jika alias penyakit ditemukan dalam pertanyaan user.
            for alias in aliases.get(disease_code, []):
                if alias in query_lower:
                    return disease_code, disease_info

        # Tidak ada penyakit yang disebut langsung.
        return None

    def _detect_symptoms_from_query(self, query_lower: str) -> List[str]:
        """
        Mendeteksi kode gejala dari kalimat bebas user.
        Ada dua teknik yang dipakai:
        1. Pencocokan frasa dari GEJALA_KEYWORDS.
           Contoh:
           "daun kuning" cocok dengan G1.
        2. Pencocokan token dengan deskripsi GEJALA dari pakar.py.
           Contoh:
           Jika user menulis beberapa kata yang mirip dengan deskripsi gejala,
           sistem juga bisa menangkapnya.
        Parameter:
        - query_lower: pertanyaan user yang sudah dibersihkan.
        Return:
        - List kode gejala yang terdeteksi.
          Contoh: ["G1", "G2"]
        """

        # Set digunakan agar kode gejala tidak dobel.
        detected = set()

        # =====================================================
        # 1. DETEKSI BERDASARKAN KAMUS SINONIM / FRASA
        # =====================================================
        for symptom_code, keywords in self.GEJALA_KEYWORDS.items():
            for keyword in keywords:
                # Jika salah satu keyword ditemukan dalam pertanyaan user,
                # maka kode gejala dimasukkan ke detected.
                if self._normalize_text(keyword) in query_lower:
                    detected.add(symptom_code)
                    break

        # =====================================================
        # 2. DETEKSI BERDASARKAN KEMIRIPAN KATA DENGAN DATA GEJALA
        # =====================================================

        # Token pertanyaan user.
        query_tokens = set(self._tokenize(query_lower))

        # Loop semua gejala dari pakar.py.
        for symptom_code, description in self.gejala_data.items():
            # Token deskripsi gejala.
            desc_tokens = set(self._tokenize(description))

            # Jika deskripsi kosong, lewati.
            if not desc_tokens:
                continue

            # Cari kata yang sama antara pertanyaan user dan deskripsi gejala.
            overlap = query_tokens.intersection(desc_tokens)

            # Minimal 3 kata sama agar tidak terlalu mudah salah deteksi.
            if len(overlap) >= 3:
                detected.add(symptom_code)

        # Urutkan kode gejala berdasarkan angka.
        # Contoh: G1, G2, G10 tetap diurutkan benar berdasarkan angka.
        return sorted(detected, key=lambda code: int(code[1:]))

    def _diagnose_from_symptoms(self, symptom_codes: List[str]) -> Optional[Dict]:
        """
        Melakukan diagnosis berdasarkan gejala yang berhasil dideteksi.
        Fungsi ini memakai RULES dari pakar.py.
        Contoh rule:
        {'conditions': ['G1', 'G2', 'G16'], 'result': 'P1'}
        Artinya:
        Jika G1, G2, dan G16 terpenuhi, maka penyakitnya P1.
        Alur kerja:
        1. Ambil semua gejala yang terdeteksi sebagai fakta.
        2. Bandingkan fakta dengan setiap rule.
        3. Hitung jumlah gejala yang cocok.
        4. Hitung persentase kecocokan.
        5. Simpan semua kandidat penyakit.
        6. Urutkan kandidat berdasarkan kecocokan tertinggi.
        7. Return hanya 1 penyakit terbaik.
        Parameter:
        - symptom_codes: list kode gejala yang ditemukan dari kalimat user.
        Return:
        - Dictionary diagnosis terbaik.
        - None jika tidak ada rule yang cocok.
        """

        # Jika rules_data kosong, diagnosis tidak bisa dilakukan.
        if not self.rules_data:
            return None

        # Gejala yang ditemukan dianggap sebagai fakta.
        facts = set(symptom_codes)

        # List untuk menyimpan kandidat penyakit.
        candidates = []

        # Loop setiap rule.
        for rule in self.rules_data:
            # Ambil daftar kondisi/gejala dari rule.
            conditions = rule.get("conditions", [])

            # Ambil kode penyakit hasil rule.
            result_code = rule.get("result")

            # Jika kode penyakit kosong atau tidak ada di PENYAKIT, lewati.
            if not result_code or result_code not in self.penyakit_data:
                continue

            # Gejala rule yang cocok dengan fakta user.
            matched = [code for code in conditions if code in facts]

            # Gejala rule yang belum disebut user.
            missing = [code for code in conditions if code not in facts]

            # Jika tidak ada satu pun gejala cocok, rule ini tidak dipakai.
            if not matched:
                continue

            # Total gejala dalam rule.
            total = len(conditions)

            # Menghitung persentase kecocokan.
            percent = round((len(matched) / total) * 100)

            # Simpan kandidat penyakit.
            candidates.append({
                "kode": result_code,
                "penyakit": self.penyakit_data[result_code],
                "rule_conditions": conditions,
                "gejala_cocok": matched,
                "gejala_kurang": missing,
                "matched": len(matched),
                "total": total,
                "persen": percent,
                "is_terbukti": len(matched) == total,
            })

        # Jika tidak ada kandidat sama sekali, return None.
        if not candidates:
            return None

        # Urutkan kandidat penyakit:
        # 1. Rule yang terbukti lengkap didahulukan.
        # 2. Persentase kecocokan tertinggi.
        # 3. Jumlah gejala cocok terbanyak.
        candidates.sort(
            key=lambda item: (item["is_terbukti"], item["persen"], item["matched"]),
            reverse=True,
        )

        # Return hanya diagnosis terbaik.
        return candidates[0]

    def _confidence_label(self, percent: int, is_proven: bool) -> str:
        """
        Mengubah nilai persentase kecocokan menjadi label teks.
        Contoh:
        - 100% dan rule lengkap     -> terdiagnosis kuat
        - >= 66%                   -> kemungkinan besar
        - >= 50%                   -> kemungkinan
        - di bawah 50%             -> kemungkinan kecil
        Parameter:
        - percent: persentase kecocokan gejala.
        - is_proven: True jika semua gejala dalam rule terpenuhi.
        Return:
        - Label confidence dalam bentuk teks.
        """

        if is_proven:
            return "terdiagnosis kuat"
        if percent >= 66:
            return "kemungkinan besar"
        if percent >= 50:
            return "kemungkinan"
        return "kemungkinan kecil"

    def _format_symptom_diagnosis(self, diagnosis: Dict, detected_symptoms: List[str]) -> str:
        """
        Membuat teks jawaban chatbot untuk hasil diagnosis berdasarkan gejala.
        Fungsi ini mengubah data diagnosis menjadi kalimat yang enak dibaca user.
        Isi jawaban:
        1. Nama penyakit yang paling mungkin.
        2. Tingkat kecocokan.
        3. Gejala yang cocok.
        4. Gejala pembeda yang belum disebutkan.
        5. Penyebab penyakit.
        6. Solusi/pengobatan.
        7. Pencegahan.
        8. Catatan agar user tetap memakai halaman konsultasi untuk hasil lebih akurat.
        Parameter:
        - diagnosis: dictionary hasil diagnosis terbaik.
        - detected_symptoms: list semua gejala yang terdeteksi dari kalimat user.
          Parameter ini disiapkan jika nanti ingin ditampilkan semua gejala terdeteksi.
        Return:
        - String jawaban chatbot.
        """

        # Ambil data penyakit dari hasil diagnosis.
        disease = diagnosis["penyakit"]

        # Ambil nama penyakit.
        disease_name = disease.get("nama", "Penyakit tidak diketahui")

        # Ambil ikon penyakit, jika ada.
        icon = disease.get("ikon", "🔎")

        # Ambil label confidence.
        label = self._confidence_label(diagnosis["persen"], diagnosis["is_terbukti"])

        # Ubah kode gejala cocok menjadi nama gejala.
        matched_names = [
            self.gejala_data.get(code, code)
            for code in diagnosis["gejala_cocok"]
        ]

        # Ubah kode gejala kurang menjadi nama gejala.
        missing_names = [
            self.gejala_data.get(code, code)
            for code in diagnosis["gejala_kurang"]
        ]

        # Kalimat pembuka hasil diagnosis.
        response = (
            f"{icon} Berdasarkan gejala yang Anda sebutkan, tanaman jagung kemungkinan mengalami {disease_name}.\n\n"
            f"Tingkat kecocokan: {diagnosis['persen']}% ({label}).\n\n"
            "Gejala yang cocok:\n"
        )

        # Tambahkan daftar gejala yang cocok.
        for item in matched_names:
            response += f"• {item}\n"

        # Jika ada gejala rule yang belum disebutkan, tampilkan sebagai gejala pembeda.
        if missing_names:
            response += "\nGejala pembeda yang belum disebutkan:\n"
            for item in missing_names:
                response += f"• {item}\n"
            response += "\nJika gejala pembeda tersebut juga terlihat, diagnosis menjadi lebih kuat.\n"

        # Tambahkan penyebab penyakit jika tersedia.
        penyebab = disease.get("penyebab")
        if penyebab:
            response += f"\nPenyebab: {penyebab}.\n"

        # Tambahkan solusi/pengobatan jika tersedia.
        pengobatan = disease.get("pengobatan", [])
        if pengobatan:
            response += "\nSolusi / pengobatan:\n"
            for index, item in enumerate(pengobatan, 1):
                response += f"{index}. {self._clean_html(item)}\n"

        # Tambahkan pencegahan jika tersedia.
        pencegahan = disease.get("pencegahan", [])
        if pencegahan:
            response += "\nPencegahan:\n"
            for index, item in enumerate(pencegahan, 1):
                response += f"{index}. {self._clean_html(item)}\n"

        # Catatan akhir agar user tahu chatbot hanya bantuan cepat.
        response += "\nCatatan: Untuk hasil yang lebih akurat, cocokkan kembali gejala pada halaman konsultasi sistem pakar."

        return response.strip()

    def _format_disease_detail(self, disease_info: Dict) -> str:
        """
        Membuat jawaban ketika user bertanya langsung tentang nama penyakit.
        Contoh:
        User:
        "Apa itu penyakit bulai?"
        Chatbot akan menjawab:
        - Nama penyakit
        - Penyebab
        - Deskripsi
        - Pengobatan
        - Pencegahan
        Parameter:
        - disease_info: dictionary detail penyakit dari PENYAKIT.
        Return:
        - String jawaban chatbot.
        """

        # Ambil data dasar penyakit.
        disease_name = disease_info.get("nama", "Penyakit")
        icon = disease_info.get("ikon", "🔎")
        penyebab = disease_info.get("penyebab", "Tidak diketahui")
        deskripsi = disease_info.get("deskripsi", "")
        pengobatan = disease_info.get("pengobatan", [])
        pencegahan = disease_info.get("pencegahan", [])

        # Susun bagian awal jawaban.
        response = f"{icon} {disease_name}\n\n"
        response += f"Penyebab: {penyebab}\n"

        # Tambahkan deskripsi.
        if deskripsi:
            response += f"\nPenjelasan:\n{deskripsi}\n"

        # Tambahkan daftar pengobatan.
        if pengobatan:
            response += "\nPengobatan:\n"
            for index, item in enumerate(pengobatan, 1):
                response += f"{index}. {self._clean_html(item)}\n"

        # Tambahkan daftar pencegahan.
        if pencegahan:
            response += "\nPencegahan:\n"
            for index, item in enumerate(pencegahan, 1):
                response += f"{index}. {self._clean_html(item)}\n"

        return response.strip()

    def _format_general_response(self, snippet: str) -> str:
        """
        Membuat format jawaban untuk pertanyaan umum dari knowledge.txt.
        Fungsi ini dipakai jika pertanyaan user tidak terdeteksi sebagai:
        - Sapaan
        - Pertanyaan penyakit
        - Pertanyaan gejala
        Parameter:
        - snippet: potongan paragraf paling relevan dari knowledge.txt.
        Return:
        - String jawaban chatbot.
        """

        return (
            f"Berikut informasi yang saya temukan:\n\n"
            f"{snippet}\n\n"
            f"Ada hal lain yang ingin ditanyakan tentang tanaman jagung?"
        )

    def _search_with_tfidf(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Mencari jawaban umum di knowledge.txt menggunakan TF-IDF.
        Alur kerja:
        1. Ubah pertanyaan user menjadi vector TF-IDF.
        2. Bandingkan vector pertanyaan dengan vector setiap paragraf.
        3. Hitung cosine similarity.
        4. Ambil paragraf dengan skor kemiripan tertinggi.
        5. Hanya ambil hasil dengan skor minimal 0.12.
        Parameter:
        - query: pertanyaan user.
        - top_k: jumlah maksimal hasil yang ingin diambil.
        Return:
        - List dictionary hasil pencarian.
        """

        # Jika TF-IDF tidak tersedia, gunakan pencarian fallback.
        if self.tfidf_matrix is None or not self.paragraphs:
            return self._fallback_search(query)

        try:
            # Mengubah pertanyaan user menjadi vector TF-IDF.
            query_vector = self.vectorizer.transform([query])

            # Menghitung kemiripan antara pertanyaan user dan semua paragraf.
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

            # Mengambil index paragraf dengan skor tertinggi.
            top_indices = np.argsort(similarities)[::-1][:top_k]

            # List hasil pencarian.
            results = []

            # Loop paragraf terbaik.
            for index in top_indices:
                score = float(similarities[index])

                # Threshold 0.12 digunakan agar jawaban tidak terlalu ngawur,
                # tetapi masih cukup fleksibel untuk pertanyaan umum.
                if score >= 0.12:
                    results.append({
                        "paragraph": self.paragraphs[index],
                        "snippet": self._extract_snippet(self.paragraphs[index], query),
                        "score": score,
                    })

            return results

        except Exception as error:
            # Jika TF-IDF error, gunakan pencarian sederhana.
            print(f"[Chatbot] Error TF-IDF: {error}")
            return self._fallback_search(query)

    def _fallback_search(self, query: str) -> List[Dict]:
        """
        Pencarian cadangan jika TF-IDF gagal atau tidak tersedia.
        Cara kerja:
        - Tokenisasi pertanyaan user.
        - Tokenisasi setiap paragraf knowledge.txt.
        - Hitung berapa kata penting yang sama.
        - Jika persentase kecocokan cukup tinggi, paragraf dianggap relevan.
        Parameter:
        - query: pertanyaan user.
        Return:
        - List dictionary hasil pencarian.
        """

        # Ubah pertanyaan user menjadi token penting.
        query_tokens = self._tokenize(query)

        # Jika tidak ada token penting, return list kosong.
        if not query_tokens:
            return []

        # List hasil pencarian.
        results = []

        # Loop semua paragraf.
        for paragraph in self.paragraphs:
            # Token paragraf.
            paragraph_tokens = self._tokenize(paragraph)

            # Hitung jumlah token query yang ada di paragraf.
            matches = sum(1 for token in query_tokens if token in paragraph_tokens)

            # Jika ada kata yang cocok, hitung skornya.
            if matches > 0:
                score = matches / len(query_tokens)

                # Minimal skor 0.35 agar hasil tidak terlalu jauh.
                if score >= 0.35:
                    results.append({
                        "paragraph": paragraph,
                        "snippet": self._extract_snippet(paragraph, query),
                        "score": score,
                    })

        # Urutkan hasil berdasarkan skor tertinggi.
        results.sort(key=lambda item: item["score"], reverse=True)

        # Ambil maksimal 3 hasil.
        return results[:3]

    def _extract_snippet(self, text: str, query: str, max_length: int = 350) -> str:
        """
        Mengambil potongan teks pendek dari paragraf knowledge.txt.
        Fungsi ini membuat jawaban tidak terlalu panjang.
        Chatbot hanya menampilkan bagian paragraf yang paling dekat
        dengan kata kunci pertanyaan user.
        Alur kerja:
        1. Bersihkan paragraf.
        2. Cari posisi kata penting dari query di paragraf.
        3. Ambil potongan teks di sekitar posisi tersebut.
        4. Jika terlalu panjang, potong maksimal 350 karakter.
        Parameter:
        - text: paragraf penuh dari knowledge.txt.
        - query: pertanyaan user.
        - max_length: panjang maksimal potongan teks.
        Return:
        - String snippet/potongan paragraf.
        """

        # Merapikan spasi paragraf.
        text = re.sub(r"\s+", " ", text).strip()

        # Token penting dari pertanyaan user.
        query_tokens = self._tokenize(query)

        # Versi lowercase dari paragraf untuk pencarian posisi kata.
        text_lower = text.lower()

        # Posisi awal kata penting di paragraf.
        best_position = -1

        # Cari token pertama yang muncul di paragraf.
        for token in query_tokens:
            position = text_lower.find(token)
            if position != -1:
                best_position = position
                break

        # Jika tidak ada token yang ditemukan, ambil dari awal paragraf.
        if best_position == -1:
            snippet = text[:max_length]

        # Jika token ditemukan, ambil teks di sekitar token tersebut.
        else:
            start = max(0, best_position - 80)
            end = min(len(text), best_position + max_length)
            snippet = text[start:end]

        # Jika snippet masih terlalu panjang, potong dengan rapi.
        if len(snippet) > max_length:
            snippet = snippet[:max_length].strip()

            # Cari spasi terakhir agar pemotongan tidak memutus kata.
            last_space = snippet.rfind(" ")
            if last_space > 0:
                snippet = snippet[:last_space]

            snippet += "..."

        return snippet.strip()
