import sqlite3
from difflib import SequenceMatcher
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    ConversationHandler, filters
)
from materi import materi_1, materi_2, materi_3
from soal import soal_kuis
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


# ======= START =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("materi_selesai"):
        await update.message.reply_text("Halo! Siapa nama lengkapmu?")
        return NAMA
    else:
        await update.message.reply_text(
            "📘 Selamat datang di *Bot Pembelajaran Fiber Optik*!\n\n"
            "Gunakan kata kunci berikut untuk mengakses materi:\n"
            "- Ketik *pertemuan 1* - Media Transmisi\n"
            "- Ketik *pertemuan 2* - Struktur & Prinsip\n"
            "- Ketik *pertemuan 3* - Jenis Fiber & Aplikasi\n\n",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
        

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
        "- Ketik *kuis pertemuan 3*\n"
        "✍ Total Soal = 100 Butir",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


materi_dict = {
    "pertemuan 1": materi_1,
    "pertemuan 2": materi_2,
    "pertemuan 3": materi_3,
}

# ======= MATERI =======
async def kirim_materi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    materi = materi_dict.get(text)
    if materi: 
        await materi(update, context) 
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
    app.add_handler(MessageHandler(filters.Regex(r"(?i)^pertemuan\s*1$|^pertemuan\s*2$|^pertemuan\s*3$"), kirim_materi),)
    
    

    print("✅ Bot siap dijalankan...")
    app.run_polling()

if __name__ == "__main__":
    main()
