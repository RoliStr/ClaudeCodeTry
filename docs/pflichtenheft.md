# Pflichtenheft — Ferienhaus-Management-Plattform

**Projekt:** Verwaltungs- und Vermarktungsplattform für Ferienhäuser in Griechenland
**Dokumentversion:** 1.1 (Entwurf)
**Stand:** 2026-08-06
**Änderung gegenüber 1.0:** Kapitel 6.11 „Automatisierte Gästekommunikation" ergänzt (Nachrichtenstrecke per E-Mail und WhatsApp); zugehörige Anpassungen in den Kapiteln 1, 2, 4, 5.5, 7, 8, 9.3, 10, 11, 12, 13 und 14.
**Auftraggeber:** Roland Strahlhofer
**Status:** Zur Abstimmung — offene Punkte siehe Kapitel 12

---

## 1. Zielsetzung und Ausgangslage

### 1.1 Ausgangslage

Ein Ferienhaus in Griechenland wird über externe Portale (Booking.com, Airbnb u. a.)
vermarktet. Belegungen, Anfragen, Reinigungs- und Pflegetermine werden derzeit ohne
zentrales System geführt. Es existiert keine eigene Gästeseite; Informationen zum Haus
und zur Umgebung werden individuell pro Gast weitergegeben.

### 1.2 Projektziele

| Nr. | Ziel | Messbar durch |
|---|---|---|
| Z-1 | Zentrale, portalübergreifende Belegungsübersicht | Alle Belegungen aller Kanäle in einem Kalender sichtbar; keine Doppelbelegung |
| Z-2 | Direktbuchungsanteil erhöhen (provisionsfrei) | Anzahl Anfragen über die eigene Gästeseite pro Saison |
| Z-3 | Betriebsaufwand für Reinigung/Pflege reduzieren | Aufgaben werden automatisch aus Buchungen erzeugt und versendet |
| Z-4 | Gäste vorab und vor Ort informieren | Hausprospekt, Umgebungs- und Notfallinformationen online abrufbar |
| Z-5 | Griechischsprachige Gäste direkt ansprechen | Vollständige griechische Sprachfassung der Gästeseite |
| Z-6 | Erweiterbarkeit auf weitere Objekte | Zweites Objekt ohne Datenmodell-Migration anlegbar |
| Z-7 | Gäste ohne manuellen Aufwand vor, während und nach dem Aufenthalt begleiten | Anteil automatisch versandter Nachrichten je Buchung; Rückgang der Einzelrückfragen zu Anreise, Schlüssel und WLAN |

### 1.3 Abgrenzung (Nicht-Ziele der Erstversion)

- Keine Online-Zahlung, keine Rechnungsstellung, keine Kassenanbindung (siehe Phase 3).
- Keine automatische Preisoptimierung / Dynamic Pricing.
- Keine Anbindung an Buchhaltungssysteme oder die griechische myDATA-Plattform.
- Keine Smart-Home-/Schließanlagen-Integration.
- Keine native Mobil-App (die Weboberfläche ist mobil-optimiert).
- Kein Nachrichten-Posteingang im System: Antworten der Gäste auf E-Mails oder WhatsApp-Nachrichten laufen im gewohnten Postfach bzw. auf dem Telefon des Betreibers auf, nicht in einer eigenen Chatoberfläche (siehe Kapitel 6.11).

---

## 2. Grundsatzentscheidungen

Die folgenden Entscheidungen sind mit dem Auftraggeber abgestimmt und bilden die
Grundlage aller nachfolgenden Anforderungen.

| Nr. | Entscheidung | Festlegung |
|---|---|---|
| E-1 | Kanalanbindung | **iCal-Synchronisation** (Import je Portal + Export eines Gesamtkalenders). Keine direkte Portal-API, kein Channel-Manager. |
| E-2 | Buchungsprozess | **Unverbindliche Anfrage**. Bestätigung erfolgt manuell durch den Betreiber. Keine Sofortbuchung, keine Online-Zahlung. |
| E-3 | Umfang | **Phasiert**. Phase 1 (MVP) liefert einen produktiv nutzbaren Stand; Phasen 2 und 3 sind spezifiziert, aber später umzusetzen. |
| E-4 | Objekte | **Mandantenfähiges Datenmodell** (Entität „Objekt"), Oberfläche zunächst auf ein Objekt ausgelegt. |
| E-5 | Technologie | **Modernes JS-Frontend** (Next.js/React) mit eigenem Backend und relationaler Datenbank. |
| E-6 | Sprachen | **Deutsch, Griechisch, Englisch, Italienisch, Französisch**. |
| E-7 | Kartendienst | **Austauschbare Kartenkomponente**. Entscheidung OpenStreetMap vs. Google Maps wird zur Umsetzung getroffen; das System kapselt den Anbieter hinter einer internen Schnittstelle. |
| E-8 | Medien | **Bilder auf eigenem Server** (automatisch skaliert), **Videos extern gehostet** (YouTube/Vimeo, ungelistet) und eingebettet. |
| E-9 | Dienstleister | **Kein eigener Login.** Aufgaben werden per E-Mail/Messenger-Link zugestellt; der Status wird vom Betreiber gepflegt. |
| E-10 | Preise | **Saisonpreise mit Preisrechner** auf der Gästeseite; Ergebnis ist ein unverbindlicher Gesamtpreis. |
| E-11 | Gästekommunikation | **Terminierte Nachrichtenstrecke** entlang der Buchung (Vorgabe: 14 Tage vor Anreise, 7 Tage vor Anreise, am Anreisetag, 1 Tag vor Abreise, 7 Tage nach Abreise). Zeitpunkte, Inhalte und Kanäle sind frei konfigurierbar. |
| E-12 | Versandwege | **E-Mail vollautomatisch.** WhatsApp zunächst **halbautomatisch** (System erzeugt fertige Nachricht und Sendelink, Betreiber löst mit einem Tippen aus). Vollautomatisches WhatsApp über die WhatsApp Business Cloud API ist als spätere Ausbaustufe vorgesehen und im System vorbereitet — Entscheidung offen (O-16). |

---

## 3. Stakeholder und Rollen

| Rolle | Beschreibung | Zugang |
|---|---|---|
| **Betreiber (Admin)** | Eigentümer/Verwalter. Vollzugriff auf alle Funktionen und Objekte. | Login mit Passwort + zweitem Faktor |
| **Mitarbeiter (Manager)** | Optionale zweite Person (z. B. Partner, lokaler Verwalter). Zugriff auf Buchungen, Aufgaben, Moderation; keine Systemeinstellungen. | Login mit Passwort + zweitem Faktor |
| **Dienstleister** | Reinigungskraft, Gärtner, Pool-/Hausmeisterservice, Handwerker. Erhält Aufgaben als Nachricht, arbeitet außerhalb des Systems. | Kein Login (E-9) |
| **Gast (angefragt/gebucht)** | Person mit bestehender Anfrage oder Buchung. Ruft Gästeseite und ggf. einen persönlichen Aufenthaltslink auf. | Kein Login; ggf. unpersonalisierter Zugangslink |
| **Besucher** | Anonymer Website-Besucher. Sieht Prospekt, Verfügbarkeit, Preisrechner, Karte; kann Anfragen und POI-Vorschläge senden. | Kein Login |

---

## 4. Systemüberblick

### 4.1 Architektur

```
                     ┌──────────────────────────────────────────┐
                     │  Gästebereich (öffentlich, 5 Sprachen)   │
                     │  Prospekt · Verfügbarkeit · Preisrechner │
                     │  Anfrage · Karte/POI · Infoseiten        │
                     └──────────────────┬───────────────────────┘
                                        │
   ┌────────────────────┐    ┌──────────┴───────────┐    ┌──────────────────┐
   │  Externe Portale   │◄──►│   Applikation        │───►│  E-Mail-Versand  │
   │  Booking.com       │iCal│   Next.js + API      │    │  (Transaktions-  │
   │  Airbnb, weitere   │    │   PostgreSQL         │    │   dienst)        │
   └────────────────────┘    │                      │    └──────────────────┘
                             │   ┌────────────────┐ │    ┌──────────────────┐
                             │   │ Zeitsteuerung  │ ├───►│  WhatsApp        │
                             │   │ (Scheduler):   │ │    │  Sendelink bzw.  │
                             │   │ Kanal-Sync,    │ │    │  Business API    │
                             │   │ Nachrichten-   │ │    └──────────────────┘
                             │   │ strecke,       │ │
                             │   │ Aufgaben       │ │
                             │   └────────────────┘ │
                             └──────────┬───────────┘
                                        │
                     ┌──────────────────┴───────────────────────┐
                     │  Internes Management (Login)             │
                     │  Belegung · Anfragen · Preise · Aufgaben │
                     │  Nachrichtenplan · Sendungsvorschau      │
                     │  POI-Moderation · Inhalte · Medien       │
                     └──────────────────────────────────────────┘
```

### 4.2 Technologie-Festlegung

| Ebene | Festlegung | Begründung |
|---|---|---|
| Frontend/Backend | Next.js (App Router) mit TypeScript, serverseitige Route Handler als API | Eine Codebasis für Gästeseite und internen Bereich; serverseitiges Rendering für SEO und Ladezeit |
| Datenbank | PostgreSQL mit ORM (Prisma) | Relationale Integrität für Belegungen; Migrationsverwaltung |
| Internationalisierung | `next-intl` mit Locale-Routing (`/de`, `/el`, `/en`, `/it`, `/fr`) | Statische UI-Texte aus Sprachdateien, Inhaltstexte aus der Datenbank |
| Authentifizierung | Auth.js (Credentials + TOTP) | Nur interner Bereich, geringe Nutzerzahl |
| Bildverarbeitung | `sharp`, Ausspielung über `next/image` | Automatische Skalierung, WebP/AVIF |
| Zeitsteuerung | Persistente Auftragswarteschlange in der Datenbank, ausgelöst durch einen minütlichen Taktgeber | Nachrichtenversand und Kanal-Sync überstehen Neustarts; jeder Versand ist nachvollziehbar und einmalig |
| Karte | Adapter-Schnittstelle, Implementierung Leaflet **oder** Google Maps JS API | Anbieterwechsel ohne Änderung der Fachlogik (E-7) |
| Betrieb | Docker-Container hinter Caddy (Reverse Proxy, automatisches HTTPS) auf Lightsail | Entspricht der bestehenden Serverumgebung des Auftraggebers |

### 4.3 Umgebungen

- **Entwicklung** — lokal, Docker Compose, Testdatensatz.
- **Produktion** — Lightsail-Instanz, eigene Domain, tägliches Datenbank-Backup.
- Eine separate Staging-Umgebung ist optional (siehe offener Punkt O-11).

---

## 5. Funktionale Anforderungen — Gästebereich (öffentlich)

Priorisierung: **MUSS** = Phase 1, **SOLL** = Phase 2, **KANN** = Phase 3 oder optional.

### 5.1 Hausprospekt und Objektdarstellung

| ID | Anforderung | Prio |
|---|---|---|
| FA-G-01 | Das System zeigt eine Startseite mit Titelbild, Kurzbeschreibung, Hauptmerkmalen (Personenzahl, Schlafzimmer, Bäder, Pool, Entfernung zum Strand) und einer Handlungsaufforderung zur Anfrage. | MUSS |
| FA-G-02 | Es existiert eine ausführliche Hausbeschreibung mit gegliederten Abschnitten (Wohnbereich, Schlafzimmer, Küche, Außenbereich, Lage). Inhalte sind im internen Bereich pflegbar. | MUSS |
| FA-G-03 | Eine Ausstattungsliste wird aus einem gepflegten Merkmalskatalog erzeugt und mit Symbolen gruppiert dargestellt (z. B. Klimaanlage, WLAN, Waschmaschine, Grill, Kinderbett, Parkplatz, Haustiere erlaubt). | MUSS |
| FA-G-04 | Eine Bildergalerie zeigt Fotos mit Bildunterschrift und Kategorie (Außen, Innen, Umgebung); Vollbildansicht und Tastaturbedienung sind möglich. | MUSS |
| FA-G-05 | Ein Begrüßungsvideo wird als eingebetteter externer Player dargestellt. Mehrere Videos mit Titel und Sprachzuordnung sind möglich (z. B. Begrüßung, Hausführung, Anreisebeschreibung). | MUSS |
| FA-G-06 | Die Einbettung externer Videos erfolgt erst nach Zustimmung des Besuchers (Zwei-Klick-Lösung), solange keine Zustimmung im Cookie-Banner vorliegt. | MUSS |
| FA-G-07 | Ein Grundriss oder eine schematische Raumübersicht kann hinterlegt werden. | KANN |
| FA-G-08 | Es existiert eine druck- und teilbare Prospektansicht (PDF-Export der Objektdarstellung). | KANN |

### 5.2 Verfügbarkeit und Preise

| ID | Anforderung | Prio |
|---|---|---|
| FA-G-10 | Ein Belegungskalender zeigt mindestens 12 Monate im Voraus die Zustände *frei*, *belegt*, *Anreisetag*, *Abreisetag*, *gesperrt*. Es werden keine Details zu Belegungen (Gastname, Kanal) angezeigt. | MUSS |
| FA-G-11 | An- und Abreisetage werden halbtags dargestellt, sodass eine Anschlussbuchung am Wechseltag erkennbar bleibt. | MUSS |
| FA-G-12 | Der Kalender kennzeichnet Zeiträume, die den Mindestaufenthalt oder eine feste Anreiseregel (z. B. nur samstags in der Hochsaison) verletzen, als nicht wählbar. | MUSS |
| FA-G-13 | Eine Saisonpreistabelle zeigt alle definierten Saisonzeiträume mit Preis pro Nacht, Mindestaufenthalt und Gültigkeitszeitraum. | MUSS |
| FA-G-14 | Ein Preisrechner ermittelt nach Auswahl von Anreise, Abreise, Personenzahl und Haustieren einen unverbindlichen Gesamtpreis. Die Berechnung ist aufgeschlüsselt darzustellen: Übernachtungen je Saison, Rabatte, Endreinigung, Personenzuschlag, Haustiergebühr, gesetzliche Abgaben. | MUSS |
| FA-G-15 | Der ausgewiesene Preis ist ausdrücklich als unverbindlich zu kennzeichnen; die Verbindlichkeit entsteht erst mit der Bestätigung durch den Betreiber. | MUSS |
| FA-G-16 | Der Preisrechner berücksichtigt saisonübergreifende Aufenthalte durch nächteweise Berechnung. | MUSS |
| FA-G-17 | Rabatte für Aufenthalte ab 7 bzw. ab 14 Nächten sowie Frühbucher- und Last-Minute-Regeln sind konfigurierbar und werden automatisch angewandt. | SOLL |
| FA-G-18 | Preise werden in Euro angezeigt. Eine Anzeige in weiteren Währungen erfolgt nicht. | MUSS |

### 5.3 Buchungsanfrage

| ID | Anforderung | Prio |
|---|---|---|
| FA-G-20 | Ein Anfrageformular erfasst: Zeitraum, Anzahl Erwachsene, Anzahl Kinder mit Alter, Haustiere, Name, E-Mail, Telefon (optional), Land, Sprache, Freitextnachricht. | MUSS |
| FA-G-21 | Vor dem Absenden prüft das System die Verfügbarkeit des gewählten Zeitraums erneut serverseitig und weist auf Konflikte hin. | MUSS |
| FA-G-22 | Der Anfragende erhält unmittelbar eine Eingangsbestätigung per E-Mail in seiner gewählten Sprache mit Zusammenfassung von Zeitraum, Personen und errechnetem Richtpreis. | MUSS |
| FA-G-23 | Der Betreiber erhält eine Benachrichtigung über jede neue Anfrage per E-Mail. | MUSS |
| FA-G-24 | Das Formular ist gegen automatisierten Missbrauch geschützt (Honeypot-Feld, zeitbasierte Prüfung, IP-Ratenbegrenzung, Captcha-Dienst ohne Personenbezugsübertragung). | MUSS |
| FA-G-25 | Die Zustimmung zur Datenschutzerklärung wird explizit erfasst und mit Zeitstempel protokolliert. | MUSS |
| FA-G-26 | Eine Anfrage reserviert den Zeitraum nicht. Optional kann der Betreiber im internen Bereich eine befristete Option (Vormerkung) setzen, die im Kalender als *optioniert* erscheint. | SOLL |

### 5.4 Umgebung, Karte und Empfehlungen

| ID | Anforderung | Prio |
|---|---|---|
| FA-G-30 | Eine Kartenansicht zeigt das Objekt sowie alle freigegebenen Empfehlungen (Points of Interest, POI) als Marker. | MUSS |
| FA-G-31 | POI sind kategorisiert. Mindestkategorien: Restaurant/Taverne, Strand, Sehenswürdigkeit, Supermarkt/Einkauf, Arzt/Apotheke/Klinik, Bank/Geldautomat, Tankstelle, Freizeit/Aktivität, Verkehr (Hafen, Flughafen, Bushaltestelle). Weitere Kategorien sind im internen Bereich anlegbar. | MUSS |
| FA-G-32 | Die Karte lässt sich nach Kategorie filtern und zeigt die Entfernung vom Objekt (Luftlinie und, sofern verfügbar, Fahrstrecke). | MUSS |
| FA-G-33 | Jeder POI besitzt eine Detailansicht mit Name, Kategorie, Beschreibung, Adresse, optionalen Öffnungszeiten, Telefonnummer, Website, Bild und einem Link „Route in Google Maps öffnen" (Deeplink über Koordinaten). | MUSS |
| FA-G-34 | Neben der Karte existiert eine Listenansicht, sortierbar nach Entfernung und Kategorie, die auch ohne geladene Karte nutzbar ist. | MUSS |
| FA-G-35 | Besucher und Gäste können neue POI vorschlagen (Formular mit Name, Kategorie, Beschreibung, Standortauswahl auf der Karte oder Adresseingabe, optional Bild und E-Mail für Rückfragen). | MUSS |
| FA-G-36 | Vorgeschlagene POI werden **nicht** sofort veröffentlicht, sondern erhalten den Status *eingereicht* und erscheinen erst nach Freigabe im internen Bereich. | MUSS |
| FA-G-37 | Das Vorschlagsformular unterliegt denselben Missbrauchsschutzmaßnahmen wie das Anfrageformular (FA-G-24). | MUSS |
| FA-G-38 | Gäste können freigegebene POI bewerten (Sterne) oder kommentieren; Kommentare unterliegen ebenfalls der Freigabe. | KANN |
| FA-G-39 | POI-Beschreibungen sind mehrsprachig pflegbar; fehlt eine Übersetzung, wird die Fassung der Fallback-Sprache angezeigt und als solche gekennzeichnet. | SOLL |

### 5.5 Gäste- und Serviceinformationen

| ID | Anforderung | Prio |
|---|---|---|
| FA-G-40 | Es existieren frei anlegbare Informationsseiten mit strukturiertem Text, Bildern und Verlinkungen (z. B. „Anreise", „Ankunft und Schlüsselübergabe", „Hausordnung", „WLAN und Technik", „Müll und Recycling", „Notfallnummern"). | MUSS |
| FA-G-41 | Eine Notfall- und Versorgungsübersicht listet Arzt, Zahnarzt, Apotheke (inkl. Notdienstinformation), Krankenhaus, Polizei, Feuerwehr, europäischer Notruf 112, mit Telefonnummer, Adresse und Kartenlink. | MUSS |
| FA-G-42 | Zu Supermärkten, Apotheken, Banken und Behörden können Öffnungszeiten inklusive Saison- und Feiertagsabweichungen hinterlegt und dargestellt werden. Der Stand der Angabe („zuletzt geprüft am") wird ausgewiesen. | MUSS |
| FA-G-43 | Alle Öffnungszeitangaben tragen den Hinweis, dass Angaben ohne Gewähr sind. | MUSS |
| FA-G-44 | Häufige Fragen (FAQ) sind als eigene Seite mit Kategorien pflegbar. | SOLL |
| FA-G-45 | Bestätigten Gästen kann ein personalisierter Aufenthaltslink zugesandt werden, der zusätzlich zeitraumbezogene Informationen enthält (Zugangscode, Schlüsselübergabe, konkrete Anreisezeiten, Kontakt vor Ort). Der Link ist nicht erratbar und läuft nach Abreise ab. | SOLL |
| FA-G-46 | Nach der Abreise kann automatisiert eine Bitte um Bewertung mit Links zu den Portalen versandt werden (Teil der Nachrichtenstrecke, Kapitel 6.11). | SOLL |
| FA-G-47 | Im Anfrageformular kann der Gast seine bevorzugte Kontaktart (E-Mail, WhatsApp) und seine WhatsApp-Nummer angeben; die Angabe ist freiwillig. | SOLL |
| FA-G-48 | Jede automatisch versandte Nachricht enthält einen Abmeldelink, über den der Gast weitere Nachrichten der Strecke abbestellen kann, ohne dass buchungsrelevante Mitteilungen entfallen. | SOLL |
| FA-G-49 | Über den Abmeldelink erreicht der Gast eine Seite, auf der er seine Kontaktpräferenzen ändern oder allen weiteren Nachrichten widersprechen kann. | SOLL |

### 5.6 Sprachen und Barrierefreiheit

| ID | Anforderung | Prio |
|---|---|---|
| FA-G-50 | Die Gästeseite ist in Deutsch, Griechisch und Englisch vollständig verfügbar (Phase 1); Italienisch und Französisch folgen in Phase 2. | MUSS/SOLL |
| FA-G-51 | Die Sprachwahl erfolgt über einen sichtbaren Umschalter; die Vorauswahl richtet sich nach der Browsersprache. Die gewählte Sprache bleibt über die Sitzung erhalten und ist in der URL abgebildet. | MUSS |
| FA-G-52 | Griechische Inhalte werden korrekt in Unicode dargestellt; Sortierungen und Datumsformate folgen der jeweiligen Locale (griechische Monatsnamen im Genitiv bei Datumsangaben). | MUSS |
| FA-G-53 | Alle Seiten enthalten `hreflang`-Angaben für die verfügbaren Sprachfassungen. | MUSS |
| FA-G-54 | Die Oberfläche erfüllt WCAG 2.2 Stufe AA (Kontraste, Tastaturbedienbarkeit, Alternativtexte, Fokusanzeige, Formularbeschriftungen). | MUSS |

---

## 6. Funktionale Anforderungen — Interner Managementbereich

### 6.1 Zugang und Rechte

| ID | Anforderung | Prio |
|---|---|---|
| FA-I-01 | Der interne Bereich ist nur nach Anmeldung erreichbar und wird von Suchmaschinen ausgeschlossen. | MUSS |
| FA-I-02 | Die Anmeldung erfordert einen zweiten Faktor (TOTP). Wiederholt fehlgeschlagene Anmeldungen werden verzögert und protokolliert. | MUSS |
| FA-I-03 | Es existieren die Rollen *Admin* und *Manager* mit unterschiedlichen Rechten (siehe Kapitel 3). | MUSS |
| FA-I-04 | Sicherheitsrelevante und datenverändernde Vorgänge (Freigaben, Löschungen, Änderungen an Buchungen und Preisen) werden mit Zeitstempel, Benutzer und Vorher-/Nachher-Wert protokolliert. | MUSS |

### 6.2 Objektstammdaten

| ID | Anforderung | Prio |
|---|---|---|
| FA-I-10 | Objekte werden mit Bezeichnung, Adresse, Koordinaten, Kapazität, Ausstattungsmerkmalen, Check-in-/Check-out-Zeiten, Hausordnung und Registrierungsnummer(n) verwaltet. | MUSS |
| FA-I-11 | Die griechische Immobilien-Registriernummer (AMA) sowie weitere gesetzlich anzugebende Kennungen sind pflegbar und werden auf der Gästeseite ausgewiesen. | MUSS |
| FA-I-12 | Das Datenmodell erlaubt beliebig viele Objekte; jede Buchung, Aufgabe, jeder POI und Inhalt ist genau einem Objekt zugeordnet (POI ggf. objektübergreifend, siehe O-6). | MUSS |
| FA-I-13 | Die Oberfläche zeigt einen Objektumschalter, sobald mehr als ein Objekt existiert. | SOLL |

### 6.3 Belegung und Buchungen

| ID | Anforderung | Prio |
|---|---|---|
| FA-I-20 | Eine Belegungsübersicht stellt alle Buchungen kanalübergreifend als Monats- und Jahresansicht dar; die Herkunft (Direkt, Booking.com, Airbnb, sonstiges Portal, Eigennutzung, Sperrung) ist farblich unterscheidbar. | MUSS |
| FA-I-21 | Buchungen können manuell angelegt, bearbeitet, storniert und gelöscht werden. Erfasst werden: Zeitraum, Kanal, Gastdaten, Personenzahl, Preis, Anzahlung, Status, interne Notiz. | MUSS |
| FA-I-22 | Zeiträume können ohne Gastbezug gesperrt werden (Eigennutzung, Wartung, Renovierung) mit Angabe eines Grundes. | MUSS |
| FA-I-23 | Überschneidende Belegungen werden beim Speichern erkannt und blockiert; entsteht eine Überschneidung durch einen Kanalimport, wird sie als Konflikt gekennzeichnet und dem Betreiber gemeldet. | MUSS |
| FA-I-24 | Buchungsstatus: *Anfrage*, *Option*, *Bestätigt*, *Angezahlt*, *Bezahlt*, *Storniert*, *Abgereist*. Statusübergänge sind protokolliert. | MUSS |
| FA-I-25 | Zu jeder Buchung können Dokumente und Notizen abgelegt werden. | SOLL |
| FA-I-26 | Eine Jahresübersicht zeigt Auslastung, Umsatz nach Kanal und durchschnittlichen Nächtepreis. | KANN |

### 6.4 Anfragenbearbeitung

| ID | Anforderung | Prio |
|---|---|---|
| FA-I-30 | Alle eingehenden Anfragen erscheinen in einer Liste mit Status *neu*, *in Bearbeitung*, *Angebot gesendet*, *bestätigt*, *abgelehnt*, *storniert*, *abgelaufen*. | MUSS |
| FA-I-31 | Aus einer Anfrage kann mit einem Schritt eine Buchung erzeugt werden; die Gastdaten werden übernommen. | MUSS |
| FA-I-32 | Der Betreiber kann eine Antwort direkt aus dem System versenden. Textvorlagen je Sprache (Angebot, Absage wegen Belegung, Rückfrage) sind pflegbar und unterstützen Platzhalter (Name, Zeitraum, Preis). | MUSS |
| FA-I-33 | Der gesamte E-Mail-Verkehr zu einer Anfrage wird chronologisch bei der Anfrage protokolliert. | SOLL |
| FA-I-34 | Unbearbeitete Anfragen werden nach einer konfigurierbaren Frist (Vorgabe: 48 Stunden) hervorgehoben und per Erinnerung gemeldet. | SOLL |

### 6.5 Kanalanbindung (iCal)

| ID | Anforderung | Prio |
|---|---|---|
| FA-I-40 | Je Objekt können beliebig viele Kanäle mit Bezeichnung, Farbe und iCal-Import-URL angelegt werden. | MUSS |
| FA-I-41 | Der Import läuft automatisiert in einem konfigurierbaren Intervall (Vorgabe: alle 30 Minuten) sowie manuell auf Knopfdruck. | MUSS |
| FA-I-42 | Importierte Belegungen werden anhand der iCal-UID eindeutig zugeordnet; Änderungen und Löschungen im Quellkalender werden übernommen. | MUSS |
| FA-I-43 | Importierte Belegungen sind als kanalgebunden gekennzeichnet und im System nicht frei editierbar, um Überschreibungen beim nächsten Import zu vermeiden. Interne Notizen und manuell ergänzte Gastdaten bleiben erhalten. | MUSS |
| FA-I-44 | Das System stellt je Objekt eine Export-iCal-URL mit nicht erratbarem Token bereit, die alle Belegungen aller Quellen enthält und in den Portalen hinterlegt werden kann. | MUSS |
| FA-I-45 | Der Export enthält keine personenbezogenen Daten (nur Zeitraum und neutraler Titel). | MUSS |
| FA-I-46 | Import- und Exportvorgänge werden protokolliert (Zeitpunkt, Kanal, Anzahl neuer/geänderter/entfernter Einträge, Fehler). | MUSS |
| FA-I-47 | Bleibt ein Import länger als eine konfigurierbare Frist erfolglos oder liefert er einen Fehler, wird der Betreiber benachrichtigt. | MUSS |
| FA-I-48 | Ein Konfliktbericht listet Doppelbelegungen aus unterschiedlichen Quellen mit Handlungsempfehlung. | MUSS |
| FA-I-49 | Die Systemgrenzen der iCal-Synchronisation (nur Zeiträume, keine Preise/Gastdaten, anbieterseitige Aktualisierungsintervalle, verbleibendes Overbooking-Restrisiko) werden dokumentiert und im Kanalbereich angezeigt. | MUSS |

### 6.6 Preis- und Saisonverwaltung

| ID | Anforderung | Prio |
|---|---|---|
| FA-I-50 | Saisonzeiträume mit Bezeichnung, Datumsbereich, Nächtepreis, Mindestaufenthalt und optionaler Anreisetagsregel sind pflegbar; Überschneidungen werden verhindert. | MUSS |
| FA-I-51 | Zusatzentgelte sind konfigurierbar: Endreinigung (pauschal), Personenzuschlag ab definierter Belegung, Haustiergebühr, Wäschepaket, Kaution, Kurtaxe bzw. gesetzliche Abgaben je Nacht oder je Aufenthalt. | MUSS |
| FA-I-52 | Rabattregeln (Wochen-/Monatsrabatt, Frühbucher, Last-Minute) mit Gültigkeitszeitraum sind pflegbar. | SOLL |
| FA-I-53 | Für einzelne Tage können Preise und Mindestaufenthalte abweichend überschrieben werden (z. B. Feiertage, lokale Feste). | SOLL |
| FA-I-54 | Eine Vorschau zeigt das Ergebnis des Preisrechners für einen beliebigen Testzeitraum, um Regeln vor Veröffentlichung zu prüfen. | SOLL |

### 6.7 Reinigung, Pflege und Instandhaltung

| ID | Anforderung | Prio |
|---|---|---|
| FA-I-60 | Dienstleister werden mit Name, Gewerk, Telefon, E-Mail, bevorzugtem Benachrichtigungsweg, Sprache und Stundensatz/Pauschale verwaltet. | SOLL |
| FA-I-61 | Aufgaben besitzen Titel, Beschreibung, Gewerk, Fälligkeitsdatum und -zeit, zugeordneten Dienstleister, Priorität, Status (*offen*, *beauftragt*, *erledigt*, *abgenommen*, *entfallen*), Kostenschätzung und tatsächliche Kosten. | SOLL |
| FA-I-62 | Aus Buchungen werden automatisch Aufgaben erzeugt: Endreinigung am Abreisetag, Vorbereitung/Check vor dem Anreisetag, Wäschewechsel bei Aufenthalten über einer konfigurierbaren Dauer. Die Regeln sind je Objekt konfigurierbar. | SOLL |
| FA-I-63 | Wiederkehrende Aufgaben mit Intervall sind anlegbar (Gartenpflege wöchentlich, Poolpflege/Wasserwerte, Klimaanlagenwartung saisonal, Rauchmelder- und Feuerlöscherprüfung jährlich, Schädlingsprophylaxe, Zisternen-/Wassertankprüfung, Winterfestmachung und Saisoneröffnung). | SOLL |
| FA-I-64 | Ein Aufgabenkalender zeigt Aufgaben und Belegungen gemeinsam, damit Wechseltage und Engpässe erkennbar sind. | SOLL |
| FA-I-65 | Aufgaben werden dem Dienstleister automatisch per E-Mail in dessen Sprache zugestellt; zusätzlich erzeugt das System einen vorbereiteten Messenger-Link (z. B. `wa.me`) mit dem Aufgabentext zum manuellen Versand. | SOLL |
| FA-I-66 | Der Erledigungsstatus wird vom Betreiber gepflegt (E-9). Rückmeldungen (Fotos, Nachrichten) können manuell an der Aufgabe abgelegt werden. | SOLL |
| FA-I-67 | Ein Mängel-/Schadensregister erfasst Meldungen mit Foto, Ort im Haus, Dringlichkeit, Status und Folgeaufgabe. | SOLL |
| FA-I-68 | Ein Inventar- und Verbrauchsmaterialbereich verwaltet Bestände (Bettwäsche, Handtücher, Reinigungsmittel, Gasflaschen, Ersatzteile) mit Mindestbestandswarnung. | KANN |
| FA-I-69 | Zählerstände (Strom, Wasser) und Versorgungskosten können erfasst und im Zeitverlauf ausgewertet werden. | KANN |
| FA-I-70 | Wiederkehrende Termine ohne Gewerksbezug (Versicherung, Grundsteuer/ENFIA, Gewerbeanmeldung, TÜV-artige Prüfungen) werden als Fristenliste mit Vorlauferinnerung geführt. | KANN |

### 6.8 POI-Moderation

| ID | Anforderung | Prio |
|---|---|---|
| FA-I-80 | Neu eingereichte POI erscheinen in einer Moderationsliste mit Kennzeichnung als *neu* und einem Zähler in der Navigation. | MUSS |
| FA-I-81 | Der Betreiber kann eingereichte POI freigeben, bearbeiten und freigeben, ablehnen (mit Grund) oder als Spam markieren. | MUSS |
| FA-I-82 | Alle POI — auch selbst angelegte — sind jederzeit bearbeitbar und löschbar. Gelöschte Einträge werden zunächst in einen Papierkorb verschoben und erst nach einer Frist endgültig entfernt. | MUSS |
| FA-I-83 | Der Betreiber kann POI selbst anlegen, inklusive Standortsetzung per Karte, Kategorie, Bild und mehrsprachiger Beschreibung. | MUSS |
| FA-I-84 | POI können als *Empfehlung des Gastgebers* hervorgehoben und in der Reihenfolge gewichtet werden. | SOLL |
| FA-I-85 | Zu jedem eingereichten POI werden Einreichungszeitpunkt, IP-Adresse (gekürzt) und ggf. Kontakt-E-Mail gespeichert, um wiederholten Missbrauch zu erkennen. Absender können gesperrt werden. | MUSS |
| FA-I-86 | Ein Massenimport von POI (CSV) ist möglich. | KANN |

### 6.9 Inhalts- und Medienverwaltung

| ID | Anforderung | Prio |
|---|---|---|
| FA-I-90 | Alle Texte der Gästeseite (Beschreibungen, Infoseiten, FAQ, rechtliche Texte) sind ohne Programmierkenntnisse über einen Editor pflegbar. | MUSS |
| FA-I-91 | Für jeden Inhalt ist der Übersetzungsstand je Sprache erkennbar (*fehlt*, *veraltet*, *aktuell*). | MUSS |
| FA-I-92 | Bilder werden hochgeladen, automatisch in mehrere Größen und moderne Formate umgewandelt und mit Alternativtext je Sprache versehen. Die Sortierung erfolgt per Drag-and-drop. | MUSS |
| FA-I-93 | Videos werden über die URL des externen Anbieters eingebunden (E-8); Titel, Sprache und Reihenfolge sind pflegbar. | MUSS |
| FA-I-94 | Beim Bildupload werden Standort-Metadaten (EXIF-GPS) entfernt. | MUSS |
| FA-I-95 | Inhalte können als Entwurf gespeichert und zu einem Zeitpunkt veröffentlicht werden. | KANN |

### 6.10 Benachrichtigungen und Auswertungen

| ID | Anforderung | Prio |
|---|---|---|
| FA-I-100 | Das Startdashboard zeigt: heutige und kommende An-/Abreisen, offene Anfragen, offene Aufgaben, POI zur Freigabe, Kanal-Synchronisationsstatus, erkannte Konflikte. | MUSS |
| FA-I-101 | Der Betreiber erhält eine Tagesübersicht per E-Mail (konfigurierbar an/aus) mit den Ereignissen des Folgetages. | SOLL |
| FA-I-102 | Auswertungen zu Auslastung, Umsatz je Kanal, Anfrage-Konversionsrate, Betriebskosten je Aufenthalt sind als Jahresvergleich abrufbar und exportierbar (CSV). | KANN |

### 6.11 Automatisierte Gästekommunikation (Nachrichtenstrecke)

Ziel ist es, jeden Gast ohne manuellen Aufwand entlang seines Aufenthalts mit den
jeweils passenden Informationen zu versorgen. Die Strecke besteht aus mehreren
Nachrichtenregeln, die sich an den Daten einer Buchung ausrichten.

#### 6.11.1 Vorkonfigurierte Nachrichtenstrecke

Die folgende Strecke wird als Standard ausgeliefert und ist vollständig änderbar.
Alle Zeitpunkte beziehen sich auf die Ortszeit des Objekts.

| Nr. | Auslöser | Zeitpunkt | Zweck / typischer Inhalt |
|---|---|---|---|
| M-1 | Anreise | 14 Tage davor | Vorfreude und Reisevorbereitung: Anreisebeschreibung, Flughafen und Fährverbindungen, Mietwagenempfehlung, Gepäckhinweise, Link zur Umgebungskarte, Bitte um Angabe der voraussichtlichen Ankunftszeit |
| M-2 | Anreise | 7 Tage davor | Konkrete Vorbereitung: Wetter- und Kleidungshinweis, Einkaufsmöglichkeiten und deren Öffnungszeiten, Restaurantempfehlungen mit Reservierungshinweis, Ausflugstipps, Rückfrage zu Sonderwünschen (Kinderbett, früher Check-in) |
| M-3 | Anreise | am Anreisetag, morgens | Ankunft: Adresse und Koordinaten, Schlüsselübergabe bzw. Zugangscode, Check-in-Zeit, WLAN-Zugang, Kontakt vor Ort, Notfallnummern, Hausordnung in Kurzform |
| M-4 | Abreise | 1 Tag davor | Abreise: Check-out-Zeit, Schlüsselrückgabe, Müll und Recycling, Zustand der Küche, Kaution und Rückerstattung, Angebot eines späten Check-outs |
| M-5 | Abreise | 7 Tage danach | Nachbereitung: Dank, Bitte um Bewertung mit Direktlink zum jeweiligen Portal, Hinweis auf Fundsachen, Angebot für eine Direktbuchung im Folgejahr |

Weitere Regeln sind jederzeit ergänzbar, etwa eine Begrüßung am zweiten Aufenthaltstag
oder eine Erinnerung an die Zahlung einer Restsumme.

#### 6.11.2 Funktionale Anforderungen

| ID | Anforderung | Prio |
|---|---|---|
| FA-I-110 | Der Betreiber verwaltet Nachrichtenregeln mit: Bezeichnung, Bezugspunkt (*Anreise*, *Abreise*, *Buchungsbestätigung*, *Anfrageeingang*), Versatz in Tagen (davor/danach), Versandzeit als Ortszeit des Objekts, Kanal (*E-Mail*, *WhatsApp*, *beide*), Vorlage, Aktivierungsschalter. | MUSS-P2 |
| FA-I-111 | Nachrichtenregeln können an Bedingungen geknüpft werden: Buchungsstatus, Herkunftskanal, Mindest-/Höchstaufenthaltsdauer, Vorhandensein bestimmter Kontaktdaten, Sprache des Gastes, Objekt. | MUSS-P2 |
| FA-I-112 | Zu jeder Regel existiert eine Vorlage je unterstützter Sprache. Der Versand erfolgt in der beim Gast hinterlegten Sprache; fehlt diese Fassung, greift eine festgelegte Fallback-Sprache. | MUSS-P2 |
| FA-I-113 | Vorlagen unterstützen Platzhalter, die beim Versand ersetzt werden: Gastname, Anreise- und Abreisedatum, Anzahl Nächte, Personenzahl, Objektname, Adresse und Koordinaten, Check-in-/Check-out-Zeit, WLAN-Zugang, Zugangscode, Restbetrag, Link zur Gästeseite, Link zum persönlichen Aufenthaltsbereich, Abmeldelink. | MUSS-P2 |
| FA-I-114 | Beim Speichern einer Vorlage wird geprüft, ob alle verwendeten Platzhalter bekannt sind; unbekannte Platzhalter werden als Fehler gemeldet und verhindern das Speichern. | MUSS-P2 |
| FA-I-115 | Eine Vorschau zeigt die fertige Nachricht mit den Daten einer wählbaren realen oder fiktiven Buchung, je Sprache und Kanal. | MUSS-P2 |
| FA-I-116 | Testnachrichten können an eine frei wählbare eigene Adresse bzw. Nummer gesendet werden, ohne den Gast zu erreichen. | MUSS-P2 |
| FA-I-117 | Sobald eine Buchung den Status *bestätigt* erreicht, erzeugt das System für alle zutreffenden Regeln geplante Sendungen mit berechnetem Versandzeitpunkt. | MUSS-P2 |
| FA-I-118 | Eine Übersicht „geplante Sendungen" zeigt alle anstehenden Nachrichten mit Empfänger, Zeitpunkt, Kanal, Regel und Vorschau. Einzelne Sendungen können vorgezogen, verschoben, bearbeitet, übersprungen oder sofort ausgelöst werden. | MUSS-P2 |
| FA-I-119 | Ändert sich der Zeitraum einer Buchung, werden alle noch nicht versandten Sendungen automatisch neu terminiert. Bereits versandte Nachrichten bleiben unverändert protokolliert. | MUSS-P2 |
| FA-I-120 | Wird eine Buchung storniert, werden alle offenen Sendungen dieser Buchung abgebrochen und als *entfallen* gekennzeichnet. | MUSS-P2 |
| FA-I-121 | Liegt ein berechneter Versandzeitpunkt bereits in der Vergangenheit (z. B. bei einer Buchung zehn Tage vor Anreise), wird die betreffende Nachricht nicht nachträglich versandt, sondern übersprungen und in der Übersicht als *nicht mehr relevant* ausgewiesen. Der Betreiber kann sie bei Bedarf manuell auslösen. | MUSS-P2 |
| FA-I-122 | Jede Sendung wird höchstens einmal versandt. Neustarts, Mehrfachläufe des Taktgebers oder parallele Prozesse dürfen keinen Doppelversand auslösen. | MUSS-P2 |
| FA-I-123 | Es gelten konfigurierbare Ruhezeiten (Vorgabe: kein Versand zwischen 21:00 und 08:00 Ortszeit). Fällt ein Versandzeitpunkt in die Ruhezeit, wird auf den nächsten zulässigen Zeitpunkt verschoben. | MUSS-P2 |
| FA-I-124 | Ein globaler Betriebsmodus ist wählbar: *automatisch* (Versand ohne Zutun) oder *mit Freigabe* (jede Sendung erscheint zur Bestätigung und geht erst nach Freigabe raus). Zusätzlich existiert ein Notaus, der jeden automatischen Versand sofort anhält. | MUSS-P2 |
| FA-I-125 | Für den Kanal WhatsApp im halbautomatischen Betrieb (E-12) erzeugt das System die fertige Nachricht und stellt sie mit einem Sendelink (`wa.me` mit vorbelegtem Text) sowie einer Kopierfunktion bereit. Fällige WhatsApp-Nachrichten werden dem Betreiber als Sammelerinnerung zugestellt und im Dashboard angezeigt. Nach dem Versand bestätigt der Betreiber die Sendung mit einem Klick. | MUSS-P2 |
| FA-I-126 | Der Kanal WhatsApp ist so gekapselt, dass ein späterer Wechsel auf die WhatsApp Business Cloud API ohne Änderung der Regeln und Vorlagen möglich ist. Die für genehmigungspflichtige Nachrichtenvorlagen nötigen Angaben (Vorlagenname, Kategorie, Parameterliste) werden im Datenmodell vorgehalten. | MUSS-P2 |
| FA-I-127 | Bei vollautomatischem WhatsApp-Betrieb versendet das System ausschließlich zuvor genehmigte Vorlagen, protokolliert den Zustellstatus (gesendet, zugestellt, gelesen, fehlgeschlagen) und weicht bei dauerhaftem Fehlschlag automatisch auf E-Mail aus. | KANN |
| FA-I-128 | Fehlen die für einen Kanal nötigen Kontaktdaten (keine E-Mail-Adresse bzw. keine Telefonnummer), wird die Sendung nicht stillschweigend verworfen, sondern als *nicht zustellbar* mit Begründung angezeigt; der Betreiber wird darauf hingewiesen. | MUSS-P2 |
| FA-I-129 | Buchungen aus Portalimporten enthalten in der Regel keine Kontaktdaten (siehe FA-I-49). Das System weist bei solchen Buchungen deutlich darauf hin, dass die Nachrichtenstrecke erst nach manueller Ergänzung von E-Mail-Adresse oder Telefonnummer greift. | MUSS-P2 |
| FA-I-130 | Ein Sendeprotokoll führt je Nachricht: Zeitpunkt, Empfänger, Kanal, Regel, verwendete Sprache, versandter Inhalt im Wortlaut, Zustellstatus und etwaige Fehlermeldung. Das Protokoll ist an der Buchung und am Gast einsehbar. | MUSS-P2 |
| FA-I-131 | Nicht zustellbare E-Mails (Bounces) und Beschwerden werden erfasst; die betroffene Adresse wird für weitere automatische Nachrichten gesperrt und dem Betreiber gemeldet. | SOLL |
| FA-I-132 | Ein Widerspruch des Gastes (Abmeldelink, FA-G-48) unterbindet alle weiteren Nachrichten der Strecke für diese Person. Unmittelbar buchungsbezogene Mitteilungen wie eine Anfragebestätigung oder eine Terminänderung bleiben davon unberührt. | MUSS-P2 |
| FA-I-133 | Der Betreiber kann eine Nachricht aus einer Vorlage jederzeit ad hoc an einen einzelnen Gast senden, unabhängig von der Strecke. | SOLL |
| FA-I-134 | Auf dem Dashboard erscheinen die in den nächsten 24 Stunden fälligen Sendungen sowie alle fehlgeschlagenen Sendungen. | MUSS-P2 |
| FA-I-135 | Bleibt der Versand über eine konfigurierbare Frist gestört (Ausfall des Versanddienstes, wiederholte Fehler), wird der Betreiber gesondert benachrichtigt. | MUSS-P2 |
| FA-I-136 | Nachrichten können Anhänge in Form von Links auf Inhaltsseiten oder Dokumente enthalten. Dateianhänge im engeren Sinn sind nicht vorgesehen, um Zustellbarkeitsprobleme zu vermeiden. | SOLL |
| FA-I-137 | Eine Auswertung zeigt je Regel die Anzahl versandter Nachrichten, die Zustellquote und — sofern messbar — die Öffnungs- und Klickrate. | KANN |

*Prio-Kennzeichnung:* **MUSS-P2** bezeichnet Anforderungen, die für die Nachrichtenstrecke
zwingend sind, deren Umsetzung aber nach Phase 1 erfolgt (siehe Kapitel 10).

#### 6.11.3 Rahmenbedingungen für den WhatsApp-Versand

Diese Punkte sind keine Anforderungen, sondern Randbedingungen, die die Gestaltung
des Kanals bestimmen und bei der Entscheidung zu O-16 zu berücksichtigen sind.

- Automatisierter WhatsApp-Versand an Personen setzt die **WhatsApp Business Platform (Cloud API)** voraus. Dafür sind ein verifiziertes Meta-Unternehmenskonto, eine dedizierte Telefonnummer und die Nutzung über einen Anbieter oder direkt bei Meta erforderlich.
- Nachrichten, die außerhalb eines laufenden Gesprächs versandt werden — und das ist bei einer terminierten Strecke immer der Fall — müssen **vorab genehmigte Vorlagen** verwenden. Freier Text ist nur innerhalb eines vom Gast eröffneten Gesprächsfensters zulässig. Genehmigungen können abgelehnt werden und benötigen Vorlauf.
- Der Versand ist **kostenpflichtig**, abgerechnet je Gespräch bzw. Nachricht und abhängig vom Land des Empfängers.
- Es ist eine **nachweisbare Einwilligung** des Gastes erforderlich, über WhatsApp kontaktiert zu werden.
- Die halbautomatische Variante (E-12, FA-I-125) unterliegt keiner dieser Einschränkungen, da der Betreiber die Nachricht selbst aus seinem privaten oder geschäftlichen WhatsApp-Konto versendet. Sie kostet pro Buchung wenige Sekunden manuellen Aufwand.

---

## 7. Datenmodell (fachlich)

Die folgende Übersicht beschreibt die fachlichen Entitäten. Technische Attribute
(Schlüssel, Zeitstempel, Löschkennzeichen) sind nicht aufgeführt.

| Entität | Wesentliche Attribute | Beziehungen |
|---|---|---|
| **Objekt** | Bezeichnung, Adresse, Koordinaten, Kapazität, Check-in/-out, Registriernummer (AMA), Standardwährung | 1:n zu nahezu allen übrigen Entitäten |
| **Merkmal** | Schlüssel, Bezeichnung (mehrsprachig), Gruppe, Symbol | n:m zu Objekt |
| **Kanal** | Name, Typ, Farbe, iCal-Import-URL, Export-Token, Intervall, letzter Lauf, letzter Fehler | n:1 Objekt |
| **Buchung** | Anreise, Abreise, Status, Herkunft, Personenzahl, Kinder/Alter, Haustiere, Gesamtpreis, Anzahlung, Notiz, externe UID | n:1 Objekt, n:1 Kanal, n:1 Gast |
| **Sperrung** | Zeitraum, Grund, Notiz | n:1 Objekt |
| **Anfrage** | Zeitraum, Personen, Kontaktangaben, Sprache, Nachricht, errechneter Richtpreis, Status, Zustimmungsnachweis | n:1 Objekt, 0:1 Buchung |
| **Gast** | Name, E-Mail, Telefon, WhatsApp-Nummer, bevorzugter Kanal, Land, Sprache, Einwilligungen je Kanal mit Zeitstempel und Herkunft, Widerspruchskennzeichen, Sperrkennzeichen (Bounce/Beschwerde), Notiz | 1:n Buchungen/Anfragen, 1:n Sendungen |
| **Saison** | Bezeichnung, Zeitraum, Nächtepreis, Mindestaufenthalt, Anreiseregel | n:1 Objekt |
| **Tagespreis-Ausnahme** | Datum, Preis, Mindestaufenthalt | n:1 Objekt |
| **Entgelt** | Typ (Pauschale/pro Nacht/pro Person/pro Aufenthalt), Betrag, Bedingung, steuerliche Kennzeichnung | n:1 Objekt |
| **Rabattregel** | Typ, Schwellwert, Höhe, Gültigkeitszeitraum | n:1 Objekt |
| **Dienstleister** | Name, Gewerk, Kontakt, bevorzugter Kanal, Sprache, Konditionen | n:1 Objekt (oder objektübergreifend) |
| **Aufgabe** | Titel, Beschreibung, Gewerk, Fälligkeit, Status, Priorität, Kosten, Herkunft (manuell/aus Buchung/wiederkehrend) | n:1 Objekt, n:1 Dienstleister, 0:1 Buchung |
| **Aufgabenregel** | Auslöser (Abreise/Anreise/Intervall), Vorlauf, Vorlage, Standard-Dienstleister | n:1 Objekt |
| **Mangel** | Beschreibung, Ort, Dringlichkeit, Bild, Status | n:1 Objekt, 0:1 Aufgabe |
| **POI** | Name, Kategorie, Koordinaten, Adresse, Beschreibung (mehrsprachig), Öffnungszeiten, Kontakt, Website, Status, Quelle (intern/Gastvorschlag), Einreicherdaten, Hervorhebung, Sortierung | n:1 Objekt oder Region, n:1 Kategorie |
| **POI-Kategorie** | Schlüssel, Bezeichnung (mehrsprachig), Symbol, Farbe | 1:n POI |
| **Inhaltsseite** | Schlüssel, Titel und Text je Sprache, Typ, Veröffentlichungsstatus | n:1 Objekt |
| **Medium** | Typ (Bild/Video), Datei bzw. externe URL, Alternativtext je Sprache, Kategorie, Sortierung | n:1 Objekt |
| **Benutzer** | Name, E-Mail, Rolle, Passwort-Hash, TOTP-Geheimnis, Status | — |
| **Nachrichtenregel** | Bezeichnung, Bezugspunkt, Versatz in Tagen, Versandzeit, Kanal, Bedingungen, aktiv/inaktiv, Sortierung | n:1 Objekt, 1:n Vorlagen, 1:n Sendungen |
| **Nachrichtenvorlage** | Sprache, Betreff, Inhalt, verwendete Platzhalter, Kanal, Status; bei WhatsApp zusätzlich Vorlagenname, Kategorie und Parameterliste des Anbieters | n:1 Nachrichtenregel |
| **Geplante Sendung** | Soll-Versandzeitpunkt, Kanal, Empfängeradresse bzw. -nummer, Sprache, Status (*geplant*, *freizugeben*, *versandt*, *fehlgeschlagen*, *übersprungen*, *entfallen*, *nicht zustellbar*), Versuchszähler, erzeugter Inhalt, Sperrschlüssel gegen Doppelversand | n:1 Nachrichtenregel, n:1 Buchung, n:1 Gast |
| **Nachrichtenprotokoll** | Empfänger, Kanal, Betreff, Zeitpunkt, Vorlage, versandter Inhalt im Wortlaut, Zustellstatus, Fehlermeldung, Auslöser (automatisch/manuell) | n:1 Anfrage/Buchung/Aufgabe/Sendung |
| **Änderungsprotokoll** | Benutzer, Zeitpunkt, Entität, Aktion, Vorher/Nachher | — |

---

## 8. Externe Schnittstellen

| Nr. | Schnittstelle | Richtung | Zweck | Anmerkung |
|---|---|---|---|---|
| S-1 | iCal-Import (Booking.com, Airbnb, weitere) | eingehend | Belegungszeiträume übernehmen | Portalseitige Aktualisierung typischerweise nicht in Echtzeit; Restrisiko dokumentiert (FA-I-49) |
| S-2 | iCal-Export | ausgehend | Gesamtbelegung an Portale melden | Tokengeschützte URL, keine personenbezogenen Daten |
| S-3 | E-Mail-Versand (SMTP oder Transaktionsdienst) | ausgehend | Bestätigungen, Benachrichtigungen, Aufgabenversand, Nachrichtenstrecke | SPF/DKIM/DMARC einzurichten; Rückmeldungen zu Zustellung und Bounces werden ausgewertet (FA-I-131) |
| S-3a | WhatsApp-Sendelink (`wa.me`) | ausgehend | Halbautomatischer Versand der Nachrichtenstrecke und von Aufgaben | Kein Vertrag, keine Kosten; Versand erfolgt durch den Betreiber (E-12) |
| S-3b | WhatsApp Business Cloud API | ein-/ausgehend | Vollautomatischer Versand, Zustellstatus | Spätere Ausbaustufe; setzt Unternehmensverifizierung, genehmigte Vorlagen und Einwilligung voraus (Kapitel 6.11.3) |
| S-4 | Kartendienst | ein-/ausgehend | Kartendarstellung, Adress-/Koordinatensuche | Über Adapter gekapselt (E-7) |
| S-5 | Videoplattform (YouTube/Vimeo) | ausgehend | Einbettung von Videos | Nur nach Einwilligung (FA-G-06) |
| S-6 | Google-Maps-Deeplink | ausgehend | Navigation zu POI | Reiner Link, keine Datenübertragung ohne Klick |
| S-7 | Captcha-/Bot-Schutzdienst | ein-/ausgehend | Missbrauchsschutz der Formulare | Datenschutzkonforme Auswahl erforderlich |
| S-8 | Zahlungsdienstleister | — | Anzahlungen | **Nicht Bestandteil** von Phase 1/2 (E-2) |

---

## 9. Nichtfunktionale Anforderungen

### 9.1 Leistung und Verfügbarkeit

| ID | Anforderung |
|---|---|
| NFA-01 | Öffentliche Seiten erreichen im Mobilfunk-Testprofil einen Largest Contentful Paint unter 2,5 Sekunden. |
| NFA-02 | Der Verfügbarkeitskalender und der Preisrechner antworten in unter 500 Millisekunden. |
| NFA-03 | Die Anwendung ist auf gleichzeitige Nutzung durch mindestens 50 Besucher ausgelegt. |
| NFA-04 | Angestrebte Verfügbarkeit: 99 % im Monatsmittel, geplante Wartungsfenster ausgenommen. |
| NFA-05 | Ein Ausfall des Kartendienstes oder der Videoplattform darf die übrigen Seiteninhalte nicht blockieren. |

### 9.2 Sicherheit

| ID | Anforderung |
|---|---|
| NFA-10 | Ausschließlich verschlüsselte Übertragung (HTTPS, HSTS). |
| NFA-11 | Passwörter werden mit einem aktuellen Verfahren (Argon2id oder bcrypt mit angemessenem Kostenfaktor) gespeichert. |
| NFA-12 | Alle öffentlichen Formulare unterliegen einer Ratenbegrenzung je IP und Zeitfenster. |
| NFA-13 | Schutz gegen die gängigen Angriffsklassen: SQL-Injection (parametrisierte Abfragen), Cross-Site-Scripting (Ausgabemaskierung, Content-Security-Policy), Cross-Site-Request-Forgery (Token), unsichere Dateiuploads (Typ- und Größenprüfung, Speicherung außerhalb des Ausführungspfads). |
| NFA-14 | Hochgeladene Bilder werden neu kodiert; die Originaldatei wird nicht unverändert ausgeliefert. |
| NFA-15 | Zugangsdaten und Schlüssel liegen ausschließlich in Umgebungsvariablen, niemals im Repository. |
| NFA-16 | Abhängigkeiten werden regelmäßig auf bekannte Schwachstellen geprüft. |

### 9.3 Datenschutz und Recht

| ID | Anforderung |
|---|---|
| NFA-20 | Verarbeitung nach DSGVO: Datenschutzerklärung in allen Sprachen, Rechtsgrundlagen je Verarbeitung dokumentiert, Verzeichnis von Verarbeitungstätigkeiten. |
| NFA-21 | Cookie-/Einwilligungsbanner mit granularer Auswahl; nicht notwendige Dienste (Karte eines externen Anbieters, Videoeinbettung, Statistik) laden erst nach Einwilligung. |
| NFA-22 | Auskunfts-, Berichtigungs- und Löschanträge sind mit vertretbarem Aufwand erfüllbar; Gastdaten sind exportierbar und löschbar. |
| NFA-23 | Löschfristen sind konfigurierbar: nicht weiterverfolgte Anfragen werden nach einer festgelegten Frist automatisch anonymisiert; Buchungsdaten bleiben so lange erhalten, wie steuerliche Aufbewahrungspflichten es verlangen. Sendungsprotokolle der Nachrichtenstrecke unterliegen der Frist der zugehörigen Buchung; nach Ablauf werden die Empfängerangaben anonymisiert, während die statistischen Kennzahlen erhalten bleiben. |
| NFA-24 | Impressum und Datenschutzerklärung sind von jeder Seite aus erreichbar. |
| NFA-25 | Die griechische Registriernummer (AMA) und weitere gesetzlich vorgeschriebene Angaben zur Kurzzeitvermietung werden auf der Gästeseite ausgewiesen. |
| NFA-26 | Anwendbare Melde- und Datenübermittlungspflichten für Kurzzeitvermietung (nationale Registrierung sowie einschlägige EU-Vorgaben zur Datenerhebung bei kurzfristiger Vermietung) sind vor Inbetriebnahme mit einem Steuer-/Rechtsberater in Griechenland zu prüfen; das System hält die dafür nötigen Datenfelder vor. |
| NFA-27 | Nutzergenerierte Inhalte (POI-Vorschläge) werden vor Veröffentlichung geprüft (FA-G-36), um Haftungsrisiken zu begrenzen. |
| NFA-28 | Nachrichten der Strecke, die der Durchführung des Aufenthalts dienen (M-1 bis M-4), stützen sich auf die Vertragserfüllung. Die Nachbereitungsnachricht mit Bewertungsbitte und Wiederbuchungsangebot (M-5) hat werblichen Charakter; ihre Rechtsgrundlage sowie die Zulässigkeit ohne gesonderte Einwilligung sind vor Inbetriebnahme zu prüfen (O-20). Jede Nachricht der Strecke enthält einen Abmeldelink (FA-G-48). |
| NFA-29 | Die Einwilligung zur Kontaktaufnahme über WhatsApp wird gesondert, nachweisbar und mit Zeitstempel erfasst; ohne sie erfolgt kein WhatsApp-Versand. |

### 9.4 Betrieb und Wartbarkeit

| ID | Anforderung |
|---|---|
| NFA-30 | Tägliches automatisiertes Datenbank-Backup mit mindestens 30 Tagen Aufbewahrung; die Wiederherstellung ist mindestens einmal erprobt zu dokumentieren. |
| NFA-31 | Hochgeladene Medien sind in das Backup einbezogen. |
| NFA-32 | Die Anwendung läuft containerisiert; eine Neuinstallation ist mit dokumentierten Schritten reproduzierbar. |
| NFA-33 | Datenbankschema-Änderungen erfolgen ausschließlich über versionierte Migrationen. |
| NFA-34 | Anwendungs- und Synchronisationsfehler werden protokolliert; kritische Fehler lösen eine Benachrichtigung aus. |
| NFA-35 | Die Codebasis ist typisiert (TypeScript) und wird durch automatisierte Prüfungen (Linting, Tests) abgesichert. Fachlogik für Preisberechnung, Verfügbarkeit und iCal-Verarbeitung ist durch Unit-Tests abgedeckt. |

### 9.5 Nutzbarkeit und Auffindbarkeit

| ID | Anforderung |
|---|---|
| NFA-40 | Mobile-First-Gestaltung; sämtliche Funktionen sind auf Smartphones bedienbar. |
| NFA-41 | Der interne Bereich ist auf Tablet und Smartphone nutzbar (Aufgaben und Belegung vor Ort). |
| NFA-42 | Suchmaschinenoptimierung: sprechende URLs, Meta-Angaben je Sprache, strukturierte Daten für Unterkünfte, XML-Sitemap, `hreflang`. |
| NFA-43 | Alle Seiten sind ohne aktiviertes JavaScript zumindest lesbar (Inhalte serverseitig gerendert). |

---

## 10. Umsetzungsphasen

### Phase 1 — MVP (produktiv nutzbar)

- Objektstammdaten, Merkmale, Check-in-Regeln
- Gästeseite: Startseite, Hausbeschreibung, Ausstattung, Galerie, Begrüßungsvideo
- Belegungskalender (öffentlich), Saisonpreistabelle, Preisrechner
- Anfrageformular mit Missbrauchsschutz, Bestätigungs- und Benachrichtigungs-E-Mails
- Interner Bereich: Login mit zweitem Faktor, Dashboard, Buchungs- und Anfrageverwaltung, Sperrungen
- iCal-Import und -Export inklusive Konflikterkennung und Fehlerbenachrichtigung
- Preis- und Saisonverwaltung
- POI: Karte, Liste, Detailansicht, Gastvorschlag mit Freigabe-Workflow, vollständige Bearbeitung intern
- Informationsseiten inklusive Notfall- und Versorgungsübersicht
- Sprachen Deutsch, Griechisch, Englisch
- Rechtstexte, Einwilligungsbanner, Backup, Deployment

### Phase 2 — Betriebsunterstützung

- **Nachrichtenstrecke (Kapitel 6.11):** Zeitsteuerung, Nachrichtenregeln, mehrsprachige Vorlagen mit Platzhaltern, geplante Sendungen mit Vorschau und Eingriffsmöglichkeit, Sendeprotokoll, Ruhezeiten, Freigabemodus und Notaus, Abmeldelink und Einwilligungsverwaltung — vollautomatisch per E-Mail, halbautomatisch per WhatsApp-Sendelink
- Dienstleisterverwaltung, Aufgaben, automatische Aufgabenerzeugung aus Buchungen
- Wiederkehrende Aufgaben, Aufgabenkalender, Aufgabenversand per E-Mail/Messenger-Link
- Mängel- und Schadensregister
- Textvorlagen, Kommunikationsprotokoll, Erinnerungen an unbearbeitete Anfragen
- Rabattregeln, Tagespreis-Ausnahmen, Preisvorschau
- Personalisierter Aufenthaltslink für bestätigte Gäste, FAQ
- Sprachen Italienisch und Französisch
- Mehrsprachige POI-Beschreibungen mit Übersetzungsstand

### Phase 3 — Ausbau

- Auswertungen und Kennzahlen, CSV-Export, Kostenerfassung, Zählerstände
- Inventar- und Verbrauchsmaterialverwaltung, Fristenliste
- Mehrobjekt-Oberfläche mit Objektumschalter
- Bewertungen und Kommentare zu POI mit Freigabe
- PDF-Prospektexport
- Vollautomatischer WhatsApp-Versand über die Business Cloud API inklusive Zustellstatus und Ausweichen auf E-Mail (FA-I-127), Auswertung der Nachrichtenstrecke (FA-I-137)
- Optional: Anzahlung per Zahlungslink (setzt Klärung von Steuer- und Rechtsfragen voraus)

> **Hinweis zur Priorisierung:** Die Nachrichtenstrecke setzt technisch nur Buchungsdaten,
> Vorlagen und E-Mail-Versand voraus — alles Bestandteile von Phase 1. Sie lässt sich daher
> auf Wunsch ganz oder teilweise (etwa nur die Anreisenachricht M-3) in Phase 1 vorziehen.
> Empfohlen wird, mit M-3 und M-4 zu beginnen, da diese den größten Teil der wiederkehrenden
> Rückfragen abfangen.

---

## 11. Abnahmekriterien (Phase 1)

| Nr. | Kriterium |
|---|---|
| AK-1 | Eine im Testkalender von Booking.com und Airbnb angelegte Belegung erscheint nach spätestens einem Synchronisationslauf im internen Kalender und blockiert den Zeitraum auf der Gästeseite. |
| AK-2 | Der Export-Kalender lässt sich in beiden Portalen erfolgreich abonnieren und zeigt dort alle Belegungen. |
| AK-3 | Ein saisonübergreifender Testzeitraum ergibt im Preisrechner exakt den Betrag der manuellen Vergleichsrechnung, inklusive Entgelten und Abgaben. |
| AK-4 | Eine über die Gästeseite gesendete Anfrage erzeugt einen Eintrag im internen Bereich, eine Eingangsbestätigung an den Gast und eine Benachrichtigung an den Betreiber. |
| AK-5 | Ein anonym eingereichter POI ist auf der Gästeseite erst nach Freigabe sichtbar und kann intern bearbeitet, abgelehnt und gelöscht werden. |
| AK-6 | Alle Seiten der Gästeseite sind in Deutsch, Griechisch und Englisch vollständig übersetzt und über den Sprachumschalter erreichbar. |
| AK-7 | Der interne Bereich ist ohne gültige Anmeldung inklusive zweitem Faktor nicht erreichbar. |
| AK-8 | Eine Wiederherstellung aus dem Backup wurde erfolgreich durchgeführt und protokolliert. |
| AK-9 | Ein Zugänglichkeitstest (automatisiert und stichprobenartig manuell) weist keine Verstöße gegen WCAG 2.2 AA auf den Hauptseiten aus. |
| AK-10 | Eine Doppelbelegung durch zwei Kanäle wird als Konflikt erkannt, angezeigt und gemeldet. |

### Abnahmekriterien Nachrichtenstrecke (Phase 2)

| Nr. | Kriterium |
|---|---|
| AK-11 | Für eine neu bestätigte Testbuchung werden alle fünf Sendungen der Standardstrecke mit korrekt berechneten Zeitpunkten in Ortszeit des Objekts erzeugt und in der Übersicht angezeigt. |
| AK-12 | Eine Verschiebung des Buchungszeitraums terminiert alle offenen Sendungen neu; eine Stornierung bricht sie ab. Bereits versandte Nachrichten bleiben unverändert protokolliert. |
| AK-13 | Eine Testbuchung mit griechischer Gastsprache erhält alle Nachrichten auf Griechisch mit korrekt ersetzten Platzhaltern; fehlt eine Sprachfassung, greift nachweislich die Fallback-Sprache. |
| AK-14 | Ein wiederholt ausgelöster Versandlauf sowie ein Neustart der Anwendung während eines Laufs führen zu keiner doppelt versandten Nachricht. |
| AK-15 | Eine auf 22:00 Uhr fallende Sendung wird gemäß Ruhezeitregel auf den nächsten zulässigen Zeitpunkt verschoben. |
| AK-16 | Ein Klick auf den Abmeldelink unterbindet alle weiteren Nachrichten der Strecke für diesen Gast; eine anschließend ausgelöste Terminänderungsmitteilung erreicht ihn dennoch. |
| AK-17 | Eine über iCal importierte Buchung ohne Kontaktdaten erzeugt keine stillschweigend verworfenen Sendungen, sondern einen sichtbaren Hinweis auf fehlende Kontaktdaten. |
| AK-18 | Eine fällige WhatsApp-Nachricht erscheint mit fertigem Text und funktionierendem Sendelink; nach dem Versand lässt sie sich als erledigt bestätigen und ist im Protokoll nachvollziehbar. |

---

## 12. Offene Punkte

| Nr. | Frage | Auswirkung |
|---|---|---|
| O-1 | Wie lauten Standort, Adresse und Koordinaten des Hauses, und wie ist der genaue Objektname für Domain und Titel? | Stammdaten, Domainwahl, SEO |
| O-2 | Welche Portale werden aktuell tatsächlich genutzt, und liegen bereits iCal-Adressen vor? Sollen griechische Portale ergänzt werden? | Kanalkonfiguration, Aufwand |
| O-3 | Wie sehen die aktuellen Saisonpreise, Mindestaufenthalte, Endreinigungspauschale, Kaution und Anreiseregeln aus? | Preisverwaltung, Preisrechner |
| O-4 | Welche gesetzliche Abgabe ist je Nacht bzw. je Aufenthalt auszuweisen, und in welcher Höhe? Wird sie vor Ort oder vorab erhoben? | Preisdarstellung, Rechtskonformität |
| O-5 | Liegt die griechische Registriernummer (AMA) vor, und gibt es weitere Pflichtangaben für Inserate? | NFA-25, Gästeseite |
| O-6 | Sollen POI global (regional) oder je Objekt geführt werden, wenn später ein zweites Haus in derselben Region hinzukommt? | Datenmodell |
| O-7 | Existieren bereits Fotos, Videos und Texte in ausreichender Qualität, oder ist eine Inhaltsproduktion einzuplanen? | Zeitplan, Aufwand |
| O-8 | Wer erstellt die Übersetzungen (professionell, maschinell mit Korrektur, eigene Kenntnisse)? Insbesondere Griechisch, Italienisch, Französisch. | Qualität, Kosten, Zeitplan |
| O-9 | Welche Domain(s) sollen verwendet werden, und existieren sie bereits? Eine Domain je Sprache oder eine gemeinsame Domain mit Sprachpfaden (Empfehlung: gemeinsam)? | Betrieb, SEO |
| O-10 | Welcher E-Mail-Absender und welcher Versanddienst sollen genutzt werden? Ist die Domain für SPF/DKIM/DMARC konfigurierbar? | Zustellbarkeit |
| O-11 | Wird eine separate Testumgebung gewünscht, oder genügt lokale Entwicklung plus Produktion? | Betriebsaufwand, Kosten |
| O-12 | Sollen bestehende Buchungen und Gästedaten aus der bisherigen Verwaltung übernommen werden, und in welcher Form liegen sie vor? | Migrationsaufwand |
| O-13 | Gibt es ein Zieldatum, etwa den Start der Saison, an dem Phase 1 produktiv sein muss? | Zeitplan, Priorisierung |
| O-14 | Soll ein zweiter Benutzer (Rolle Manager) von Beginn an eingerichtet werden? | Rechteverwaltung |
| O-15 | Wie hoch ist das Budget für laufende Dienste (Karten-API, E-Mail-Versand, Bot-Schutz, Hosting)? Davon hängt die Entscheidung aus E-7 ab. | Anbieterwahl |
| O-16 | Soll WhatsApp halbautomatisch bleiben (Sendelink, kostenfrei, wenige Sekunden Aufwand je Nachricht) oder über die Business Cloud API vollautomatisch laufen (Unternehmensverifizierung, genehmigte Vorlagen, Kosten je Gespräch)? | Kanalumsetzung, Kosten, Aufwand |
| O-17 | Welche Absenderidentität soll für WhatsApp genutzt werden — die private Nummer, eine separate Nummer für die Vermietung? Bei der Cloud API wird eine eigene, nicht anderweitig in WhatsApp genutzte Nummer benötigt. | Einrichtung, Erreichbarkeit |
| O-18 | Sind die vorgeschlagenen Zeitpunkte der Standardstrecke (14 Tage, 7 Tage, Anreisetag, 1 Tag vor Abreise, 7 Tage nach Abreise) so gewünscht, und zu welcher Uhrzeit sollen die Nachrichten versandt werden? | Konfiguration der Regeln |
| O-19 | Welche Inhalte sollen die fünf Nachrichten konkret enthalten — insbesondere, ob Zugangscode und WLAN-Zugang per Nachricht versandt werden dürfen oder nur über den persönlichen Aufenthaltslink? | Vorlagen, Sicherheit |
| O-20 | Darf die Nachbereitungsnachricht (M-5) mit Bewertungsbitte und Wiederbuchungsangebot ohne gesonderte Einwilligung versandt werden? Dies ist werbliche Kommunikation und mit dem Rechtsberater zu klären (NFA-28). | Rechtskonformität |
| O-21 | Sollen Gäste aus Portalbuchungen in die Strecke einbezogen werden? Das setzt voraus, dass Kontaktdaten manuell nachgetragen werden, und die Nutzungsbedingungen der Portale zur Direktkontaktaufnahme sind zu beachten. | Reichweite der Strecke, Portalregeln |

---

## 13. Risiken

| Nr. | Risiko | Bewertung | Gegenmaßnahme |
|---|---|---|---|
| R-1 | Overbooking durch verzögerte iCal-Synchronisation | mittel / hoch | Kurzes Synchronisationsintervall, Konflikterkennung mit sofortiger Meldung, Hinweis im Anfrageprozess auf Bestätigungsvorbehalt |
| R-2 | Spam und unpassende Inhalte in POI-Vorschlägen | hoch / gering | Durchgängige Freigabepflicht, Bot-Schutz, Absendersperre |
| R-3 | Rechtliche Anforderungen in Griechenland unvollständig erfasst | mittel / hoch | Prüfung durch lokalen Steuer-/Rechtsberater vor Inbetriebnahme (NFA-26) |
| R-4 | Pflegeaufwand für fünf Sprachfassungen | hoch / mittel | Übersetzungsstand je Inhalt sichtbar, Fallback-Sprache, gestaffelte Einführung (Phase 1: drei Sprachen) |
| R-5 | Betriebskosten externer Dienste steigen unerwartet | gering / mittel | Kartenanbieter über Adapter austauschbar, kostenlose Alternative verfügbar |
| R-6 | Ressourcengrenzen der kleinen Serverinstanz | mittel / mittel | Videos extern, Bilder vorskaliert, Zwischenspeicherung von Kalender- und Preisabfragen, Überwachung |
| R-7 | Datenverlust | gering / hoch | Tägliche Backups, erprobte Wiederherstellung (NFA-30, AK-8) |
| R-8 | Fehlerhafte oder doppelte Nachrichten erreichen Gäste und wirken unprofessionell | mittel / mittel | Vorschau und Testversand vor Aktivierung, Freigabemodus für den Anlauf, Einmaligkeitssicherung (FA-I-122), Notaus (FA-I-124) |
| R-9 | Portalbuchungen tragen keine Kontaktdaten, die Strecke greift dort nicht | hoch / mittel | Sichtbarer Hinweis an der Buchung (FA-I-129), manuelles Nachtragen, Fokus der Strecke auf Direktbuchungen — was zugleich Ziel Z-2 unterstützt |
| R-10 | WhatsApp-Vorlagen werden nicht genehmigt oder Kosten und Auflagen der Cloud API stehen in keinem Verhältnis zum Nutzen | mittel / gering | Halbautomatischer Betrieb als vollwertiger Ausgangszustand (E-12); Kanal gekapselt, Wechsel jederzeit ohne Änderung von Regeln und Vorlagen möglich (FA-I-126) |
| R-11 | Automatische Nachrichten werden als Werbung eingestuft oder landen im Spam-Ordner | mittel / mittel | SPF/DKIM/DMARC, Abmeldelink in jeder Nachricht, Bounce- und Beschwerdeauswertung (FA-I-131), rechtliche Klärung der werblichen Nachricht (O-20) |

---

## 14. Glossar

| Begriff | Bedeutung |
|---|---|
| **iCal** | Standardformat für Kalenderdaten (RFC 5545); von Buchungsportalen zum Austausch von Belegungszeiträumen unterstützt |
| **POI** | Point of Interest — Empfehlung in der Umgebung (Restaurant, Strand, Sehenswürdigkeit, Versorgungseinrichtung) |
| **Kanal** | Vertriebsweg für Buchungen (eigene Website, Booking.com, Airbnb, sonstige Portale) |
| **AMA** | Αριθμός Μητρώου Ακινήτου — griechische Registriernummer für Kurzzeitvermietung |
| **Mandantenfähig** | Datenmodell, das mehrere Objekte getrennt verwalten kann |
| **MVP** | Minimum Viable Product — kleinster produktiv nutzbarer Funktionsumfang |
| **WCAG 2.2 AA** | Internationale Richtlinie für barrierefreie Webinhalte, Konformitätsstufe AA |
| **TOTP** | Zeitbasiertes Einmalpasswort als zweiter Anmeldefaktor |
| **Nachrichtenstrecke** | Folge automatisch terminierter Nachrichten, die sich an den Daten einer Buchung ausrichtet (Kapitel 6.11) |
| **Nachrichtenregel** | Vorschrift, wann und über welchen Kanal eine bestimmte Nachricht einer Strecke versandt wird |
| **Geplante Sendung** | Konkrete, aus einer Regel und einer Buchung erzeugte Nachricht mit festem Versandzeitpunkt |
| **Platzhalter** | Markierung in einer Vorlage, die beim Versand durch einen konkreten Wert ersetzt wird (z. B. Gastname, Anreisedatum) |
| **WhatsApp Business Cloud API** | Offizielle Schnittstelle von Meta für den automatisierten WhatsApp-Versand an Kunden |
| **Genehmigte Vorlage** | Von Meta vorab freigegebener Nachrichtentext, ohne den außerhalb eines laufenden Gesprächs kein WhatsApp-Versand möglich ist |
| **Bounce** | Rückläufer einer nicht zustellbaren E-Mail |
