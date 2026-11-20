"""
Menu Module
Sesuai MODULE_CONTRACT.md Bagian 5.5.A
Mengelola tampilan menu dan alur navigasi program.
"""

from typing import List, Dict
from src import Process, ExecutionSegment, ProcessMetrics, MemoryBlock
from src.scheduling.fcfs import run_fcfs
from src.scheduling.sjf_preemptive import run_sjf_preemptive
from src.scheduling.metrics import calculate_metrics, calculate_average_metrics
from src.memory.first_fit import FirstFitAllocator
from src.visualization.gantt import display_gantt
from src.visualization.memory_map import display_memory_map
from src.interface.input_handler import (
    get_processes,
    get_memory_capacity,
    get_memory_request,
    get_release_pid,
)


def display_main_menu() -> None:
    """Menampilkan menu utama program ke terminal."""
    print("=" * 60)
    print("OS-SIMULATOR")
    print("Simulator Penjadwalan CPU & Manajemen Alokasi Memori Dinamis")
    print("=" * 60)
    print()
    print("MENU UTAMA:")
    print("1. CPU Scheduling (FCFS & SJF Preemptive)")
    print("2. Memory Allocation (First-Fit)")
    print("3. Keluar")
    print()


def _display_cpu_scheduling_submenu() -> None:
    """Menampilkan sub-menu CPU Scheduling (hanya informasi, tidak interaktif)."""
    print("\n=== CPU SCHEDULING ===")
    print("Menjalankan simulasi FCFS dan SJF Preemptive pada proses yang sama.")
    print("Hasil: Gantt Chart, Metrik per Proses, Rata-rata, dan Perbandingan.")
    print()


def _display_memory_allocation_submenu() -> None:
    """Menampilkan sub-menu Memory Allocation."""
    print("\n=== MEMORY ALLOCATION (FIRST-FIT) ===")
    print("1. Alokasi Memori")
    print("2. Release Memori")
    print("3. Tampilkan Memory Map")
    print("4. Kembali ke Menu Utama")
    print()


def _display_metrics_table(metrics: List[ProcessMetrics], avg: Dict[str, float], algo_name: str) -> None:
    """
    Menampilkan tabel metrik per proses dan rata-rata.

    Args:
        metrics: List ProcessMetrics per proses.
        avg: Dict dengan key avg_waiting_time, avg_turnaround_time, avg_response_time.
        algo_name: Nama algoritma untuk header.
    """
    print(f"\n--- {algo_name} ---")
    print("Metrik per Proses:")
    print("+------+-----+-----+-----+")
    print("| PID  | WT  | TAT | RT  |")
    print("+------+-----+-----+-----+")
    for m in metrics:
        print(f"| {m.pid:<4} | {m.waiting_time:>3} | {m.turnaround_time:>3} | {m.response_time:>3} |")
    print("+------+-----+-----+-----+")
    print(f"Rata-rata: WT={avg['avg_waiting_time']:.2f}, TAT={avg['avg_turnaround_time']:.2f}, RT={avg['avg_response_time']:.2f}")


def _display_comparison(
    metrics_fcfs: List[ProcessMetrics],
    metrics_sjf: List[ProcessMetrics],
    avg_fcfs: Dict[str, float],
    avg_sjf: Dict[str, float]
) -> None:
    """
    Menampilkan tabel perbandingan FCFS vs SJF Preemptive.

    Args:
        metrics_fcfs: Metrik dari FCFS.
        metrics_sjf: Metrik dari SJF Preemptive.
        avg_fcfs: Rata-rata FCFS.
        avg_sjf: Rata-rata SJF Preemptive.
    """
    print("\n--- PERBANDINGAN FCFS vs SJF PREEMPTIVE ---")
    print("+--------------+----------+----------+----------+")
    print("| Algoritma    | Avg WT   | Avg TAT  | Avg RT   |")
    print("+--------------+----------+----------+----------+")
    print(f"| {'FCFS':<12} | {avg_fcfs['avg_waiting_time']:>8.2f} | {avg_fcfs['avg_turnaround_time']:>8.2f} | {avg_fcfs['avg_response_time']:>8.2f} |")
    print(f"| {'SJF Preemptive':<12} | {avg_sjf['avg_waiting_time']:>8.2f} | {avg_sjf['avg_turnaround_time']:>8.2f} | {avg_sjf['avg_response_time']:>8.2f} |")
    print("+--------------+----------+----------+----------+")


def _run_cpu_scheduling_flow(processes: List[Process]) -> None:
    """
    Menjalankan alur lengkap CPU Scheduling: FCFS -> SJF -> Metrik -> Perbandingan.

    Args:
        processes: Daftar proses yang sudah divalidasi (minimal 5).
    """
    print(f"\nJumlah proses: {len(processes)}")
    for p in processes:
        print(f"  {p.pid}: Arrival={p.arrival_time}, Burst={p.burst_time}")

    # FCFS
    print("\n" + "=" * 50)
    print("MENJALANKAN FCFS (First Come First Served)")
    print("=" * 50)
    timeline_fcfs = run_fcfs(processes)
    display_gantt(timeline_fcfs)
    metrics_fcfs = calculate_metrics(processes, timeline_fcfs)
    avg_fcfs = calculate_average_metrics(metrics_fcfs)
    _display_metrics_table(metrics_fcfs, avg_fcfs, "FCFS")

    # SJF Preemptive
    print("\n" + "=" * 50)
    print("MENJALANKAN SJF PREEMPTIVE (SRTF)")
    print("=" * 50)
    timeline_sjf = run_sjf_preemptive(processes)
    display_gantt(timeline_sjf)
    metrics_sjf = calculate_metrics(processes, timeline_sjf)
    avg_sjf = calculate_average_metrics(metrics_sjf)
    _display_metrics_table(metrics_sjf, avg_sjf, "SJF Preemptive")

    # Perbandingan
    _display_comparison(metrics_fcfs, metrics_sjf, avg_fcfs, avg_sjf)

    print("\nTekan Enter untuk kembali ke menu utama...")
    input()


def _run_memory_allocation_flow(allocator: FirstFitAllocator) -> None:
    """
    Menjalankan loop Memory Allocation: alokasi, release, tampilkan map.

    Args:
        allocator: Instance FirstFitAllocator yang sudah diinisialisasi.
    """
    while True:
        _display_memory_allocation_submenu()
        display_memory_map(allocator.get_blocks())

        choice = input("Pilihan [1-4]: ").strip()

        if choice == "1":
            request = get_memory_request()
            # Cek duplicate PID sebelum allocate untuk pesan error yang tepat
            blocks = allocator.get_blocks()
            active_pids = [b.process_id for b in blocks if b.process_id is not None]

            if request.pid in active_pids:
                print(f"Alokasi GAGAL: PID '{request.pid}' sudah memiliki alokasi aktif.")
            else:
                success = allocator.allocate(request)
                if success:
                    print(f"Alokasi memori untuk {request.pid} ({request.size} unit) BERHASIL.")
                else:
                    print(f"Alokasi GAGAL: Tidak ditemukan blok kosong cukup untuk {request.pid} ({request.size} unit).")
            display_memory_map(allocator.get_blocks())
            print("Tekan Enter untuk melanjutkan...")
            input()

        elif choice == "2":
            blocks = allocator.get_blocks()
            allocated_pids = [b.process_id for b in blocks if b.process_id is not None]
            if not allocated_pids:
                print("Tidak ada proses yang memiliki alokasi memori aktif.")
                print("Tekan Enter untuk kembali...")
                input()
                continue
            pid = get_release_pid(allocated_pids)
            success = allocator.release(pid)
            if success:
                print(f"Release memori untuk {pid} BERHASIL.")
            else:
                print(f"Release GAGAL: PID {pid} tidak ditemukan.")
            display_memory_map(allocator.get_blocks())
            print("Tekan Enter untuk melanjutkan...")
            input()

        elif choice == "3":
            display_memory_map(allocator.get_blocks())
            print("Tekan Enter untuk melanjutkan...")
            input()

        elif choice == "4":
            print("Kembali ke menu utama...")
            break

        else:
            print("Pilihan tidak valid. Masukkan 1-4.")
            print("Tekan Enter untuk melanjutkan...")
            input()


def run_menu() -> None:
    """
    Entry point menu utama. Loop sampai user memilih keluar.
    Menangani KeyboardInterrupt dan EOFError untuk keluar bersih.
    """
    try:
        while True:
            display_main_menu()
            choice = input("Pilihan [1-3]: ").strip()

            if choice == "1":
                processes = get_processes()
                _run_cpu_scheduling_flow(processes)

            elif choice == "2":
                capacity = get_memory_capacity()
                allocator = FirstFitAllocator(capacity)
                _run_memory_allocation_flow(allocator)

            elif choice == "3":
                print("\nTerima kasih telah menggunakan OS-SIMULATOR. Sampai jumpa!")
                break

            else:
                print("Pilihan tidak valid. Masukkan 1, 2, atau 3.")
                print("Tekan Enter untuk melanjutkan...")
                input()

    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna (Ctrl+C). Sampai jumpa!")
    except EOFError:
        print("\n\nInput ditutup (EOF). Sampai jumpa!")
