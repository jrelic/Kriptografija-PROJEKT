import klijent
import banka

klijent_kljucevi = {'e': 324, 'n': 3853}
banka_kljucevi = {'d': 534, 'n': 3853}
iznos = 560
klijent_id = 253183

klijent_podaci = klijent.Klijent(iznos=iznos, identitet=klijent_id, kljucevi=klijent_kljucevi)
banka_podaci = banka.Banka(kljucevi=banka_kljucevi)

klijent_podaci.ProcesZasljepljivanjaNovcanogNaloga()
banka_podaci.dohvati_slijepe_novcane_naloge(klijent_podaci.slijepi_novcani_nalozi)
banka_podaci.odslijepi_zahtjeve()
klijent_podaci.odslijepljivanje(banka_podaci.odslijepiti_novcane_naloge)
banka_podaci.dohvati_odslijepljene_novcane_naloge(klijent_podaci.odslijepljeni_novcani_nalozi)
banka_podaci.dohvati_otkrivajuce_informacije(klijent_podaci.razotkrivanje(banka_podaci.odslijepiti_novcane_naloge))
banka_podaci.potpisi_novcani_nalog()
klijent_podaci.primanje_potpisa(banka_podaci.potpisati_novcani_nalog_kljuc, banka_podaci.potpis_banke)
klijent_podaci.odslijepi_potpisani_novcani_nalog()
klijent_podaci.ispisi_novcani_nalog(klijent_podaci.slijepi_novcani_nalozi, 'slijepi')
klijent_podaci.ispisi_novcani_nalog(klijent_podaci.odslijepljeni_novcani_nalozi, 'odslijepljeni')
klijent_podaci.ispisi_novcani_nalog(klijent_podaci.potpisani_novcani_nalog, 'potpisani')
klijent_podaci.ispisi_novcani_nalog(klijent_podaci.odslijepljeni_potpisani_novcani_nalog, 'odslijepljeni potpisani')
