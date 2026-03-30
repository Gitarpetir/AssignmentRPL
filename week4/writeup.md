# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: Muhammad Alfi Gunawan \
SUNet ID: \
Citations: GitHub Copilot Chat Documentation, Claude Code Best Practices \

This assignment took me about 3 hours to do. 

## YOUR RESPONSES

### Automation #1: Project Context & Guardrails (CLAUDE.md Adaptation)
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspirasi desain ini diambil dari panduan "Claude Code best practices" bagian CLAUDE.md guidance files. Tujuannya adalah memberikan konteks repositori, aturan *routing*, dan ekspektasi perkakas (seperti `pytest`, `black`, `ruff`) sebelum agen mulai menulis kode. Karena saya menggunakan GitHub Copilot, saya mengadaptasi konsep ini dengan menaruh aturan tersebut di dalam file `CLAUDE.md` dan memanggilnya sebagai konteks (menggunakan fitur `#file`) di awal obrolan.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** Memastikan AI selalu menghasilkan kode yang sesuai dengan arsitektur FastAPI proyek ini dan mengikuti standar PEP8, tanpa perlu diinstruksikan berulang kali.
> **Inputs:** Perintah pembuatan fitur dari *developer* (misal: "Buat endpoint baru").
> **Outputs:** Kode yang ditempatkan di struktur folder yang benar (`backend/app/routers/` untuk API, `backend/tests/` untuk tes).
> **Steps:** > 1. Membuat file `CLAUDE.md` berisi SOP arsitektur dan aturan *testing*.
> 2. Mengaitkan file tersebut di jendela obrolan AI sebelum memberikan instruksi *coding*.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run:** Buka jendela obrolan Copilot, ketik perintah pembuatan fitur dan sertakan referensi file dengan mengetik `#file:CLAUDE.md`. (Contoh: *"Tolong buatkan skema database untuk user berdasarkan aturan di #file:CLAUDE.md"*).
> **Expected outputs:** AI tidak memberikan kode mentah yang berantakan, melainkan memberikan instruksi langkah demi langkah dan kode yang merujuk pada folder `app/routers` atau `data/seed.sql`.
> **Rollback/safety notes:** Selalu tinjau (*review*) kode yang dihasilkan AI sebelum menyimpannya ke dalam file (*no auto-save*). Pastikan menjalankan `make lint` setelah memodifikasi file.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Saat diminta membuat fitur, AI sering berhalusinasi dengan membuat struktur folder sendiri (misal membuat folder `controllers/` atau `views/` yang tidak sesuai dengan FastAPI) atau menggunakan *framework* pengujian selain `pytest`.
> **After:** AI langsung memahami batasan proyek. AI tahu di mana harus meletakkan kode *router*, skema *database*, dan *file test*, sehingga menghemat waktu *refactoring* manual.

e. How you used the automation to enhance the starter application
> [KOSONGKAN DULU - Kita akan isi setelah kita melakukan praktik di Part II]


### Automation #2: SubAgents (Test-Driven Development Workflow)
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspirasi diambil dari "SubAgents overview", khususnya pola *TestAgent + CodeAgent*. Untuk mengatasi keterbatasan memori konteks (Context Window) pada AI, saya memecah tugas kompleks menjadi dua alur peran (*persona*) terpisah yang mensimulasikan SubAgents di dalam sesi obrolan yang berbeda.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** Menerapkan *Test-Driven Development* (TDD) secara ketat untuk meminimalisir *bug* dan halusinasi logika pada AI.
> **Inputs:** Deskripsi fitur untuk TestAgent. Lalu, hasil tes dari TestAgent menjadi input untuk CodeAgent.
> **Outputs:** 1) *Failing tests* (kode tes yang gagal) dari TestAgent. 2) *Passing code* (implementasi fitur FastAPI) dari CodeAgent.
> **Steps:**
> 1. Buka sesi *chat* 1 (TestAgent): Instruksikan AI untuk hanya bertindak sebagai QA dan menulis kode `pytest`.
> 2. Buka sesi *chat* 2 (CodeAgent): Berikan kode tes dari langkah 1, lalu instruksikan AI untuk menulis implementasi kode backend agar lulus dari tes tersebut.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run:** > - Command 1 (TestAgent): *"Bertindaklah sebagai TestAgent ahli. Baca fitur X. Tuliskan kode pytest-nya saja. Dilarang menulis implementasi fitur."*
> - Command 2 (CodeAgent): *"Bertindaklah sebagai CodeAgent. Ini tes yang dibuat TestAgent: [paste tes]. Tuliskan implementasi FastAPI untuk fitur X agar lulus semua tes ini."*
> **Expected outputs:** File tes baru di `backend/tests/` dan *file router* baru di `backend/app/routers/`. Menjalankan `make test` akan menghasilkan status *passed* (hijau).
> **Rollback/safety notes:** Eksekusi kedua agen harus dilakukan di sesi *chat* (atau *thread*) yang di-*reset* agar konteks TestAgent tidak memengaruhi gaya penulisan CodeAgent. Jika tes gagal, kembalikan *error log* ke CodeAgent untuk koreksi otomatis.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Menyuruh AI menulis tes dan fitur sekaligus sering kali membuat AI "curang"; ia akan menulis tes yang terlalu sederhana agar kodenya pasti lulus, atau kodenya menjadi tumpang tindih dalam satu file besar.
> **After:** Kualitas tes jauh lebih komprehensif karena TestAgent fokus mencari celah (edge cases). Implementasi backend juga lebih rapi karena CodeAgent memiliki tujuan yang sangat jelas: membuat kode yang bisa lulus dari tes yang ada.

e. How you used the automation to enhance the starter application
> [KOSONGKAN DULU - Kita akan isi setelah kita melakukan praktik di Part II]