TEMPLATES_EC = {
            "iM2641902_1_0": """Bewertungskriterien
Korrekt (TRUE), wenn:
- Eine Zeitdauer angegeben wird, die höchstens 250 Tage beträgt,

Beispiele für richtige Lösungen:
- 100 ml : 0,4 ml/Tag = 250 Tage
- 166 UND 100 : 0,6 ≈ 166
- 100 ml : 2ml/Tag = 50 Tage
- 50 UND 10 mal 0,2 = 2 ml/Tag

Beispiele für falsche Lösungen:
- Es kommt ja drauf an wie groß sie parfüm flasche ist
- 1+1=3
""",
            "iM2641903_1_0": """Bewertungskriterien
Korrekt (TRUE), wenn:
- Ergibnis 0,30

Beispiele für richtige Lösungen:
- 75 € / 50 ml = x / 0,2 ml → x = 0,30 €
- 50 ml kosten 75 €. 1 ml kostet 1,50 €. 0,2 ml kosten 0,30 €.

Beispiele für falsche Lösungen:
- 2 mal 50 geteilt durch 75 sind 1,33
- ich habe in den taschenrechner so lange 50ml*x eingegeben bis ich auf 75 kam
- 75 geteilt durch 50 ergeben 1,50 Euro pro Pumpstoß
""",
            "iM2672802": """Bewertungskriterien
Korrekt (TRUE), wenn:
- Eine natürliche Zahl aus dem Intervall [6; 12] ODER Ein ganzzahliges Intervall aus dem Intervall [6; 12] 
- UND Lösungsweg, mit der Annahme über das durchschnittliche Gewicht einer Person. 
- Das Gesamtgewicht aller dieser Personen darf die maximale Belastung von 600 kg nicht überschreiten.

Falsch (FALSE), wenn:
- Alle anderen Antworten, die zur Überschreitung von 600 kg führen.
- ODER keine realistische Annahme für das Durchschnittsgewicht getroffen wird,

Beispiele für richtige Lösungen:
- Wenn jede Person 60 kg wiegt, dürfen 10 Personen den Fahrstuhl gleichzeitig  benutzen, da 10 mal 60kg = 600kg.
- Wenn 8 Personen ein durchschnittliches Gewicht von 70 kg haben, dürfen sie gleichzeitig den Fahrstuhl benutzen, da dann 600 kg nicht überschritten werden.
- 7 UND Ein Erwachsener wiegt etwa 80 kg.
- 600kg: 60kg = 10

Beispiele für falsche Lösungen:
- 8 UND Annahme Erwachsener wiegt ca. 80 kg (640 kg > 600 kg)
- ["8","ein erwachsener ca. 70-80kg 70*600= 560 80*600= 640"]
- ["6","6 Personen x 99kg = 594kg"]
""",
            "iM2700801_1_0": """Bewertungskriterien
Korrekt (TRUE), wenn:
- Zahl aus dem Intervall [30; 80]

Beispiele für richtige Lösungen:
- Daumen (5 cm), Kunstwerk (2 m), 40-mal so hoch
- 220 cm : 4 cm = 55

Beispiele für falsche Lösungen:
- wenn die Frau bis zur Hälfte von dem Daumen geht das ist dr Daumen doppelt so groß wie die Frau
- ein menschlicher daumen ist ungefähr 9,5 cm lang und der Kunst daumen ist mindestens 2,5 - 3 Meter
""",
        "iM2702701": """Bewertungskriterien
Korrekt (TRUE), wenn:
- Zahl aus dem Intervall [50000; 110000] 
- UND nachvollziehbare Modellierung.

Falsch (FALSE), wenn:
- Alle anderen Antworten ohne nachvollziehbare Modellierung.

Beispiele für richtige Lösungen:
- Fünf Päckchen Papier pro Karton; 31 Kartons; Insgesamt also 31 mal 5 + 1 Papierpäckchen mit je 500 Blatt; Also 156 mal 500 = 78000 Blatt Papier
- 64000 UND Pro Karton 2000 Blätter und dann alle Kartons zusammenrechnen.

Beispiele für falsche Lösungen:
- ["77500","Nö ._."]
""",
    "iM4620701_0": """Bewertungskriterien
Korrekt (TRUE), wenn:
- Exakte Funktionsgleichung y = 3x + 2

Beispiele für richtige Lösungen:
- y = 3x + 2
- x*3+2
- x*3Eu.+2Eu.

Beispiele für falsche Lösungen:
- x+Die Karte
- m*x
""",
    "iM4620702_0_1": """Bewertungskriterien
Korrekt (TRUE), wenn:
- Die Antwort inhaltlich zum Ausdruck bringt, dass sich der Preis nicht verdoppelt.

Beispiele für richtige Lösungen:
- Nein weil er ja auch nicht die doppelte anzahl an karten nimmt wie frau alfonso.
- Weil es der doppelte preis wäre da es die doppelte anzahl der Rosen sind.
- Weil er eine gemeinsame Glückwunschkarte kauft und somit verdoppelt der Preis sich nicht.

Beispiele für falsche Lösungen:
- Der Preis verdoppelt sich,weil die Rosen mehr werden und dadurch auch mehr kosten. Genauso mit der Glückwunschkarte.
- die rose kostet 3€ herr Meier verdoppelt es und die karte wollen auch beide haben
""",
    "iM4640402_0": """Bewertungskriterien
Korrekt (TRUE), wenn:
- Angabe einer Gleichung mit unendlich vielen Lösungen.

Falsch (FALSE), wenn:
- Jede Gleichung mit endlicher Lösungsmenge

Beispiele für richtige Lösungen:
- x + 2 = x + 2

Beispiele für falsche Lösungen:
- x = x:x
- x=unendlich
""",
    "iM5662901_0": """Bewertungskriterien

Korrekt (TRUE), wenn:
- Ergebniss: 1 /24

Beispiele für richtige Lösungen:
- 1/24
- 1 zu 24
- 4,2%

Beispiele für falsche Lösungen:
- die schüler/in bekommen die geschenke nach dem Wochenende
- 1/48
- zu 50% weill man sammstags und sonntags am montag macht und da 3 kinder gezogen werden
"""
}


# ===================================================================================================================================================


Evaluation_hinweise = """
Hinweise zur Bewertung:

Wenn das Endergebnis aufgrund kleiner Rundungsfehler leicht abweicht, gilt es trotzdem als korrekt.
Wenn der Lösungsweg korrekt ist, aber das Endergebnis fehlt oder Tippfehler enthält, kann trotzdem TRUE vergeben werden.
Sei tolerant bei Schreibweisen, Rundungen und Darstellungsformen.

"""