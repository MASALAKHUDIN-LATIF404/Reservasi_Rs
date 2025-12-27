from datetime import datetime
import getpass
import time
from fungsi.core import *
from colorama import Fore
from fungsi.color import *

#Fungsi Login
def login():
    while True:
        data = load_data()
        print("\n--- Login ---")
        username = input("Username: ")
        kata_sandi = getpass.getpass("Password: ") # Menggunakan getpass untuk input kata sandi tersembunyi

        pengguna = data["users"].get(username)
        if pengguna and pengguna["password"] == kata_sandi:
            print(f"\nLogin berhasil! Selamat datang, {username} (Role: {pengguna['role']})")
            # Jika login berhasil, kembalikan ID pasien jika ada
            return pengguna.get("id"), username, pengguna.get("role"), pengguna.get("id_pasien")
        else:
            print(Fore.RED + "Username atau password salah. Silakan coba lagi.")
            # Kembalikan None jika login gagal
            return None, None, None, None

#Fungsi Register (Hanya untuk pengguna biasa, peran 'user')
def register():
    data = load_data()
    print("\n--- Register ---")
    nama = input("Input nama lengkap: ")
    telepon = input("Input nomor HP: ")
    alamat = input("Input alamat: ")
    tahun_lahir = input("Tahun lahir: ")
    bulan_lahir = input("Bulan lahir: ")
    tanggal_lahir = input("Tanggal lahir: ")

    while True:
        username = input("masukkan username pengguna: ")
        if username in data["users"]:
            print(Fore.RED + "Username sudah digunakan. Silakan coba yang lain.")
        else:
            break

    kata_sandi = getpass.getpass("masukkan katasandi pengguna: ") 
    peran = 'user'

    # Membuat ID baru yang unik dan berurutan
    id_user_maks = 0
    for info_user in data["users"].values():
        try:
            id_saat_ini = int(info_user["id"])
            if id_saat_ini > id_user_maks:
                id_user_maks = id_saat_ini
        except ValueError:
            # Abaikan jika 'id' bukan angka (misal: data lama yang tidak konsisten)
            pass
    id_user = str(id_user_maks + 1)

    id_pasien_maks = 0
    for id_pasien_iter, info_pasien in data["pasien"].items():
        try:
            id_saat_ini = int(id_pasien_iter)
            if id_saat_ini > id_pasien_maks:
                id_pasien_maks = id_saat_ini
        except ValueError:
            # Abaikan jika 'id' bukan angka (misal: data lama yang tidak konsisten)
            pass
    id_pasien = str(id_pasien_maks + 1)

    data["users"][username] = {
        "id": id_user, 
        "password": kata_sandi, 
        "role": peran,
        "id_pasien": id_pasien  # Tautkan pengguna baru ke id_pasien baru
    }
    save_data(data)
    data["pasien"][id_pasien] = {
        "nama": nama,
        "telepon": telepon,
        "alamat": alamat,
        "tanggal_lahir": f"{tahun_lahir}-{bulan_lahir}-{tanggal_lahir}",
        "dibuat_pada": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    save_data(data)

    print(f"{H}[🗸]Registrasi berhasil! Silakan login.{R}")
    time.sleep(3)
    clear_screen()
        # Kembali ke menu utama setelah registrasi