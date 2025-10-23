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






# --- Fungsi Utama (Main Menu) ---
def main():
    colorama.init(autoreset=True) # untuk mengaktifkan colorama dan autoreset=True memastikan bahwa warna teks akan otomatis kembali normal setelah setiap perintah print, sehingga tidak semua teks di terminal menjadi merah.

    data = load_data()

    while True:
        print("\n=== Aplikasi Reservasi Rumah Sakit ===")
        print("1. Login")
        print("2. Register (User Biasa)")
        print("3. Keluar")
        choice = input("Pilih menu: ")

        if choice == '1':
            user_id, username, role, patient_id = login(data)
            if user_id: # Jika login berhasil (user_id tidak None)
                clear_screen()
                if role == 'admin':
                    menu_admin(data)
                elif role == 'staff':
                    menu_staff(data)
                elif role == 'user':
                    menu_user(data, username, patient_id) # Teruskan patient_id
                else:
                    print(Fore.RED + "Role tidak dikenali.")
            else:
                time.sleep(2)
                clear_screen()
        elif choice == '2':
            register(data)
        elif choice == '3':
            print("Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")
            time.sleep(1)
            clear_screen()

if __name__ == "__main__":
    main()