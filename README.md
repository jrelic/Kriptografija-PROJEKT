# Kriptografija-PROJEKT
Pokretanje projekta:
  1. pip install gmpy2
  2. python transakcija.py


KAKO RADI?
- Klijent generira tri novčana naloga
- Različiti nasumični jedinstveni string brojevi su primijenjeni na svaki novčani nalog
- Razdijeljivanje tajne (eng. Secret splitting) i obvezivanje bitovima (eng. Bit commitment) su protokoli implementirani na identifikacijski string koji opisuje klijenta, te je slijepi potpis protokol koji je implementiran na sva tri novčana naloga
- Banka nasumično odabire jedan od tri novčana naloga poslana od strane klijenta da ostane neotvoren
- Te na kraju algoritam potvrđuje da su dva novčana naloga ispunjena sa validnim informacijama 
- Programski kod je razdvojen u tri datoteke klijent.py, banka.py i transakcija.py

