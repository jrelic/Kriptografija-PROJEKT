import hashlib
import random

class Banka(object):
    def __init__(self, kljucevi):
        print("Inicijalizacija banke")
        self.kljucevi = kljucevi

    def hash_izracun(self, polje_int):
        int_string = str(polje_int[0]) + str(polje_int[1]) + str(polje_int[2])
        byte_string = bytes(int_string, encoding='utf-8')
        hash_vrijednost = hashlib.sha256(byte_string).hexdigest()
        int_vrijednost = int(hash_vrijednost, 16) % self.kljucevi['n']

        return int_vrijednost

    def verifikacijski_izracun(self):
        iznosi = []
        for nn in self.odslijepiti_novcane_naloge:
            otkrij_informacije = self.otkrij_informacije[nn]
            odslijepi_nn = self.odslijepi_novcane_naloge[nn]

            iznosi.append(odslijepi_nn['iznos'])

            for kljuc in otkrij_informacije.keys():
                identifikacijski_string = odslijepi_nn[kljuc]['identifikacijski_string']

                lijevi = otkrij_informacije[kljuc][0]
                desni = otkrij_informacije[kljuc][1]

                izracunato_lijevo = [self.hash_izracun(lijevi), lijevi[1]]
                izracunato_desno = [self.hash_izracun(desni), desni[1]]
                izracunati_identifikacijski_string = [izracunato_lijevo, izracunato_desno]

                if not izracunati_identifikacijski_string == identifikacijski_string:
                    print("Novcani nalog: %s, Kljuc: %s" % (nn, kljuc))
                    print("Izracunato: %s, Dato: %s" % (str(izracunati_identifikacijski_string),
                                                   str(identifikacijski_string)))
                    return False
        iznosi = set(iznosi)
        if len(iznosi) > 1:
            print("Iznosi se ne podudaraju")
            return False
        return True


    def dohvati_slijepe_novcane_naloge(self, novcaninalozi):
        print("Banka je primila slijepe novčane naloge")
        self.slijepi_novcani_nalozi = novcaninalozi


    def dohvati_otkrivajuce_informacije(self, otkrij_informacije):
        print("Banka je primila informacije o novčanim nalozima")
        self.otkrij_informacije = otkrij_informacije


    def dohvati_odslijepljene_novcane_naloge(self, novcaninalozi):
        print("Banka je primila odslijepljene novcane naloge")
        self.odslijepi_novcane_naloge = novcaninalozi

    def potpisi_novcani_nalog(self):
        if not self.verifikacijski_izracun():
            print('Odslijepljeni novčani nalozi ne mogu biti verificirani')

        potpis_banke = []
        d = self.kljucevi['d']
        n = self.kljucevi['n']
        slijepi_nn = self.potpisati_novcani_nalog

        potpis_banke.append(slijepi_nn['iznos'] ** d % n)
        potpis_banke.append(slijepi_nn['jedinstvenost'] ** d % n)
        id_kljucevi = ['I1', 'I2', 'I3']
        for kljuc in id_kljucevi:
            for i in slijepi_nn[kljuc]['identifikacijski_string']:
                potpis_banke.append(i[0] ** d %n)
                potpis_banke.append(i[1] ** d % n)
        print("Verificirano: Banka potpisuje")

        self.potpis_banke = potpis_banke

    def odslijepi_zahtjeve(self):
        print("Banka zahtijeva odslijepljenje")

        nasumicni_donji_broj = 0
        nasumicni_gornji_broj = len(self.slijepi_novcani_nalozi.keys()) - 1

        potpisati_nn_index = random.randint(nasumicni_donji_broj, nasumicni_gornji_broj)

        lista_kljuceva = list(self.slijepi_novcani_nalozi.keys())
        potpisati_nn_kljuc = lista_kljuceva[potpisati_nn_index]

        self.potpisati_novcani_nalog_kljuc = potpisati_nn_kljuc
        self.potpisati_novcani_nalog = self.slijepi_novcani_nalozi[potpisati_nn_kljuc]

        odslijepiti_nn = list(self.slijepi_novcani_nalozi.keys())
        odslijepiti_nn.pop(odslijepiti_nn.index(potpisati_nn_kljuc))
        self.odslijepiti_novcane_naloge = odslijepiti_nn


    def verifikacija_odslijepljenog(self, novcaninalog):
        pass
