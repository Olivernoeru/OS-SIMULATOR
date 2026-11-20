"""
Performance Metrics Calculation for CPU Scheduling
Sesuai MODULE_CONTRACT.md Bagian 5.2.C dan 6.2
"""
from typing import List, Dict
from src import Process, ExecutionSegment, ProcessMetrics


def calculate_metrics(
    processes: List[Process],
    timeline: List[ExecutionSegment]
) -> List[ProcessMetrics]:
    """
    Menghitung Waiting Time (WT), Turnaround Time (TAT), dan Response Time (RT)
    untuk setiap proses berdasarkan timeline hasil penjadwalan.

    Args:
        processes: Daftar proses yang dijadwalkan.
        timeline: Hasil timeline dari algoritma penjadwalan (FCFS atau SRTF).

    Returns:
        List[ProcessMetrics]: Metrik untuk setiap proses, berurutan sesuai input processes.

    Raises:
        ValueError: Jika processes kosong, timeline kosong, atau proses tidak memiliki segmen eksekusi.
    """
    if not processes:
        raise ValueError("Daftar proses kosong")
    if not timeline:
        raise ValueError("Timeline kosong")

    # Bangun pemetaan segmen per proses (hanya proses, abaikan IDLE)
    process_segments: Dict[str, List[ExecutionSegment]] = {}
    for seg in timeline:
        if seg.pid == "IDLE":
            continue
        if seg.pid not in process_segments:
            process_segments[seg.pid] = []
        process_segments[seg.pid].append(seg)

    metrics_list: List[ProcessMetrics] = []

    for process in processes:
        segments = process_segments.get(process.pid)
        if not segments:
            raise ValueError(f"Proses {process.pid} tidak memiliki segmen eksekusi dalam timeline")

        # Completion Time = waktu selesai terakhir
        completion_time = max(seg.end_time for seg in segments)
        # First Start Time = waktu mulai pertama
        first_start_time = min(seg.start_time for seg in segments)

        # Rumus sesuai Kontrak Bagian 6.2
        turnaround_time = completion_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_time = first_start_time - process.arrival_time

        metrics_list.append(ProcessMetrics(
            pid=process.pid,
            waiting_time=waiting_time,
            turnaround_time=turnaround_time,
            response_time=response_time
        ))

    return metrics_list


def calculate_average_metrics(metrics: List[ProcessMetrics]) -> Dict[str, float]:
    """
    Menghitung rata-rata Waiting Time, Turnaround Time, dan Response Time.

    Args:
        metrics: Daftar metrik setiap proses.

    Returns:
        Dict[str, float]: Dictionary dengan key 'avg_waiting_time', 'avg_turnaround_time', 'avg_response_time'.

    Raises:
        ValueError: Jika daftar metrik kosong.
    """
    if not metrics:
        raise ValueError("Daftar metrik kosong, tidak dapat menghitung rata-rata")

    n = len(metrics)
    return {
        "avg_waiting_time": sum(m.waiting_time for m in metrics) / n,
        "avg_turnaround_time": sum(m.turnaround_time for m in metrics) / n,
        "avg_response_time": sum(m.response_time for m in metrics) / n,
    }
