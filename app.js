(function () {
  'use strict';

  /* ---------- dane z jubilat.com.pl (stan 23.10.2026) ---------- */
  // godziny: [od, do] w formacie 'HH:MM'; nh = niedziela handlowa; null = nieczynne
  var PL = [
    { id: 'dh', typ: 'sklep', dh: true, nazwa: 'Dom Handlowy Jubilat', rodzaj: 'Dom handlowy', adres: 'Al. Krasińskiego 1', kod: '31-111 Kraków',
      lat: 50.055744, lng: 19.927863, tel: '12 619 33 00', foto: 'img/dh-m.jpg',
      godz: { pt: ['06:00', '22:00'], sob: ['07:00', '22:00'], nh: ['08:00', '20:00'] },
      dzialy: [
        { n: 'HOME ze strefą Beauty (I p.)', godz: { pt: ['09:00', '20:00'], sob: ['09:00', '19:00'], nh: ['10:00', '18:00'] } },
        { n: 'Salon Eleganza (II i III p.)', godz: { pt: ['09:00', '20:00'], sob: ['09:00', '19:00'], nh: ['10:00', '18:00'] } }
      ],
      uslugi: 'Opłacisz rachunki, zapłacisz kartą i bonami Pluxee, wypłacisz gotówkę (cashback), kupisz pieczywo i ciasta.' },
    { id: 'lniana', typ: 'sklep', nazwa: 'ul. Lniana 2', rodzaj: 'Sklep spożywczo-przemysłowy', adres: 'ul. Lniana 2', lat: 50.11285, lng: 19.89859, tel: '12 420 28 60', foto: 'img/s-lniana.jpg',
      godz: { pt: ['06:15', '20:00'], sob: ['07:15', '17:15'], nh: ['09:00', '17:00'] } },
    { id: 'makowskiego', typ: 'sklep', nazwa: 'ul. Makowskiego 18A', rodzaj: 'Sklep spożywczo-przemysłowy', adres: 'ul. T. Makowskiego 18A', lat: 50.08811, lng: 19.91413, tel: '12 637 58 59', foto: 'img/s-makowskiego.jpg',
      godz: { pt: ['06:00', '20:00'], sob: ['07:00', '16:00'], nh: ['09:00', '17:00'] } },
    { id: 'mazowiecka', typ: 'sklep', nazwa: 'ul. Mazowiecka 88', rodzaj: 'Sklep spożywczo-przemysłowy', adres: 'ul. Mazowiecka 88', lat: 50.07675, lng: 19.92080, tel: '12 633 37 07', foto: 'img/s-mazowiecka.jpg',
      godz: { pt: ['06:00', '21:00'], sob: ['07:00', '19:00'], nh: ['09:00', '17:00'] } },
    { id: 'rydla', typ: 'sklep', nazwa: 'ul. Rydla 7', rodzaj: 'Sklep spożywczo-przemysłowy', adres: 'ul. Lucjana Rydla 7', lat: 50.07546, lng: 19.90093, tel: '12 637 21 56', foto: 'img/s-rydla.jpg',
      godz: { pt: ['06:00', '21:00'], sob: ['07:00', '19:00'], nh: ['09:00', '17:00'] } },
    { id: 'modrzewiowa', typ: 'sklep', nazwa: 'al. Modrzewiowa 17', rodzaj: 'Sklep spożywczo-przemysłowy', adres: 'al. Modrzewiowa 17', lat: 50.06527, lng: 19.86631, tel: '12 425 25 87', foto: 'img/s-modrzewiowa.jpg',
      godz: { pt: ['06:00', '21:30'], sob: ['07:00', '19:00'], nh: ['09:00', '17:00'] } },
    { id: 'nastawach', typ: 'sklep', nazwa: 'Plac Na Stawach', rodzaj: 'Sklep spożywczo-przemysłowy', adres: 'Plac Na Stawach', lat: 50.05473, lng: 19.92111, tel: '12 422 68 06', foto: 'img/s-nastawach.jpg',
      godz: { pt: ['06:00', '18:00'], sob: ['07:00', '14:00'], nh: null } },
    { id: 'orla', typ: 'sklep', nazwa: 'ul. Orla 62', rodzaj: 'Sklep spożywczo-przemysłowy', adres: 'ul. Orla 62', lat: 50.04386, lng: 19.82743, tel: '12 429 71 80', foto: 'img/s-orla.jpg',
      godz: { pt: ['06:00', '20:00'], sob: ['07:00', '19:00'], nh: ['09:00', '17:00'] } },
    { id: 'przegorzalska', typ: 'sklep', nazwa: 'ul. Przegorzalska 2', rodzaj: 'Sklep spożywczo-przemysłowy', adres: 'ul. Przegorzalska 2', lat: 50.04819, lng: 19.87257, tel: '12 429 73 24', foto: 'img/s-przegorzalska.jpg',
      godz: { pt: ['06:00', '20:00'], sob: ['07:00', '19:00'], nh: ['09:00', '17:00'] } },
    { id: 'zaczek', typ: 'bar', nazwa: 'Bar mleczny Żaczek', rodzaj: 'Bar mleczny', adres: 'ul. Czarnowiejska 75', kod: '30-049 Kraków', lat: 50.067797, lng: 19.917558, tel: '12 633 96 76', foto: 'img/bar-zaczek.jpg',
      godz: { pt: ['08:00', '17:00'], sob: null, nh: null } },
    { id: 'flisak', typ: 'bar', nazwa: 'Bar mleczny Flisak', rodzaj: 'Bar mleczny', adres: 'ul. Kościuszki 1', kod: '30-105 Kraków', lat: 50.055301, lng: 19.926972, tel: '12 422 21 05', foto: 'img/bar-flisak.jpg',
      godz: { pt: ['08:00', '18:00'], sob: ['09:30', '14:30'], nh: null } }
  ];

  // niedziele handlowe i swieta (sklepy nieczynne) 2026-2027
  var NH = ['2026-01-25', '2026-03-29', '2026-04-26', '2026-06-28', '2026-08-30', '2026-12-06', '2026-12-13', '2026-12-20',
    '2027-01-31', '2027-03-21', '2027-04-25', '2027-06-27', '2027-08-29', '2027-12-05', '2027-12-12', '2027-12-19'];
  var SW = ['2026-01-01', '2026-01-06', '2026-04-05', '2026-04-06', '2026-05-01', '2026-05-03', '2026-05-24', '2026-06-04', '2026-08-15', '2026-11-01', '2026-11-11', '2026-12-24', '2026-12-25', '2026-12-26',
    '2027-01-01', '2027-01-06', '2027-03-28', '2027-03-29', '2027-05-01', '2027-05-03', '2027-05-16', '2027-05-27', '2027-08-15', '2027-11-01', '2027-11-11', '2027-12-24', '2027-12-25', '2027-12-26'];

  var MENU = {
    zakres: ['2026-10-19', '2026-10-23'], opis: '19-23.10.2026',
    zaczek: [
      ['Mała zupa grochowa z makaronem', 'Kotlet mielony, ziemniaki, buraczki', '28,23'],
      ['Zupa ziemniaczana', 'Papryka faszerowana ryżem i mięsem, sos pomidorowy', '28,03'],
      ['Mała zupa kalafiorowa z ryżem', 'Zraziki z kurczaka, sos z suszonych pomidorów, kopytka, surówka z białej kapusty', '36,18'],
      ['Mały rosół', 'Kotlet schabowy, ziemniaki, kapusta zasmażana', '34,24'],
      ['Barszcz ukraiński', 'Pierogi ruskie', '23,28']
    ],
    flisak: [
      ['Zupa pieczarkowa', 'Gołąbki z sosem pomidorowym', '26,30'],
      ['Zupa grochowa z makaronem', 'Mielony, ziemniaki, buraczki', '23,40'],
      ['Zupa pomidorowa z ryżem', 'Udko pieczone, ziemniaki, surówka z marchewki', '31,60'],
      ['Zupa ogórkowa', 'Kotlet schabowy, ziemniaki, kapusta zasmażana', '33,05'],
      ['Barszcz czerwony zabielany z ziemniakami', 'Pierogi ruskie', '22,40']
    ]
  };
  var BARY = {
    zaczek: { foto: 'img/bar-zaczek.jpg', alt: 'Wejście do baru mlecznego Żaczek przy ul. Czarnowiejskiej',
      wolt: 'https://wolt.com/pl/pol/krakow/restaurant/bar-mleczny-zaczek', bolt: 'https://food.bolt.eu/en/211-krakow/p/203649-bar-mleczny-zaczek/', glovo: 'https://glovoapp.com/pl/pl/krakow/stores/zaczek-bar-mleczny-kra',
      godzTxt: 'pn-pt 8:00-17:00, sobota i niedziela nieczynne' },
    flisak: { foto: 'img/bar-flisak.jpg', alt: 'Bar mleczny Flisak przy ul. Kościuszki, witryna z menu',
      wolt: 'https://wolt.com/pl/pol/krakow/restaurant/bar-mleczny-flisak', bolt: 'https://food.bolt.eu/en/211-krakow/p/203842-bar-mleczny-flisak/', glovo: 'https://glovoapp.com/pl/pl/krakow/stores/flisak-bar-mleczny-kra',
      godzTxt: 'pn-pt 8:00-18:00, sob 9:30-14:30, niedziela nieczynne' }
  };

  var PROD = [
    ['jogurt', 'Jogurt naturalny Nadbużański 9%', 'Kuchnia Lubelska', '1 kg', '13,79'],
    ['kefir', 'Kefir naturalny ze Skały', 'OSM w Skale', '500 ml', '5,69'],
    ['smietanka', 'Śmietanka kremowa 30% pasteryzowana', 'OSM w Skale', '500 ml', '17,29'],
    ['twarog-klimek', 'Twaróg półtłusty', 'Klimek', '1 kg', '49,69'],
    ['twarog-lapy', 'Twaróg półtłusty, klinek z Łap', 'Spółdzielnia Mleczarska w Łapach', '1 kg', '30,59'],
    ['lazanki', 'Łazanki ręcznie robione', 'Kuchnia Brawaty', '300 g', '19,29'],
    ['pierogi', 'Pierogi zbójnickie ręcznie robione', 'Kuchnia Brawaty', '350 g', '21,89'],
    ['miod', 'Miód lipowy nektarowy', 'Łysoń', '1,25 kg', '84,99'],
    ['syrop', 'Syrop malinowy', 'Polska Róża', '250 ml', '18,99'],
    ['syrop-mocy', 'Syrop mocy Złote mleko', 'A to dobre!', '250 ml', '17,99'],
    ['jarzebina', 'Jarzębina do herbaty', 'Bacówka', '200 g', '15,99'],
    ['herbatka', 'Herbatka owocowo-ziołowa Owocowy Raj', 'Natura Wita', '100 g', '23,99'],
    ['lipa', 'Lipa kwiatostan, susz ziołowy', 'Natura Wita', '50 g', '14,29'],
    ['ciasteczka', 'Bombonierka', 'Ciasteczka z Krakowa', '250 g', '22,79'],
    ['praliny', 'Bombonierka Rum&Gin Club', 'Edle Tropfen', '1 szt.', '21,99'],
    ['cotedor', 'Czekolada biała z ciasteczkami Lotus', "Côte d'Or", '380 g', '29,99']
  ];
  var OKAZJE = [
    ['banany', 'Banany, Kostaryka/Panama', '6,27', 'zł/kg', '8,99 zł/kg'],
    ['kiwi', 'Kiwi, Grecja', '1,37', 'zł/szt.', '2,49 zł/szt.'],
    ['cashmir', 'Papier toaletowy rumiankowy Cashmir 3W, 8 rolek', '8,97', 'zł/szt.', '10,99 zł/szt.'],
    ['ludwik', 'Płyn do mycia naczyń Ludwik 450 g, wybrane rodzaje', '4,77', 'zł/szt.', '6,69 zł/szt.'],
    ['hortex', 'Sok jabłkowy Hortex 1 l', '4,57', 'zł/szt.', '8,19 zł']
  ];

  /* ---------- czas w Krakowie ---------- */
  var DNI_W = ['w niedzielę', 'w poniedziałek', 'we wtorek', 'w środę', 'w czwartek', 'w piątek', 'w sobotę'];
  var DNI = ['Niedziela', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota'];
  var MIES = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia'];
  function teraz() {
    var p = {};
    try {
      new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Warsaw', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })
        .formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
      return { y: +p.year, m: +p.month, d: +p.day, min: (+p.hour % 24) * 60 + +p.minute };
    } catch (e) {
      var n = new Date();
      return { y: n.getFullYear(), m: n.getMonth() + 1, d: n.getDate(), min: n.getHours() * 60 + n.getMinutes() };
    }
  }
  function ds(y, m, d) { return y + '-' + String(m).padStart(2, '0') + '-' + String(d).padStart(2, '0'); }
  function dodajDni(t, n) { var x = new Date(Date.UTC(t.y, t.m - 1, t.d + n)); return { y: x.getUTCFullYear(), m: x.getUTCMonth() + 1, d: x.getUTCDate(), dow: x.getUTCDay() }; }
  function mm(s) { var a = s.split(':'); return +a[0] * 60 + +a[1]; }
  function hh(min) { return Math.floor(min / 60) + ':' + String(min % 60).padStart(2, '0'); }
  function godzDnia(g, dz) {
    var k = ds(dz.y, dz.m, dz.d);
    if (SW.indexOf(k) > -1) return null;
    if (dz.dow === 0) return NH.indexOf(k) > -1 ? g.nh : null;
    if (dz.dow === 6) return g.sob;
    return g.pt;
  }
  function status(g) {
    var t = teraz(), dz = dodajDni(t, 0), h = godzDnia(g, dz);
    if (h && t.min >= mm(h[0]) && t.min < mm(h[1])) {
      var zost = mm(h[1]) - t.min;
      return { otw: true, do: mm(h[1]), txt: zost <= 45 ? 'Zamykamy za ' + zost + ' min, o ' + hh(mm(h[1])) : 'Otwarte do ' + hh(mm(h[1])), wkrotce: zost <= 45 };
    }
    for (var i = 0; i < 9; i++) {
      var d2 = dodajDni(t, i), h2 = godzDnia(g, d2);
      if (!h2) continue;
      if (i === 0 && t.min >= mm(h2[0])) continue;
      var kiedy = i === 0 ? 'dziś' : i === 1 ? 'jutro' : DNI_W[d2.dow];
      return { otw: false, txt: 'Zamknięte, otwieramy ' + kiedy + ' o ' + hh(mm(h2[0])), za: i * 1440 + mm(h2[0]) - t.min };
    }
    return { otw: false, txt: 'Zamknięte', za: 99999 };
  }
  function nastNH() {
    var t = teraz(), k = ds(t.y, t.m, t.d);
    for (var i = 0; i < NH.length; i++) if (NH[i] >= k) { var a = NH[i].split('-'); return +a[2] + ' ' + MIES[+a[1] - 1]; }
    return '';
  }

  /* ---------- odleglosc ---------- */
  var poz = null;
  function km(a, b) {
    var R = 6371, r = Math.PI / 180, dLa = (b.lat - a.lat) * r, dLo = (b.lng - a.lng) * r;
    var x = Math.sin(dLa / 2) * Math.sin(dLa / 2) + Math.cos(a.lat * r) * Math.cos(b.lat * r) * Math.sin(dLo / 2) * Math.sin(dLo / 2);
    return 2 * R * Math.asin(Math.sqrt(x));
  }
  function fOdl(k) { return k < 1 ? Math.round(k * 1000 / 10) * 10 + ' m' : k.toFixed(1).replace('.', ',') + ' km'; }

  /* ---------- lista i mapa ---------- */
  var lista = document.getElementById('lista');
  var filtr = 'all', tylkoOtw = false, aktywny = null;
  var mapa = null, markery = {};

  function telHref(t) { return 'tel:+48' + t.replace(/\D/g, ''); }
  function prowadz(p) { return 'https://www.google.com/maps/dir/?api=1&destination=' + p.lat + ',' + p.lng; }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }

  function tabelaGodz(g, tytul) {
    var t = teraz(), dz = dodajDni(t, 0), k = ds(dz.y, dz.m, dz.d);
    var dzisRodz = SW.indexOf(k) > -1 ? 'sw' : dz.dow === 0 ? 'nd' : dz.dow === 6 ? 'sob' : 'pt';
    function w(nazwa, h, r) { return '<tr' + (r === dzisRodz ? ' class="dzis"' : '') + '><td>' + nazwa + '</td><td>' + (h ? hh(mm(h[0])) + '-' + hh(mm(h[1])) : 'nieczynne') + '</td></tr>'; }
    var nh = nastNH();
    return (tytul ? '<tr><td class="dzial" colspan="2">' + tytul + '</td></tr>' : '') +
      w('Poniedziałek-piątek', g.pt, 'pt') + w('Sobota', g.sob, 'sob') +
      w('Niedziela handlowa' + (nh && g.nh ? ' (najbliższa ' + nh + ')' : ''), g.nh, 'nh') + w('Pozostałe niedziele i święta', null, dzisRodz === 'nd' || dzisRodz === 'sw' ? dzisRodz : 'x');
  }

  var otwarteGodz = {};
  function rysujListe() {
    lista.querySelectorAll('.pl').forEach(function (li) { var g = li.querySelector('.godz'); otwarteGodz[li.dataset.id] = g && !g.hidden; });
    var dane = PL.map(function (p) { var s = status(p.godz); return { p: p, s: s, odl: poz ? km(poz, p) : null }; });
    dane = dane.filter(function (x) { return (filtr === 'all' || x.p.typ === filtr) && (!tylkoOtw || x.s.otw); });
    if (poz) dane.sort(function (a, b) { return a.odl - b.odl; });
    lista.innerHTML = '';
    if (!dane.length) {
      lista.appendChild(el('li', 'pusto', '<p class="pl-dod" style="padding:18px 0">Teraz żadna placówka z tej grupy nie jest otwarta. Wyłącz filtr „Tylko otwarte teraz”, żeby zobaczyć godziny.</p>'));
    }
    dane.forEach(function (x) {
      var p = x.p, s = x.s;
      var li = el('li', 'pl' + (aktywny === p.id ? ' akt' : ''));
      li.id = 'pl-' + p.id;
      li.dataset.id = p.id;
      var dod = '';
      if (p.dzialy) {
        var sd = status(p.dzialy[0].godz);
        dod = '<p class="pl-dod">Stoisko spożywcze na parterze. HOME i Eleganza: ' + (sd.otw ? 'otwarte do ' + hh(sd.do) : sd.txt.replace('Zamknięte, otwieramy', 'otwieramy')) + '</p>';
      }
      var tabela = '<table>' + tabelaGodz(p.godz, p.dzialy ? 'Stoisko spożywcze' : '') + (p.dzialy ? tabelaGodz(p.dzialy[0].godz, 'HOME i Salon Eleganza') : '') + '</table>' +
        (p.uslugi ? '<p class="uslugi">' + p.uslugi + '</p>' : p.typ === 'sklep' ? '<p class="uslugi">Opłacisz rachunki, zapłacisz kartą i bonami Pluxee, wypłacisz gotówkę (cashback), skorzystasz z karty klienta.</p>' : '');
      li.innerHTML =
        '<img class="pl-foto" src="' + p.foto + '" alt="' + p.rodzaj + ', ' + p.adres + '" loading="lazy" width="96" height="96">' +
        '<div class="pl-tresc">' +
        '<p class="pl-rodzaj">' + p.rodzaj + (p.dh ? '' : '') + '</p>' +
        '<h3>' + p.nazwa + '</h3>' +
        (p.dh || p.typ === 'bar' ? '<p class="pl-dod">' + p.adres + (p.kod ? ', ' + p.kod : '') + '</p>' : '') +
        '<p class="pl-status' + (s.otw ? (s.wkrotce ? ' wkrotce' : '') : ' zamk') + '"><span>' + s.txt + '</span>' + (x.odl != null ? '<span class="odl">' + fOdl(x.odl) + ' od Ciebie</span>' : '') + '</p>' +
        dod +
        '<div class="pl-akcje">' +
        '<a class="tel" href="' + telHref(p.tel) + '">' + p.tel + '</a>' +
        '<a href="' + prowadz(p) + '" target="_blank" rel="noopener">Prowadź</a>' +
        '<button type="button" class="pokaz-godz" aria-expanded="' + !!otwarteGodz[p.id] + '">' + (otwarteGodz[p.id] ? 'Zwiń godziny' : 'Godziny') + '</button>' +
        '</div>' +
        '<div class="godz"' + (otwarteGodz[p.id] ? '' : ' hidden') + '>' + tabela + '</div>' +
        '</div>';
      lista.appendChild(li);
    });
    rysujMarkery(dane);
    var zl = function (id, n) { var e = document.getElementById(id); if (e) e.textContent = n; };
    zl('nAll', PL.length); zl('nSklep', PL.filter(function (p) { return p.typ === 'sklep'; }).length); zl('nBar', PL.filter(function (p) { return p.typ === 'bar'; }).length);
  }

  function ikona(p, s) {
    return L.divIcon({ className: '', iconSize: p.dh ? [38, 38] : [26, 26], iconAnchor: p.dh ? [19, 19] : [13, 13],
      html: '<div class="pin' + (p.dh ? ' dh' : '') + (p.typ === 'bar' ? ' bar' : '') + (s.otw ? '' : ' zamk') + (aktywny === p.id ? ' akt' : '') + '"></div>' });
  }
  function rysujMarkery(dane) {
    if (!mapa) return;
    var widoczne = {};
    dane.forEach(function (x) { widoczne[x.p.id] = x; });
    PL.forEach(function (p) {
      var x = widoczne[p.id];
      if (!x) { if (markery[p.id]) { mapa.removeLayer(markery[p.id]); delete markery[p.id]; } return; }
      var ic = ikona(p, x.s);
      if (markery[p.id]) markery[p.id].setIcon(ic);
      else {
        markery[p.id] = L.marker([p.lat, p.lng], { icon: ic, title: p.nazwa, zIndexOffset: p.dh ? 500 : 0 }).addTo(mapa)
          .bindPopup('<b>' + p.nazwa + '</b><br>' + p.adres + '<br><span class="pp-st"></span>')
          .on('click', function () { wybierz(p.id, true); });
      }
      markery[p.id].setPopupContent('<b>' + (p.dh ? p.nazwa : p.rodzaj) + '</b><br>' + p.adres + '<br>' + x.s.txt);
    });
  }
  function wybierz(id, zMapy) {
    aktywny = id;
    lista.querySelectorAll('.pl').forEach(function (li) { li.classList.toggle('akt', li.dataset.id === id); });
    var p = PL.filter(function (q) { return q.id === id; })[0];
    if (mapa && p) {
      Object.keys(markery).forEach(function (k) {
        var ic = markery[k].getElement && markery[k].getElement();
        if (ic && ic.firstChild) ic.firstChild.classList.toggle('akt', k === id);
      });
      if (!zMapy) { mapa.flyTo([p.lat, p.lng], Math.max(mapa.getZoom(), 14), { duration: .6 }); markery[id] && markery[id].openPopup(); }
    }
    if (zMapy) {
      var li = document.getElementById('pl-' + id);
      if (li && window.innerWidth > 1060) li.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  lista.addEventListener('click', function (e) {
    var b = e.target.closest('.pokaz-godz');
    if (b) {
      var g = b.closest('.pl').querySelector('.godz');
      g.hidden = !g.hidden; b.setAttribute('aria-expanded', String(!g.hidden)); b.textContent = g.hidden ? 'Godziny' : 'Zwiń godziny';
      return;
    }
    var li = e.target.closest('.pl');
    if (li && (e.target.closest('h3') || e.target.closest('.pl-foto'))) {
      wybierz(li.dataset.id, false);
      if (window.innerWidth <= 1060) document.querySelector('.mapa-box').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
  document.querySelectorAll('.seg button').forEach(function (b) {
    b.addEventListener('click', function () {
      filtr = b.dataset.f;
      document.querySelectorAll('.seg button').forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', String(x === b)); });
      rysujListe(); dopasuj();
    });
  });
  document.getElementById('tylkoOtw').addEventListener('change', function (e) { tylkoOtw = e.target.checked; rysujListe(); });

  var geoBtn = document.getElementById('geoBtn'), geoInfo = document.getElementById('geoInfo');
  geoBtn.addEventListener('click', function () {
    if (poz) { poz = null; geoBtn.classList.remove('on'); geoInfo.hidden = true; if (mapa && mapa._ja) { mapa.removeLayer(mapa._ja); } rysujListe(); dopasuj(); return; }
    if (!navigator.geolocation) { geoInfo.hidden = false; geoInfo.textContent = 'Ta przeglądarka nie udostępnia lokalizacji. Pokazujemy listę w zwykłej kolejności.'; return; }
    geoInfo.hidden = false; geoInfo.textContent = 'Ustalamy Twoje położenie…';
    navigator.geolocation.getCurrentPosition(function (pos) {
      poz = { lat: pos.coords.latitude, lng: pos.coords.longitude };
      geoBtn.classList.add('on');
      rysujListe();
      var najbl = PL.slice().sort(function (a, b) { return km(poz, a) - km(poz, b); })[0];
      geoInfo.textContent = 'Najbliżej: ' + (najbl.dh ? najbl.nazwa : najbl.rodzaj.toLowerCase() + ' ' + najbl.nazwa) + ', ' + fOdl(km(poz, najbl)) + '. Lista posortowana od najbliższej placówki. Kliknij przycisk ponownie, żeby wyłączyć.';
      if (mapa) {
        if (mapa._ja) mapa.removeLayer(mapa._ja);
        mapa._ja = L.circleMarker([poz.lat, poz.lng], { radius: 8, color: '#fff', weight: 3, fillColor: '#1d1d1b', fillOpacity: 1 }).addTo(mapa).bindTooltip('Tu jesteś');
        mapa.fitBounds(L.latLngBounds([[poz.lat, poz.lng], [najbl.lat, najbl.lng]]).pad(.4), { maxZoom: 15 });
      }
      wybierz(najbl.id, false);
    }, function () {
      geoInfo.textContent = 'Bez dostępu do lokalizacji pokazujemy listę w zwykłej kolejności. Możesz go włączyć w ustawieniach przeglądarki.';
    }, { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 });
  });

  function dopasuj() {
    if (!mapa) return;
    var pts = Object.keys(markery).map(function (k) { return markery[k].getLatLng(); });
    if (pts.length) mapa.fitBounds(L.latLngBounds(pts).pad(.12), { maxZoom: 15 });
  }
  function initMapa() {
    if (!window.L) return;
    mapa = L.map('mapa', { scrollWheelZoom: false, zoomControl: true, attributionControl: true }).setView([50.07, 19.9], 12);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' }).addTo(mapa);
    mapa.attributionControl.setPrefix('<a href="https://leafletjs.com">Leaflet</a>');
  }

  /* ---------- hero: co jest otwarte teraz ---------- */
  function rysujTeraz() {
    var st = PL.map(function (p) { return { p: p, s: status(p.godz) }; });
    var otw = st.filter(function (x) { return x.s.otw; });
    var e = document.getElementById('teraz'), t = document.getElementById('terazTxt');
    if (otw.length) {
      var dh = st[0];
      var najdl = otw.slice().sort(function (a, b) { return b.s.do - a.s.do; })[0];
      e.classList.remove('zamk');
      t.innerHTML = 'Teraz otwarte: <b>' + otw.length + ' z ' + PL.length + ' placówek</b>. ' +
        (dh.s.otw ? 'Dom Handlowy do ' + hh(dh.s.do) + '.' : 'Najdłużej: ' + (najdl.p.dh ? 'Dom Handlowy' : najdl.p.nazwa) + ', do ' + hh(najdl.s.do) + '.');
    } else {
      var najw = st.slice().sort(function (a, b) { return a.s.za - b.s.za; })[0];
      e.classList.add('zamk');
      t.innerHTML = 'Teraz wszystkie placówki są zamknięte. ' + najw.s.txt.replace('Zamknięte, otwieramy', 'Najwcześniej otwieramy') + (najw.p.dh ? ' (Dom Handlowy).' : ' (' + najw.p.nazwa + ').');
    }
  }

  /* ---------- produkty ---------- */
  var polka = document.getElementById('polka');
  PROD.forEach(function (x) {
    polka.appendChild(el('li', 'prod', '<img src="img/p-' + x[0] + '.jpg" alt="' + x[1] + '" width="440" height="440" loading="lazy"><div class="prod-in"><p class="cena">' + x[4] + ' zł</p><h3>' + x[1] + '</h3><p>' + x[2] + ', ' + x[3] + '</p></div>'));
  });
  document.querySelectorAll('.strzalki button').forEach(function (b) {
    b.addEventListener('click', function () { polka.scrollBy({ left: +b.dataset.kier * polka.clientWidth * .8, behavior: 'smooth' }); });
  });

  /* ---------- okazje ---------- */
  var ok = document.getElementById('okazje');
  OKAZJE.forEach(function (x) {
    ok.appendChild(el('li', 'ok', '<img src="img/o-' + x[0] + '.jpg" alt="' + x[1] + '" width="395" height="280" loading="lazy"><div class="ok-in"><p class="cena">' + x[2] + ' <small>' + x[3] + '</small></p><h4>' + x[1] + '</h4><p>Najniższa cena z 30 dni: ' + x[4] + '</p></div>'));
  });

  /* ---------- bary ---------- */
  function rysujBary() {
    var t = teraz(), k = ds(t.y, t.m, t.d), dz = dodajDni(t, 0);
    var wTyg = k >= MENU.zakres[0] && k <= MENU.zakres[1] && dz.dow >= 1 && dz.dow <= 5;
    var u = document.getElementById('baryUklad');
    u.innerHTML = '';
    ['zaczek', 'flisak'].forEach(function (id) {
      var p = PL.filter(function (q) { return q.id === id; })[0], b = BARY[id], m = MENU[id], s = status(p.godz);
      var dzis = wTyg ? m[dz.dow - 1] : null;
      var naj = m.reduce(function (a, c) { return parseFloat(c[2].replace(',', '.')) < parseFloat(a[2].replace(',', '.')) ? c : a; });
      var art = el('article', 'bar');
      art.innerHTML =
        '<img class="bar-foto" src="' + b.foto + '" alt="' + b.alt + '" loading="lazy">' +
        '<h3>' + p.nazwa.replace('Bar mleczny ', 'Bar ') + '</h3>' +
        '<p class="bar-adr">' + p.adres + ', ' + p.kod + '</p>' +
        '<p class="bar-status' + (s.otw ? '' : ' zamk') + '">' + s.txt + '</p>' +
        (dzis ? '<div class="dzis"><p class="dzis-tyt">Dziś, ' + DNI[dz.dow].toLowerCase() + ': zupa i drugie danie</p><p class="dzis-danie">' + dzis[0] + '<br>' + dzis[1] + '</p><p class="dzis-cena">' + dzis[2] + ' zł</p></div>'
          : '<div class="dzis"><p class="dzis-tyt">Zestaw zupa i drugie danie</p><p class="dzis-danie">w menu tygodnia ' + MENU.opis + ' od ' + naj[2] + ' zł</p></div>') +
        '<details class="menu-tyg"' + (dzis ? '' : ' open') + '><summary>Menu tygodnia ' + MENU.opis + '</summary><ul>' +
        m.map(function (r, i) { return '<li' + (dzis && i === dz.dow - 1 ? ' class="dzisiaj"' : '') + '><span class="md">' + DNI[i + 1] + '</span><span>' + r[0] + ', ' + r[1].charAt(0).toLowerCase() + r[1].slice(1) + '</span><span class="mc">' + r[2] + ' zł</span></li>'; }).join('') +
        '</ul></details>' +
        '<p class="bar-godz">' + b.godzTxt + '</p>' +
        '<div class="bar-akcje"><a class="btn btn-or" href="' + telHref(p.tel) + '">Zadzwoń: ' + p.tel + '</a><a class="btn btn-linia" href="' + prowadz(p) + '" target="_blank" rel="noopener">Prowadź</a></div>' +
        '<p class="dowoz">Z dowozem: <a href="' + b.wolt + '" target="_blank" rel="noopener">Wolt</a>, <a href="' + b.bolt + '" target="_blank" rel="noopener">Bolt Food</a>, <a href="' + b.glovo + '" target="_blank" rel="noopener">Glovo</a></p>';
      u.appendChild(art);
    });
  }

  /* ---------- formularz wynajmu ---------- */
  var F = { typ: 'sala', biuro: '' };
  var NAZWY = { sala: 'sali konferencyjnej', biuro: 'biura', lokal: 'lokalu użytkowego przy ul. Machaya 1 (122 m²)', magazyn: 'powierzchni magazynowej' };
  var TELE = { sala: ['+48126193398', '12 619 33 98'], biuro: ['+48126193419', '12 619 34 19'], lokal: ['+48126193419', '12 619 34 19'], magazyn: ['+48126193419', '12 619 34 19'] };
  var $ = function (id) { return document.getElementById(id); };
  function tekst() {
    var L1 = ['Dzień dobry,', '', 'jestem zainteresowany/a wynajmem ' + NAZWY[F.typ] + ' w Handlowej Spółdzielni Jubilat.'];
    if (F.typ === 'sala') {
      if ($('fData').value) { var a = $('fData').value.split('-'); L1.push('Termin: ' + +a[2] + ' ' + MIES[+a[1] - 1] + ' ' + a[0] + '.'); }
      if ($('fOsoby').value) L1.push('Liczba osób: ' + $('fOsoby').value + '.');
    }
    if (F.typ === 'biuro' && F.biuro) L1.push('Interesuje mnie biuro o powierzchni ' + F.biuro + '.');
    if (F.typ === 'magazyn' && $('fM2').value) L1.push('Potrzebna powierzchnia: ok. ' + $('fM2').value + ' m².');
    if (F.typ !== 'sala') L1.push('Termin: ' + ($('fOd').value || 'od zaraz') + '.');
    if ($('fOpis').value.trim()) L1.push('', $('fOpis').value.trim());
    L1.push('', 'Proszę o informację o dostępności i warunkach najmu.', '', 'Pozdrawiam');
    if ($('fImie').value.trim()) L1.push($('fImie').value.trim());
    if ($('fTel').value.trim()) L1.push('tel. ' + $('fTel').value.trim());
    return L1.join('\n');
  }
  function temat() { return 'Zapytanie o wynajem ' + NAZWY[F.typ].replace(' przy ul. Machaya 1 (122 m²)', ', ul. Machaya 1'); }
  function odswiezForm() {
    document.querySelectorAll('.wyn-form .pola[data-dla]').forEach(function (p) { p.hidden = p.dataset.dla.split(' ').indexOf(F.typ) < 0; });
    var t = tekst();
    $('podglad').textContent = t;
    $('wynMail').href = 'mailto:administracja@jubilat.com.pl?subject=' + encodeURIComponent(temat()) + '&body=' + encodeURIComponent(t);
    $('wynTel').href = 'tel:' + TELE[F.typ][0];
    $('wynTel').textContent = 'lub zadzwoń: ' + TELE[F.typ][1];
  }
  document.querySelectorAll('.wyn-form .chipy').forEach(function (g) {
    g.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      g.querySelectorAll('button').forEach(function (x) { x.classList.toggle('on', x === b); });
      F[g.dataset.p] = b.dataset.v; odswiezForm();
    });
  });
  $('wynForm').addEventListener('input', odswiezForm);
  $('wynForm').addEventListener('submit', function (e) { e.preventDefault(); });
  $('wynKopiuj').addEventListener('click', function () {
    var b = this, t = tekst();
    var gotowe = function () { b.textContent = 'Skopiowano'; setTimeout(function () { b.textContent = 'Kopiuj treść'; }, 1800); };
    if (navigator.clipboard) navigator.clipboard.writeText(t).then(gotowe, gotowe); else gotowe();
  });
  odswiezForm();

  /* ---------- menu mobilne i pasek ---------- */
  var burger = document.querySelector('.burger'), panel = document.getElementById('panel');
  function zamknij() { panel.hidden = true; burger.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; }
  burger.addEventListener('click', function () {
    var o = panel.hidden; panel.hidden = !o; burger.setAttribute('aria-expanded', String(o)); document.body.style.overflow = o ? 'hidden' : '';
  });
  panel.addEventListener('click', function (e) { if (e.target.closest('a')) zamknij(); });
  var mob = document.getElementById('mob'), heroCta = document.querySelector('.hero-cta');
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en) {
      var e = en[0];
      mob.classList.toggle('widac', !e.isIntersecting && e.boundingClientRect.top < 0);
    }).observe(heroCta);
  }

  /* ---------- start ---------- */
  initMapa();
  rysujListe();
  dopasuj();
  rysujTeraz();
  rysujBary();
  setInterval(function () { rysujTeraz(); rysujListe(); }, 60000);
})();
