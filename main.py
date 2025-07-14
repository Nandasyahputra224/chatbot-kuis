import sqlite3
from difflib import SequenceMatcher
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    ConversationHandler, filters
)
from openpyxl import Workbook

API_TOKEN = '7669791642:AAE6vBLfeatGTL8bRq96nzsJE_l5LL9937A'

NAMA, KUIS1, KUIS2, KUIS3 = range(4)

soal_kuis = {
    "1": [
        ("Apa perbedaan antara guided media dan unguided media?", "guided media menggunakan kabel fisik, unguided media menggunakan gelombang udara"),
        ("Sebutkan kelebihan kabel coaxial!", "memiliki pelindung kuat, tahan interferensi"),
        ("Mengapa fiber optik cocok untuk transmisi jarak jauh?", "sinyal tidak mudah terganggu, sangat cepat, bebas interferensi"),
        ("Media transmisi mana yang paling tahan terhadap interferensi listrik?", "fiber optik"),
        ("Apa kekurangan kabel UTP dibandingkan fiber optik?", "mudah terganggu, jarak transmisi pendek"),
    ],
    "2": [
        ("Apa fungsi core dan cladding dalam kabel fiber?", "core menghantarkan cahaya, cladding memantulkan cahaya ke core"),
        ("Jelaskan prinsip pantulan total internal!", "cahaya dipantulkan sepenuhnya di dalam core oleh cladding"),
        ("Sebutkan 2 sumber cahaya dalam fiber optik!", "led dan laser"),
        ("Apa yang menyebabkan bending loss?", "serat ditekuk terlalu tajam"),
        ("Sebutkan 3 keunggulan fiber optik dibanding kabel tembaga.", "bandwidth tinggi, bebas interferensi, ringan dan fleksibel"),
    ],
    "3": [
        ("Apa beda utama single-mode dan multi-mode?", "single-mode hanya satu jalur cahaya, multi-mode banyak jalur cahaya"),
        ("Dalam situasi apa kita menggunakan multi-mode?", "untuk jaringan lan jarak dekat"),
        ("Sebutkan 3 aplikasi umum dari fiber optik!", "backbone jaringan, ftth, cctv"),
        ("Alat apa yang digunakan untuk mengukur redaman fiber?", "otdr"),
        ("Apa nama konektor kecil yang umum di sfp?", "lc"),
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
    soal_list = context.user_data["soal_list"]
    pertemuan = context.user_data["pertemuan"]
    index = context.user_data["soal_index"]
    pertanyaan, kunci = soal_list[index]
    jawaban = update.message.text.lower()

    similarity = SequenceMatcher(None, jawaban, kunci.lower()).ratio()
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

    print("✅ Bot Fiber Optik siap dijalankan...")
    app.run_polling()

if __name__ == "__main__":
    main()
