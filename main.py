from controllers import SistemLaboratorium
from data_dummy import buat_kategori, isi_peralatan
from views import jalankan_menu


if __name__ == "__main__":
    lab = SistemLaboratorium(buat_kategori())
    isi_peralatan(lab)
    jalankan_menu(lab)
