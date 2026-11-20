"""
OS-SIMULATOR - Entry Point
Simulator Penjadwalan CPU & Manajemen Alokasi Memori Dinamis Berbasis CLI
UTS Sistem Operasi - Project Individu
"""

def main() -> None:
    from src.interface.menu import run_menu
    run_menu()

if __name__ == "__main__":
    main()
