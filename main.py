import sqlite3
from difflib import SequenceMatcher
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    ConversationHandler, filters
)
import re
import pandas as pd
import os

API_TOKEN = '8063639769:AAE9CUsrTtJ14_l2YHaOvG4zbylRvA4IxBk'

NAMA, KUIS1, KUIS2, KUIS3 = range(4)

# ======= DATABASE =======
def init_db():
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS siswa (
            telegram_id INTEGER PRIMARY KEY,
            nama TEXT,
            waktu_daftar TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS jawaban (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            pertemuan TEXT,
            soal TEXT,
            jawaban TEXT,
            benar INTEGER,
            waktu TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# ======= MATERI =======
materi_1 = """
📘 *Pertemuan 1: Media Transmisi Jaringan*

Media transmisi adalah saluran yang digunakan untuk mengirim data dari satu perangkat ke perangkat lainnya. Media ini dibagi menjadi dua kategori utama: *guided* (terarah) dan *unguided* (tidak terarah).

🔌 *Guided Media* (Media Berkabel):
Merupakan media transmisi yang menggunakan jalur fisik seperti kabel. Contohnya:

• **UTP (Unshielded Twisted Pair)**: 
  - Banyak digunakan dalam jaringan LAN.
  - Keunggulan: murah, fleksibel, dan mudah dipasang.
  - Kekurangan: mudah terkena interferensi elektromagnetik dan memiliki jangkauan yang terbatas.

• **Kabel Coaxial**:
  - Terdiri dari konduktor pusat, isolator, lapisan pelindung, dan jaket luar.
  - Lebih tahan terhadap interferensi dibanding UTP.
  - Banyak dipakai di CCTV dan jaringan TV kabel.

• **Fiber Optik**:
  - Menggunakan cahaya sebagai media transmisi melalui serat kaca.
  - Keunggulan utama: kecepatan tinggi, tahan terhadap gangguan elektromagnetik, cocok untuk jarak jauh.
  - Paling ideal digunakan pada backbone jaringan.

📡 *Unguided Media* (Media Nirkabel):
Tidak menggunakan kabel fisik. Data dikirim melalui gelombang elektromagnetik, seperti:

• **Wi-Fi, Bluetooth, Gelombang Radio**:
  - Lebih fleksibel untuk mobilitas tinggi.
  - Rentan terhadap gangguan sinyal dan keamanan.
  - Cocok untuk perangkat portabel atau lokasi sulit dijangkau kabel.

Kesimpulan:
Guided media cocok untuk koneksi stabil dan aman, sedangkan unguided media menawarkan fleksibilitas namun lebih rentan terhadap gangguan.
"""

materi_2 = """
📘 *Pertemuan 2: Struktur & Prinsip Kerja Fiber Optik*

Fiber optik terdiri dari tiga lapisan utama:

🔹 **Core**:
Bagian tengah yang sangat kecil (dalam mikrometer) tempat cahaya merambat. Bahan dasarnya adalah kaca atau plastik khusus dengan indeks bias tinggi.

🔹 **Cladding**:
Lapisan yang mengelilingi core, memiliki indeks bias lebih rendah untuk memungkinkan *pantulan total internal*.

🔹 **Coating atau Buffer**:
Lapisan pelindung tambahan untuk mencegah kerusakan fisik atau kelembaban.

✨ *Prinsip Pantulan Total Internal*:
Cahaya yang masuk pada sudut tertentu akan terpantul sempurna di dalam core karena perbedaan indeks bias antara core dan cladding. Inilah yang membuat cahaya tetap berada di dalam serat dan dapat menjangkau jarak sangat jauh tanpa banyak kehilangan sinyal.

💡 *Sumber Cahaya dalam Fiber Optik*:
• **LED (Light Emitting Diode)**:
  - Cocok untuk jarak pendek.
  - Murah dan awet, tapi kecepatannya lebih rendah.
• **Laser (Light Amplification by Stimulated Emission of Radiation)**:
  - Cocok untuk transmisi jarak jauh dan cepat.
  - Mahal, tapi menghasilkan cahaya terfokus dengan intensitas tinggi.

⚠️ *Bending Loss*:
Kerugian sinyal yang terjadi jika fiber ditekuk terlalu tajam sehingga cahaya bocor keluar dari core.

🏆 Keunggulan Fiber Optik:
- Bandwidth sangat tinggi.
- Tidak terpengaruh interferensi elektromagnetik.
- Lebih ringan dan fleksibel dibanding kabel tembaga.
"""

materi_3 = """
📘 *Pertemuan 3: Jenis Fiber Optik dan Aplikasinya*

Ada dua jenis utama serat optik berdasarkan mode transmisinya:

🔸 **Single-mode Fiber**:
- Memiliki core sangat kecil (sekitar 8–10 µm).
- Hanya mengalirkan satu mode cahaya.
- Digunakan untuk transmisi jarak jauh, seperti antar kota atau backbone ISP.
- Menggunakan sumber cahaya laser.

🔸 **Multi-mode Fiber**:
- Core lebih besar (50–62,5 µm).
- Mengalirkan banyak jalur cahaya secara bersamaan.
- Cocok untuk jarak pendek, seperti jaringan LAN dalam gedung.
- Sumber cahaya biasanya LED.

📌 *Aplikasi Umum Fiber Optik*:
- **Backbone jaringan**: menghubungkan server utama dan switch jaringan antar gedung.
- **FTTH (Fiber To The Home)**: menyediakan akses internet langsung ke rumah pelanggan.
- **CCTV & Sistem Keamanan**: transmisi gambar resolusi tinggi tanpa delay.
- **Industri medis**: digunakan dalam alat seperti endoskopi.
- **Komunikasi militer**: tahan terhadap penyadapan dan cocok di lingkungan ekstrim.

🧪 *Peralatan Pendukung*:
- **OTDR (Optical Time-Domain Reflectometer)**:
  Digunakan untuk mengukur redaman sinyal, mendeteksi kerusakan dan lokasi sambungan.
  
- **Konektor LC (Lucent Connector)**:
  Konektor berukuran kecil, umum digunakan pada perangkat SFP (Small Form-factor Pluggable).

Kesimpulan:
Pemilihan jenis fiber tergantung pada kebutuhan jarak, kecepatan, dan anggaran. Fiber optik semakin penting dalam perkembangan jaringan modern karena efisiensi dan kapasitasnya.
"""


materi_dict = {
    "pertemuan 1": materi_1,
    "pertemuan 2": materi_2,
    "pertemuan 3": materi_3,
}

# ======= SOAL KUIS =======
soal_kuis = {
    "1": [
        ("Apa perbedaan antara guided media dan unguided media?", "guided media merupakan media transmisi yang menggunakan jalur fisik seperti kabel, unguided media tidak menggunakan kabel fisik. Data dikirim melalui gelombang elektromagnetik"),
        ("Sebutkan apa kelebihan dari kabel coaxial!", "Lebih tahan terhadap interferensi dibanding UTP"),
        ("Mengapa fiber optik cocok untuk transmisi jarak jauh?", "kecepatan tinggi, tahan terhadap gangguan elektromagnetik, cocok untuk jarak jauh."),
        ("Media transmisi mana yang paling tahan terhadap interferensi listrik?", "fiber optik"),
        ("Apa kekurangan kabel UTP dibandingkan fiber optik?", "mudah terkena interferensi elektromagnetik dan memiliki jangkauan yang terbatas"),
    ],
    "2": [
        ("Apa perbedaan core dan cladding dalam lapisan kabel fiber?", "core bagian tengah yang sangat kecil (dalam mikrometer) tempat cahaya merambat. Bahan dasarnya adalah kaca atau plastik khusus dengan indeks bias tinggi,cladding lapisan yang mengelilingi core, memiliki indeks bias lebih rendah untuk memungkinkan *pantulan total internal"),
        ("Jelaskan prinsip pantulan total internal!", "Cahaya yang masuk pada sudut tertentu akan terpantul sempurna di dalam core karena perbedaan indeks bias antara core dan cladding. Inilah yang membuat cahaya tetap berada di dalam serat dan dapat menjangkau jarak sangat jauh tanpa banyak kehilangan sinyal"),
        ("Sebutkan 2 sumber cahaya dalam fiber optik!", "led dan laser"),
        ("Apa yang menyebabkan bending loss?", "Kerugian sinyal yang terjadi jika fiber ditekuk terlalu tajam sehingga cahaya bocor keluar dari core"),
        ("Sebutkan 3 keunggulan fiber optik dibanding kabel tembaga.", "Bandwidth sangat tinggi, Tidak terpengaruh interferensi elektromagnetik, Lebih ringan dan fleksibel dibanding kabel tembaga"),
    ],
    "3": [
        ("Apa beda utama single-mode dan multi-mode?", "single-mode memiliki core sangat kecil (sekitar 8–10 µm), Hanya mengalirkan satu mode cahaya, Digunakan untuk transmisi jarak jauh, seperti antar kota atau backbone ISP, Menggunakan sumber cahaya laser, multi-mode core lebih besar (50–62,5 µm), Mengalirkan banyak jalur cahaya secara bersamaan, Cocok untuk jarak pendek, seperti jaringan LAN dalam gedung, Sumber cahaya biasanya LED."),
        ("Dalam situasi apa kita menggunakan multi-mode?", " Cocok untuk jaringan jarak pendek, seperti jaringan LAN dalam gedung"),
        ("Sebutkan 3 aplikasi umum dari fiber optik!", "backbone jaringan, ftth, cctv, Industri medis, Komunikasi militer"),
        ("Alat apa yang digunakan untuk mengukur redaman fiber?", "otdr"),
        ("Apa nama konektor kecil yang umum di SFP(Small Form-factor Pluggable)?", "lc"),
    ]
}

# ======= START =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "materi_selesai" not in context.user_data:
        await update.message.reply_text(
            "📘 Selamat datang di *Bot Pembelajaran Fiber Optik*!\n\n"
            "Gunakan kata kunci berikut untuk mengakses materi:\n"
            "- Ketik *pertemuan 1* - Media Transmisi\n"
            "- Ketik *pertemuan 2* - Struktur & Prinsip\n"
            "- Ketik *pertemuan 3* - Jenis Fiber & Aplikasi\n\n",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("Halo! Siapa nama lengkapmu?")
        return NAMA

# ======= SIMPAN NAMA SISWA =======
async def simpan_nama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nama = update.message.text
    telegram_id = update.message.from_user.id
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO siswa (telegram_id, nama) VALUES (?, ?)", (telegram_id, nama))
    conn.commit()
    conn.close()

    await update.message.reply_text(
        f"Terima kasih, {nama}!\n\n"
        "💡 Pilih kuis yang ingin kamu kerjakan:\n"
        "- Ketik *kuis pertemuan 1*\n"
        "- Ketik *kuis pertemuan 2*\n"
        "- Ketik *kuis pertemuan 3*",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

# ======= MATERI =======
async def kirim_materi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    materi = materi_dict.get(text)
    if materi:
        await update.message.reply_text(materi, parse_mode="Markdown")
        await update.message.reply_text("✅ Setelah mempelajari materi, ketik /start untuk mulai kuis.")
        context.user_data["materi_selesai"] = True
    else:
        await update.message.reply_text("Materi tidak ditemukan. Ketik: pertemuan 1, pertemuan 2, atau pertemuan 3.")

# ======= KUIS =======
async def mulai_kuis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pertemuan = update.message.text.strip().split()[-1]
    if pertemuan not in soal_kuis:
        await update.message.reply_text("❌ Pertemuan tidak valid. Ketik: kuis pertemuan 1, 2, atau 3.")
        return ConversationHandler.END

    context.user_data["soal_index"] = 0
    context.user_data["skor"] = 0
    context.user_data["soal_list"] = soal_kuis[pertemuan]
    context.user_data["pertemuan"] = pertemuan

    await update.message.reply_text(f"📝 Kuis Pertemuan {pertemuan} dimulai!")
    await update.message.reply_text(soal_kuis[pertemuan][0][0])
    return int(pertemuan)

def bersihkan(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def cek_kemiripan(jawaban_user, jawaban_benar, ambang=0.7):
    return SequenceMatcher(None, bersihkan(jawaban_user), bersihkan(jawaban_benar)).ratio() >= ambang

async def proses_jawaban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    soal_list = context.user_data["soal_list"]
    pertemuan = context.user_data["pertemuan"]
    index = context.user_data["soal_index"]
    pertanyaan, kunci = soal_list[index]
    jawaban = update.message.text

    benar = int(cek_kemiripan(jawaban, kunci))

    telegram_id = update.message.from_user.id
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("INSERT INTO jawaban (telegram_id, pertemuan, soal, jawaban, benar) VALUES (?, ?, ?, ?, ?)",
              (telegram_id, pertemuan, pertanyaan, jawaban, benar))
    conn.commit()
    conn.close()

    if benar:
        await update.message.reply_text("✅ Benar!")
        context.user_data["skor"] += 1
    else:
        await update.message.reply_text(f"❌ Salah. Jawaban benar: {kunci}")

    index += 1
    if index < len(soal_list):
        context.user_data["soal_index"] = index
        await update.message.reply_text(soal_list[index][0])
        return int(pertemuan)
    else:
        skor = context.user_data["skor"]
        await update.message.reply_text(f"✅ Kuis selesai! Skor kamu: {skor}/{len(soal_list)}")
        context.user_data.pop("materi_selesai", None)
        return ConversationHandler.END
    
async def reset_jawaban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("DELETE FROM jawaban WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()
    await update.message.reply_text("✅ Semua jawaban kamu berhasil dihapus!")

# EXPORT JAWABAN KE EXCEL
async def export_jawaban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("siswa.db")
    df = pd.read_sql_query("""
        SELECT s.nama, j.pertemuan, j.soal, j.jawaban, j.benar, j.waktu 
        FROM jawaban j 
        JOIN siswa s ON s.telegram_id = j.telegram_id
        ORDER BY j.waktu ASC
    """, conn)
    conn.close()

    if df.empty:
        await update.message.reply_text("📭 Belum ada data jawaban yang bisa diexport.")
        return

    filename = "jawaban.xlsx"
    df.to_excel(filename, index=False)

    await update.message.reply_document(document=open(filename, 'rb'))
    os.remove(filename)


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Silakan ketik /start untuk mulai atau ketik pertemuan 1/2/3.")

# ======= MAIN =======
def main():
    init_db()
    app = ApplicationBuilder().token(API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex(r"^kuis pertemuan\s+[1-3]$"), mulai_kuis),
        ],
        states={
            NAMA: [MessageHandler(filters.TEXT & ~filters.COMMAND, simpan_nama)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, proses_jawaban)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, proses_jawaban)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, proses_jawaban)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, fallback)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("reset", reset_jawaban))
    app.add_handler(CommandHandler("export", export_jawaban))
    app.add_handler(MessageHandler(filters.Regex(r"^pertemuan\s+[1-3]$"), kirim_materi))

    print("✅ Bot siap dijalankan...")
    app.run_polling()

if __name__ == "__main__":
    main()
