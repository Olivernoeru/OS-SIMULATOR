# MODULE CONTRACT

## 1. PROJECT OVERVIEW & SCOPE

### 1.1 Identitas Proyek
| Keterangan | Detail |
|---|---|
| Nama Proyek | OS-SIMULATOR |
| Judul | Simulator Penjadwalan CPU & Manajemen Alokasi Memori Dinamis Berbasis CLI |
| Jenis Proyek | Project Individu UTS Sistem Operasi |
| Bahasa Pemrograman | Python |
| Antarmuka | Command Line Interface (CLI) |
| Algoritma Penjadwalan CPU | FCFS dan Preemptive SJF |
| Algoritma Alokasi Memori | First-Fit |
| Pendekatan Pengembangan | Modular Programming |

### 1.2 Gambaran Proyek
OS-SIMULATOR adalah program berbasis terminal yang dibuat menggunakan Python untuk menyimulasikan dua konsep utama dalam sistem operasi, yaitu penjadwalan CPU dan manajemen alokasi memori dinamis.

Program ini memiliki dua fitur simulasi yang dapat dijalankan secara terpisah:

1. **CPU Scheduling:** Menyimulasikan algoritma FCFS dan Preemptive SJF untuk melihat bagaimana proses mendapatkan giliran penggunaan CPU.
2. **Memory Allocation:** Menyimulasikan pengalokasian dan pelepasan memori menggunakan metode First-Fit.

Program ini dibuat sebagai media pembelajaran untuk memahami cara kerja kedua konsep tersebut. Setiap bagian dikembangkan dalam modul yang berbeda agar tugas setiap file memiliki tanggung jawab yang jelas, kode lebih mudah diperiksa, dan pengujian dapat dilakukan secara terpisah.

### 1.3 Tujuan Proyek
Pembuatan OS-SIMULATOR memiliki beberapa tujuan:

1. Mengimplementasikan algoritma penjadwalan CPU FCFS dan Preemptive SJF.
2. Menampilkan urutan eksekusi proses menggunakan Text-Based Gantt Chart.
3. Menghitung Waiting Time (WT), Turnaround Time (TAT), dan Response Time (RT) untuk setiap proses.
4. Membandingkan hasil penjadwalan dari kedua algoritma berdasarkan metrik yang dihitung.
5. Mengimplementasikan alokasi memori dinamis menggunakan metode First-Fit.
6. Menampilkan perubahan kondisi blok memori setiap kali terjadi alokasi atau pelepasan.
7. Mengamati fragmentasi eksternal yang dapat terjadi selama proses alokasi dan pelepasan memori.
8. Menerapkan pemrograman modular agar setiap komponen memiliki tanggung jawab yang jelas.

### 1.4 Ruang Lingkup Fitur
Program memiliki dua fitur utama dengan ruang lingkup sebagai berikut.

#### A. CPU Scheduling
Fitur ini digunakan untuk menyimulasikan dan membandingkan dua algoritma penjadwalan CPU.

Ketentuan implementasi:

- Pengguna dapat memasukkan minimal lima proses.
- Setiap proses memiliki Process ID, Arrival Time, dan Burst Time.
- Program menjalankan algoritma FCFS.
- Program menjalankan algoritma Preemptive SJF.
- Preemptive SJF dapat menghentikan proses yang sedang berjalan ketika terdapat proses lain dengan sisa Burst Time yang lebih pendek.
- Program menampilkan urutan eksekusi menggunakan Text-Based Gantt Chart.
- Program menghitung Waiting Time (WT), Turnaround Time (TAT), dan Response Time (RT).
- Hasil perhitungan ditampilkan untuk setiap proses beserta nilai rata-ratanya.
- Program menampilkan perbandingan hasil FCFS dan Preemptive SJF.

#### B. Dynamic Memory Allocation
Fitur ini digunakan untuk menyimulasikan pembagian memori secara dinamis berdasarkan kebutuhan setiap proses.

Ketentuan implementasi:

- Pengguna menentukan kapasitas total memori.
- Pengguna memasukkan identitas proses dan ukuran memori yang dibutuhkan.
- Program menggunakan metode First-Fit untuk mencari blok kosong pertama yang mencukupi.
- Blok memori dibagi sesuai ukuran permintaan proses.
- Program menampilkan kondisi setiap blok memori, termasuk status allocated dan free.
- Perubahan kondisi memori ditampilkan setiap kali terjadi alokasi atau pelepasan.
- Jika tidak ditemukan blok kosong yang mencukupi, permintaan alokasi ditolak tanpa mengubah kondisi memori.
- Ketika proses selesai, memori yang digunakan dikembalikan menjadi blok kosong.
- Blok kosong yang bersebelahan digabungkan kembali.
- Program menampilkan kondisi memori setelah setiap operasi.

Kedua fitur ini berjalan secara terpisah. Simulasi CPU Scheduling tidak bergantung pada hasil simulasi Memory Allocation, begitu juga sebaliknya.

### 1.5 Teknologi yang Digunakan
| Komponen | Teknologi |
|---|---|
| Bahasa Pemrograman | Python |
| Antarmuka Program | Command Line Interface (CLI) |
| Struktur Data | Python Dataclass |
| Unit Testing | Python unittest |
| Dependensi | Python Standard Library |

Program mengutamakan penggunaan Python Standard Library untuk menjaga implementasi tetap sederhana dan mengurangi kebutuhan dependensi eksternal. Jika terdapat kebutuhan teknis yang memerlukan library tambahan, dependensi tersebut akan dicantumkan dalam `requirements.txt`.

## 2. SYSTEM ARCHITECTURE
Setelah ruang lingkup dan fitur utama pada OS-SIMULATOR ditentukan, langkah selanjutnya yang saya lakukan adalah menyusun arsitektur program yang akan dibuat. Arsitektur ini menjelaskan bagaimana program dibagi menjadi beberapa modul, bagaimana setiap modul menjalankan tugas dan tanggung jawabnya masing-masing, dan bagaimana seluruh komponen disusun agar dapat bekerja secara terstruktur.

### 2.1 Pendekatan Arsitektur
OS-SIMULATOR menggunakan pendekatan Modular Programming. Pendekatan ini membagi kode program menjadi beberapa modul berdasarkan fungsi dan tanggung jawabnya.

Setiap modul memiliki tugas yang berbeda agar tidak terjadi tumpang tindih dalam proses pengolahan data maupun pelaksanaan fitur. Pembagian ini juga memudahkan proses pengembangan dan pengujian karena setiap modul dapat diperiksa secara terpisah.

Program dibagi menjadi empat kelompok modul utama yaitu Scheduling, Memory, Visualization, dan Interface. Seluruh kelompok modul tersebut dihubungkan melalui program utama (`main.py`).

### 2.2 Struktur Direktori Proyek
Struktur direktori OS-SIMULATOR disusun untuk memisahkan file berdasarkan fungsi dan tanggung jawabnya. Susunan direktori yang digunakan adalah sebagai berikut:

OS-SIMULATOR/
│
├── main.py
├── MODULE_CONTRACT.md
├── README.md
├── requirements.txt
│
├── report/
│
├── src/
│   ├── __init__.py
│   │
│   ├── scheduling/
│   │   ├── __init__.py
│   │   ├── fcfs.py
│   │   ├── sjf_preemptive.py
│   │   └── metrics.py
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   └── first_fit.py
│   │
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── gantt.py
│   │   └── memory_map.py
│   │
│   └── interface/
│       ├── __init__.py
│       ├── menu.py
│       └── input_handler.py
│
└── tests/
    ├── __init__.py
    ├── test_fcfs.py
    ├── test_sjf_preemptive.py
    ├── test_metrics.py
    └── test_first_fit.py

Struktur tersebut terdiri dari beberapa direktori utama:

1. **Root Directory:** Menyimpan program utama serta dokumentasi dan konfigurasi proyek.
2. **src/:** Menyimpan seluruh kode sumber program yang dibagi berdasarkan fungsi masing-masing modul.
3. **tests/:** Menyimpan file pengujian untuk memeriksa hasil kerja setiap komponen.
4. **report/:** Menyimpan laporan akhir dalam format PDF beserta file pendukung yang diperlukan.

### 2.3 Gambaran Komponen Sistem
Setiap folder dan file dalam OS-SIMULATOR memiliki fungsi dan tanggung jawab yang berbeda. Pembagian komponen tersebut adalah sebagai berikut.

#### A. Program Utama
- **main.py:** Menjadi titik awal ketika program dijalankan. File ini menghubungkan program utama dengan menu dan fitur yang tersedia.

#### B. Scheduling Module
Kelompok modul ini menangani seluruh proses penjadwalan CPU.

- **fcfs.py:** Menjalankan algoritma First Come First Served.
- **sjf_preemptive.py:** Menjalankan algoritma Preemptive Shortest Job First.
- **metrics.py:** Menghitung Waiting Time (WT), Turnaround Time (TAT), dan Response Time (RT) beserta nilai rata-ratanya.

#### C. Memory Module
Kelompok modul ini menangani simulasi alokasi dan pelepasan memori.

- **first_fit.py:** Menangani pembagian blok memori serta proses pencarian blok kosong menggunakan metode First-Fit. Modul ini juga menangani alokasi dan pelepasan memori serta penggabungan blok kosong yang bersebelahan.

#### D. Visualization Module
Kelompok modul ini bertanggung jawab menampilkan hasil simulasi dalam bentuk teks di terminal.

- **gantt.py:** Menampilkan urutan eksekusi proses dalam bentuk Text-Based Gantt Chart.
- **memory_map.py:** Menampilkan kondisi blok memori termasuk blok yang sedang digunakan dan blok yang masih kosong.

#### E. Interface Module
Kelompok modul ini menangani interaksi antara pengguna dan program.

- **menu.py:** Menampilkan menu utama dan mengatur pilihan fitur yang dijalankan pengguna.
- **input_handler.py:** Menerima dan memvalidasi masukan pengguna sebelum diteruskan ke proses simulasi.

#### F. Testing Module
Kelompok ini berisi file pengujian untuk memastikan setiap komponen bekerja sesuai dengan ketentuan yang telah ditetapkan.

- **test_fcfs.py:** Menguji algoritma FCFS.
- **test_sjf_preemptive.py:** Menguji algoritma Preemptive SJF.
- **test_metrics.py:** Menguji perhitungan metrik penjadwalan.
- **test_first_fit.py:** Menguji proses alokasi dan pelepasan memori menggunakan First-Fit.

### 2.4 Alur Komunikasi Antar-Modul
Komunikasi antar-modul dilakukan melalui pemanggilan fungsi dan pertukaran data sesuai dengan tanggung jawab masing-masing komponen.

Secara umum alur komunikasi program dibagi menjadi dua bagian.

#### A. Alur CPU Scheduling
1. `main.py` menjalankan menu utama melalui `menu.py`.
2. Pengguna memilih fitur CPU Scheduling.
3. `input_handler.py` menerima dan memvalidasi data proses.
4. Data proses diteruskan ke `fcfs.py` dan `sjf_preemptive.py` untuk menjalankan simulasi masing-masing algoritma.
5. Hasil simulasi diteruskan ke `metrics.py` untuk menghitung metrik penjadwalan.
6. Hasil urutan eksekusi diteruskan ke `gantt.py` untuk ditampilkan dalam bentuk Gantt Chart.
7. Program menampilkan hasil simulasi dan perbandingan kedua algoritma kepada pengguna.

#### B. Alur Memory Allocation
1. `main.py` menjalankan menu utama melalui `menu.py`.
2. Pengguna memilih fitur Memory Allocation.
3. `input_handler.py` menerima dan memvalidasi kapasitas memori serta permintaan alokasi.
4. Data diteruskan ke `first_fit.py` untuk menjalankan proses alokasi atau pelepasan memori.
5. Kondisi blok memori setelah operasi diteruskan ke `memory_map.py`.
6. Program menampilkan kondisi memori kepada pengguna.

Kedua alur tersebut berjalan secara terpisah. Modul CPU Scheduling tidak menggunakan hasil dari Memory Allocation. Begitu juga sebaliknya.

## 3. DATA MODEL SPECIFICATION
Setelah arsitektur program dan pembagian modul ditentukan, langkah selanjutnya adalah menentukan struktur data yang akan digunakan. Struktur data ini menjadi dasar bagi setiap modul dalam menerima, mengolah, dan meneruskan data selama proses simulasi berlangsung.

### 3.1 Pendekatan Struktur Data
OS-SIMULATOR menggunakan Python Dataclass sebagai pendekatan untuk mendefinisikan struktur data utama.

Dataclass digunakan agar setiap data memiliki atribut dan tipe data yang jelas. Pendekatan ini juga memudahkan modul lain dalam mengakses data melalui nama atribut tanpa harus menggunakan indeks atau mengambil nilai berdasarkan nama key seperti pada dictionary.

Setiap struktur data dibuat berdasarkan kebutuhan fitur yang tersedia. Data untuk CPU Scheduling dipisahkan dari data untuk Memory Allocation karena kedua fitur tersebut berjalan secara terpisah.

### 3.2 Struktur Data CPU Scheduling
Fitur CPU Scheduling menggunakan tiga struktur data utama.

#### A. Process
`Process` digunakan untuk menyimpan informasi setiap proses yang akan dijadwalkan oleh CPU.

| Atribut | Tipe Data | Keterangan |
|---|---|---|
| pid | str | Identitas unik setiap proses |
| arrival_time | int | Waktu kedatangan proses |
| burst_time | int | Total waktu yang dibutuhkan proses untuk menyelesaikan eksekusi |

Setiap proses harus memiliki PID yang unik. Arrival Time dan Burst Time tidak boleh bernilai negatif. Burst Time harus lebih besar dari nol.

#### B. ExecutionSegment
`ExecutionSegment` digunakan untuk mencatat setiap bagian eksekusi proses dalam timeline CPU.

| Atribut | Tipe Data | Keterangan |
|---|---|---|
| pid | str | Identitas proses yang menggunakan CPU |
| start_time | int | Waktu dimulainya segmen eksekusi |
| end_time | int | Waktu berakhirnya segmen eksekusi |

Struktur ini digunakan untuk menyimpan urutan eksekusi dari algoritma FCFS dan Preemptive SJF. Jika CPU tidak sedang menjalankan proses maka PID menggunakan nilai `IDLE`.

#### C. ProcessMetrics
`ProcessMetrics` digunakan untuk menyimpan hasil perhitungan metrik penjadwalan setiap proses.

| Atribut | Tipe Data | Keterangan |
|---|---|---|
| pid | str | Identitas proses |
| waiting_time | int | Total waktu proses menunggu untuk mendapatkan CPU |
| turnaround_time | int | Total waktu sejak proses tiba hingga selesai |
| response_time | int | Waktu sejak proses tiba hingga pertama kali mendapatkan CPU |

Struktur ini digunakan untuk menampilkan hasil perhitungan setiap proses serta membantu proses perbandingan antara FCFS dan Preemptive SJF.

### 3.3 Struktur Data Memory Allocation
Fitur Memory Allocation menggunakan dua struktur data utama.

#### A. MemoryRequest
`MemoryRequest` digunakan untuk menyimpan informasi permintaan alokasi memori dari suatu proses.

| Atribut | Tipe Data | Keterangan |
|---|---|---|
| pid | str | Identitas proses yang meminta memori |
| size | int | Jumlah memori yang dibutuhkan |

Setiap permintaan harus memiliki PID yang unik pada alokasi yang sedang berlangsung. Ukuran memori yang diminta harus lebih besar dari nol.

#### B. MemoryBlock
`MemoryBlock` digunakan untuk merepresentasikan setiap blok dalam pembagian memori.

| Atribut | Tipe Data | Keterangan |
|---|---|---|
| start_address | int | Alamat awal blok memori |
| size | int | Kapasitas blok memori |
| process_id | Optional[str] | Identitas proses yang menggunakan blok atau None jika blok masih kosong |

Atribut `process_id` digunakan untuk membedakan blok yang sedang digunakan dengan blok yang masih kosong. Jika nilainya `None` maka blok tersebut berstatus free. Jika memiliki identitas proses maka blok tersebut berstatus allocated.

Setiap blok memiliki alamat awal dan ukuran yang digunakan untuk menentukan posisi serta kapasitasnya dalam memori.

### 3.4 Ketentuan Penggunaan Data
Seluruh struktur data digunakan sesuai dengan kebutuhan modul masing-masing.

Beberapa ketentuan yang harus diperhatikan:

1. Data `Process` digunakan oleh modul CPU Scheduling.
2. Data `ExecutionSegment` digunakan untuk menyimpan timeline hasil penjadwalan.
3. Data `ProcessMetrics` digunakan untuk menyimpan hasil perhitungan metrik.
4. Data `MemoryRequest` digunakan sebagai masukan dalam proses alokasi memori.
5. Data `MemoryBlock` digunakan untuk menyimpan kondisi setiap blok memori.
6. Struktur data harus memiliki atribut dan tipe data yang konsisten ketika diteruskan antar-modul.
7. Data CPU Scheduling tidak digabungkan dengan data Memory Allocation karena kedua fitur memiliki proses simulasi yang berbeda.

## 4. MODULE RESPONSIBILITY
Setelah struktur data yang digunakan ditentukan, langkah selanjutnya adalah menjelaskan tanggung jawab setiap modul secara lebih rinci. Pembagian ini bertujuan agar setiap file memiliki fungsi yang jelas sehingga tidak terjadi tumpang tindih dalam proses pengolahan data.

### 4.1 Program Utama
**File: `main.py`**

Program utama bertanggung jawab menjadi titik awal ketika OS-SIMULATOR dijalankan.

Tanggung jawab:

- Menjalankan program.
- Memanggil menu utama.
- Menghubungkan proses awal program dengan fitur yang tersedia.

File ini tidak menangani perhitungan algoritma maupun proses pengolahan memori.

### 4.2 Interface Module
Kelompok modul ini menangani interaksi antara pengguna dan program.

#### A. menu.py
Tanggung jawab:

- Menampilkan menu utama.
- Menampilkan pilihan CPU Scheduling dan Memory Allocation.
- Menerima pilihan fitur dari pengguna.
- Mengatur perpindahan menu dan proses kembali ke menu utama.
- Menangani pilihan untuk keluar dari program.

#### B. input_handler.py
Tanggung jawab:

- Menerima data proses untuk CPU Scheduling.
- Memvalidasi Process ID, Arrival Time, dan Burst Time.
- Menerima kapasitas total memori.
- Menerima identitas proses dan ukuran memori yang dibutuhkan.
- Memvalidasi setiap masukan sebelum diteruskan ke modul simulasi.

Modul ini hanya menangani penerimaan dan validasi masukan. Perhitungan algoritma tidak dilakukan di dalam file ini.

### 4.3 Scheduling Module
Kelompok modul ini bertanggung jawab menjalankan algoritma penjadwalan CPU dan menghitung hasilnya.

#### A. fcfs.py
Tanggung jawab:

- Menerima daftar proses yang telah divalidasi.
- Menjalankan algoritma First Come First Served.
- Menentukan urutan eksekusi berdasarkan Arrival Time.
- Menghasilkan timeline eksekusi proses.

#### B. sjf_preemptive.py
Tanggung jawab:

- Menerima daftar proses yang telah divalidasi.
- Menjalankan algoritma Preemptive Shortest Job First.
- Memilih proses berdasarkan sisa Burst Time terpendek dari proses yang sudah tiba.
- Melakukan preemption ketika terdapat proses lain dengan sisa Burst Time yang lebih pendek.
- Menghasilkan timeline eksekusi proses.

#### C. metrics.py
Tanggung jawab:

- Menerima data proses dan timeline hasil penjadwalan.
- Menghitung Waiting Time (WT).
- Menghitung Turnaround Time (TAT).
- Menghitung Response Time (RT).
- Menghitung nilai rata-rata dari setiap metrik.
- Menghasilkan data metrik untuk setiap proses.

Perhitungan metrik dilakukan melalui satu modul agar FCFS dan Preemptive SJF menggunakan aturan perhitungan yang sama.

### 4.4 Memory Module
**File: `first_fit.py`**

Modul ini bertanggung jawab menangani seluruh proses simulasi alokasi memori dinamis menggunakan metode First-Fit.

Tanggung jawab:

- Menginisialisasi kapasitas total memori.
- Membentuk blok memori awal.
- Mencari blok kosong pertama yang memiliki kapasitas mencukupi.
- Membagi blok memori sesuai ukuran permintaan.
- Melakukan alokasi memori.
- Melakukan pelepasan memori berdasarkan identitas proses.
- Menggabungkan blok kosong yang bersebelahan.
- Memastikan kondisi memori tetap konsisten setelah setiap operasi.

Jika permintaan alokasi tidak dapat dipenuhi maka modul harus menolak permintaan tanpa mengubah kondisi memori.

### 4.5 Visualization Module
Kelompok modul ini bertanggung jawab menampilkan hasil simulasi dalam bentuk teks di terminal.

#### A. gantt.py
Tanggung jawab:

- Menerima timeline hasil penjadwalan.
- Menampilkan urutan eksekusi proses dalam bentuk Text-Based Gantt Chart.
- Menampilkan waktu mulai dan berakhirnya setiap segmen eksekusi.
- Menampilkan kondisi CPU ketika tidak ada proses yang berjalan.

#### B. memory_map.py
Tanggung jawab:

- Menerima daftar blok memori.
- Menampilkan alamat awal dan ukuran setiap blok.
- Menampilkan status allocated dan free.
- Menampilkan identitas proses pada blok yang sedang digunakan.
- Menampilkan perubahan kondisi memori setelah setiap operasi.

### 4.6 Testing Module
Kelompok modul ini bertanggung jawab melakukan pengujian terhadap komponen utama program.

#### A. test_fcfs.py
Menguji urutan eksekusi dan hasil timeline algoritma FCFS.

#### B. test_sjf_preemptive.py
Menguji pemilihan proses dan mekanisme preemption pada algoritma Preemptive SJF.

#### C. test_metrics.py
Menguji perhitungan Waiting Time, Turnaround Time, Response Time, dan nilai rata-ratanya.

#### D. test_first_fit.py
Menguji proses alokasi, penolakan permintaan, pelepasan memori, dan penggabungan blok kosong.

Setiap file pengujian berfokus pada komponen yang sesuai dengan namanya. Dengan demikian hasil pengujian dapat diperiksa tanpa harus menjalankan seluruh fitur program.

## 5. MODULE INTERFACE CONTRACT
Setelah tanggung jawab setiap modul ditentukan, langkah selanjutnya adalah menetapkan cara setiap modul berkomunikasi satu sama lain. Bagian ini menjelaskan data yang diterima dan hasil yang harus diberikan oleh setiap modul agar proses integrasi dapat berjalan dengan baik.

### 5.1 Ketentuan Komunikasi Antar-Modul
Setiap modul berkomunikasi melalui fungsi atau method yang telah ditentukan.

Beberapa ketentuan yang harus diterapkan:

1. Modul hanya boleh mengakses fungsi atau method yang memang disediakan oleh modul lain.
2. Data yang diteruskan antar-modul harus menggunakan struktur data yang telah ditentukan pada Bagian 3.
3. Modul tidak boleh mengambil alih tanggung jawab modul lain.
4. Modul algoritma tidak menangani input maupun tampilan menu.
5. Modul visualization hanya bertugas menampilkan hasil dan tidak melakukan perhitungan algoritma.
6. Setiap fungsi harus memberikan hasil dengan format yang konsisten agar dapat digunakan oleh modul berikutnya.

### 5.2 Interface Scheduling Module
#### A. fcfs.py

**Fungsi utama:**

`run_fcfs(processes)`

| Parameter | Tipe Data | Keterangan |
|---|---|---|
| processes | List[Process] | Daftar proses yang akan dijadwalkan |

**Hasil:**

`List[ExecutionSegment]`

Fungsi mengembalikan daftar segmen eksekusi yang menunjukkan urutan proses berdasarkan algoritma FCFS.

#### B. sjf_preemptive.py
**Fungsi utama:**

`run_sjf_preemptive(processes)`

| Parameter | Tipe Data | Keterangan |
|---|---|---|
| processes | List[Process] | Daftar proses yang akan dijadwalkan |

**Hasil:**

`List[ExecutionSegment]`

Fungsi mengembalikan daftar segmen eksekusi berdasarkan algoritma Preemptive SJF.

Kedua algoritma harus menghasilkan struktur timeline yang sama agar dapat diproses oleh modul metrik dan visualization.

#### C. metrics.py
**Fungsi utama:**

`calculate_metrics(processes, timeline)`

| Parameter | Tipe Data | Keterangan |
|---|---|---|
| processes | List[Process] | Daftar proses yang dijadwalkan |
| timeline | List[ExecutionSegment] | Hasil timeline dari algoritma penjadwalan |

**Hasil:**

`List[ProcessMetrics]`

Fungsi mengembalikan hasil perhitungan WT, TAT, dan RT untuk setiap proses.

**Fungsi tambahan:**

`calculate_average_metrics(metrics)`

| Parameter | Tipe Data | Keterangan |
|---|---|---|
| metrics | List[ProcessMetrics] | Daftar hasil metrik setiap proses |

**Hasil:**

`Dict[str, float]`

Fungsi mengembalikan nilai rata-rata Waiting Time, Turnaround Time, dan Response Time.

### 5.3 Interface Memory Module
#### first_fit.py

Modul ini menyediakan pengelola memori yang menangani proses alokasi dan pelepasan memori.

**Class utama:**

`FirstFitAllocator`

**Method yang disediakan:**

| Method | Parameter | Hasil | Keterangan |
|---|---|---|---|
| `__init__()` | `total_memory: int` | - | Menginisialisasi kapasitas dan blok memori awal |
| `allocate()` | `request: MemoryRequest` | `bool` | Melakukan alokasi menggunakan First-Fit |
| `release()` | `pid: str` | `bool` | Melepaskan memori berdasarkan PID |
| `get_blocks()` | - | `List[MemoryBlock]` | Mengembalikan kondisi seluruh blok memori |

Ketentuan:

- Kapasitas total memori harus lebih besar dari nol.
- Alokasi hanya dapat dilakukan jika ditemukan blok kosong yang mencukupi.
- Permintaan alokasi yang gagal tidak boleh mengubah kondisi memori.
- Proses yang tidak memiliki alokasi aktif tidak dapat melepaskan memori.
- Blok kosong yang bersebelahan harus digabungkan setelah pelepasan memori.
- Data blok yang diberikan kepada modul lain tidak boleh menyebabkan perubahan kondisi memori secara langsung.

### 5.4 Interface Visualization Module
#### A. gantt.py

**Fungsi utama:**

`display_gantt(timeline)`

| Parameter | Tipe Data | Keterangan |
|---|---|---|
| timeline | List[ExecutionSegment] | Daftar segmen hasil penjadwalan |

**Hasil:**

Menampilkan Text-Based Gantt Chart di terminal.

#### B. memory_map.py
**Fungsi utama:**

`display_memory_map(blocks)`

| Parameter | Tipe Data | Keterangan |
|---|---|---|
| blocks | List[MemoryBlock] | Daftar kondisi blok memori |

**Hasil:**

Menampilkan gambaran kondisi blok memori di terminal.

Kedua fungsi hanya bertanggung jawab menampilkan data. Tidak ada proses perhitungan algoritma maupun perubahan kondisi memori di dalam modul visualization.

### 5.5 Interface Module
#### A. menu.py

Modul ini menyediakan fungsi untuk menampilkan dan mengatur menu program.

Fungsi utama yang disediakan:

- `display_main_menu()` untuk menampilkan pilihan menu utama.
- `run_menu()` untuk menjalankan alur menu dan menghubungkan pilihan pengguna dengan fitur yang tersedia.

#### B. input_handler.py
Modul ini menyediakan fungsi untuk menerima dan memvalidasi masukan pengguna.

Fungsi utama yang disediakan:

- `get_processes()` untuk menerima daftar proses CPU Scheduling.
- `get_memory_capacity()` untuk menerima kapasitas total memori.
- `get_memory_request()` untuk menerima permintaan alokasi memori.
- `get_release_pid()` untuk menerima identitas proses yang akan melepaskan memori.

Setiap fungsi harus memastikan masukan sesuai dengan ketentuan sebelum data diteruskan ke modul berikutnya.

### 5.6 Ketentuan Integrasi
Seluruh modul harus mengikuti interface yang telah ditentukan agar proses integrasi tidak menimbulkan perbedaan format data.

Ketentuan integrasi:

1. `main.py` memulai program melalui `run_menu()`.
2. `menu.py` mengatur pemilihan fitur dan memanggil fungsi input yang sesuai.
3. `input_handler.py` mengembalikan data yang telah divalidasi.
4. Modul Scheduling menerima data `Process` dan menghasilkan `ExecutionSegment`.
5. Modul Metrics menerima data proses beserta timeline untuk menghasilkan `ProcessMetrics`.
6. Modul Memory menerima `MemoryRequest` dan mengelola kondisi `MemoryBlock`.
7. Modul Visualization menerima hasil simulasi untuk ditampilkan di terminal.
8. CPU Scheduling dan Memory Allocation tetap berjalan secara terpisah.

Seluruh interface tersebut menjadi acuan dalam proses implementasi. Jika terdapat perubahan pada interface maka modul yang menggunakan interface tersebut harus diperiksa kembali agar tidak terjadi ketidaksesuaian.

# 6. ALGORITHM SPECIFICATION
Bagian ini menjelaskan aturan kerja algoritma yang digunakan dalam simulator. Setiap algoritma memiliki ketentuan pemrosesan yang jelas agar hasil implementasi dapat diuji dan dibandingkan.

## 6.1 CPU Scheduling
Simulator menggunakan dua algoritma penjadwalan CPU yaitu FCFS dan Preemptive SJF.

### A. First Come First Served (FCFS)
FCFS menjalankan proses berdasarkan urutan kedatangan.

Ketentuannya:
- Proses dengan Arrival Time paling awal dijalankan terlebih dahulu.
- Jika beberapa proses memiliki Arrival Time yang sama maka urutan input digunakan sebagai penentu.
- Proses berjalan sampai selesai tanpa interupsi.
- Jika belum ada proses yang datang maka CPU berada dalam kondisi IDLE.
- Hasil simulasi disimpan dalam bentuk `ExecutionSegment`.

### B. Preemptive Shortest Job First (SJF)
Preemptive SJF atau Shortest Remaining Time First (SRTF) memilih proses berdasarkan waktu eksekusi yang masih tersisa.

Ketentuannya:
- Hanya proses yang sudah tiba yang dapat dipilih.
- Proses dengan Remaining Time paling kecil mendapatkan prioritas.
- Pemilihan proses dievaluasi setiap satu satuan waktu.
- Jika proses baru memiliki Remaining Time lebih kecil maka proses yang sedang berjalan dapat dihentikan sementara.
- Jika Remaining Time sama maka proses dengan Arrival Time lebih awal mendapatkan prioritas.
- Jika Arrival Time juga sama maka urutan input digunakan sebagai penentu.
- Proses yang terpilih kembali setelah mengalami interupsi akan melanjutkan sisa waktu eksekusinya.
- Jika belum ada proses yang dapat dijalankan maka CPU berada dalam kondisi IDLE.
- Hasil simulasi disimpan dalam bentuk `ExecutionSegment`.

### C. Pencatatan Timeline
Kedua algoritma menghasilkan timeline dalam bentuk `List[ExecutionSegment]`.

Setiap segmen mencatat:
- PID proses yang berjalan.
- Waktu mulai eksekusi.
- Waktu selesai eksekusi.

Jika CPU tidak menjalankan proses apa pun maka PID menggunakan nilai `IDLE`.

Segmen dengan PID yang sama dan berjalan secara berurutan tanpa jeda harus digabung menjadi satu segmen. Hal ini dilakukan agar Gantt Chart lebih mudah dibaca.

## 6.2 Performance Metrics
Simulator menghitung tiga metrik untuk setiap proses.

### A. Waiting Time (WT)
Waiting Time menunjukkan total waktu proses menunggu sebelum mendapatkan CPU.

Rumus:

`WT = TAT - BT`

### B. Turnaround Time (TAT)
Turnaround Time menunjukkan total waktu sejak proses tiba sampai selesai dieksekusi.

Rumus:

`TAT = Completion Time - Arrival Time`

### C. Response Time (RT)
Response Time menunjukkan waktu sejak proses tiba sampai pertama kali mendapatkan CPU.

Rumus:

`RT = First Start Time - Arrival Time`

Keterangan:
- `Completion Time` adalah waktu selesai terakhir suatu proses dalam timeline.
- `First Start Time` adalah waktu pertama kali proses mendapatkan CPU.
- `BT` adalah Burst Time.
- `Arrival Time` adalah waktu kedatangan proses.

### D. Average Metrics
Simulator menghitung rata-rata WT, TAT, dan RT dari seluruh proses.

Rumus:

`Average = Total Nilai Metrik / Jumlah Proses`

Hasil perhitungan disimpan menggunakan struktur `ProcessMetrics` dan `Dict[str, float]` sesuai interface pada Bagian 5.

## 6.3 Dynamic Memory Allocation — First-Fit
Simulator menggunakan Dynamic Partitioning dengan metode First-Fit.

Ketentuan pengelolaan memori:

### A. Inisialisasi Memori
- Kapasitas memori ditentukan oleh pengguna.
- Seluruh kapasitas awal dianggap sebagai satu blok kosong.
- Alamat awal memori dimulai dari 0.
- Setiap blok mencatat alamat awal, ukuran, dan PID jika sedang digunakan.

### B. Alokasi Memori
- Permintaan alokasi diterima dalam bentuk `MemoryRequest`.
- Program mencari blok kosong pertama yang ukurannya mencukupi.
- Pencarian dilakukan berdasarkan urutan alamat memori dari yang paling rendah.
- Jika ukuran blok lebih besar dari permintaan maka blok dibagi menjadi bagian teralokasi dan bagian kosong.
- Jika ukurannya sama maka seluruh blok digunakan.
- Jika tidak ditemukan blok yang mencukupi maka alokasi ditolak tanpa mengubah kondisi memori.

### C. Pelepasan Memori
- Pengguna memasukkan PID yang ingin dilepaskan.
- Program mencari blok yang sedang digunakan oleh PID tersebut.
- Jika ditemukan maka blok dikembalikan menjadi blok kosong.
- Jika PID tidak ditemukan maka pelepasan ditolak.

### D. Penggabungan Blok Kosong
Setelah proses pelepasan memori dilakukan program menggabungkan blok kosong yang bersebelahan.

Penggabungan dilakukan selama dua blok kosong tersebut memiliki alamat yang saling berurutan.

Tujuannya adalah mengurangi external fragmentation dan menjaga struktur blok memori tetap konsisten.

## 6.4 Memory Fragmentation
Simulator menggunakan pendekatan visual untuk menunjukkan kondisi memori setelah setiap operasi alokasi atau pelepasan.

External fragmentation dapat terjadi ketika kapasitas total memori yang kosong masih mencukupi suatu permintaan tetapi tersebar dalam beberapa blok yang tidak bersebelahan.

Contohnya:
- Total memori kosong sebesar 100 KB.
- Permintaan alokasi sebesar 70 KB.
- Tidak ada satu blok kosong yang memiliki ukuran minimal 70 KB.

Dalam kondisi tersebut alokasi ditolak karena tidak tersedia blok kosong yang berukuran cukup besar secara berurutan.

Penggabungan blok kosong dilakukan untuk mengurangi kondisi tersebut.

# 7. EXECUTION FLOW & CLI SPECIFICATION
Bagian ini menjelaskan urutan interaksi antara pengguna dan program. Alur dibuat sederhana agar setiap fitur dapat dijalankan secara terpisah melalui terminal.

## 7.1 Program Startup
Saat program dijalankan:
1. `main.py` menjadi titik awal eksekusi.
2. Program memanggil `run_menu()` dari modul interface.
3. Menu utama ditampilkan melalui terminal.
4. Pengguna memilih fitur yang ingin dijalankan.
5. Setelah fitur selesai program kembali ke menu utama atau keluar sesuai pilihan pengguna.

## 7.2 CPU Scheduling Flow
Ketika pengguna memilih CPU Scheduling:

1. Program meminta jumlah proses yang akan disimulasikan.
2. Jumlah proses minimal adalah lima.
3. Program meminta PID, Arrival Time, dan Burst Time setiap proses.
4. Input diperiksa sebelum digunakan.
5. Data proses digunakan oleh algoritma FCFS dan Preemptive SJF.
6. Kedua algoritma menghasilkan timeline masing-masing.
7. Modul metrics menghitung WT, TAT, dan RT.
8. Program menampilkan Gantt Chart untuk kedua algoritma.
9. Program menampilkan hasil metrik setiap proses dan nilai rata-ratanya.
10. Program menampilkan perbandingan hasil kedua algoritma.

Kedua algoritma menggunakan data proses yang sama agar hasil perbandingan tetap adil.

## 7.3 Memory Allocation Flow
Ketika pengguna memilih Memory Allocation:

1. Program meminta kapasitas total memori.
2. Input kapasitas diperiksa sebelum digunakan.
3. Program membuat objek `FirstFitAllocator`.
4. Kondisi awal memori ditampilkan.
5. Pengguna dapat memilih operasi alokasi atau pelepasan memori.
6. Program meminta data yang dibutuhkan sesuai operasi.
7. Input diperiksa sebelum diteruskan ke allocator.
8. Allocator menjalankan operasi yang diminta.
9. Program menampilkan hasil operasi dan kondisi memori terbaru.
10. Pengguna dapat melanjutkan operasi atau kembali ke menu utama.

Memory Map ditampilkan setelah setiap operasi yang berhasil maupun gagal agar kondisi memori tetap dapat diamati.

## 7.4 Main Menu
Menu utama menyediakan tiga pilihan:

1. CPU Scheduling
2. Memory Allocation
3. Exit

Setiap fitur dijalankan secara terpisah. Pengguna dapat kembali ke menu utama setelah menyelesaikan simulasi.

# 8. ERROR HANDLING & DATA VALIDATION
Bagian ini mengatur pemeriksaan input dan penanganan kesalahan agar program tidak memproses data yang tidak sesuai.

## 8.1 CPU Scheduling Validation
Input proses harus memenuhi ketentuan berikut:

- Jumlah proses minimal lima.
- PID tidak boleh kosong.
- Setiap PID harus unik.
- Arrival Time harus berupa bilangan bulat dan bernilai minimal 0.
- Burst Time harus berupa bilangan bulat dan lebih besar dari 0.

Jika input tidak sesuai maka program meminta pengguna memasukkan data kembali.

Data yang belum valid tidak boleh diteruskan ke modul scheduling.

## 8.2 Memory Allocation Validation
Input memori harus memenuhi ketentuan berikut:

- Kapasitas total memori harus berupa bilangan bulat positif.
- PID permintaan alokasi tidak boleh kosong.
- Ukuran permintaan memori harus berupa bilangan bulat positif.
- PID yang sedang menggunakan memori tidak boleh digunakan kembali untuk alokasi baru.
- PID yang dilepaskan harus sesuai dengan proses yang sedang menggunakan memori.

Input yang tidak sesuai harus ditolak sebelum operasi diteruskan ke allocator.

## 8.3 Allocation and Release Errors
Penanganan kesalahan pada pengelolaan memori meliputi:

- Alokasi ditolak jika tidak tersedia blok kosong yang mencukupi.
- Alokasi ditolak jika PID sudah digunakan.
- Pelepasan ditolak jika PID tidak ditemukan.
- Operasi yang gagal tidak boleh mengubah kondisi memori.
- Program menampilkan pesan yang menjelaskan apakah operasi berhasil atau gagal.

Fungsi `allocate()` dan `release()` tetap menggunakan nilai boolean sebagai hasil operasi sesuai interface pada Bagian 5.

## 8.4 General Program Error Handling
Program harus memenuhi ketentuan berikut:

- Input dengan tipe data yang salah tidak boleh menyebabkan program langsung berhenti.
- Nilai yang tidak sesuai ketentuan harus ditolak.
- Kesalahan operasi tidak boleh merusak data simulasi.
- Pesan kesalahan harus mudah dipahami pengguna.
- Pengguna tetap dapat kembali ke menu utama setelah menyelesaikan atau mengalami kegagalan simulasi.

Pemeriksaan input dilakukan melalui `input_handler.py`. Sementara itu modul simulasi bertanggung jawab menjaga konsistensi data selama proses berjalan.

# 9. TESTING & ACCEPTANCE CRITERIA
Pengujian dilakukan untuk memastikan setiap modul bekerja sesuai tanggung jawab dan aturan yang telah ditentukan.

## 9.1 Testing Approach
Pengujian menggunakan dua pendekatan:

**A. Unit Testing**

Menggunakan Python `unittest` untuk menguji fungsi dan algoritma secara terpisah.

**B. Manual Testing**

Dilakukan melalui terminal untuk memastikan menu, input, alur simulasi, dan tampilan hasil berjalan sesuai kebutuhan.

## 9.2 CPU Scheduling Testing
### A. FCFS Testing
Pengujian mencakup:
- Urutan proses berdasarkan Arrival Time.
- Proses dengan Arrival Time yang sama.
- Proses yang datang setelah proses sebelumnya selesai.
- Kondisi CPU IDLE.
- Ketepatan waktu mulai dan selesai setiap proses.

### B. Preemptive SJF Testing
Pengujian mencakup:
- Pemilihan proses berdasarkan Remaining Time terkecil.
- Proses yang mengalami preemption.
- Proses yang melanjutkan sisa eksekusinya.
- Penentuan prioritas ketika Remaining Time sama.
- Kondisi CPU IDLE.
- Ketepatan timeline hasil simulasi.

## 9.3 Metrics Testing
Pengujian mencakup:
- Perhitungan Waiting Time.
- Perhitungan Turnaround Time.
- Perhitungan Response Time.
- Perhitungan rata-rata setiap metrik.
- Kesesuaian hasil perhitungan dengan timeline simulasi.

## 9.4 Memory Allocation Testing
Pengujian First-Fit mencakup:
- Inisialisasi satu blok kosong.
- Pemilihan blok kosong pertama yang mencukupi.
- Pemecahan blok setelah alokasi.
- Alokasi dengan ukuran yang sama persis dengan blok kosong.
- Penolakan alokasi ketika memori tidak mencukupi.
- Penolakan alokasi dengan PID yang sudah digunakan.
- Pelepasan blok memori.
- Penolakan pelepasan PID yang tidak ditemukan.
- Penggabungan blok kosong yang bersebelahan.
- Konsistensi total kapasitas memori setelah setiap operasi.

## 9.5 Acceptance Criteria
Program dinyatakan memenuhi kebutuhan proyek jika:

**A. CPU Scheduling**
- Menerima minimal lima proses.
- Menjalankan FCFS dan Preemptive SJF.
- Menampilkan Gantt Chart.
- Menghitung WT, TAT, dan RT.
- Menampilkan rata-rata setiap metrik.
- Menampilkan perbandingan kedua algoritma.

**B. Memory Allocation**
- Menggunakan Dynamic Partitioning dengan First-Fit.
- Menampilkan kondisi blok memori.
- Mendukung alokasi dan pelepasan memori.
- Melakukan pemecahan dan penggabungan blok.
- Menolak operasi yang tidak valid tanpa merusak kondisi memori.

**C. Program Structure**
- Setiap modul memiliki tanggung jawab yang jelas.
- Komunikasi antarmodul mengikuti interface yang disepakati.
- Program dapat dijalankan melalui terminal.
- Program dapat kembali ke menu utama setelah simulasi.

**D. Testing**
- Unit test untuk setiap modul berhasil dijalankan.
- Hasil pengujian sesuai dengan aturan algoritma.
- Pengujian manual memastikan alur program berjalan dengan baik.

# 10. CODING STANDARDS & CONSTRAINTS
Bagian ini menjadi pedoman selama implementasi agar struktur kode tetap konsisten dan sesuai dengan rancangan yang telah ditentukan.

## 10.1 Coding Standards
Standar penulisan kode meliputi:

- Menggunakan `snake_case` untuk nama fungsi dan variabel.
- Menggunakan `PascalCase` untuk nama class.
- Menggunakan huruf kapital untuk konstanta.
- Menggunakan type hints pada fungsi dan parameter.
- Menggunakan Python `dataclass` untuk struktur data yang telah ditentukan.
- Menggunakan indentasi empat spasi.
- Menambahkan komentar atau docstring pada bagian yang membutuhkan penjelasan.
- Menghindari pengulangan kode yang tidak diperlukan.

## 10.2 Modular Programming
Setiap file harus menjalankan tanggung jawab sesuai struktur arsitektur pada Bagian 2 dan pembagian modul pada Bagian 4.

Ketentuannya:
- `main.py` hanya menjadi titik awal program.
- Modul interface mengatur interaksi pengguna.
- Modul scheduling menjalankan algoritma CPU.
- Modul metrics menghitung hasil penjadwalan.
- Modul memory mengelola alokasi dan pelepasan memori.
- Modul visualization menampilkan hasil simulasi.
- Modul testing menguji fungsi setiap komponen.

Setiap modul hanya menjalankan tugas yang menjadi tanggung jawabnya. Proses perhitungan tidak boleh dipindahkan ke modul visualization dan interaksi terminal tidak boleh dimasukkan ke modul algoritma.

## 10.3 Implementation Constraints
Implementasi harus mengikuti ketentuan berikut:

- Mengikuti struktur direktori yang telah disepakati.
- Menggunakan struktur data sesuai Bagian 3.
- Menggunakan pembagian tanggung jawab sesuai Bagian 4.
- Menggunakan nama fungsi, parameter, dan tipe nilai sesuai Bagian 5.
- Tidak menambahkan modul atau file baru tanpa kebutuhan teknis yang jelas.
- Tidak menggabungkan beberapa modul yang memiliki tanggung jawab berbeda.
- Menjaga agar integrasi antarmodul tidak mengubah kontrak yang telah ditentukan.

## 10.4 Dependency Constraints
Program mengutamakan Python Standard Library.

Tidak menggunakan library eksternal jika kebutuhan program dapat dipenuhi dengan fitur bawaan Python.

Jika terdapat kebutuhan teknis yang mengharuskan penggunaan library tambahan maka dependensi tersebut harus dicantumkan dalam `requirements.txt`.

## 10.5 Project Scope Constraints
Implementasi dibatasi pada ruang lingkup berikut:

- Antarmuka program menggunakan CLI.
- Algoritma CPU hanya menggunakan FCFS dan Preemptive SJF.
- Pengelolaan memori hanya menggunakan Dynamic Partitioning dengan First-Fit.
- Simulasi CPU Scheduling dan Memory Allocation berjalan secara terpisah.
- Program tidak melakukan modifikasi terhadap sistem operasi atau pengelolaan memori fisik komputer.
- Tidak menambahkan fitur di luar kebutuhan soal UTS dan kontrak proyek.