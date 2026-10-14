class Mahasiswa:
    def __init__(self, nim, nama, no_hp):
        self.__nim = nim
        self.__nama = nama
        self.__no_hp = no_hp
        self.__status_aktif = True

    @property
    def nim(self):
        return self.__nim

    @property
    def nama(self):
        return self.__nama

    @property
    def no_hp(self):
        return self.__no_hp

    def is_aktif(self):
        return self.__status_aktif

    def set_status_aktif(self, status):
        self.__status_aktif = status
