"""
Input Handler Module
Sesuai MODULE_CONTRACT.md Bagian 5.5.B
Mengelola validasi dan pengambilan input pengguna untuk CPU Scheduling dan Memory Allocation.
"""

from typing import List, Set
from src import Process, MemoryRequest


def _get_int_input(prompt: str, min_val: int = None, positive_only: bool = False, allow_zero: bool = True) -> int:
    """
    Helper internal: minta input integer dengan validasi.

    Args:
        prompt: Pesan prompt untuk pengguna.
        min_val: Nilai minimum (inklusif), None = tidak ada batas bawah.
        positive_only: Jika True, nilai harus > 0.
        allow_zero: Jika False, nilai 0 tidak diperbolehkan.

    Returns:
        Integer yang divalidasi.
    """
    while True:
        try:
            raw = input(prompt).strip()
            if not raw:
                print("Input tidak boleh kosong. Masukkan bilangan bulat.")
                continue
            val = int(raw)
            if positive_only and val <= 0:
                print("Nilai harus bilangan bulat positif (> 0).")
                continue
            if not allow_zero and val == 0:
                print("Nilai tidak boleh 0.")
                continue
            if min_val is not None and val < min_val:
                print(f"Nilai harus >= {min_val}.")
                continue
            return val
        except ValueError:
            print("Input tidak valid. Masukkan bilangan bulat.")


def _get_non_empty_string(prompt: str) -> str:
    """Helper internal: minta string non-kosong (setelah strip)."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Input tidak boleh kosong.")


def _is_pid_unique(pid: str, existing_pids: Set[str]) -> bool:
    """Cek apakah PID unik (case-sensitive) di antara existing_pids."""
    return pid not in existing_pids


def get_processes() -> List[Process]:
    """
    Menerima dan memvalidasi daftar proses untuk CPU Scheduling.
    Minimal 5 proses. Setiap proses: PID unik, arrival_time >= 0, burst_time > 0.

    Returns:
        List[Process]: Daftar proses yang divalidasi, urut sesuai input pengguna.
    """
    print("\n=== INPUT PROSES CPU SCHEDULING ===")
    print("Masukkan minimal 5 proses.")
    print("Format: PID (unik), Arrival Time (>= 0), Burst Time (> 0)")
    print()

    processes: List[Process] = []
    used_pids: Set[str] = set()
    process_num = 1

    while True:
        print(f"--- Proses ke-{process_num} ---")
        # PID
        while True:
            pid = _get_non_empty_string("PID: ")
            if pid == "IDLE":
                print("PID 'IDLE' adalah identifier khusus untuk CPU idle dan tidak boleh digunakan.")
                print("Masukkan PID yang berbeda.")
                continue
            if _is_pid_unique(pid, used_pids):
                used_pids.add(pid)
                break
            print(f"PID '{pid}' sudah digunakan. Masukkan PID yang berbeda.")

        # Arrival Time
        arrival_time = _get_int_input("Arrival Time: ", min_val=0, allow_zero=True)

        # Burst Time
        burst_time = _get_int_input("Burst Time: ", min_val=1, positive_only=True)

        processes.append(Process(pid=pid, arrival_time=arrival_time, burst_time=burst_time))
        print(f"Proses {pid} ditambahkan.\n")

        process_num += 1

        # Setelah minimal 5, tanya apakah lanjut
        if len(processes) >= 5:
            while True:
                lanjut = input("Tambah proses lagi? (y/n): ").strip().lower()
                if lanjut in ('y', 'yes'):
                    print()
                    break
                elif lanjut in ('n', 'no'):
                    print()
                    return processes
                else:
                    print("Masukkan 'y' untuk ya atau 'n' untuk tidak.")


def get_memory_capacity() -> int:
    """
    Menerima dan memvalidasi kapasitas total memori.

    Returns:
        int: Kapasitas memori (> 0).
    """
    print("\n=== INPUT KAPASITAS MEMORI ===")
    capacity = _get_int_input("Kapasitas total memori: ", min_val=1, positive_only=True)
    print(f"Kapasitas memori disetel ke {capacity} unit.\n")
    return capacity


def get_memory_request() -> MemoryRequest:
    """
    Menerima dan memvalidasi permintaan alokasi memori.
    PID harus unik di antara proses yang sedang memiliki alokasi aktif (divalidasi di allocator).
    Size harus integer positif.

    Returns:
        MemoryRequest: Objek permintaan alokasi (pid, size).
    """
    print("\n=== ALOKASI MEMORI ===")
    pid = _get_non_empty_string("PID Proses: ")
    size = _get_int_input("Ukuran memori yang dibutuhkan: ", min_val=1, positive_only=True)
    print()
    return MemoryRequest(pid=pid, size=size)


def get_release_pid(allocated_pids: List[str]) -> str:
    """
    Menerima dan memvalidasi PID untuk pelepasan memori.
    PID harus ada di daftar allocated_pids.

    Args:
        allocated_pids: Daftar PID yang sedang memiliki alokasi aktif.

    Returns:
        str: PID yang valid untuk direlease.
    """
    print("\n=== RELEASE MEMORI ===")
    print("Proses dengan alokasi aktif:", ", ".join(allocated_pids) if allocated_pids else "(tidak ada)")

    while True:
        pid = _get_non_empty_string("PID yang akan dilepaskan: ")
        if pid in allocated_pids:
            print()
            return pid
        print(f"PID '{pid}' tidak ditemukan dalam daftar alokasi aktif. Masukkan PID yang valid.")
