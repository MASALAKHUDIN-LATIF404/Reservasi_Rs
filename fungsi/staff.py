import datetime
import time
from colorama import Fore
from fungsi.color import *
from fungsi.core import *


H = "\033[92m" # warna hijau
M = "\033[91m" # warna merah
R = "\033[0m" # reset warna





def menu_staff():
    while True:
        data = load_data() # data menu staff
        print(f"\n--- {H}Menu Staff{R} ---")
        print("1. Data Pasien")
        print("2. Data Jadwal") 
        print("3. Data Janji")
        print("4. Buat Janji")
        print("5. Data CheckUp")
        print("6. Data Rawat Inap")
        print("7. Data Pembayaran")
        print("0. Logout Menu Staff")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            clear_screen()
            data_pasien(data)
        elif pilihan == '2':
            clear_screen()
            data_jadwal(data)
        elif pilihan == '3':
            clear_screen()
            data_janji(data)
        elif pilihan == '4':
            clear_screen()
            buat_janji()
        elif pilihan == '5':
            clear_screen()
            data_checkup(data)
        elif pilihan == '6':
            clear_screen()
            data_rawat_inap(data)
        elif pilihan == '7':
            clear_screen()
            menu_pembayaran(data)
        elif pilihan == '0':
            konfirmasi = input("Apakah Anda Yakin Ingin Logout Menu Staff? [Y/N] : ").lower()
            if konfirmasi == 'y':
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

# --- Fungsi Data Pasien (Staff) ---
def data_pasien(data):
    while True:
        data = load_data() # Muat ulang data
        print(f"\n--- Data Pasien ({H}Staff{R}) ---")
        print("1. Lihat Semua Pasien")
        print("2. Tambah Pasien Baru")
        print("3. Edit Pasien")
        print("4. Hapus Pasien")
        print("0. Kembali ke Menu Staff")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            if not data["pasien"]:
                print(Fore.YELLOW + "\nBelum ada data pasien.")
                time.sleep(3)
                clear_screen()
            else:
                print(Fore.YELLOW + "Daftar Pasien:")
                for id_pasien_iter, info_pasien in data["pasien"].items():
                    print(f"ID: {id_pasien_iter}, Nama: {info_pasien['nama']}, Telp: {info_pasien['telepon']}, Alamat: {info_pasien['alamat']}, Tanggal Lahir: {info_pasien['tanggal_lahir']}")
        elif pilihan == '2':
            nama = input("Nama Pasien: ")
            telepon = input("Nomor Telepon: ")
            alamat = input("Alamat: ")
            tanggal_lahir = input("Tanggal Lahir (YYYY-MM-DD): ")
            
            print(f"\n{H}Buat Akun Login untuk Pasien:{R}")
            while True:
                username = input("Username Baru: ").strip()
                if not username:
                    print(Fore.RED + "Username tidak boleh kosong.")
                    continue
                if username in data["users"]:
                    print(Fore.RED + "Username sudah digunakan. Silakan pilih yang lain.")
                    continue
                break
            
            password = input("Password Baru: ").strip()
            if not password:
                 print(Fore.RED + "Password tidak boleh kosong. Menggunakan default '123456'")
                 password = "123456"

            # Menggunakan metode pembuatan ID yang lebih aman
            id_maks = max([int(k) for k in data["pasien"].keys()] or [0])
            id_pasien = str(id_maks + 1)
            
            # Buat Patient Data
            data["pasien"][id_pasien] = {
                "nama": nama,
                "telepon": telepon,
                "alamat": alamat,
                "tanggal_lahir": tanggal_lahir,
                "dibuat_pada": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Buat User Data
            id_user_maks = 0
            for info_user in data["users"].values():
                try:
                    id_saat_ini = int(info_user["id"])
                    if id_saat_ini > id_user_maks:
                        id_user_maks = id_saat_ini
                except ValueError:
                    pass
            id_user = str(id_user_maks + 1)

            data["users"][username] = {
                "id": id_user,
                "password": password,
                "role": "user",
                "id_pasien": id_pasien
            }
            save_data(data)
            print(f"{H}[🗸] Data pasien berhasil ditambahkan.{R}")
            time.sleep(4)
            clear_screen()
        elif pilihan == '3':
            print(f"\n{H}Daftar Pasien:{R}")
            for id_pasien_iter, info_pasien in data["pasien"].items():
                print(f"ID: {id_pasien_iter}, Nama: {info_pasien['nama']}, Telp: {info_pasien['telepon']}, Alamat: {info_pasien['alamat']}, Tanggal Lahir: {info_pasien['tanggal_lahir']}")
            id_pasien = input("Masukkan ID Pasien yang akan diedit: ")
            if id_pasien in data["pasien"]:
                info_pasien = data["pasien"][id_pasien]
                print(f"Data saat ini: ID: {id_pasien}, Nama: {info_pasien['nama']}, Telp: {info_pasien['telepon']}, Alamat: {info_pasien['alamat']}, Tanggal Lahir: {info_pasien['tanggal_lahir']}")
                nama_baru = input(f"Nama Baru (sekarang: {info_pasien['nama']}): ") or info_pasien['nama']
                telepon_baru = input(f"Telp Baru (sekarang: {info_pasien['telepon']}): ") or info_pasien['telepon']
                alamat_baru = input(f"Alamat Baru (sekarang: {info_pasien['alamat']}): ") or info_pasien['alamat']
                tgl_lahir_baru = input(f"Tgl Lahir Baru (sekarang: {info_pasien['tanggal_lahir']}): ") or info_pasien['tanggal_lahir']
                data["pasien"][id_pasien] = {
                    "nama": nama_baru,
                    "telepon": telepon_baru,
                    "alamat": alamat_baru,
                    "tanggal_lahir": tgl_lahir_baru,
                    "dibuat_pada": info_pasien["dibuat_pada"]
                }
                save_data(data)
                print(f"{H}[🗸] Data pasien berhasil diubah.{R}")
                time.sleep(3)
                clear_screen()
            else:
                print(Fore.RED + "ID Pasien tidak ditemukan.")
        elif pilihan == '4':
            print(f"\n{H}Daftar Pasien:{R}")
            for id_pasien_iter, info_pasien in data["pasien"].items():
                print(f"ID: {id_pasien_iter}, Nama: {info_pasien['nama']}, Telp: {info_pasien['telepon']}, Alamat: {info_pasien['alamat']}, Tanggal Lahir: {info_pasien['tanggal_lahir']}")
            id_pasien = input("Masukkan ID Pasien yang akan dihapus: ")
            if id_pasien in data["pasien"]:
                del data["pasien"][id_pasien]
                janji_yg_dihapus = []
                # Hapus janji, checkup, dan rawat inap yang terkait dengan pasien
                for id_janji, info_janji in data["janji_temu"].items():
                    if info_janji["id_pasien"] == id_pasien:
                        janji_yg_dihapus.append(id_janji)
                for id_janji in janji_yg_dihapus:
                    periksa_yg_dihapus = []
                    for id_periksa, info_periksa in data["pemeriksaan"].items():
                        if info_periksa["id_janji_temu"] == id_janji:
                            periksa_yg_dihapus.append(id_periksa)
                    for id_periksa in periksa_yg_dihapus:
                        del data["pemeriksaan"][id_periksa]
                    del data["janji_temu"][id_janji]
                
                rawat_inap_yg_dihapus = []
                for id_rawat, info_rawat in data["rawat_inap"].items():
                    if info_rawat["id_pasien"] == id_pasien:
                        rawat_inap_yg_dihapus.append(id_rawat)
                for id_rawat in rawat_inap_yg_dihapus:
                    # Kembalikan status ruangan
                    id_kamar = info_rawat["id_kamar"]
                    data["kamar"][id_kamar]["tersedia"] = True
                    del data["rawat_inap"][id_rawat]

                # --- Logika untuk mengurutkan ulang ID Pasien ---
                pasien_baru = {}
                peta_id = {}
                # Urutkan ID lama secara numerik untuk konsistensi
                id_lama_diurutkan = sorted(data["pasien"].keys(), key=int)

                for i, id_lama in enumerate(id_lama_diurutkan):
                    id_baru = str(i + 1)
                    pasien_baru[id_baru] = data["pasien"][id_lama]
                    if id_lama != id_baru:
                        peta_id[id_lama] = id_baru
                
                # Ganti dictionary patients lama dengan yang baru
                data["pasien"] = pasien_baru

                # Perbarui referensi id_pasien di appointments dan admissions
                for dict_entitas in [data["janji_temu"], data["rawat_inap"]]:
                    for info_entitas in dict_entitas.values():
                        if info_entitas.get("id_pasien") in peta_id:
                            info_entitas["id_pasien"] = peta_id[info_entitas["id_pasien"]]
                
                save_data(data)
                print(f"{H}[🗸] Data pasien berhasil dihapus dan semua ID terkait telah diurutkan ulang.{R}")
                time.sleep(4)
                clear_screen()
            else:
                print(Fore.RED + "ID Pasien tidak ditemukan.")
        elif pilihan == '0':
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()



# --- Fungsi Data Jadwal (Staff) ---
def data_jadwal(data):
    while True:
        data = load_data()
        print(f"\n--- Data Jadwal ({H}Staff{R}) ---")
        print("1. Lihat Semua Jadwal")
        print("2. Tambah Jadwal Baru")
        print("3. Edit Jadwal")
        print("4. Hapus Jadwal")
        print("0. Kembali ke Menu Staff")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            if not data["jadwal"]:
                print(Fore.YELLOW + "\nBelum ada data jadwal.")
                time.sleep(3)
                clear_screen()
            else:
                print(f"\n{H}Daftar Jadwal:{R}")
                for id_jadwal, info_jadwal in data["jadwal"].items():
                    info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {"nama": "Tidak Ditemukan"})
                    nama_departemen = data["departemen"].get(data["dokter"].get(info_jadwal["id_dokter"], {}).get("id_spesialis"), {"nama": "Tidak Ditemukan"})["nama"]
                    tersedia = info_jadwal.get("tersedia", True)
                    if tersedia:
                        tampilan_status = f"{Fore.GREEN}Tersedia{R}"
                    else:
                        tampilan_status = f"{Fore.YELLOW}Tidak Tersedia{R} {M}Terpakai ( Database System ){R}"
                    print(f"ID: {id_jadwal}, Dokter: {info_dokter['nama']}, Departemen: {nama_departemen}, Tanggal: {info_jadwal['tanggal_tersedia']}, Waktu: {info_jadwal['waktu_tersedia']}, Status: {tampilan_status}")
        elif pilihan == '2':
            print(f"\n{H}Daftar Dokter:{R}")
            for id_dokter_iter, info_dokter in data["dokter"].items():
                nama_departemen = data["departemen"].get(info_dokter["id_spesialis"], {"nama": "Tidak Ditemukan"})["nama"]
                print(f"ID: {id_dokter_iter}, Nama: {info_dokter['nama']}, Departemen: {nama_departemen}")
            id_dokter = input("ID Dokter: ")
            if id_dokter not in data["dokter"]:
                print(Fore.RED + "ID Dokter tidak ditemukan.")
                return
            tanggal = input("Tanggal Tersedia (YYYY-MM-DD): ")
            waktu_jadwal = input("Waktu Tersedia (HH:MM - HH:MM): ")
            id_jadwal = str(len(data["jadwal"]) + 1)
            data["jadwal"][id_jadwal] = {
                "id_dokter": id_dokter,
                "tanggal_tersedia": tanggal,
                "waktu_tersedia": waktu_jadwal,
                "tersedia": True
            }
            save_data(data)
            print(F"{H}[🗸] Jadwal dokter berhasil ditambahkan.{R}")
            time.sleep(3)
            clear_screen()
        elif pilihan == '3':
            print(f"\n{H}Daftar Jadwal Tersedia untuk Diedit:{R}")
            jadwal_tersedia_ditemukan = False
            for id_jadwal, info_jadwal in data["jadwal"].items():
                info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {"nama": "Tidak Ditemukan"})
                nama_departemen = data["departemen"].get(data["dokter"].get(info_jadwal["id_dokter"], {}).get("id_spesialis"), {"nama": "Tidak Ditemukan"})["nama"]
                tersedia = info_jadwal.get("tersedia", True)
                teks_status = "Tersedia" if tersedia else "Tidak Tersedia"
                warna_status = Fore.GREEN if tersedia else Fore.YELLOW
                if tersedia: # Hanya tampilkan jadwal yang tersedia
                    jadwal_tersedia_ditemukan = True
                    print(f"ID: {id_jadwal}, Dokter: {info_dokter['nama']}, Departemen: {nama_departemen}, Tanggal: {info_jadwal['tanggal_tersedia']}, Waktu: {info_jadwal['waktu_tersedia']}, Status: {warna_status}{teks_status}{R}")
            if not jadwal_tersedia_ditemukan:
                print(Fore.YELLOW + "Tidak ada jadwal tersedia yang dapat diedit.")
                time.sleep(3)
                clear_screen()
                continue
            id_jadwal = input("Masukkan ID Jadwal yang akan diedit: ")
            if id_jadwal in data["jadwal"]:
                info_jadwal = data["jadwal"][id_jadwal]
                info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {"nama": "Tidak Ditemukan"})
                print(f"Data saat ini: ID: {id_jadwal}, Dokter: {info_dokter['nama']}, Tanggal: {info_jadwal['tanggal_tersedia']}, Waktu: {info_jadwal['waktu_tersedia']}")
                print("\nDaftar Dokter:")
                for id_dokter_iter, info_dokter in data["dokter"].items():
                    nama_departemen = data["departemen"].get(info_dokter["id_spesialis"], {"nama": "Tidak Ditemukan"})["nama"]
                    print(f"ID: {id_dokter_iter}, Nama: {info_dokter['nama']}, Departemen: {nama_departemen}")
                id_dokter_baru = input(f"ID Dokter Baru (sekarang: {info_jadwal['id_dokter']}): ") or info_jadwal['id_dokter']
                if id_dokter_baru not in data["dokter"]:
                    print(Fore.RED + "ID Dokter tidak ditemukan.")
                    return
                tanggal_baru = input(f"Tanggal Baru (sekarang: {info_jadwal['tanggal_tersedia']}): ") or info_jadwal['tanggal_tersedia']
                waktu_baru = input(f"Waktu Baru (sekarang: {info_jadwal['waktu_tersedia']}): ") or info_jadwal['waktu_tersedia']
                if not info_jadwal.get("tersedia", True):
                     print(Fore.YELLOW + "Peringatan: Jadwal ini sedang dipesan. Edit mungkin mempengaruhi janji yang sudah dibuat.")
                data["jadwal"][id_jadwal] = {
                    "id_dokter": id_dokter_baru,
                    "tanggal_tersedia": tanggal_baru,
                    "waktu_tersedia": waktu_baru,
                    "tersedia": info_jadwal.get("tersedia", True)
                }
                save_data(data)
                print(f"{H}[🗸] Jadwal dokter berhasil diubah.{R}")
            else:
                print(Fore.RED + "ID Jadwal tidak ditemukan.")
                time.sleep(3)
                clear_screen()
        elif pilihan == '4':
            print(f"\n{H}Daftar Jadwal Tersedia untuk Dihapus:{R}")
            jadwal_tersedia_ditemukan = False
            for id_jadwal, info_jadwal in data["jadwal"].items():
                info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {"nama": "Tidak Ditemukan"})
                nama_departemen = data["departemen"].get(data["dokter"].get(info_jadwal["id_dokter"], {}).get("id_spesialis"), {"nama": "Tidak Ditemukan"})["nama"]
                tersedia = info_jadwal.get("tersedia", True)
                if tersedia: # Hanya tampilkan jadwal yang tersedia
                    jadwal_tersedia_ditemukan = True
                    print(f"ID: {id_jadwal}, Dokter: {info_dokter['nama']}, Departemen: {nama_departemen}, Tanggal: {info_jadwal['tanggal_tersedia']}, Waktu: {info_jadwal['waktu_tersedia']}")
            if not jadwal_tersedia_ditemukan:
                print(Fore.YELLOW + "Tidak ada jadwal tersedia yang dapat dihapus.")
                time.sleep(3)
                clear_screen()
                continue
            id_jadwal = input("Masukkan ID Jadwal yang akan dihapus: ")
            if id_jadwal in data["jadwal"]:
                info_jadwal = data["jadwal"][id_jadwal]
                sudah_dipesan = any(info_janji["id_jadwal"] == id_jadwal for info_janji in data["janji_temu"].values())
                if sudah_dipesan:
                    print(Fore.RED + f"Jadwal ID {id_jadwal} sedang dipesan oleh pasien. Tidak bisa dihapus.")
                else:
                    # Hapus jadwal yang dipilih
                    del data["jadwal"][id_jadwal]

                    # --- Logika untuk mengurutkan ulang ID Jadwal ---
                    jadwal_baru = {}
                    peta_id = {}
                    # Urutkan ID lama secara numerik untuk konsisten
                    id_lama_diurutkan = sorted(data["jadwal"].keys(), key=int)

                    for i, id_lama in enumerate(id_lama_diurutkan):
                        id_baru = str(i + 1)
                        jadwal_baru[id_baru] = data["jadwal"][id_lama]
                        if id_lama != id_baru:
                            peta_id[id_lama] = id_baru
                    
                    # Ganti dictionary lama ke yang baru
                    data["jadwal"] = jadwal_baru

                    # Perbarui referensi id_jadwal di appointments
                    for info_janji in data["janji_temu"].values():
                        if info_janji.get("id_jadwal") in peta_id:
                            info_janji["id_jadwal"] = peta_id[info_janji["id_jadwal"]]

                    save_data(data)
                    print(f"{H}[🗸] Jadwal dokter berhasil dihapus dan semua ID terkait telah diurutkan ulang.{R}")
            else:
                print(Fore.RED + "ID Jadwal tidak ditemukan.")
        elif pilihan == '0':
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()


#Fungsi untuk Buat Janji (Staff)
def buat_janji():
    data = load_data()
    print(f"\n--- Buat Janji Baru ({H}Staff{R}) ---")
    
    
    print(f"{H}Daftar Pasien:{R}")
    for id_pasien_iter, info_pasien in data["pasien"].items():
        print(f"ID: {id_pasien_iter}, Nama: {info_pasien['nama']}")
    id_pasien = input("Masukkan ID Pasien: ")
    if id_pasien not in data["pasien"]:
        print(Fore.RED + "ID Pasien tidak ditemukan.")
        time.sleep(3)
        clear_screen()
        return

    print(f"\n{H}Jadwal yang Tersedia:{R}")
    jadwal_yg_tersedia = {id_jadwal: info_jadwal for id_jadwal, info_jadwal in data["jadwal"].items() if info_jadwal.get("tersedia", True)}
    if not jadwal_yg_tersedia:
        print(Fore.YELLOW + "Tidak ada jadwal yang tersedia saat ini.")
        return
    for id_jadwal, info_jadwal in jadwal_yg_tersedia.items():
        info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {"nama": "Tidak Ditemukan"})
        nama_departemen = data["departemen"].get(data["dokter"].get(info_jadwal["id_dokter"], {}).get("id_spesialis"), {"nama": "Tidak Ditemukan"})["nama"]
        print(f"ID: {id_jadwal}, Dokter: {info_dokter['nama']}, Departemen: {nama_departemen}, Tanggal: {info_jadwal['tanggal_tersedia']}, Waktu: {info_jadwal['waktu_tersedia']}")
    id_jadwal = input("\nMasukkan ID Jadwal: ")
    if id_jadwal not in jadwal_yg_tersedia:
        print(Fore.RED + "ID Jadwal tidak ditemukan atau tidak tersedia.")
        time.sleep(3)
        clear_screen()
        return

    id_janji = str(len(data["janji_temu"]) + 1)
    data["janji_temu"][id_janji] = {
        "id_pasien": id_pasien,
        "id_jadwal": id_jadwal,
        "tanggal_pemesanan": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Terjadwal"
    }
    data["jadwal"][id_jadwal]["tersedia"] = False

    #Otomatis buat data pembayaran untuk janji baru (Integrasi)
    print(f"\n{H}--- Input Data Pembayaran untuk Janji Baru ---{R}")
    print("Jenis Layanan:")
    print("1. Konsultasi Umum (Rp 150.000)")
    print("2. Konsultasi Spesialis (Rp 250.000)")
    print("3. Emergency (Rp 500.000)")
    print("4. Lainnya (Input Manual)")

    pilihan_layanan = input("Pilih jenis layanan (1-4): ")
    jumlah = 0
    jenis_layanan = ""

    if pilihan_layanan == '1':
        jumlah = 150000
        jenis_layanan = "Konsultasi Umum"
    elif pilihan_layanan == '2':
        jumlah = 250000
        jenis_layanan = "Konsultasi Spesialis"
    elif pilihan_layanan == '3':
        jumlah = 500000
        jenis_layanan = "Emergency"
    elif pilihan_layanan == '4':
        try:
            jenis_layanan = input("Jenis layanan: ")
            jumlah = int(input("Masukkan jumlah biaya manual: Rp "))
            if not jenis_layanan: 
                jenis_layanan = "Layanan Lainnya"
        except ValueError:
            print(Fore.RED + "Input jumlah tidak valid. Menggunakan default Konsultasi Umum.")
            jumlah = 150000
            jenis_layanan = "Konsultasi Umum"
    else:
        print(Fore.YELLOW + "Pilihan tidak valid. Menggunakan default Konsultasi Umum.")
        jumlah = 150000
        jenis_layanan = "Konsultasi Umum"

    id_pembayaran = str(len(data["pembayaran"]) + 1)
    data["pembayaran"][id_pembayaran] = {
        "id_janji_temu": id_janji,
        "id_pasien": id_pasien,
        "jumlah": jumlah,
        "tanggal_pembayaran": "",
        "status": "Menunggu",
        "metode_pembayaran": "",
        "jenis_layanan": jenis_layanan
    }
    #Akhir integrasi pembayaran

    save_data(data) # Simpan data setelah janji dan pembayaran dibuat

    print(f"{H}[🗸] Janji berhasil dibuat dan tagihan telah dicatat!{R}")
    janji_baru = data["janji_temu"][id_janji]
    info_pasien = data["pasien"][id_pasien]
    info_jadwal = data["jadwal"][id_jadwal]
    info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {"nama": "Tidak Ditemukan"})
    nama_departemen = data["departemen"].get(data["dokter"].get(info_jadwal["id_dokter"], {}).get("id_spesialis"), {"nama": "Tidak Ditemukan"})["nama"]
    print(f"\nKonfirmasi Janji:")
    print(f"ID Janji: {id_janji}")
    print(f"Nama Pasien: {info_pasien['nama']}")
    print(f"Dokter: {info_dokter['nama']}")
    print(f"Departemen: {nama_departemen}")
    print(f"Tanggal: {info_jadwal['tanggal_tersedia']}")
    print(f"Waktu: {info_jadwal['waktu_tersedia']}")
    print(f"Status: {H}{janji_baru['status']}{R}")
    print(f"Tagihan Pembayaran: ID {id_pembayaran}, Jumlah Rp {jumlah:,}, Layanan: {jenis_layanan}, Status: {Fore.YELLOW}Pending{R}")
    time.sleep(5) # Memberi waktu pengguna untuk membaca konfirmasi
    clear_screen()

#Fungsi Data Janji (Staff)
def data_janji(data):
    while True:
        data = load_data()
        print(f"\n--- Data Janji ({H}Staff{R}) ---")
        print("1. Lihat Semua Janji")
        print("2. Hapus Janji")
        print("0. Kembali ke Menu Staff")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            if not data["janji_temu"]:
                print(Fore.YELLOW + "Belum ada data janji.")
            else:
                print(f"\n{H}Daftar Janji:{R}")
                for id_janji, info_janji in data["janji_temu"].items():
                    info_pasien = data["pasien"].get(info_janji["id_pasien"], {"nama": "Tidak Ditemukan"})
                    info_jadwal = data["jadwal"].get(info_janji["id_jadwal"], {"id_dokter": "Tidak Ditemukan"})
                    info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {"nama": "Tidak Ditemukan"})
                    nama_departemen = data["departemen"].get(data["dokter"].get(info_jadwal["id_dokter"], {}).get("id_spesialis"), {"nama": "Tidak Ditemukan"})["nama"] # type: ignore
                    
                    warna_status = Fore.GREEN if info_janji['status'] == "Selesai" else (Fore.YELLOW if info_janji['status'] == "Terjadwal" else H)
                    
                    print(f"ID: {id_janji}, Pasien: {info_pasien['nama']}, Dokter: {info_dokter['nama']}, Departemen: {nama_departemen}, Tanggal: {info_jadwal['tanggal_tersedia']}, Waktu: {info_jadwal['waktu_tersedia']}, Status: {warna_status}{info_janji['status']}{R}")
        elif pilihan == '2':
            if not data["janji_temu"]:
                print(Fore.YELLOW + "Belum ada data janji untuk dihapus.")
                continue
            
            print(f"\n{H}Daftar Janji:{R}")
            for id_janji, info_janji in data["janji_temu"].items():
                info_pasien = data["pasien"].get(info_janji["id_pasien"], {"nama": "Tidak Ditemukan"})
                info_jadwal = data["jadwal"].get(info_janji["id_jadwal"], {"id_dokter": "Tidak Ditemukan"})
                info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {"nama": "Tidak Ditemukan"})
                nama_departemen = data["departemen"].get(data["dokter"].get(info_jadwal["id_dokter"], {}).get("id_spesialis"), {"nama": "Tidak Ditemukan"})["nama"] # type: ignore
                
                warna_status = Fore.GREEN if info_janji['status'] == "Selesai" else (Fore.YELLOW if info_janji['status'] == "Terjadwal" else H)
                
                print(f"ID: {id_janji}, Pasien: {info_pasien['nama']}, Dokter: {info_dokter['nama']}, Departemen: {nama_departemen}, Tanggal: {info_jadwal['tanggal_tersedia']}, Waktu: {info_jadwal['waktu_tersedia']}, Status: {warna_status}{info_janji['status']}{R}")
            id_janji = input("Masukkan ID Janji yang akan dihapus: ")
            if id_janji in data["janji_temu"]:
                # Ambil id_jadwal(jadwal) sebelum menghapus janji
                id_jadwal = data["janji_temu"][id_janji].get("id_jadwal")

                # Hapus janji
                del data["janji_temu"][id_janji]

                # Kembalikan status jadwal 
                if id_jadwal and id_jadwal in data["jadwal"]:
                    data["jadwal"][id_jadwal]["tersedia"] = True

                # Hapus juga data checkup yang terkait
                periksa_yg_dihapus = [id_periksa for id_periksa, info_periksa in data["pemeriksaan"].items() if info_periksa.get("id_janji_temu") == id_janji]
                for id_periksa in periksa_yg_dihapus:
                    del data["pemeriksaan"][id_periksa]

                save_data(data)
                print(f"{H}[🗸] Janji ID {id_janji} dan data terkait berhasil dihapus. Jadwal telah tersedia kembali.{R}")
                time.sleep(3)
                clear_screen()
            else:
                print(Fore.RED + "ID Janji tidak ditemukan.")
                time.sleep(3)
        elif pilihan == '0':
            time.sleep(3)
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(3)
            clear_screen()

#Fungsi Data CheckUp (Staff)
def data_checkup(data):
    while True:
        data = load_data() # Muat ulang data
        print(f"\n--- Input Data Pemeriksaan ({H}CheckUp{R}) ({H}Staff{R}) ---")
        print("1. Tambah/Edit Data Pemeriksaan")
        print("2. Lihat Semua Data Pemeriksaan") 
        print("3. Data Pembayaran")
        print("0. Kembali ke Menu Staff")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            print(Fore.LIGHTRED_EX + "\nDaftar Janji (Hanya Janji yang Berstatus 'Terjadwal' atau 'Selesai' yang bisa diisi):")
            janji_yg_bisa_diisi = {id_janji: info_janji for id_janji, info_janji in data["janji_temu"].items() if info_janji["status"] in ["Terjadwal", "Selesai"]}
            if not janji_yg_bisa_diisi:
                print(Fore.YELLOW + "Tidak ada janji yang tersedia untuk diisi hasil pemeriksaannya.")
            else:
                for id_janji, info_janji in janji_yg_bisa_diisi.items():
                    warna_status = H if info_janji['status'] == "Selesai" else Fore.YELLOW
                    info_pasien = data["pasien"].get(info_janji["id_pasien"], {"nama": "Tidak Ditemukan"})
                    info_jadwal = data["jadwal"].get(info_janji["id_jadwal"], {"id_dokter": "Tidak Ditemukan"})
                    info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {"nama": "Tidak Ditemukan"})
                    tanggal_janji = info_jadwal.get('tanggal_tersedia', 'N/A')
                    print(f"ID Janji: {id_janji}, Pasien: {H}{info_pasien['nama']}{R}, Dokter: {info_dokter['nama']}, Tanggal: {tanggal_janji}, Status: {warna_status}{info_janji['status']}{R}")
            
            id_janji_input = input("\nMasukkan ID Janji untuk diisi pemeriksaannya: ")
            if id_janji_input not in janji_yg_bisa_diisi:
                print(Fore.RED + "ID Janji tidak ditemukan atau statusnya tidak memungkinkan untuk diisi pemeriksaan.")
            else:
                diagnosis = input("Masukkan Diagnosis: ")
                catatan = input("Catatan Tambahan: ")
                
                # Biaya Tambahan (Fitur Baru)
                try:
                    biaya_tambahan = int(input("Biaya Tambahan Tindakan/Obat (Rp): ") or 0)
                except ValueError:
                    print("Input tidak valid. Biaya tambahan di-set ke 0.")
                    biaya_tambahan = 0
                
                id_periksa_ada = None
                for id_periksa, info_periksa in data["pemeriksaan"].items():
                    if info_periksa["id_janji_temu"] == id_janji_input:
                        id_periksa_ada = id_periksa
                        break
                
                if id_periksa_ada:
                    print(f"Data pemeriksaan untuk Janji ID {id_janji_input} sudah ada (ID CheckUp: {id_periksa_ada}). Apakah Anda ingin menggantinya? (y/n): ")
                    konfirmasi = input().lower()
                    if konfirmasi == 'y':
                        data["pemeriksaan"][id_periksa_ada] = {
                            "id_janji_temu": id_janji_input,
                            "tanggal_pemeriksaan": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "diagnosis": diagnosis,
                            "catatan": catatan
                        }
                        print("Data pemeriksaan berhasil diperbarui.")
                    else:
                        print("Operasi dibatalkan.")
                else:
                    id_periksa = str(len(data["pemeriksaan"]) + 1)
                    data["pemeriksaan"][id_periksa] = {
                        "id_janji_temu": id_janji_input,
                        "tanggal_pemeriksaan": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "diagnosis": diagnosis,
                        "catatan": catatan
                    }
                    print(f"{H}[🗸] Data pemeriksaan berhasil ditambahkan.{R}")
                
                # Proses Biaya Tambahan
                if biaya_tambahan > 0:
                     id_pembayaran_baru = str(len(data["pembayaran"]) + 1)
                     id_pasien = data["janji_temu"][id_janji_input]["id_pasien"]
                     data["pembayaran"][id_pembayaran_baru] = {
                        "id_janji_temu": id_janji_input,
                        "id_pasien": id_pasien,
                        "jumlah": biaya_tambahan,
                        "tanggal_pembayaran": "",
                        "status": "Menunggu",
                        "metode_pembayaran": "",
                        "jenis_layanan": "Biaya Tambahan (Checkup)"
                     }
                     print(f"{H}Tagihan tambahan sebesar Rp {biaya_tambahan:,} berhasil dibuat.{R}")
                
                #mengubah status janji menjadi completed
                data["janji_temu"][id_janji_input]["status"] = "Selesai"
                
                # Otomatis buat data pembayaran jika belum ada
                ada_pembayaran = any(info_pasien["id_janji_temu"] == id_janji_input for info_pasien in data["pembayaran"].values())
                if not ada_pembayaran:
                    id_pembayaran = str(len(data["pembayaran"]) + 1)
                    id_pasien = data["janji_temu"][id_janji_input]["id_pasien"]
                    
                    # Tentukan biaya berdasarkan jenis layanan
                    print(f"\n{H}--- Input Data Pembayaran ---{R}")
                    print("Jenis Layanan:")
                    print("1. Konsultasi Umum (Rp 150.000)")
                    print("2. Konsultasi Spesialis (Rp 250.000)") 
                    print("3. Emergency (Rp 500.000)")
                    print("4. Lainnya (Input Manual)")
                    
                    pilihan_layanan = input("Pilih jenis layanan (1-4): ")
                    if pilihan_layanan == '1':
                        jumlah = 150000
                        jenis_layanan = "Konsultasi Umum"
                    elif pilihan_layanan == '2':
                        jumlah = 250000
                        jenis_layanan = "Konsultasi Spesialis"
                    elif pilihan_layanan == '3':
                        jumlah = 500000
                        jenis_layanan = "Emergency"
                    else:
                        jumlah = int(input("Masukkan jumlah biaya manual: Rp "))
                        jenis_layanan = input("Jenis layanan: ")
                    
                    data["pembayaran"][id_pembayaran] = {
                        "id_janji_temu": id_janji_input,
                        "id_pasien": id_pasien,
                        "jumlah": jumlah,
                        "tanggal_pembayaran": "",
                        "status": "Menunggu",
                        "metode_pembayaran": "",
                        "jenis_layanan": jenis_layanan
                    }
                    print(f"{H}[🗸] Data pembayaran berhasil dibuat - ID: {id_pembayaran}{R}")
                
                save_data(data)
                print(f"Status janji untuk ID tersebut telah diperbarui menjadi '{H}Completed{R}'.")

        elif pilihan == '2':
            if not data["pemeriksaan"]:
                print(Fore.YELLOW + "\nBelum ada data pemeriksaan.")
            else:
                print(f"\n{H}Daftar Data Pemeriksaan:{R}")
                for id_periksa, info_periksa in data["pemeriksaan"].items():
                    id_janji = info_periksa["id_janji_temu"]
                    info_janji = data["janji_temu"].get(id_janji, {})
                    info_pasien = data["pasien"].get(info_janji.get("id_pasien"), {"nama": "Tidak Ditemukan"})
                    print(f"ID CheckUp: {id_periksa}, ID Janji: {id_janji}, Nama Pasien: {H}{info_pasien['nama']}{R}, Tanggal: {info_periksa['tanggal_pemeriksaan']}")
                    print(f"  Diagnosis: {H}{info_periksa['diagnosis']}{R}")
                    print(f"  Catatan: {H}{info_periksa['catatan']}{R}\n")
        
        elif pilihan == '3':
            menu_pembayaran(data)
            
        elif pilihan == '0':
            time.sleep(2)
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(1)
            clear_screen()

#Fungsi Menu Pembayaran
def menu_pembayaran(data):
    while True:
        data = load_data() # Muat ulang data
        print(f"\n--- {H}Menu Data Pembayaran{R} ---")
        print("1. Lihat Semua Data Pembayaran")
        print("2. Proses Pembayaran")
        print("3. Edit Data Pembayaran")
        print("4. Hapus Data Pembayaran")
        print("0. Kembali ke Menu Sebelumnya")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            if not data["pembayaran"]:
                print(Fore.YELLOW + "\nBelum ada data pembayaran.")
            else:
                print(f"\n{H}Daftar Semua Pembayaran:{R}")
                total_lunas = 0
                total_tertunda = 0
                
                for id_pembayaran, info_pembayaran in data["pembayaran"].items():
                    info_pasien = data["pasien"].get(info_pembayaran["id_pasien"], {"nama": "Tidak Ditemukan"})
                    appointment_info = data["janji_temu"].get(info_pembayaran["id_janji_temu"], {})
                    
                    warna_status = H if info_pembayaran["status"] == "Lunas" else Fore.YELLOW
                    print(f"ID: {id_pembayaran}, Pasien: {info_pasien['nama']}, Janji ID: {info_pembayaran['id_janji_temu']}")
                    print(f"  Layanan: {info_pembayaran['jenis_layanan']}, Jumlah: Rp {info_pembayaran['jumlah']:,}")
                    print(f"  Status: {warna_status}{info_pembayaran['status']}{R}, Metode: {info_pembayaran.get('metode_pembayaran', '-')}")
                    print(f"  Tanggal Bayar: {info_pembayaran.get('tanggal_pembayaran', '-')}")
                    print()
                    
                    # Hitung total
                    if info_pembayaran["status"] == "Lunas":
                        total_lunas += info_pembayaran["jumlah"]
                    else:
                        total_tertunda += info_pembayaran["jumlah"]
                
                print(f"{H}Summary:{R}")
                print(f"Total Pembayaran Lunas: Rp {total_lunas:,}")
                print(f"Total Pembayaran Pending: Rp {total_tertunda:,}")
                print(f"Total Keseluruhan: Rp {total_lunas + total_tertunda:,}")

        elif pilihan == '2':
            # Tampilkan pembayaran yang pending
            pembayaran_tertunda = {id_pembayaran: info_pembayaran for id_pembayaran, info_pembayaran in data["pembayaran"].items() if info_pembayaran["status"] == "Menunggu"}
            
            if not pembayaran_tertunda:
                print(Fore.YELLOW + "\nTidak ada pembayaran yang pending.")
                continue
                
            print(f"\n{H}Daftar Pembayaran Pending:{R}")
            for id_pembayaran, info_pembayaran in pembayaran_tertunda.items():
                info_pasien = data["pasien"].get(info_pembayaran["id_pasien"], {"nama": "Tidak Ditemukan"})
                print(f"ID: {id_pembayaran}, Pasien: {info_pasien['nama']}, Layanan: {info_pembayaran['jenis_layanan']}, Jumlah: Rp {info_pembayaran['jumlah']:,}")
            
            id_pembayaran = input("\nMasukkan ID Pembayaran yang akan diproses: ")
            if id_pembayaran not in pembayaran_tertunda:
                print(Fore.RED + "ID Pembayaran tidak ditemukan atau sudah diproses.")
                continue
                
            info_pembayaran = data["pembayaran"][id_pembayaran]
            info_pasien = data["pasien"].get(info_pembayaran["id_pasien"], {"nama": "Tidak Ditemukan"})
            
            print(f"\n{H}Detail Pembayaran:{R}")
            print(f"Pasien: {info_pasien['nama']}")
            print(f"Layanan: {info_pembayaran['jenis_layanan']}")
            print(f"Jumlah: Rp {info_pembayaran['jumlah']:,}")
            
            # Pilih metode pembayaran
            print(f"\n{H}Metode Pembayaran:{R}")
            print("1. Cash")
            print("2. Transfer Bank")
            print("3. Kartu Kredit/Debit")
            pilihan_metode = input("Pilih metode pembayaran (1-3): ")
            
            if pilihan_metode == '1':
                metode_pembayaran = "Cash"
            elif pilihan_metode == '2':
                metode_pembayaran = "Transfer Bank"
            elif pilihan_metode == '3':
                metode_pembayaran = "Kartu Kredit/Debit"
            else:
                metode_pembayaran = "Cash"
                
            # Konfirmasi pembayaran
            konfirmasi = input(f"\nKonfirmasi pembayaran Rp {info_pembayaran['jumlah']:,} via {metode_pembayaran}? (y/n): ").lower()
            if konfirmasi == 'y':
                data["pembayaran"][id_pembayaran]["status"] = "Lunas"
                data["pembayaran"][id_pembayaran]["metode_pembayaran"] = metode_pembayaran
                data["pembayaran"][id_pembayaran]["tanggal_pembayaran"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_data(data)
                print(f"{H}[🗸] Pembayaran berhasil diproses!{R}")
            else:
                print("Proses pembayaran dibatalkan.")

        elif pilihan == '3':
            if not data["pembayaran"]:
                print(Fore.YELLOW + "\nBelum ada data pembayaran.")
                continue
                
            print(f"\n{H}Daftar Pembayaran:{R}")
            for id_pembayaran, info_pembayaran in data["pembayaran"].items():
                info_pasien = data["pasien"].get(info_pembayaran["id_pasien"], {"nama": "Tidak Ditemukan"})
                warna_status = H if info_pembayaran["status"] == "Lunas" else Fore.YELLOW
                print(f"ID: {id_pembayaran}, Pasien: {info_pasien['nama']}, Status: {warna_status}{info_pembayaran['status']}{R}, Jumlah: Rp {info_pembayaran['jumlah']:,}")
            
            id_pembayaran = input("\nMasukkan ID Pembayaran yang akan diedit: ")
            if id_pembayaran not in data["pembayaran"]:
                print(Fore.RED + "ID Pembayaran tidak ditemukan.")
                continue
                
            info_pembayaran = data["pembayaran"][id_pembayaran]
            print(f"\nData saat ini:")
            print(f"Jumlah: Rp {info_pembayaran['jumlah']:,}")
            print(f"Status: {info_pembayaran['status']}")
            print(f"Metode: {info_pembayaran.get('metode_pembayaran', '-')}")
            print(f"Layanan: {info_pembayaran['jenis_layanan']}")
            
            print(f"\n{H}--- Edit Data ---{R} (Tekan Enter untuk melewati)")
            jumlah_baru = input(f"Jumlah Baru (sekarang: {info_pembayaran['jumlah']}): ") or info_pembayaran['jumlah']
            layanan_baru = input(f"Layanan Baru (sekarang: {info_pembayaran['jenis_layanan']}): ") or info_pembayaran['jenis_layanan']
            metode_baru = input(f"Metode Baru (sekarang: {info_pembayaran.get('metode_pembayaran', '-')}) : ") or info_pembayaran.get('metode_pembayaran', '')
            
            print(f"Status Baru (sekarang: {info_pembayaran['status']}):")
            print("1. Lunas")
            print("2. Menunggu")
            pilihan_status = input("Pilih status baru (1-2, Enter untuk tidak mengubah): ")
            
            status_baru = info_pembayaran['status'] # Default ke status lama
            if pilihan_status == '1':
                status_baru = "Lunas"
            elif pilihan_status == '2':
                status_baru = "Menunggu"
            
            try:
                jumlah_baru = int(jumlah_baru)
            except ValueError:
                print(Fore.RED + "Jumlah harus angka.")
                continue
            
            # Update data pembayaran
            data["pembayaran"][id_pembayaran]["jumlah"] = jumlah_baru
            data["pembayaran"][id_pembayaran]["jenis_layanan"] = layanan_baru
            data["pembayaran"][id_pembayaran]["metode_pembayaran"] = metode_baru
            data["pembayaran"][id_pembayaran]["status"] = status_baru
            
            save_data(data)
            print(f"{H}[🗸] Data pembayaran berhasil diupdate.{R}")

        elif pilihan == '4':
            if not data["pembayaran"]:
                print(Fore.YELLOW + "\nBelum ada data pembayaran.")
                continue
                
            print(f"\n{H}Daftar Pembayaran:{R}")
            for id_pembayaran, info_pembayaran in data["pembayaran"].items():
                info_pasien = data["pasien"].get(info_pembayaran["id_pasien"], {"nama": "Tidak Ditemukan"})
                warna_status = H if info_pembayaran["status"] == "Lunas" else Fore.YELLOW
                print(f"ID: {id_pembayaran}, Pasien: {info_pasien['nama']}, Status: {warna_status}{info_pembayaran['status']}{R}, Jumlah: Rp {info_pembayaran['jumlah']:,}")
            
            id_pembayaran = input("\nMasukkan ID Pembayaran yang akan dihapus: ")
            if id_pembayaran not in data["pembayaran"]:
                print(Fore.RED + "ID Pembayaran tidak ditemukan.")
                continue
                
            konfirmasi = input("Apakah Anda yakin ingin menghapus data pembayaran ini? (y/n): ").lower()
            if konfirmasi == 'y':
                del data["pembayaran"][id_pembayaran]
                save_data(data)
                print(f"{H}[🗸] Data pembayaran berhasil dihapus.{R}")
            else:
                print(f"{H}[🗸] Penghapusan dibatalkan.{R}")

        elif pilihan == '0':
            time.sleep(2)
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(1)
            clear_screen()

#Fungsi Data Rawat Inap (Staff)
def data_rawat_inap(data):
    while True:
        data = load_data() # Muat ulang data
        print(f"\n--- Data Rawat Inap ({H}Staff{R}) ---")
        print("1. Lihat Semua Rawat Inap")
        print("2. Tambah Rawat Inap Baru")
        print("3. Edit Rawat Inap (Status Keluar)")
        print("4. Hapus Rawat Inap")
        print("0. Kembali ke Menu Staff")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            if not data["rawat_inap"]:
                print(Fore.YELLOW + "\nBelum ada data rawat inap.")
            else:
                print(f"\n{H}Daftar Rawat Inap:{R}")
                for id_rawat, info_rawat in data["rawat_inap"].items():
                    info_pasien = data["pasien"].get(info_rawat["id_pasien"], {"nama": "Tidak Ditemukan"})
                    info_kamar = data["kamar"].get(info_rawat["id_kamar"], {"nama": "Tidak Ditemukan"})
                    print(f"ID Rawat Inap: {id_rawat}, Pasien: {info_pasien['nama']}, Ruangan: {info_kamar['nama']}, Masuk: {info_rawat['tanggal_masuk']}, Estimasi Keluar: {info_rawat['tanggal_keluar']}, Status: {H}{info_rawat['status']}{R}")
        elif pilihan == '2':
            print(f"\n{H}Daftar Pasien:{R}")
            for id_pasien_iter, info_pasien in data["pasien"].items():
                print(f"ID: {id_pasien_iter}, Nama: {info_pasien['nama']}")
            id_pasien = input("Masukkan ID Pasien: ")
            if id_pasien not in data["pasien"]:
                print(Fore.RED + "ID Pasien tidak ditemukan.")
                time.sleep(3)
                clear_screen()
                return

            print(Fore.RED + "\nDaftar Janji (Hanya Janji yang Berstatus 'Selesai' yang bisa dijadikan dasar rawat inap):")
            janji_selesai = {id_janji: info_janji for id_janji, info_janji in data["janji_temu"].items() if info_janji["status"] == "Selesai" and info_janji["id_pasien"] == id_pasien}
            if not janji_selesai:
                print(Fore.YELLOW + "Pasien ini belum memiliki janji yang selesai (Completed).")
                return
            for id_janji, info_janji in janji_selesai.items():
                 info_jadwal = data["jadwal"].get(info_janji["id_jadwal"], {"id_dokter": "Tidak Ditemukan"})
                 info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {"nama": "Tidak Ditemukan"})
                 print(f"ID Janji: {id_janji}, Dokter: {info_dokter['nama']}, Tanggal: {info_jadwal['tanggal_tersedia']}")
            id_janji = input("Masukkan ID Janji sebagai dasar rawat inap: ")
            if id_janji not in janji_selesai:
                print(Fore.RED + "ID Janji tidak ditemukan atau bukan milik pasien ini atau belum selesai.")
                return

            print(f"\n{H}Daftar Ruangan Tersedia:{R}")
            kamar_tersedia = {id_kamar_iter: info_kamar for id_kamar_iter, info_kamar in data["kamar"].items() if info_kamar.get("tersedia", True)}
            if not kamar_tersedia:
                print("Tidak ada ruangan yang tersedia saat ini.")
                return
            for id_kamar_iter, info_kamar in kamar_tersedia.items():
                print(f"ID: {id_kamar_iter}, Nama: {info_kamar['nama']}, Tipe: {info_kamar['tipe']}")
            id_kamar = input("Masukkan ID Ruangan: ")
            if id_kamar not in kamar_tersedia:
                print(Fore.RED + "ID Ruangan tidak ditemukan atau tidak tersedia.")
                return

            tanggal_masuk = input("Tanggal Masuk (YYYY-MM-DD): ")
            tanggal_keluar = input("Estimasi Tanggal Keluar (YYYY-MM-DD): ")
            
            # Biaya Kamar Manual
            try:
                biaya_kamar = int(input("Biaya Kamar (Rp): ") or 0)
            except ValueError:
                print("Input tidak valid. Biaya kamar di-set ke 0.")
                biaya_kamar = 0

            id_rawat_inap = str(len(data["rawat_inap"]) + 1)
            data["rawat_inap"][id_rawat_inap] = {
                "id_pasien": id_pasien,
                "id_janji_temu": id_janji,
                "id_kamar": id_kamar,
                "tanggal_masuk": tanggal_masuk,
                "tanggal_keluar": tanggal_keluar,
                "status": "Dirawat"
            }
            
            # Buat Tagihan Biaya Kamar
            if biaya_kamar > 0:
                id_pembayaran_kamar = str(len(data["pembayaran"]) + 1)
                data["pembayaran"][id_pembayaran_kamar] = {
                    "id_janji_temu": id_janji,
                    "id_pasien": id_pasien,
                    "jumlah": biaya_kamar,
                    "tanggal_pembayaran": "",
                    "status": "Menunggu",
                    "metode_pembayaran": "",
                    "jenis_layanan": "Biaya Rawat Inap"
                }
                print(f"{H}Tagihan Biaya Rawat Inap sebesar Rp {biaya_kamar:,} berhasil dibuat.{R}")
        
            data["kamar"][id_kamar]["tersedia"] = False
            save_data(data)
            print(f"{H}[🗸] Data rawat inap berhasil ditambahkan.{R}")

        elif pilihan == '3':
            print(f"\n{H}Daftar Rawat Inap:{R}")
            for id_rawat, info_rawat in data["rawat_inap"].items():
                info_pasien = data["pasien"].get(info_rawat["id_pasien"], {"nama": "Tidak Ditemukan"})
                info_kamar = data["kamar"].get(info_rawat["id_kamar"], {"nama": "Tidak Ditemukan"})
                print(f"ID Rawat Inap: {id_rawat}, Pasien: {info_pasien['nama']}, Ruangan: {info_kamar['nama']}, Masuk: {info_rawat['tanggal_masuk']}, Estimasi Keluar: {info_rawat['tanggal_keluar']}, Status: {H}{info_rawat['status']}{R}")
            id_rawat_inap = input("Masukkan ID Rawat Inap untuk diubah statusnya (keluar): ")
            if id_rawat_inap in data["rawat_inap"]:
                info_rawat = data["rawat_inap"][id_rawat_inap]
                if info_rawat["status"] == "Keluar":
                    print(Fore.YELLOW + "Pasien sudah dikeluarkan.")
                    continue
                print(f"Data saat ini: ID Rawat Inap: {id_rawat_inap}, Pasien: {data['pasien'].get(info_rawat['id_pasien'], {'nama': 'Tidak Ditemukan'})['nama']}, Status: {H}{info_rawat['status']}{R}")
                konfirmasi = input("Apakah pasien ini dikeluarkan sekarang? (y/n): ").lower()
                if konfirmasi == 'y':
                    # Kembalikan status ruangan menjadi tersedia
                    data["kamar"][info_rawat["id_kamar"]]["tersedia"] = True
                    data["rawat_inap"][id_rawat_inap]["status"] = "Keluar"
                    data["rawat_inap"][id_rawat_inap]["tanggal_keluar_aktual"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_data(data)
                    print(f"Status rawat inap berhasil diubah menjadi '{H}Keluar{R}'.")
                else:
                    print("Operasi dibatalkan.")
            else:
                print(Fore.RED + "ID Rawat Inap tidak ditemukan.")
        elif pilihan == '4':
            print(f"\n{H}Daftar Rawat Inap:{R}")
            for id_rawat, info_rawat in data["rawat_inap"].items():
                info_pasien = data["pasien"].get(info_rawat["id_pasien"], {"nama": "Tidak Ditemukan"})
                info_kamar = data["kamar"].get(info_rawat["id_kamar"], {"nama": "Tidak Ditemukan"})
                print(f"ID Rawat Inap: {id_rawat}, Pasien: {info_pasien['nama']}, Ruangan: {info_kamar['nama']}, Masuk: {info_rawat['tanggal_masuk']}, Estimasi Keluar: {info_rawat['tanggal_keluar']}, Status: {H}{info_rawat['status']}{R}")
            id_rawat_inap = input("Masukkan ID Rawat Inap yang akan dihapus: ")
            if id_rawat_inap in data["rawat_inap"]:
                 info_rawat = data["rawat_inap"][id_rawat_inap]
                 # Kembalikan status ruangan jika rawat inap belum selesai
                 if info_rawat["status"] != "Keluar":
                     data["kamar"][info_rawat["id_kamar"]]["tersedia"] = True
                 del data["rawat_inap"][id_rawat_inap]
                 save_data(data)
                 print(Fore.GREEN + "Data rawat inap berhasil dihapus.")
            else:
                print(Fore.RED + "ID Rawat Inap tidak ditemukan.")
        elif pilihan == '0':
            time.sleep(2)
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(1)
            clear_screen()
