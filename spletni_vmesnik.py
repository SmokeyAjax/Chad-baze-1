import bottle
from sqlite3 import IntegrityError
from model import LoginError,  Igre, Podjetje, Platforma

# Glavna Stran
@bottle.get('/')
def glavna_stran():
    return bottle.template(
        'html/glavna_stran.html',
        najnovejse_igre = Igre.najnovejse_igre()
    )

# Prikaz igre
@bottle.get('/<igra>/')
def igra(igra):
    return bottle.template(
        'html/igra.html',
        igra = igra,
        podatki_o_igri = Igre.podatki_o_igri(igra)
    )

# Prikaz Podjetja
@bottle.get('/podjetje/<podjetje>/')
def podjetje(podjetje):
    return bottle.template(
        'html/podjetje.html',
        podjetje = podjetje,
        podatki_o_podjetju = Podjetje.podatki_o_podjetju(podjetje)
    )

# Prikaz Platforme
@bottle.get('/platforme/<platforma>/')
def platforma(platforma):
    return bottle.template(
        'html/platforma.html',
        platforma = platforma,
        podatki_o_platformi = Platforma.podatki_o_platformi(platforma)
    )

# Iskanje stran
@bottle.get('/isci/')
def iskanje():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    igre = Igre.poisci(iskalni_niz)
    return bottle.template(
        'html/iskanje.html',
        iskalni_niz = iskalni_niz,
        igre = igre
    )

# Glej vse igre stran, + vse verjante
@bottle.get('/glej_vse_igre/')
def glej_vse_igre():
    return bottle.template(
        'html/glej_vse_igre.html',
        glej_vse_igre=Igre.glej_vse_igre()
    )

@bottle.get('/glej_vse_igre/po_imenih/')
def glej_vse_igre_imena():
    return bottle.template(
        'html/glej_vse_igre_po_imenih.html',
        glej_vse_igre_imena=Igre.glej_vse_igre_imena()
    )

@bottle.get('/glej_vse_igre/po_datumu/')
def glej_vse_igre_datum():
    return bottle.template(
        'html/glej_vse_igre_po_datumu.html',
        glej_vse_igre_datum=Igre.glej_vse_igre_datum()
    )

@bottle.get('/glej_vse_igre/po_ceni/')
def glej_vse_igre_cena():
    return bottle.template(
        'html/glej_vse_igre_po_ceni.html',
        glej_vse_igre_cena=Igre.glej_vse_igre_cena()
    )

@bottle.get('/glej_vse_igre/po_oceni/')
def glej_vse_igre_ocena():
    return bottle.template(
        'html/glej_vse_igre_po_oceni.html',
        glej_vse_igre_ocena=Igre.glej_vse_igre_ocena()
    )

# Dodajanje igre
@bottle.get('/dodaj_igro/')
def dodaj_igro():
    return bottle.template(
        'html/dodaj_igro.html',
        napaka = None, ime_igre = "",
        datum_izdaje = "", cena = "",
        vsebuje = "", razvija = "",
        povprecno_igranje = "",mediana = "",
        ocena = "", podjetje= "", platforma= ""
    )

@bottle.post('/dodaj_igro/')
def dodaj_igro_post():
    ime_igre = bottle.request.forms.getunicode('ime_igre')
    datum_izdaje = bottle.request.forms.getunicode('datum_izdaje')
    cena = bottle.request.forms.getunicode('cena')
    vsebuje = bottle.request.forms.getunicode('vsebuje')
    razvija = bottle.request.forms.getunicode('razvija')
    povprecno_igranje = bottle.request.forms.getunicode('povprecno_igranje')
    mediana = bottle.request.forms.getunicode('mediana')
    ocena = bottle.request.forms.getunicode('ocena')

    podjetje = bottle.request.forms.getunicode('podjetje')
    platforma = bottle.request.forms.getunicode('platforma')

    if len(ime_igre) == 0 :
        return bottle.template(
            'html/dodaj_igro.html',
            napaka='Ime Igre ne sme bit prazen!',
            ime_igre = ime_igre,
            datum_izdaje=datum_izdaje, cena=cena,
            vsebuje=vsebuje, razvija=razvija,
            povprecno_igranje=povprecno_igranje, meadina_igranja=mediana,
            ocena=ocena, podjetje=podjetje, platforma=platforma
        )
    else:
        igra = Igre(ime_igre, datum_izdaje, cena, vsebuje, razvija, povprecno_igranje, mediana, ocena, podjetje, platforma)
        igra.dodaj_v_bazo()
        bottle.redirect('/')

# Dodajanje Podjetja
@bottle.get('/dodaj_podjetje/')
def dodaj_podjetje():
    return bottle.template(
        'html/dodaj_podjetje.html',
        ime = "", drzava = "", datum_ustanovitve = "", opis=""
    )

@bottle.post('/dodaj_podjetje/')
def dodaj_podjetje_post():
    ime = bottle.request.forms.getunicode('ime')
    drzava = bottle.request.forms.getunicode('drzava')
    datum_ustanovitve = bottle.request.forms.getunicode('datum_ustanovitve')
    opis = bottle.request.forms.getunicode('opis')
    podjetje = Podjetje(ime, drzava, datum_ustanovitve, opis)
    podjetje.dodaj_v_bazo()
    bottle.redirect('/')

bottle.run(debug=True, reloader=True)