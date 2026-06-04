import string
import random
from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class JaguKnowledgeBase:
    """Knowledge base dengan conversational AI untuk chatbot manusiawi."""

    # Greeting responses
    GREETINGS = {
        'salam': ['Halo! 👋 Senang bertemu Anda. Ada yang bisa saya bantu tentang jagung?', 
                  'Pagi! 🌅 Apa pertanyaan Anda tentang jagung?',
                  'Halo teman! 😊 Saya siap membantu tentang budidaya jagung.'],
        'thank': ['Sama-sama! 😊 Ada lagi yang ingin ditanyakan?',
                  'Senang membantu! 🌽 Butuh info lainnya?',
                  'Terima kasih kembali! Jangan ragu untuk bertanya lagi.'],
        'bye': ['Sampai jumpa! 👋 Semoga tanamanmu tumbuh subur!',
                'Bye! 🌽 Semoga sukses bercocok tanam!',
                'Sampai lagi! Jangan lupa rawat tanamanmu dengan baik!']
    }

    # Encouraging messages
    ENCOURAGEMENTS = [
        '🌱 Pertanyaan yang bagus!',
        '💡 Itu informasi yang penting!',
        '👍 Bagus! Kamu peduli dengan tanaman.',
        '✨ Semangat belajar cocok tanam!',
        '🎯 Pertanyaan yang tepat untuk hasil panen maksimal!',
    ]

    # Follow-up suggestions
    SUGGESTIONS_MAP = {
        'tanam': ['Sudahkah Anda tahu tentang jarak tanam yang tepat?', 'Apakah Anda ingin tahu tentang pemilihan benih?'],
        'penyakit': ['Ingin tahu cara mencegah penyakit ini?', 'Apakah Anda tertarik dengan pengendalian hama?'],
        'pupuk': ['Ingin tahu dosis pemupukan yang tepat?', 'Apakah Anda penasaran dengan jenis pupuk lainnya?'],
        'panen': ['Ingin tips penyimpanan hasil panen?', 'Apakah Anda tahu cara memilih jagung yang matang?'],
        'varietas': ['Tertarik belajar tentang penyakit yang rentan pada varietas ini?', 'Ingin tahu keuntungan varietas lain?'],
    }

    def __init__(self, knowledge_file: str = 'knowledge.txt', penyakit_data: Dict = None, gejala_data: Dict = None):
        self.knowledge_file = knowledge_file
        self.content = ""
        self.paragraphs = []
        self.penyakit_data = penyakit_data or {}
        self.gejala_data = gejala_data or {}
        
        print(f"[Chatbot Init] penyakit_data: {len(self.penyakit_data)} diseases")
        print(f"[Chatbot Init] gejala_data: {len(self.gejala_data)} symptoms")
        
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words=self._get_stopwords(),
            token_pattern=r'\b[a-z]{2,}\b',
            max_features=500
        )
        self.tfidf_matrix = None
        self.conversation_count = 0
        self._load_knowledge()
        self._build_tfidf_index()

    def _get_stopwords(self) -> List[str]:
        """Stopwords Bahasa Indonesia."""
        return [
            'dan', 'atau', 'yang', 'di', 'ke', 'dari', 'pada', 'untuk', 'adalah',
            'ini', 'itu', 'dengan', 'oleh', 'dalam', 'ke', 'jika', 'maka', 'dapat',
            'akan', 'telah', 'sudah', 'juga', 'saja', 'saat', 'karena', 'sebab',
            'namun', 'tetapi', 'tapi', 'sementara', 'lalu', 'kemudian', 'sering',
            'jarang', 'selalu', 'tidak', 'belum', 'pun', 'pula', 'sampai', 'hingga',
            'sebelum', 'sesudah', 'sekali', 'dua', 'tiga', 'empat', 'lima', 'enam',
            'tujuh', 'delapan', 'sembilan', 'sepuluh', 'ribuan', 'jutaan',
            'ada', 'berada', 'terdapat'
        ]

    def _load_knowledge(self):
        """Load knowledge dari knowledge.txt."""
        try:
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                self.content = f.read()
            
            # Split menjadi paragraf (split by double newline)
            self.paragraphs = [
                p.strip() 
                for p in self.content.split('\n\n') 
                if p.strip() and len(p.strip()) > 20
            ]
            print(f"✓ Knowledge loaded: {len(self.paragraphs)} paragraphs")
        except FileNotFoundError as e:
            print(f"⚠ Knowledge file not found: {self.knowledge_file}")
            self.content = "Knowledge file tidak ditemukan"
            self.paragraphs = [self.content]
        except Exception as e:
            print(f"✗ Error loading knowledge: {e}")
            self.paragraphs = []

    def _build_tfidf_index(self):
        """Build TF-IDF matrix untuk semua paragraf."""
        if not self.paragraphs:
            return
        
        try:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.paragraphs)
        except Exception as e:
            print(f"Error building TF-IDF: {e}")
            self.tfidf_matrix = None

    def _tokenize(self, text: str) -> List[str]:
        """Tokenisasi dan normalize text."""
        # Lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Split by whitespace
        tokens = text.split()
        
        # Remove stopwords dan tokens pendek
        tokens = [
            t for t in tokens 
            if t not in self._get_stopwords() and len(t) > 2
        ]
        
        return tokens

    def get_response(self, query: str) -> Dict:
        """Generate response untuk query user."""
        query = query.strip()

        if not query:
            return {
                'success': False,
                'message': 'Silakan masukkan pertanyaan tentang jagung.',
                'type': 'error',
            }

        query_lower = query.lower()
        self.conversation_count += 1
        
        print(f"[Query] '{query}'")

        # Check greeting/farewell
        greeting_response = self._detect_greeting_farewell(query_lower)
        if greeting_response:
            print(f"[Match] Greeting/Farewell")
            return greeting_response

        # Check disease/symptom questions
        disease_response = self._detect_disease_question(query_lower)
        if disease_response:
            print(f"[Match] Disease detected")
            return disease_response

        # Search knowledge base
        print(f"[Search] TF-IDF search...")
        results = self._search_with_tfidf(query)

        if not results:
            return {
                'success': False,
                'message': '😔 Maaf, saya belum menemukan informasi itu. Coba tanyakan tentang:\n\n🌱 Varietas jagung\n🦠 Penyakit jagung\n🌾 Cara penanaman\n🥗 Pemupukan\n🌽 Panen\n\nAda yang bisa saya bantu?',
                'type': 'not_found',
                'is_fallback': True,
            }

        # Get best result
        best_result = results[0]
        
        # Generate conversational message
        response_message = self._format_conversational_response(
            best_result['snippet'],
            query_lower,
            best_result['score']
        )
        
        return {
            'success': True,
            'message': response_message,
            'type': 'success',
            'confidence': f"{best_result['score']:.0%}",
        }

    def _detect_greeting_farewell(self, query_lower: str) -> Dict | None:
        """Detect greeting dan farewell messages."""
        # Greeting keywords
        greeting_keywords = ['halo', 'hai', 'pagi', 'siang', 'sore', 'malam', 'siapa', 'apa kabar', 'boleh nanya']
        for keyword in greeting_keywords:
            if keyword in query_lower:
                message = random.choice(self.GREETINGS['salam'])
                return {
                    'success': True,
                    'message': message,
                    'type': 'greeting',
                }
        
        # Thank you keywords
        thank_keywords = ['terima kasih', 'makasih', 'thanks', 'thx', 'tq', 'tks']
        for keyword in thank_keywords:
            if keyword in query_lower:
                message = random.choice(self.GREETINGS['thank'])
                return {
                    'success': True,
                    'message': message,
                    'type': 'thank',
                }
        
        # Goodbye keywords
        bye_keywords = ['bye', 'dah', 'dadah', 'sampai jumpa', 'selamat tinggal', 'goodbye']
        for keyword in bye_keywords:
            if keyword in query_lower:
                message = random.choice(self.GREETINGS['bye'])
                return {
                    'success': True,
                    'message': message,
                    'type': 'farewell',
                }
        
        return None

    def _format_conversational_response(self, snippet: str, query_lower: str, confidence: float) -> str:
        """Format response dengan tone yang lebih manusiawi dan ringkas."""
        # Add encouragement (50% chance)
        encouragement = random.choice(self.ENCOURAGEMENTS) if random.random() > 0.5 else ""
        
        # Main answer dengan formatting lebih baik
        if encouragement:
            main_answer = f"{encouragement}\n\n{snippet}"
        else:
            main_answer = snippet
        
        # Add suggestion based on query topic
        suggestion = self._get_suggestion(query_lower)
        
        # Add follow-up question
        follow_up_questions = [
            "\n\n❓ Ada pertanyaan lain tentang jagung?",
            "\n\n💭 Perlu penjelasan lebih?",
            "\n\n🤔 Ada yang ingin ditanyakan lagi?",
        ]
        
        follow_up = random.choice(follow_up_questions)
        
        if suggestion:
            return f"{main_answer}\n\n💡 {suggestion}{follow_up}"
        else:
            return f"{main_answer}{follow_up}"

    def _get_suggestion(self, query_lower: str) -> str | None:
        """Generate suggestion based on query topic."""
        for topic, suggestions in self.SUGGESTIONS_MAP.items():
            if topic in query_lower:
                return random.choice(suggestions)
        return None

    def _detect_disease_question(self, query_lower: str) -> Dict | None:
        """Detect kalau user bertanya tentang penyakit atau gejala tertentu."""
        if not self.penyakit_data:
            print(f"[Disease] penyakit_data is empty, skipping...")
            return None

        # Disease keywords for detection
        disease_keywords = ['penyakit', 'sakit', 'gejala', 'tanda', 'ciri', 'apa itu', 'bagaimana', 'cara', 'obat', 'pengobatan', 'pencegahan', 'hama']
        
        # Check jika query mengandung disease keywords
        has_disease_keyword = any(kw in query_lower for kw in disease_keywords)
        print(f"[Disease] has_disease_keyword: {has_disease_keyword}")
        
        if not has_disease_keyword:
            return None

        # Search disease by name or keywords
        matched_disease = None
        
        for disease_code, disease_info in self.penyakit_data.items():
            disease_name = disease_info.get('nama', '').lower()
            disease_cause = disease_info.get('penyebab', '').lower()
            
            # Check jika nama penyakit ada di query
            if disease_name and disease_name in query_lower:
                print(f"[Disease] Matched by name: {disease_code} - {disease_name}")
                matched_disease = (disease_code, disease_info)
                break
            
            # Check jika keyword dari penyebab ada di query
            if disease_cause:
                cause_keywords = disease_cause.split()
                for keyword in cause_keywords:
                    if len(keyword) > 3 and keyword in query_lower:
                        print(f"[Disease] Matched by cause keyword: {disease_code} - {keyword}")
                        matched_disease = (disease_code, disease_info)
                        break
                if matched_disease:
                    break

        if matched_disease:
            disease_code, disease_info = matched_disease
            response_message = self._format_disease_response(disease_info)
            
            return {
                'success': True,
                'message': response_message,
                'type': 'disease',
                'disease_code': disease_code,
            }

        print(f"[Disease] No disease matched")
        return None

    def _format_disease_response(self, disease_info: Dict) -> str:
        """Format disease information menjadi response yang detail dan terstruktur."""
        disease_name = disease_info.get('nama', 'Penyakit')
        penyebab = disease_info.get('penyebab', 'Tidak diketahui')
        deskripsi = disease_info.get('deskripsi', '')
        pengobatan = disease_info.get('pengobatan', [])
        pencegahan = disease_info.get('pencegahan', [])
        ikon = disease_info.get('ikon', '🔍')

        # Build response
        response = f"{ikon} **{disease_name}**\n\n"
        
        # Penyebab
        response += f"🔬 **Penyebab**: {penyebab}\n\n"
        
        # Deskripsi
        if deskripsi:
            response += f"📖 **Penjelasan**: {deskripsi}\n\n"
        
        # Pengobatan
        if pengobatan:
            response += f"💊 **Pengobatan**:\n"
            for i, treatment in enumerate(pengobatan, 1):
                # Remove HTML tags untuk display
                clean_treatment = treatment.replace('<strong>', '').replace('</strong>', '').replace('<em>', '').replace('</em>', '')
                response += f"   {i}. {clean_treatment}\n"
            response += "\n"
        
        # Pencegahan
        if pencegahan:
            response += f"🛡️ **Pencegahan**:\n"
            for i, prevention in enumerate(pencegahan, 1):
                # Remove HTML tags
                clean_prevention = prevention.replace('<strong>', '').replace('</strong>', '').replace('<em>', '').replace('</em>', '')
                response += f"   {i}. {clean_prevention}\n"
            response += "\n"
        
        response += "\n💡 Informasi lengkap telah ditampilkan. Ada pertanyaan lain?"
        
        return response

    def _search_with_tfidf(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search menggunakan TF-IDF similarity (Cosine Similarity)."""
        if self.tfidf_matrix is None or len(self.paragraphs) == 0:
            return self._fallback_search(query)

        try:
            # Vectorize query menggunakan fitted vectorizer
            query_vector = self.vectorizer.transform([query])
            
            # Compute cosine similarity dengan semua paragraf
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Get top-k results dengan score tertinggi
            top_indices = np.argsort(similarities)[::-1][:top_k]
            top_scores = similarities[top_indices]
            
            results = []
            for idx, score in zip(top_indices, top_scores):
                if score > 0.1:  # Minimum relevance threshold
                    snippet = self._extract_snippet(self.paragraphs[idx], query)
                    results.append({
                        'paragraph': self.paragraphs[idx],
                        'snippet': snippet,
                        'score': score,
                        'index': idx,
                    })
            
            return results
        except Exception as e:
            print(f"Error in TF-IDF search: {e}")
            return self._fallback_search(query)

    def _fallback_search(self, query: str) -> List[Dict]:
        """Fallback search jika TF-IDF gagal (token-based matching)."""
        query_tokens = self._tokenize(query)
        
        if not query_tokens:
            return []

        results = []
        for para in self.paragraphs:
            para_tokens = self._tokenize(para)
            
            # Count matching tokens
            matches = sum(1 for token in query_tokens if token in para_tokens)
            
            if matches > 0:
                score = matches / len(query_tokens)
                snippet = self._extract_snippet(para, query)
                results.append({
                    'paragraph': para,
                    'snippet': snippet,
                    'score': score,
                })

        # Sort by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:3]

    def _extract_snippet(self, text: str, query: str, max_length: int = 180) -> str:
        """Extract snippet yang relevan dengan context dan lebih ringkas."""
        text_lower = text.lower()
        query_lower = query.lower()

        # Cari query dalam text (case-insensitive)
        idx = text_lower.find(query_lower)

        if idx != -1:
            # Temukan awal kalimat sebelum match
            start = text.rfind('. ', 0, idx)
            if start == -1:
                start = 0
            else:
                start += 2

            # Temukan akhir kalimat setelah match
            end = text.find('. ', idx)
            if end == -1:
                end = len(text)
            else:
                end += 1

            snippet = text[start:end].strip()
        else:
            # Fallback: ambil awal text
            snippet = text[:max_length].strip()

        # Smart truncation: jika snippet > max_length
        if len(snippet) > max_length:
            snippet = snippet[:max_length].strip()
            # Potong di kata terakhir yang complete
            last_space = snippet.rfind(' ')
            if last_space > max_length * 0.7:  # jika ada space di 70% ke atas
                snippet = snippet[:last_space]
            snippet += '...'

        return snippet if snippet else text[:max_length]
