import sqlite3
from difflib import SequenceMatcher
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    ConversationHandler, filters
)
from src.materi.__init__ import materi_1, materi_2, materi_3
from src.materi.pertemuan_1 import get_materi_1_text
from src.materi.pertemuan_2 import get_materi_2_text
from src.materi.pertemuan_3 import get_materi_3_text
from src.soal.soal import soal_kuis
from utils.ai_helpers import safe_generate_content
from dotenv import load_dotenv
import re
import pandas as pd
import os
import google.generativeai as genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_TOKEN = os.getenv("API_TOKEN")

NAMA, KUIS1, KUIS2, KUIS3 = range(4)
STATE_PILIH_MATERI, STATE_TANYA_JAWAB = range(100, 102)
MAX_PERTANYAAN = 120

genai.configure(api_key=GEMINI_API_KEY)
client = genai

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
    if context.user_data.get("materi_selesai"):
        context.user_data.clear()
        await update.message.reply_text("Halo! Siapa nama lengkapmu?")
        return NAMA
    else:
        await update.message.reply_text(
            "Selamat datang di *Bot Pembelajaran Fiber Optik*!\n\n"
            "Gunakan kata kunci berikut untuk mengakses materi:\n"
            "- Ketik *pertemuan 1* - Media Transmisi\n"
            "- Ketik *pertemuan 2* - Struktur & Prinsip\n"
            "- Ketik *pertemuan 3* - Jenis Fiber & Aplikasi\n\n",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
        

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
        "Pilih kuis yang ingin kamu kerjakan:\n"
        "- Ketik *kuis pertemuan 1*\n" 
        "- Ketik *kuis pertemuan 2*\n"
        "- Ketik *kuis pertemuan 3*\n",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


materi_dict = {
    "pertemuan 1": get_materi_1_text(),
    "pertemuan 2": get_materi_2_text(),
    "pertemuan 3": get_materi_3_text(),
}

materi_func_dict = {
    "pertemuan 1": materi_1,
    "pertemuan 2": materi_2,
    "pertemuan 3": materi_3,
}


async def kirim_materi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    materi_func = materi_func_dict.get(text)
    if materi_func: 
        await materi_func(update, context) 
        context.user_data.clear()
        context.user_data["materi_selesai"] = True
    else:
        await update.message.reply_text("Materi tidak ditemukan. Ketik: pertemuan 1, pertemuan 2, atau pertemuan 3.")


async def mulai_kuis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pertemuan = update.message.text.strip().split()[-1]
    if pertemuan not in soal_kuis:
        await update.message.reply_text("Pertemuan tidak valid. Ketik: kuis pertemuan 1, 2, atau 3.")
        return ConversationHandler.END

    context.user_data["soal_index"] = 0
    context.user_data["skor"] = 0
    context.user_data["soal_list"] = soal_kuis[pertemuan]
    context.user_data["pertemuan"] = pertemuan

    await update.message.reply_text(f"Kuis Pertemuan {pertemuan} dimulai!")
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
        await update.message.reply_text("Benar!")
        context.user_data["skor"] += 1
    else:
        await update.message.reply_text(f"Salah. Jawaban benar: {kunci}")

    index += 1
    if index < len(soal_list):
        context.user_data["soal_index"] = index
        await update.message.reply_text(soal_list[index][0])
        return int(pertemuan)
    else:
        skor = context.user_data["skor"]
        await update.message.reply_text(f"Kuis selesai! Skor kamu: {skor}/{len(soal_list)}")
        context.user_data.pop("materi_selesai", None)
        return ConversationHandler.END


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Chat berhasil di-restart. Ketik /start untuk memulai ulang.")

    
async def reset_jawaban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    conn = sqlite3.connect("siswa.db")
    c = conn.cursor()
    c.execute("DELETE FROM jawaban WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()
    await update.message.reply_text("Semua jawaban kamu berhasil dihapus!")



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
        await update.message.reply_text("Belum ada data jawaban yang bisa diexport.")
        return

    filename = "jawaban.xlsx"
    df.to_excel(filename, index=False)

    await update.message.reply_document(document=open(filename, 'rb'))
    os.remove(filename)


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Perintah tidak dikenali. Gunakan /start atau ketik kuis pertemuan 1/2/3.")


def jawab_gemini(prompt=""):
    response_text = safe_generate_content(genai, prompt)
    return response_text
   

async def tanya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["pertemuan 1", "pertemuan 2"],["pertemuan 3"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Pilih materi yang ingin kamu tanyakan:\n"
        "- Pertemuan 1 - Media Transmisi\n"
        "- Pertemuan 2 - Struktur & Prinsip\n"
        "- Pertemuan 3 - Jenis Fiber & Aplikasi"
        , reply_markup=reply_markup)
    return STATE_PILIH_MATERI


async def pilih_materi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pilih = update.message.text.lower()
    materi = materi_dict.get(pilih)

    if not materi:
        await update.message.reply_text("Materi tidak ada. Pilih salah satu materi valid yang terdapat pada opsi.")
        return ConversationHandler.END    
    
    context.user_data.clear()
    context.user_data["materi_text"] = materi
    context.user_data["jumlah_tanya"] = 0


    await update.message.reply_text("Silakan ajukan pertanyaan kamu seputar materi ini.")
    return STATE_TANYA_JAWAB


async def jawab_pertanyaan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jumlah_tanya = context.user_data.get("jumlah_tanya", 0)

    if jumlah_tanya >= MAX_PERTANYAAN:
        await update.message.reply_text("Kamu sudah mencapai batas maksimal 120 pertanyaan.")
        return ConversationHandler.END 
    
    pertanyaan = update.message.text
    materi = context.user_data.get("materi_text", "")

    if not materi:
        await update.message.reply_text("Materi belum dipilih. Gunakan /tanya untuk memilih materi.")
        return ConversationHandler.END 

    prompt = f"""Berikut adalah materi pembelajaran:
    {materi}

    Kamu berperan sebagai asisten pengajar. Jika ada pertanyaan yang **tidak relevan dengan materi**, jangan hanya menolaknya. Sebaliknya:
    1. Jelaskan dengan sopan bahwa topik tersebut **tidak berkaitan langsung dengan materi** yang sedang dipelajari.
    2. Berikan sedikit penjelasan tentang topik itu jika memungkinkan (misalnya pengertian atau konteks dasarnya).
    3. Kemudian **arahkan kembali fokus** ke materi pembelajaran yang sesuai.
    Berikan jawaban yang mengalir, edukatif, dan tetap menjaga konteks akademik.
    Jawablah pertanyaan berikut sesuai dengan instruksi ini:
    {pertanyaan}    
        """

    try:
        jawaban = jawab_gemini(prompt)
    except Exception as e:
        await update.message.reply_text(f"Gagal menjawab: {str(e)}")
        return STATE_TANYA_JAWAB 
     
   
    jumlah_tanya += 1
    context.user_data["jumlah_tanya"] = jumlah_tanya
    sisa = MAX_PERTANYAAN - jumlah_tanya

    await update.message.reply_text(jawaban)
    await update.message.reply_text(
        f"▲ Total Pertanyaan : {jumlah_tanya}/120\n"
        f"▼ Sisa pertanyaan  : {sisa}"
    )
    return STATE_TANYA_JAWAB


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sesi tanya jawab selesai. Ketik /tanya untuk mulai lagi.")
    return ConversationHandler.END

# Debug model AI
# def list_model():
#     models = genai.list_models()
#     for m in models:
#         print(m.name, "->", m.supported_generation_methods)

# list_model()

def main():
    init_db()
    app = ApplicationBuilder().token(API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("tanya", tanya),
            CommandHandler("start", start),
            MessageHandler(filters.Regex(r"(?i)^kuis pertemuan\s+[1-3]$"), mulai_kuis),
        ], 
        states={
            STATE_PILIH_MATERI: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, pilih_materi)
            ],
            STATE_TANYA_JAWAB: 
                [MessageHandler(filters.TEXT & ~filters.COMMAND, jawab_pertanyaan)
            ],
            NAMA: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, simpan_nama),  
                CommandHandler("start", start),  
                CommandHandler("restart", restart),
            ],
            1: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, proses_jawaban),  
                CommandHandler("start", start),  
                CommandHandler("restart", restart),
            ],
            2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, proses_jawaban),  
                CommandHandler("start", start),  
                CommandHandler("restart", restart),
            ],
            3: [ 
                
                MessageHandler(filters.TEXT & ~filters.COMMAND, proses_jawaban),  
                CommandHandler("start", start), 
                CommandHandler("restart", restart),
            ],
        },
        # fallbacks=[MessageHandler(filters.COMMAND & ~filters.Regex(r"^/restart$"), fallback)]
        fallbacks=[
            CommandHandler("start", start), 
            CommandHandler("restart", restart),
            CommandHandler("cancel", cancel),
        ],

        name="conv_handler",
        persistent=False,
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("reset_jawaban", reset_jawaban))
    app.add_handler(CommandHandler("export", export_jawaban))
    app.add_handler(CommandHandler("restart", restart))
    app.add_handler(MessageHandler(filters.Regex(r"(?i)^pertemuan\s*1$|^pertemuan\s*2$|^pertemuan\s*3$"), kirim_materi),)
    

    print("✅ Bot siap dijalankan...")
    app.run_polling()

if __name__ == "__main__":
    main()
