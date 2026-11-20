# OS-SIMULATOR
### Simulator Penjadwalan CPU & Manajemen Alokasi Memori Dinamis Berbasis CLI

## 1. Deskripsi Proyek

OS-SIMULATOR adalah program simulasi berbasis Command Line Interface (CLI) yang dibuat untuk menerapkan dua materi dalam mata kuliah Sistem Operasi, yaitu **CPU Scheduling** dan **Memory Allocation**.

Melalui program ini, pengguna dapat memasukkan data proses, melihat bagaimana CPU menjalankan proses berdasarkan algoritma penjadwalan tertentu, serta mencoba proses alokasi dan pelepasan memori secara langsung melalui terminal.

Program ini menggunakan dua algoritma penjadwalan CPU, yaitu First Come First Served (FCFS) dan Shortest Job First (SJF) Preemptive atau Shortest Remaining Time First (SRTF). Untuk simulasi manajemen memori, program menggunakan metode Dynamic Partitioning dengan algoritma First-Fit.

Kedua simulasi dibuat secara terpisah agar setiap materi dapat dijalankan dan diamati tanpa saling memengaruhi.

## 2. Fitur Program

### A. CPU Scheduling

Bagian CPU Scheduling digunakan untuk melihat bagaimana beberapa proses mendapatkan giliran penggunaan CPU.

Algoritma yang tersedia:

- **First Come First Served (FCFS)**  
  Proses dijalankan berdasarkan urutan kedatangannya. Proses yang lebih dahulu datang akan mendapatkan giliran lebih awal dan dijalankan sampai selesai.

- **Shortest Job First (SJF) Preemptive / SRTF**  
  CPU menjalankan proses dengan sisa waktu eksekusi paling pendek. Jika ada proses baru yang memiliki sisa waktu lebih pendek daripada proses yang sedang berjalan, CPU dapat beralih menjalankan proses tersebut.

Pengguna perlu memasukkan minimal lima proses dengan data:
- Process ID (PID)
- Arrival Time
- Burst Time

Setelah data dimasukkan, program menjalankan kedua algoritma menggunakan data proses yang sama. Hasilnya ditampilkan dalam bentuk Gantt Chart berbasis teks dan tabel perhitungan yang berisi:

- Waiting Time (WT)
- Turnaround Time (TAT)
- Response Time (RT)
- Rata-rata setiap metrik

Program juga menampilkan perbandingan hasil FCFS dan SJF Preemptive agar pengguna dapat melihat perbedaan kinerja kedua algoritma berdasarkan data yang dimasukkan.

### B. Memory Allocation

Bagian Memory Allocation digunakan untuk menyimulasikan pembagian ruang memori menggunakan metode Dynamic Partitioning dengan algoritma First-Fit.

Pada bagian ini, pengguna dapat:

- Menentukan kapasitas total memori.
- Memasukkan proses yang ingin dialokasikan ke memori.
- Melihat posisi dan ukuran setiap blok memori.
- Melepaskan memori berdasarkan PID.
- Melihat perubahan kondisi memori setelah alokasi atau pelepasan.

Algoritma First-Fit akan mencari blok memori kosong pertama yang ukurannya cukup untuk menampung proses. Jika ukuran blok lebih besar daripada kebutuhan proses, blok tersebut akan dibagi sesuai ukuran yang diperlukan dan sisanya tetap menjadi ruang kosong.

Jika ukuran blok sama dengan kebutuhan proses, seluruh blok akan digunakan.

Ketika proses dilepaskan, ruang memorinya kembali menjadi kosong. Apabila terdapat dua atau lebih blok kosong yang saling bersebelahan, program akan menggabungkannya kembali menjadi satu blok kosong.

Program juga menangani beberapa kondisi, seperti ukuran alokasi yang melebihi kapasitas memori tersedia dan penggunaan PID yang masih aktif. Jika alokasi gagal, kondisi memori tidak berubah.

## 3. Teknologi yang Digunakan

Program ini dibuat menggunakan:

| Teknologi | Penggunaan |
|---|---|
| Python | Bahasa pemrograman utama |
| Python Standard Library | Mendukung struktur data dan proses program |
| Dataclass | Menyimpan data proses, segmen eksekusi, metrik, dan blok memori |
| Unittest | Menjalankan pengujian otomatis |
| Command Line Interface | Antarmuka interaksi melalui terminal |

Program tidak menggunakan library eksternal. Seluruh kebutuhan implementasi dan pengujian menggunakan Python Standard Library.

## 4. Struktur Direktori

Struktur folder proyek disusun berdasarkan tanggung jawab masing-masing modul agar bagian penjadwalan CPU, manajemen memori, visualisasi, dan antarmuka program tidak tercampur.

```
OS-SIMULATOR/
├── main.py
├── MODULE_CONTRACT.md
├── README.md
├── requirements.txt
├── report/
├── src/
│   ├── __init__.py
│   ├── scheduling/
│   │   ├── __init__.py
│   │   ├── fcfs.py
│   │   ├── sjf_preemptive.py
│   │   └── metrics.py
│   ├── memory/
│   │   ├── __init__.py
│   │   └── first_fit.py
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── gantt.py
│   │   └── memory_map.py
│   └── interface/
│       ├── __init__.py
│       ├── menu.py
│       └── input_handler.py
└── tests/
    ├── __init__.py
    ├── test_fcfs.py
    ├── test_sjf_preemptive.py
    ├── test_metrics.py
    └── test_first_fit.py
```

Pembagian modul dalam proyek:

- `main.py` menjadi titik awal untuk menjalankan program.
- `src/scheduling/` berisi implementasi algoritma FCFS, SJF Preemptive, dan perhitungan metrik.
- `src/memory/` berisi implementasi alokasi dan pelepasan memori menggunakan First-Fit.
- `src/visualization/` digunakan untuk menampilkan Gantt Chart dan Memory Map.
- `src/interface/` mengatur menu program dan proses penerimaan serta validasi input pengguna.
- `tests/` berisi pengujian otomatis untuk memeriksa fungsi-fungsi utama program.
- `MODULE_CONTRACT.md` berisi kesepakatan struktur data, tanggung jawab modul, dan antarmuka fungsi yang digunakan selama pengembangan.
- `report/` disediakan untuk menyimpan laporan akhir proyek.

## 5. Persyaratan Sistem

Sebelum menjalankan program, pastikan perangkat sudah memiliki:

- Python versi 3.10 atau lebih baru.
- Terminal atau Command Prompt.
- Git, jika ingin mengambil proyek langsung dari GitHub.

Tidak diperlukan instalasi library tambahan karena program menggunakan Python Standard Library.

## 6. Mengambil Proyek

Proyek dapat diambil melalui repository GitHub berikut:

https://github.com/Olivernoeru/OS-SIMULATOR

Jalankan perintah berikut melalui terminal:

```powershell
git clone https://github.com/Olivernoeru/OS-SIMULATOR.git
```

Masuk ke folder proyek:

```powershell
cd OS-SIMULATOR
```

## 7. Menjalankan Program

Jalankan program menggunakan perintah:

```powershell
python main.py
```

Setelah program dijalankan, menu utama akan ditampilkan:

```text
OS-SIMULATOR
Simulator Penjadwalan CPU & Manajemen Alokasi Memori Dinamis

MENU UTAMA:
1. CPU Scheduling (FCFS & SJF Preemptive)
2. Memory Allocation (First-Fit)
3. Keluar

Pilihan [1-3]:
```

Pilih menu sesuai simulasi yang ingin dijalankan.

### Menjalankan CPU Scheduling

Pilih menu nomor 1. Program akan meminta pengguna memasukkan minimal lima proses beserta PID, Arrival Time, dan Burst Time.

Setelah seluruh data dimasukkan, program akan menampilkan hasil penjadwalan FCFS dan SJF Preemptive, termasuk Gantt Chart, perhitungan metrik setiap proses, dan perbandingan rata-rata kedua algoritma.

### Menjalankan Memory Allocation

Pilih menu nomor 2. Program akan meminta kapasitas total memori sebelum pengguna dapat melakukan alokasi atau pelepasan memori.

Pengguna kemudian dapat memasukkan PID dan ukuran memori yang dibutuhkan oleh suatu proses. Program akan menampilkan kondisi blok memori setelah operasi dilakukan.

Jika ingin mengembalikan ruang memori, pengguna dapat memilih operasi pelepasan berdasarkan PID proses yang masih menempati memori.

## 8. Pengujian Program

Pengujian otomatis dibuat menggunakan modul `unittest` dari Python Standard Library.

Untuk menjalankan seluruh pengujian, gunakan perintah:

```powershell
python -m unittest discover -v
```

Pengujian mencakup empat bagian utama:

| File Pengujian | Bagian yang Diuji |
|---|---|
| `test_fcfs.py` | Algoritma FCFS |
| `test_sjf_preemptive.py` | Algoritma SJF Preemptive |
| `test_metrics.py` | Perhitungan metrik penjadwalan |
| `test_first_fit.py` | Alokasi dan pelepasan memori First-Fit |

Pada pengujian akhir yang dilakukan selama pengembangan, seluruh **62 test berhasil dijalankan tanpa kegagalan maupun error**.

## 9. Batasan Program

OS-SIMULATOR dibuat sebagai program simulasi untuk menerapkan konsep dasar Sistem Operasi. Oleh karena itu, terdapat beberapa batasan:

- Program hanya berjalan melalui Command Line Interface (CLI).
- Simulasi CPU Scheduling hanya menyediakan FCFS dan SJF Preemptive.
- Simulasi Memory Allocation hanya menggunakan Dynamic Partitioning dengan algoritma First-Fit.
- Program tidak melakukan perubahan terhadap proses atau pengelolaan memori pada sistem operasi yang sebenarnya.
- Simulasi CPU Scheduling dan Memory Allocation berjalan secara terpisah.

## 10. Penutup

Melalui OS-SIMULATOR, konsep penjadwalan CPU dan alokasi memori dapat dicoba secara langsung melalui data yang dimasukkan oleh pengguna. Hasil setiap operasi ditampilkan agar alur eksekusi proses dan perubahan kondisi memori lebih mudah diamati.

Proyek ini dikembangkan sebagai penerapan materi Sistem Operasi menggunakan Python dengan pembagian modul yang terstruktur serta pengujian otomatis untuk memeriksa hasil implementasinya.