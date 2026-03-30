# Panduan Proyek (Starter App Week 4)

Aplikasi ini adalah "developer's command center" yang menggunakan backend FastAPI dan database SQLite.

Ketika diminta untuk menulis atau memodifikasi kode, harap selalu patuhi aturan berikut:

1. **Lokasi File:** Semua rute API (endpoints) harus diletakkan di dalam folder `backend/app/routers/`. Jangan membuat file router di luar folder tersebut.
2. **Pengujian (Testing):** Proyek ini menggunakan `pytest`. Setiap kali menambahkan fitur baru, wajib membuatkan tes otomatisnya di dalam folder `backend/tests/`.
3. **Format Kode:** Kami menggunakan `black` dan `ruff`. Pastikan kode Python selalu rapi dan mengikuti standar PEP8.
4. **Database:** Skema database menggunakan SQLAlchemy. Jangan asal mengubah struktur tabel tanpa melihat file `data/seed.sql`.
