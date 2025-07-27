from telegram import Update
from telegram.ext import ContextTypes
from config.combined import send_combined_image


# Materi pertemuan 3
async def materi_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pembuka
    await update.message.reply_text(
        "📘 *Pertemuan 3: Jenis Fiber Optik dan Aplikasinya*\n\n"
        "Fiber optik memiliki dua jenis utama berdasarkan *mode transmisi cahaya* yang melewati inti seratnya, yaitu *Single-mode* dan *Multi-mode*. "
        "Perbedaan antara keduanya terletak pada ukuran core, jumlah jalur cahaya yang dapat ditransmisikan, serta jarak dan kecepatan transmisinya.",
        parse_mode="Markdown"
    )

    # Single-mode dan Multi-mode Fiber
    await send_combined_image(
        update,
        url1="https://www.mjadom.com/data/upload/ueditor/20230625/6497c57a9a764.png",
        url2="https://images.ctfassets.net/aoyx73g9h2pg/2akZ34C0SwKh3lRZg3u0M5/bbdbf30bbe3d7f6939a78d50df925a28/Single-Mode-vs-Multimode-Fiber-Diagram.jpg",
        caption=(
            "📷 *Singgle-mode & Multi-mode*\n\n"
            "1.*Single-mode Fiber (SMF)*\n\n"
            "⚙️ Core sangat kecil (sekitar 8–10 µm)\n"
            "🔦 Hanya mentransmisikan satu jalur cahaya\n"
            "🚀 Cocok untuk transmisi jarak jauh (hingga ratusan km)\n"
            "💡 Menggunakan sumber cahaya *laser*\n"
            "📡 Digunakan untuk backbone antar kota, jaringan metropolitan (MAN), dan ISP\n\n"
            "🧠 *Kelebihan*:\n"
            "- Redaman dan distorsi rendah\n"
            "- Jangkauan sangat jauh\n"
            "- Ideal untuk kecepatan tinggi (10 Gbps+)\n\n\n"

            "2.*Multi-mode Fiber (MMF)*\n\n"
            "⚙️ Core lebih besar (50–62,5 µm)\n"
            "🔦 Mengalirkan banyak jalur cahaya secara bersamaan\n"
            "📏 Cocok untuk jarak pendek (ratusan meter)\n"
            "💡 Menggunakan sumber cahaya *LED*\n"
            "🏢 Umum untuk jaringan lokal (LAN) dan gedung\n\n"
            "🧠 *Kelebihan*:\n"
            "- Instalasi lebih mudah\n"
            "- Biaya perangkat lebih murah\n"
            "- Cocok untuk penggunaan dalam gedung"
        ),
    )

    # Perbandingan
    await update.message.reply_text(
        "📊 *Perbandingan Singkat SMF vs MMF:*\n\n"
        "```\n"
        "Fitur          | Single-mode     | Multi-mode      \n"
        "---------------|-----------------|-----------------\n"
        "Core           | 8–10 µm         | 50–62,5 µm      \n"
        "Sumber Cahaya  | Laser           | LED             \n"
        "Jarak          | Jauh (jarak km) | Pendek (jarak m)\n"
        "Harga          | Lebih mahal     | Lebih murah     \n"
        "Aplikasi Umum  | Backbone, ISP   | LAN, gedung     \n"
        "```",
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        "📌 *Aplikasi Umum Fiber Optik*:\n\n"
        "🏙️ *Backbone Jaringan*: Menghubungkan server & switch antar gedung.\n"
        "🏠 *FTTH (Fiber To The Home)*: Internet langsung ke rumah pelanggan.\n"
        "🎥 *CCTV & Sistem Keamanan*: Video HD tanpa delay & aman.\n"
        "🏥 *Industri Medis*: Digunakan pada alat seperti endoskop.\n"
        "🪖 *Komunikasi Militer*: Aman dari penyadapan & tahan lingkungan ekstrem.\n\n",
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        "🧪 *Peralatan Pendukung Fiber Optik*:\n\n"
        "🔍 *OTDR*: Untuk mendeteksi redaman sinyal & lokasi kerusakan fiber.\n"
        "🔌 *Konektor LC*: Konektor kecil yang umum digunakan pada perangkat SFP.\n"
        "🧰 *Lainnya*:\n"
        "- *Fusion splicer*: Menyambung serat optik secara permanen.\n"
        "- *Fiber cleaver*: Memotong ujung fiber dengan presisi tinggi.\n"
        "- *Patch panel fiber*: Panel pengatur distribusi koneksi fiber.",
        parse_mode="Markdown"
    )

    # Penutup
    await update.message.reply_text(
        "📚 *Kesimpulan*:\n\n"
        "Pemilihan antara *Single-mode* dan *Multi-mode* harus disesuaikan dengan kebutuhan jarak, kecepatan, dan biaya. "
        "Fiber optik telah menjadi tulang punggung jaringan modern karena kecepatan, kapasitas besar, dan tahan gangguan. "
        "Teknologi ini tidak hanya digunakan dalam jaringan internet, tetapi juga di dunia medis, militer, dan keamanan.",
        parse_mode="Markdown"
    )
    context.user_data["materi_selesai"] = True
    await update.message.reply_text("✅ Setelah mempelajari materi, ketik /start untuk mulai kuis.")
    await update.message.reply_text("🤖 Tanya lebih lengkap tentang materi pertemuan?\nKetik /tanya untuk memilih materi dan bertanya.")

def get_materi_3_text():
    return (
        "📘 *Pertemuan 3: Jenis Fiber Optik dan Aplikasinya*\n\n"
        "Fiber optik memiliki dua jenis utama berdasarkan *mode transmisi cahaya* yang melewati inti seratnya, yaitu *Single-mode* dan *Multi-mode*. "
        "Perbedaan antara keduanya terletak pada ukuran core, jumlah jalur cahaya yang dapat ditransmisikan, serta jarak dan kecepatan transmisinya.\n\n"

        "📷 *Singgle-mode & Multi-mode*\n\n"
        "1.*Single-mode Fiber (SMF)*\n\n"
        "⚙️ Core sangat kecil (sekitar 8–10 µm)\n"
        "🔦 Hanya mentransmisikan satu jalur cahaya\n"
        "🚀 Cocok untuk transmisi jarak jauh (hingga ratusan km)\n"
        "💡 Menggunakan sumber cahaya *laser*\n"
        "📡 Digunakan untuk backbone antar kota, jaringan metropolitan (MAN), dan ISP\n\n"
        "🧠 *Kelebihan*:\n"
        "- Redaman dan distorsi rendah\n"
        "- Jangkauan sangat jauh\n"
        "- Ideal untuk kecepatan tinggi (10 Gbps+)\n\n\n"

        "2.*Multi-mode Fiber (MMF)*\n\n"
        "⚙️ Core lebih besar (50–62,5 µm)\n"
        "🔦 Mengalirkan banyak jalur cahaya secara bersamaan\n"
        "📏 Cocok untuk jarak pendek (ratusan meter)\n"
        "💡 Menggunakan sumber cahaya *LED*\n"
        "🏢 Umum untuk jaringan lokal (LAN) dan gedung\n\n"
        "🧠 *Kelebihan*:\n"
        "- Instalasi lebih mudah\n"
        "- Biaya perangkat lebih murah\n"
        "- Cocok untuk penggunaan dalam gedung\n\n"

        "📊 *Perbandingan Singkat SMF vs MMF:*\n\n"
        "```\n"
        "Fitur          | Single-mode     | Multi-mode      \n"
        "---------------|-----------------|-----------------\n"
        "Core           | 8–10 µm         | 50–62,5 µm      \n"
        "Sumber Cahaya  | Laser           | LED             \n"
        "Jarak          | Jauh (jarak km) | Pendek (jarak m)\n"
        "Harga          | Lebih mahal     | Lebih murah     \n"
        "Aplikasi Umum  | Backbone, ISP   | LAN, gedung     \n"
        "```\n\n"

        "📌 *Aplikasi Umum Fiber Optik*:\n\n"
        "🏙️ *Backbone Jaringan*: Menghubungkan server & switch antar gedung.\n"
        "🏠 *FTTH (Fiber To The Home)*: Internet langsung ke rumah pelanggan.\n"
        "🎥 *CCTV & Sistem Keamanan*: Video HD tanpa delay & aman.\n"
        "🏥 *Industri Medis*: Digunakan pada alat seperti endoskop.\n"
        "🪖 *Komunikasi Militer*: Aman dari penyadapan & tahan lingkungan ekstrem.\n\n"

        "🧪 *Peralatan Pendukung Fiber Optik*:\n\n"
        "🔍 *OTDR*: Untuk mendeteksi redaman sinyal & lokasi kerusakan fiber.\n"
        "🔌 *Konektor LC*: Konektor kecil yang umum digunakan pada perangkat SFP.\n"
        "🧰 *Lainnya*:\n"
        "- *Fusion splicer*: Menyambung serat optik secara permanen.\n"
        "- *Fiber cleaver*: Memotong ujung fiber dengan presisi tinggi.\n"
        "- *Patch panel fiber*: Panel pengatur distribusi koneksi fiber.\n\n"

        "📚 *Kesimpulan*:\n\n"
        "Pemilihan antara *Single-mode* dan *Multi-mode* harus disesuaikan dengan kebutuhan jarak, kecepatan, dan biaya. "
        "Fiber optik telah menjadi tulang punggung jaringan modern karena kecepatan, kapasitas besar, dan tahan gangguan. "
        "Teknologi ini tidak hanya digunakan dalam jaringan internet, tetapi juga di dunia medis, militer, dan keamanan.\n\n"
    )
