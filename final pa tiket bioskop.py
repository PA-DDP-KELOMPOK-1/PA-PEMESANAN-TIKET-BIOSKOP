import csv
from prettytable import PrettyTable
import pwinput
import datetime

file_film = "data_film.csv"
file_kursi = "data_kursi.csv"
file_data = "data_akun.csv"

def registrasi():
    nama = input("Masukkan nama: ")
    password = pwinput.pwinput("Masukkan password anda: ")
    role = 'user'
    saldo = 0 
    found = False
    with open(file_data, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == nama:
                found = True
                print(f"Nama {nama} sudah tersedia, Silahkan login atau gunakan nama yang lain!")
                return

    if not found:
        with open(file_data, mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([nama, password, role, saldo])
        print(f"Halo {nama}, Sudah berhasil registrasi, Silahkan login yaaa!!!!")

def tambah_film():
    nama_film = input("Masukkan Nama Film: ")
    rating_film = input("Masukkan Rating Film: ")

    while True:
        try:
            harga_tiket = int(input("Masukkan Harga Tiket: Rp."))
            break
        except ValueError:
            print("Harga tiket harus berupa angka")

    while True:
        try:
            kursi_tersedia = int(input("Masukkan jumlah kursi yang tersedia: "))
            break
        except ValueError:
            print("Jumlah kursi harus berupa angka")

    found = False
    try:
        with open(file_film, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == nama_film:
                    found = True
                    print(f"Film {nama_film} sudah ada!")
                    return

        if not found:
            with open(file_film, mode='a', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([nama_film, rating_film, harga_tiket])
            print(f"Film {nama_film} berhasil ditambahkan.")

        with open(file_kursi, mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            for kursi in range(1, kursi_tersedia + 1):
                csv_writer.writerow([nama_film, f"{kursi}", "tersedia"])
            print(f"Kursi untuk film {nama_film} berhasil ditambahkan")
    except Exception as e:
        print(f"Terjadi error pada  {e}")


def daftar_film():
    try:
        print("\nFilm yang tersedia saat ini")
        table = PrettyTable()
        table.field_names = ["Film","Rating","Harga"]
        found = False

        with open(file_film, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) == 3:  
                    table.add_row(row)
                    found = True

        if found:
            print(table)
        else:
            print("Tidak ada film yang tersedia.")
    
    except Exception as e:
        print(f"Terjadi error: {e}")

def update_film():
    daftar_film()
    nama_film = input("Film yang ingin diubah: ")
    rating_film = input("Rating film: ")

    while True:
        try:
            harga_tiket = int(input("Harga tiket: Rp."))
            break
        except ValueError:
            print("Harga tiket harus berupa angka")

    updated_rows = []
    found = False

    with open(file_film, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == nama_film:
                updated_rows.append([nama_film, rating_film, harga_tiket])
                found = True
                print(f"Film {nama_film} berhasil diperbarui")
            else:
                updated_rows.append(row)

    if not found:
        print(f"Film {nama_film} tidak ditemukan")
        return
    
    with open(file_film, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(updated_rows)


def hapus_film():
    daftar_film()
    nama_film = input("Nama film yang ingin dihapus: ")
    updated_rows = []
    found = False
    with open(file_film, mode='r') as file:
        csv_reader = list(csv.reader(file))
        for row in csv_reader:
            if row[0] == nama_film:
                found = True
                print(f"Film {nama_film} berhasil dihapus")
            else:
                updated_rows.append(row)

    if not found:
        print(f"Film tidak ada dalam data")
        return

    with open(file_film, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(updated_rows)

    updated_kursi_rows = []
    with open(file_kursi, mode='r') as file:
        kursi_reader = csv.reader(file)
        for row in kursi_reader:
            if row[0].lower() != nama_film.lower():
                updated_kursi_rows.append(row)

    with open(file_kursi, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(updated_kursi_rows)

    print(f"Kursi untuk film {nama_film} berhasil dihapus.")


def tambah_saldo():
    nama = input("Masukkan nama user: ")
    password = pwinput.pwinput(prompt="Masukkan Password: ")

    while True:
        try:
            saldo_baru = int(input("Masukkan jumlah saldo yang ingin ditambahkan: Rp."))
            break
        except ValueError:
            print("Saldo harus berupa angka")

    updated_rows = []
    found = False

    with open(file_data, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == nama and row[1] == password:
                saldo_lama = int(row[3])
                saldo_total = saldo_lama + saldo_baru
                updated_rows.append([nama, password, 'user', saldo_total])
                found = True
                print(f"Saldo {nama} berhasil ditambahkan. Saldo sekarang: Rp.{saldo_total}")
            else:
                updated_rows.append(row)

    if not found:
        print(f"User {nama} tidak ditemukan")
        return

    with open(file_data, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(updated_rows)

def search_film():
    search = input("Ingin mencari film apa: ")
    found = False

    with open(file_film, mode='r') as file:
        table = PrettyTable()
        table.field_names = ["Film", "Rating", "Harga"]
        
        for row in csv.reader(file):
            if search.lower() in row[0].lower():  
                table.add_row(row)
                found = True

        if found:
            print("Hasil pencarian film:")
            print(table)
        
        if not found:
            print("Film tidak ada!")
            return

def sort_film():
    table = PrettyTable()
    table.field_names = ["No", "Urutkan dari"]
    table.add_row(["1", "Dari Z-A"])
    table.add_row(["2", "Dari A-Z"])
    print(table)

    pilih = input("Pilih cara pengurutan (1/2): ")

    with open(file_film, mode='r') as file:
        films = list(csv.reader(file))

    if pilih == '1':
        films.sort(key=lambda x: x[0].lower(), reverse=True)
    elif pilih == '2':
        films.sort(key=lambda x: x[0].lower())
    else:
        print("Pilihan tidak valid.")
        return

    result_table = PrettyTable()
    result_table.field_names = ["Nama", "Rating", "Harga"]

    for row in films:
        result_table.add_row(row)

    print("Hasil pengurutan film:")
    print(result_table)

def pesan_tiket():
    daftar_film()
    nama_film = input("Masukkan nama film yang ingin dipesan: ")
    nama_user = input("Masukkan nama pengguna: ")

    with open(file_film, mode='r') as file:
        film_reader = list(csv.reader(file))
        film_data = None
        for row in film_reader:
            if row[0].lower() == nama_film.lower():
                film_data = row
                break

    if not film_data:
        print(f"Film '{nama_film}' tidak ditemukan.")
        return

    try:
        harga_tiket = int(film_data[2])
    except ValueError:
        print("Harga tiket tidak valid.")
        return

    with open(file_data, mode='r') as file:
        akun_reader = list(csv.reader(file))
        user_data = None
        for row in akun_reader:
            if row[0] == nama_user:
                user_data = row
                break

    if not user_data:
        print("Akun tidak ditemukan.")
        return

    saldo_user = int(user_data[3])
    emoney = saldo_user
    if emoney < harga_tiket:
        print("Saldo E-money tidak cukup untuk memesan tiket.")
        return

    with open(file_kursi, mode='r') as file:
        kursi_reader = list(csv.reader(file))
        kursi_tersedia = []
        for row in kursi_reader:
            if row[0].lower() == nama_film.lower() and row[2] == "tersedia":
                kursi_tersedia.append(row[1])  

    if not kursi_tersedia:
        print(f"Tidak ada kursi yang tersedia untuk film '{nama_film}'.")
        return

    print(f"Kursi yang tersedia untuk film '{nama_film}':")
    print(", ".join(kursi_tersedia))
    print(f"Jumlah kursi tersedia: {len(kursi_tersedia)}")

    try:
        jumlah_tiket = int(input("Masukkan jumlah tiket yang ingin dipesan: "))
    except ValueError:
        print("Jumlah tiket harus berupa angka.")
        return

    if jumlah_tiket <= 0:
        print("Jumlah tiket harus lebih dari 0.")
        return

    if jumlah_tiket > len(kursi_tersedia):
        print(f"Maaf, hanya {len(kursi_tersedia)} kursi yang tersedia.")
        return

    kursi_dipesan = []
    for i in range(jumlah_tiket):
        while True:
            kursi_pilihan = input(f"Masukkan nomor kursi ke-{i+1} yang ingin dipesan (misal: 1): ")
            if kursi_pilihan in kursi_tersedia:
                kursi_dipesan.append(kursi_pilihan)
                kursi_tersedia.remove(kursi_pilihan)
                break
            else:
                print(f"Kursi {kursi_pilihan} tidak tersedia atau sudah dipesan. Silakan pilih kursi lain.")

    total_harga = harga_tiket * jumlah_tiket
    if emoney < total_harga:
        print("Saldo E-money anda tidak cukup untuk memesan tiket.")
        return

    emoney -= total_harga

    for i, row in enumerate(akun_reader):
        if row[0] == nama_user:
            akun_reader[i][3] = str(emoney)

    with open(file_data, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(akun_reader)

    with open(file_kursi, mode='r') as file:
        kursi_reader = list(csv.reader(file))

    for row in kursi_reader:
        if row[0].lower() == nama_film.lower() and row[1] in kursi_dipesan:
            row[2] = nama_user  

    with open(file_kursi, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(kursi_reader)

    now = datetime.datetime.now()
    waktu_transaksi = now.strftime("%Y-%m-%d %H:%M:%S")

    with open("transaksi.txt", "w") as f:
        print("==================== Tiket Bioskop =====================", file=f)
        print(f"Nama Pemesan           : {nama_user}", file=f)
        print(f"Metode Pembayaran      : E-money", file=f)
        print(f"Film                   : {nama_film}", file=f)
        print(f"Jumlah Tiket           : {jumlah_tiket}", file=f)
        print(f"Kursi                  : {', '.join(kursi_dipesan)}", file=f)
        print(f"Waktu Pemesanan        : {waktu_transaksi}", file=f)
        print(f"Total Harga Tiket      : Rp {total_harga}", file=f)
        print("==========================================================", file=f)
        print(f"Sisa saldo E-money     : Rp {emoney}", end="\n\n", file=f)

    print(f"Tiket untuk film '{nama_film}' sebanyak {jumlah_tiket} tiket telah berhasil dipesan. Kursi: {', '.join(kursi_dipesan)}")

    with open("transaksi.txt", "r") as f:
        print(f.read())


def lihat_saldo():
    nama = input("Masukkan nama user: ")
    with open(file_data, mode='r') as file:
        csv_reader = csv.reader(file)
        found = False
        for row in csv_reader:
            if row[0] == nama:
                print(f"Saldo Anda saat ini: Rp.{row[3]}")
                found = True
                break

    if not found:
        print("Nama pengguna atau password salah.")


def admin():
    while True:
        menu = PrettyTable()
        menu.field_names = ["No", "Opsi"]
        menu.add_row(["1", "Tambah Film"])
        menu.add_row(["2", "Lihat Daftar Film"])
        menu.add_row(["3", "Update film"])
        menu.add_row(["4" ,"Hapus film"])
        menu.add_row(["5", "Topup saldo"])
        menu.add_row(["6", "Logout"])
        print(menu)
        admin = input("Pilih opsi: ")

        if admin == "1":
            tambah_film()
        elif admin == "2":
            daftar_film()
        elif admin == "3":
            update_film()
        elif admin == "4":
            hapus_film()
        elif admin == "5":
            tambah_saldo()
        elif admin == "6":
            print("Logout Berhasil!")
            break
        else:
            print("Opsi tidak tersedia!")

def user():
    
    while True:
        menu = PrettyTable()
        menu.field_names = ["No", "Opsi"]
        menu.add_row(["1", "Lihat daftar film"])
        menu.add_row(["2", "Search film"])
        menu.add_row(["3", "Sorting film"])
        menu.add_row(["4", "Pesan tiket"])
        menu.add_row(["5", "Lihat Saldo"])
        menu.add_row(["6", "Logout"])
        print(menu)
        user = input("Pilih opsi: ")

        if user == "1":
            daftar_film()
        elif user == "2":
            search_film()
        elif user == "3":
            sort_film()
        elif user == "4":
            pesan_tiket()
        elif user == "5":
            lihat_saldo()
        elif user == "6":
            print("Logout berhasil")
            break
        else:
            print("Opsi tidak tersedia!")

def login():
    nama = input("Masukkan username: ")
    password = pwinput.pwinput(prompt="Masukkan password: ")
    try:
        with open(file_data, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == nama and row[1] == password:
                    print(f"Login berhasil, Selamat datang {nama}")
                    return row[2]
    except Exception as e:
        print(f"Terjadi error saat login {e}")
            
    print("Username atau password salah")
    return None

def main():
    while True:
        pilih = PrettyTable()
        pilih.field_names = ["No", "Pilihan"]
        pilih.add_row(["1", "Login"])
        pilih.add_row(["2", "Register"])
        pilih.add_row(["3", "Exit"])
        print(pilih)
        opsi = input("Silahkan pilih opsi: ")

        if opsi == "1":
            role = login()
            if role == "admin":
                admin()
            elif role == "user":
                user()
        elif opsi == "2":
            registrasi()
        elif opsi == "3":
            print("Terimakasih telah menggunakan program kami, Berkunjung lagi lain kali yaaaa!")
            break
        else:
            print("Opsi tidak valid")

if __name__ == "__main__":
    main()