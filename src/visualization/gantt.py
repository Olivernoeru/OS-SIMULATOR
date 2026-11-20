"""
Gantt Chart Visualization
Sesuai MODULE_CONTRACT.md Bagian 4.5.A, 5.4.A
Text-Based Gantt Chart untuk hasil penjadwalan CPU
"""
from typing import List
from src import ExecutionSegment


# Konstanta rendering
CHAR_PER_UNIT = 2      # 2 karakter mewakili 1 unit waktu
MIN_WIDTH = 4          # Minimal "| X |" (4 karakter)


def _segment_width(pid: str, duration: int) -> int:
    """
    Hitung lebar kotak dasar untuk satu segmen (berdasarkan PID dan durasi).
    
    Args:
        pid: ID proses
        duration: end_time - start_time
    
    Returns:
        Lebar dalam karakter (integer)
    """
    pid_width = len(pid) + 2          # padding 1 spasi kiri + 1 kanan
    duration_width = duration * CHAR_PER_UNIT
    return max(pid_width, duration_width, MIN_WIDTH)


def _adjust_widths_for_time_labels(
    timeline: List[ExecutionSegment],
    widths: List[int]
) -> List[int]:
    """
    Sesuaikan lebar segmen agar label waktu (angka) muat di boundary.
    
    Label waktu muncul di:
    - Boundary 0 (kiri segmen pertama): start_time segmen pertama (left-aligned)
    - Boundary i (kanan segmen i-1 / kiri segmen i): end_time segmen i-1 (center-aligned)
    - Boundary terakhir (kanan segmen terakhir): end_time segmen terakhir (center-aligned)
    
    Args:
        timeline: Daftar segmen eksekusi
        widths: Lebar awal segmen
    
    Returns:
        Lebar yang disesuaikan
    """
    if not timeline:
        return widths
    
    adjusted = widths.copy()
    
    # Boundary 0: start_time segmen pertama (posisi 0, left-aligned)
    # Label ini memerlukan lebar penuh len(label) di segmen pertama
    first_start_label = str(timeline[0].start_time)
    start_label_len = len(first_start_label)
    
    # Boundary i (1..n-1): end_time segmen i-1, muncul di boundary setelah segmen i-1
    # Boundary terakhir (n): end_time segmen terakhir, muncul di ujung kanan
    for i in range(len(timeline)):
        end_label = str(timeline[i].end_time)
        label_len = len(end_label)
        
        # Posisi boundary ini: setelah segmen 0..i
        # Kita butuh ruang di segmen i untuk label ini (centered di boundary)
        # Minimal: setengah label di kiri boundary, setengah di kanan
        # Tapi karena boundary di ujung segmen i, label butuh ruang di segmen i
        needed_half = (label_len + 1) // 2  # ceil(label_len/2)
        
        # Segmen i harus cukup lebar untuk accommodate label di kanannya
        if adjusted[i] < needed_half * 2:
            adjusted[i] = max(adjusted[i], needed_half * 2)
        
        # Juga cek segmen i-1 (label center di boundary, butuh ruang di kiri juga)
        if i > 0:
            if adjusted[i - 1] < needed_half * 2:
                adjusted[i - 1] = max(adjusted[i - 1], needed_half * 2)
    
    # Khusus: pastikan segmen 0 cukup lebar agar start_time (left-aligned di boundary 0)
    # tidak bertabrakan dengan end_time pertama (center-aligned di boundary 1)
    # Boundary 1 = adjusted[0] + 1
    # end_time pertama mulai di: boundary_1 - len(end_label_0)//2
    # start_time berakhir di: start_label_len - 1
    # Butuh: start_label_len < (adjusted[0] + 1) - len(end_label_0)//2  (dengan spasi minimal 1)
    # => adjusted[0] >= start_label_len + len(end_label_0)//2
    if timeline:
        first_end_label = str(timeline[0].end_time)
        min_width_0 = start_label_len + len(first_end_label) // 2
        if adjusted[0] < min_width_0:
            adjusted[0] = min_width_0
    
    return adjusted


def _build_time_line(timeline: List[ExecutionSegment], widths: List[int]) -> str:
    """
    Bangun string baris waktu dengan angka sejajar boundary segmen.
    
    Args:
        timeline: Daftar segmen
        widths: Lebar segmen (sudah disesuaikan)
    
    Returns:
        String baris waktu
    """
    if not timeline:
        return ""
    
    # Hitung posisi boundary (index karakter di string output)
    # Border: "+" + "-"*w0 + "+" + "-"*w1 + "+" ...
    # Boundary 0 (karakter '+' kiri) = index 0
    # Boundary i = sum(widths[:i]) + i  (karena setiap '+' mengambil 1 posisi)
    boundaries = [0]
    
    for w in widths:
        # Boundary berikutnya = boundary sebelumnya + width + 1 (karakter '+')
        boundaries.append(boundaries[-1] + w + 1)
    
    # Label waktu: start_time pertama, lalu end_time setiap segmen
    labels = [str(timeline[0].start_time)] + [str(seg.end_time) for seg in timeline]
    
    # Bangun string dengan menempatkan label di posisi boundary
    # Gunakan list karakter untuk presisi
    max_pos = boundaries[-1] + max(len(l) for l in labels) + 2
    chars = [' '] * max_pos
    
    for idx, (boundary_pos, label) in enumerate(zip(boundaries, labels)):
        if idx == 0:
            # Label pertama (start_time): left-aligned di boundary 0
            start_pos = boundary_pos
        else:
            # Label berikutnya (end_time): center-aligned di boundary
            start_pos = boundary_pos - len(label) // 2
        
        for i, ch in enumerate(label):
            if 0 <= start_pos + i < max_pos:
                chars[start_pos + i] = ch
    
    # Trim trailing spaces
    while chars and chars[-1] == ' ':
        chars.pop()
    
    return ''.join(chars)


def display_gantt(timeline: List[ExecutionSegment]) -> None:
    """
    Menampilkan Text-Based Gantt Chart di terminal.

    Args:
        timeline: List[ExecutionSegment] - hasil dari run_fcfs() atau run_sjf_preemptive()
                  Setiap segmen memiliki pid, start_time, end_time
    """
    if not timeline:
        print("Gantt Chart: (kosong)")
        return

    # 1. Hitung lebar dasar setiap segmen
    base_widths = [
        _segment_width(seg.pid, seg.end_time - seg.start_time)
        for seg in timeline
    ]

    # 2. Sesuaikan lebar untuk label waktu (angka 3+ digit)
    widths = _adjust_widths_for_time_labels(timeline, base_widths)

    # 3. Render border atas/bawah
    print("Gantt Chart:")
    border = "+" + "+".join("-" * w for w in widths) + "+"
    print(border)

    # 4. Render baris PID (tengah)
    pid_row = "|" + "|".join(seg.pid.center(w) for seg, w in zip(timeline, widths)) + "|"
    print(pid_row)

    # 5. Render border bawah
    print(border)

    # 6. Render baris timeline numbers
    time_line = _build_time_line(timeline, widths)
    print(time_line)
