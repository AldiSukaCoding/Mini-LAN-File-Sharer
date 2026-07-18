# # Mini LAN File Sharer Pro
  Aplikasi desktop berbasis GUI (Antarmuka Grafis) yang ringan dan modern untuk mengirim dan menerima berkas antar-perangkat dalam satu jaringan Wi-Fi lokal tanpa menggunakan kuota internet. Aplikasi ini dibangun menggunakan **Python** dengan antarmuka **CustomTkinter**, serta ditenagai oleh pustaka jaringan bawaan **Socket** dan generator **PyQRCode**.

---

## Fitur Utama
- **Antarmuka Modern:** Menggunakan tema bawaan CustomTkinter yang mendukung otomatisasi Mode Gelap/Terang (System Theme).
- **Deteksi IP Otomatis:** Otomatis mencari dan menampilkan alamat IP lokal komputer Anda saat aplikasi dijalankan sebagai alamat server.
- **QR Code Generator:** Membuat kode QR secara instan di dalam aplikasi agar perangkat lain (seperti smartphone Android/iOS) dapat langsung memindai tautan unduhan.
- **Bebas Hang/Freeze:** Proses penayangan server lokal berjalan di latar belakang menggunakan teknik *Asynchronous Threading*, sehingga GUI tetap responsif saat mentransfer berkas.
- **Port Swapping Pintar:** Otomatis mencari dan mengalihkan port jaringan yang kosong secara mandiri jika port default (`8080`) sedang digunakan oleh aplikasi lain.
- **Konsol Log Aktivitas:** Menampilkan laporan *real-time* mengenai status server, alamat tautan unduhan aktif, hingga indikasi keberhasilan jaringan.

---

## Prasyarat & Dependensi
Sebelum menjalankan aplikasi ini, pastikan komputer Anda sudah terinstal pustaka dan komponen berikut:
### 1. Python
Pastikan Python resmi versi 3.8 atau yang lebih baru sudah terpasang di sistem Anda.
### 2. Pustaka Python (Pip)
Instal pustaka yang dibutuhkan dengan menjalankan perintah berikut di terminal/command prompt:
```bash
pip install customtkinter pyqrcode pypng Pillow
