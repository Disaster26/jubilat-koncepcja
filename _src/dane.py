# -*- coding: utf-8 -*-
"""Dane strony Jubilat - jedno miejsce do edycji treści (w WordPressie: pola ACF / wpisy).

Źródła: jubilat.com.pl (stan 05.11.2026), materiały działu marketingu (28.10 i 05.11.2026),
umowa z 05.11.2026. Niczego nie dopisujemy od siebie - brakujące dane są w PYTANIA (build.py).
"""

# ---------------------------------------------------------------- ustawienia
CANONICAL_BASE = "https://jubilat.com.pl"      # docelowa domena (canonical, sitemap, JSON-LD)
PREVIEW = True                                  # True = wersja testowa: noindex + robots Disallow
TEST_NOTES = True                               # True = pokazuje dyskretne dopiski "wersja testowa"
# Stopka wykonawcy: ustaw na None, żeby usunąć link z całej strony.
WYKONANIE = {"tekst": "wykonanie: Wylinka", "url": "https://wylinka.pl"}

FIRMA = {
    "nazwa": "Handlowa Spółdzielnia JUBILAT",
    "ulica": "al. Zygmunta Krasińskiego 1",
    "kod": "31-111",
    "miasto": "Kraków",
    "tel": "12 422 80 40",
    "faks": "12 422 25 65",
    "email": "info@jubilat.com.pl",
    "krs": "0000168419",
    "nip": "675-000-32-30",
    "regon": "001096350",
    "social": [
        ("Facebook", "https://www.facebook.com/JubilatKrakow"),
        ("Instagram", "https://www.instagram.com/jubilat_domhandlowy/"),
        ("TikTok", "https://www.tiktok.com/@jubilatkrakow"),
        ("YouTube", "https://www.youtube.com/@Sie%C4%87HandlowaJUBILAT"),
    ],
}

KONTAKTY = [  # (dział, telefon, e-mail)
    ("Sekretariat spółdzielni", "12 422 80 40", "info@jubilat.com.pl"),
    ("Dom Handlowy Jubilat, informacja", "12 619 33 00", None),
    ("Salon Eleganza", "12 619 33 32", None),
    ("Sala konferencyjna", "12 619 33 98", "administracja@jubilat.com.pl"),
    ("Lokale, biura i magazyny", "12 619 34 19", "administracja@jubilat.com.pl"),
    ("Rekrutacja", "780 191 147", "rekrutacja@jubilat.com.pl"),
    ("Bony dla firm, marketing", None, "marketing@jubilat.com.pl"),
    ("Pomoc w sprawie aplikacji", "780 191 172", None),
]

ZARZAD = [  # z sekcji "Poznaj nas lepiej" na jubilat.com.pl
    ("Prezes Zarządu", "Aneta Agnieszka Kurbiel-Mucharska"),
    ("Wiceprezes Zarządu", "Leszek Piotr Klimczak"),
    ("Kierownik Działu Handlu i Marketingu", "Mariusz Kurbiel"),
    ("Kierownik Działu Administracyjno-Technicznego", "Michał Baran"),
    ("Główny Księgowy", "Anna Waluch"),
    ("Kierownik Działu Organizacji i Samorządu", "Barbara Brzukała"),
    ("Kierownik Działu Kadr i Rachuby Płac", "Agnieszka Januszewska"),
]

# ---------------------------------------------------------------- kalendarz
# Niedziele handlowe (ustawa z 10.01.2018 r. z późn. zm.): ostatnia niedziela stycznia, kwietnia,
# czerwca i sierpnia, niedziela przed Wielkanocą oraz trzy niedziele przed Bożym Narodzeniem.
NIEDZIELE_HANDLOWE = [
    "2026-01-25", "2026-03-29", "2026-04-26", "2026-06-28", "2026-08-30", "2026-12-06", "2026-12-13", "2026-12-20",
    "2027-01-31", "2027-03-21", "2027-04-25", "2027-06-27", "2027-08-29", "2027-12-05", "2027-12-12", "2027-12-19",
]
# Święta (dni ustawowo wolne od pracy) - sklepy nieczynne.
SWIETA = {
    "2026-01-01": "Nowy Rok", "2026-01-06": "Trzech Króli", "2026-04-05": "Wielkanoc", "2026-04-06": "Poniedziałek Wielkanocny",
    "2026-05-01": "Święto Pracy", "2026-05-03": "Święto Konstytucji 3 Maja", "2026-05-24": "Zielone Świątki", "2026-06-04": "Boże Ciało",
    "2026-08-15": "Wniebowzięcie NMP", "2026-11-01": "Wszystkich Świętych", "2026-11-11": "Narodowe Święto Niepodległości",
    "2026-12-24": "Wigilia", "2026-12-25": "Boże Narodzenie", "2026-12-26": "drugi dzień Bożego Narodzenia",
    "2027-01-01": "Nowy Rok", "2027-01-06": "Trzech Króli", "2027-03-28": "Wielkanoc", "2027-03-29": "Poniedziałek Wielkanocny",
    "2027-05-01": "Święto Pracy", "2027-05-03": "Święto Konstytucji 3 Maja", "2027-05-16": "Zielone Świątki", "2027-05-27": "Boże Ciało",
    "2027-08-15": "Wniebowzięcie NMP", "2027-11-01": "Wszystkich Świętych", "2027-11-11": "Narodowe Święto Niepodległości",
    "2027-12-24": "Wigilia", "2027-12-25": "Boże Narodzenie", "2027-12-26": "drugi dzień Bożego Narodzenia",
}
# Wielka Sobota - handel do 14:00 (ustawa).
SKROCONE = {"2026-04-04": "14:00", "2027-03-27": "14:00"}

# ---------------------------------------------------------------- placówki
# godz: pt = poniedziałek-piątek, sob = sobota, nh = niedziela handlowa; None = nieczynne
_SKLEP_OPIS = ("Świeże pieczywo, ciasta i drożdżówki, mięsa i wędliny, owoce i warzywa. Bogaty wybór nabiału, "
               "także od lokalnych i regionalnych producentów, unikatowe marki spożywcze i artykuły gospodarczo-przemysłowe.")
_SKLEP_USLUGI = ["Płatność kartą", "Bony Pluxee i bony Jubilat", "Wypłata gotówki przy kasie (cashback)",
                 "Opłaty rachunków", "Karta klienta i aplikacja Jubilat", "Pieczywo 10% taniej od 19:00"]

PLACOWKI = [
    {"id": "dh", "typ": "dh", "slug": "dom-handlowy", "nazwa": "Dom Handlowy Jubilat", "krotka": "Dom Handlowy",
     "adres": "al. Zygmunta Krasińskiego 1", "kod": "31-111", "dzielnica": "Zwierzyniec, przy moście Dębnickim",
     "lat": 50.055744, "lng": 19.927863, "tel": "12 619 33 00", "foto": "dh",
     "godz": {"pt": ["06:00", "22:00"], "sob": ["07:00", "22:00"], "nh": ["08:00", "20:00"]},
     "dzialy": [
         {"poz": "Parter", "nazwa": "Sklep spożywczy z delikatesami", "godz": {"pt": ["06:00", "22:00"], "sob": ["07:00", "22:00"], "nh": ["08:00", "20:00"]}},
         {"poz": "I piętro", "nazwa": "Stoisko HOME ze strefą Beauty", "godz": {"pt": ["09:00", "20:00"], "sob": ["09:00", "19:00"], "nh": ["10:00", "18:00"]}},
         {"poz": "II-III piętro", "nazwa": "Salon Eleganza", "godz": {"pt": ["09:00", "20:00"], "sob": ["09:00", "19:00"], "nh": ["10:00", "18:00"]}},
     ]},
    {"id": "lniana", "typ": "sklep", "slug": "lniana-2", "nazwa": "Sklep Jubilat, ul. Lniana 2", "krotka": "ul. Lniana 2",
     "adres": "ul. Lniana 2", "lat": 50.11285, "lng": 19.89859, "tel": "12 420 28 60", "foto": "s-lniana",
     "godz": {"pt": ["06:15", "20:00"], "sob": ["07:15", "17:15"], "nh": ["09:00", "17:00"]}},
    {"id": "makowskiego", "typ": "sklep", "slug": "makowskiego-18a", "nazwa": "Sklep Jubilat, ul. Makowskiego 18A", "krotka": "ul. Makowskiego 18A",
     "adres": "ul. Tadeusza Makowskiego 18A", "lat": 50.08811, "lng": 19.91413, "tel": "12 637 58 59", "foto": "s-makowskiego",
     "godz": {"pt": ["06:00", "20:00"], "sob": ["07:00", "16:00"], "nh": ["09:00", "17:00"]}},
    {"id": "mazowiecka", "typ": "sklep", "slug": "mazowiecka-88", "nazwa": "Sklep Jubilat, ul. Mazowiecka 88", "krotka": "ul. Mazowiecka 88",
     "adres": "ul. Mazowiecka 88", "lat": 50.07675, "lng": 19.92080, "tel": "12 633 37 07", "foto": "s-mazowiecka",
     "godz": {"pt": ["06:00", "21:00"], "sob": ["07:00", "19:00"], "nh": ["09:00", "17:00"]}},
    {"id": "rydla", "typ": "sklep", "slug": "rydla-7", "nazwa": "Sklep Jubilat, ul. Rydla 7", "krotka": "ul. Rydla 7",
     "adres": "ul. Lucjana Rydla 7", "lat": 50.07546, "lng": 19.90093, "tel": "12 637 21 56", "foto": "s-rydla",
     "godz": {"pt": ["06:00", "21:00"], "sob": ["07:00", "19:00"], "nh": ["09:00", "17:00"]}},
    {"id": "modrzewiowa", "typ": "sklep", "slug": "modrzewiowa-17", "nazwa": "Sklep Jubilat, al. Modrzewiowa 17", "krotka": "al. Modrzewiowa 17",
     "adres": "al. Modrzewiowa 17", "lat": 50.06527, "lng": 19.86631, "tel": "12 425 25 87", "foto": "s-modrzewiowa",
     "godz": {"pt": ["06:00", "21:30"], "sob": ["07:00", "19:00"], "nh": ["09:00", "17:00"]}},
    {"id": "nastawach", "typ": "sklep", "slug": "plac-na-stawach", "nazwa": "Sklep Jubilat, Plac Na Stawach", "krotka": "Plac Na Stawach",
     "adres": "Plac Na Stawach", "lat": 50.05473, "lng": 19.92111, "tel": "12 422 68 06", "foto": "s-nastawach",
     "godz": {"pt": ["06:00", "18:00"], "sob": ["07:00", "14:00"], "nh": None}},
    {"id": "orla", "typ": "sklep", "slug": "orla-62", "nazwa": "Sklep Jubilat, ul. Orla 62", "krotka": "ul. Orla 62",
     "adres": "ul. Orla 62", "lat": 50.04386, "lng": 19.82743, "tel": "12 429 71 80", "foto": "s-orla",
     "godz": {"pt": ["06:00", "20:00"], "sob": ["07:00", "19:00"], "nh": ["09:00", "17:00"]}},
    {"id": "przegorzalska", "typ": "sklep", "slug": "przegorzalska-2", "nazwa": "Sklep Jubilat, ul. Przegorzalska 2", "krotka": "ul. Przegorzalska 2",
     "adres": "ul. Przegorzalska 2", "lat": 50.04819, "lng": 19.87257, "tel": "12 429 73 24", "foto": "s-przegorzalska",
     "godz": {"pt": ["06:00", "20:00"], "sob": ["07:00", "19:00"], "nh": ["09:00", "17:00"]}},
    {"id": "zaczek", "typ": "bar", "slug": "bar-zaczek", "nazwa": "Bar mleczny Żaczek", "krotka": "Bar Żaczek",
     "adres": "ul. Czarnowiejska 75", "kod": "30-049", "lat": 50.067797, "lng": 19.917558, "tel": "12 633 96 76", "foto": "bar-zaczek",
     "godz": {"pt": ["08:00", "17:00"], "sob": None, "nh": None},
     "dowoz": [("Wolt", "https://wolt.com/pl/pol/krakow/restaurant/bar-mleczny-zaczek"),
               ("Bolt Food", "https://food.bolt.eu/en/211-krakow/p/203649-bar-mleczny-zaczek/"),
               ("Glovo", "https://glovoapp.com/pl/pl/krakow/stores/zaczek-bar-mleczny-kra")]},
    {"id": "flisak", "typ": "bar", "slug": "bar-flisak", "nazwa": "Bar mleczny Flisak", "krotka": "Bar Flisak",
     "adres": "ul. Tadeusza Kościuszki 1", "kod": "30-105", "lat": 50.055301, "lng": 19.926972, "tel": "12 422 21 05", "foto": "bar-flisak",
     "godz": {"pt": ["08:00", "18:00"], "sob": ["09:30", "14:30"], "nh": None},
     "dowoz": [("Wolt", "https://wolt.com/pl/pol/krakow/restaurant/bar-mleczny-flisak"),
               ("Bolt Food", "https://food.bolt.eu/en/211-krakow/p/203842-bar-mleczny-flisak/"),
               ("Glovo", "https://glovoapp.com/pl/pl/krakow/stores/flisak-bar-mleczny-kra")]},
]
for _p in PLACOWKI:
    if _p["typ"] == "sklep":
        _p["opis"] = _SKLEP_OPIS
        _p["uslugi"] = _SKLEP_USLUGI

# ---------------------------------------------------------------- menu barów (aktualizowane co tydzień)
# Źródło: grafiki "Menu tygodnia" z jubilat.com.pl (wgrane 11.2026). Zestaw = zupa + drugie danie.
MENU = {
    "od": "2026-11-02", "do": "2026-11-06",
    "zaczek": [
        ("Mała zupa grochowa", "Sznycel wieprzowy „górski”, ziemniaki, ogórek kiszony", "32,98"),
        ("Zupa ziemniaczana", "Pulpety drobiowe, ryż, marchewka z groszkiem", "31,72"),
        ("Mała zupa kalafiorowa z ryżem", "Gulasz z indyka, ziemniaki, surówka z marchewki", "35,70"),
        ("Mały rosół z makaronem", "Kotlet schabowy, ziemniaki, kapusta zasmażana", "34,24"),
        ("Barszcz ukraiński", "Pierogi leniwe", "26,29"),
    ],
    "flisak": [
        ("Zupa pieczarkowa", "Gołąbki z sosem pomidorowym", "26,30"),
        ("Zupa grochowa z makaronem", "Klopsy w sosie pieczarkowym, ziemniaki, buraczki", "27,55"),
        ("Zupa jarzynowa z zacierką", "Pałki pieczone z kurczaka, ziemniaki, surówka z marchewki", "29,45"),
        ("Zupa ogórkowa z ryżem", "Karczek z cebulką, ziemniaki, kapusta zasmażana", "29,85"),
        ("Barszcz zabielany z ziemniakami", "Kluski śląskie z sosem pieczarkowym", "19,75"),
    ],
}

# ---------------------------------------------------------------- gazetka
GAZETKA = {"plik": "gazetka-jubilat-21-10-2026.pdf", "zrodlo": "live_0511/gazetka_10.pdf",
           "od": "2026-10-21", "do": "2026-11-04", "strony": 20, "tytul": "Jesienne okazje",
           "miejsce": "Oferta Domu Handlowego Jubilat, al. Krasińskiego 1"}

# ---------------------------------------------------------------- okazje (publikacja z datą od-do)
# W wersji testowej: produkty i ceny z okazji w aplikacji 20-26.10.2026, daty ustawione przykładowo.
OKAZJE = [
    {"img": "o-banany", "nazwa": "Banany, Kostaryka/Panama", "cena": "6,27", "jedn": "zł/kg", "min30": "8,99 zł/kg", "od": "2026-11-03", "do": "2026-11-16"},
    {"img": "o-kiwi", "nazwa": "Kiwi, Grecja", "cena": "1,37", "jedn": "zł/szt.", "min30": "2,49 zł/szt.", "od": "2026-11-03", "do": "2026-11-16"},
    {"img": "o-cashmir", "nazwa": "Papier toaletowy rumiankowy Cashmir 3W, 8 rolek", "cena": "8,97", "jedn": "zł/szt.", "min30": "10,99 zł/szt.", "od": "2026-11-03", "do": "2026-11-16"},
    {"img": "o-ludwik", "nazwa": "Płyn do mycia naczyń Ludwik 450 g, wybrane rodzaje", "cena": "4,77", "jedn": "zł/szt.", "min30": "6,69 zł/szt.", "od": "2026-11-03", "do": "2026-11-16"},
    {"img": "o-hortex", "nazwa": "Sok jabłkowy Hortex 1 l", "cena": "4,57", "jedn": "zł/szt.", "min30": "8,19 zł/szt.", "od": "2026-11-03", "do": "2026-11-16"},
    # przykład zaplanowany na później - pojawi się sam 17.11
    {"img": "o-banany", "nazwa": "Banany, Kostaryka/Panama", "cena": "6,27", "jedn": "zł/kg", "min30": "8,99 zł/kg", "od": "2026-11-17", "do": "2026-11-23"},
]

# ---------------------------------------------------------------- komunikaty / banery z datą od-do
KOMUNIKATY = [
    {"od": "2026-11-05", "do": "2026-11-11", "tekst": "11 listopada (środa) Dom Handlowy i sklepy Jubilat są nieczynne. 10 listopada zapraszamy w zwykłych godzinach.", "link": None},
    {"od": "2026-11-23", "do": "2026-12-20", "tekst": "Niedziele handlowe: 6, 13 i 20 grudnia. Dom Handlowy otwarty 8:00-20:00, sklepy osiedlowe 9:00-17:00 (sklep przy Placu Na Stawach nieczynny).", "link": ("Godziny placówek", "sklepy/")},
    {"od": "2026-12-21", "do": "2026-12-26", "tekst": "24, 25 i 26 grudnia wszystkie sklepy są nieczynne.", "link": None},
]

# ---------------------------------------------------------------- produkty unikatowe (ceny z jubilat.com.pl)
PRODUKTY_STAN = "05.11.2026"
PRODUKTY = [
    ("jogurt", "Jogurt naturalny Nadbużański 9%", "Kuchnia Lubelska", "1 kg", "13,79"),
    ("kefir", "Kefir naturalny ze Skały", "OSM w Skale", "500 ml", "5,69"),
    ("smietanka", "Śmietanka kremowa 30% pasteryzowana", "OSM w Skale", "500 ml", "17,29"),
    ("twarog-klimek", "Twaróg półtłusty", "Klimek", "1 kg", "49,69"),
    ("twarog-lapy", "Twaróg półtłusty, klinek z Łap", "Spółdzielnia Mleczarska w Łapach", "1 kg", "30,59"),
    ("lazanki", "Łazanki ręcznie robione", "Kuchnia Brawaty", "300 g", "19,29"),
    ("pierogi", "Pierogi zbójnickie ręcznie robione", "Kuchnia Brawaty", "350 g", "21,89"),
    ("herbatka", "Herbatka owocowo-ziołowa Owocowy Raj", "Natura Wita", "100 g", "23,99"),
    ("grzaniec", "Grzaniec strażacki, herbatka owocowo-ziołowa", "Natura Wita", "100 g", "15,69"),
    ("lipa", "Lipa kwiatostan, susz ziołowy", "Natura Wita", "50 g", "14,29"),
    ("praliny", "Bombonierka Rum&Gin Club", "Edle Tropfen", "1 szt.", "21,99"),
    ("cotedor", "Czekolada biała z ciasteczkami Lotus", "Côte d'Or", "380 g", "29,99"),
    ("jarzebina", "Jarzębina do herbaty", "Bacówka", "200 g", "15,99"),
    ("syrop", "Syrop malinowy", "Polska Róża", "250 ml", "18,99"),
    ("syrop-mocy", "Syrop mocy Złote mleko", "A to dobre!", "250 ml", "17,99"),
    ("miod", "Miód lipowy nektarowy", "Łysoń", "1,25 kg", "84,99"),
    ("ciasteczka", "Bombonierka", "Ciasteczka z Krakowa", "250 g", "22,79"),
]

# ---------------------------------------------------------------- Salon Eleganza
LOOKBOOK = [  # (plik w img/eleganza/lb, opis)
    ("k54", "Bluzka we wzór i szerokie bordowe spodnie"),
    ("k2", "Płaszcz w kolorze camel i sukienka w kratę"),
    ("k13", "Kobaltowy komplet: żakiet z baskinką i ołówkowa spódnica"),
    ("k19", "Spodnie i kurtka ze skóry w kolorze śliwki"),
    ("k15", "Granatowy garnitur i mała czarna"),
    ("k10", "Sukienka w groszki i marynarka w jodełkę"),
    ("k7", "Płaszcz z futrzanym kołnierzem i męska marynarka ecru"),
    ("k23", "Puchowa kurtka ecru i dzianinowy komplet"),
    ("k21", "Spódnica we wzór, sweter i kurtka ecru"),
    ("k50", "Bluzka z kokardą, długi płaszcz i męski sweter"),
    ("k39", "Dzianinowy komplet ecru i męski sweter"),
    ("k29", "Kardigan w kolorze khaki i skórzane spodnie"),
    ("k26", "Jeans, koszula w kratę i pikowana kurtka"),
]
# (klucz, nazwa, szerokość optyczna w px, co oferuje - z jubilat.com.pl)
MARKI = [
    ("skorska", "Dom Mody Skórska", 134, "odzież damska, tylko u nas w Krakowie"),
    ("feria", "Feria", 101, "odzież damska"),
    ("red", "Red Button", 150, "odzież damska"),
    ("micha", "Micha", 104, "odzież damska"),
    ("rino", "Rino&Pelle", 172, "odzież damska"),
    ("infront", "In Front", 0, "odzież damska"),
    ("gap", "GAP", 0, "obuwie damskie i męskie"),
    ("lee", "Lee Cooper", 85, "jeansy, koszule, obuwie"),
    ("tamaris", "Tamaris", 142, "obuwie damskie"),
    ("gabol", "Gabol", 132, "torebki i walizki"),
    ("anekke", "Anekke", 128, "galanteria, obuwie, kubki"),
    ("gabriella", "Gabriella", 128, "rajstopy i pończochy"),
    ("mayoral", "Mayoral", 112, "odzież dziecięca"),
    ("ido", "iDO", 80, "odzież dziecięca"),
    ("nena", "Nena Bebe", 57, "skarpetki i rajstopy dziecięce"),
    ("oxyd", "OXYD Perfume", 51, "perfumy"),
]

# ---------------------------------------------------------------- aktualności (przeniesione z jubilat.com.pl)
AKTUALNOSCI = [
    {"slug": "nena-bebe", "stary": "nena-bebe", "data": "2026-10-13", "tytul": "Nena Bebe w Salonie Eleganza", "img": "nena", "kat": "Salon Eleganza",
     "tresc": ["Nena Bebe to polska marka oferująca stylowe skarpetki, podkolanówki, zakolanówki i rajstopy dla dzieci. Kolekcje wyróżniają się modnym wzornictwem, delikatnymi ażurami, falbankami, tiulem i eleganckimi detalami, dzięki czemu świetnie sprawdzają się zarówno w codziennych, jak i wizytowych stylizacjach dziecięcych.",
               "Produkty Nena Bebe łączą komfort noszenia z estetycznym wykonaniem i są dobrym wyborem dla rodziców szukających modnych oraz efektownych dodatków dla dzieci. To propozycje na co dzień, do przedszkola, szkoły, na uroczystości rodzinne, święta i wyjątkowe okazje.",
               "Zapraszamy do Salonu Eleganza na II piętrze Domu Handlowego Jubilat, al. Krasińskiego 1."]},
    {"slug": "perfumy-oxyd", "stary": "oxyd-perume-2", "data": "2026-08-14", "tytul": "Perfumy OXYD w Salonie Eleganza", "img": "oxyd", "kat": "Salon Eleganza",
     "tresc": ["OXYD Perfume to polska marka oferująca perfumy inspirowane popularnymi zapachami designerskimi i niszowymi. W kolekcjach OXYD znajdziesz propozycje damskie, męskie i unisex, dostępne w różnych pojemnościach i atrakcyjnych cenach.",
               "Marka stawia na wysoką koncentrację esencji zapachowych oraz szeroki wybór kompozycji - od świeżych i cytrusowych, przez kwiatowe, aż po intensywne, drzewne i orientalne.",
               "Perfumy OXYD są dostępne w Salonie Eleganza na III piętrze Domu Handlowego Jubilat. Zapraszamy do poznania kolekcji i wybrania zapachu dla siebie."]},
    {"slug": "ido-w-salonie-eleganza", "stary": "nowosc-w-salonie-eleganza-wloska-marka-ido-juz-dostepna", "data": "2026-08-14", "tytul": "Nowość w Salonie Eleganza: włoska marka iDO", "img": "ido", "kat": "Salon Eleganza",
     "tresc": ["Oferta Salonu Eleganza w Domu Handlowym Jubilat powiększyła się o nową markę - iDO, włoską markę odzieżową stworzoną z myślą o dzieciach i młodzieży.",
               "iDO łączy modny, nowoczesny design z wygodą i funkcjonalnością, tak ważnymi w codziennych stylizacjach najmłodszych. Kolekcje wyróżniają się starannym wykonaniem, ciekawymi fasonami i kolorystyką wpisującą się w aktualne trendy.",
               "W ofercie są propozycje dla dziewczynek i chłopców - na co dzień, do szkoły, na rodzinne wyjścia i wyjątkowe okazje. Zapraszamy do Salonu Eleganza w DH Jubilat."]},
    {"slug": "perfumy-pepe-jeans", "stary": "oxyd-perume", "data": "2026-08-13", "tytul": "Perfumy Pepe Jeans London na stoisku HOME", "img": None, "kat": "Stoisko HOME i Beauty",
     "tresc": ["Pepe Jeans London to marka o londyńskich korzeniach, która łączy modowy, miejski styl z nowoczesnym podejściem do zapachów. Jej perfumy wyróżniają się oryginalnymi kompozycjami oraz charakterystycznymi flakonami.",
               "W ofercie są zapachy damskie i męskie - od świeżych i energetycznych, po słodsze, bardziej zmysłowe i intensywne kompozycje.",
               "Perfumy Pepe Jeans London są dostępne na stoisku HOME ze strefą Beauty na I piętrze Domu Handlowego Jubilat."]},
    {"slug": "golden-rose", "stary": "kurczaki-z-rozna", "data": "2025-10-27", "tytul": "Golden Rose w strefie Beauty", "img": None, "kat": "Stoisko HOME i Beauty",
     "tresc": ["Golden Rose to nowa marka w strefie Beauty na stoisku HOME (I piętro, DH Jubilat, al. Krasińskiego 1). Piękne kolorystyki i dopracowane formuły kosmetyków w przystępnych cenach."]},
    {"slug": "dom-mody-skorska", "stary": "lorem-ipsum-4", "data": "2025-09-28", "tytul": "Dom Mody Skórska - tylko u nas w Krakowie", "img": "skorska", "kat": "Salon Eleganza",
     "tresc": ["Wyjątkowy asortyment polskiego producenta, w Krakowie dostępny tylko w Salonie Eleganza. Marka została założona w 2000 roku i oferuje odzież damską, w tym sukienki, żakiety i ramoneski.",
               "Wszystkie modele marki Dom Mody Skórska są projektowane, konstruowane i szyte w centrali firmy w Łodzi."]},
    {"slug": "rabat-dla-krakowskich-rodzin", "stary": "lorem-ipsum-3", "data": "2025-09-12", "tytul": "Wspieramy krakowskie rodziny: 3% rabatu", "img": None, "kat": "Dla klientów",
     "tresc": ["Posiadacze kart Krakowskie Rodziny z Niepełnosprawnym Dzieckiem, Krakowska Duża Rodzina oraz Rodzina 3+ otrzymują przy każdych zakupach w naszych sklepach 3% rabatu. Wystarczy okazać jedną z tych kart przy kasie.",
               "Rabat naliczany jest od kwoty zakupów min. 5 zł. Nie obejmuje alkoholu, wyrobów tytoniowych, prasy, doładowań telefonicznych oraz toreb na zakupy."]},
    {"slug": "la-le-krakowskie-kosmetyki", "stary": "lorem-ipsum-2", "data": "2025-09-12", "tytul": "La-Le, krakowska manufaktura kosmetyków", "img": None, "kat": "Stoisko HOME i Beauty",
     "tresc": ["La-Le to krakowska manufaktura kosmetyków tworzonych z szacunkiem do natury. Receptury opierają się na naturalnych ekstraktach roślinnych i olejkach eterycznych, które pielęgnują skórę delikatnie, a zarazem skutecznie.",
               "Prostota w użyciu, minimalizm w wyglądzie i autentyczność w każdym detalu. Kosmetyki La-Le znajdziesz na I piętrze w DH Jubilat."]},
    {"slug": "bony-towarowe-podarunkowe-pluxee", "stary": "lorem-ipsum", "data": "2025-09-12", "tytul": "Bony towarowe, podarunkowe i Pluxee", "img": None, "kat": "Dla klientów",
     "tresc": ["W sieci handlowej Jubilat za zakupy zapłacisz bonami towarowymi i podarunkowymi wydawanymi przez HS Jubilat oraz bonami i kartami Pluxee.",
               "Sprzedajemy także bony towarowe dla firm o nominałach 10, 20 i 50 zł, za które można kupić wszystkie towary dostępne w DH Jubilat i 8 sklepach sieci. Zamówienia przyjmujemy mailowo: marketing@jubilat.com.pl. Płatność przelewem potwierdzonym przez bank; ponieważ ta forma usługi nie jest objęta podatkiem VAT, podstawą rozliczenia jest nota księgowa wystawiona w dniu odbioru bonów.",
               "Bony podarunkowe o nominale 50 zł można zrealizować tylko na stoiskach przemysłowych Domu Handlowego Jubilat (I, II i III piętro). Kupisz je na stoiskach na I i II piętrze DH Jubilat w godzinach otwarcia Domu Handlowego."]},
]

# ---------------------------------------------------------------- praca
PRACA_LINK = "https://system.erecruiter.pl/FormTemplates/RecruitmentForm.aspx?WebID=a64696e07d6d4a519818511da1ca7836"
PRACA = [
    {"slug": "zastepca-kierownika-sklepu", "tytul": "Zastępca kierownika sklepu (K/M)", "od": "2026-10-01", "do": None,
     "zadania": ["Planowanie, organizowanie i nadzorowanie pracy zespołu", "Obsługa klienta przy kasie fiskalnej i na sali sprzedaży",
                 "Odpowiedzialność za dostępność towaru, jego ekspozycję i prawidłowe funkcjonowanie sklepu"],
     "wymagania": ["Doświadczenie w koordynowaniu pracy zespołu", "Komunikatywność, samodzielność i proaktywne podejście do zadań", "Nastawienie na realizację celów sprzedażowych"],
     "oferta": ["Stabilne zatrudnienie na podstawie umowy o pracę", "Wynagrodzenie z systemem motywacyjnym w postaci premii",
                "Praca w firmie o ugruntowanej pozycji na rynku", "Wdrożenie pod okiem opiekuna: krok po kroku, jak zarządzać sklepem i osiągać cele"]},
    {"slug": "kierownik-sklepu", "tytul": "Kierownik / Kierowniczka sklepu", "od": "2026-04-01", "do": None,
     "zadania": ["Zarządzanie zespołem", "Organizacja pracy sklepu", "Współpraca z kontrahentami", "Zamawianie towaru", "Odpowiedzialność za asortyment"],
     "wymagania": [],
     "oferta": ["Umowa o pracę, pełny etat", "Szkolenia podnoszące kwalifikacje zawodowe", "Świadczenia socjalne", "Przyjazna atmosfera"]},
    {"slug": "kasjer-sprzedawca", "tytul": "Kasjer-sprzedawca (K/M), praca zmianowa", "od": "2026-04-01", "do": None,
     "zadania": ["Sprawna, uprzejma obsługa klientów", "Obsługa stoiska mięsno-wędliniarskiego", "Dbałość o ekspozycję produktów",
                 "Obsługa kasy fiskalnej i porządek w miejscu pracy"],
     "wymagania": ["Aktualne badania do celów sanitarno-epidemiologicznych", "Zaangażowanie w wykonywaną pracę", "Kultura osobista", "Rzetelność i uczciwość"],
     "oferta": ["Umowa o pracę i wynagrodzenie zawsze na czas", "Praca w firmie o ugruntowanej pozycji na rynku", "Stabilność zatrudnienia",
                "Elastyczny czas pracy", "Nieoprocentowane pożyczki zakładowe", "Ubezpieczenie na życie", "Możliwość przystąpienia do prywatnej opieki medycznej"]},
]

# ---------------------------------------------------------------- historia
HISTORIA = [
    ("1908", "Na krakowskim rynku działa spółdzielczość spożywców „Społem”, z której wywodzi się Jubilat."),
    ("1958", "Na 50-lecie spółdzielni rodzi się pomysł nowoczesnego centrum handlowego dla Krakowa."),
    ("1959", "Pierwsza koncepcja architektoniczna z kawiarnią na dachu i widokiem na Wisłę. Wstępny projekt przygotował Henryk Jerzy Marconi."),
    ("1969", "W lipcu otwarcie Domu Handlowego „Jubilat” według projektu zespołu pod kierunkiem Jadwigi Sanickiej. Budowa na podmokłym gruncie przy Wiśle trwała blisko dekadę."),
    ("1991", "Spółdzielnia przyjmuje nazwę Handlowa Spółdzielnia Jubilat."),
    ("2014", "Modernizacja stolarki: szyby o delikatnie niebieskim odcieniu zastępują pierwotne, brązowe."),
]
