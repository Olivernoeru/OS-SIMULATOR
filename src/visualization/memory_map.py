"""
Memory Map Visualization
Sesuai MODULE_CONTRACT.md Bagian 4.5.B, 5.4.B
Text-Based Memory Map untuk hasil alokasi memori
"""
from typing import List
from src import MemoryBlock


def _block_width(block: MemoryBlock) -> int:
    """
    Hitung lebar kolom untuk satu blok memori.
    
    Args:
        block: MemoryBlock dengan start_address, size, process_id
    
    Returns:
        Lebar kolom dalam karakter
    """
    start = block.start_address
    end = block.start_address + block.size - 1
    pid = block.process_id if block.process_id else "FREE"
    addr_str = f"{start}-{end}"
    size_str = f"({block.size})"
    return max(len(pid), len(addr_str), len(size_str)) + 2  # padding


def display_memory_map(blocks: List[MemoryBlock]) -> None:
    """
    Menampilkan gambaran kondisi blok memori di terminal.

    Args:
        blocks: List[MemoryBlock] - hasil dari allocator.get_blocks()
                Setiap blok memiliki start_address, size, process_id (None = free)
    """
    if not blocks:
        print("Memory Map: (kosong)")
        return

    # 1. Hitung lebar setiap kolom
    widths = [_block_width(block) for block in blocks]

    # 2. Render border atas
    print("Memory Map:")
    border = "+" + "+".join("-" * w for w in widths) + "+"
    print(border)

    # 3. Render baris status (PID atau FREE)
    status_row = "|" + "|".join(
        (block.process_id if block.process_id else "FREE").center(w)
        for block, w in zip(blocks, widths)
    ) + "|"
    print(status_row)

    # 4. Render baris alamat (start-end)
    addr_row = "|" + "|".join(
        f"{block.start_address}-{block.start_address + block.size - 1}".center(w)
        for block, w in zip(blocks, widths)
    ) + "|"
    print(addr_row)

    # 5. Render baris ukuran (size)
    size_row = "|" + "|".join(
        f"({block.size})".center(w)
        for block, w in zip(blocks, widths)
    ) + "|"
    print(size_row)

    # 6. Render border bawah
    print(border)

    # 7. Render summary
    total = sum(block.size for block in blocks)
    used = sum(block.size for block in blocks if block.process_id is not None)
    free = sum(block.size for block in blocks if block.process_id is None)
    print(f"Total: {total} | Used: {used} | Free: {free}")
