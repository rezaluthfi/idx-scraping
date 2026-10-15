# IDX Financial Report Scraper (Anti-Cloudflare)

Skrip Python otomatis untuk mengunduh laporan keuangan dan laporan tahunan emiten dari Bursa Efek Indonesia (IDX / BEI).

Skrip ini dirancang khusus untuk mengatasi masalah **HTTP 403 Forbidden** yang disebabkan oleh proteksi Cloudflare WAF / Turnstile pada portal resmi IDX (`idx.co.id`) menggunakan sesi browser otomatis (`undetected-chromedriver`).

---

## Fitur Utama

- **Bypass Proteksi Cloudflare**: Menangani tantangan Cloudflare Turnstile/Bot Management secara otomatis.
- **Unduh Otomatis Dokumen Lengkap**: Mengunduh berkas laporan keuangan PDF, Excel (`.xlsx`), Laporan Tahunan (*Annual Report*), dan XBRL (`.zip`).
- **Penyimpanan Terstruktur**: Berkas otomatis dikelompokkan ke dalam folder rapi berdasarkan `[KODE_EMITEN]_[TAHUN]_[PERIODE]`.
- **Skip File Duplikat**: Otomatis melewati berkas yang sudah pernah diunduh sebelumnya agar hemat bandwidth dan waktu.

---

## Prasyarat (Requirements)

Sebelum menjalankan skrip, pastikan di komputer sudah terpasang:
1. **Python 3.8+**
2. **Google Chrome** (versi standar/terbaru)

---

## Cara Instalasi

1. **Clone repository ini** (atau unduh zip-nya):
   ```bash
   git clone https://github.com/rezaluthfi/idx-scraping.git
   cd idx-scraping
   ```

2. **(Opsional) Buat virtual environment**:
   ```bash
   python -m venv venv
   # Di Windows (CMD/PowerShell):
   .\venv\Scripts\activate
   # Di Linux/macOS:
   source venv/bin/activate
   ```

3. **Install library yang dibutuhkan**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Cara Menggunakan

1. Buka file `scrap_idx.py` menggunakan teks editor (VS Code, Notepad, dll.).
2. Pada bagian paling bawah skrip (`if __name__ == "__main__":`), sesuaikan parameter yang ingin diunduh:
   ```python
   # Contoh konfigurasi:
   kode_saham = ["BBCA", "TLKM", "ASII"]  # Masukkan kode saham yang diinginkan
   tahun = 2023                           # Tahun laporan keuangan
   periode = "Audit"                      # Pilihan periode: 'Audit', 'TW1', 'TW2', 'TW3'
   
   download_idx_financial_report(kode_saham, tahun, periode)
   ```
3. Jalankan skrip melalui terminal:
   ```bash
   python scrap_idx.py
   ```
4. Jendela Chrome akan terbuka otomatis beberapa detik untuk menyelesaikan verifikasi Cloudflare, kemudian proses download akan berjalan di terminal.

---

## Opsi Periode Laporan

Nilai parameter `periode` yang dapat digunakan:
- `"Audit"` atau `"Tahunan"` : Laporan Keuangan Tahunan (Full Year / Audited)
- `"TW1"` atau `"Quarter 1"` : Laporan Keuangan Kuartal 1
- `"TW2"` atau `"Quarter 2"` : Laporan Keuangan Kuartal 2 (Semester 1)
- `"TW3"` atau `"Quarter 3"` : Laporan Keuangan Kuartal 3

---

## Lokasi Hasil Unduhan

Semua berkas yang berhasil diunduh akan otomatis tersimpan di folder `downloads/` dengan struktur:
```text
downloads/
  ├── BBCA_2023_audit/
  │     ├── FinancialStatement-2023-Tahunan-BBCA.pdf
  │     ├── FinancialStatement-2023-Tahunan-BBCA.xlsx
  │     ├── AnnualReport2023-BBCA.pdf
  │     └── instance.zip
  └── TLKM_2023_audit/
        └── ...
```

---

## Troubleshooting

- **Error Google Chrome tidak ditemukan**: Pastikan Google Chrome sudah terinstall di sistem operasi Anda.
- **Proses berhenti di verifikasi Cloudflare**: Jika koneksi internet sangat lambat atau Cloudflare menampilkan captcha gambar interaktif, cukup selesaikan captcha di jendela Chrome yang terbuka, dan skrip akan otomatis melanjutkan.
