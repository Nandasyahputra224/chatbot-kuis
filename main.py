import sqlite3
from difflib import SequenceMatcher
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    ConversationHandler, filters
)
from openpyxl import Workbook

API_TOKEN = '7801526226:AAHBmBlK0NfabVywPKO2wsSWrdpjqhjnzH4'

NAMA, KUIS1, KUIS2, KUIS3 = range(4)

soal_kuis = {
    "1": [
        ("Apa perbedaan utama antara media transmisi guided (terpandu) dan unguided (tidak terpandu) dalam jaringan komputer? Berikan contoh masing-masing!", "guided media menggunakan kabel fisik contohnya kabel UTP, COAXIAL, dan fiber optik, sedangkan unguided media menggunakan gelombang suara salah satu contohnya yaitu gelombang radio."),
        ("Sebutkan dua kelebihan utama dari penggunaan kabel coaxial dalam jaringan komputer!", "Memiliki perlindungan terhadap interferensi elektromagnetik karena adanya lapisan pelindung, Mampu mentransmisikan data dengan kecepatan sedang dan stabil dalam jarak menengah"),
        ("Mengapa kabel fiber optik dianggap sangat cocok untuk transmisi data jarak jauh dan kecepatan tinggi? Jelaskan alasannya!", "Fiber optik menggunakan cahaya untuk mentransmisikan data, sehingga tidak terpengaruh interferensi elektromagnetik dan memiliki kapasitas bandwidth yang sangat besar"),
        ("Dari berbagai media transmisi, manakah yang paling tahan terhadap gangguan interferensi listrik? Jelaskan alasannya!", "Fiber optik, karena menggunakan sinyal cahaya, bukan listrik, sehingga tidak terpengaruh oleh interferensi elektromagnetik atau gangguan listrik dari luar"),
        ("Apa kelemahan utama kabel UTP jika dibandingkan dengan kabel fiber optik dalam jaringan komputer?", "Kabel UTP lebih rentan terhadap interferensi elektromagnetik, memiliki bandwidth lebih rendah, dan tidak mampu mentransmisikan data sejauh atau secepat fiber optik"),
    ],
    "2": [
        ("Jelaskan fungsi bagian core dan cladding pada kabel fiber optik, serta bagaimana keduanya bekerja untuk mentransmisikan cahaya!", "core adalah bagaian tengah dari kabel fiber optik berfungsi untuk menghantarkan cahaya, cladding adalah lampisan pembungkus core berfungsi untuk memantulkan cahaya kembali ke core"),
        ("Apa yang dimaksud dengan prinsip pantulan total internal dalam fiber optik dan bagaimana syarat terjadinya?", "Pantulan total internal terjadi ketika cahaya merambat dari medium dengan indeks bias lebih tinggi (core) ke medium dengan indeks bias lebih rendah (cladding) dan sudut datang melebihi sudut kritis. Dalam kondisi ini, cahaya dipantulkan sepenuhnya kembali ke dalam core, memungkinkan cahaya tetap berada di dalam fiber dan merambat dalam jarak jauh tanpa banyak kehilangan sinyal"),
        ("Sebutkan dan jelaskan dua jenis sumber cahaya yang digunakan dalam transmisi sinyal pada kabel fiber optik!", "Led digunakan untuk jarak pendek dan kecepatan transmisi rendah. Lebih murah dan efisien, Laser digunakan untuk jarak jauh dan kecepatan tinggi karena menghasilkan cahaya dengan intensitas lebih tinggi dan arah yang lebih terfokus"),
        ("Apa yang menyebabkan terjadinya bending loss pada kabel fiber optik dan bagaimana cara mencegahnya?", "Bending loss terjadi ketika kabel fiber optik ditekuk terlalu tajam sehingga cahaya tidak lagi dapat dipantulkan secara total ke dalam core dan keluar dari jalur. Ini menyebabkan hilangnya sinyal. Untuk mencegahnya, kabel harus dipasang dengan radius kelengkungan minimum sesuai spesifikasi dan tidak ditekuk berlebihan."),
        ("Sebutkan tiga keunggulan utama kabel fiber optik dibanding kabel tembaga dalam sistem jaringan!", "Kecepatan transmisi tinggi, Jangkauan lebih jauh, Tahan terhadap interferensi elektromagnetik"),
    ],
    "3": [
        ("Apa perbedaan utama antara kabel fiber optik single-mode dan multi-mode dari segi ukuran inti dan jarak transmisi?", "Single-mode memiliki inti core yang sangat kecil ~9 mikrometer dan digunakan untuk transmisi jarak jauh hingga puluhan kilometer, Multi-mode memiliki inti yang lebih besar ~50–62,5 mikrometer dan digunakan untuk jarak pendek biasanya di bawah 2 km"),
        ("Dalam kondisi jaringan seperti apa kita lebih cocok menggunakan kabel fiber optik multi-mode dibanding single-mode?", "Multi-mode lebih cocok digunakan di lingkungan LAN, gedung perkantoran, kampus, atau pusat data, di mana jarak antar perangkat relatif dekat biasanya di bawah 550 meter"),
        ("Sebutkan tiga aplikasi umum dari kabel fiber optik dalam kehidupan sehari-hari atau industri!", "backbone jaringan, ftth, endoskopi dan militer"),
        ("Apa nama alat yang digunakan untuk mengukur tingkat redaman (loss) sinyal dalam kabel fiber optik?", "otdr"),
        ("Apa nama konektor kecil yang umum digunakan pada modul SFP (Small Form-factor Pluggable)?", "konektor lc"),
    ]
}

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Siapa nama lengkapmu?")
    return NAMA

async def simpan_nama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nama = update.message.text
    telegram_id = update.message.from_user.id
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO siswa (telegram_id, nama) VALUES (?, ?)", (telegram_id, nama))
    conn.commit()
    conn.close()
    await update.message.reply_text(f"Terima kasih, {nama}. Ketik: kuis 1, kuis 2, atau kuis 3 untuk mulai.")
    return ConversationHandler.END

async def mulai_kuis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pertemuan = update.message.text.strip().split()[-1]
    if pertemuan not in soal_kuis:
        await update.message.reply_text("❌ Pertemuan tidak valid. Ketik: kuis 1, kuis 2, atau kuis 3.")
        return ConversationHandler.END

    context.user_data["soal_index"] = 0
    context.user_data["skor"] = 0
    context.user_data["soal_list"] = soal_kuis[pertemuan]
    context.user_data["pertemuan"] = pertemuan

    await update.message.reply_text(f"📝 Kuis Pertemuan {pertemuan} dimulai!")
    await update.message.reply_text(soal_kuis[pertemuan][0][0])
    return int(pertemuan)

async def proses_jawaban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    def bersihkan(teks):
        import re
        teks = teks.lower()
        teks = re.sub(r"[^\w\s]", "", teks)
        teks = re.sub(r"\s+", " ", teks).strip()
        return teks

    soal_list = context.user_data["soal_list"]
    pertemuan = context.user_data["pertemuan"]
    index = context.user_data["soal_index"]
    pertanyaan, kunci = soal_list[index]
    jawaban = update.message.text

    jawaban_bersih = bersihkan(jawaban)
    kunci_bersih = bersihkan(kunci)

    similarity = SequenceMatcher(None, jawaban_bersih, kunci_bersih).ratio()
    benar = int(similarity > 0.7)

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
        return ConversationHandler.END


async def export_jawaban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("""
        SELECT s.nama, j.pertemuan, j.soal, j.jawaban, j.benar, j.waktu
        FROM jawaban j
        JOIN siswa s ON j.telegram_id = s.telegram_id
        ORDER BY j.waktu
    """)
    rows = c.fetchall()
    conn.close()

    if not rows:
        await update.message.reply_text("Belum ada data jawaban untuk diexport.")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Jawaban"

    headers = ["Nama", "Pertemuan", "Soal", "Jawaban", "Benar (1/0)", "Waktu"]
    ws.append(headers)

    for row in rows:
        ws.append(row)

    file_path = "jawaban_siswa.xlsx"
    wb.save(file_path)

    await update.message.reply_document(document=open(file_path, "rb"), filename="jawaban_siswa.xlsx")
    await update.message.reply_text("✅ Data jawaban berhasil diexport!")


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Silakan ketik /start untuk mulai atau ketik: kuis 1, kuis 2, kuis 3.")

async def reset_jawaban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("DELETE FROM jawaban WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()
    await update.message.reply_text("✅ Jawabanmu berhasil direset! Sekarang kamu bisa mengulang kuis dari awal.")

def main():
    init_db()
    app = ApplicationBuilder().token(API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex(r"^kuis\s+[1-3]$"), mulai_kuis),
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
    app.add_handler(CommandHandler("export", export_jawaban))
    app.add_handler(CommandHandler("reset_jawaban", reset_jawaban))



    print("✅ Bot Fiber Optik siap dijalankan...")
    app.run_polling()

if __name__ == "__main__":
    main()


