import json
import os



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

# sebuah fungsi untuk membersihkan layar terminal
def clear_screen():
    os_name = os.name # untuk mendeteksi nama sistem operasi yang digunakan ('nt' = Windows, 'posix' = Linux/Mac)
    if os_name == 'nt': # Jika sistem operasi terdeteksi Windows
        os.system('cls') # Otomatis jalankan perintah 'cls' untuk membersihkan layar terminal di Windows
    else: # Jika sistem operasi terdeteksi Linux/Mac
        os.system('clear') # Otomatis jalankan perintah 'clear' untuk membersihkan layar terminal di Linux/Mac
