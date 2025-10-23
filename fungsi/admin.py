import time
from colorama import Fore
from fungsi.color import *
from fungsi.core import *



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
