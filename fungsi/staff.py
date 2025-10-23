import datetime
import time
from colorama import Fore
from fungsi.color import *
from fungsi.core import *




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
        print("7. Data Pembayaran")
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
        elif choice == '7':
            clear_screen()
            menu_pembayaran(data)
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
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        "booking_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
        print("3. Data Pembayaran")
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
                            "checkup_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
                        "checkup_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "diagnosis": diagnosis,
                        "notes": notes
                    }
                    print(f"{H}[🗸] Data pemeriksaan berhasil ditambahkan.{R}")
                
                # Ubah status janji menjadi Completed
                data["appointments"][app_id]["status"] = "Completed"
                
                # Otomatis buat data pembayaran jika belum ada
                payment_exists = any(pinfo["appointment_id"] == app_id for pinfo in data["payments"].values())
                if not payment_exists:
                    payment_id = str(len(data["payments"]) + 1)
                    patient_id = data["appointments"][app_id]["patient_id"]
                    
                    # Tentukan biaya berdasarkan jenis layanan
                    print(f"\n{H}--- Input Data Pembayaran ---{R}")
                    print("Jenis Layanan:")
                    print("1. Konsultasi Umum (Rp 150.000)")
                    print("2. Konsultasi Spesialis (Rp 250.000)") 
                    print("3. Emergency (Rp 500.000)")
                    print("4. Lainnya (Input Manual)")
                    
                    service_choice = input("Pilih jenis layanan (1-4): ")
                    if service_choice == '1':
                        amount = 150000
                        service_type = "Konsultasi Umum"
                    elif service_choice == '2':
                        amount = 250000
                        service_type = "Konsultasi Spesialis"
                    elif service_choice == '3':
                        amount = 500000
                        service_type = "Emergency"
                    else:
                        amount = int(input("Masukkan jumlah biaya manual: Rp "))
                        service_type = input("Jenis layanan: ")
                    
                    data["payments"][payment_id] = {
                        "appointment_id": app_id,
                        "patient_id": patient_id,
                        "amount": amount,
                        "payment_date": "",
                        "status": "Pending",
                        "payment_method": "",
                        "service_type": service_type
                    }
                    print(f"{H}[🗸] Data pembayaran berhasil dibuat - ID: {payment_id}{R}")
                
                save_data(data)
                print(f"Status janji untuk ID tersebut telah diperbarui menjadi '{H}Completed{R}'.")

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
        
        elif choice == '3':
            menu_pembayaran(data)
            
        elif choice == '0':
            time.sleep(2)
            clear_screen()
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            time.sleep(1)
            clear_screen()

# --- Fungsi Menu Pembayaran ---
def menu_pembayaran(data):
    while True:
        print(f"\n--- {H}Menu Data Pembayaran{R} ---")
        print("1. Lihat Semua Data Pembayaran")
        print("2. Proses Pembayaran")
        print("3. Edit Data Pembayaran")
        print("4. Hapus Data Pembayaran")
        print("0. Kembali ke Menu Sebelumnya")
        choice = input("Pilih menu: ")

        if choice == '1':
            if not data["payments"]:
                print(Fore.YELLOW + "\nBelum ada data pembayaran.")
            else:
                print(f"\n{H}Daftar Semua Pembayaran:{R}")
                total_paid = 0
                total_pending = 0
                
                for pid, pinfo in data["payments"].items():
                    patient_info = data["patients"].get(pinfo["patient_id"], {"name": "Tidak Ditemukan"})
                    appointment_info = data["appointments"].get(pinfo["appointment_id"], {})
                    
                    status_color = H if pinfo["status"] == "Paid" else Fore.YELLOW
                    print(f"ID: {pid}, Pasien: {patient_info['name']}, Janji ID: {pinfo['appointment_id']}")
                    print(f"  Layanan: {pinfo['service_type']}, Jumlah: Rp {pinfo['amount']:,}")
                    print(f"  Status: {status_color}{pinfo['status']}{R}, Metode: {pinfo.get('payment_method', '-')}")
                    print(f"  Tanggal Bayar: {pinfo.get('payment_date', '-')}")
                    print()
                    
                    # Hitung total
                    if pinfo["status"] == "Paid":
                        total_paid += pinfo["amount"]
                    else:
                        total_pending += pinfo["amount"]
                
                print(f"{H}Summary:{R}")
                print(f"Total Pembayaran Lunas: Rp {total_paid:,}")
                print(f"Total Pembayaran Pending: Rp {total_pending:,}")
                print(f"Grand Total: Rp {total_paid + total_pending:,}")

        elif choice == '2':
            # Tampilkan pembayaran yang pending
            pending_payments = {pid: pinfo for pid, pinfo in data["payments"].items() if pinfo["status"] == "Pending"}
            
            if not pending_payments:
                print(Fore.YELLOW + "\nTidak ada pembayaran yang pending.")
                continue
                
            print(f"\n{H}Daftar Pembayaran Pending:{R}")
            for pid, pinfo in pending_payments.items():
                patient_info = data["patients"].get(pinfo["patient_id"], {"name": "Tidak Ditemukan"})
                print(f"ID: {pid}, Pasien: {patient_info['name']}, Layanan: {pinfo['service_type']}, Jumlah: Rp {pinfo['amount']:,}")
            
            payment_id = input("\nMasukkan ID Pembayaran yang akan diproses: ")
            if payment_id not in pending_payments:
                print(Fore.RED + "ID Pembayaran tidak ditemukan atau sudah diproses.")
                continue
                
            payment_info = data["payments"][payment_id]
            patient_info = data["patients"].get(payment_info["patient_id"], {"name": "Tidak Ditemukan"})
            
            print(f"\n{H}Detail Pembayaran:{R}")
            print(f"Pasien: {patient_info['name']}")
            print(f"Layanan: {payment_info['service_type']}")
            print(f"Jumlah: Rp {payment_info['amount']:,}")
            
            # Pilih metode pembayaran
            print(f"\n{H}Metode Pembayaran:{R}")
            print("1. Cash")
            print("2. Transfer Bank")
            print("3. Kartu Kredit/Debit")
            method_choice = input("Pilih metode pembayaran (1-3): ")
            
            if method_choice == '1':
                payment_method = "Cash"
            elif method_choice == '2':
                payment_method = "Transfer Bank"
            elif method_choice == '3':
                payment_method = "Kartu Kredit/Debit"
            else:
                payment_method = "Cash"
                
            # Konfirmasi pembayaran
            confirm = input(f"\nKonfirmasi pembayaran Rp {payment_info['amount']:,} via {payment_method}? (y/n): ").lower()
            if confirm == 'y':
                data["payments"][payment_id]["status"] = "Paid"
                data["payments"][payment_id]["payment_method"] = payment_method
                data["payments"][payment_id]["payment_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_data(data)
                print(f"{H}[🗸] Pembayaran berhasil diproses!{R}")
            else:
                print("Proses pembayaran dibatalkan.")

        elif choice == '3':
            if not data["payments"]:
                print(Fore.YELLOW + "\nBelum ada data pembayaran.")
                continue
                
            print(f"\n{H}Daftar Pembayaran:{R}")
            for pid, pinfo in data["payments"].items():
                patient_info = data["patients"].get(pinfo["patient_id"], {"name": "Tidak Ditemukan"})
                status_color = H if pinfo["status"] == "Paid" else Fore.YELLOW
                print(f"ID: {pid}, Pasien: {patient_info['name']}, Status: {status_color}{pinfo['status']}{R}, Jumlah: Rp {pinfo['amount']:,}")
            
            payment_id = input("\nMasukkan ID Pembayaran yang akan diedit: ")
            if payment_id not in data["payments"]:
                print(Fore.RED + "ID Pembayaran tidak ditemukan.")
                continue
                
            payment_info = data["payments"][payment_id]
            print(f"\nData saat ini:")
            print(f"Jumlah: Rp {payment_info['amount']:,}")
            print(f"Status: {payment_info['status']}")
            print(f"Metode: {payment_info.get('payment_method', '-')}")
            print(f"Layanan: {payment_info['service_type']}")
            
            new_amount = input(f"Jumlah Baru (sekarang: {payment_info['amount']}): ") or payment_info['amount']
            new_service = input(f"Layanan Baru (sekarang: {payment_info['service_type']}): ") or payment_info['service_type']
            
            try:
                new_amount = int(new_amount)
            except ValueError:
                print(Fore.RED + "Jumlah harus angka.")
                continue
                
            data["payments"][payment_id]["amount"] = new_amount
            data["payments"][payment_id]["service_type"] = new_service
            save_data(data)
            print(f"{H}[🗸] Data pembayaran berhasil diupdate.{R}")

        elif choice == '4':
            if not data["payments"]:
                print(Fore.YELLOW + "\nBelum ada data pembayaran.")
                continue
                
            print(f"\n{H}Daftar Pembayaran:{R}")
            for pid, pinfo in data["payments"].items():
                patient_info = data["patients"].get(pinfo["patient_id"], {"name": "Tidak Ditemukan"})
                status_color = H if pinfo["status"] == "Paid" else Fore.YELLOW
                print(f"ID: {pid}, Pasien: {patient_info['name']}, Status: {status_color}{pinfo['status']}{R}, Jumlah: Rp {pinfo['amount']:,}")
            
            payment_id = input("\nMasukkan ID Pembayaran yang akan dihapus: ")
            if payment_id not in data["payments"]:
                print(Fore.RED + "ID Pembayaran tidak ditemukan.")
                continue
                
            confirm = input("Apakah Anda yakin ingin menghapus data pembayaran ini? (y/n): ").lower()
            if confirm == 'y':
                del data["payments"][payment_id]
                save_data(data)
                print(f"{H}[🗸] Data pembayaran berhasil dihapus.{R}")
            else:
                print("Penghapusan dibatalkan.")

        elif choice == '0':
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
                    data["admissions"][admission_id]["discharge_date_actual"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
