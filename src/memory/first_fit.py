"""
First-Fit Dynamic Memory Allocator
Sesuai MODULE_CONTRACT.md Bagian 4.4, 5.3, 6.3
"""
from typing import List
from src import MemoryRequest, MemoryBlock


class FirstFitAllocator:
    """Dynamic Partitioning dengan metode First-Fit."""

    def __init__(self, total_memory: int) -> None:
        """
        Inisialisasi memori dengan satu blok kosong penuh.

        Args:
            total_memory: Kapasitas total memori (harus int positif).

        Raises:
            ValueError: Jika total_memory bukan integer positif.
        """
        # Validasi ketat: int positif, bukan bool, bukan float
        if not isinstance(total_memory, int) or isinstance(total_memory, bool) or total_memory <= 0:
            raise ValueError("Kapasitas total memori harus bilangan bulat positif")

        self._total_memory = total_memory
        # Satu blok kosong: start=0, size=total_memory, process_id=None
        self._blocks: List[MemoryBlock] = [MemoryBlock(0, total_memory, None)]

    def allocate(self, request: MemoryRequest) -> bool:
        """
        Alokasi memori menggunakan First-Fit.

        Args:
            request: Permintaan alokasi (pid, size).

        Returns:
            True jika berhasil, False jika tidak ada blok cukup atau PID sudah teralokasi (state tidak berubah).

        Raises:
            ValueError: Jika request.size tidak valid.
        """
        # Validasi size
        if not isinstance(request.size, int) or isinstance(request.size, bool) or request.size <= 0:
            raise ValueError("Ukuran permintaan memori harus bilangan bulat positif")

        # Validasi PID unik di allocated blocks
        for b in self._blocks:
            if b.process_id == request.pid:
                return False  # Duplicate PID → gagal, state tidak berubah

        # First-Fit search: urut by start_address (sudah terurut)
        for i, block in enumerate(self._blocks):
            if block.process_id is None and block.size >= request.size:
                # DITEMUKAN blok yang cukup
                if block.size == request.size:
                    # Exact fit: replace dengan allocated
                    new_blocks = self._blocks[:i] + [MemoryBlock(block.start_address, block.size, request.pid)] + self._blocks[i+1:]
                else:
                    # Split: allocated + remaining free
                    allocated = MemoryBlock(block.start_address, request.size, request.pid)
                    remaining = MemoryBlock(
                        block.start_address + request.size,
                        block.size - request.size,
                        None
                    )
                    new_blocks = self._blocks[:i] + [allocated, remaining] + self._blocks[i+1:]

                self._blocks = new_blocks
                return True

        # Tidak ditemukan blok yang cukup
        return False

    def release(self, pid: str) -> bool:
        """
        Lepaskan memori berdasarkan PID.

        Args:
            pid: Identitas proses.

        Returns:
            True jika ditemukan dan dilepaskan, False jika PID tidak ditemukan.
        """
        for i, block in enumerate(self._blocks):
            if block.process_id == pid:
                # DITEMUKAN: jadikan free
                self._blocks[i] = MemoryBlock(block.start_address, block.size, None)
                # Coalescing otomatis
                self._coalesce()
                return True
        return False

    def get_blocks(self) -> List[MemoryBlock]:
        """
        Dapatkan salinan kondisi semua blok memori.

        Returns:
            List[MemoryBlock]: Deep copy - aman dari modifikasi eksternal.
        """
        # Deep copy: buat instance MemoryBlock baru
        return [
            MemoryBlock(b.start_address, b.size, b.process_id)
            for b in self._blocks
        ]

    def _coalesce(self) -> None:
        """Gabungkan blok kosong (process_id=None) yang bersebelahan."""
        if not self._blocks:
            return

        merged = [self._blocks[0]]
        for block in self._blocks[1:]:
            last = merged[-1]
            # Keduanya free DAN bersebelahan (alamat contiguous)
            if last.process_id is None and block.process_id is None:
                if last.start_address + last.size == block.start_address:
                    # Gabungkan
                    merged[-1] = MemoryBlock(
                        last.start_address,
                        last.size + block.size,
                        None
                    )
                else:
                    merged.append(block)
            else:
                merged.append(block)

        self._blocks = merged
