# PA-PEMESANAN-TIKET-BIOSKOP
KELOMPOK 1

```  Fauzia Inanta Aurelia      2409116044  ```

```  Ghifari Al Azhar           2409116059  ```

```  Daffa Syahrandy Husain     2409116069  ```

1.  Mengimport modul library yang akan digunakan dalam program ini
``` ruby
import csv  # CSV digunakan untuk menyimpan data 
from prettytable import PrettyTable  # prettytable digunakan untuk menampilkan sebuah daftar dalam bentuk tabel agar terlihat lebih rapi
import pwinput  # pwinput digunakan untuk mengsensor ketika kita menginput sebuah password
import datetime  # datetime digunakan untuk menampilkan kapan waktu dilakukannya pemesanan
```

2.  Mendefinisikan file csv yang digunakan sebagai penyimpanan
``` ruby
file_film = "data_film.csv"  # Digunakan untuk menyimpan data film yang ada
file_kursi = "data_kursi.csv"  # Digunakan untuk menyimpan data kursi ketika menambahkan film dan pemesan kursi
file_data = "data_akun.csv"  # Digunakan untuk menyimpan data akun
```

3.  Membuat function registrasi untuk user yang belum mempunyai akun
``` ruby
def registrasi():
    nama = input("Masukkan nama: ")
    password = pwinput.pwinput("Masukkan password anda: ")
    role = 'user'  # untuk memastikan role ketika user registrasi adalah sebagai user
    saldo = 0 
    found = False  # digunakan untuk melakukan pengecekan nama user, apakah sudah dipakai atau belum
    with open(file_data, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == nama:
                found = True  # Jika nama sudah tersedia maka tidak dapat melakukan registrasi
                print(f"Nama {nama} sudah tersedia, Silahkan login atau gunakan nama yang lain!")
                return

    if not found:
        with open(file_data, mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([nama, password, role, saldo])
        print(f"Halo {nama}, Sudah berhasil registrasi, Silahkan login yaaa!!!!")
```

4.  Membuat function untuk menambahkan film, fitur ini digunakan khusus admin
``` ruby
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
        with open(file_film, mode='r') as file:    # Melakukan pengecekan untuk nama film
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == nama_film:
                    found = True
                    print(f"Film {nama_film} sudah ada!")
                    return

        if not found:
            with open(file_film, mode='a', newline='') as file:    # Jika nama film tidak ada dalam penyimpanan maka akan menambahkan film ke penyimpanan
                csv_writer = csv.writer(file)
                csv_writer.writerow([nama_film, rating_film, harga_tiket])
            print(f"Film {nama_film} berhasil ditambahkan.")

        with open(file_kursi, mode='a', newline='') as file:    # Menambahkan kursi dari film yang ditambahkan
            csv_writer = csv.writer(file)
            for kursi in range(1, kursi_tersedia + 1):
                csv_writer.writerow([nama_film, f"{kursi}", "tersedia"])
            print(f"Kursi untuk film {nama_film} berhasil ditambahkan")
    except Exception as e:
        print(f"Terjadi error pada  {e}")
```

5.  Membuat function untuk menampilkan daftar film yang tersedia dengan menampilkan film yang ada di penyimpanan
``` ruby
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
```

6.  Membuat function untuk mengupdate sebuah film yang ada didalam penyimpanan
``` ruby
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

    with open(file_film, mode='r') as file:    # Melakukan pengecekan film didalam penyimpanan
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
```

7.  Membuat function untuk menghapus film yang ingin dihapus dari penyimpanan
``` ruby
def hapus_film():
    daftar_film()    # Menampilkan daftar film yang ada di penyimpanan
    nama_film = input("Nama film yang ingin dihapus: ")
    updated_rows = []
    found = False
    with open(file_film, mode='r') as file:    # Melakukan pengecekan data film
        csv_reader = list(csv.reader(file))
        for row in csv_reader:
            if row[0] == nama_film:
                found = True    # Jika film ada dalam penyimpanan
                print(f"Film {nama_film} berhasil dihapus")
            else:
                updated_rows.append(row)

    if not found:    # Jika film tidak ada dalam penyimpanan
        print(f"Film tidak ada dalam data")
        return

    with open(file_film, mode='w', newline='') as file:    # Menghapus film
        csv_writer = csv.writer(file)
        csv_writer.writerows(updated_rows)

    updated_kursi_rows = []
    with open(file_kursi, mode='r') as file:
        kursi_reader = csv.reader(file)
        for row in kursi_reader:
            if row[0].lower() != nama_film.lower():
                updated_kursi_rows.append(row)

    with open(file_kursi, mode='w', newline='') as file:    # Menghapus kursi dari film yang dihapus juga
        csv_writer = csv.writer(file)
        csv_writer.writerows(updated_kursi_rows)

    print(f"Kursi untuk film {nama_film} berhasil dihapus.")
```

8.  Membuat function untuk menambahkan saldo user yang ingin dipilih
``` ruby
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

    with open(file_data, mode='r') as file:    # Melakukan pengecekan data user di penyimpanan
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == nama and row[1] == password:
                saldo_lama = int(row[3])
                saldo_total = saldo_lama + saldo_baru
                updated_rows.append([nama, password, 'user', saldo_total])
                found = True    # Jika data tersedia maka akan menambahkan saldo
                print(f"Saldo {nama} berhasil ditambahkan. Saldo sekarang: Rp.{saldo_total}")
            else:
                updated_rows.append(row)

    if not found:    # Jika data tida ditemukan maka akan kembali ke menu awal
        print(f"User {nama} tidak ditemukan")
        return

    with open(file_data, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(updated_rows)
```

9.  Membuat function untuk mencari sebuah film
``` ruby
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
```

10.  Membuat function untuk mensorting film dengan ascending dan descending
``` ruby
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
        films.sort(key=lambda x: x[0].lower(), reverse=True)  # Mengurutkan dengan terbalik dari huruf Z sampai A
    elif pilih == '2':
        films.sort(key=lambda x: x[0].lower())  # Mengurutkan film dari huruf A sampai Z
    else:
        print("Pilihan tidak valid.")
        return

    result_table = PrettyTable()
    result_table.field_names = ["Nama", "Rating", "Harga"]

    for row in films:
        result_table.add_row(row)

    print("Hasil pengurutan film:")
    print(result_table)
```

11.  Membuat function untuk memesan tiket dan kursi sebuah film
``` ruby
def pesan_tiket():
    daftar_film()
    nama_film = input("Masukkan nama film yang ingin dipesan: ")  # Memilih nama film yang ingin dipesan
    nama_user = input("Masukkan nama pengguna: ")  # Digunakan untuk mengganti ketersediaan kursi dengan nama pemesan

    with open(file_film, mode='r') as file:  # Melakukan pengecekan film, apakah film tersedia tau tidak didalam penyimpanan
        film_reader = list(csv.reader(file))
        film_data = None
        for row in film_reader:
            if row[0].lower() == nama_film.lower():
                film_data = row
                break

    if not film_data:  # Jika film tidak ada didalam penyimpanan
        print(f"Film '{nama_film}' tidak ditemukan.")
        return

    try:
        harga_tiket = int(film_data[2])
    except ValueError:
        print("Harga tiket tidak valid.")
        return

    with open(file_data, mode='r') as file:  # Melakukan pengecekan apakah data user ada didalam penyimpanan
        akun_reader = list(csv.reader(file))
        user_data = None
        for row in akun_reader:
            if row[0] == nama_user:
                user_data = row
                break

    if not user_data:  # Jika nama user tidak ditemukan didalam penyimpanan
        print("Akun tidak ditemukan.")
        return

    saldo_user = int(user_data[3]) 
    emoney = saldo_user 
    if emoney < harga_tiket:
        print("Saldo E-money tidak cukup untuk memesan tiket.")
        return

    with open(file_kursi, mode='r') as file:  # Melakukan pengecekan ketersediaan kursi untuk sebuah film
        kursi_reader = list(csv.reader(file))
        kursi_tersedia = []
        for row in kursi_reader:
            if row[0].lower() == nama_film.lower() and row[2] == "tersedia":
                kursi_tersedia.append(row[1])  

    if not kursi_tersedia:  # Jika kursi tidak tersedia
        print(f"Tidak ada kursi yang tersedia untuk film '{nama_film}'.")
        return

    print(f"Kursi yang tersedia untuk film '{nama_film}':")
    print(", ".join(kursi_tersedia))
    print(f"Jumlah kursi tersedia: {len(kursi_tersedia)}")

    try:
        jumlah_tiket = int(input("Masukkan jumlah tiket yang ingin dipesan: "))  # Menginput jumlah tiket yang ingin dipesan
    except ValueError:
        print("Jumlah tiket harus berupa angka.")
        return

    if jumlah_tiket <= 0:  # Memastikan jika jumlah memesan tiket tidak boleh kurang dari atau 0
        print("Jumlah tiket harus lebih dari 0.")
        return

    if jumlah_tiket > len(kursi_tersedia):  # Menampilkan kursi yang tersedia
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

    total_harga = harga_tiket * jumlah_tiket  Menghitung harga tiket sesuai dengan yang dipesan
    if emoney < total_harga:
        print("Saldo E-money anda tidak cukup untuk memesan tiket.")
        return

    emoney -= total_harga  # Mengurangi jumlah saldo

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
    waktu_transaksi = now.strftime("%Y-%m-%d %H:%M:%S")  # Digunakan untuk menampilkan waktu pemesanan

    with open("transaksi.txt", "w") as f:  # Membuat invoice untuk pemesanan tiket bioskop
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

```

12.  Membuat function untuk menampilkan saldo
``` ruby
def lihat_saldo():
    nama = input("Masukkan nama user: ")  # Menginput nama user
    with open(file_data, mode='r') as file:  # Melakukan pengecekan apakah data user ada di dalam penyimpanan
        csv_reader = csv.reader(file)
        found = False
        for row in csv_reader:
            if row[0] == nama:
                print(f"Saldo Anda saat ini: Rp.{row[3]}")
                found = True
                break

    if not found:  # Jika data user tidak ada dalam penyimpanan
        print("Nama pengguna atau password salah.")
```

13.  Membuat function admin untuk menampilkan fitur fitur yang dapat digunakan oleh admin
``` ruby
def admin():
    while True:  # Penggunaan while True untuk melakukan perulangan
        menu = PrettyTable()  # Menampilkan fitur fitur admin dalam bentuk tabel
        menu.field_names = ["No", "Opsi"]
        menu.add_row(["1", "Tambah Film"])
        menu.add_row(["2", "Lihat Daftar Film"])
        menu.add_row(["3", "Update film"])
        menu.add_row(["4" ,"Hapus film"])
        menu.add_row(["5", "Topup saldo"])
        menu.add_row(["6", "Logout"])
        print(menu)
        admin = input("Pilih opsi: ")

        if admin == "1":  # Jika admin memilih 1 maka admin akan memproses untuk menambahkan sebuah film
            tambah_film()  # Memanggil function tambah_film untuk menambahkan film
        elif admin == "2":  # Jika admin memilih 2 makan admin dapat melihat daftar film
            daftar_film()  # Memanggil function daftar_film untuk menampilkan film yang tersedia
        elif admin == "3":  # Jika admin memilih 3 maka admin akan mengupdate sebuah film
            update_film()  # Memanggil function update_film untuk mengupdate film
        elif admin == "4":  # Jika admin memilih 4 maka admin akan menghapus sebuah film
            hapus_film()  # Memanggil function hapus_film untuk menghapus film
        elif admin == "5":  # Jika admin memilih 5 maka admin akan mengisi saldo user
            tambah_saldo()  # Memanggil function tambah_saldo untuk mengisi saldo user
        elif admin == "6":  # Jika admin memilih 6 maka akan keluar dari menu admin
            print("Logout Berhasil!")
            break  # Menghentikan perulangan
        else:  # Jika opsi yang dipilih selain yang dijelaskan
            print("Opsi tidak tersedia!")
```

14.  Membuat function user untuk menampilkan fitur fitur user yang bisa digunakan user
``` ruby
def user():
    while True:
        menu = PrettyTable()  # Menampilkan menu user dalam bentuk tabel
        menu.field_names = ["No", "Opsi"]
        menu.add_row(["1", "Lihat daftar film"])
        menu.add_row(["2", "Search film"])
        menu.add_row(["3", "Sorting film"])
        menu.add_row(["4", "Pesan tiket"])
        menu.add_row(["5", "Lihat Saldo"])
        menu.add_row(["6", "Logout"])
        print(menu)
        user = input("Pilih opsi: ")

        if user == "1":  # Jika user memilih 1 maka akan menampilkan daftar film
            daftar_film()  # Memanggil function daftar_film untuk menampilkan daftar film
        elif user == "2":  # Jika user memilih 2 maka user akan mencari film yang ingin dicari
            search_film()  # Memanggil function search_film untuk mencari film
        elif user == "3":  # Jika user memilih 3 maka akan mensorting film
            sort_film()  # Memanggil function sort_film untuk mensorting film
        elif user == "4":  # Jika user memilih 4 maka akan memesan tiket
            pesan_tiket()  # Memanggil function pesan_tiket untuk memesan tiket
        elif user == "5":  # Jika user memilih 5 maka akan menampilkan saldo user
            lihat_saldo()  # Memanggil function lihat_saldo untuk menampilkan saldo
        elif user == "6":  # Jika user memilih 6 maka akan keluar dari menu user
            print("Logout berhasil")
            break  # Berhenti dari perulangan
        else:
            print("Opsi tidak tersedia!")
```

15.  Membuat function login untuk melakukan login
``` ruby
def login():
    nama = input("Masukkan username: ")
    password = pwinput.pwinput(prompt="Masukkan password: ")
    try:
        with open(file_data, mode='r') as file:  # Melakukan pengecekan ketersediaan data akun di penyimpanan
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == nama and row[1] == password:
                    print(f"Login berhasil, Selamat datang {nama}")
                    return row[2]
    except Exception as e:
        print(f"Terjadi error saat login {e}")
            
    print("Username atau password salah")  # Jika data akun tidak valid/salah
    return None
```

16.  Membuat function main untuk menampilkan menu utama dan untuk memulai program
``` ruby
def main():
    while True:  # Melakukan pengulangan 
        pilih = PrettyTable()  # Menampilkan menu utama dalam bentuk tabel
        pilih.field_names = ["No", "Pilihan"]
        pilih.add_row(["1", "Login"])
        pilih.add_row(["2", "Register"])
        pilih.add_row(["3", "Exit"])
        print(pilih)
        opsi = input("Silahkan pilih opsi: ")

        if opsi == "1":  # Jika memilih 1 maka akan menampilkan menu login
            role = login()  # Pengecekan role ketika login
            if role == "admin":  # Jika role adalah admin maka akan menampilkan menu admin
                admin()  # Memanggil function admin
            elif role == "user":  # Jika role adalah user maka akan menampilkan menu user
                user()  # Memanggil function user
        elif opsi == "2":  #  Jika memilih 2 maka akan menampilkan menu registrasi
            registrasi()  # Memanggil function registrasi
        elif opsi == "3":  # Jika memilih 3 maka akan keluar dari program
            print("Terimakasih telah menggunakan program kami, Berkunjung lagi lain kali yaaaa!")
            break  # Berhenti dari program 
        else:  # Jika memilih selain pilihan diatas maka melakukan pengulangan
            print("Opsi tidak valid")
```

17.  Memanggil function main untuk memulai program
``` ruby
if __name__ == "__main__":
    main()
```
