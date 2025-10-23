import json
import os
from datetime import datetime

DATA_FILE = "hospital_data_extended.json"

def clear_screen():
    os_name = os.name
    if os_name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("File data rusak, menggunakan data kosong.")
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
        password = input("Password: ")

        user = data["users"].get(username)
        if user and user["password"] == password:
            print(f"\nLogin berhasil! Selamat datang, {username} (Role: {user['role']})")
            return user["id"], username, user["role"]
        else:
            print("Username atau password salah. Silakan coba lagi.")

# --- Fungsi Register (Hanya untuk user biasa, role 'user') ---
def register(data):
    print("\n--- Register ---")
    username = input("Masukkan username baru: ")
    password = input("Masukkan password baru: ")
    role = 'user' # Tetap sebagai 'user'

    if username in data["users"]:
        print("Username sudah digunakan. Silakan coba yang lain.")
    else:
        user_id = str(len(data["users"]) + 1)
        data["users"][username] = {"id": user_id, "password": password, "role": role}
        save_data(data)
        print("Registrasi berhasil! Silakan login.")

# --- Menu Admin ---
def menu_admin(data):
    while True:
        print("\n--- Menu Admin ---")
        print("1. Manajemen User")
        print("2. Manajemen Departemen")
        print("3. Manajemen Dokter")
        print("4. Manajemen Ruangan")
        print("5. Laporan Sederhana")
        print("0. Kembali ke Menu Utama")
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
            clear_screen()
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# --- Menu Staff ---
def menu_staff(data):
    while True:
        print("\n--- Menu Staff ---")
        print("1. Data Pasien")
        print("2. Data Jadwal")
        print("3. Data Janji")
        print("4. Buat Janji")
        print("5. Data CheckUp")
        print("6. Data Rawat Inap")
        print("0. Kembali ke Menu Utama")
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
            clear_screen()
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# --- Menu User Biasa ---
def menu_user(data, current_username):
    while True:
        print(f"\n--- Menu User ({current_username}) ---")
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
            clear_screen()
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# --- Fungsi Lihat Jadwal Tersedia (untuk User) ---
def lihat_jadwal_tersedia(data):
    print("\n--- Jadwal Dokter Tersedia ---")
    # Filter hanya jadwal yang tersedia
    available_schedules = {sid: sinfo for sid, sinfo in data["schedules"].items() if sinfo.get("is_available", True)}
    if not available_schedules:
        print("Tidak ada jadwal yang tersedia saat ini.")
        return

    # Tampilkan dengan detail dokter dan departemen
    print("Daftar Jadwal Tersedia:")
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
        print(f"Anda ({current_username}) belum terdaftar sebagai pasien. Silakan daftar dulu atau hubungi staff.")
        return

    # Tampilkan jadwal yang tersedia
    available_schedules = {sid: sinfo for sid, sinfo in data["schedules"].items() if sinfo.get("is_available", True)}
    if not available_schedules:
        print("Tidak ada jadwal yang tersedia saat ini.")
        return

    print("Daftar Jadwal Tersedia:")
    for sid, sinfo in available_schedules.items():
        doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
        dept_info = data["departments"].get(doctor_info["specialty_id"], {"name": "Tidak Ditemukan"})
        print(f"ID Jadwal: {sid}, Dokter: {doctor_info['name']}, Departemen: {dept_info['name']}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}")
    
    schedule_id = input("\nMasukkan ID Jadwal yang dipilih: ")
    if schedule_id not in available_schedules:
        print("ID Jadwal tidak valid atau sudah dipesan.")
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
    print("Janji berhasil dibuat untuk Anda!")

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
        print("Anda belum terdaftar sebagai pasien.")
        return

    user_appointments = {aid: ainfo for aid, ainfo in data["appointments"].items() if ainfo["patient_id"] == patient_id}
    if not user_appointments:
        print("Anda belum memiliki janji temu.")
        return

    print("Daftar Janji Anda:")
    for aid, ainfo in user_appointments.items():
        sinfo = data["schedules"].get(ainfo["schedule_id"], {"doctor_id": "Tidak Ditemukan"})
        doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
        dept_info = data["departments"].get(doctor_info["specialty_id"], {"name": "Tidak Ditemukan"})
        print(f"ID Janji: {aid}, Dokter: {doctor_info['name']}, Departemen: {dept_info['name']}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}, Status: {ainfo['status']}")

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
        print("Anda belum terdaftar sebagai pasien.")
        return

    # Cari janji pasien
    patient_appointments = [aid for aid, ainfo in data["appointments"].items() if ainfo["patient_id"] == patient_id]

    if not patient_appointments:
        print("Anda belum memiliki riwayat janji.")
        return

    print("Riwayat Pemeriksaan:")
    for aid in patient_appointments:
        # Cari data checkup terkait
        checkup_found = False
        for cid, cinfo in data["checkups"].items():
            if cinfo["appointment_id"] == aid:
                ainfo = data["appointments"][aid]
                sinfo = data["schedules"].get(ainfo["schedule_id"], {"doctor_id": "Tidak Ditemukan"})
                doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                print(f"ID Janji: {aid}, Tanggal Checkup: {cinfo['checkup_date']}, Dokter: {doctor_info['name']}")
                print(f"  Diagnosis: {cinfo['diagnosis']}")
                print(f"  Catatan: {cinfo['notes']}")
                checkup_found = True
                break
        if not checkup_found:
            print(f"ID Janji: {aid} - Belum ada data pemeriksaan.")

# --- Fungsi Manajemen User (Admin) ---
def manajemen_user(data):
    while True:
        print("\n--- Manajemen User (Admin) ---")
        print("1. Lihat Semua User")
        print("2. Tambah User")
        print("3. Edit User")
        print("4. Hapus User")
        print("0. Kembali ke Menu Admin")
        choice = input("Pilih menu: ")

        if choice == '1':
            print("\nDaftar User:")
            for uname, uinfo in data["users"].items():
                print(f"Username: {uname}, ID: {uinfo['id']}, Role: {uinfo['role']}")
        elif choice == '2':
            username = input("Username Baru: ")
            password = input("Password Baru: ")
            role = input("Role (admin/staff/user): ")
            if role not in ['admin', 'staff', 'user']:
                print("Role tidak valid.")
                continue
            if username in data["users"]:
                print("Username sudah digunakan.")
                continue
            user_id = str(len(data["users"]) + 1)
            data["users"][username] = {"id": user_id, "password": password, "role": role}
            save_data(data)
            print("User berhasil ditambahkan.")
        elif choice == '3':
            username = input("Username yang akan diedit: ")
            if username not in data["users"]:
                print("Username tidak ditemukan.")
                continue
            uinfo = data["users"][username]
            print(f"Data saat ini: Username: {username}, ID: {uinfo['id']}, Role: {uinfo['role']}")
            new_role = input(f"Role Baru (sekarang: {uinfo['role']}): ") or uinfo['role']
            if new_role not in ['admin', 'staff', 'user']:
                print("Role tidak valid.")
                continue
            new_password = input("Password Baru (tekan Enter jika tidak ingin diganti): ")
            if new_password:
                data["users"][username]["password"] = new_password
            data["users"][username]["role"] = new_role
            save_data(data)
            print("User berhasil diubah.")
        elif choice == '4':
            username = input("Username yang akan dihapus: ")
            if username == 'admin': # Proteksi akun admin default
                print("Tidak bisa menghapus akun admin default.")
                continue
            if username in data["users"]:
                del data["users"][username]
                save_data(data)
                print("User berhasil dihapus.")
            else:
                print("Username tidak ditemukan.")
        elif choice == '0':
            break
        else:
            print("Pilihan tidak valid.")

# --- Fungsi Manajemen Departemen (Admin) ---
def manajemen_departemen(data):
    while True:
        print("\n--- Manajemen Departemen (Admin) ---")
        print("1. Lihat Semua Departemen")
        print("2. Tambah Departemen")
        print("3. Edit Departemen")
        print("4. Hapus Departemen")
        print("0. Kembali ke Menu Admin")
        choice = input("Pilih menu: ")

        if choice == '1':
            print("\nDaftar Departemen:")
            for did, dinfo in data["departments"].items():
                print(f"ID: {did}, Nama: {dinfo['name']}")
        elif choice == '2':
            name = input("Nama Departemen Baru: ")
            dept_id = str(len(data["departments"]) + 1)
            data["departments"][dept_id] = {"name": name}
            save_data(data)
            print("Departemen berhasil ditambahkan.")
        elif choice == '3':
            dept_id = input("ID Departemen yang akan diedit: ")
            if dept_id not in data["departments"]:
                print("ID Departemen tidak ditemukan.")
                continue
            dinfo = data["departments"][dept_id]
            print(f"Data saat ini: ID: {dept_id}, Nama: {dinfo['name']}")
            new_name = input(f"Nama Baru (sekarang: {dinfo['name']}): ") or dinfo['name']
            data["departments"][dept_id]["name"] = new_name
            save_data(data)
            print("Departemen berhasil diubah.")
        elif choice == '4':
            dept_id = input("ID Departemen yang akan dihapus: ")
            if dept_id not in data["departments"]:
                print("ID Departemen tidak ditemukan.")
                continue
            # Cek apakah ada dokter di departemen ini
            doctors_in_dept = [doc_id for doc_id, doc_info in data["doctors"].items() if doc_info["specialty_id"] == dept_id]
            if doctors_in_dept:
                print(f"Departemen '{data['departments'][dept_id]['name']}' masih memiliki dokter ({len(doctors_in_dept)}). Hapus dokter terlebih dahulu.")
                continue
            del data["departments"][dept_id]
            save_data(data)
            print("Departemen berhasil dihapus.")
        elif choice == '0':
            break
        else:
            print("Pilihan tidak valid.")

# --- Fungsi Manajemen Dokter (Admin) ---
def manajemen_dokter(data):
    while True:
        print("\n--- Manajemen Dokter (Admin) ---")
        print("1. Lihat Semua Dokter")
        print("2. Tambah Dokter")
        print("3. Edit Dokter")
        print("4. Hapus Dokter")
        print("0. Kembali ke Menu Admin")
        choice = input("Pilih menu: ")

        if choice == '1':
            print("\nDaftar Dokter:")
            for doc_id, doc_info in data["doctors"].items():
                dept_name = data["departments"].get(doc_info["specialty_id"], {"name": "Tidak Ditemukan"})["name"]
                print(f"ID: {doc_id}, Nama: {doc_info['name']}, Departemen: {dept_name}, Telp: {doc_info['phone']}")
        elif choice == '2':
            name = input("Nama Dokter Baru: ")
            phone = input("Nomor Telepon: ")
            print("\nDaftar Departemen:")
            for did, dinfo in data["departments"].items():
                print(f"ID: {did}, Nama: {dinfo['name']}")
            specialty_id = input("ID Departemen: ")
            if specialty_id not in data["departments"]:
                print("ID Departemen tidak ditemukan.")
                continue
            doc_id = str(len(data["doctors"]) + 1)
            data["doctors"][doc_id] = {"name": name, "specialty_id": specialty_id, "phone": phone}
            save_data(data)
            print("Dokter berhasil ditambahkan.")
        elif choice == '3':
            doc_id = input("ID Dokter yang akan diedit: ")
            if doc_id not in data["doctors"]:
                print("ID Dokter tidak ditemukan.")
                continue
            doc_info = data["doctors"][doc_id]
            dept_name = data["departments"].get(doc_info["specialty_id"], {"name": "Tidak Ditemukan"})["name"]
            print(f"Data saat ini: ID: {doc_id}, Nama: {doc_info['name']}, Departemen: {dept_name}, Telp: {doc_info['phone']}")
            new_name = input(f"Nama Baru (sekarang: {doc_info['name']}): ") or doc_info['name']
            new_phone = input(f"Telp Baru (sekarang: {doc_info['phone']}): ") or doc_info['phone']
            print("\nDaftar Departemen:")
            for did, dinfo in data["departments"].items():
                print(f"ID: {did}, Nama: {dinfo['name']}")
            new_spec_id = input(f"ID Departemen Baru (sekarang: {doc_info['specialty_id']}): ") or doc_info['specialty_id']
            if new_spec_id not in data["departments"]:
                print("ID Departemen tidak ditemukan.")
                continue
            data["doctors"][doc_id] = {"name": new_name, "specialty_id": new_spec_id, "phone": new_phone}
            save_data(data)
            print("Dokter berhasil diubah.")
        elif choice == '4':
            doc_id = input("ID Dokter yang akan dihapus: ")
            if doc_id not in data["doctors"]:
                print("ID Dokter tidak ditemukan.")
                continue
            # Cek apakah ada jadwal aktif untuk dokter ini
            schedules_for_doc = [sid for sid, sinfo in data["schedules"].items() if sinfo["doctor_id"] == doc_id]
            if schedules_for_doc:
                print(f"Dokter '{data['doctors'][doc_id]['name']}' masih memiliki jadwal aktif. Hapus jadwal terlebih dahulu.")
                continue
            del data["doctors"][doc_id]
            save_data(data)
            print("Dokter berhasil dihapus.")
        elif choice == '0':
            break
        else:
            print("Pilihan tidak valid.")

# --- Fungsi Manajemen Ruangan (Admin) ---
def manajemen_ruangan(data):
    while True:
        print("\n--- Manajemen Ruangan (Admin) ---")
        print("1. Lihat Semua Ruangan")
        print("2. Tambah Ruangan")
        print("3. Edit Ruangan")
        print("4. Hapus Ruangan")
        print("0. Kembali ke Menu Admin")
        choice = input("Pilih menu: ")

        if choice == '1':
            print("\nDaftar Ruangan:")
            for rid, rinfo in data["rooms"].items():
                status = "Tersedia" if rinfo.get("is_available", True) else "Tidak Tersedia"
                print(f"ID: {rid}, Nama: {rinfo['name']}, Tipe: {rinfo['type']}, Status: {status}")
        elif choice == '2':
            name = input("Nama Ruangan Baru: ")
            type_room = input("Tipe Ruangan (VIP/Kelas 1/Kelas 2/Kelas 3): ")
            room_id = str(len(data["rooms"]) + 1)
            data["rooms"][room_id] = {"name": name, "type": type_room, "is_available": True}
            save_data(data)
            print("Ruangan berhasil ditambahkan.")
        elif choice == '3':
            room_id = input("ID Ruangan yang akan diedit: ")
            if room_id not in data["rooms"]:
                print("ID Ruangan tidak ditemukan.")
                continue
            rinfo = data["rooms"][room_id]
            print(f"Data saat ini: ID: {room_id}, Nama: {rinfo['name']}, Tipe: {rinfo['type']}, Tersedia: {rinfo.get('is_available', True)}")
            new_name = input(f"Nama Baru (sekarang: {rinfo['name']}): ") or rinfo['name']
            new_type = input(f"Tipe Baru (sekarang: {rinfo['type']}): ") or rinfo['type']
            # Tidak mengedit is_available di sini, karena statusnya tergantung pada rawat inap
            data["rooms"][room_id] = {"name": new_name, "type": new_type, "is_available": rinfo.get('is_available', True)}
            save_data(data)
            print("Ruangan berhasil diubah.")
        elif choice == '4':
            room_id = input("ID Ruangan yang akan dihapus: ")
            if room_id not in data["rooms"]:
                print("ID Ruangan tidak ditemukan.")
                continue
            rinfo = data["rooms"][room_id]
            if not rinfo.get("is_available", True): # Jika tidak tersedia, berarti sedang digunakan
                print(f"Ruangan '{rinfo['name']}' sedang digunakan (tidak tersedia). Hapus data rawat inap terlebih dahulu.")
                continue
            del data["rooms"][room_id]
            save_data(data)
            print("Ruangan berhasil dihapus.")
        elif choice == '0':
            break
        else:
            print("Pilihan tidak valid.")

# --- Fungsi Laporan Sederhana (Admin) ---
def laporan_sederhana(data):
    print("\n--- Laporan Sederhana (Admin) ---")
    print("1. Laporan Janji Harian")
    print("2. Laporan Pasien per Departemen")
    print("3. Laporan Ruangan Tersedia")
    sub_choice = input("Pilih laporan: ")

    if sub_choice == '1':
        date = input("Masukkan Tanggal (YYYY-MM-DD): ")
        print(f"\nLaporan Janji untuk Tanggal: {date}")
        for aid, ainfo in data["appointments"].items():
            sinfo = data["schedules"].get(ainfo["schedule_id"], {})
            if sinfo.get("available_date") == date:
                pinfo = data["patients"].get(ainfo["patient_id"], {"name": "Tidak Ditemukan"})
                doc_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                print(f"ID Janji: {aid}, Pasien: {pinfo['name']}, Dokter: {doc_info['name']}, Status: {ainfo['status']}")
    elif sub_choice == '2':
        print("\nLaporan Jumlah Pasien per Departemen:")
        dept_counts = {}
        for aid, ainfo in data["appointments"].items():
            sinfo = data["schedules"].get(ainfo["schedule_id"], {})
            doc_info = data["doctors"].get(sinfo["doctor_id"], {})
            dept_id = doc_info.get("specialty_id")
            if dept_id:
                dept_name = data["departments"].get(dept_id, {"name": "Tidak Ditemukan"})["name"]
                dept_counts[dept_name] = dept_counts.get(dept_name, 0) + 1
        for dept_name, count in dept_counts.items():
            print(f"Departemen: {dept_name}, Jumlah Pasien: {count}")
    elif sub_choice == '3':
        print("\nLaporan Ruangan Tersedia:")
        available_rooms = [rinfo for rinfo in data["rooms"].values() if rinfo.get("is_available", True)]
        if not available_rooms:
            print("Tidak ada ruangan yang tersedia saat ini.")
        else:
            for rinfo in available_rooms:
                print(f"Nama: {rinfo['name']}, Tipe: {rinfo['type']}")
    else:
        print("Pilihan tidak valid.")

# --- Fungsi Data Pasien (Staff) ---
def data_pasien(data):
    while True:
        print("\n--- Data Pasien (Staff) ---")
        print("1. Lihat Semua Pasien")
        print("2. Tambah Pasien Baru")
        print("3. Edit Pasien")
        print("4. Hapus Pasien")
        print("0. Kembali ke Menu Staff")
        choice = input("Pilih menu: ")

        if choice == '1':
            if not data["patients"]:
                print("\nBelum ada data pasien.")
            else:
                print("\nDaftar Pasien:")
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
            print("Data pasien berhasil ditambahkan.")
        elif choice == '3':
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
                print("Data pasien berhasil diubah.")
            else:
                print("ID Pasien tidak ditemukan.")
        elif choice == '4':
            patient_id = input("Masukkan ID Pasien yang akan dihapus: ")
            if patient_id in data["patients"]:
                del data["patients"][patient_id]
                appointments_to_delete = []
                for aid, ainfo in data["appointments"].items():
                    if ainfo["patient_id"] == patient_id:
                        appointments_to_delete.append(aid)
                for aid in appointments_to_delete:
                    del data["appointments"][aid]
                    checkups_to_delete = []
                    for cid, cinfo in data["checkups"].items():
                        if cinfo["appointment_id"] == aid:
                            checkups_to_delete.append(cid)
                    for cid in checkups_to_delete:
                        del data["checkups"][cid]
                
                admissions_to_delete = []
                for adid, adinfo in data["admissions"].items():
                    if adinfo["patient_id"] == patient_id:
                        admissions_to_delete.append(adid)
                for adid in admissions_to_delete:
                    # Kembalikan status ruangan
                    room_id = adinfo["room_id"]
                    data["rooms"][room_id]["is_available"] = True
                    del data["admissions"][adid]
                
                save_data(data)
                print("Data pasien, janji, dan rawat inap terkait berhasil dihapus.")
            else:
                print("ID Pasien tidak ditemukan.")
        elif choice == '0':
            break
        else:
            print("Pilihan tidak valid.")

# --- Fungsi Data Jadwal (Staff) ---
def data_jadwal(data):
    while True:
        print("\n--- Data Jadwal (Staff) ---")
        print("1. Lihat Semua Jadwal")
        print("2. Tambah Jadwal Baru")
        print("3. Edit Jadwal")
        print("4. Hapus Jadwal")
        print("0. Kembali ke Menu Staff")
        choice = input("Pilih menu: ")

        if choice == '1':
            if not data["schedules"]:
                print("\nBelum ada data jadwal.")
            else:
                print("\nDaftar Jadwal:")
                for sid, sinfo in data["schedules"].items():
                    doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                    dept_info = data["departments"].get(data["doctors"].get(sinfo["doctor_id"], {}).get("specialty_id"), {"name": "Tidak Ditemukan"})["name"]
                    status = "Tersedia" if sinfo.get("is_available", True) else "Tidak Tersedia"
                    print(f"ID: {sid}, Dokter: {doctor_info['name']}, Departemen: {dept_info}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}, Status: {status}")
        elif choice == '2':
            print("\nDaftar Dokter:")
            for doc_id, doc_info in data["doctors"].items():
                dept_name = data["departments"].get(doc_info["specialty_id"], {"name": "Tidak Ditemukan"})["name"]
                print(f"ID: {doc_id}, Nama: {doc_info['name']}, Departemen: {dept_name}")
            doctor_id = input("ID Dokter: ")
            if doctor_id not in data["doctors"]:
                print("ID Dokter tidak ditemukan.")
                return
            date = input("Tanggal Tersedia (YYYY-MM-DD): ")
            time = input("Waktu Tersedia (HH:MM): ")
            schedule_id = str(len(data["schedules"]) + 1)
            data["schedules"][schedule_id] = {
                "doctor_id": doctor_id,
                "available_date": date,
                "available_time": time,
                "is_available": True
            }
            save_data(data)
            print("Jadwal dokter berhasil ditambahkan.")
        elif choice == '3':
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
                    print("ID Dokter tidak ditemukan.")
                    return
                new_date = input(f"Tanggal Baru (sekarang: {sinfo['available_date']}): ") or sinfo['available_date']
                new_time = input(f"Waktu Baru (sekarang: {sinfo['available_time']}): ") or sinfo['available_time']
                if not sinfo.get("is_available", True):
                     print("Peringatan: Jadwal ini sedang dipesan. Edit mungkin mempengaruhi janji yang sudah dibuat.")
                data["schedules"][schedule_id] = {
                    "doctor_id": new_doctor_id,
                    "available_date": new_date,
                    "available_time": new_time,
                    "is_available": sinfo.get("is_available", True)
                }
                save_data(data)
                print("Jadwal dokter berhasil diubah.")
            else:
                print("ID Jadwal tidak ditemukan.")
        elif choice == '4':
            schedule_id = input("Masukkan ID Jadwal yang akan dihapus: ")
            if schedule_id in data["schedules"]:
                sinfo = data["schedules"][schedule_id]
                is_booked = any(ainfo["schedule_id"] == schedule_id for ainfo in data["appointments"].values())
                if is_booked:
                    print(f"Jadwal ID {schedule_id} sedang dipesan oleh pasien. Tidak bisa dihapus.")
                else:
                    del data["schedules"][schedule_id]
                    save_data(data)
                    print("Jadwal dokter berhasil dihapus.")
            else:
                print("ID Jadwal tidak ditemukan.")
        elif choice == '0':
            break
        else:
            print("Pilihan tidak valid.")

# --- Fungsi Buat Janji (Staff) ---
def buat_janji(data):
    print("\n--- Buat Janji Baru (Staff) ---")
    
    print("Daftar Pasien:")
    for pid, pinfo in data["patients"].items():
        print(f"ID: {pid}, Nama: {pinfo['name']}")
    patient_id = input("Masukkan ID Pasien: ")
    if patient_id not in data["patients"]:
        print("ID Pasien tidak ditemukan.")
        return

    print("\nJadwal yang Tersedia:")
    available_schedules = {sid: sinfo for sid, sinfo in data["schedules"].items() if sinfo.get("is_available", True)}
    if not available_schedules:
        print("Tidak ada jadwal yang tersedia saat ini.")
        return
    for sid, sinfo in available_schedules.items():
        doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
        dept_info = data["departments"].get(data["doctors"].get(sinfo["doctor_id"], {}).get("specialty_id"), {"name": "Tidak Ditemukan"})["name"]
        print(f"ID: {sid}, Dokter: {doctor_info['name']}, Departemen: {dept_info}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}")
    schedule_id = input("Masukkan ID Jadwal: ")
    if schedule_id not in available_schedules:
        print("ID Jadwal tidak ditemukan atau sudah dipesan.")
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
    print(f"Status: {new_app['status']}")

# --- Fungsi Data Janji (Staff) ---
def data_janji(data):
    print("\n--- Data Janji (Staff) ---")
    if not data["appointments"]:
        print("Belum ada data janji.")
    else:
        print("\nDaftar Janji:")
        for aid, ainfo in data["appointments"].items():
            pinfo = data["patients"].get(ainfo["patient_id"], {"name": "Tidak Ditemukan"})
            sinfo = data["schedules"].get(ainfo["schedule_id"], {"doctor_id": "Tidak Ditemukan"})
            doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
            dept_info = data["departments"].get(data["doctors"].get(sinfo["doctor_id"], {}).get("specialty_id"), {"name": "Tidak Ditemukan"})["name"]
            print(f"ID: {aid}, Pasien: {pinfo['name']}, Dokter: {doctor_info['name']}, Departemen: {dept_info}, Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}, Status: {ainfo['status']}")

# --- Fungsi Data CheckUp (Staff) ---
def data_checkup(data):
    while True:
        print("\n--- Input Data Pemeriksaan (CheckUp) (Staff) ---")
        print("1. Tambah/Edit Data Pemeriksaan")
        print("2. Lihat Semua Data Pemeriksaan")
        print("0. Kembali ke Menu Staff")
        choice = input("Pilih menu: ")

        if choice == '1':
            print("\nDaftar Janji (Hanya Janji yang Berstatus 'Scheduled' atau 'Completed' yang bisa diisi):")
            eligible_apps = {aid: ainfo for aid, ainfo in data["appointments"].items() if ainfo["status"] in ["Scheduled", "Completed"]}
            if not eligible_apps:
                print("Tidak ada janji yang tersedia untuk diisi hasil pemeriksaannya.")
            else:
                for aid, ainfo in eligible_apps.items():
                    pinfo = data["patients"].get(ainfo["patient_id"], {"name": "Tidak Ditemukan"})
                    sinfo = data["schedules"].get(ainfo["schedule_id"], {"doctor_id": "Tidak Ditemukan"})
                    doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                    print(f"ID Janji: {aid}, Pasien: {pinfo['name']}, Dokter: {doctor_info['name']}, Tanggal: {sinfo['available_date']}, Status: {ainfo['status']}")
            
            app_id = input("\nMasukkan ID Janji untuk diisi pemeriksaannya: ")
            if app_id not in eligible_apps:
                print("ID Janji tidak ditemukan atau statusnya tidak memungkinkan untuk diisi pemeriksaan.")
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
                    print("Data pemeriksaan berhasil ditambahkan.")
                
                data["appointments"][app_id]["status"] = "Completed"
                print("Status janji untuk ID tersebut telah diperbarui menjadi 'Completed'.")
                save_data(data)

        elif choice == '2':
            if not data["checkups"]:
                print("\nBelum ada data pemeriksaan.")
            else:
                print("\nDaftar Data Pemeriksaan:")
                for cid, cinfo in data["checkups"].items():
                    aid = cinfo["appointment_id"]
                    ainfo = data["appointments"].get(aid, {})
                    pinfo = data["patients"].get(ainfo.get("patient_id"), {"name": "Tidak Ditemukan"})
                    print(f"ID CheckUp: {cid}, ID Janji: {aid}, Nama Pasien: {pinfo['name']}, Tanggal: {cinfo['checkup_date']}")
                    print(f"  Diagnosis: {cinfo['diagnosis']}")
                    print(f"  Catatan: {cinfo['notes']}\n")
        elif choice == '0':
            break
        else:
            print("Pilihan tidak valid.")

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
                    print(f"ID Rawat Inap: {adid}, Pasien: {pinfo['name']}, Ruangan: {rinfo['name']}, Masuk: {adinfo['admission_date']}, Estimasi Keluar: {adinfo['discharge_date']}, Status: {adinfo['status']}")
        elif choice == '2':
            print("\nDaftar Pasien:")
            for pid, pinfo in data["patients"].items():
                print(f"ID: {pid}, Nama: {pinfo['name']}")
            patient_id = input("Masukkan ID Pasien: ")
            if patient_id not in data["patients"]:
                print("ID Pasien tidak ditemukan.")
                return

            print("\nDaftar Janji (Hanya Janji yang Berstatus 'Completed' yang bisa dijadikan dasar rawat inap):")
            completed_apps = {aid: ainfo for aid, ainfo in data["appointments"].items() if ainfo["status"] == "Completed" and ainfo["patient_id"] == patient_id}
            if not completed_apps:
                print("Pasien ini belum memiliki janji yang selesai (Completed).")
                return
            for aid, ainfo in completed_apps.items():
                 sinfo = data["schedules"].get(ainfo["schedule_id"], {"doctor_id": "Tidak Ditemukan"})
                 doctor_info = data["doctors"].get(sinfo["doctor_id"], {"name": "Tidak Ditemukan"})
                 print(f"ID Janji: {aid}, Dokter: {doctor_info['name']}, Tanggal: {sinfo['available_date']}")
            appointment_id = input("Masukkan ID Janji sebagai dasar rawat inap: ")
            if appointment_id not in completed_apps:
                print("ID Janji tidak ditemukan atau bukan milik pasien ini atau belum selesai.")
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
                print("ID Ruangan tidak ditemukan atau tidak tersedia.")
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
                    print("Pasien sudah dikeluarkan.")
                    continue
                print(f"Data saat ini: ID Rawat Inap: {admission_id}, Pasien: {data['patients'].get(adinfo['patient_id'], {'name': 'Tidak Ditemukan'})['name']}, Status: {adinfo['status']}")
                confirm = input("Apakah pasien ini dikeluarkan sekarang? (y/n): ").lower()
                if confirm == 'y':
                    # Kembalikan status ruangan menjadi tersedia
                    data["rooms"][adinfo["room_id"]]["is_available"] = True
                    data["admissions"][admission_id]["status"] = "Discharged"
                    data["admissions"][admission_id]["discharge_date_actual"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_data(data)
                    print("Status rawat inap berhasil diubah menjadi 'Discharged'.")
                else:
                    print("Operasi dibatalkan.")
            else:
                print("ID Rawat Inap tidak ditemukan.")
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
                print("ID Rawat Inap tidak ditemukan.")
        elif choice == '0':
            break
        else:
            print("Pilihan tidak valid.")

# --- Fungsi Utama (Main Menu) ---
def main():
    data = load_data()

    while True:
        print("\n=== Aplikasi Reservasi Rumah Sakit (Versi Lengkap) ===")
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
                print("Role tidak dikenali.")
        elif choice == '2':
            register(data)
        elif choice == '3':
            print("Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()