from xmlrpc.server import SimpleXMLRPCServer  # Mengimpor SimpleXMLRPCServer dari modul xmlrpc.server
import threading  # Mengimpor modul threading untuk threading
import time  # Mengimpor modul time untuk manipulasi waktu

QUEUE_TIME = 10  # Konstanta untuk waktu antrian

class ClinicServer:  # Mendefinisikan kelas ClinicServer
    def __init__(self):  # Fungsi konstruktor untuk kelas ClinicServer
        # Mendefinisikan status klinik dengan beberapa data klinik
        self.klinik_status = {
            1: {"name": "Klinik A", "status": "Buka", "queue_wait_time": [], "queue_patients": []},
            2: {"name": "Klinik B", "status": "Tutup", "queue_wait_time": [], "queue_patients": []},
            3: {"name": "Klinik C", "status": "Buka", "queue_wait_time": [], "queue_patients": []},
        }

        self.thread_dequeue = threading.Thread(target=self.dequeue)  # Membuat thread baru untuk fungsi dequeue

    def dequeue(self):  # Mendefinisikan fungsi dequeue
        while True:  # Loop tak terbatas
            time.sleep(QUEUE_TIME)  # Tidur selama waktu antrian
            print("UPDATING QUEUES...")  # Mencetak pesan
            for clinic_id in self.klinik_status.keys():  # Iterasi melalui setiap klinik
                # Mengupdate waktu tunggu di setiap klinik
                for i in range(len(self.klinik_status[clinic_id]["queue_wait_time"])):
                    self.klinik_status[clinic_id]["queue_wait_time"][i] = max([0, self.klinik_status[clinic_id]["queue_wait_time"][i] - QUEUE_TIME])
                # Mencetak status waktu tunggu terakhir
                print(f'{self.klinik_status[clinic_id]["name"]}: last queue waiting time = {max([0] + self.klinik_status[clinic_id]["queue_wait_time"])}')

    def register_patient(self, clinic_id, patient_info):  # Fungsi untuk mendaftarkan pasien
        if (self.klinik_status[clinic_id]["status"] == "Tutup"):  # Jika klinik tutup
            return "none"  # Mengembalikan "none"

        # Menambahkan pasien ke antrian
        self.klinik_status[clinic_id]["queue_patients"].append(patient_info)

        # Menghitung dan memperbarui waktu tunggu antrian
        last_queue_wait_time = max(self.klinik_status[clinic_id]["queue_wait_time"] + [0])
        self.klinik_status[clinic_id]["queue_wait_time"].append(last_queue_wait_time + QUEUE_TIME)

        return f"{clinic_id}{len(self.klinik_status[clinic_id]['queue_patients']) - 1}"  # Mengembalikan ID antrian

    def get_queue_status(self, queue_id):  # Fungsi untuk mendapatkan status antrian
        clinic_id = int(queue_id[0])  # Mengambil ID klinik dari ID antrian
        queue_wait_time_index = int(queue_id[1:])  # Mengambil index waktu tunggu dari ID antrian
        estimation_wait_time = self.klinik_status[clinic_id]["queue_wait_time"][queue_wait_time_index]  # Menghitung estimasi waktu tunggu
        return f"Estimasi waktu tunggu kode antrian {queue_id}: {estimation_wait_time}"  # Mengembalikan estimasi waktu tunggu

    def get_menu(self):  # Fungsi untuk mendapatkan menu
        menu_text = "Selamat Datang di Antredis\n"
        menu_text += "No.\tNama\t\tStatus\tEstimasi Waktu Tunggu\n"
        for id in self.klinik_status.keys():  # Iterasi melalui setiap klinik
            # Menambahkan informasi klinik ke teks menu
            menu_text += f"{id}.\t{self.klinik_status[id]['name']}\t{self.klinik_status[id]['status']}\t{max([0] + self.klinik_status[id]['queue_wait_time'])}\n"
        
        menu_text += "9. Lihat semua status antrian\n"
        menu_text += "0. Keluar"
        return menu_text  # Mengembalikan teks menu

def run_server():  # Fungsi untuk menjalankan server
    server = SimpleXMLRPCServer(("0.0.0.0", 8000))  # Membuat server XMLRPC di alamat tertentu
    clinic_server = ClinicServer()  # Membuat instance dari ClinicServer
    server.register_instance(clinic_server)  # Mendaftarkan instance ClinicServer ke server
    print("Server listening on port 8000...")  # Mencetak pesan

    clinic_server.thread_dequeue.start()  # Memulai thread dequeue
    server.serve_forever()  # Menjalankan server selamanya
    clinic_server.thread_dequeue.join()  # Menunggu thread dequeue selesai

if __name__ == "__main__":  # Jika file dijalankan sebagai skrip utama
    run_server()  # Menjalankan fungsi run_server
