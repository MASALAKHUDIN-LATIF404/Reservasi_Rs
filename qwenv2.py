import json
import os
from datetime import datetime
import getpass
import time
import colorama # library colorama untuk style warna

"""
Fore → digunakan untuk memberi warna pada teks di terminal (foreground).
Style → digunakan untuk memberi gaya teks (kasus ini auto reset warna default)
"""
from colorama import Fore, Style # mengimpor 2 objek Fore, Style dari colorama.


#---- Kumpulan code warna ----#
H = "\033[92m" # warna hijau
M = "\033[91m" # warna merah
R = "\033[0m" # reset warna



DATA_FILE = "hospital_data_extended.json"


# sebuah fungsi untuk membersihkan layar terminal
def clear_screen():
    os_name = os.name # untuk mendeteksi nama sistem operasi yang digunakan ('nt' = Windows, 'posix' = Linux/Mac)
    if os_name == 'nt': # Jika sistem operasi terdeteksi Windows
        os.system('cls') # Otomatis jalankan perintah 'cls' untuk membersihkan layar terminal di Windows
    else: # Jika sistem operasi terdeteksi Linux/Mac
        os.system('clear') # Otomatis jalankan perintah 'clear' untuk membersihkan layar terminal di Linux/Mac


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(Fore.RED + "File data rusak, menggunakan data kosong.") # Fore.RED + di depan string. Ini memberitahu terminal untuk mencetak teks tersebut dengan warna merah.
                return get_default_data_structure()
    else:
        return get_default_data_structure()

def get_default_data_structure():
    return {
        "users": {
            "admin": {"id": "1", "password": "adminpass", "role": "admin"},
            "staff": {"id": "2", "password": "staffpass", "role": "staff"}
        },
        "departments": {
            "1": {"name": "Penyakit Dalam"},
            "2": {"name": "Bedah"},
            "3": {"name": "Anak"},
            "4": {"name": "Kandungan"}
        },
        "doctors": {
            "1": {"name": "Dr. Ahmad", "specialty_id": "1", "phone": "081234567890"},
            "2": {"name": "Dr. Siti", "specialty_id": "2", "phone": "081234567891"},
            "3": {"name": "Dr. Budi", "specialty_id": "3", "phone": "081234567892"}
        },
        "rooms": {
            "1": {"name": "Melati 101", "type": "VIP", "is_available": True},
            "2": {"name": "Anggrek 202", "type": "Kelas 1", "is_available": True},
            "3": {"name": "Mawar 303", "type": "Kelas 2", "is_available": False}
        },
        "patients": {},
        "schedules": {},
        "appointments": {},
        "checkups": {},
        "admissions": {} # Rawat Inap
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Fungsi Login ---
def login(data):
    while True:
        print("\n--- Login ---")
        username = input("Username: ")
        password = getpass.getpass("Password: ") # Menggunakan getpass untuk input password tersembunyi

        user = data["users"].get(username)
        if user and user["password"] == password:
            print(f"\nLogin berhasil! Selamat datang, {username} (Role: {user['role']})")
            return user["id"], username, user["role"]
        else:
            print(Fore.RED + "Username atau password salah. Silakan coba lagi.")
            time.sleep(3) # untuk memberi jeda 2 detik sebelum reset layar (clear)
            clear_screen() # fungsi reset (clear terminal)
            main() # mengembalikan ke funsgi menu utama

# --- Fungsi Register (Hanya untuk user biasa, role 'user') ---
def register(data):
    print("\n--- Register ---")
    username = input("Masukkan username baru: ")
    password = getpass.getpass("Masukkan password baru: ") # Menggunakan getpass untuk input password tersembunyi
    role = 'user' # Tetap sebagai 'user'

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

        data["users"][username] = {"id": user_id, "password": password, "role": role}
        save_data(data)
        print(f"{H}[🗸]Registrasi berhasil! Silakan login.{R}")
        time.sleep(3)
        clear_screen()

# --- Menu Admin ---
def menu_admin(data):
    while True:
        print(f"\n--- {H}Menu Admin{R} ---\n")
        print("1. Manajemen User")
        print("2. Manajemen Departemen")
        print("3. Manajemen Dokter")
        print("4. Manajemen Ruangan")
        print("5. Laporan Sederhana")
        print("0. Logout Admin")
        choice = input("Pilih menu: ")

        if choice == '1':
            clear_screen()
            manajemen_user(data)
        elif choice == '2':
            clear_screen()
            manajemen_departemen(data)
        elif choice == '3':
            clear_screen()
            manajemen_dokter(data)
        elif choice == '4':
            clear_screen()
            manajemen_ruangan(data)
        elif choice == '5':
            clear_screen()
            laporan_sederhana(data)
        elif choice == '0':
            confirm = input("Apakah Anda Yakin Ingin Logout? [Y/N] : ").lower()
            if confirm == 'y':
                print(f"{H}[🗸] Logout berhasil.{R}")
                time.sleep(2)
                clear_screen()
                break
            else:
                print(f"{H}[🗸] Logout dibatalkan.{R}")
                time.sleep(2)
                clear_screen()
        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")
            time.sleep(3)
            clear_screen()



# --- Menu Staff ---
def menu_staff(data):
    while True:
        print(f"\n--- {H}Menu Staff{R} ---")
        print("1. Data Pasien")
        print("2. Data Jadwal")
        print("3. Data Janji")
        print("4. Buat Janji")
        print("5. Data CheckUp")
        print("6. Data Rawat Inap")
        print("0. Logout Menu Staff")
        choice = input("Pilih menu: ")

        if choice == '1':
            clear_screen()
            data_pasien(data)
        elif choice == '2':
            clear_screen()
            data_jadwal(data)
        elif choice == '3':
            clear_screen()
            data_janji(data)
        elif choice == '4':
            clear_screen()
            buat_janji(data)
        elif choice == '5':
            clear_screen()
            data_checkup(data)
        elif choice == '6':
            clear_screen()
            data_rawat_inap(data)
        elif choice == '0':
            confirm = input("Apakah Anda Yakin Ingin Logout Menu Staff? [Y/N] : ").lower()
            if confirm == 'y':
                clear_screen()
                break
            else:
                print(f"{H}[🗸] Aksi dibatalkan.")
                time.sleep(2)
                clear_screen()
        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")
            time.sleep(3)
            clear_screen()



# --- Menu User Biasa ---
def menu_user(data, current_username):
    while True:
        print(f"\n--- Menu User ({H}{current_username}{R}) ---")
        print("1. Lihat Jadwal Tersedia")
        print("2. Buat Janji Saya")
        print("3. Lihat Janji Saya")
        print("4. Lihat Riwayat Kesehatan Saya")
        print("0. Kembali ke Menu Utama")
        choice = input("Pilih menu: ")

        if choice == '1':
            clear_screen()
            lihat_jadwal_tersedia(data)
        elif choice == '2':
            clear_screen()
            buat_janji_user(data, current_username) # Perlu fungsi baru
        elif choice == '3':
            clear_screen()
            lihat_janji_user(data, current_username)
        elif choice == '4':
            clear_screen()
            lihat_riwayat_user(data, current_username)
        elif choice == '0':
            confirm = input("Apakah Anda Yakin Ingin Kembali ke Menu Utama? [Y/N] : ").lower()
            if confirm == 'y':
                clear_screen()
                break
            else:
                print("Aksi dibatalkan.")
                time.sleep(2)
                clear_screen()
        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")
            time.sleep(3)
            clear_screen()


# --- Fungsi Lihat Jadwal Tersedia (untuk User) ---
def lihat_jadwal_tersedia(data):
    print("\n--- Jadwal Dokter Tersedia ---")
    # Filter hanya jadwal yang tersedia
    available_schedules = {sid: sinfo for sid, sinfo in data["schedules"].items() if sinfo.get("is_available", True)}
    if not available_schedules:
        print(Fore.YELLOW + "Tidak ada jadwal yang tersedia saat ini.")
        return

    # Tampilkan dengan detail dokter dan departemen
    print(f"{H}Daftar Jadwal Tersedia:{R}")
    for sid, sinfo in available_schedules.items():
        doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
        dept_info = data["departments"].get(doctor_info["specialty_id"], {"name": "Tidak Ditemukan"})
        print(f"ID Jadwal: {sid}, Dokter: {doctor_info['name']}, Departemen: {dept_info['name']}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}")

# --- Fungsi Buat Janji (untuk User) ---
def buat_janji_user(data, current_username):
    print("\n--- Buat Janji Saya ---")
    # Cari ID pasien berdasarkan username (asumsi username = nama pasien atau terkait)
    patient_id = None
    for pid, pinfo in data["patients"].items():
        if pinfo["name"].lower() == current_username.lower():
            patient_id = pid
            break

    if not patient_id:
        print(Fore.RED + f"Anda ({current_username}) belum terdaftar sebagai pasien. Silakan daftar dulu atau hubungi staff.")
        return

    # Tampilkan jadwal yang tersedia
    available_schedules = {sid: sinfo for sid, sinfo in data["schedules"].items() if sinfo.get("is_available", True)}
    if not available_schedules:
        print(Fore.YELLOW + "Tidak ada jadwal yang tersedia saat ini.")
        return

    print(f"{H}Daftar Jadwal Tersedia:{R}")
    for sid, sinfo in available_schedules.items():
        doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": Fore.RED + "Tidak Ditemukan"})
        dept_info = data["departments"].get(doctor_info["specialty_id"], {"name": "Tidak Ditemukan"})
        print(f"ID Jadwal: {sid}, Dokter: {doctor_info['name']}, Departemen: {dept_info['name']}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}")
    
    schedule_id = input("\nMasukkan ID Jadwal yang dipilih: ")
    if schedule_id not in available_schedules:
        print(Fore.RED + "ID Jadwal tidak valid atau sudah dipesan.")
        return

    # Buat Janji
    appointment_id = str(len(data["appointments"]) + 1)
    data["appointments"][appointment_id] = {
        "patient_id": patient_id,
        "schedule_id": schedule_id,
        "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Scheduled"
    }
    data["schedules"][schedule_id]["is_available"] = False
    save_data(data)
    print(f"{H}[🗸] Janji berhasil dibuat untuk Anda!{R}")

# --- Fungsi Lihat Janji Saya (untuk User) ---
def lihat_janji_user(data, current_username):
    print("\n--- Janji Saya ---")
    # Cari ID pasien
    patient_id = None
    for pid, pinfo in data["patients"].items():
        if pinfo["name"].lower() == current_username.lower():
            patient_id = pid
            break

    if not patient_id:
        print(Fore.RED + "Anda belum terdaftar sebagai pasien.")
        return

    user_appointments = {aid: ainfo for aid, ainfo in data["appointments"].items() if ainfo["patient_id"] == patient_id}
    if not user_appointments:
        print(Fore.YELLOW + "Anda belum memiliki janji temu.")
        return

    print(f"{H}Daftar Janji Anda:{R}")
    for aid, ainfo in user_appointments.items():
        sinfo = data["schedules"].get(ainfo["schedule_id"], {"doctor_id": "Tidak Ditemukan"})
        doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
        dept_info = data["departments"].get(doctor_info["specialty_id"], {"name": "Tidak Ditemukan"})
        print(f"ID Janji: {aid}, Dokter: {doctor_info['name']}, Departemen: {dept_info['name']}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}, Status: {H}{ainfo['status']}{R}")

# --- Fungsi Lihat Riwayat Kesehatan Saya (untuk User) ---
def lihat_riwayat_user(data, current_username):
    print("\n--- Riwayat Kesehatan Saya ---")
    # Cari ID pasien
    patient_id = None
    for pid, pinfo in data["patients"].items():
        if pinfo["name"].lower() == current_username.lower():
            patient_id = pid
            break

    if not patient_id:
        print(Fore.RED + "Anda belum terdaftar sebagai pasien.")
        return

    # Cari janji pasien
    patient_appointments = [aid for aid, ainfo in data["appointments"].items() if ainfo["patient_id"] == patient_id]

    if not patient_appointments:
        print(Fore.YELLOW + "Anda belum memiliki riwayat janji.")
        return

    print(f"{H}Riwayat Pemeriksaan:{R}")
    for aid in patient_appointments:
        # Cari data checkup terkait
        checkup_found = False
        for cid, cinfo in data["checkups"].items():
            if cinfo["appointment_id"] == aid:
                ainfo = data["appointments"][aid]
                sinfo = data["schedules"].get(ainfo["schedule_id"], {"doctor_id": "Tidak Ditemukan"})
                doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                print(f"ID Janji: {aid}, Tanggal Checkup: {cinfo['checkup_date']}, Dokter: {doctor_info['name']}")
                print(f"  Diagnosis: {H}{cinfo['diagnosis']}{R}")
                print(f"  Catatan: {H}{cinfo['notes']}{R}")
                checkup_found = True
                break
        if not checkup_found:
            print(Fore.YELLOW + f"ID Janji: {aid} - Belum ada data pemeriksaan.")


# --- Fungsi Manajemen User (Admin) ---
def manajemen_user(data):
    while True:
        print(f"\n--- Manajemen User ({H}Admin{R}) ---") # f-string H & R untuk kode warna
        print("1. Lihat Semua User")
        print("2. Tambah User")
        print("3. Edit User")
        print("4. Hapus User")
        print("0. Kembali ke Menu Admin")
        choice = input("Pilih menu: ")

        if choice == '1':
            print(f"\n{H}Daftar User:")
            for uname, uinfo in data["users"].items():
                print(f"Username: {uname}, ID: {uinfo['id']}, Role: {uinfo['role']}")
        elif choice == '2':
            username = input("Username Baru: ")
            password = input("Password Baru: ")
            role = input("Role (admin/staff/user): ")
            if role not in ['admin', 'staff', 'user']:
                print(Fore.RED + "Role tidak valid.")
                time.sleep(3)
                clear_screen()
                continue
            if username in data["users"]:
                print(Fore.RED + "Username sudah digunakan.")
                continue
            
            # Membuat ID baru yang unik dan berurutan
            max_user_id = 0
            for uinfo in data["users"].values():
                try:
                    current_id = int(uinfo["id"])
                    if current_id > max_user_id:
                        max_user_id = current_id
                except ValueError:
                    # Abaikan jika 'id' bukan angka
                    pass
            user_id = str(max_user_id + 1)

            data["users"][username] = {"id": user_id, "password": password, "role": role}
            save_data(data)
            print(f"{H}[🗸] User berhasil ditambahkan.{R}")
            time.sleep(3)
            clear_screen() # Membersihkan layar setelah penambahan
        elif choice == '3':
            print(f"\n{H}Daftar User:")
            for uname, uinfo in data["users"].items():
                print(f"Username: {uname}, ID: {uinfo['id']}, Role: {uinfo['role']}")
            username = input("Username yang akan diedit: ")
            if username not in data["users"]:
                print(Fore.RED + "Username tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            uinfo = data["users"][username]
            print(f"Data saat ini: Username: {username}, ID: {uinfo['id']}, Role: {uinfo['role']}")
            new_role = input(f"Role Baru (sekarang: {uinfo['role']}): ") or uinfo['role']
            if new_role not in ['admin', 'staff', 'user']:
                print("Role tidak valid.")
                time.sleep(3)
                clear_screen()
                continue
            new_password = input("Password Baru (tekan Enter jika tidak ingin diganti): ")
            if new_password:
                data["users"][username]["password"] = new_password
            data["users"][username]["role"] = new_role
            save_data(data)
            print(f"{H}[🗸] User berhasil diubah.{R}")
            time.sleep(3)
            clear_screen()
        elif choice == '4':
            print(f"\n{H}Daftar User:")
            for uname, uinfo in data["users"].items():
                print(f"Username: {uname}, ID: {uinfo['id']}, Role: {uinfo['role']}")
            username = input("Username yang akan dihapus: ")
            if username == 'admin': # Proteksi akun admin default
                print(Fore.RED + "Tidak bisa menghapus akun admin default.")
                time.sleep(3)
                clear_screen()
                continue
            if username in data["users"]:
                # Hapus user yang dipilih
                del data["users"][username]

                # --- Logika untuk mengurutkan ulang ID ---
                new_users = {}
                # Urutkan berdasarkan username untuk konsistensi saat re-indexing
                sorted_user_items = sorted(data["users"].items())

                for i, (uname, uinfo) in enumerate(sorted_user_items):
                    new_id = str(i + 1)
                    uinfo["id"] = new_id # Perbarui ID di dalam objek user
                    new_users[uname] = uinfo
                
                # Ganti dictionary users lama dengan yang baru
                data["users"] = new_users

                save_data(data)
                print(f"{H}[🗸] User berhasil dihapus dan ID telah diurutkan ulang.{R}")
                time.sleep(3)
                clear_screen()
            else:
                print(Fore.RED + "Username tidak ditemukan.")
                time.sleep(3)
                clear_screen()
        elif choice == '0':
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()



# --- Fungsi Manajemen Departemen (Admin) ---
def manajemen_departemen(data):
    while True:
        print(f"\n--- Manajemen Departemen ({H}Admin{R}) ---")
        print("1. Lihat Semua Departemen")
        print("2. Tambah Departemen")
        print("3. Edit Departemen")
        print("4. Hapus Departemen")
        print("0. Kembali ke Menu Admin")
        choice = input("Pilih menu: ")

        if choice == '1':
            print(f"\n{H}Daftar Departemen:{R}")
            for did, dinfo in data["departments"].items():
                print(f"ID: {did}, Nama: {dinfo['name']}")
        elif choice == '2':
            name = input("Nama Departemen Baru: ").strip()
            if not name:
                print(Fore.RED + "Nama departemen tidak boleh kosong.")
                time.sleep(3)
                clear_screen()
                continue
            dept_id = str(len(data["departments"]) + 1)
            data["departments"][dept_id] = {"name": name}
            save_data(data)
            print(f"{H}[🗸] Departemen berhasil ditambahkan.{R}")
            time.sleep(3)
            clear_screen()
        elif choice == '3':
            print(f"\n{H}Daftar Departemen:{R}")
            for did, dinfo in data["departments"].items():
                print(f"ID: {did}, Nama: {dinfo['name']}")
            dept_id = input("ID Departemen yang akan diedit: ").strip() # Menambahkan .strip()
            if dept_id not in data["departments"]:
                print(Fore.RED + "ID Departemen tidak ditemukan.")
                time.sleep(3) # Menambahkan jeda waktu
                clear_screen()
                continue
            dinfo = data["departments"][dept_id]
            print(f"\nData saat ini: ID: {dept_id}, Nama: {dinfo['name']}")
            new_name = input(f"Nama Baru (sekarang: {dinfo['name']}): ").strip()
            if not new_name:
                print(Fore.RED + "Nama departemen tidak boleh kosong. Pembatalan edit.")
                time.sleep(3)
                clear_screen()
                continue
            data["departments"][dept_id]["name"] = new_name
            save_data(data)
            print(f"{H}[🗸] Departemen berhasil diubah.{R}")
            time.sleep(3)
            clear_screen()
        elif choice == '4':
            print(f"\n{H}Daftar Departemen:{R}")
            for did, dinfo in data["departments"].items():
                print(f"ID: {did}, Nama: {dinfo['name']}")
            dept_id = input("ID Departemen yang akan dihapus: ").strip()
            if dept_id not in data["departments"]:
                print(Fore.RED + "ID Departemen tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            # Cek apakah ada dokter di departemen ini
            doctors_in_dept = [doc_id for doc_id, doc_info in data["doctors"].items() if doc_info["specialty_id"] == dept_id]
            if doctors_in_dept:
                print(Fore.RED + f"Departemen '{data['departments'][dept_id]['name']}' masih memiliki dokter ({len(doctors_in_dept)}). Hapus dokter terlebih dahulu.")
                continue
            
            # Hapus departemen yang dipilih
            del data["departments"][dept_id]

            # --- Logika untuk mengurutkan ulang ID ---
            # 1. Buat dictionary departemen baru dan peta ID
            new_departments = {}
            id_map = {}
            # Urutkan berdasarkan ID numerik untuk konsistensi
            sorted_old_ids = sorted(data["departments"].keys(), key=int)

            for i, old_id in enumerate(sorted_old_ids):
                new_id = str(i + 1)
                new_departments[new_id] = data["departments"][old_id]
                if old_id != new_id:
                    id_map[old_id] = new_id
            
            # 2. Ganti dictionary departemen lama dengan yang baru
            data["departments"] = new_departments

            # 3. Perbarui referensi 'specialty_id' di data dokter
            for doc_info in data["doctors"].values():
                if doc_info["specialty_id"] in id_map:
                    doc_info["specialty_id"] = id_map[doc_info["specialty_id"]]

            save_data(data)
            print(f"{H}[🗸] Departemen berhasil dihapus dan ID telah diurutkan ulang.{R}")
            time.sleep(3)
            clear_screen()
        elif choice == '0':
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()


# --- Fungsi Manajemen Dokter (Admin) ---
def manajemen_dokter(data):
    while True:
        print(f"\n--- Manajemen Dokter ({H}Admin{R}) ---")
        print("1. Lihat Semua Dokter")
        print("2. Tambah Dokter")
        print("3. Edit Dokter")
        print("4. Hapus Dokter")
        print("0. Kembali ke Menu Admin")
        choice = input("Pilih menu: ")

        if choice == '1':
            print(f"\n{H}Daftar Dokter:{R}")
            for doc_id, doc_info in data["doctors"].items():
                dept_name = data["departments"].get(doc_info["specialty_id"], {"name": "Tidak Ditemukan"})["name"]
                print(f"ID: {doc_id}, Nama: {doc_info['name']}, Departemen: {dept_name}, Telp: {doc_info['phone']}")
        elif choice == '2':
            name = input("Nama Dokter Baru: ").strip()
            if not name:
                print(Fore.RED + "Nama dokter tidak boleh kosong.")
                time.sleep(3)
                clear_screen()
                continue

            phone = input("Nomor Telepon: ").strip()
            if not phone:
                print(Fore.RED + "Nomor telepon tidak boleh kosong.")
                time.sleep(3)
                clear_screen()
                continue

            print(f"\n{H}Pilih Daftar Kategori Departemen Dokter Baru:{R}")
            for did, dinfo in data["departments"].items():
                print(f"ID: {did}, Nama: {dinfo['name']}")
            specialty_id = input("Pilih ID Departemen: ").strip()
            if specialty_id not in data["departments"]:
                print(Fore.RED + "ID Departemen tidak valid atau tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            
            # Membuat ID baru yang lebih andal
            doc_id = str(max([int(k) for k in data["doctors"].keys()] or [0]) + 1)
            data["doctors"][doc_id] = {"name": name, "specialty_id": specialty_id, "phone": phone}
            save_data(data)
            print(f"{H}[🗸] Dokter berhasil ditambahkan.{R}")
            time.sleep(3)
            clear_screen()
        elif choice == '3':
            print(f"\n{H}Daftar Dokter:{R}")
            for doc_id, doc_info in data["doctors"].items():
                dept_name = data["departments"].get(doc_info["specialty_id"], {"name": "Tidak Ditemukan"})["name"]
                print(f"ID: {doc_id}, Nama: {doc_info['name']}, Departemen: {dept_name}, Telp: {doc_info['phone']}")
            doc_id = input("ID Dokter yang akan diedit: ")
            if doc_id not in data["doctors"]:
                print(Fore.RED + "ID Dokter tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            doc_info = data["doctors"][doc_id]
            dept_name = data["departments"].get(doc_info["specialty_id"], {"name": "Tidak Ditemukan"})["name"]
            print(f"Data saat ini: ID: {doc_id}, Nama: {doc_info['name']}, Departemen: {dept_name}, Telp: {doc_info['phone']}")
            new_name = input(f"Nama Baru (sekarang: {doc_info['name']}): ") or doc_info['name']
            new_phone = input(f"Telp Baru (sekarang: {doc_info['phone']}): ") or doc_info['phone']
            print(f"\n{H}Daftar Departemen:{R}")
            for did, dinfo in data["departments"].items():
                print(f"ID: {did}, Nama: {dinfo['name']}")
            new_spec_id = input(f"ID Departemen Baru (sekarang: {doc_info['specialty_id']}): ") or doc_info['specialty_id']
            if new_spec_id not in data["departments"]:
                print(Fore.RED + "ID Departemen tidak ditemukan.")
                clear_screen()
                continue
            data["doctors"][doc_id] = {"name": new_name, "specialty_id": new_spec_id, "phone": new_phone}
            save_data(data)
            print(f"{H}[🗸] Dokter berhasil diubah.{R}")
            time.sleep(3)
            clear_screen()
        elif choice == '4':
            print(f"\n{H}Daftar Dokter:{R}")
            for doc_id, doc_info in data["doctors"].items():
                dept_name = data["departments"].get(doc_info["specialty_id"], {"name": "Tidak Ditemukan"})["name"]
                print(f"ID: {doc_id}, Nama: {doc_info['name']}, Departemen: {dept_name}, Telp: {doc_info['phone']}")
            doc_id = input("ID Dokter yang akan dihapus: ").strip()
            if doc_id not in data["doctors"]:
                print(Fore.RED + "ID Dokter tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            # Cek apakah ada jadwal aktif untuk dokter ini
            schedules_for_doc = [sid for sid, sinfo in data["schedules"].items() if sinfo["doctor_id"] == doc_id]
            if schedules_for_doc:
                print(Fore.RED + f"Dokter '{data['doctors'][doc_id]['name']}' masih memiliki jadwal aktif. Hapus jadwal terlebih dahulu.")
                continue
            
            # Hapus dokter yang dipilih
            del data["doctors"][doc_id]

            # --- Logika untuk mengurutkan ulang ID ---
            # 1. Buat dictionary dokter baru dan peta ID
            new_doctors = {}
            id_map = {}
            # Urutkan berdasarkan ID numerik untuk konsistensi
            sorted_old_ids = sorted(data["doctors"].keys(), key=int)

            for i, old_id in enumerate(sorted_old_ids):
                new_id = str(i + 1)
                new_doctors[new_id] = data["doctors"][old_id]
                if old_id != new_id:
                    id_map[old_id] = new_id
            
            # 2. Ganti dictionary dokter lama dengan yang baru
            data["doctors"] = new_doctors

            # 3. Perbarui referensi di 'schedules' (jadwal)
            for schedule_id, schedule_info in data["schedules"].items():
                if schedule_info["doctor_id"] in id_map:
                    schedule_info["doctor_id"] = id_map[schedule_info["doctor_id"]]

            save_data(data)
            print(f"{H}[🗸] Dokter berhasil dihapus dan ID telah diurutkan ulang.{R}")
            time.sleep(3)
            clear_screen()
        elif choice == '0':
            clear_screen()
            menu_admin(data)
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()



# --- Fungsi Manajemen Ruangan (Admin) ---
def manajemen_ruangan(data):
    while True:
        print(f"\n--- Manajemen Ruangan ({H}Admin{R}) ---")
        print("1. Lihat Semua Ruangan")
        print("2. Tambah Ruangan")
        print("3. Edit Ruangan")
        print("4. Hapus Ruangan")
        print("0. Kembali ke Menu Admin")
        choice = input("Pilih menu: ")

        if choice == '1':
            print(f"\n{H}Daftar Ruangan:{R}")
            for rid, rinfo in data["rooms"].items():
                status = "Tersedia" if rinfo.get("is_available", True) else "Tidak Tersedia"
                print(f"ID: {rid}, Nama: {rinfo['name']}, Tipe: {rinfo['type']}, Status: {status}")
        elif choice == '2':
            name = input("Nama Ruangan Baru: ").strip()
            if not name:
                print(Fore.RED + "Nama ruangan tidak boleh kosong.")
                time.sleep(3)
                clear_screen()
                continue

            type_room = input("Tipe Ruangan (VIP/Kelas 1/Kelas 2/Kelas 3): ").strip()
            if not type_room:
                print(Fore.RED + "Tipe ruangan tidak boleh kosong.")
                time.sleep(3)
                clear_screen()
                continue

            # Membuat ID baru yang lebih andal
            room_id = str(max([int(k) for k in data["rooms"].keys()] or [0]) + 1)
            data["rooms"][room_id] = {"name": name, "type": type_room, "is_available": True}
            save_data(data)
            print(f"{H}[🗸] Ruangan berhasil ditambahkan.{R}")
            time.sleep(3)
            clear_screen()
        elif choice == '3':
            print(f"\n{H}Daftar Ruangan:{R}")
            for rid, rinfo in data["rooms"].items():
                status = "Tersedia" if rinfo.get("is_available", True) else "Tidak Tersedia"
                print(f"ID: {rid}, Nama: {rinfo['name']}, Tipe: {rinfo['type']}, Status: {status}")
            room_id = input("ID Ruangan yang akan diedit: ").strip()
            if not room_id:
                print(Fore.RED + "ID Ruangan tidak boleh kosong.")
                time.sleep(3)
                clear_screen()
                continue
            if room_id not in data["rooms"]:
                print(Fore.RED + "ID Ruangan tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            rinfo = data["rooms"][room_id]
            print(f"Data saat ini: ID: {room_id}, Nama: {rinfo['name']}, Tipe: {rinfo['type']}, Tersedia: {rinfo.get('is_available', True)}")
            new_name = input(f"Nama Baru (sekarang: {rinfo['name']}): ") or rinfo['name']
            new_type = input(f"Tipe Baru (sekarang: {rinfo['type']}): ") or rinfo['type']
            # Tidak mengedit is_available di sini, karena statusnya tergantung pada rawat inap
            data["rooms"][room_id] = {"name": new_name, "type": new_type, "is_available": rinfo.get('is_available', True)}
            save_data(data)
            print(f"{H}[🗸] Ruangan berhasil diubah.{R}")
            time.sleep(3)
            clear_screen()
        elif choice == '4':
            print(f"\n{H}Daftar Ruangan:{R}")
            for rid, rinfo in data["rooms"].items():
                status = "Tersedia" if rinfo.get("is_available", True) else "Tidak Tersedia"
                print(f"ID: {rid}, Nama: {rinfo['name']}, Tipe: {rinfo['type']}, Status: {status}")
            room_id = input("ID Ruangan yang akan dihapus: ")
            if room_id not in data["rooms"]:
                print(Fore.RED + "ID Ruangan tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            rinfo = data["rooms"][room_id]
            if not rinfo.get("is_available", True): # Jika tidak tersedia, berarti sedang digunakan
                print(Fore.RED + f"Ruangan '{rinfo['name']}' sedang digunakan (tidak tersedia). Hapus data rawat inap terlebih dahulu.")
                continue
            
            # Hapus ruangan yang dipilih
            del data["rooms"][room_id]

            # --- Logika untuk mengurutkan ulang ID ---
            # 1. Buat dictionary ruangan baru dan peta ID
            new_rooms = {}
            id_map = {}
            # Urutkan berdasarkan ID numerik untuk konsistensi
            sorted_old_ids = sorted(data["rooms"].keys(), key=int)
            
            for i, old_id in enumerate(sorted_old_ids):
                new_id = str(i + 1)
                new_rooms[new_id] = data["rooms"][old_id]
                if old_id != new_id:
                    id_map[old_id] = new_id
            
            # 2. Ganti dictionary ruangan lama dengan yang baru
            data["rooms"] = new_rooms

            # 3. Perbarui referensi di 'admissions' (rawat inap)
            for admission_id, admission_info in data["admissions"].items():
                if admission_info["room_id"] in id_map:
                    admission_info["room_id"] = id_map[admission_info["room_id"]]
            
            save_data(data)
            print(f"{H}[🗸] Ruangan berhasil dihapus.{R}")
            time.sleep(3)
            clear_screen()
        elif choice == '0':
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()



# --- Fungsi Laporan Sederhana (Admin) ---
def laporan_sederhana(data):
    print(f"\n--- Laporan Sederhana ({H}Admin{R}) ---")
    print("1. Laporan Janji Harian")
    print("2. Laporan Pasien per Departemen")
    print("3. Laporan Ruangan Tersedia")
    sub_choice = input("Pilih laporan: ")

    if sub_choice == '1':
        date = input("Masukkan Tanggal (YYYY-MM-DD): ")
        print(f"\n{H}Laporan Janji untuk Tanggal:{R} {date}")
        found = False
        for aid, ainfo in data["appointments"].items():
            sinfo = data["schedules"].get(ainfo["schedule_id"], {})
            if sinfo.get("available_date") == date:
                found = True
                pinfo = data["patients"].get(ainfo["patient_id"], {"name": "Tidak Ditemukan"})
                doc_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                print(f"ID Janji: {aid}, Pasien: {pinfo['name']}, Dokter: {doc_info['name']}, Status: {H}{ainfo['status']}{R}")
        if not found:
            print(Fore.YELLOW + "Tidak Ada data Laporan Janji harian")
            time.sleep(3)
            clear_screen()
    elif sub_choice == '2':
        print(f"\n{H}Laporan Jumlah Pasien per Departemen:{R}")
        dept_counts = {}
        for aid, ainfo in data["appointments"].items():
            sinfo = data["schedules"].get(ainfo["schedule_id"], {})
            doc_info = data["doctors"].get(sinfo["doctor_id"], {})
            dept_id = doc_info.get("specialty_id")
            if dept_id:
                dept_name = data["departments"].get(dept_id, {"name": "Tidak Ditemukan"})["name"]
                dept_counts[dept_name] = dept_counts.get(dept_name, 0) + 1
        if not dept_counts:
            print(Fore.YELLOW + "Tidak Ada data Laporan Pasien per Departemen")
            time.sleep(3)
            clear_screen()
        else:
            for dept_name, count in dept_counts.items():
                print(f"Departemen: {dept_name}, Jumlah Pasien: {count}")
    elif sub_choice == '3':
        print(f"\n{H}Laporan Ruangan Tersedia:{R}")
        available_rooms = [rinfo for rinfo in data["rooms"].values() if rinfo.get("is_available", True)]
        if not available_rooms:
            print(Fore.YELLOW + "Tidak ada ruangan yang tersedia saat ini.")
        else:
            for rinfo in available_rooms:
                print(f"Nama: {rinfo['name']}, Tipe: {rinfo['type']}")
    else:
        print(Fore.RED + "Pilihan tidak valid.")
        time.sleep(3)
        clear_screen()



# --- Fungsi Data Pasien (Staff) ---
def data_pasien(data):
    while True:
        print(f"\n--- Data Pasien ({H}Staff{R}) ---")
        print("1. Lihat Semua Pasien")
        print("2. Tambah Pasien Baru")
        print("3. Edit Pasien")
        print("4. Hapus Pasien")
        print("0. Kembali ke Menu Staff")
        choice = input("Pilih menu: ")

        if choice == '1':
            if not data["patients"]:
                print(Fore.YELLOW + "\nBelum ada data pasien.")
                time.sleep(3)
                clear_screen()
            else:
                print(f"\n{H}Daftar Pasien:{R}")
                for pid, pinfo in data["patients"].items():
                    print(f"ID: {pid}, Nama: {pinfo['name']}, Telp: {pinfo['phone']}, Alamat: {pinfo['address']}, Tanggal Lahir: {pinfo['birth_date']}")
        elif choice == '2':
            name = input("Nama Pasien: ")
            phone = input("Nomor Telepon: ")
            address = input("Alamat: ")
            birth_date = input("Tanggal Lahir (YYYY-MM-DD): ")
            patient_id = str(len(data["patients"]) + 1)
            data["patients"][patient_id] = {
                "name": name,
                "phone": phone,
                "address": address,
                "birth_date": birth_date,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_data(data)
            print(f"{H}[🗸] Data pasien berhasil ditambahkan.{R}")
            time.sleep(4)
            clear_screen()
        elif choice == '3':
            print(f"\n{H}Daftar Pasien:{R}")
            for pid, pinfo in data["patients"].items():
                print(f"ID: {pid}, Nama: {pinfo['name']}, Telp: {pinfo['phone']}, Alamat: {pinfo['address']}, Tanggal Lahir: {pinfo['birth_date']}")
            patient_id = input("Masukkan ID Pasien yang akan diedit: ")
            if patient_id in data["patients"]:
                pinfo = data["patients"][patient_id]
                print(f"Data saat ini: ID: {patient_id}, Nama: {pinfo['name']}, Telp: {pinfo['phone']}, Alamat: {pinfo['address']}, Tanggal Lahir: {pinfo['birth_date']}")
                new_name = input(f"Nama Baru (sekarang: {pinfo['name']}): ") or pinfo['name']
                new_phone = input(f"Telp Baru (sekarang: {pinfo['phone']}): ") or pinfo['phone']
                new_address = input(f"Alamat Baru (sekarang: {pinfo['address']}): ") or pinfo['address']
                new_birth_date = input(f"Tgl Lahir Baru (sekarang: {pinfo['birth_date']}): ") or pinfo['birth_date']
                data["patients"][patient_id] = {
                    "name": new_name,
                    "phone": new_phone,
                    "address": new_address,
                    "birth_date": new_birth_date,
                    "created_at": pinfo["created_at"]
                }
                save_data(data)
                print(f"{H}[🗸] Data pasien berhasil diubah.{R}")
                time.sleep(3)
                clear_screen()
            else:
                print(Fore.RED + "ID Pasien tidak ditemukan.")
        elif choice == '4':
            print(f"\n{H}Daftar Pasien:{R}")
            for pid, pinfo in data["patients"].items():
                print(f"ID: {pid}, Nama: {pinfo['name']}, Telp: {pinfo['phone']}, Alamat: {pinfo['address']}, Tanggal Lahir: {pinfo['birth_date']}")
            patient_id = input("Masukkan ID Pasien yang akan dihapus: ")
            if patient_id in data["patients"]:
                del data["patients"][patient_id]
                appointments_to_delete = []
                # Hapus janji, checkup, dan rawat inap yang terkait dengan pasien
                for aid, ainfo in data["appointments"].items():
                    if ainfo["patient_id"] == patient_id:
                        appointments_to_delete.append(aid)
                for aid in appointments_to_delete:
                    checkups_to_delete = []
                    for cid, cinfo in data["checkups"].items():
                        if cinfo["appointment_id"] == aid:
                            checkups_to_delete.append(cid)
                    for cid in checkups_to_delete:
                        del data["checkups"][cid]
                    del data["appointments"][aid]
                
                admissions_to_delete = []
                for adid, adinfo in data["admissions"].items():
                    if adinfo["patient_id"] == patient_id:
                        admissions_to_delete.append(adid)
                for adid in admissions_to_delete:
                    # Kembalikan status ruangan
                    room_id = adinfo["room_id"]
                    data["rooms"][room_id]["is_available"] = True
                    del data["admissions"][adid]

                # --- Logika untuk mengurutkan ulang ID Pasien ---
                new_patients = {}
                id_map = {}
                # Urutkan ID lama secara numerik untuk konsistensi
                sorted_old_ids = sorted(data["patients"].keys(), key=int)

                for i, old_id in enumerate(sorted_old_ids):
                    new_id = str(i + 1)
                    new_patients[new_id] = data["patients"][old_id]
                    if old_id != new_id:
                        id_map[old_id] = new_id
                
                # Ganti dictionary patients lama dengan yang baru
                data["patients"] = new_patients

                # Perbarui referensi patient_id di appointments dan admissions
                for entity_dict in [data["appointments"], data["admissions"]]:
                    for entity_info in entity_dict.values():
                        if entity_info.get("patient_id") in id_map:
                            entity_info["patient_id"] = id_map[entity_info["patient_id"]]
                
                save_data(data)
                print(f"{H}[🗸] Data pasien berhasil dihapus dan semua ID terkait telah diurutkan ulang.{R}")
                time.sleep(4)
                clear_screen()
            else:
                print(Fore.RED + "ID Pasien tidak ditemukan.")
        elif choice == '0':
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()



# --- Fungsi Data Jadwal (Staff) ---
def data_jadwal(data):
    while True:
        print(f"\n--- Data Jadwal ({H}Staff{R}) ---")
        print("1. Lihat Semua Jadwal")
        print("2. Tambah Jadwal Baru")
        print("3. Edit Jadwal")
        print("4. Hapus Jadwal")
        print("0. Kembali ke Menu Staff")
        choice = input("Pilih menu: ")

        if choice == '1':
            if not data["schedules"]:
                print(Fore.YELLOW + "\nBelum ada data jadwal.")
                time.sleep(3)
                clear_screen()
            else:
                print(f"\n{H}Daftar Jadwal:{R}")
                for sid, sinfo in data["schedules"].items():
                    doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                    dept_info = data["departments"].get(data["doctors"].get(sinfo["doctor_id"], {}).get("specialty_id"), {"name": "Tidak Ditemukan"})["name"]
                    status = "Tersedia" if sinfo.get("is_available", True) else "Tidak Tersedia"
                print(f"ID: {sid}, Dokter: {doctor_info['name']}, Departemen: {dept_info}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}, Status: {H}{status}{R}")
        elif choice == '2':
            print(f"\n{H}Daftar Dokter:{R}")
            for doc_id, doc_info in data["doctors"].items():
                dept_name = data["departments"].get(doc_info["specialty_id"], {"name": "Tidak Ditemukan"})["name"]
                print(f"ID: {doc_id}, Nama: {doc_info['name']}, Departemen: {dept_name}")
            doctor_id = input("ID Dokter: ")
            if doctor_id not in data["doctors"]:
                print(Fore.RED + "ID Dokter tidak ditemukan.")
                return
            date = input("Tanggal Tersedia (YYYY-MM-DD): ")
            schedule_time = input("Waktu Tersedia (HH:MM - HH:MM): ")
            schedule_id = str(len(data["schedules"]) + 1)
            data["schedules"][schedule_id] = {
                "doctor_id": doctor_id,
                "available_date": date,
                "available_time": schedule_time,
                "is_available": True
            }
            save_data(data)
            print(F"{H}[🗸] Jadwal dokter berhasil ditambahkan.{R}")
            time.sleep(3)
            clear_screen()
        elif choice == '3':
            print(f"\n{H}Daftar Jadwal:{R}")
            for sid, sinfo in data["schedules"].items():
                doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                dept_info = data["departments"].get(data["doctors"].get(sinfo["doctor_id"], {}).get("specialty_id"), {"name": "Tidak Ditemukan"})["name"]
                status = "Tersedia" if sinfo.get("is_available", True) else "Tidak Tersedia"
                print(f"ID: {sid}, Dokter: {doctor_info['name']}, Departemen: {dept_info}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}, Status: {H}{status}{R}")
            schedule_id = input("Masukkan ID Jadwal yang akan diedit: ")
            if schedule_id in data["schedules"]:
                sinfo = data["schedules"][schedule_id]
                doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                print(f"Data saat ini: ID: {schedule_id}, Dokter: {doctor_info['name']}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}")
                print("\nDaftar Dokter:")
                for doc_id, doc_info in data["doctors"].items():
                    dept_name = data["departments"].get(doc_info["specialty_id"], {"name": "Tidak Ditemukan"})["name"]
                    print(f"ID: {doc_id}, Nama: {doc_info['name']}, Departemen: {dept_name}")
                new_doctor_id = input(f"ID Dokter Baru (sekarang: {sinfo['doctor_id']}): ") or sinfo['doctor_id']
                if new_doctor_id not in data["doctors"]:
                    print(Fore.RED + "ID Dokter tidak ditemukan.")
                    return
                new_date = input(f"Tanggal Baru (sekarang: {sinfo['available_date']}): ") or sinfo['available_date']
                new_time = input(f"Waktu Baru (sekarang: {sinfo['available_time']}): ") or sinfo['available_time']
                if not sinfo.get("is_available", True):
                     print(Fore.YELLOW + "Peringatan: Jadwal ini sedang dipesan. Edit mungkin mempengaruhi janji yang sudah dibuat.")
                data["schedules"][schedule_id] = {
                    "doctor_id": new_doctor_id,
                    "available_date": new_date,
                    "available_time": new_time,
                    "is_available": sinfo.get("is_available", True)
                }
                save_data(data)
                print(f"{H}[🗸] Jadwal dokter berhasil diubah.{R}")
            else:
                print(Fore.RED + "ID Jadwal tidak ditemukan.")
                time.sleep(3)
                clear_screen()
        elif choice == '4':
            print(f"\n{H}Daftar Jadwal:{R}")
            for sid, sinfo in data["schedules"].items():
                doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                dept_info = data["departments"].get(data["doctors"].get(sinfo["doctor_id"], {}).get("specialty_id"), {"name": "Tidak Ditemukan"})["name"]
                status = "Tersedia" if sinfo.get("is_available", True) else "Tidak Tersedia"
                print(f"ID: {sid}, Dokter: {doctor_info['name']}, Departemen: {dept_info}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}, Status: {H}{status}{R}")
            schedule_id = input("Masukkan ID Jadwal yang akan dihapus: ")
            if schedule_id in data["schedules"]:
                sinfo = data["schedules"][schedule_id]
                is_booked = any(ainfo["schedule_id"] == schedule_id for ainfo in data["appointments"].values())
                if is_booked:
                    print(Fore.RED + f"Jadwal ID {schedule_id} sedang dipesan oleh pasien. Tidak bisa dihapus.")
                else:
                    del data["schedules"][schedule_id]
                    save_data(data)
                    print("Jadwal dokter berhasil dihapus.")
            else:
                print(Fore.RED + "ID Jadwal tidak ditemukan.")
        elif choice == '0':
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()


# --- Fungsi Buat Janji (Staff) ---
def buat_janji(data):
    print(f"\n--- Buat Janji Baru ({H}Staff{R}) ---")
    
    print(f"{H}Daftar Pasien:{R}")
    for pid, pinfo in data["patients"].items():
        print(f"ID: {pid}, Nama: {pinfo['name']}")
    patient_id = input("Masukkan ID Pasien: ")
    if patient_id not in data["patients"]:
        print(Fore.RED + "ID Pasien tidak ditemukan.")
        time.sleep(3)
        clear_screen()
        return

    print(f"\n{H}Jadwal yang Tersedia:{R}")
    available_schedules = {sid: sinfo for sid, sinfo in data["schedules"].items() if sinfo.get("is_available", True)}
    if not available_schedules:
        print(Fore.YELLOW + "Tidak ada jadwal yang tersedia saat ini.")
        return
    for sid, sinfo in available_schedules.items():
        doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
        dept_info = data["departments"].get(data["doctors"].get(sinfo["doctor_id"], {}).get("specialty_id"), {"name": "Tidak Ditemukan"})["name"]
        print(f"ID: {sid}, Dokter: {doctor_info['name']}, Departemen: {dept_info}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}")
    schedule_id = input("\nMasukkan ID Jadwal: ")
    if schedule_id not in available_schedules:
        print(Fore.RED + "ID Jadwal tidak ditemukan atau tidak tersedia.")
        time.sleep(3)
        clear_screen()
        return

    appointment_id = str(len(data["appointments"]) + 1)
    data["appointments"][appointment_id] = {
        "patient_id": patient_id,
        "schedule_id": schedule_id,
        "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Scheduled"
    }
    data["schedules"][schedule_id]["is_available"] = False
    save_data(data)
    print("Janji berhasil dibuat!")

    new_app = data["appointments"][appointment_id]
    patient_info = data["patients"][patient_id]
    schedule_info = data["schedules"][schedule_id]
    doctor_info = data["doctors"].get(schedule_info["doctor_id"], {"name": "Tidak Ditemukan"})
    dept_info = data["departments"].get(data["doctors"].get(schedule_info["doctor_id"], {}).get("specialty_id"), {"name": "Tidak Ditemukan"})["name"]
    print(f"\nKonfirmasi Janji:")
    print(f"ID Janji: {appointment_id}")
    print(f"Nama Pasien: {patient_info['name']}")
    print(f"Dokter: {doctor_info['name']}")
    print(f"Departemen: {dept_info}")
    print(f"Tanggal: {schedule_info['available_date']}")
    print(f"Waktu: {schedule_info['available_time']}")
    print(f"Status: {H}{new_app['status']}{R}")

# --- Fungsi Data Janji (Staff) ---
def data_janji(data):
    while True:
        print(f"\n--- Data Janji ({H}Staff{R}) ---")
        print("1. Lihat Semua Janji")
        print("2. Hapus Janji")
        print("0. Kembali ke Menu Staff")
        choice = input("Pilih menu: ")

        if choice == '1':
            if not data["appointments"]:
                print(Fore.YELLOW + "Belum ada data janji.")
            else:
                print(f"\n{H}Daftar Janji:{R}")
                for aid, ainfo in data["appointments"].items():
                    pinfo = data["patients"].get(ainfo["patient_id"], {"name": "Tidak Ditemukan"})
                    sinfo = data["schedules"].get(ainfo["schedule_id"], {"doctor_id": "Tidak Ditemukan"})
                    doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                    dept_info = data["departments"].get(data["doctors"].get(sinfo["doctor_id"], {}).get("specialty_id"), {"name": "Tidak Ditemukan"})["name"]
                    print(f"ID: {aid}, Pasien: {pinfo['name']}, Dokter: {doctor_info['name']}, Departemen: {dept_info}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}, Status: {H}{ainfo['status']}{R}")
        elif choice == '2':
            if not data["appointments"]:
                print(Fore.YELLOW + "Belum ada data janji untuk dihapus.")
                continue
            
            print(f"\n{H}Daftar Janji:{R}")
            for aid, ainfo in data["appointments"].items():
                pinfo = data["patients"].get(ainfo["patient_id"], {"name": "Tidak Ditemukan"})
                sinfo = data["schedules"].get(ainfo["schedule_id"], {"doctor_id": "Tidak Ditemukan"})
                doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                dept_info = data["departments"].get(data["doctors"].get(sinfo["doctor_id"], {}).get("specialty_id"), {"name": "Tidak Ditemukan"})["name"]
                print(f"ID: {aid}, Pasien: {pinfo['name']}, Dokter: {doctor_info['name']}, Departemen: {dept_info}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}, Status: {H}{ainfo['status']}{R}")
            appointment_id = input("Masukkan ID Janji yang akan dihapus: ")
            if appointment_id in data["appointments"]:
                # Ambil schedule_id sebelum menghapus janji
                schedule_id = data["appointments"][appointment_id].get("schedule_id")

                # Hapus janji
                del data["appointments"][appointment_id]

                # Kembalikan status jadwal menjadi tersedia
                if schedule_id and schedule_id in data["schedules"]:
                    data["schedules"][schedule_id]["is_available"] = True

                # Hapus juga data checkup yang terkait
                checkups_to_delete = [cid for cid, cinfo in data["checkups"].items() if cinfo.get("appointment_id") == appointment_id]
                for cid in checkups_to_delete:
                    del data["checkups"][cid]

                save_data(data)
                print(f"{H}[🗸] Janji ID {appointment_id} dan data terkait berhasil dihapus. Jadwal telah tersedia kembali.{R}")
                time.sleep(3)
                clear_screen()
            else:
                print(Fore.RED + "ID Janji tidak ditemukan.")
                time.sleep(3)
        elif choice == '0':
            time.sleep(3)
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()

# --- Fungsi Data CheckUp (Staff) ---
def data_checkup(data):
    while True:
        print(f"\n--- Input Data Pemeriksaan (CheckUp) ({H}Staff{R}) ---")
        print("1. Tambah/Edit Data Pemeriksaan")
        print("2. Lihat Semua Data Pemeriksaan")
        print("0. Kembali ke Menu Staff")
        choice = input("Pilih menu: ")

        if choice == '1':
            print(Fore.LIGHTRED_EX + "\nDaftar Janji (Hanya Janji yang Berstatus 'Scheduled' atau 'Completed' yang bisa diisi):")
            eligible_apps = {aid: ainfo for aid, ainfo in data["appointments"].items() if ainfo["status"] in ["Scheduled", "Completed"]}
            if not eligible_apps:
                print(Fore.YELLOW + "Tidak ada janji yang tersedia untuk diisi hasil pemeriksaannya.")
            else:
                for aid, ainfo in eligible_apps.items():
                    pinfo = data["patients"].get(ainfo["patient_id"], {"name": "Tidak Ditemukan"})
                    sinfo = data["schedules"].get(ainfo["schedule_id"], {"doctor_id": "Tidak Ditemukan"})
                    doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                    print(f"ID Janji: {aid}, Pasien: {H}{pinfo['name']}{R}, Dokter: {doctor_info['name']}, Tanggal: {sinfo['available_date']}, Status: {H}{ainfo['status']}{R}")
            
            app_id = input("\nMasukkan ID Janji untuk diisi pemeriksaannya: ")
            if app_id not in eligible_apps:
                print(Fore.RED + "ID Janji tidak ditemukan atau statusnya tidak memungkinkan untuk diisi pemeriksaan.")
            else:
                diagnosis = input("Masukkan Diagnosis: ")
                notes = input("Catatan Tambahan: ")
                
                existing_checkup_id = None
                for cid, cinfo in data["checkups"].items():
                    if cinfo["appointment_id"] == app_id:
                        existing_checkup_id = cid
                        break
                
                if existing_checkup_id:
                    print(f"Data pemeriksaan untuk Janji ID {app_id} sudah ada (ID CheckUp: {existing_checkup_id}). Apakah Anda ingin menggantinya? (y/n): ")
                    confirm = input().lower()
                    if confirm == 'y':
                        data["checkups"][existing_checkup_id] = {
                            "appointment_id": app_id,
                            "checkup_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "diagnosis": diagnosis,
                            "notes": notes
                        }
                        print("Data pemeriksaan berhasil diperbarui.")
                    else:
                        print("Operasi dibatalkan.")
                else:
                    checkup_id = str(len(data["checkups"]) + 1)
                    data["checkups"][checkup_id] = {
                        "appointment_id": app_id,
                        "checkup_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "diagnosis": diagnosis,
                        "notes": notes
                    }
                    print(f"{H}[🗸] Data pemeriksaan berhasil ditambahkan.{R}")
                
                data["appointments"][app_id]["status"] = "Completed"
                print(f"Status janji untuk ID tersebut telah diperbarui menjadi '{H}Completed{R}'.")
                save_data(data)

        elif choice == '2':
            if not data["checkups"]:
                print("\nBelum ada data pemeriksaan.")
            else:
                print(f"\n{H}Daftar Data Pemeriksaan:{R}")
                for cid, cinfo in data["checkups"].items():
                    aid = cinfo["appointment_id"]
                    ainfo = data["appointments"].get(aid, {})
                    pinfo = data["patients"].get(ainfo.get("patient_id"), {"name": "Tidak Ditemukan"})
                    print(f"ID CheckUp: {cid}, ID Janji: {aid}, Nama Pasien: {H}{pinfo['name']}{R}, Tanggal: {cinfo['checkup_date']}")
                    print(f"  Diagnosis: {H}{cinfo['diagnosis']}{R}")
                    print(f"  Catatan: {H}{cinfo['notes']}{R}\n")
        elif choice == '0':
            time.sleep(2)
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(1)
            clear_screen()


# --- Fungsi Data Rawat Inap (Staff) ---
def data_rawat_inap(data):
    while True:
        print("\n--- Data Rawat Inap (Staff) ---")
        print("1. Lihat Semua Rawat Inap")
        print("2. Tambah Rawat Inap Baru")
        print("3. Edit Rawat Inap (Status Keluar)")
        print("4. Hapus Rawat Inap")
        print("0. Kembali ke Menu Staff")
        choice = input("Pilih menu: ")

        if choice == '1':
            if not data["admissions"]:
                print("\nBelum ada data rawat inap.")
            else:
                print("\nDaftar Rawat Inap:")
                for adid, adinfo in data["admissions"].items():
                    pinfo = data["patients"].get(adinfo["patient_id"], {"name": "Tidak Ditemukan"})
                    rinfo = data["rooms"].get(adinfo["room_id"], {"name": "Tidak Ditemukan"})
                    print(f"ID Rawat Inap: {adid}, Pasien: {pinfo['name']}, Ruangan: {rinfo['name']}, Masuk: {adinfo['admission_date']}, Estimasi Keluar: {adinfo['discharge_date']}, Status: {H}{adinfo['status']}{R}")
        elif choice == '2':
            print("\nDaftar Pasien:")
            for pid, pinfo in data["patients"].items():
                print(f"ID: {pid}, Nama: {pinfo['name']}")
            patient_id = input("Masukkan ID Pasien: ")
            if patient_id not in data["patients"]:
                print(Fore.RED + "ID Pasien tidak ditemukan.")
                return

            print("\nDaftar Janji (Hanya Janji yang Berstatus 'Completed' yang bisa dijadikan dasar rawat inap):")
            completed_apps = {aid: ainfo for aid, ainfo in data["appointments"].items() if ainfo["status"] == "Completed" and ainfo["patient_id"] == patient_id}
            if not completed_apps:
                print(Fore.YELLOW + "Pasien ini belum memiliki janji yang selesai (Completed).")
                return
            for aid, ainfo in completed_apps.items():
                 sinfo = data["schedules"].get(ainfo["schedule_id"], {"doctor_id": "Tidak Ditemukan"})
                 doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                 print(f"ID Janji: {aid}, Dokter: {doctor_info['name']}, Tanggal: {sinfo['available_date']}")
            appointment_id = input("Masukkan ID Janji sebagai dasar rawat inap: ")
            if appointment_id not in completed_apps:
                print(Fore.RED + "ID Janji tidak ditemukan atau bukan milik pasien ini atau belum selesai.")
                return

            print("\nDaftar Ruangan Tersedia:")
            available_rooms = {rid: rinfo for rid, rinfo in data["rooms"].items() if rinfo.get("is_available", True)}
            if not available_rooms:
                print("Tidak ada ruangan yang tersedia saat ini.")
                return
            for rid, rinfo in available_rooms.items():
                print(f"ID: {rid}, Nama: {rinfo['name']}, Tipe: {rinfo['type']}")
            room_id = input("Masukkan ID Ruangan: ")
            if room_id not in available_rooms:
                print(Fore.RED + "ID Ruangan tidak ditemukan atau tidak tersedia.")
                return

            admission_date = input("Tanggal Masuk (YYYY-MM-DD): ")
            discharge_date = input("Estimasi Tanggal Keluar (YYYY-MM-DD): ")
            admission_id = str(len(data["admissions"]) + 1)
            data["admissions"][admission_id] = {
                "patient_id": patient_id,
                "appointment_id": appointment_id,
                "room_id": room_id,
                "admission_date": admission_date,
                "discharge_date": discharge_date,
                "status": "Admitted" # Status awal
            }
            # Ubah status ruangan menjadi tidak tersedia
            data["rooms"][room_id]["is_available"] = False
            save_data(data)
            print("Data rawat inap berhasil ditambahkan.")

        elif choice == '3':
            admission_id = input("Masukkan ID Rawat Inap untuk diubah statusnya (keluar): ")
            if admission_id in data["admissions"]:
                adinfo = data["admissions"][admission_id]
                if adinfo["status"] == "Discharged":
                    print(Fore.YELLOW + "Pasien sudah dikeluarkan.")
                    continue
                print(f"Data saat ini: ID Rawat Inap: {admission_id}, Pasien: {data['patients'].get(adinfo['patient_id'], {'name': 'Tidak Ditemukan'})['name']}, Status: {H}{adinfo['status']}{R}")
                confirm = input("Apakah pasien ini dikeluarkan sekarang? (y/n): ").lower()
                if confirm == 'y':
                    # Kembalikan status ruangan menjadi tersedia
                    data["rooms"][adinfo["room_id"]]["is_available"] = True
                    data["admissions"][admission_id]["status"] = "Discharged"
                    data["admissions"][admission_id]["discharge_date_actual"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_data(data)
                    print(f"Status rawat inap berhasil diubah menjadi '{H}Discharged{R}'.")
                else:
                    print("Operasi dibatalkan.")
            else:
                print(Fore.RED + "ID Rawat Inap tidak ditemukan.")
        elif choice == '4':
             admission_id = input("Masukkan ID Rawat Inap yang akan dihapus: ")
             if admission_id in data["admissions"]:
                 adinfo = data["admissions"][admission_id]
                 # Kembalikan status ruangan jika rawat inap belum selesai
                 if adinfo["status"] != "Discharged":
                     data["rooms"][adinfo["room_id"]]["is_available"] = True
                 del data["admissions"][admission_id]
                 save_data(data)
                 print("Data rawat inap berhasil dihapus.")
             else:
                print(Fore.RED + "ID Rawat Inap tidak ditemukan.")
        elif choice == '0':
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(1)
            clear_screen()


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
            user_id, username, role = login(data)
            clear_screen()
            if role == 'admin':
                menu_admin(data)
            elif role == 'staff':
                menu_staff(data)
            elif role == 'user':
                menu_user(data, username)
            else:
                print(Fore.RED + "Role tidak dikenali.")
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