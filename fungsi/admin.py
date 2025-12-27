import time
from colorama import Fore
from fungsi.color import *
from fungsi.core import *



# --- Menu Admin ---
def menu_admin():
    while True:
        data = load_data() # Muat data setiap kali menu utama admin ditampilkan
        print(f"\n--- {H}Menu Admin{R} ---\n")
        print("1. Manajemen User")
        print("2. Manajemen Departemen")
        print("3. Manajemen Dokter")
        print("4. Manajemen Ruangan")
        print("5. Laporan Sederhana")
        print("0. Logout Admin")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            clear_screen()
            manajemen_user(data)
        elif pilihan == '2':
            clear_screen()
            manajemen_departemen(data)
        elif pilihan == '3':
            clear_screen()
            manajemen_dokter(data)
        elif pilihan == '4':
            clear_screen()
            manajemen_ruangan(data)
        elif pilihan == '5':
            clear_screen()
            laporan_sederhana()
        elif pilihan == '0':
            konfirmasi = input("Apakah Anda Yakin Ingin Logout? [Y/N] : ").lower()
            if konfirmasi == 'y':
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
        data = load_data() # Muat ulang data setiap kali menu manajemen user ditampilkan
        print(f"\n--- Manajemen User ({H}Admin{R}) ---") # f-string H & R untuk kode warna
        print("1. Lihat Semua User")
        print("2. Tambah User")
        print("3. Edit User")
        print("4. Hapus User")
        print("0. Kembali ke Menu Admin")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            print(f"\n{H}Daftar User:")
            for username, info_user in data["users"].items():
                print(f"Username: {username}, ID: {info_user['id']}, Peran: {info_user['role']}")
        elif pilihan == '2':
            username = input("Username Baru: ")
            kata_sandi = input("Password Baru: ")
            peran = input("Peran (admin/staff/user): ")
            if peran not in ['admin', 'staff', 'user']:
                print(Fore.RED + "Peran tidak valid.")
                time.sleep(3)
                clear_screen()
                continue
            if username in data["users"]:
                print(Fore.RED + "Username sudah digunakan.")
                continue
            
            # Membuat ID baru yang unik dan berurutan
            id_user_maks = 0
            for info_user in data["users"].values():
                try:
                    id_saat_ini = int(info_user["id"])
                    if id_saat_ini > id_user_maks:
                        id_user_maks = id_saat_ini
                except ValueError:
                    # Abaikan jika 'id' bukan angka
                    pass
            id_user = str(id_user_maks + 1)

            data["users"][username] = {"id": id_user, "password": kata_sandi, "role": peran}
            save_data(data)
            print(f"{H}[🗸] User berhasil ditambahkan.{R}")
            time.sleep(3)
            clear_screen() # Membersihkan layar setelah penambahan
        elif pilihan == '3':
            print(f"\n{H}Daftar User:")
            for username, info_user in data["users"].items():
                print(f"Username: {username}, ID: {info_user['id']}, Peran: {info_user['role']}")
            username = input("Username yang akan diedit: ")
            if username not in data["users"]:
                print(Fore.RED + "Username tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            info_user = data["users"][username]
            print(f"Data saat ini: Username: {username}, ID: {info_user['id']}, Peran: {info_user['role']}")
            peran_baru = input(f"Peran Baru (sekarang: {info_user['role']}): ") or info_user['role']
            if peran_baru not in ['admin', 'staff', 'user']:
                print("Peran tidak valid.")
                time.sleep(3)
                clear_screen()
                continue
            kata_sandi_baru = input("Kata Sandi Baru (tekan Enter jika tidak ingin diganti): ")
            if kata_sandi_baru:
                data["users"][username]["password"] = kata_sandi_baru
            data["users"][username]["role"] = peran_baru
            save_data(data)
            print(f"{H}[🗸] User berhasil diubah.{R}")
            time.sleep(3)
            clear_screen()
        elif pilihan == '4':
            print(f"\n{H}Daftar User:")
            for username, info_user in data["users"].items():
                print(f"Username: {username}, ID: {info_user['id']}, Peran: {info_user['role']}")
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
                user_baru_dict = {}
                # Urutkan berdasarkan username untuk konsistensi saat re-indexing
                item_user_diurutkan = sorted(data["users"].items())

                for i, (username, info_user) in enumerate(item_user_diurutkan):
                    id_baru = str(i + 1)
                    info_user["id"] = id_baru # Perbarui ID di dalam objek user
                    user_baru_dict[username] = info_user
                
                # Ganti dictionary users lama dengan yang baru
                data["users"] = user_baru_dict

                save_data(data)
                print(f"{H}[🗸] User berhasil dihapus dan ID telah diurutkan ulang.{R}")
                time.sleep(3)
                clear_screen()
            else:
                print(Fore.RED + "Username tidak ditemukan.")
                time.sleep(3)
                clear_screen()
        elif pilihan == '0':
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()



# --- Fungsi Manajemen Departemen (Admin) ---
def manajemen_departemen(data):
    while True:
        data = load_data() # Muat ulang data
        print(f"\n--- Manajemen Departemen ({H}Admin{R}) ---")
        print("1. Lihat Semua Departemen")
        print("2. Tambah Departemen")
        print("3. Edit Departemen")
        print("4. Hapus Departemen")
        print("0. Kembali ke Menu Admin")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            print(f"\n{H}Daftar Departemen:{R}")
            for id_dept, info_dept in data["departemen"].items():
                print(f"ID: {id_dept}, Nama: {info_dept['nama']}")
        elif pilihan == '2':
            name = input("Nama Departemen Baru: ").strip()
            if not name:
                print(Fore.RED + "Nama departemen tidak boleh kosong.")
                time.sleep(3)
                clear_screen()
                continue
            id_departemen = str(len(data["departemen"]) + 1)
            data["departemen"][id_departemen] = {"nama": name}
            save_data(data)
            print(f"{H}[🗸] Departemen berhasil ditambahkan.{R}")
            time.sleep(3)
            clear_screen()
        elif pilihan == '3':
            print(f"\n{H}Daftar Departemen:{R}")
            for id_dept, info_dept in data["departemen"].items():
                print(f"ID: {id_dept}, Nama: {info_dept['nama']}")
            id_departemen = input("ID Departemen yang akan diedit: ").strip() # Menambahkan .strip()
            if id_departemen not in data["departemen"]:
                print(Fore.RED + "ID Departemen tidak ditemukan.")
                time.sleep(3) # Menambahkan jeda waktu
                clear_screen()
                continue
            info_dept = data["departemen"][id_departemen]
            print(f"\nData saat ini: ID: {id_departemen}, Nama: {info_dept['nama']}")
            nama_baru = input(f"Nama Baru (sekarang: {info_dept['nama']}): ").strip()
            if not nama_baru:
                print(Fore.RED + "Nama departemen tidak boleh kosong. Pembatalan edit.")
                time.sleep(3)
                clear_screen()
                continue
            data["departemen"][id_departemen]["nama"] = nama_baru
            save_data(data)
            print(f"{H}[🗸] Departemen berhasil diubah.{R}")
            time.sleep(3)
            clear_screen()
        elif pilihan == '4':
            print(f"\n{H}Daftar Departemen:{R}")
            for id_dept, info_dept in data["departemen"].items():
                print(f"ID: {id_dept}, Nama: {info_dept['nama']}")
            id_departemen = input("ID Departemen yang akan dihapus: ").strip()
            if id_departemen not in data["departemen"]:
                print(Fore.RED + "ID Departemen tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            # Cek apakah ada dokter di departemen ini
            dokter_di_dept = [id_dokter for id_dokter, info_dokter in data["dokter"].items() if info_dokter["id_spesialis"] == id_departemen]
            if dokter_di_dept:
                print(Fore.RED + f"Departemen '{data['departemen'][id_departemen]['nama']}' masih memiliki dokter ({len(dokter_di_dept)}). Hapus dokter terlebih dahulu.")
                continue
            
            # Hapus departemen yang dipilih
            del data["departemen"][id_departemen]

            # --- Logika untuk mengurutkan ulang ID ---
            # 1. Buat dictionary departemen baru dan peta ID
            departemen_baru = {}
            peta_id = {}
            # Urutkan berdasarkan ID numerik untuk konsistensi
            id_lama_diurutkan = sorted(data["departemen"].keys(), key=int)

            for i, id_lama in enumerate(id_lama_diurutkan):
                id_baru = str(i + 1)
                departemen_baru[id_baru] = data["departemen"][id_lama]
                if id_lama != id_baru:
                    peta_id[id_lama] = id_baru
            
            # 2. Ganti dictionary departemen lama dengan yang baru
            data["departemen"] = departemen_baru

            # 3. Perbarui referensi 'id_spesialis' di data dokter
            for info_dokter in data["dokter"].values():
                if info_dokter["id_spesialis"] in peta_id:
                    info_dokter["id_spesialis"] = peta_id[info_dokter["id_spesialis"]]

            save_data(data)
            print(f"{H}[🗸] Departemen berhasil dihapus dan ID telah diurutkan ulang.{R}")
            time.sleep(3)
            clear_screen()
        elif pilihan == '0':
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()


# --- Fungsi Manajemen Dokter (Admin) ---
def manajemen_dokter(data):
    while True:
        data = load_data() # Muat ulang data
        print(f"\n--- Manajemen Dokter ({H}Admin{R}) ---")
        print("1. Lihat Semua Dokter")
        print("2. Tambah Dokter")
        print("3. Edit Dokter")
        print("4. Hapus Dokter")
        print("0. Kembali ke Menu Admin")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            print(f"\n{H}Daftar Dokter:{R}")
            for id_dokter, info_dokter in data["dokter"].items():
                nama_departemen = data["departemen"].get(info_dokter["id_spesialis"], {"nama": "Tidak Ditemukan"})["nama"]
                print(f"ID: {id_dokter}, Nama: {info_dokter['nama']}, Departemen: {nama_departemen}, Telp: {info_dokter['telepon']}")
        elif pilihan == '2':
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
            for id_dept, info_dept in data["departemen"].items():
                print(f"ID: {id_dept}, Nama: {info_dept['nama']}")
            id_spesialis = input("Pilih ID Departemen: ").strip()
            if id_spesialis not in data["departemen"]:
                print(Fore.RED + "ID Departemen tidak valid atau tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            
            # Membuat ID baru yang lebih andal
            id_dokter = str(max([int(k) for k in data["dokter"].keys()] or [0]) + 1)
            data["dokter"][id_dokter] = {"nama": name, "id_spesialis": id_spesialis, "telepon": phone}
            save_data(data)
            print(f"{H}[🗸] Dokter berhasil ditambahkan.{R}")
            time.sleep(3)
            clear_screen()
        elif pilihan == '3':
            print(f"\n{H}Daftar Dokter:{R}")
            for id_dokter, info_dokter in data["dokter"].items():
                nama_departemen = data["departemen"].get(info_dokter["id_spesialis"], {"nama": "Tidak Ditemukan"})["nama"]
                print(f"ID: {id_dokter}, Nama: {info_dokter['nama']}, Departemen: {nama_departemen}, Telp: {info_dokter['telepon']}")
            id_dokter = input("ID Dokter yang akan diedit: ")
            if id_dokter not in data["dokter"]:
                print(Fore.RED + "ID Dokter tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            info_dokter = data["dokter"][id_dokter]
            nama_departemen = data["departemen"].get(info_dokter["id_spesialis"], {"nama": "Tidak Ditemukan"})["nama"]
            print(f"Data saat ini: ID: {id_dokter}, Nama: {info_dokter['nama']}, Departemen: {nama_departemen}, Telp: {info_dokter['telepon']}")
            nama_baru = input(f"Nama Baru (sekarang: {info_dokter['nama']}): ") or info_dokter['nama']
            telepon_baru = input(f"Telp Baru (sekarang: {info_dokter['telepon']}): ") or info_dokter['telepon']
            print(f"\n{H}Daftar Departemen:{R}")
            for id_dept, info_dept in data["departemen"].items():
                print(f"ID: {id_dept}, Nama: {info_dept['nama']}")
            id_spesialis_baru = input(f"ID Departemen Baru (sekarang: {info_dokter['id_spesialis']}): ") or info_dokter['id_spesialis']
            if id_spesialis_baru not in data["departemen"]:
                print(Fore.RED + "ID Departemen tidak ditemukan.")
                clear_screen()
                continue
            data["dokter"][id_dokter] = {"nama": nama_baru, "id_spesialis": id_spesialis_baru, "telepon": telepon_baru}
            save_data(data)
            print(f"{H}[🗸] Dokter berhasil diubah.{R}")
            time.sleep(3)
            clear_screen()
        elif pilihan == '4':
            print(f"\n{H}Daftar Dokter:{R}")
            for id_dokter, info_dokter in data["dokter"].items():
                nama_departemen = data["departemen"].get(info_dokter["id_spesialis"], {"nama": "Tidak Ditemukan"})["nama"]
                print(f"ID: {id_dokter}, Nama: {info_dokter['nama']}, Departemen: {nama_departemen}, Telp: {info_dokter['telepon']}")
            id_dokter = input("ID Dokter yang akan dihapus: ").strip()
            if id_dokter not in data["dokter"]:
                print(Fore.RED + "ID Dokter tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            # Cek apakah ada jadwal aktif untuk dokter ini
            jadwal_dokter = [sid for sid, info_jadwal in data["jadwal"].items() if info_jadwal["id_dokter"] == id_dokter]
            if jadwal_dokter:
                print(Fore.RED + f"Dokter '{data['dokter'][id_dokter]['nama']}' masih memiliki jadwal aktif. Hapus jadwal terlebih dahulu.")
                continue
            
            # Hapus dokter yang dipilih
            del data["dokter"][id_dokter]

            # --- Logika untuk mengurutkan ulang ID ---
            # 1. Buat dictionary dokter baru dan peta ID
            dokter_baru = {}
            peta_id = {}
            # Urutkan berdasarkan ID numerik untuk konsistensi
            id_lama_diurutkan = sorted(data["dokter"].keys(), key=int)

            for i, id_lama in enumerate(id_lama_diurutkan):
                id_baru = str(i + 1)
                dokter_baru[id_baru] = data["dokter"][id_lama]
                if id_lama != id_baru:
                    peta_id[id_lama] = id_baru
            
            # 2. Ganti dictionary dokter lama dengan yang baru
            data["dokter"] = dokter_baru

            # 3. Perbarui referensi di 'schedules' (jadwal)
            for schedule_id, schedule_info in data["jadwal"].items():
                if schedule_info["id_dokter"] in peta_id:
                    schedule_info["id_dokter"] = peta_id[schedule_info["id_dokter"]]

            save_data(data)
            print(f"{H}[🗸] Dokter berhasil dihapus dan ID telah diurutkan ulang.{R}")
            time.sleep(3)
            clear_screen()
        elif pilihan == '0':
            clear_screen()
            # Cukup break untuk kembali ke menu admin utama, yang akan memuat ulang data
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()



# --- Fungsi Manajemen Ruangan (Admin) ---
def manajemen_ruangan(data):
    while True:
        data = load_data() # Muat ulang data
        print(f"\n--- Manajemen Ruangan ({H}Admin{R}) ---")
        print("1. Lihat Semua Ruangan")
        print("2. Tambah Ruangan")
        print("3. Edit Ruangan")
        print("4. Hapus Ruangan")
        print("0. Kembali ke Menu Admin")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            print(f"\n{H}Daftar Ruangan:{R}")
            for id_kamar, info_kamar in data["kamar"].items():
                tersedia = info_kamar.get("tersedia", True)
                teks_status = "Tersedia" if tersedia else "Tidak Tersedia"
                warna_status = Fore.GREEN if tersedia else Fore.YELLOW
                print(f"ID: {id_kamar}, Nama: {info_kamar['nama']}, Tipe: {info_kamar['tipe']}, Status: {warna_status}{teks_status}{R}")
        elif pilihan == '2':
            name = input("Nama Ruangan Baru: ").strip()
            if not name:
                print(Fore.RED + "Nama ruangan tidak boleh kosong.")
                time.sleep(3)
                clear_screen()
                continue

            tipe_kamar = input("Tipe Ruangan (VIP/Kelas 1/Kelas 2/Kelas 3): ").strip()
            if not tipe_kamar:
                print(Fore.RED + "Tipe ruangan tidak boleh kosong.")
                time.sleep(3)
                clear_screen()
                continue

            # Membuat ID baru yang lebih andal
            id_kamar = str(max([int(k) for k in data["kamar"].keys()] or [0]) + 1)
            data["kamar"][id_kamar] = {"nama": name, "tipe": tipe_kamar, "tersedia": True}
            save_data(data)
            print(f"{H}[🗸] Ruangan berhasil ditambahkan.{R}")
            time.sleep(3)
            clear_screen()
        elif pilihan == '3':
            print(f"\n{H}Daftar Ruangan:{R}")
            for id_kamar, info_kamar in data["kamar"].items():
                tersedia = info_kamar.get("tersedia", True)
                teks_status = "Tersedia" if tersedia else "Tidak Tersedia"
                warna_status = Fore.GREEN if tersedia else Fore.YELLOW
                print(f"ID: {id_kamar}, Nama: {info_kamar['nama']}, Tipe: {info_kamar['tipe']}, Status: {warna_status}{teks_status}{R}")
            id_kamar = input("ID Ruangan yang akan diedit: ").strip()
            if not id_kamar:
                print(Fore.RED + "ID Ruangan tidak boleh kosong.")
                time.sleep(3)
                clear_screen()
                continue
            if id_kamar not in data["kamar"]:
                print(Fore.RED + "ID Ruangan tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            info_kamar = data["kamar"][id_kamar]
            print(f"Data saat ini: ID: {id_kamar}, Nama: {info_kamar['nama']}, Tipe: {info_kamar['tipe']}, Tersedia: {info_kamar.get('tersedia', True)}")
            nama_baru = input(f"Nama Baru (sekarang: {info_kamar['nama']}): ") or info_kamar['nama']
            tipe_baru = input(f"Tipe Baru (sekarang: {info_kamar['tipe']}): ") or info_kamar['tipe']
            status_saat_ini = info_kamar.get('tersedia', True)
            label_status = "Tersedia" if status_saat_ini else "Tidak Tersedia"
            status_input = input(f"Ubah Status Ketersediaan? (y=Tersedia, n=Tidak Tersedia, Enter=Tetap [{label_status}]): ").lower().strip()
            
            status_baru = status_saat_ini
            if status_input == 'y':
                status_baru = True
            elif status_input == 'n':
                status_baru = False

            data["kamar"][id_kamar] = {"nama": nama_baru, "tipe": tipe_baru, "tersedia": status_baru}
            save_data(data)
            print(f"{H}[🗸] Ruangan berhasil diubah.{R}")
            time.sleep(3)
            clear_screen()
        elif pilihan == '4':
            print(f"\n{H}Daftar Ruangan:{R}")
            for id_kamar, info_kamar in data["kamar"].items():
                tersedia = info_kamar.get("tersedia", True)
                teks_status = "Tersedia" if tersedia else "Tidak Tersedia"
                warna_status = Fore.GREEN if tersedia else Fore.YELLOW
                print(f"ID: {id_kamar}, Nama: {info_kamar['nama']}, Tipe: {info_kamar['tipe']}, Status: {warna_status}{teks_status}{R}")
            id_kamar = input("ID Ruangan yang akan dihapus: ")
            if id_kamar not in data["kamar"]:
                print(Fore.RED + "ID Ruangan tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                continue
            info_kamar = data["kamar"][id_kamar]
            if not info_kamar.get("tersedia", True): # Jika tidak tersedia, berarti sedang digunakan
                print(Fore.RED + f"Ruangan '{info_kamar['nama']}' sedang digunakan (tidak tersedia). Hapus data rawat inap terlebih dahulu.")
                continue
            
            # Hapus ruangan yang dipilih
            del data["kamar"][id_kamar]

            # --- Logika untuk mengurutkan ulang ID ---
            # 1. Buat dictionary ruangan baru dan peta ID
            kamar_baru = {}
            peta_id = {}
            # Urutkan berdasarkan ID numerik untuk konsistensi
            id_lama_diurutkan = sorted(data["kamar"].keys(), key=int)
            
            for i, id_lama in enumerate(id_lama_diurutkan):
                id_baru = str(i + 1)
                kamar_baru[id_baru] = data["kamar"][id_lama]
                if id_lama != id_baru:
                    peta_id[id_lama] = id_baru
            
            # 2. Ganti dictionary ruangan lama dengan yang baru
            data["kamar"] = kamar_baru

            # 3. Perbarui referensi di 'admissions' (rawat inap)
            for id_rawat_inap, info_rawat_inap in data["rawat_inap"].items():
                if info_rawat_inap["id_kamar"] in peta_id:
                    info_rawat_inap["id_kamar"] = peta_id[info_rawat_inap["id_kamar"]]
            
            save_data(data)
            print(f"{H}[🗸] Ruangan berhasil dihapus.{R}")
            time.sleep(3)
            clear_screen()
        elif pilihan == '0':
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()



# --- Fungsi Laporan Sederhana (Admin) ---
def laporan_sederhana():
    data = load_data()
    print(f"\n--- Laporan Sederhana ({H}Admin{R}) ---")
    print("1. Laporan Janji Harian")
    print("2. Laporan Pasien per Departemen")
    print("3. Laporan Ruangan Tersedia")
    pilihan_sub = input("Pilih laporan: ")

    if pilihan_sub == '1':
        tanggal = input("Masukkan Tanggal (YYYY-MM-DD): ")
        print(f"\n{H}Laporan Janji untuk Tanggal:{R} {tanggal}")
        ditemukan = False
        for id_janji, info_janji in data["janji_temu"].items():
            info_jadwal = data["jadwal"].get(info_janji["id_jadwal"], {})
            if info_jadwal.get("tanggal_tersedia") == tanggal:
                ditemukan = True
                info_pasien = data["pasien"].get(info_janji["id_pasien"], {"nama": "Tidak Ditemukan"})
                info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {"nama": "Tidak Ditemukan"})
                print(f"ID Janji: {id_janji}, Pasien: {info_pasien['nama']}, Dokter: {info_dokter['nama']}, Status: {H}{info_janji['status']}{R}")
        if not ditemukan:
            print(Fore.YELLOW + "Tidak Ada data Laporan Janji harian")
            time.sleep(3)
            clear_screen()
    elif pilihan_sub == '2':
        print(f"\n{H}Laporan Jumlah Pasien per Departemen:{R}")
        jumlah_per_dept = {}
        for id_janji, info_janji in data["janji_temu"].items():
            info_jadwal = data["jadwal"].get(info_janji["id_jadwal"], {})
            info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {})
            id_departemen = info_dokter.get("id_spesialis")
            if id_departemen:
                nama_departemen = data["departemen"].get(id_departemen, {"nama": "Tidak Ditemukan"})["nama"]
                jumlah_per_dept[nama_departemen] = jumlah_per_dept.get(nama_departemen, 0) + 1
        if not jumlah_per_dept:
            print(Fore.YELLOW + "Tidak Ada data Laporan Pasien per Departemen")
            time.sleep(3)
            clear_screen()
        else:
            for nama_departemen, jumlah in jumlah_per_dept.items():
                print(f"Departemen: {nama_departemen}, Jumlah Pasien: {jumlah}")
    elif pilihan_sub == '3':
        print(f"\n{H}Laporan Ruangan Tersedia:{R}")
        kamar_tersedia = [info_kamar for info_kamar in data["kamar"].values() if info_kamar.get("tersedia", True)]
        if not kamar_tersedia:
            print(Fore.YELLOW + "Tidak ada ruangan yang tersedia saat ini.")
        else:
            for info_kamar in kamar_tersedia:
                print(f"Nama: {info_kamar['nama']}, Tipe: {info_kamar['tipe']}")
    else:
        print(Fore.RED + "Pilihan tidak valid.")
        time.sleep(3)
        clear_screen()
