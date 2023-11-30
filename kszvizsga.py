from abc import ABC, abstractmethod
from datetime import datetime


class Foglalas:
    def __init__(self, szobaszam, foglalas_datum):
        self.szobaszam = szobaszam
        self.foglalas_datum = foglalas_datum

    def __str__(self):
        return f"Szobaszám: {self.szobaszam}, Foglalás dátuma: {self.foglalas_datum.strftime('%Y.%m.%d')}"

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar
        self.foglalasok = []

    def szabad_e(self, foglalas_datum):
        for foglalas in self.foglalasok:
            if foglalas.foglalas_datum == foglalas_datum:
                return False
        return True

    def foglalas_lemond(self, foglalas_datum):
        foglalas_torles = [foglalas for foglalas in self.foglalasok if foglalas.foglalas_datum == foglalas_datum]
        if not foglalas_torles:
            return f"Nincs foglalás ezen a dátumon a szobához."

        # Csak az első találatot töröljük
        self.foglalasok.remove(foglalas_torles[0])
        return f"Foglalás törölve a szobából {foglalas_datum.strftime('%Y.%m.%d')} dátumon."

    def foglal(self, foglalas_datum):
        if foglalas_datum < datetime.now():
            return f"Hibás dátum. A foglalás dátuma nem lehet múltbeli."
        if not self.szabad_e(foglalas_datum):
            return f"A {self.szobaszam} szoba már foglalt ezen a napon."

        self.foglalasok.append(Foglalas(self.szobaszam, foglalas_datum))
        return f"A {self.szobaszam} szoba foglalva lett {foglalas_datum.strftime('%Y.%m.%d')}."

    def foglalas_datumok(self):
        foglalasok_str_list = []
        for foglalas in self.foglalasok:
            foglalas_datum_str = foglalas.foglalas_datum.strftime('%Y.%m.%d')
            foglalasok_str_list.append(f"{foglalas_datum_str}")
        return ", ".join(foglalasok_str_list)

    @abstractmethod
    def __str__(self):
        pass


class EgyagyasSzoba(Szoba):
    def __str__(self):
        foglalasok_str = self.foglalas_datumok()
        return f"Egyágyas szoba. A szoba száma: {self.szobaszam}, Ár: {self.ar}, Foglalások: {foglalasok_str if foglalasok_str else 'Nincsenek foglalások'}"


class KetagyasSzoba(Szoba):
    def __str__(self):
        foglalasok_str = self.foglalas_datumok()
        return f"Kétágyas szoba. A szoba száma: {self.szobaszam}, Ár: {self.ar}, Foglalások: {foglalasok_str if foglalasok_str else 'Nincsenek foglalások'}"


class Szalloda:
    def __init__(self):
        self.szobak = []

    def szoba_hozzaadas(self, szoba: Szoba):
        self.szobak.append(szoba)

    def adatfeltoltes(self):
        self.szoba_hozzaadas(EgyagyasSzoba(101, 4000))
        self.szoba_hozzaadas(EgyagyasSzoba(102, 4500))
        self.szoba_hozzaadas(KetagyasSzoba(201, 7000))
        self.szoba_hozzaadas(KetagyasSzoba(202, 7500))

    def foglalasok_lekerdezes(self):
        return '\n'.join(str(szoba) for szoba in self.szobak)

    def foglalas(self, szobaszam, foglalas_datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                return szoba.foglal(foglalas_datum)
        return "Szoba nem található."


def foglalasi_folyamat(szalloda: Szalloda):
    szalloda.adatfeltoltes()

    while True:
        print("Üdvözöljük a Szálloda foglalási rendszerében!")
        valasztas = input("Mit szeretne tenni? (1: foglalasok, 2: foglal, 3: lemond, 4: kilep): ")
        if valasztas == "1":
            print(szalloda.foglalasok_lekerdezes())
        elif valasztas == "2":
            szobaszam = int(input("Adja meg a szobaszámot: "))
            foglalas_datum_str = input("Adja meg a foglalás dátumát (éééé.hh.nn): ")
            foglalas_datum = datetime.strptime(foglalas_datum_str, '%Y.%m.%d')
            print(szalloda.foglalas(szobaszam, foglalas_datum))
        elif valasztas == "3":
            szobaszam = int(input("Adja meg a szobaszámot: "))
            lemond_datum_str = input("Adja meg a lemondás dátumát (yyyy.mm.dd): ")
            lemond_datum = datetime.strptime(lemond_datum_str, '%Y.%m.%d')
            print(szalloda.foglalas_lemond(szobaszam, lemond_datum))
        elif valasztas == "4":
            print("Viszlát!")
            break
        else:
            print("Érvénytelen választás.")


szalloda = Szalloda()
foglalasi_folyamat(szalloda)