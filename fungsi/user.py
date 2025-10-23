import time
from colorama import Fore
from fungsi.core import *
from datetime import datetime
from fungsi.color import *

# --- Menu User Biasa ---
def menu_user(data, current_username, patient_id):
    while True:
        print(f"\n--- Menu User ({H}{current_username}{R}) ---")
        print("1. Lihat Jadwal Tersedia")
        print("2. Buat Janji Saya")
        print("3. Lihat Janji Saya")
        print("4. Lihat Riwayat Kesehatan Saya")
        print("5. Lihat Riwayat Rawat Inap Saya")
        print("6. Data Pembayaran Saya")  # Menu baru untuk pembayaran
        print("0. Kembali ke Menu Utama")
        choice = input("Pilih menu: ")

        if choice == '1':
            clear_screen()
            lihat_jadwal_tersedia(data)
        elif choice == '2':
            clear_screen()
            buat_janji_user(data, current_username, patient_id)
        elif choice == '3':
            clear_screen()
            lihat_janji_user(data, current_username, patient_id)
        elif choice == '4':
            clear_screen()
            lihat_riwayat_user(data, current_username, patient_id)
        elif choice == '5':
            clear_screen()
            lihat_riwayat_inap(data, current_username, patient_id)
        elif choice == '6':  # Menu baru untuk pembayaran
            clear_screen()
            menu_pembayaran_user(data, current_username, patient_id)
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

# --- Menu Pembayaran untuk User ---
def menu_pembayaran_user(data, current_username, patient_id):
    while True:
        print(f"\n--- {H}Menu Pembayaran{R} ({current_username}) ---")
        print("1. Lihat Tagihan Saya")
        print("2. Lihat Riwayat Pembayaran")
        print("3. Bayar Tagihan")
        print("0. Kembali ke Menu User")
        choice = input("Pilih menu: ")

        if choice == '1':
            clear_screen()
            lihat_tagihan_user(data, current_username, patient_id)
        elif choice == '2':
            clear_screen()
            lihat_riwayat_pembayaran_user(data, current_username, patient_id)
        elif choice == '3':
            clear_screen()
            bayar_tagihan_user(data, current_username, patient_id)
        elif choice == '0':
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(1)
            clear_screen()

# --- Fungsi Lihat Tagihan User ---
def lihat_tagihan_user(data, current_username, patient_id):
    print(f"\n--- {H}Tagihan Saya{R} ---")

    if not patient_id:
        print(Fore.RED + "Anda belum terdaftar sebagai pasien.")
        return

    # Cari pembayaran yang masih pending untuk user ini
    pending_payments = []
    total_pending = 0
    
    for pid, pinfo in data["payments"].items():
        if pinfo["patient_id"] == patient_id and pinfo["status"] == "Pending":
            pending_payments.append((pid, pinfo))
            total_pending += pinfo["amount"]

    if not pending_payments:
        print(Fore.GREEN + "Tidak ada tagihan yang belum dibayar.")
        return

    print(f"{H}Daftar Tagihan Belum Dibayar:{R}")
    for payment_id, payment_info in pending_payments:
        # Dapatkan info appointment
        appointment_info = data["appointments"].get(payment_info["appointment_id"], {})
        schedule_info = data["schedules"].get(appointment_info.get("schedule_id", ""), {})
        doctor_info = data["doctors"].get(schedule_info.get("doctor_id", ""), {"name": "Tidak Ditemukan"})
        
        print(f"\nID Pembayaran: {payment_id}")
        print(f"  Jenis Layanan: {payment_info['service_type']}")
        print(f"  Dokter: {doctor_info.get('name', 'Tidak Ditemukan')}")
        print(f"  Jumlah: {H}Rp {payment_info['amount']:,}{R}")
        print(f"  Status: {Fore.YELLOW}{payment_info['status']}{R}")
        
        if appointment_info.get('booking_date'):
            print(f"  Tanggal Janji: {appointment_info['booking_date']}")

    print(f"\n{H}Total Tagihan: Rp {total_pending:,}{R}")

# --- Fungsi Lihat Riwayat Pembayaran User ---
def lihat_riwayat_pembayaran_user(data, current_username, patient_id):
    print(f"\n--- {H}Riwayat Pembayaran Saya{R} ---")

    if not patient_id:
        print(Fore.RED + "Anda belum terdaftar sebagai pasien.")
        return

    # Cari semua pembayaran untuk user ini
    user_payments = []
    total_paid = 0
    
    for pid, pinfo in data["payments"].items():
        if pinfo["patient_id"] == patient_id:
            user_payments.append((pid, pinfo))
            if pinfo["status"] == "Paid":
                total_paid += pinfo["amount"]

    if not user_payments:
        print(Fore.YELLOW + "Belum ada riwayat pembayaran.")
        return

    print(f"{H}Riwayat Pembayaran:{R}")
    for payment_id, payment_info in user_payments:
        # Dapatkan info appointment
        appointment_info = data["appointments"].get(payment_info["appointment_id"], {})
        schedule_info = data["schedules"].get(appointment_info.get("schedule_id", ""), {})
        doctor_info = data["doctors"].get(schedule_info.get("doctor_id", ""), {"name": "Tidak Ditemukan"})
        
        status_color = H if payment_info["status"] == "Paid" else Fore.YELLOW
        status_text = "LUNAS" if payment_info["status"] == "Paid" else "BELUM BAYAR"
        
        print(f"\nID Pembayaran: {payment_id}")
        print(f"  Jenis Layanan: {payment_info['service_type']}")
        print(f"  Dokter: {doctor_info.get('name', 'Tidak Ditemukan')}")
        print(f"  Jumlah: Rp {payment_info['amount']:,}")
        print(f"  Status: {status_color}{status_text}{R}")
        print(f"  Metode: {payment_info.get('payment_method', '-')}")
        
        if payment_info.get('payment_date'):
            print(f"  Tanggal Bayar: {payment_info['payment_date']}")
        else:
            print(f"  Tanggal Bayar: -")

    print(f"\n{H}Total Sudah Dibayar: Rp {total_paid:,}{R}")

# --- Fungsi Bayar Tagihan User ---
def bayar_tagihan_user(data, current_username, patient_id):
    print(f"\n--- {H}Bayar Tagihan{R} ---")

    if not patient_id:
        print(Fore.RED + "Anda belum terdaftar sebagai pasien.")
        return

    # Tampilkan tagihan yang masih pending
    pending_payments = []
    for pid, pinfo in data["payments"].items():
        if pinfo["patient_id"] == patient_id and pinfo["status"] == "Pending":
            pending_payments.append((pid, pinfo))

    if not pending_payments:
        print(Fore.GREEN + "Tidak ada tagihan yang perlu dibayar.")
        return

    print(f"{H}Tagihan yang Belum Dibayar:{R}")
    for payment_id, payment_info in pending_payments:
        appointment_info = data["appointments"].get(payment_info["appointment_id"], {})
        schedule_info = data["schedules"].get(appointment_info.get("schedule_id", ""), {})
        doctor_info = data["doctors"].get(schedule_info.get("doctor_id", ""), {"name": "Tidak Ditemukan"})
        
        print(f"ID: {payment_id} - {payment_info['service_type']} - Dokter: {doctor_info.get('name', 'Tidak Ditemukan')} - Rp {payment_info['amount']:,}")

    payment_id = input("\nMasukkan ID Pembayaran yang akan dibayar: ")
    
    # Cek apakah payment_id valid
    if payment_id not in data["payments"]:
        print(Fore.RED + "ID Pembayaran tidak ditemukan.")
        return
        
    payment_info = data["payments"][payment_id]
    
    # Cek apakah pembayaran ini milik user yang login
    if payment_info["patient_id"] != patient_id:
        print(Fore.RED + "Anda tidak memiliki akses untuk membayar tagihan ini.")
        return
        
    # Cek apakah sudah dibayar
    if payment_info["status"] == "Paid":
        print(Fore.YELLOW + "Tagihan ini sudah dibayar.")
        return

    # Tampilkan detail pembayaran
    appointment_info = data["appointments"].get(payment_info["appointment_id"], {})
    schedule_info = data["schedules"].get(appointment_info.get("schedule_id", ""), {})
    doctor_info = data["doctors"].get(schedule_info.get("doctor_id", ""), {"name": "Tidak Ditemukan"})
    
    print(f"\n{H}Detail Pembayaran:{R}")
    print(f"Jenis Layanan: {payment_info['service_type']}")
    print(f"Dokter: {doctor_info.get('name', 'Tidak Ditemukan')}")
    print(f"Jumlah: {H}Rp {payment_info['amount']:,}{R}")
    
    # Pilih metode pembayaran
    print(f"\n{H}Pilih Metode Pembayaran:{R}")
    print("1. Transfer Bank")
    print("2. Kartu Kredit/Debit")
    print("3. E-Wallet")
    print("4. Cash (Bayar di Loket)")
    
    method_choice = input("Pilih metode (1-4): ")
    
    if method_choice == '1':
        payment_method = "Transfer Bank"
        print("\nSilakan transfer ke:")
        print("Bank: BCA")
        print("No. Rekening: 123-456-7890")
        print("a.n: Rumah Sakit Sehat Sentosa")
        print(f"Jumlah: Rp {payment_info['amount']:,}")
        input("\nTekan Enter setelah transfer...")
        
    elif method_choice == '2':
        payment_method = "Kartu Kredit/Debit"
        card_number = input("Masukkan nomor kartu: ")
        expiry_date = input("Masukkan tanggal kadaluarsa (MM/YY): ")
        cvv = input("Masukkan CVV: ")
        print("Verifikasi pembayaran...")
        time.sleep(2)
        
    elif method_choice == '3':
        payment_method = "E-Wallet"
        print("Pilih E-Wallet:")
        print("1. Gopay")
        print("2. OVO")
        print("3. Dana")
        print("4. LinkAja")
        ewallet_choice = input("Pilih (1-4): ")
        ewallet_options = {
            "1": "Gopay",
            "2": "OVO", 
            "3": "Dana",
            "4": "LinkAja"
        }
        payment_method = f"E-Wallet ({ewallet_options.get(ewallet_choice, 'Gopay')})"
        print(f"Silakan bayar menggunakan {payment_method}")
        input("Tekan Enter setelah pembayaran...")
        
    elif method_choice == '4':
        payment_method = "Cash"
        print("Silakan bayar di loket rumah sakit")
        input("Tekan Enter untuk konfirmasi...")
        
    else:
        payment_method = "Transfer Bank"
        print("Metode default: Transfer Bank")
        input("Tekan Enter untuk konfirmasi...")

    # Konfirmasi pembayaran
    confirm = input(f"\nKonfirmasi pembayaran Rp {payment_info['amount']:,} via {payment_method}? (y/n): ").lower()
    if confirm == 'y':
        data["payments"][payment_id]["status"] = "Paid"
        data["payments"][payment_id]["payment_method"] = payment_method
        data["payments"][payment_id]["payment_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(data)
        
        print(f"\n{H}=== PEMBAYARAN BERHASIL ==={R}")
        print(f"ID Pembayaran: {payment_id}")
        print(f"Jumlah: Rp {payment_info['amount']:,}")
        print(f"Metode: {payment_method}")
        print(f"Tanggal: {data['payments'][payment_id]['payment_date']}")
        print(f"{H}Terima kasih telah melakukan pembayaran!{R}")
        
    else:
        print("Pembayaran dibatalkan.")

# --- Fungsi Lihat Riwayat Rawat Inap User ---
def lihat_riwayat_inap(data, current_username, patient_id):
    print("\n--- Riwayat Rawat Inap ---")

    if not patient_id:
        print(Fore.RED + "Anda belum terdaftar sebagai pasien.")
        return

    # Ambil daftar rawat inap berdasarkan patient_id
    patient_admissions = [
        (aid, ainfo) for aid, ainfo in data["admissions"].items()
        if ainfo["patient_id"] == patient_id
    ]

    if not patient_admissions:
        print(Fore.YELLOW + "Anda belum memiliki riwayat rawat inap.")
        return

    print(f"{H}Riwayat Rawat Inap:{R}")
    for aid, ainfo in patient_admissions:
        # Ambil data appointment (janji) terkait
        appointment = data["appointments"].get(ainfo["appointment_id"], None)
        schedule = None
        doctor = None

        if appointment:
            schedule = data["schedules"].get(appointment["schedule_id"], None)
            if schedule:
                doctor = data["doctors"].get(schedule["doctor_id"], {"name": "Tidak Ditemukan"})

        room = data["rooms"].get(ainfo["room_id"], {"name": "Tidak Ditemukan", "type": "-"})

        print(f"\nID Rawat Inap: {aid}")
        print(f"  Ruangan: {H}{room['name']} ({room['type']}){R}")
        print(f"  Tanggal Masuk: {ainfo['admission_date']}")
        print(f"  Tanggal Keluar: {ainfo['discharge_date']}")
        print(f"  Status: {H}{ainfo['status']}{R}")

        if doctor:
            print(f"  Dokter Penanggung Jawab: {doctor['name']}")
        else:
            print(Fore.YELLOW + "  Dokter tidak ditemukan.")

        # Cek apakah ada data checkup terkait admission tersebut
        related_checkup = None
        for cid, cinfo in data["checkups"].items():
            if cinfo["appointment_id"] == ainfo["appointment_id"]:
                related_checkup = cinfo
                break

        if related_checkup:
            print(f"  Diagnosis: {H}{related_checkup['diagnosis']}{R}")
            print(f"  Catatan Dokter: {H}{related_checkup['notes']}{R}")
        else:
            print(Fore.YELLOW + "  Belum ada data pemeriksaan / checkup untuk rawat inap ini.")

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
def buat_janji_user(data, current_username, patient_id):
    print("\n--- Buat Janji Saya ---")

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
    
    # Otomatis buat data pembayaran untuk janji baru
    payment_id = str(len(data["payments"]) + 1)
    data["payments"][payment_id] = {
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "amount": 150000,  # Biaya default konsultasi
        "payment_date": "",
        "status": "Pending",
        "payment_method": "",
        "service_type": "Konsultasi Umum"
    }
    
    save_data(data)
    print(f"{H}[🗸] Janji berhasil dibuat untuk Anda!{R}")
    print(f"{H}Tagihan sebesar Rp 150.000 telah dibuat. Silakan cek menu Pembayaran.{R}")

# --- Fungsi Lihat Janji Saya (untuk User) ---
def lihat_janji_user(data, current_username, patient_id):
    print("\n--- Janji Saya ---")

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
        
        # Cek status pembayaran
        payment_status = "Belum Bayar"
        for pid, pinfo in data["payments"].items():
            if pinfo["appointment_id"] == aid:
                payment_status = "Lunas" if pinfo["status"] == "Paid" else "Belum Bayar"
                break
        
        payment_color = H if payment_status == "Lunas" else Fore.YELLOW
        
        print(f"ID Janji: {aid}, Dokter: {doctor_info['name']}, Departemen: {dept_info['name']}")
        print(f"  Tanggal: {sinfo['available_date']}, Waktu: {sinfo['available_time']}")
        print(f"  Status Janji: {H}{ainfo['status']}{R}, Status Bayar: {payment_color}{payment_status}{R}")
        print()

# --- Fungsi Lihat Riwayat Kesehatan Saya (untuk User) ---
def lihat_riwayat_user(data, current_username, patient_id):
    print("\n--- Riwayat Kesehatan Saya ---")

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