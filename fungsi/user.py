import time
from colorama import Fore
from fungsi.core import *
from datetime import datetime
from fungsi.color import *

# --- Menu User Biasa ---
def menu_user(username_saat_ini, id_pasien):

    while True:
        # data = load_data()  <- No longer needed here for sub-menus, but useful for display if we wanted specific user data in the header. 
        # However, to be consistent, sub-menus load their own.
        print(f"\n--- Menu User ({H}{username_saat_ini}{R}) ---")
        print("1. Lihat Jadwal Tersedia")
        print("2. Buat Janji Saya")
        print("3. Lihat Janji Saya")
        print("4. Lihat Riwayat Kesehatan Saya")
        print("5. Lihat Riwayat Rawat Inap Saya")
        print("6. Data Pembayaran Saya")  # Menu baru untuk pembayaran
        print("0. Logout Menu User")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            clear_screen()
            lihat_jadwal_tersedia()
        elif pilihan == '2':
            clear_screen()
            buat_janji_user(username_saat_ini, id_pasien)
        elif pilihan == '3':
            clear_screen()
            lihat_janji_user(username_saat_ini, id_pasien)
        elif pilihan == '4':
            clear_screen()
            lihat_riwayat_user(username_saat_ini, id_pasien)
        elif pilihan == '5':
            clear_screen()
            lihat_riwayat_inap(username_saat_ini, id_pasien)
        elif pilihan == '6':  # Menu baru untuk pembayaran
            clear_screen()
            menu_pembayaran_user(username_saat_ini, id_pasien)
        elif pilihan == '0':
            konfirmasi = input("Apakah Anda Yakin Ingin Kembali ke Menu Utama? [Y/N] : ").lower()
            if konfirmasi == 'y':
                clear_screen()
                break
            else:
                print(f"{H}[🗸] Aksi dibatalkan.{R}")
                time.sleep(2)
                clear_screen()
        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")
            time.sleep(3)
            clear_screen()

# --- Menu Pembayaran untuk User ---
def menu_pembayaran_user(username_saat_ini, id_pasien): # data di-pass dari menu_user
    while True:
        data = load_data() # Muat ulang data
        print(f"\n--- Menu Pembayaran ({H}{username_saat_ini}{R}) ---")
        print("1. Lihat Tagihan Saya")
        print("2. Lihat Riwayat Pembayaran")
        print("3. Bayar Tagihan")
        print("0. Kembali ke Menu User")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            clear_screen()
            lihat_tagihan_user(username_saat_ini, id_pasien)
        elif pilihan == '2':
            clear_screen()
            lihat_riwayat_pembayaran_user(username_saat_ini, id_pasien)
        elif pilihan == '3':
            clear_screen()
            bayar_tagihan_user(username_saat_ini, id_pasien)
        elif pilihan == '0':
            time.sleep(2)
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(1)
            clear_screen()

# --- Fungsi Lihat Tagihan User ---
def lihat_tagihan_user(username_saat_ini, id_pasien):
    data = load_data() # data realtime
    print(f"\n--- {H}Tagihan Saya{R} ---")

    if not id_pasien:
        print(Fore.RED + "Anda belum terdaftar sebagai pasien.")
        return

    # Cari pembayaran yang masih pending untuk user ini
    pembayaran_tertunda = []
    total_tertunda = 0
    
    for id_pembayaran_iter, info_pembayaran in data["pembayaran"].items():
        if info_pembayaran["id_pasien"] == id_pasien and info_pembayaran["status"] == "Menunggu":
            pembayaran_tertunda.append((id_pembayaran_iter, info_pembayaran))
            total_tertunda += info_pembayaran["jumlah"]

    if not pembayaran_tertunda:
        print(Fore.GREEN + "Tidak ada tagihan yang belum dibayar.")
        return

    print(f"{H}Daftar Tagihan Belum Dibayar:{R}")
    for id_pembayaran, info_pembayaran in pembayaran_tertunda:
        # Dapatkan info appointment
        info_janji_temu = data["janji_temu"].get(info_pembayaran["id_janji_temu"], {})
        info_jadwal = data["jadwal"].get(info_janji_temu.get("id_jadwal", ""), {})
        info_dokter = data["dokter"].get(info_jadwal.get("id_dokter", ""), {"nama": "Tidak Ditemukan"})
        
        print(f"\nID Pembayaran: {id_pembayaran}")
        print(f"  Jenis Layanan: {info_pembayaran['jenis_layanan']}")
        print(f"  Dokter: {info_dokter.get('nama', 'Tidak Ditemukan')}")
        print(f"  Jumlah: {H}Rp {info_pembayaran['jumlah']:,}{R}")
        print(f"  Status: {Fore.YELLOW}{info_pembayaran['status']}{R}")
        
        if info_janji_temu.get('tanggal_pemesanan'):
            print(f"  Tanggal Janji: {info_janji_temu['tanggal_pemesanan']}")

    print(f"\n{H}Total Tagihan: Rp {total_tertunda:,}{R}")

# --- Fungsi Lihat Riwayat Pembayaran User ---
def lihat_riwayat_pembayaran_user(username_saat_ini, id_pasien):
    data = load_data() # data realtime
    print(f"\n--- {H}Riwayat Pembayaran Saya{R} ---")

    if not id_pasien:
        print(Fore.RED + "Anda belum terdaftar sebagai pasien.")
        return

    # Cari semua pembayaran untuk user ini
    pembayaran_pengguna = []
    total_dibayar = 0
    
    for id_pembayaran_iter, info_pembayaran in data["pembayaran"].items():
        if info_pembayaran["id_pasien"] == id_pasien:
            pembayaran_pengguna.append((id_pembayaran_iter, info_pembayaran))
            if info_pembayaran["status"] == "Lunas":
                total_dibayar += info_pembayaran["jumlah"]

    if not pembayaran_pengguna:
        print(Fore.YELLOW + "Belum ada riwayat pembayaran.")
        return

    print(f"{H}Riwayat Pembayaran:{R}")
    for id_pembayaran, info_pembayaran in pembayaran_pengguna:
        # Dapatkan info appointment
        info_janji_temu = data["janji_temu"].get(info_pembayaran["id_janji_temu"], {})
        info_jadwal = data["jadwal"].get(info_janji_temu.get("id_jadwal", ""), {})
        info_dokter = data["dokter"].get(info_jadwal.get("id_dokter", ""), {"nama": "Tidak Ditemukan"})
        
        status_color = H if info_pembayaran["status"] == "Lunas" else Fore.YELLOW
        status_text = "LUNAS" if info_pembayaran["status"] == "Lunas" else "BELUM BAYAR"
        
        print(f"\nID Pembayaran: {id_pembayaran}")
        print(f"  Jenis Layanan: {info_pembayaran['jenis_layanan']}")
        print(f"  Dokter: {info_dokter.get('nama', 'Tidak Ditemukan')}")
        print(f"  Jumlah: Rp {info_pembayaran['jumlah']:,}")
        print(f"  Status: {status_color}{status_text}{R}")
        print(f"  Metode: {info_pembayaran.get('metode_pembayaran', '-')}")
        
        if info_pembayaran.get('tanggal_pembayaran'):
            print(f"  Tanggal Bayar: {info_pembayaran['tanggal_pembayaran']}")
        else:
            print(f"  Tanggal Bayar: -")

    print(f"\n{H}Total Sudah Dibayar: Rp {total_dibayar:,}{R}")

# --- Fungsi Bayar Tagihan User ---
def bayar_tagihan_user(username_saat_ini, id_pasien):
    data = load_data() # data realtime
    print(f"\n--- {H}Bayar Tagihan{R} ---")

    if not id_pasien:
        print(Fore.RED + "Anda belum terdaftar sebagai pasien.")
        return

    # Tampilkan tagihan yang masih pending
    pembayaran_tertunda = []
    for id_pembayaran_iter, info_pembayaran in data["pembayaran"].items():
        if info_pembayaran["id_pasien"] == id_pasien and info_pembayaran["status"] == "Menunggu":
            pembayaran_tertunda.append((id_pembayaran_iter, info_pembayaran))

    if not pembayaran_tertunda:
        print(Fore.GREEN + "Tidak ada tagihan yang perlu dibayar.")
        return

    print(f"{H}Tagihan yang Belum Dibayar:{R}")
    for id_pembayaran, info_pembayaran in pembayaran_tertunda:
        info_janji_temu = data["janji_temu"].get(info_pembayaran["id_janji_temu"], {})
        info_jadwal = data["jadwal"].get(info_janji_temu.get("id_jadwal", ""), {})
        info_dokter = data["dokter"].get(info_jadwal.get("id_dokter", ""), {"nama": "Tidak Ditemukan"})
        
        print(f"ID: {id_pembayaran} - {info_pembayaran['jenis_layanan']} - Dokter: {info_dokter.get('nama', 'Tidak Ditemukan')} - Rp {info_pembayaran['jumlah']:,}")

    id_pembayaran = input("\nMasukkan ID Pembayaran yang akan dibayar: ")
    
    # Cek apakah id_pembayaran valid
    if id_pembayaran not in data["pembayaran"]:
        print(Fore.RED + "ID Pembayaran tidak ditemukan.")
        return
        
    info_pembayaran = data["pembayaran"][id_pembayaran]
    
    # Cek apakah pembayaran ini milik user yang login
    if info_pembayaran["id_pasien"] != id_pasien:
        print(Fore.RED + "Anda tidak memiliki akses untuk membayar tagihan ini.")
        return
        
    # Cek apakah sudah dibayar
    if info_pembayaran["status"] == "Lunas":
        print(Fore.YELLOW + "Tagihan ini sudah dibayar.")
        return

    # Tampilkan detail pembayaran
    info_janji_temu = data["janji_temu"].get(info_pembayaran["id_janji_temu"], {})
    info_jadwal = data["jadwal"].get(info_janji_temu.get("id_jadwal", ""), {})
    info_dokter = data["dokter"].get(info_jadwal.get("id_dokter", ""), {"nama": "Tidak Ditemukan"})
    
    print(f"\n{H}Detail Pembayaran:{R}")
    print(f"Jenis Layanan: {info_pembayaran['jenis_layanan']}")
    print(f"Dokter: {info_dokter.get('nama', 'Tidak Ditemukan')}")
    print(f"Jumlah: {H}Rp {info_pembayaran['jumlah']:,}{R}")
    
    # Pilih metode pembayaran
    print(f"\n{H}Pilih Metode Pembayaran:{R}")
    print("1. Transfer Bank")
    print("2. Kartu Kredit/Debit")
    print("3. E-Wallet")
    print("4. Cash (Bayar di Loket)")
    
    pilihan_metode = input("Pilih metode (1-4): ")
    
    if pilihan_metode == '1':
        metode_pembayaran = "Transfer Bank"
        # Membuat Virtual Account otomatis berdasarkan ID Pembayaran
        bank_code = "8808" # Kode unik untuk rumah sakit (contoh)
        nomor_va = f"{bank_code}{id_pembayaran.zfill(8)}"
        print("\nSilakan transfer ke:")
        print("Bank: BCA")
        print(f"No. Virtual Account: {H}{nomor_va}{R}")
        print("Atas Nama: Rumah Sakit Sehat Sentosa")
        print(f"Jumlah: Rp {info_pembayaran['jumlah']:,}")
        input("\nTekan Enter setelah transfer...")
        
    elif pilihan_metode == '2':
        metode_pembayaran = "Kartu Kredit/Debit"
        nomor_kartu = input("Masukkan nomor kartu: ")
        tanggal_kadaluarsa = input("Masukkan tanggal kadaluarsa (MM/YY): ")
        cvv = input("Masukkan CVV (Card Verification Value): ")
        print("Verifikasi pembayaran...")
        time.sleep(2)
        
    elif pilihan_metode == '3':
        metode_pembayaran = "E-Wallet"
        print("\nPilih E-Wallet:")
        print("1. Gopay")
        print("2. OVO")
        print("3. Dana")
        print("4. LinkAja")
        pilihan_ewallet = input("Pilih (1-4): ")
        
        opsi_ewallet = {
            "1": {"nama": "Gopay", "prefix": "99001"},
            "2": {"nama": "OVO", "prefix": "99002"},
            "3": {"nama": "Dana", "prefix": "99003"},
            "4": {"nama": "LinkAja", "prefix": "99004"}
        }
        
        ewallet_terpilih = opsi_ewallet.get(pilihan_ewallet)
        
        if ewallet_terpilih:
            metode_pembayaran = f"E-Wallet ({ewallet_terpilih['nama']})"
            kode_pembayaran = f"{ewallet_terpilih['prefix']}{id_pembayaran.zfill(8)}"
            print(f"\nSilakan bayar menggunakan {ewallet_terpilih['nama']} ke nomor berikut:")
            print(f"Kode Pembayaran: {H}{kode_pembayaran}{R}")
            input("\nTekan Enter setelah pembayaran...")
        else:
            print(Fore.RED + "Pilihan E-Wallet tidak valid. Pembayaran dibatalkan.")
            return
        
    elif pilihan_metode == '4':
        metode_pembayaran = "Cash"
        print("Silakan bayar di loket rumah sakit")
        input("Tekan Enter untuk konfirmasi...")
        
    else:
        metode_pembayaran = "Transfer Bank"
        print("Metode default: Transfer Bank")
        input("Tekan Enter untuk konfirmasi...")

    # Konfirmasi pembayaran
    konfirmasi = input(f"\nKonfirmasi pembayaran Rp {info_pembayaran['jumlah']:,} via {metode_pembayaran}? (y/n): ").lower()
    if konfirmasi == 'y':
        data["pembayaran"][id_pembayaran]["status"] = "Lunas"
        data["pembayaran"][id_pembayaran]["metode_pembayaran"] = metode_pembayaran
        data["pembayaran"][id_pembayaran]["tanggal_pembayaran"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(data)
        
        print(f"\n{H}=== PEMBAYARAN BERHASIL ==={R}")
        print(f"ID Pembayaran: {id_pembayaran}")
        print(f"Jumlah: Rp {info_pembayaran['jumlah']:,}")
        print(f"Metode: {metode_pembayaran}")
        print(f"Tanggal: {data['pembayaran'][id_pembayaran]['tanggal_pembayaran']}")
        print(f"{H}Terima kasih telah melakukan pembayaran!{R}")
        
    else:
        print("Pembayaran dibatalkan.")

# --- Fungsi Lihat Riwayat Rawat Inap User ---
def lihat_riwayat_inap(username_saat_ini, id_pasien):
    data = load_data() # data realtime
    print("\n--- Riwayat Rawat Inap ---")

    if not id_pasien:
        print(Fore.RED + "Anda belum terdaftar sebagai pasien.")
        return

    # Ambil daftar rawat inap berdasarkan id_pasien
    rawat_inap_pasien = [
        (id_rawat_inap, info_rawat_inap) for id_rawat_inap, info_rawat_inap in data["rawat_inap"].items()
        if info_rawat_inap["id_pasien"] == id_pasien
    ]

    if not rawat_inap_pasien:
        print(Fore.YELLOW + "Anda belum memiliki riwayat rawat inap.")
        return

    print(f"{H}Riwayat Rawat Inap:{R}")
    for id_rawat_inap, info_rawat_inap in rawat_inap_pasien:
        # Ambil data appointment (janji) terkait
        info_janji_temu = data["janji_temu"].get(info_rawat_inap["id_janji_temu"], None)
        info_jadwal = None
        info_dokter = None

        if info_janji_temu:
            info_jadwal = data["jadwal"].get(info_janji_temu["id_jadwal"], None)
            if info_jadwal:
                info_dokter = data["dokter"].get(info_jadwal["id_dokter"], {"nama": "Tidak Ditemukan"})

        kamar = data["kamar"].get(info_rawat_inap["id_kamar"], {"nama": "Tidak Ditemukan", "tipe": "-"})

        print(f"\nID Rawat Inap: {id_rawat_inap}")
        print(f"  Ruangan: {H}{kamar['nama']} ({kamar['tipe']}){R}")
        print(f"  Tanggal Masuk: {info_rawat_inap['tanggal_masuk']}")
        print(f"  Tanggal Keluar: {info_rawat_inap['tanggal_keluar']}")
        print(f"  Status: {H}{info_rawat_inap['status']}{R}")

        if info_dokter:
            print(f"  Dokter Penanggung Jawab: {info_dokter['nama']}")
        else:
            print(Fore.YELLOW + "  Dokter tidak ditemukan.")

        # Cek apakah ada data checkup terkait admission tersebut
        pemeriksaan_terkait = None
        for id_pemeriksaan_iter, info_pemeriksaan_iter in data["pemeriksaan"].items():
            if info_pemeriksaan_iter["id_janji_temu"] == info_rawat_inap["id_janji_temu"]:
                pemeriksaan_terkait = info_pemeriksaan_iter
                break

        if pemeriksaan_terkait:
            print(f"  Diagnosis: {H}{pemeriksaan_terkait['diagnosis']}{R}")
            print(f"  Catatan Dokter: {H}{pemeriksaan_terkait['catatan']}{R}")
        else:
            print(Fore.YELLOW + "  Belum ada data pemeriksaan / checkup untuk rawat inap ini.")

# --- Fungsi Lihat Jadwal Tersedia (untuk User) ---
def lihat_jadwal_tersedia():
    data = load_data() # data realtime
    print("\n--- Jadwal Dokter Tersedia ---")
    # Filter hanya jadwal yang tersedia
    jadwal_tersedia = {id_jadwal_iter: info_jadwal_iter for id_jadwal_iter, info_jadwal_iter in data["jadwal"].items() if info_jadwal_iter.get("tersedia", True)}
    if not jadwal_tersedia:
        print(Fore.YELLOW + "Tidak ada jadwal yang tersedia saat ini.")
        return

    # Tampilkan dengan detail dokter dan departemen
    print(f"{H}Daftar Jadwal Tersedia:{R}")
    for id_jadwal_iter, info_jadwal_iter in jadwal_tersedia.items():
        info_dokter = data["dokter"].get(info_jadwal_iter["id_dokter"], {"nama": "Tidak Ditemukan"})
        info_departemen = data["departemen"].get(info_dokter["id_spesialis"], {"nama": "Tidak Ditemukan"})
        print(f"ID Jadwal: {id_jadwal_iter}, Dokter: {info_dokter['nama']}, Departemen: {info_departemen['nama']}, Tanggal: {info_jadwal_iter['tanggal_tersedia']}, Waktu: {info_jadwal_iter['waktu_tersedia']}")

# --- Fungsi Buat Janji (untuk User) ---
def buat_janji_user(username_saat_ini, id_pasien):
    data = load_data() # data realtime
    print("\n--- Buat Janji Saya ---")

    if not id_pasien:
        print(Fore.RED + f"Anda ({username_saat_ini}) belum terdaftar sebagai pasien. Silakan daftar dulu atau hubungi staff.")
        return

    # Tampilkan jadwal yang tersedia
    jadwal_tersedia = {id_jadwal_iter: info_jadwal_iter for id_jadwal_iter, info_jadwal_iter in data["jadwal"].items() if info_jadwal_iter.get("tersedia", True)}
    if not jadwal_tersedia:
        print(Fore.YELLOW + "Tidak ada jadwal yang tersedia saat ini.")
        return

    print(f"{H}Daftar Jadwal Tersedia:{R}")
    for id_jadwal_iter, info_jadwal_iter in jadwal_tersedia.items():
        info_dokter = data["dokter"].get(info_jadwal_iter["id_dokter"], {"nama": Fore.RED + "Tidak Ditemukan"})
        info_departemen = data["departemen"].get(info_dokter["id_spesialis"], {"nama": "Tidak Ditemukan"})
        print(f"ID Jadwal: {id_jadwal_iter}, Dokter: {info_dokter['nama']}, Departemen: {info_departemen['nama']}, Tanggal: {info_jadwal_iter['tanggal_tersedia']}, Waktu: {info_jadwal_iter['waktu_tersedia']}")
    
    id_jadwal = input("\nMasukkan ID Jadwal yang dipilih: ")
    if id_jadwal not in jadwal_tersedia:
        print(Fore.RED + "ID Jadwal tidak valid atau sudah dipesan.")
        return

    # Buat Janji
    id_janji_temu = str(len(data["janji_temu"]) + 1)
    data["janji_temu"][id_janji_temu] = {
        "id_pasien": id_pasien,
        "id_jadwal": id_jadwal,
        "tanggal_pemesanan": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Terjadwal"
    }
    data["jadwal"][id_jadwal]["tersedia"] = False
    
    # Otomatis buat data pembayaran untuk janji baru
    # --- Otomatis buat data pembayaran untuk janji baru dengan pilihan layanan ---
    print(f"\n{H}--- Pilih Jenis Layanan ---{R}")
    print("1. Konsultasi Umum (Rp 150.000)")
    print("2. Konsultasi Spesialis (Rp 250.000)")
    print("3. Lainnya (Input Manual)")
    
    pilihan_layanan = input("Pilih jenis layanan (1-3): ")
    jumlah = 0
    jenis_layanan = ""

    if pilihan_layanan == '1':
        jumlah = 150000
        jenis_layanan = "Konsultasi Umum"
    elif pilihan_layanan == '2':
        # Cek apakah dokter yang dipilih adalah spesialis
        info_jadwal = data["jadwal"][id_jadwal]
        info_dokter = data["dokter"][info_jadwal["id_dokter"]]
        info_departemen = data["departemen"][info_dokter["id_spesialis"]]
        
        # Asumsikan 'Poliklinik Umum' bukan spesialis
        if "Umum" in info_departemen["nama"]:
            print(Fore.YELLOW + "Dokter yang dipilih bukan spesialis. Menggunakan layanan Konsultasi Umum.")
            jumlah = 150000
            jenis_layanan = "Konsultasi Umum"
        else:
            jumlah = 250000
            jenis_layanan = "Konsultasi Spesialis"
    else:
        print(Fore.YELLOW + "Pilihan tidak valid. Menggunakan default Konsultasi Umum.")
        jumlah = 150000
        jenis_layanan = "Konsultasi Umum"

    id_pembayaran = str(len(data["pembayaran"]) + 1)
    data["pembayaran"][id_pembayaran] = {
        "id_janji_temu": id_janji_temu,
        "id_pasien": id_pasien,
        "jumlah": jumlah,
        "tanggal_pembayaran": "",
        "status": "Menunggu",
        "metode_pembayaran": "",
        "jenis_layanan": jenis_layanan
    }
    
    save_data(data)
    print(f"{H}[🗸] Janji berhasil dibuat untuk Anda!{R}")
    print(f"{H}Tagihan untuk '{jenis_layanan}' sebesar Rp {jumlah:,} telah dibuat. Silakan cek menu Pembayaran.{R}")

# --- Fungsi Lihat Janji Saya (untuk User) ---
def lihat_janji_user(username_saat_ini, id_pasien):
    data = load_data() # data realtime
    print("\n--- Janji Saya ---")

    if not id_pasien:
        print(Fore.RED + "Anda belum terdaftar sebagai pasien.")
        return

    janji_temu_pengguna = {id_janji_temu: info_janji_temu for id_janji_temu, info_janji_temu in data["janji_temu"].items() if info_janji_temu["id_pasien"] == id_pasien}
    if not janji_temu_pengguna:
        print(Fore.YELLOW + "Anda belum memiliki janji temu.")
        return

    print(f"{H}Daftar Janji Anda:{R}")
    for id_janji_temu, info_janji_temu in janji_temu_pengguna.items():
        info_jadwal_iter = data["jadwal"].get(info_janji_temu["id_jadwal"], {"id_dokter": "Tidak Ditemukan"})
        info_dokter = data["dokter"].get(info_jadwal_iter["id_dokter"], {"nama": "Tidak Ditemukan"})
        info_departemen = data["departemen"].get(info_dokter["id_spesialis"], {"nama": "Tidak Ditemukan"})
        
        warna_status_janji = Fore.GREEN if info_janji_temu['status'] == "Selesai" else (Fore.YELLOW if info_janji_temu['status'] == "Terjadwal" else H)

        # Cek status pembayaran
        status_pembayaran = "Belum Bayar"
        for id_pembayaran_iter, info_pembayaran in data["pembayaran"].items():
            if info_pembayaran["id_janji_temu"] == id_janji_temu:
                status_pembayaran = "Lunas" if info_pembayaran["status"] == "Lunas" else "Belum Bayar"
                break
        
        warna_pembayaran = H if status_pembayaran == "Lunas" else Fore.YELLOW
        
        print(f"ID Janji: {id_janji_temu}, Dokter: {info_dokter['nama']}, Departemen: {info_departemen['nama']}")
        print(f"  Tanggal: {info_jadwal_iter['tanggal_tersedia']}, Waktu: {info_jadwal_iter['waktu_tersedia']}") # type: ignore
        print(f"  Status Janji: {warna_status_janji}{info_janji_temu['status']}{R}, Status Bayar: {warna_pembayaran}{status_pembayaran}{R}")
        print()

# --- Fungsi Lihat Riwayat Kesehatan Saya (untuk User) ---
def lihat_riwayat_user(username_saat_ini, id_pasien):
    data = load_data() # data realtime
    print("\n--- Riwayat Kesehatan Saya ---")

    if not id_pasien:
        print(Fore.RED + "Anda belum terdaftar sebagai pasien.")
        return

    # Cari janji pasien
    janji_temu_pasien = [id_janji_temu for id_janji_temu, info_janji_temu in data["janji_temu"].items() if info_janji_temu["id_pasien"] == id_pasien]

    if not janji_temu_pasien:
        print(Fore.YELLOW + "Anda belum memiliki riwayat janji.")
        return

    print(f"{H}Riwayat Pemeriksaan:{R}")
    for id_janji_temu in janji_temu_pasien:
        # Cari data checkup terkait
        pemeriksaan_ditemukan = False
        for id_pemeriksaan_iter, info_pemeriksaan_iter in data["pemeriksaan"].items():
            if info_pemeriksaan_iter["id_janji_temu"] == id_janji_temu:
                info_janji_temu = data["janji_temu"][id_janji_temu]
                info_jadwal_iter = data["jadwal"].get(info_janji_temu["id_jadwal"], {"id_dokter": "Tidak Ditemukan"})
                info_dokter = data["dokter"].get(info_jadwal_iter["id_dokter"], {"nama": "Tidak Ditemukan"})
                print(f"ID Janji: {id_janji_temu}, Tanggal Checkup: {info_pemeriksaan_iter['tanggal_pemeriksaan']}, Dokter: {info_dokter['nama']}")
                print(f"  Diagnosis: {H}{info_pemeriksaan_iter['diagnosis']}{R}")
                print(f"  Catatan: {H}{info_pemeriksaan_iter['catatan']}{R}")
                pemeriksaan_ditemukan = True
                break
        if not pemeriksaan_ditemukan:
            print(Fore.YELLOW + f"ID Janji: {id_janji_temu} - Belum ada data pemeriksaan.")