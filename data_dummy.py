from models import Kategori

def buat_kategori():
    return [
        Kategori("K01", "Perangkat Jaringan"),
        Kategori("K02", "IoT dan Mikrokontroler"),
        Kategori("K03", "Komputer dan Aksesori"),
        Kategori("K04", "Multimedia dan Audio Visual"),
    ]


def isi_peralatan(lab):
    # K01: Perangkat Jaringan
    lab.tambah_alat("A001", "Router MikroTik", "K01", 10)
    lab.tambah_alat("A002", "Switch Managed 24-Port", "K01", 5)

    # K02: IoT dan Mikrokontroler
    lab.tambah_alat("A003", "ESP32 NodeMCU", "K02", 15)
    lab.tambah_alat("A004", "Arduino Uno Rev3", "K02", 20)

    # K03: Komputer dan Aksesori
    lab.tambah_alat("A005", "PC Server Workstation", "K03", 4)
    lab.tambah_alat("A006", "Webcam HD 1080p", "K03", 8)

    # K04: Multimedia dan Audio Visual
    lab.tambah_alat("A007", "Proyektor HDMI", "K04", 3)
    lab.tambah_alat("A008", "VR Headset", "K04", 2)