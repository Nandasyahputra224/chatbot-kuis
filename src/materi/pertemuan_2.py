from telegram import Update
from telegram.ext import ContextTypes
from config.combined import send_combined_image


# Materi Pertemuan 2
async def materi_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pembuka
    await update.message.reply_text(
        "📘 *Pertemuan 2: Struktur & Prinsip Kerja Fiber Optik*\n\n"
        "Fiber optik adalah media transmisi modern yang mentransmisikan data dalam bentuk pulsa cahaya. "
        "Media ini menggunakan serat kaca atau plastik yang sangat halus sebagai jalur utama untuk membawa sinyal. "
        "Dengan kemampuannya mengirim data dalam jumlah besar, cepat, dan jarak jauh, fiber optik menjadi tulang punggung komunikasi masa kini seperti internet, telekomunikasi, hingga jaringan data internasional.",
        parse_mode="Markdown"
    )

    # Struktur Fiber Optik
    await update.message.reply_photo(
        photo="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjF0RrlNyODM9bbUngJ6v1mybuPJ54c7ctvMEwFbe4IN1-vWbsnZOSnrVQlGv0sY_B4YYVKDoY9gxqyrPeMWWYyrWWW8XEeG8ew7SI3nD25H00jKz11e1fWjHW3VceSR8nQiAMP7CbJbMLg/s1600/Capture.JPG",
        caption=(
            "🔹 *Struktur Fiber Optik*\n\n"
            "*1. Core (Inti Serat)*\n"
            "📏 Ukuran sangat kecil, antara 8–62,5 mikrometer\n"
            "🔬 Dibuat dari silika murni atau plastik dengan indeks bias tinggi\n"
            "📌 Berfungsi sebagai jalur utama di mana cahaya membawa data\n\n"
            "*2. Cladding (Lapisan Pembungkus)*\n"
            "🧪 Mengelilingi core dan memiliki indeks bias lebih rendah\n"
            "⚙️ Memantulkan cahaya yang merambat di core agar tidak bocor keluar\n"
            "📍 Prinsip: *Total Internal Reflection* (pantulan total dalam)\n\n"
            "*3. Coating / Buffer (Lapisan Pelindung)*\n"
            "🛡️ Lapisan luar berbahan polimer fleksibel\n"
            "🧵 Melindungi serat optik dari goresan, tekanan mekanik, kelembaban, serta kerusakan selama instalasi"
        ),
        parse_mode="Markdown"
    )

    # Prinsip Kerja
    await update.message.reply_photo(
        photo="https://todaystechnologyy.weebly.com/uploads/3/9/1/0/39104677/721900466_orig.jpg?459",
        caption=(
            "✨ *Pantulan Total Internal*\n\n"
            "🔄 Fiber optik bekerja berdasarkan prinsip pantulan total internal (total internal reflection).\n\n"
            "📐 Ketika cahaya masuk ke core dengan sudut tertentu, cahaya tidak akan keluar dari core, "
            "melainkan dipantulkan terus-menerus oleh lapisan cladding yang memiliki indeks bias lebih rendah.\n\n"
            "📌 Hasilnya, cahaya dapat bergerak jauh tanpa keluar jalur meski kabel dibengkokkan sedikit."
        ),
        parse_mode="Markdown"
    )

    # Sumber Cahaya
    await send_combined_image(
        update,
        url1 = "https://img.lazcdn.com/g/p/6ea06ab54b4a0edfea2673c4255ea76f.jpg_720x720q80.jpg",
        url2 = "https://images-cdn.ubuy.co.id/635de983b71d793563228d76-6ft-led-fiber-optic-whip-light-up-rave.jpg",
        caption=(
            "💡 *Sumber Cahaya dalam Fiber Optik*\n\n"
            "Dalam sistem fiber optik, sumber cahaya sangat penting untuk mengubah sinyal listrik menjadi cahaya:\n\n"
            "🔸 *Laser Diode*\n"
            "- Memiliki koherensi tinggi dan arah pancaran tetap\n"
            "- Cocok untuk komunikasi jarak jauh dan kecepatan tinggi\n"
            "- Sering digunakan pada kabel *single-mode*\n\n"
            "🔸 *LED (Light Emitting Diode)*\n"
            "- Lebih murah dan tahan lama\n"
            "- Cocok untuk transmisi jarak pendek\n"
            "- Umumnya digunakan pada kabel *multimode*"
        ),
    )
  

    # Bending Loss
    await update.message.reply_photo(
        photo="https://cdn.fiberopticx.com/wp-content/uploads/2022/10/Micro-bending-loss-in-optical-fiber.jpg",
        caption=(
            "⚠️ *Bending Loss (Kehilangan akibat Tekukan)*\n\n"
            "Kehilangan daya optik bisa terjadi saat kabel fiber dibengkokkan secara ekstrem:\n\n"
            "🔍 *Macro-bending*: Tekukan besar menyebabkan cahaya keluar dari core\n"
            "🔍 *Micro-bending*: Tekanan kecil dalam kabel yang merusak jalur cahaya\n\n"
            "📌 Untuk mencegah ini:\n"
            "- Hindari tikungan tajam saat instalasi\n"
            "- Gunakan pelindung khusus atau teknologi 'bend-insensitive fiber'"
        ),
        parse_mode="Markdown"
    )

    # Penutup
    await update.message.reply_text(
        "🏆 *Keunggulan Fiber Optik*\n\n"
        "✔️ *Bandwidth tinggi*: Dapat mentransfer data dalam jumlah besar dengan cepat\n"
        "✔️ *Tahan terhadap interferensi elektromagnetik*: Tidak terganggu oleh sinyal listrik\n"
        "✔️ *Tingkat keamanan tinggi*: Sulit disadap dan tidak memancarkan sinyal\n"
        "✔️ *Ringan dan fleksibel*: Mudah dipasang dalam berbagai kondisi\n"
        "✔️ *Jangkauan jauh tanpa repeater*: Sinyal bisa menjangkau puluhan kilometer tanpa penguat\n\n"
    )

    await update.message.reply_text(
        "📚 *Kesimpulan*\n\n"
        "Fiber optik adalah tulang punggung jaringan komunikasi masa kini. Dengan memahami strukturnya yang presisi dan prinsip kerjanya yang efisien, "
        "kita bisa lebih memahami mengapa fiber optik menjadi pilihan utama dalam pembangunan infrastruktur jaringan masa depan.",
        parse_mode="Markdown"
    )
    await update.message.reply_text(
        "📝 *Soal Kuis* : \n\n"
        "1. Jelaskan fungsi bagian core dan cladding pada kabel fiber optik, serta bagaimana keduanya bekerja untuk mentransmisikan cahaya!\n"
        "2. Apa yang dimaksud dengan prinsip pantulan total internal dalam fiber optik dan bagaimana syarat terjadinya?\n"
        "3. Sebutkan dan jelaskan dua jenis sumber cahaya yang digunakan dalam transmisi sinyal pada kabel fiber optik!\n"
        "4. Apa yang menyebabkan terjadinya bending loss pada kabel fiber optik dan bagaimana cara mencegahnya?\n"
        "5. Sebutkan tiga keunggulan utama kabel fiber optik dibanding kabel tembaga dalam sistem jaringan!",
        parse_mode="Markdown"
    )
    context.user_data["materi_selesai"] = True
    await update.message.reply_text("✅ Setelah mempelajari materi, ketik /start untuk mulai kuis.")
    await update.message.reply_text("🤖 Tanya lebih lengkap tentang materi pertemuan?\nKetik /tanya untuk memilih materi dan bertanya.")


def get_materi_2_text():
    return (
        "📘 *Pertemuan 2: Struktur & Prinsip Kerja Fiber Optik*\n\n"
        "Fiber optik adalah media transmisi modern yang mentransmisikan data dalam bentuk pulsa cahaya melalui serat kaca atau plastik yang sangat halus. "
        "Dengan kecepatan tinggi dan kemampuan jangkauan jauh, fiber optik menjadi tulang punggung komunikasi modern seperti internet dan telekomunikasi.\n\n"

        "🔹 *Struktur Fiber Optik*\n"
        "1. *Core (Inti)*: Jalur utama cahaya, sangat kecil (8–62,5 µm), terbuat dari silika murni/plastik.\n"
        "2. *Cladding*: Mengelilingi core, memantulkan cahaya agar tetap di jalur, berdasarkan prinsip pantulan total dalam.\n"
        "3. *Coating / Buffer*: Pelindung luar dari tekanan, kelembaban, dan goresan.\n\n"

        "✨ *Prinsip Kerja: Pantulan Total Internal*\n"
        "Cahaya yang masuk ke core dengan sudut tertentu akan dipantulkan terus-menerus oleh cladding sehingga tidak keluar jalur dan tetap mengalir meskipun kabel sedikit bengkok.\n\n"

        "💡 *Sumber Cahaya dalam Fiber Optik*\n"
        "- *Laser Diode*: Presisi tinggi, cocok untuk kabel single-mode dan jarak jauh.\n"
        "- *LED*: Lebih murah, cocok untuk kabel multimode dan jarak pendek.\n\n"

        "⚠️ *Bending Loss (Kehilangan Akibat Tekukan)*\n"
        "- *Macro-bending*: Tekukan besar menyebabkan cahaya bocor.\n"
        "- *Micro-bending*: Tekanan kecil dalam kabel merusak jalur cahaya.\n"
        "Tips: Hindari tekukan tajam dan gunakan teknologi 'bend-insensitive fiber'.\n\n"

        "🏆 *Keunggulan Fiber Optik*\n"
        "✔️ Bandwidth sangat tinggi\n"
        "✔️ Tahan gangguan elektromagnetik\n"
        "✔️ Aman dan sulit disadap\n"
        "✔️ Ringan, fleksibel, dan jangkauan jauh tanpa repeater\n\n"

        "📚 *Kesimpulan*\n"
        "Fiber optik adalah tulang punggung jaringan modern karena efisiensinya dalam mentransmisikan data jarak jauh dengan kecepatan tinggi dan stabilitas tinggi."
    )
