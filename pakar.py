from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ============================================================
# KNOWLEDGE BASE
# ============================================================

GEJALA = {
    'G1':  'Daun menguning pucat',
    'G2':  'Pertumbuhan tanaman menjadi kerdil',
    'G3':  'Muncul bercak coklat kemerahan pada daun seperti karat',
    'G4':  'Terdapat bercak titik-titik memanjang sempit berwarna coklat tua hingga coklat kekuningan',
    'G5':  'Daun menguning dimulai dari ujung daun',
    'G6':  'Daun mengering sebelum waktunya',
    'G7':  'Muncul bercak memanjang berwarna coklat keabu-abuan pada daun',
    'G8':  'Batang tanaman menjadi lunak dan berair',
    'G9':  'Bagian dalam batang berwarna coklat',
    'G10': 'Tanaman mudah roboh',
    'G11': 'Tongkol jagung berjamur',
    'G12': 'Tongkol mengeluarkan bau tidak sedap',
    'G13': 'Tongkol mengalami pembusukan',
    'G14': 'Daun tanaman berlubang',
    'G15': 'Terdapat kotoran hama yang menyerupai serbuk pada daun',
    # Gejala pembeda tambahan (G16–G19)
    'G16': 'Terdapat lapisan tepung putih/abu-abu di bawah permukaan daun pada pagi hari',
    'G17': 'Bercak pada daun terasa kasar atau timbul jika diraba (seperti amplas halus)',
    'G18': 'Terdapat kerusakan pada pucuk/titik tumbuh daun muda (pupus)',
    'G19': 'Terdapat lendir atau bau busuk menyengat pada pangkal batang',
}

KELOMPOK_GEJALA = [
    {
        'label': 'Gejala pada Daun',
        'icon': '🌿',
        'kode': ['G1', 'G3', 'G4', 'G5', 'G6', 'G7', 'G14', 'G15', 'G16', 'G17', 'G18'],
    },
    {
        'label': 'Gejala pada Pertumbuhan Tanaman',
        'icon': '🌱',
        'kode': ['G2'],
    },
    {
        'label': 'Gejala pada Batang',
        'icon': '🪵',
        'kode': ['G8', 'G9', 'G10', 'G19'],
    },
    {
        'label': 'Gejala pada Tongkol',
        'icon': '🌽',
        'kode': ['G11', 'G12', 'G13'],
    },
]

PENYAKIT = {
    'P1': {
        'nama': 'Penyakit Bulai',
        'penyebab': 'Jamur Peronosclerospora spp.',
        'deskripsi': (
            'Penyakit bulai merupakan salah satu penyakit yang sering menyerang tanaman jagung. '
            'Biasanya mulai menyerang tanaman jagung pada umur sekitar 21 hari setelah tanam.'
        ),
        'umur_tanaman': (0, 30),   # 0–30 HST (fase vegetatif awal)
        'pengobatan': [
            'Semprotkan fungisida <strong>Antracol</strong> dua kali dalam seminggu hingga penyakit menghilang.',
            'Berikan pupuk <strong>Ultradap</strong> dan <strong>Grandasil</strong> untuk memperkuat akar dan batang '
            '(diaplikasikan mulai umur 15 hari tanaman).',
        ],
        'pencegahan': [
            'Gunakan benih varietas hibrida yang tahan penyakit bulai.',
            'Lakukan <em>seed treatment</em> (perlakuan benih) dengan fungisida berbahan aktif '
            '<strong>metalaksil</strong> sebelum tanam untuk menekan infeksi dini.',
        ],
        'warna': 'warning',
        'ikon': '🟡',
    },
    'P2': {
        'nama': 'Penyakit Karat Daun',
        'penyebab': 'Jamur Puccinia polysora dan Puccinia sorghi',
        'deskripsi': (
            'Penyakit karat daun umumnya menyerang tanaman jagung pada umur sekitar 30 hari '
            'atau satu bulan setelah tanam.'
        ),
        'umur_tanaman': (30, 60),  # 30–60 HST (fase vegetatif akhir–generatif)
        'pengobatan': [
            'Semprotkan fungisida <strong>Amistar Top</strong> sebanyak dua kali dalam seminggu hingga penyakit menghilang.',
        ],
        'pencegahan': [
            'Lakukan pemantauan rutin mulai tanaman berumur 3 minggu untuk mendeteksi gejala awal.',
            'Pilih varietas jagung yang memiliki ketahanan terhadap penyakit karat daun.',
        ],
        'warna': 'danger',
        'ikon': '🟤',
    },
    'P3': {
        'nama': 'Penyakit Hawar Daun',
        'penyebab': 'Jamur Helminthosporium turcicum',
        'deskripsi': (
            'Penyakit hawar daun dapat menyebabkan penurunan produktivitas tanaman jagung '
            'apabila tidak segera ditangani.'
        ),
        'umur_tanaman': (30, 60),  # 30–60 HST (fase vegetatif akhir–generatif)
        'pengobatan': [
            'Semprotkan fungisida <strong>Amistar Top</strong> sebanyak dua kali dalam seminggu hingga penyakit hawar daun hilang.',
        ],
        'pencegahan': [
            'Jaga jarak tanam yang cukup renggang agar sirkulasi udara di sekitar kanopi tanaman tetap baik.',
            'Lakukan rotasi tanaman untuk memutus siklus patogen di dalam tanah '
            '(hindari menanam jagung secara terus-menerus di lahan yang sama).',
        ],
        'warna': 'danger',
        'ikon': '🟠',
    },
    'P4': {
        'nama': 'Penyakit Busuk Batang',
        'penyebab': 'Jamur (dipicu curah hujan tinggi, jarak tanam rapat, dan drainase buruk)',
        'deskripsi': (
            'Penyakit busuk batang disebabkan oleh jamur dan biasanya terjadi akibat curah hujan yang tinggi, '
            'jarak tanam yang terlalu rapat, serta drainase yang buruk sehingga terjadi genangan air.'
        ),
        'umur_tanaman': (60, 120), # 60–120 HST (fase pengisian biji)
        'pengobatan': [
            'Cabut dan musnahkan tanaman yang telah terinfeksi agar penyakit tidak menyebar ke tanaman lainnya.',
            '<em>Catatan teknis:</em> Gunakan alat semprot/cangkul yang telah disterilkan '
            '(dicuci bersih dan direndam desinfektan) setelah menangani tanaman sakit '
            'agar tidak menulari tanaman sehat.',
        ],
        'pencegahan': [
            'Perbaiki sistem drainase lahan agar air tidak menggenang di sekitar perakaran tanaman.',
            'Kurangi dosis pupuk Nitrogen (Urea) saat musim hujan untuk menghindari pertumbuhan jaringan yang terlalu lunak.',
            'Atur jarak tanam yang memadai agar tidak terlalu rapat.',
        ],
        'warna': 'dark',
        'ikon': '⚫',
    },
    'P5': {
        'nama': 'Penyakit Busuk Tongkol',
        'penyebab': 'Jamur (dipicu curah hujan tinggi dan jarak tanam rapat)',
        'deskripsi': (
            'Penyakit busuk tongkol disebabkan oleh jamur dan biasanya terjadi karena curah hujan yang tinggi '
            'serta jarak tanam yang terlalu rapat sehingga sinar matahari yang mengenai tongkol menjadi terbatas.'
        ),
        'umur_tanaman': (60, 120), # 60–120 HST (fase pengisian biji)
        'pengobatan': [
            'Cabut dan musnahkan tanaman atau tongkol yang terinfeksi agar penyakit tidak menyebar ke tanaman lain.',
            '<em>Catatan teknis:</em> Gunakan alat semprot/cangkul yang telah disterilkan '
            '(dicuci bersih dan direndam desinfektan) setelah menangani tanaman sakit '
            'agar tidak menulari tanaman sehat.',
        ],
        'pencegahan': [
            'Perbaiki sistem drainase lahan agar air tidak menggenang.',
            'Kurangi dosis pupuk Nitrogen (Urea) saat musim hujan.',
            'Atur jarak tanam yang memadai agar sinar matahari dapat menyinari tongkol secara optimal.',
        ],
        'warna': 'secondary',
        'ikon': '🔵',
    },
    'P6': {
        'nama': 'Hama Ulat Grayak',
        'penyebab': 'Ulat grayak (hama invasif)',
        'deskripsi': (
            'Ulat grayak merupakan hama invasif yang sering menyerang tanaman jagung, terutama pada malam hari. '
            'Hama ini dapat menyerang daun, batang, hingga tongkol tanaman jagung. '
            'Serangan biasanya terjadi pada tanaman berumur 20 hari hingga 2 bulan.'
        ),
        'umur_tanaman': (20, 60),  # 20–60 HST
        'pengobatan': [
            'Semprotkan insektisida <strong>Proclaim</strong> sebanyak satu kali dalam seminggu.',
            '<em>Catatan teknis:</em> Semprotkan pada <strong>malam hari atau pagi buta</strong>; '
            'arahkan nozzle sprayer tepat ke dalam pucuk daun (<em>pupus</em>) '
            'karena ulat bersembunyi di sana saat siang hari.',
        ],
        'pencegahan': [
            'Lakukan rotasi tanaman untuk memutus siklus hidup hama '
            '(hindari menanam jagung secara terus-menerus di lahan yang sama).',
            'Pasang perangkap feromon untuk memantau dan menekan populasi ngengat dewasa.',
            'Lakukan pengamatan rutin pada malam hari, terutama saat tanaman masih muda.',
        ],
        'warna': 'success',
        'ikon': '🟢',
    },
}

# Rule IF–THEN dengan gejala pembeda tambahan (G16–G19 memperkuat diagnosis)
RULES = [
    {'conditions': ['G1', 'G2', 'G16'], 'result': 'P1'},  # Rule 1 – Bulai (+ lapisan tepung putih)
    {'conditions': ['G3', 'G4', 'G17'], 'result': 'P2'},  # Rule 2 – Karat Daun (+ bercak kasar/timbul)
    {'conditions': ['G5', 'G6', 'G7'],  'result': 'P3'},  # Rule 3 – Hawar Daun
    {'conditions': ['G8', 'G9', 'G10', 'G19'], 'result': 'P4'},  # Rule 4 – Busuk Batang (+ lendir/bau pangkal)
    {'conditions': ['G11', 'G12', 'G13'],       'result': 'P5'},  # Rule 5 – Busuk Tongkol
    {'conditions': ['G14', 'G15', 'G18'],       'result': 'P6'},  # Rule 6 – Ulat Grayak (+ kerusakan pucuk)
]

# ============================================================
# INFERENCE ENGINE (Backward Chaining)
# ============================================================

def _confidence_label(persen: int) -> tuple[str, str]:
    """Mengembalikan (label_teks, level) berdasarkan persentase kecocokan."""
    if persen == 100:
        return 'Terdiagnosis',      'high'
    elif persen >= 66:
        return 'Kemungkinan Besar', 'medium-high'
    elif persen >= 50:
        return 'Kemungkinan',       'medium'
    else:
        return 'Kemungkinan Kecil', 'low'


def _prove_goal(goal: str, facts: set[str], visited: set[str] | None = None) -> bool:
    """Membuktikan goal menggunakan backward chaining rekursif."""
    if goal in facts:
        return True

    # Gejala adalah fakta terminal: jika tidak ada di fakta maka gagal dibuktikan.
    if goal in GEJALA:
        return False

    if visited is None:
        visited = set()
    if goal in visited:
        return False
    visited.add(goal)

    # Cari rule yang menyimpulkan goal, lalu buktikan semua premisnya.
    kandidat_rule = [rule for rule in RULES if rule['result'] == goal]
    for rule in kandidat_rule:
        if all(_prove_goal(prasyarat, facts, visited.copy()) for prasyarat in rule['conditions']):
            return True

    return False


def backward_chaining(gejala_dipilih: list[str], umur_hst: int | None = None) -> list[dict]:
    """
    Inferensi backward chaining.
    Sistem menguji tiap hipotesis penyakit (goal) berdasarkan rule IF-THEN,
    lalu memeriksa apakah seluruh gejala prasyarat dapat dibuktikan dari fakta input.
    """
    fakta = set(gejala_dipilih)
    hasil = []

    for rule in RULES:
        total = len(rule['conditions'])
        gejala_cocok = [g for g in rule['conditions'] if g in fakta]
        gejala_kurang = [g for g in rule['conditions'] if g not in fakta]
        matched = len(gejala_cocok)

        # Sembunyikan hipotesis yang sama sekali tidak didukung fakta.
        if matched == 0:
            continue

        is_terbukti = _prove_goal(rule['result'], fakta)
        persen = round((matched / total) * 100)

        if is_terbukti:
            label_confidence, confidence_level = 'Terdiagnosis', 'high'
        else:
            label_confidence, confidence_level = _confidence_label(persen)

        penyakit = PENYAKIT[rule['result']]
        umur_warning = None
        if umur_hst is not None:
            fase_min, fase_max = penyakit['umur_tanaman']
            if not (fase_min <= umur_hst <= fase_max):
                umur_warning = (
                    f'Penyakit ini umumnya menyerang pada umur '
                    f'{fase_min}–{fase_max} HST, '
                    f'sementara tanaman Anda berumur {umur_hst} HST. '
                    f'Pertimbangkan diagnosis ini dengan hati-hati.'
                )

        hasil.append({
            'kode': rule['result'],
            'rule_conditions': rule['conditions'],
            'gejala_cocok': gejala_cocok,
            'gejala_kurang': gejala_kurang,
            'persen': persen,
            'matched': matched,
            'total': total,
            'is_terbukti': is_terbukti,
            'status_backward': 'Terbukti' if is_terbukti else 'Belum Terbukti',
            'label_confidence': label_confidence,
            'confidence_level': confidence_level,
            'umur_warning': umur_warning,
            **penyakit,
        })

    # Hipotesis terbukti ditaruh paling atas, lalu sisanya berdasar kecocokan terbesar.
    hasil.sort(key=lambda x: (x['is_terbukti'], x['persen']), reverse=True)
    return hasil

# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    total_penyakit = len(PENYAKIT)
    total_gejala = len(GEJALA)
    total_rule = len(RULES)
    return render_template('index.html',
                           total_penyakit=total_penyakit,
                           total_gejala=total_gejala,
                           total_rule=total_rule)


@app.route('/konsultasi')
def konsultasi():
    return render_template('konsultasi.html',
                           gejala=GEJALA,
                           kelompok=KELOMPOK_GEJALA)


@app.route('/diagnosa', methods=['POST'])
def diagnosa():
    gejala_dipilih = request.form.getlist('gejala')

    if not gejala_dipilih:
        return redirect(url_for('konsultasi'))

    # Ambil umur tanaman (opsional, validasi int)
    umur_hst: int | None = None
    try:
        umur_raw = request.form.get('umur_hst', '').strip()
        if umur_raw:
            umur_hst = max(1, min(int(umur_raw), 365))
    except ValueError:
        umur_hst = None

    hasil = backward_chaining(gejala_dipilih, umur_hst)
    gejala_terpilih = {k: GEJALA[k] for k in gejala_dipilih if k in GEJALA}

    return render_template('hasil.html',
                           hasil=hasil,
                           gejala_terpilih=gejala_terpilih,
                           umur_hst=umur_hst)


@app.route('/basis-pengetahuan')
def basis_pengetahuan():
    return render_template('basis_pengetahuan.html',
                           penyakit=PENYAKIT,
                           gejala=GEJALA,
                           rules=RULES)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
