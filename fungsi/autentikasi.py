from datetime import datetime
import getpass
import time
from fungsi.core import *
from colorama import Fore
from fungsi.color import *

# --- Fungsi Login ---
def login(data):
    while True:
        print("\n--- Login ---")
        username = input("Username: ")
        password = getpass.getpass("Password: ") # Menggunakan getpass untuk input password tersembunyi

        user = data["users"].get(username)
        if user and user["password"] == password:
            print(f"\nLogin berhasil! Selamat datang, {username} (Role: {user['role']})")
            # Jika login berhasil, kembalikan ID pasien jika ada
            return user.get("id"), username, user.get("role"), user.get("patient_id")
        else:
            print(Fore.RED + "Username atau password salah. Silakan coba lagi.")
            # Kembalikan None jika login gagal
            return None, None, None, None

# --- Fungsi Register (Hanya untuk user biasa, role 'user') ---
def register(data):
    print("\n--- Register ---")
    username = input("Masukkan username baru: ")
    password = getpass.getpass("Masukkan password baru: ") # Menggunakan getpass untuk input password tersembunyi
    role = 'user' # Tetap sebagai 'user'
    name = input("Input nama lengkap: ")
    phone = input("Input nomor HP: ")
    address = input("Input alamat: ")
    tahun_lahir = input("Tahun lahir: ")
    bulan_lahir = input("Bulan lahir: ")
    tanggal_lahir = input("Tanggal lahir: ")

    if username in data["users"]:
        print(Fore.RED + "Username sudah digunakan. Silakan coba yang lain.")
    else:
        # Membuat ID baru yang unik dan berurutan
        max_user_id = 0
        for uinfo in data["users"].values():
            try:
                current_id = int(uinfo["id"])
                if current_id > max_user_id:
                    max_user_id = current_id
            except ValueError:
                # Abaikan jika 'id' bukan angka (misal: data lama yang tidak konsisten)
                pass
        user_id = str(max_user_id + 1)

        max_patient_id = 0
        for key, pinfo in data["patients"].items():
            try:
                current_id = int(key)
                if current_id > max_patient_id:
                    max_patient_id = current_id
            except ValueError:
                # Abaikan jika 'id' bukan angka (misal: data lama yang tidak konsisten)
                pass
        patient_id = str(max_patient_id + 1)

        data["users"][username] = {
            "id": user_id, 
            "password": password, 
            "role": role,
            "patient_id": patient_id  # Tautkan user baru ke patient_id baru
        }
        save_data(data)
        data["patients"][patient_id] = {
            "name": name,
            "phone": phone,
            "address": address,
            "birth_date": f"{tahun_lahir}-{bulan_lahir}-{tanggal_lahir}",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        save_data(data)

        print(f"{H}[🗸]Registrasi berhasil! Silakan login.{R}")
        time.sleep(3)
        clear_screen()
        # Kembali ke menu utama setelah registrasi