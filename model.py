import baza
import sqlite3
from pomozne_funkcije import Seznam
from geslo import sifriraj_geslo, preveri_geslo

conn = sqlite3.connect('igre.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

uporabnik, podjetje, igra, platforma, distributira, podpira = baza.pripravi_tabele(conn)


class LoginError(Exception):
    """
    Napaka ob napačnem uporabniškem imenu ali geslu.
    """
    pass


class Uporabnik:
    """
    Razred za uporabnika.
    """

    def __init__(self, ime, *, id=None):
        """
        Konstruktor uporabnika.
        """
        self.id = id
        self.ime = ime

    def __str__(self):
        """
        Znakovna predstavitev uporabnika.
        Vrne uporabniško ime.
        """
        return self.ime


    @staticmethod
    def prijava(ime, geslo):
        """
        Preveri, ali sta uporabniško ime geslo pravilna.
        """
        sql = """
            SELECT id, zgostitev, sol FROM uporabnik
            WHERE ime = ?
        """
        try:
            id, zgostitev, sol = conn.execute(sql, [ime]).fetchone()
            if preveri_geslo(geslo, zgostitev, sol):
                return Uporabnik(ime, id=id)
        except TypeError:
            pass
        raise LoginError(ime)

    def dodaj_v_bazo(self, geslo):
        """
        V bazo doda uporabnika s podanim geslom.
        """
        assert self.id is None
        zgostitev, sol = sifriraj_geslo(geslo)
        with conn:
            self.id = uporabnik.dodaj_vrstico(ime=self.ime, zgostitev=zgostitev, sol=sol)


class Igre:
    """
    Razred za igre.
    """

    def __init__(self, ime_igre, datum_izdaje, cena, st_prodanih, razvijalec, cas_igranja
        , meadina_igranja, ocena, *ostalo):
        """
        Konstruktor igre.
        """
        self.ime_igre = ime_igre
        self.datum_izdaje = datum_izdaje
        self.cena = cena
        self.st_prodanih = st_prodanih
        self.razvijalec = razvijalec
        self.cas_igranja = cas_igranja
        self.meadina_igranja = meadina_igranja
        self.ocena = ocena
        self.ostalo = ostalo

    @staticmethod
    def najnovejse_igre():
        """
        Vrne najboljših 10 filmov v danem letu.
        """
        sql = """
            SELECT ime_igre, datum_izdaje, cena, vsebuje, razvija, povprecno_igranje, mediana, ocena
            FROM igra
            ORDER BY datum_izdaje DESC
            LIMIT 10
        """
        for ime_igre, datum_izdaje, *ostalo in conn.execute(sql):
            yield Igre(ime_igre, datum_izdaje, *ostalo)

    @staticmethod
    def podatki_o_igri(igra):
        """
        Vrne vse podatke o igri.
        """
        sql = """
            SELECT igra.ime_igre, datum_izdaje, cena, vsebuje, razvija, povprecno_igranje, mediana, ocena,
             distributira.podjetje, podpira.platforma
            FROM igra LEFT JOIN podpira ON (igra.ime_igre = podpira.ime_igre)
                      LEFT JOIN distributira ON (igra.ime_igre = distributira.ime_igre)
            WHERE igra.ime_igre == ?
        """
        for ime_igre, datum_izdaje, cena, st_prodanih, razvijalec, cas_igranja, meadina_igranja, ocena, distibuter, platforma in conn.execute(sql, [igra]):
            yield Igre(ime_igre, datum_izdaje, cena, st_prodanih, razvijalec, cas_igranja, meadina_igranja, ocena, distibuter, platforma)

    @staticmethod
    def poisci(niz):
        """
        Vrne vse igre, ki v imenu vsebujejo dani niz.
        """
        sql = """
            SELECT ime_igre, datum_izdaje, cena, vsebuje, razvija, povprecno_igranje, mediana, ocena
            FROM igra
            WHERE ime_igre LIKE ?
        """
        for ime_igre, *ostalo in conn.execute(sql, ['%' + niz + '%']):
            yield Igre(ime_igre, *ostalo)

    @staticmethod
    def glej_vse_igre():
        """
        Vrne vse podatke o igri.
        """
        sql = """
                SELECT ime_igre, datum_izdaje, cena, vsebuje, razvija, povprecno_igranje, mediana, ocena
                FROM igra
            """
        for ime_igre, datum_izdaje, cena, ocena, *ostalo  in conn.execute(sql):
            yield Igre(ime_igre, datum_izdaje, cena, ocena, *ostalo)

    # def dodaj_v_bazo(self, reziserji, igralci):
    #     """
    #     V bazo doda film s podanimi režiserji in igralci
    #     """
    #     assert self.id is None
    #     with conn:
    #         id = film.dodaj_vrstico(naslov=self.naslov, leto=self.leto, ocena=self.ocena)
    #         for mesto, oseba in enumerate(reziserji, 1):
    #             vloga.dodaj_vrstico(film=id, oseba=oseba.id, tip=TipVloge.R.name, mesto=mesto)
    #         for mesto, oseba in enumerate(igralci, 1):
    #             vloga.dodaj_vrstico(film=id, oseba=oseba.id, tip=TipVloge.I.name, mesto=mesto)
    #         self.id = id1


# class Oseba:
#     """
#     Razred za osebo.
#     """

#     def __init__(self, ime, *, id=None):
#         """
#         Konstruktor osebe.
#         """
#         self.id = id
#         self.ime = ime

#     def __str__(self):
#         """
#         Znakovna predstavitev osebe.
#         Vrne ime osebe.
#         """
#         return self.ime

#     def poisci_vloge(self):
#         """
#         Vrne vloge osebe.
#         """
#         sql = """
#             SELECT film.naslov, film.leto, vloga.tip
#             FROM film
#                 JOIN vloga ON film.id = vloga.film
#             WHERE vloga.oseba = ?
#             ORDER BY leto
#         """
#         for naslov, leto, tip_vloge in conn.execute(sql, [self.id]):
#             yield (naslov, leto, TipVloge[tip_vloge])

#     @staticmethod
#     def poisci(niz):
#         """
#         Vrne vse osebe, ki v imenu vsebujejo dani niz.
#         """
#         sql = "SELECT id, ime FROM oseba WHERE ime LIKE ?"
#         for id, ime in conn.execute(sql, ['%' + niz + '%']):
#             yield Oseba(ime=ime, id=id)

#     def dodaj_v_bazo(self):
#         """
#         Doda osebo v bazo.
#         """
#         assert self.id is None
#         with conn:
#             self.id = oseba.dodaj_vrstico(ime=self.ime)


# class TipVloge(Seznam):
#     """
#     Oznake za tip vloge.
#     """
#     I = 'igralec'
#     R = 'režiser'