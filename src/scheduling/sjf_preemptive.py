"""
Preemptive SJF (Shortest Remaining Time First / SRTF) CPU Scheduling Algorithm
Sesuai MODULE_CONTRACT.md Bagian 6.1.B
"""
from typing import List, Dict, Any
from src import Process, ExecutionSegment


def _merge_segments(segments: List[ExecutionSegment]) -> List[ExecutionSegment]:
    """
    Gabungkan segmen berurutan dengan PID yang sama tanpa jeda.
    Sesuai Kontrak Bagian 6.1.C.
    """
    if not segments:
        return []

    merged = []
    current = segments[0]

    for seg in segments[1:]:
        if seg.pid == current.pid and seg.start_time == current.end_time:
            # Gabungkan: perpanjang end_time
            current = ExecutionSegment(current.pid, current.start_time, seg.end_time)
        else:
            merged.append(current)
            current = seg

    merged.append(current)
    return merged


def run_sjf_preemptive(processes: List[Process]) -> List[ExecutionSegment]:
    """
    Menjalankan algoritma Preemptive Shortest Job First (SRTF).

    Args:
        processes: Daftar proses yang akan dijadwalkan.

    Returns:
        List[ExecutionSegment]: Timeline eksekusi proses.
    """
    if not processes:
        return []

    # Inisialisasi state proses internal (menggunakan dict, bukan dataclass baru)
    proc_states: List[Dict[str, Any]] = []
    for idx, process in enumerate(processes):
        proc_states.append({
            "process": process,
            "remaining_time": process.burst_time,
            "first_start_time": None,
            "completed": False,
            "input_index": idx,
        })

    timeline: List[ExecutionSegment] = []
    current_time = 0
    current_pid: str | None = None
    segment_start = 0

    # Loop utama: berjalan selama ada proses yang belum selesai
    while any(not ps["completed"] for ps in proc_states):
        # Cari proses yang sudah tiba dan belum selesai
        ready = [
            ps for ps in proc_states
            if ps["process"].arrival_time <= current_time and not ps["completed"]
        ]

        if not ready:
            # Tidak ada proses siap -> CPU IDLE
            if current_pid is not None:
                # Tutup segmen sebelumnya
                timeline.append(ExecutionSegment(current_pid, segment_start, current_time))
            current_pid = "IDLE"
            segment_start = current_time
            current_time += 1
            continue

        # Pilih proses dengan remaining_time terkecil
        # Tie-breaking: remaining_time -> arrival_time -> input_index
        selected = min(
            ready,
            key=lambda ps: (ps["remaining_time"], ps["process"].arrival_time, ps["input_index"])
        )

        selected_pid = selected["process"].pid

        # Context switch jika PID berubah
        if selected_pid != current_pid:
            if current_pid is not None:
                # Tutup segmen lama
                timeline.append(ExecutionSegment(current_pid, segment_start, current_time))
            current_pid = selected_pid
            segment_start = current_time
            # Catat first start time jika pertama kali jalan
            if selected["first_start_time"] is None:
                selected["first_start_time"] = current_time

        # Eksekusi 1 unit waktu
        selected["remaining_time"] -= 1
        current_time += 1

        # Cek apakah proses selesai
        if selected["remaining_time"] == 0:
            selected["completed"] = True
            # Segmen akan ditutup di iterasi berikutnya saat context switch
            # atau di finalisasi di bawah

    # Finalisasi: tutup segmen terakhir jika ada
    if current_pid is not None:
        timeline.append(ExecutionSegment(current_pid, segment_start, current_time))

    # Gabungkan segmen berurutan dengan PID sama
    return _merge_segments(timeline)
