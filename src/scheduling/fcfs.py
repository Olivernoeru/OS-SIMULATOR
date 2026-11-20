"""
FCFS (First Come First Served) CPU Scheduling Algorithm
Sesuai MODULE_CONTRACT.md Bagian 6.1.A
"""
from typing import List
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


def run_fcfs(processes: List[Process]) -> List[ExecutionSegment]:
    """
    Menjalankan algoritma First Come First Served (FCFS).

    Args:
        processes: Daftar proses yang akan dijadwalkan.

    Returns:
        List[ExecutionSegment]: Timeline eksekusi proses.
    """
    if not processes:
        return []

    # Stable sort: arrival_time ASC, lalu input order (index)
    indexed_processes = list(enumerate(processes))
    indexed_processes.sort(key=lambda x: (x[1].arrival_time, x[0]))

    timeline: List[ExecutionSegment] = []
    current_time = 0

    for _, process in indexed_processes:
        # Jika CPU idle sebelum proses ini tiba
        if process.arrival_time > current_time:
            timeline.append(ExecutionSegment("IDLE", current_time, process.arrival_time))
            current_time = process.arrival_time

        # Eksekusi proses hingga selesai (non-preemptive)
        start_time = current_time
        end_time = current_time + process.burst_time
        timeline.append(ExecutionSegment(process.pid, start_time, end_time))
        current_time = end_time

    # Gabungkan segmen berurutan dengan PID sama
    return _merge_segments(timeline)
