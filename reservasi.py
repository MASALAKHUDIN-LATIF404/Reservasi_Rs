from datetime import datetime
import time
import colorama # library colorama untuk style warna
from fungsi.core import load_data, clear_screen
from fungsi.autentikasi import *
from fungsi.admin import *
from fungsi.staff import *
from fungsi.user import *

"""
Fore → digunakan untuk memberi warna pada teks di terminal (foreground).
Style → digunakan untuk memberi gaya teks (kasus ini auto reset warna default)
"""
from colorama import Fore






#Fungsi Utama (Main Menu)
def main():
    colorama.init(autoreset=True) # untuk mengaktifkan colorama dan memastikan bahwa warna teks akan otomatis kembali normal setelah setiap perintah print, sehingga tidak semua teks di terminal menjadi merah.

    while True:
        # Setiap kali kembali ke menu utama, data dimuat ulang untuk memastikan sesi baru (jika login ulang) mendapat data segar.
        # data = load_data() # Tidak lagi diperlukan di sini karena setiap fungsi meload datanya sendiri
        print("\n=== Aplikasi Reservasi Rumah Sakit ===")
        print("1. Login")
        print("2. Register (Pengguna Biasa)")
        print("3. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            id_pengguna, username, peran, id_pasien = login()
            if id_pengguna: # Jika login berhasil (id_pengguna tidak None)
                clear_screen()
                if peran == 'admin':
                    menu_admin() # Tidak perlu mengoper data lagi
                elif peran == 'staff':
                    menu_staff() # Tidak perlu mengoper data lagi
                elif peran == 'user':
                    menu_user(username, id_pasien) # Tidak perlu mengoper data lagi
                else:
                    print(Fore.RED + "Peran tidak dikenali.")
            else:
                time.sleep(2)
                clear_screen()
        elif pilihan == '2':
            register()
        elif pilihan == '3':
            print("Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")
            time.sleep(1)
            clear_screen()

if __name__ == "__main__":
    main()