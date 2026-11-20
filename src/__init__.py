"""
OS-SIMULATOR - Core Data Structures
Lima dataclass utama sesuai MODULE_CONTRACT.md Bagian 3.2 & 3.3
"""
from dataclasses import dataclass
from typing import Optional

__all__ = [
    "Process",
    "ExecutionSegment",
    "ProcessMetrics",
    "MemoryRequest",
    "MemoryBlock",
]

@dataclass
class Process:
    """Proses CPU Scheduling (Bagian 3.2.A)."""
    pid: str
    arrival_time: int
    burst_time: int

@dataclass
class ExecutionSegment:
    """Segmen eksekusi Gantt Chart (Bagian 3.2.B)."""
    pid: str
    start_time: int
    end_time: int

@dataclass
class ProcessMetrics:
    """Metrik performa per proses (Bagian 3.2.C)."""
    pid: str
    waiting_time: int
    turnaround_time: int
    response_time: int

@dataclass
class MemoryRequest:
    """Permintaan alokasi memori (Bagian 3.3.A)."""
    pid: str
    size: int

@dataclass
class MemoryBlock:
    """Blok memori Dynamic Partitioning (Bagian 3.3.B)."""
    start_address: int
    size: int
    process_id: Optional[str] = None  # None = free, str = allocated
