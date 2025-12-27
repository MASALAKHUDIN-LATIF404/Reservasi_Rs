import json
import os

from colorama import Fore # Import Fore untuk penggunaan warna


DATA_FILE = "hospital_data_extended.json"

# sebuah fungsi untuk membersihkan layar terminal
def clear_screen():
    nama_os = os.name # untuk mendeteksi nama sistem operasi yang digunakan ('nt' = Windows, 'posix' = Linux/Mac)
    if nama_os == 'nt': # Jika sistem operasi terdeteksi Windows
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
                default_data = get_default_data_structure()
                save_data(default_data)
                return default_data
    else:
        default_data = get_default_data_structure()
        save_data(default_data)
        return default_data

def get_default_data_structure():
    return {
        "users": {
            "admin": {"id": "1", "password": "adminpass", "role": "admin"},
            "staff": {"id": "2", "password": "staffpass", "role": "staff"}
        },
        "departemen": {
            "1": {"nama": "Penyakit Dalam"},
            "2": {"nama": "Bedah"},
            "3": {"nama": "Anak"},
            "4": {"nama": "Kandungan"}
        },
        "dokter": {
            "1": {"nama": "Dr. Ahmad", "id_spesialis": "1", "telepon": "081234567890"},
            "2": {"nama": "Dr. Siti", "id_spesialis": "2", "telepon": "081234567891"},
            "3": {"nama": "Dr. Budi", "id_spesialis": "3", "telepon": "081234567892"}
        },
        "kamar": {
            "1": {"nama": "Melati 101", "tipe": "VIP", "tersedia": True},
            "2": {"nama": "Anggrek 202", "tipe": "Kelas 1", "tersedia": True},
            "3": {"nama": "Mawar 303", "tipe": "Kelas 2", "tersedia": False}
        },
        "pasien": {},
        "jadwal": {},
        "janji_temu": {},
        "pemeriksaan": {},
        "rawat_inap": {}, # Rawat Inap
        "pembayaran": {} # Tambahkan kunci 'pembayaran'
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
