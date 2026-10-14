from datetime import datetime

from models import Mahasiswa, Peralatan, TransaksiPeminjaman, LogActivity


class SistemLaboratorium:
    def __init__(self, daftar_kategori=None):
        self.__data_mahasiswa = {}
        self.__data_peralatan = {}
        self.__data_kategori = {}
        self.__data_transaksi = {}
        self.__logs = []

        if daftar_kategori:
            for k in daftar_kategori:
                self.__data_kategori[k.id_kategori] = k

    @property
    def data_mahasiswa(self):
        return self.__data_mahasiswa

    @property
    def data_kategori(self):
        return self.__data_kategori

    @property
    def data_peralatan(self):
        return self.__data_peralatan

    @property
    def data_transaksi(self):
        return self.__data_transaksi

    @property
    def logs(self):
        return self.__logs

    def tambah_mahasiswa(self, nim, nama, no_hp):
        if nim in self.__data_mahasiswa:
            print("[X]  NIM sudah terdaftar")
            return
        self.__data_mahasiswa[nim] = Mahasiswa(nim, nama, no_hp)
        self.catat_log(f"Tambah mahasiswa {nama} ({nim})")

    def hapus_mahasiswa(self, nim):
        if nim not in self.__data_mahasiswa:
            return False
        for trx in self.__data_transaksi.values():
            if trx.mahasiswa.nim == nim and trx.status_transaksi == "dipinjam":
                print("[X]  Mahasiswa masih punya peminjaman yang belum selesai")
                return False
        nama = self.__data_mahasiswa[nim].nama
        del self.__data_mahasiswa[nim]
        self.catat_log(f"Hapus mahasiswa {nama} ({nim})")
        return True

    def tambah_alat(self, kode, nama, id_kategori, stok):
        if id_kategori not in self.__data_kategori:
            print("[X]  Kategori tidak ditemukan")
            return
        if kode in self.__data_peralatan:
            print("[X]  Kode alat sudah ada")
            return
        kategori = self.__data_kategori[id_kategori]
        self.__data_peralatan[kode] = Peralatan(kode, nama, kategori, stok)
        self.catat_log(f"Tambah alat {nama} ({kode}) stok {stok}")

    def hapus_alat(self, kode):
        if kode not in self.__data_peralatan:
            return False
        for trx in self.__data_transaksi.values():
            if trx.status_transaksi == "dipinjam":
                for detail in trx.daftar_detail:
                    if detail.alat.kode_alat == kode:
                        print("[X]  Alat masih ada di peminjaman yang belum selesai")
                        return False
        nama = self.__data_peralatan[kode].nama_alat
        del self.__data_peralatan[kode]
        self.catat_log(f"Hapus alat {nama} ({kode})")
        return True

    def buat_transaksi(self, nim, list_alat_pinjam):
        mhs = self.__data_mahasiswa.get(nim)
        if mhs is None or not mhs.is_aktif():
            print("[X]  Mahasiswa tidak ditemukan atau tidak aktif")
            return None
        if len(list_alat_pinjam) == 0:
            print("[X]  Alat yang dipinjam masih kosong")
            return None

        for kode, jumlah in list_alat_pinjam.items():
            alat = self.__data_peralatan.get(kode)
            if alat is None or not alat.is_tersedia(jumlah):
                print(f"[X]  Alat {kode} tidak tersedia")
                return None

        id_trx = "TRX" + str(len(self.__data_transaksi) + 1).zfill(3)
        transaksi = TransaksiPeminjaman(id_trx, mhs)
        for kode, jumlah in list_alat_pinjam.items():
            transaksi.tambah_detail(self.__data_peralatan[kode], jumlah)

        self.__data_transaksi[id_trx] = transaksi
        self.catat_log(f"Transaksi {id_trx} dibuat oleh {mhs.nama}")
        return transaksi

    def proses_pengembalian(self, id_transaksi, kode_alat, jumlah, kondisi):
        transaksi = self.__data_transaksi.get(id_transaksi)
        if transaksi is None:
            return False

        for detail in transaksi.daftar_detail:
            if detail.alat.kode_alat == kode_alat:
                berhasil = detail.proses_pengembalian(jumlah, kondisi, datetime.now())
                if berhasil:
                    status = transaksi.update_status_transaksi()
                    self.catat_log(f"{id_transaksi}: {kode_alat} x{jumlah} kembali ({kondisi}), status {status}")
                return berhasil
        return False

    def cari_alat_fleksibel(self, keyword):
        keyword = keyword.lower()
        hasil = []
        for alat in self.__data_peralatan.values():
            if (keyword in alat.nama_alat.lower()
                    or keyword in alat.kode_alat.lower()
                    or keyword in alat.kategori.nama_kategori.lower()):
                hasil.append(alat)
        return hasil

    def catat_log(self, aktivitas):
        self.__logs.append(LogActivity(aktivitas))
