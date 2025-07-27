from telegram import Update
from telegram.ext import ContextTypes



# Materi Pertemuan 1
async def materi_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pembuka
    await update.message.reply_text(
        "📘 *Pertemuan 1: Media Transmisi Jaringan*\n\n"
        "Media transmisi adalah jalur atau sarana yang digunakan untuk mengirimkan sinyal data dari satu perangkat ke perangkat lainnya. "
        "Media ini sangat penting dalam sistem jaringan karena menentukan kecepatan, kualitas, dan keandalan komunikasi data.\n\n"
        "Secara umum, media transmisi dibagi menjadi dua jenis utama:\n"
        "🔌 *A. Guided Media (Media Berkabel)*\n"
        "Guided Media atau media transmisi terpandu adalah jenis media transmisi jaringan yang menggunakan jalur fisik (berwujud) seperti kabel untuk menghantarkan sinyal data dari satu perangkat ke perangkat lainnya. Dalam media ini, gelombang elektromagnetik dipandu atau diarahkan sepanjang jalur fisik tertentu, seperti kabel tembaga atau serat optik.Karena menggunakan media fisik, guided media memiliki arah dan batasan yang jelas dalam penyebaran sinyal, sehingga lebih stabil, lebih terlindungi dari gangguan, dan umumnya memiliki kecepatan serta keandalan yang lebih baik dibanding media nirkabel (unguided media)\n\n"
        "📡 *B. Unguided Media (Media Nirkabel)*\n"
        "Unguided Media atau media transmisi tak terpandu adalah jenis media transmisi jaringan yang tidak menggunakan jalur fisik (kabel) untuk menghantarkan data. Sebagai gantinya, data dikirim melalui udara menggunakan gelombang elektromagnetik seperti gelombang radio, gelombang mikro (microwave), atau sinyal inframerah. Media ini disebut “tak terpandu” karena sinyal tidak dibatasi oleh lintasan fisik, melainkan menyebar bebas di ruang udara, memungkinkan komunikasi tanpa kabel antar perangkat dalam jangkauan tertentu",
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
    await update.message.reply_text("🤖 Tanya lebih lengkap tentang materi pertemuan?\nKetik /tanya untuk memilih materi dan bertanya.")

def get_materi_1_text():
    return (
        "📘 *Pertemuan 1: Media Transmisi Jaringan*\n\n"
        "Media transmisi adalah jalur atau sarana yang digunakan untuk mengirimkan sinyal data dari satu perangkat ke perangkat lainnya. "
        "Media ini sangat penting dalam sistem jaringan karena menentukan kecepatan, kualitas, dan keandalan komunikasi data.\n\n"
        "Secara umum, media transmisi dibagi menjadi dua jenis utama:\n"
        "🔌 *A. Guided Media (Media Berkabel)*\n"
        "1. UTP (Unshielded Twisted Pair): kabel tembaga terpilin, murah dan fleksibel.\n"
        "2. Kabel Coaxial: tahan gangguan, cocok untuk TV kabel.\n"
        "3. Fiber Optik: pakai cahaya, bandwidth sangat tinggi.\n\n"
        "📡 *B. Unguided Media (Media Nirkabel)*\n"
        "1. Wi-Fi: pakai gelombang radio 2.4 GHz / 5 GHz.\n"
        "2. Bluetooth: komunikasi jarak pendek.\n\n"
        "📌 *Kesimpulan:*\n"
        "Guided media stabil, cocok untuk infrastruktur tetap. Unguided media fleksibel, cocok untuk mobilitas.\n"
    )

   