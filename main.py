import sqlite3
import sys
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    ConversationHandler, filters
)
from openpyxl import Workbook

API_TOKEN = '7723992246:AAHP_z53JAiRZUKFv8Eni7JPST1Ng5bTu34'

NAMA, MENGISI = range(2)

soal_angket = [
    "Chatbot membantu saya memahami materi WAN dengan lebih baik.",
    "Menggunakan chatbot meningkatkan hasil belajar saya.",
    "Saya merasa penggunaan chatbot sangat mudah dan tidak membingungkan.",
    "Menggunakan chatbot tidak memerlukan banyak usaha dari saya.",
    "Teman dan guru saya mendukung saya untuk menggunakan chatbot ini.",
    "Saya merasa tersedia fasilitas yang memadai untuk mengakses chatbot.",
    "Saya menikmati pengalaman belajar dengan menggunakan chatbot.",
    "Belajar dengan chatbot terasa menyenangkan bagi saya.",
    "Saya bermaksud terus menggunakan chatbot dalam pembelajaran mendatang.",
    "Jika tersedia, saya akan merekomendasikan chatbot ini kepada teman lain.",
    "Chatbot memberikan jawaban yang sesuai dengan pertanyaan saya.",
    "Bahasa yang digunakan dalam chatbot mudah dimengerti.",
    "Chatbot mampu menjelaskan materi Jaringan Kabel Fiber Optik dengan jelas.",
    "Saya merasa lebih percaya diri setelah belajar menggunakan chatbot.",
    "Chatbot membantu saya belajar secara mandiri di luar kelas.",
    "Saya merasa lebih fokus belajar ketika menggunakan chatbot.",
    "Saya tidak kesulitan memahami instruksi penggunaan chatbot.",
    "Materi yang tersedia dalam chatbot sesuai dengan kurikulum.",
    "Chatbot membantu saya memahami konsep jaringan WAN yang sulit.",
    "Chatbot memberikan contoh soal dan penjelasan yang memadai.",
    "Chatbot mampu menjawab pertanyaan saya dengan cepat.",
    "Saya merasa puas dengan layanan chatbot pembelajaran ini.",
    "Saya tidak mengalami kendala teknis saat menggunakan chatbot.",
    "Chatbot mampu membuat saya lebih aktif dalam belajar.",
    "Saya lebih cepat memahami materi Jaringan Kabel Fiber Optik dengan bantuan chatbot.",
    "Chatbot dapat diakses kapan saja sesuai kebutuhan saya.",
    "Saya merasa chatbot sebagai solusi alternatif belajar yang efisien.",
    "Tampilan antarmuka chatbot nyaman dan menarik.",
    "Saya merasa penggunaan chatbot lebih efektif daripada belajar mandiri dari buku.",
    "Saya ingin materi lain juga disediakan dalam bentuk chatbot."
]

skor_map = {"st": 4, "s": 3, "ks": 2, "ts": 1}

def init_db():
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS siswa (
            telegram_id INTEGER PRIMARY KEY,
            nama TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS angket (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            soal TEXT,
            jawaban TEXT,
            skor INTEGER
        )
    """)
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM angket WHERE telegram_id = ?", (telegram_id,))
    sudah_isi = c.fetchone()[0]
    conn.close()

    if sudah_isi > 0:
        await update.message.reply_text("❌ Kamu sudah mengisi angket. Ketik /reset jika ingin mengisi ulang.")
        return ConversationHandler.END

    await update.message.reply_text("Halo! Siapa nama lengkapmu?")
    return NAMA

async def simpan_nama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nama = update.message.text
    telegram_id = update.message.from_user.id
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO siswa (telegram_id, nama) VALUES (?, ?)", (telegram_id, nama))
    conn.commit()
    conn.close()

    await update.message.reply_text(
        f"Terima kasih, {nama}.\n\nOpsi jawaban:\n- st: sangat setuju\n- s: setuju\n- ks: kurang setuju\n- ts: tidak setuju\n\nKetik /lanjut untuk mulai angket."
    )
    return ConversationHandler.END

async def lanjut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM angket WHERE telegram_id = ?", (telegram_id,))
    sudah_isi = c.fetchone()[0]
    conn.close()

    if sudah_isi > 0:
        await update.message.reply_text("❌ Kamu sudah mengisi angket. Ketik /reset jika ingin mengisi ulang.")
        return ConversationHandler.END

    context.user_data["index"] = 0
    await update.message.reply_text(f"Pertanyaan 1:\n{soal_angket[0]}\n\nJawab dengan: [ st / s / ks / ts ]")
    return MENGISI

async def isi_jawaban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teks = update.message.text.lower()
    if teks not in skor_map:
        await update.message.reply_text("❌ Jawaban tidak valid. Jawab dengan: [ st / s / ks / ts ]")
        return MENGISI

    index = context.user_data["index"]
    skor = skor_map[teks]
    soal = soal_angket[index]
    telegram_id = update.message.from_user.id

    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("INSERT INTO angket (telegram_id, soal, jawaban, skor) VALUES (?, ?, ?, ?)", (telegram_id, soal, teks, skor))
    conn.commit()
    conn.close()

    index += 1
    context.user_data["index"] = index

    if index < len(soal_angket):
        await update.message.reply_text(f"Pertanyaan {index + 1}:\n{soal_angket[index]}\n\nJawab dengan: [ st / s / ks / ts ]")
        return MENGISI
    else:
        await update.message.reply_text("✅ Terima kasih, angket selesai! Ketik /export untuk export data kamu atau /export_all untuk semua data.")
        return ConversationHandler.END

async def export_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("SELECT nama FROM siswa WHERE telegram_id = ?", (telegram_id,))
    row = c.fetchone()
    nama = row[0] if row else "Tidak diketahui"

    c.execute("SELECT soal, jawaban, skor FROM angket WHERE telegram_id = ?", (telegram_id,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        await update.message.reply_text("❌ Kamu belum mengisi angket atau sudah direset.")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Jawaban Kamu"

    ws.append(["Nama", nama])
    ws.append(["Telegram ID", telegram_id])
    ws.append([])
    ws.append(["No", "Pertanyaan", "Jawaban", "Skor"])

    for idx, (soal, jawaban, skor) in enumerate(rows, 1):
        ws.append([idx, soal, jawaban.upper(), skor])

    file_path = f"{telegram_id}_angket.xlsx"
    wb.save(file_path)

    await update.message.reply_document(document=open(file_path, "rb"))
    await update.message.reply_text("✅ Hasil jawabanmu berhasil diexport ke Excel!")

async def export_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("SELECT DISTINCT telegram_id FROM angket")
    all_ids = c.fetchall()

    wb = Workbook()
    ws = wb.active
    ws.title = "Semua Jawaban"

    ws.append(["No", "Nama", "Telegram ID", "Pertanyaan", "Jawaban", "Skor"])

    row_num = 1
    for idx, (telegram_id,) in enumerate(all_ids, 1):
        c.execute("SELECT nama FROM siswa WHERE telegram_id = ?", (telegram_id,))
        nama_row = c.fetchone()
        nama = nama_row[0] if nama_row else "Tidak diketahui"

        c.execute("SELECT soal, jawaban, skor FROM angket WHERE telegram_id = ?", (telegram_id,))
        rows = c.fetchall()

        for soal_idx, (soal, jawaban, skor) in enumerate(rows, 1):
            ws.append([idx, nama, telegram_id, soal, jawaban.upper(), skor])
            row_num += 1

    conn.close()

    file_path = "semua_jawaban.xlsx"
    wb.save(file_path)

    await update.message.reply_document(document=open(file_path, "rb"))
    await update.message.reply_text("✅ Semua hasil jawaban berhasil diexport ke Excel!")

async def reset_jawaban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("DELETE FROM angket WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()
    await update.message.reply_text("✅ Jawabanmu berhasil direset! Sekarang kamu bisa mengisi ulang.")

async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Perintah tidak dikenali. Gunakan /start, /lanjut, /export, /export_all, atau /reset.")

def main():
    init_db()
    app = ApplicationBuilder().token(API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("lanjut", lanjut)
        ],
        states={
            NAMA: [MessageHandler(filters.TEXT & ~filters.COMMAND, simpan_nama)],
            MENGISI: [MessageHandler(filters.TEXT & ~filters.COMMAND, isi_jawaban)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, fallback)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("export", export_excel))
    app.add_handler(CommandHandler("export_all", export_all))
    app.add_handler(CommandHandler("reset", reset_jawaban))
   

    print("✅ Chatbot siap dijalankan...")
    app.run_polling()

if __name__ == "__main__":
    main()
