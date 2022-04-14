import hashlib
import random
import gmpy2

class Klijent(object):
    def __init__(self, iznos, identitet, kljucevi):
        print("Inicijalizacija klijenta")
        self.iznos = iznos
        self.identitet = identitet
        self.kljucevi = kljucevi
        self.novcani_nalozi = {}


        for i in range(1, 4):
            ime_novcanog_naloga = "novcani nalog" + str(i)
            self.novcani_nalozi[ime_novcanog_naloga] = self.kreiranje_novcanog_naloga(ime_novcanog_naloga)


    def obvezivanje_bitovima(self, identifikacijski_integer):

        nasumicni_broj1 = self.generator_slucajnog_broja()
        nasumicni_broj2 = self.generator_slucajnog_broja()


        int_string = str(identifikacijski_integer) + str(nasumicni_broj1) + str(nasumicni_broj2)
        byte_string = bytes(int_string, encoding='utf-8')
        hash_vrijednost = hashlib.sha256(byte_string).hexdigest()
        int_vrijednost = int(hash_vrijednost, 16) % self.kljucevi['n']

        return [int_vrijednost, nasumicni_broj1, nasumicni_broj2]


    def ProcesZasljepljivanjaNovcanogNaloga(self):
        print("Zasljepljivanje novcanih naloga")
        self.slijepi_novcani_nalozi = {}
        n = self.kljucevi['n']
        for novcani_nalog in self.novcani_nalozi.keys():
            slijepi_novcani_nalog = {}
            originalni_novcani_nalog = self.novcani_nalozi[novcani_nalog]
            zasljepljujuci_faktor = originalni_novcani_nalog['k'] ** self.kljucevi['e'] % n

            slijepi_novcani_nalog['naziv'] = originalni_novcani_nalog['naziv']
            slijepi_novcani_nalog['iznos'] = (originalni_novcani_nalog['iznos'] * zasljepljujuci_faktor % n)
            slijepi_novcani_nalog['jedinstvenost'] = (originalni_novcani_nalog['jedinstvenost'] * zasljepljujuci_faktor % n)

            for kljuc in originalni_novcani_nalog.keys():
                if not kljuc.startswith('I'):
                    continue
                slijepi_novcani_nalog[kljuc] = {}
                slijepi_novcani_nalog[kljuc]['identifikacijski_string'] = []
                for i in originalni_novcani_nalog[kljuc]['identifikacijski_string']:
                    slijepi_hash = (i[0] * zasljepljujuci_faktor % n)
                    slijepi_nasumicni = (i[1] * zasljepljujuci_faktor % n)
                    slijepi_novcani_nalog[kljuc]['identifikacijski_string'].append([slijepi_hash, slijepi_nasumicni])

            self.slijepi_novcani_nalozi[novcani_nalog] = slijepi_novcani_nalog


    def kreiranje_stringa_identiteta(self):

        n, t = self.razdijeljivanje_tajne()
        lijevi_hash, n1, n2 = self.obvezivanje_bitovima(identifikacijski_integer=n)
        desni_hash, t1, t2 = self.obvezivanje_bitovima(identifikacijski_integer=t)
        id_string = [[lijevi_hash, n1], [desni_hash, t1]]
        razotkrivajuce_polje = [[n, n1, n2], [t, t1, t2]]

        return {'identifikacijski_string':id_string, 'razotkrivajuce_polje':razotkrivajuce_polje}


    def kreiranje_novcanog_naloga(self, naziv):

        print("Kreiranje novcanog naloga %s" % naziv)
        print("Pokretanje obvezivanja bitovima")
        novcani_nalog = {}
        novcani_nalog['naziv'] = naziv
        novcani_nalog['iznos'] = self.iznos
        novcani_nalog['jedinstvenost'] = self.generator_slucajnog_broja()
        novcani_nalog['k'] = self.generator_slucajnog_broja()
        novcani_nalog['I1'] = self.kreiranje_stringa_identiteta()
        print("Kreiranje stringa identiteta I1")
        novcani_nalog['I2'] = self.kreiranje_stringa_identiteta()
        print("Kreiranje stringa identiteta I2")
        novcani_nalog['I3'] = self.kreiranje_stringa_identiteta()
        print("Kreiranje stringa identiteta I3")

        return novcani_nalog


    def ispisi_novcani_nalog(self, novcani_nalozi, vrsta_novcanog_naloga):

        print("Ispisivanje novcanog naloga...")
        for novcani_nalog in novcani_nalozi.keys():
            polje_stringova = []
            ime_datoteke = '%s_%s.txt' % (vrsta_novcanog_naloga,novcani_nalog)
            ispisi_novcani_nalog = novcani_nalozi[novcani_nalog]
            naziv_str = "Naziv: %s" % ispisi_novcani_nalog['naziv']

            polje_stringova.append(naziv_str)
            elektronicki_iznos = "Iznos: %d" % ispisi_novcani_nalog['iznos']

            polje_stringova.append(elektronicki_iznos)
            elektronicka_jedinstvenost = "Jedinstvenost: %d" % ispisi_novcani_nalog['jedinstvenost']

            polje_stringova.append(elektronicka_jedinstvenost)
            I1_identifikacijski_string = "I1 identifikacijski string: %s" % str(ispisi_novcani_nalog['I1']['identifikacijski_string'])

            polje_stringova.append(I1_identifikacijski_string)
            I2_identifikacijski_string = "I2 identifikacijski string: %s" % str(ispisi_novcani_nalog['I2']['identifikacijski_string'])

            polje_stringova.append(I2_identifikacijski_string)
            I3_identifikacijski_string = "I3 identifikacijski string: %s" % str(ispisi_novcani_nalog['I3']['identifikacijski_string'])

            polje_stringova.append(I3_identifikacijski_string)

            if 'potpis' in ispisi_novcani_nalog:
                potpis_string = "potpis: %s" % str(ispisi_novcani_nalog['potpis'])
                polje_stringova.append(potpis_string)
            with open(ime_datoteke, 'w') as f:
                for i in polje_stringova:
                    f.write(i + '\n')



    def generator_slucajnog_broja(self):
        '''Generira slucajni broj i vraca ga'''
        nasumicna_donja_vrijednost = 100
        nasumicna_gornja_vrijednost = 10000
        return random.randint(nasumicna_donja_vrijednost, nasumicna_gornja_vrijednost) % self.kljucevi['n']


    def primanje_potpisa(self, novcaninalog, potpis):
        print("Primljen potpisani novčani nalog")
        potpisani_nn = {}

        potpisani_nn[novcaninalog] = dict(self.slijepi_novcani_nalozi[novcaninalog])
        potpisani_nn[novcaninalog]['potpis'] = potpis
        self.potpisani_novcani_nalog = potpisani_nn


    def razotkrivanje(self, novcaninalozi):

        print("Razotkrivanje odabranih novčaih naloga")
        razotkriveni_brojevi = {}
        for nn in novcaninalozi:
            originalni_nn = self.novcani_nalozi[nn]
            razotkriveni_brojevi[nn] = {}
            for kljuc in originalni_nn.keys():
                if kljuc.startswith('I'):
                    razotkriveni_brojevi[nn][kljuc] = originalni_nn[kljuc]['razotkrivajuce_polje']

        return razotkriveni_brojevi


    def razdijeljivanje_tajne(self):

        n = self.generator_slucajnog_broja()
        t = n ^ self.identitet

        return n,t


    def odslijepljivanje(self, novcaninalozi):

        print("Odslijepljivanje novčanih naloga")
        self.odslijepljeni_novcani_nalozi = {}
        n = self.kljucevi['n']

        for nn in novcaninalozi:
            originalni_nn = self.novcani_nalozi[nn]
            slijepi_nn = self.slijepi_novcani_nalozi[nn]

            inv_k = int(gmpy2.invert(originalni_nn['k'], n))
            faktor_odslijepljivanja = (inv_k ** self.kljucevi['e']) % n

            odslijepi_nn = {}

            odslijepi_nn['naziv'] = originalni_nn['naziv']
            odslijepi_nn['iznos'] = (slijepi_nn['iznos'] * faktor_odslijepljivanja % n)
            odslijepi_nn['jedinstvenost'] = (slijepi_nn['jedinstvenost'] * faktor_odslijepljivanja % n)

            for kljuc in slijepi_nn.keys():
                if not kljuc.startswith('I'):
                    continue
                odslijepi_nn[kljuc] = {'identifikacijski_string': []}
                for i in slijepi_nn[kljuc]['identifikacijski_string']:
                    odslijepi_hash = (i[0] * faktor_odslijepljivanja % n)
                    odslijepi_nasumicne = (i[1] * faktor_odslijepljivanja % n)
                    odslijepi_nn[kljuc]['identifikacijski_string'].append([odslijepi_hash,
                                                         odslijepi_nasumicne])

            self.odslijepljeni_novcani_nalozi[nn] = odslijepi_nn


    def odslijepi_potpisani_novcani_nalog(self):
        print("Odslijepljivanje novčanih naloga")
        self.odslijepljeni_potpisani_novcani_nalog = {}
        n = self.kljucevi['n']

        for nn in self.potpisani_novcani_nalog.keys():
            originalni_nn = self.novcani_nalozi[nn]
            slijepi_nn = self.potpisani_novcani_nalog[nn]

            inv_k = int(gmpy2.invert(originalni_nn['k'], n))
            faktor_odslijepljivanja = (inv_k ** self.kljucevi['e']) % n

            odslijepljeni_nn = {}

            odslijepljeni_nn['naziv'] = originalni_nn['naziv']
            odslijepljeni_nn['iznos'] = (slijepi_nn['iznos'] * faktor_odslijepljivanja % n)
            odslijepljeni_nn['jedinstvenost'] = (slijepi_nn['jedinstvenost'] * faktor_odslijepljivanja % n)

            for kljuc in slijepi_nn.keys():
                if kljuc == 'potpis':
                    odslijepljeni_potpis = []
                    for i in slijepi_nn[kljuc]:
                        odslijepi_i = i * faktor_odslijepljivanja % n
                        odslijepljeni_potpis.append(odslijepi_i)
                    odslijepljeni_nn[kljuc] = odslijepljeni_potpis
                if kljuc.startswith('I'):
                    odslijepljeni_nn[kljuc] = {'identifikacijski_string': []}
                    for i in odslijepljeni_nn[kljuc]['identifikacijski_string']:
                        odslijepljeni_hash = (i[0] * faktor_odslijepljivanja % n)
                        odslijepljeni_nasumicni = (i[1] * faktor_odslijepljivanja % n)
                        odslijepljeni_nn[kljuc]['identifikacijski_string'].append([odslijepljeni_hash,
                                                             odslijepljeni_nasumicni])

            self.odslijepljeni_potpisani_novcani_nalog[nn] = odslijepljeni_nn

