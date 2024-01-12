import xmlrpc.client  # Mengimpor modul xmlrpc.client

queue_ids = []  # Mendefinisikan variabel global untuk menyimpan ID antrian

class ClinicClient:  # Mendefinisikan kelas ClinicClient
    def __init__(self, server_address):  # Fungsi konstruktor untuk kelas ClinicClient
        # Menghubungkan ke server menggunakan alamat server
        self.server = xmlrpc.client.ServerProxy(server_address)

    def register_patient(self, clinic_id, patient_info):  # Fungsi untuk mendaftarkan pasien
        queue_id = self.server.register_patient(clinic_id, patient_info)  # Memanggil fungsi register_patient pada server
        if queue_id == "none":  # Jika pendaftaran gagal
            print(f"Pendaftaran gagal. Klinik sedang tutup")
            return None
        else:
            queue_ids.append(queue_id)  # Menambahkan ID antrian ke daftar
            print(f"Pendaftaran berhasil. Kode antrian: {queue_id}")
            return queue_id

    def get_queue_status(self, clinic_id):  # Fungsi untuk mendapatkan status antrian
        status = self.server.get_queue_status(clinic_id)  # Memanggil fungsi get_queue_status pada server
        print(f"{status}")  # Mencetak status antrian

    def get_menu(self):  # Fungsi untuk mendapatkan menu
        print(self.server.get_menu())  # Memanggil fungsi get_menu pada server dan mencetak hasilnya

if __name__ == "__main__":  # Jika file dijalankan sebagai skrip utama
    server_address = "http://127.0.0.1:8000"  # Mendefinisikan alamat server
    client = ClinicClient(server_address)  # Membuat instance dari ClinicClient

    client.get_menu()  # Memanggil fungsi untuk menampilkan menu

    pilihan_menu = int(input("Pilihan menu: "))  # Meminta input dari pengguna untuk pilihan menu
    while (pilihan_menu <= 3 and pilihan_menu >= 1) or pilihan_menu == 9:  # Loop selama pilihan menu valid

        if pilihan_menu != 9:  # Jika pilihan bukan 9
            name = input("Nama Lengkap: ")  # Meminta input nama lengkap
            dob = input("Tanggal Lahir (contoh: 30-01-2003): ")  # Meminta input tanggal lahir

            patient_info = {"name": name, "dob": dob}  # Membuat dictionary informasi pasien
            queue_id = client.register_patient(pilihan_menu, patient_info)  # Mendaftarkan pasien
            if queue_id != None:  # Jika pendaftaran berhasil
                client.get_queue_status(queue_id)  # Mendapatkan status antrian
        elif pilihan_menu == 9:  # Jika pilihan adalah 9
            if len(queue_ids) > 0:  # Jika ada ID antrian

                for queue_id in queue_ids:  # Iterasi melalui setiap ID antrian
                    client.get_queue_status(queue_id)  # Mendapatkan status untuk setiap antrian
            else:
                print("Anda belum melakukan registrasi")  # Jika belum ada pendaftaran
        client.get_menu()  # Menampilkan menu lagi
        pilihan_menu = int(input("Pilihan menu: "))  # Meminta input pilihan menu lagi
