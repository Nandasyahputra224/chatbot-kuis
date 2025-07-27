from telegram import Update
from telegram.ext import ContextTypes
import requests
from PIL import Image
from io import BytesIO
import os

async def send_combined_image(update: Update, url1: str, url2: str, caption: str):
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    img1 = Image.open(BytesIO(response1.content)).convert("RGB")
    img2 = Image.open(BytesIO(response2.content)).convert("RGB")

    height = max(img1.height, img2.height)
    img1 = img1.resize((int(img1.width * height / img1.height), height))
    img2 = img2.resize((int(img2.width * height / img2.height), height))

    combined = Image.new("RGB", (img1.width + img2.width, height))
    combined.paste(img1, (0, 0))
    combined.paste(img2, (img1.width, 0))

    output = BytesIO()
    output.name = "combined.jpg"
    combined.save(output, format="JPEG")
    output.seek(0)

    await update.message.reply_photo(photo=output, caption=caption, parse_mode="Markdown")


# Materi Pertemuan 1
async def materi_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pembuka
    await update.message.reply_text(
        "📘 *Pertemuan 1: Media Transmisi Jaringan*\n\n"
        "Media transmisi adalah jalur atau sarana yang digunakan untuk mengirimkan sinyal data dari satu perangkat ke perangkat lainnya. "
        "Media ini sangat penting dalam sistem jaringan karena menentukan kecepatan, kualitas, dan keandalan komunikasi data.\n\n"
        "Secara umum, media transmisi dibagi menjadi dua jenis utama:\n"
        "🔌 *A. Guided Media (Media Berkabel)*\n"
        "📡 *B. Unguided Media (Media Nirkabel)*",
        parse_mode="Markdown"
    )

    # Guided Media - UTP
    await update.message.reply_photo(
        photo="https://nds.id/wp-content/uploads/2022/08/memilih-kabel-UTP.jpg",
        caption=(
            "🔌 *1. UTP (Unshielded Twisted Pair)*\n\n"
            "Merupakan kabel yang terdiri dari sepasang kawat tembaga yang dipilin bersama tanpa pelindung tambahan. "
            "UTP adalah jenis kabel yang paling umum digunakan dalam jaringan komputer skala kecil hingga menengah seperti LAN (Local Area Network).\n\n"
            "📈 *Penggunaan*: Jaringan komputer, telepon, dan CCTV ringan.\n"
            "✨ *Kelebihan*: Biaya rendah, mudah dalam instalasi dan pemeliharaan, fleksibel.\n"
            "❌ *Kekurangan*: Kurang tahan terhadap gangguan elektromagnetik (EMI) dan interferensi karena tidak memiliki shielding atau pelindung logam."
        ),
        parse_mode="Markdown"
    )

    # Guided Media - Coaxial
    await update.message.reply_photo(
        photo="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjBROGbzaIY4Lj9doWjrcadhic-QlMDm-IWxUA6UBY8iSm4zwkw7Scf22H1Jizfamdj3PPHrxKnbTxviKBs3Ky67Rfazb_VEIQmS3wiKFA41c65YMKRTqjYiJkQNS4qTPumSX72jID_pBs/s1600/kabel+coaxial.png",
        caption=(
            "🔌 *2. Kabel Coaxial*\n\n"
            "Kabel coaxial terdiri dari inti tembaga yang dikelilingi oleh lapisan isolator, pelindung logam (braided shield), dan jaket luar. "
            "Struktur ini membuat kabel coaxial lebih tahan terhadap interferensi eksternal dibanding UTP.\n\n"
            "📈 *Penggunaan*: TV kabel, sistem CCTV, koneksi internet broadband awal.\n"
            "✨ *Kelebihan*: Daya tahan tinggi terhadap interferensi dan dapat menjangkau jarak lebih jauh.\n"
            "❌ *Kekurangan*: Lebih mahal dan lebih sulit dipasang daripada UTP."
        ),
        parse_mode="Markdown"
    )

    # Guided Media - Fiber Optik
    await update.message.reply_photo(
        photo="https://www.hostnic.id/blog/wp-content/uploads/2020/07/Kabel-Fiber-Optics.png",
        caption=(
            "🔌 *3. Fiber Optik*\n\n"
            "Media transmisi modern yang menggunakan cahaya untuk mengirimkan data melalui inti serat kaca atau plastik yang sangat halus. "
            "Data dikirim dalam bentuk pulsa cahaya dari sumber cahaya seperti laser atau LED.\n\n"
            "📈 *Penggunaan*: Backbone jaringan, FTTH (Fiber to the Home), komunikasi antar kota dan negara.\n"
            "✨ *Kelebihan*: Bandwidth sangat tinggi, tidak terpengaruh EMI, mendukung jarak sangat jauh.\n"
            "❌ *Kekurangan*: Biaya pemasangan dan peralatan lebih mahal, membutuhkan penanganan teknis khusus."
        ),
        parse_mode="Markdown"
    )

    # Unguided Media - Wi-Fi
    await update.message.reply_photo(
        photo="https://assets.telkomsel.com/public/2025-02/Access-Point.jpg?VersionId=cyXGWI_ttxDo6NU9nrwb6eWhMWRrmLkn",
        caption=(
            "📡 *1. Wi-Fi (Wireless Fidelity)*\n\n"
            "Wi-Fi adalah media transmisi nirkabel yang memanfaatkan gelombang radio untuk menghubungkan perangkat ke jaringan lokal tanpa kabel fisik. "
            "Bekerja pada frekuensi 2.4 GHz dan 5 GHz (hingga 6 GHz di Wi-Fi 6).\n\n"
            "📈 *Penggunaan*: Jaringan rumah, perkantoran, hotspot publik.\n"
            "✨ *Kelebihan*: Mobilitas tinggi, instalasi mudah.\n"
            "❌ *Kekurangan*: Jangkauan terbatas, kualitas sinyal bisa menurun karena hambatan fisik (tembok, lantai)."
        ),
        parse_mode="Markdown"
    )

    # Unguided Media - Bluetooth
    await update.message.reply_photo(
        photo="https://www.mokosmart.com/wp-content/uploads/2024/06/origin-of-Bluetooth.webp",
        caption=(
            "📡 *2. Bluetooth*\n\n"
            "Bluetooth adalah teknologi komunikasi nirkabel jarak dekat (short-range) yang bekerja pada frekuensi 2.4 GHz. "
            "Dirancang untuk menghubungkan perangkat secara langsung tanpa infrastruktur jaringan tambahan.\n\n"
            "📈 *Penggunaan*: Headset, keyboard, mouse, transfer file antar smartphone.\n"
            "✨ *Kelebihan*: Hemat daya, mudah dipasangkan.\n"
            "❌ *Kekurangan*: Jarak sangat terbatas (~10 meter), bandwidth rendah dibanding Wi-Fi."
        ),
        parse_mode="Markdown"
    )

    # Penutup
    await update.message.reply_text(
        "📌 *Kesimpulan:*\n\n"
        "Media transmisi memegang peran penting dalam efektivitas sistem jaringan. "
        "Guided media (seperti UTP, coaxial, dan fiber optik) menawarkan kecepatan dan stabilitas, sangat cocok untuk infrastruktur tetap. "
        "Sementara itu, unguided media (seperti Wi-Fi dan Bluetooth) menawarkan fleksibilitas dan kemudahan mobilitas meskipun rentan terhadap interferensi.\n\n"
        "🔍 Pemilihan media harus mempertimbangkan: kebutuhan bandwidth, jarak transmisi, biaya, serta lingkungan operasional.",
        parse_mode="Markdown"
    )
    context.user_data["materi_selesai"] = True
    await update.message.reply_text("✅ Setelah mempelajari materi, ketik /start untuk mulai kuis.")

    

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
    context.user_data["materi_selesai"] = True
    await update.message.reply_text("✅ Setelah mempelajari materi, ketik /start untuk mulai kuis.")


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


