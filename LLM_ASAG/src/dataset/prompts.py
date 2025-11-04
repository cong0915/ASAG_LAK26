TEMPLATES_zeroshot = {
            "iM2641902_1_0": """T: {s_text}
Q: {s_question}
A: {s_input}
R:
""",
            "iM2641903_1_0": """T: {s_text}
Q: {s_question}
A: {s_input}
R:
""",
            "iM2672802": """T: {s_text}
Q: {s_question}
A: {s_input}
R:
""",
            "iM2700801_1_0": """T: {s_text}
Q: {s_question}
A: {s_input}
R:
""",
            "iM2702701": """T: {s_text}
Q: {s_question}
A: {s_input}
R:
""",
            "iM4620701_0": """T: {s_text}
Q: {s_question}
A: {s_input}
R:
""",
            "iM4620702_0_1": """T: {s_text}
Q: {s_question}
A: {s_input}
R: 
""",
            "iM4640402_0": """T: {s_text}
Q: {s_question}
A: {s_input}
R:
""",
            "iM5662901_0": """T: {s_text}
Q: {s_question}
A: {s_input}
R:
"""
}

# ===================================================================================================================================================

TEMPLATES_fewshot = {
            "iM2641902_1_0": """T: {s_text}
Q: {s_question}
A: Es kommt ja drauf an wie groß sie parfüm flasche ist
R: false
A: 100ml :5= 20
R: true
A: 1+1=3
R: false
A: 0,6x160
R: true
A: wenn sie 3 pumstößenimmt reicht das parfüm für 167 tage weil jeden tag 0.6 ml verwendet werden bei drei pumpstößen
R: true
A: {s_input}
R:
""",
            "iM2641903_1_0": """T: {s_text}
Q: {s_question}
A: 2 mal 50 geteilt durch 75 sind 1,33
R: false
A: 1ml = 1,50 : 5 = 0,2ml =0,30 ct
R: true
A: ich habe in den taschenrechner so lange 50ml*x eingegeben bis ich auf 75 kam
R: false
A: 75 geteilt durch 50 ergeben 1,50 Euro pro Pumpstoß
R: false
A: 50/0,2=250 und dann 75/250=0,3
R: true
A: {s_input}
R:
""",
            "iM2672802": """T: {s_text}
Q: {s_question}
A: ["7-9","600kg/70=8,57"]
R: true 
A: ["8","ein erwachsener ca. 70-80kg 70*600= 560 80*600= 640"]
R: false
A: ["7","1 Erwachsener= ca. 80 kg 80kgx 7= 580kg"]
R: true
A: ["6","6 Personen x 99kg = 594kg"]
R: false
A: ["7","ich schätze das ein durchschnittlicher erwachsener ungefähr 80kg wieckt und bei 7 personen sind es 560 kg also wären 8zu viel gewicht"]
R: true
A: {s_input}
R:
""",
            "iM2700801_1_0": """T: {s_text}
Q: {s_question}
A: wenn die Frau bis zur Hälfte von dem Daumen geht das ist dr Daumen doppelt so groß wie die Frau
R: false
A: Wenn das Kunstwerk 3,5 meter hoch ist und Ellis daumen 5 cm ist, dann würde das kunstwerk 70 mal länger sein als ihr daumen.
R: true
A: ich habe geschätzt wie lang ihr daumen ist (0,1) und dan (Länge der staute) 5,58 durch 0,1 gerechnet bin auf das ergebnis 55,8
R: true
A: ein menschlicher daumen ist ungefähr 9,5 cm lang und der Kunst daumen ist mindestens 2,5 - 3 Meter
R: false
A: Ein Daumen ist ca. 5cm lang, ich schätze mal das das Kunstwerk 2m hoch ist. in 2m passen also 40 Daumen.
R: true
A: {s_input}
R:
""",
            "iM2702701": """T: {s_text}
Q: {s_question}
A: ["78000","Es sind 31 Kartons mit ungefähr 5 Paketen wo 500 Blätter drin sind. ich rechne zuerst 31*5 was 155 ist dann rechne ich die 155*500 was 77500 ist plus das eine\nfreiliegende Paket mit 500 blättern ergibt dann 78000"]
R: true
A: ["62500","ich habe geschätzt wie fiele pläter in einen kartong pasen (2000) dann habe ich die kartongs gezählt 31 und dan plus 500 wegen den Psket"]
R: true
A: ["77500","Nö ._."]
R: false 
A: ["62000","In eine Karton sind 4 Pakete Blätter also in in einen Karton 2000 Blätter. Es sind 31 Kartons also 31x2000=62000.Es sind 62000 Blätter"]
R: false
A: ["62500","31 Kisten mit jeweils 4 Paketen + 1 Paket (31x4x)500 +500"]
R: true
A: {s_input}
R:
""",
            "iM4620701_0": """T: {s_text}
Q: {s_question}
A: x+Die Karte
R: false
A: m*x
R: false
A: x*3+2
R: true
A: x*3Eu.+2Eu.
R: true
A: 2€+(x+2)
R: false
A: {s_input}
R:
""",
            "iM4620702_0_1": """T: {s_text}
Q: {s_question}
A: Nein weil er ja auch nicht die doppelte anzahl an karten nimmt wie frau alfonso.
R: true
A: Der Preis verdoppelt sich,weil die Rosen mehr werden und dadurch auch mehr kosten . Genauso mit der Glückwunschkarte.
R: false
A: Weil es der doppelte preis wäre da es die doppelte anzahl der Rosen sind
R: true
A: die rose kostet 3€ herr Meier verdoppelt es und die karte wollen auch beide haben
R: false
A: Weil er eine gemeinsame Glückwunschkarte kauft und somit verdoppelt der Preis sich nicht.
R: true
A: {s_input}
R: 
""",
            "iM4640402_0": """T: {s_text}
Q: {s_question}
A: x * 0 = 0
R: true
A: x = x:x
R: false 
A: x=unendlich
R: false
A: x=unendlich
R: false
A: 0x+2=2
R: false
A: {s_input}
R:
""",
            "iM5662901_0": """T: {s_text}
Q: {s_question}
A: die schüler/in bekommen die geschenke nach dem Wochenende
R: false
A: 1 zu 24
R: true
A: zu 50% weill man sammstags und sonntags am montag macht und da 3 kinder gezogen werden
R: false
A: '4,2%
R: true
A: die wahrscheinlichkeit ist nicht so groß
R: false
A: {s_input}
R:
"""
}

# ===================================================================================================================================================

a22_2_t = """Parfüms werden meist in edlen Glasflaschen verkauft. Ein
Pumpzerstäuber auf diesen Flaschen verteilt das Parfüm in winzig kleine Tröpfchen. 
Dabei werden mit jedem Pumpstoß durchschnittlich 0,2 ml Parfüm verteilt."""

a22_2_q = """Sandra kauft eine Parfümflasche mit 100 ml Inhalt.
Gib an, wie lange diese Flasche wohl reicht, wenn Sandra täglich mehrere Pumpstöße
Parfüm verwendet."""

# ===================================================================================================================================================

a22_3_t = """Parfüms werden meist in edlen Glasflaschen verkauft. Ein
Pumpzerstäuber auf diesen Flaschen verteilt das Parfüm in winzig kleine Tröpfchen. Dabei werden mit jedem Pumpstoß durchschnittlich 0,2 ml Parfüm
verteilt."""

a22_3_q = """Eine Parfümflasche mit 50 ml Inhalt kostet im Verkauf 75 €. Gib an, wie viel Euro ein einzelner Pumpstoß etwa kostet."""

# ===================================================================================================================================================

a16_2_t = """Die maximale Belastung eines Fahrstuhls beträgt 600 kg.
Wenn die maximale Belastung überschritten wird, ertönt ein Warnsignal und der
Fahrstuhl fährt nicht los."""

a16_2_q = """Schätze, wie viele Erwachsene höchstens den Fahrstuhl betreten können, ohne dass
das Warnsignal ertönt."""

# ===================================================================================================================================================

a25_1_t = """Elli sieht in Koblenz das Kunstwerk „Der Daumen“ und vergleicht das Kunstwerk mit
ihrem eigenen Daumen. Das Daumenkunstwerk ist ungefähr anderthalb so groß wie sie."""

a25_1_q = """Wievielmal länger als Ellis Daumen ist das Kunstwerk ungefähr?"""

# ===================================================================================================================================================

a17_1_t = """Im Kopierraum einer Schule befindet sich folgender Vorrat an Kopierpapier:
31 Kartons mit je 4 oder 5 Paketen und ein zusätzliches Paket. Also ungefähr (31 * 4 oder 31 * 5) + 1 Pakete.
Ein einzelnes Paket Papier enthält 500 Blätter. (Also zwischen 62500 bis 78000 Blätter insgesamt)."""

a17_1_q = """Schätze, wie viele Blätter Kopierpapier sich in dem abgebildeten Vorrat ungefähr
befinden."""

# ===================================================================================================================================================

a13_2_t = """Frau Alfonso will ihrem Nachbarn zum Jubiläum einen Rosenstrauß schenken. Jede Rose
kostet 3 €. Im Blumenladen will sie zusammen mit dem Strauß eine Glückwunschkarte für
2 € kaufen."""

a13_2_q = """x bezeichnet die Anzahl der Rosen, y bezeichnet den Gesamtpreis in Euro (Preis der
Rosen plus Karte).
Gib eine Gleichung an, mit der sich y aus x berechnen lässt."""

# ===================================================================================================================================================

a13_1_t = """Frau Alfonso will ihrem Nachbarn zum Jubiläum einen Rosenstrauß schenken. Jede Rose
kostet 3 €. Im Blumenladen will sie zusammen mit dem Strauß eine Glückwunschkarte für
2 € kaufen."""

a13_1_q = """Herr Meier will sich an dem Geschenk zum Jubiläum beteiligen. Er schlägt vor, einen
Strauß mit der doppelten Anzahl an Rosen und dazu eine gemeinsame
Glückwunschkarte zu kaufen.
Verdoppelt sich dann der Gesamtpreis? Begründe deine Entscheidung!"""

# ===================================================================================================================================================

a14_1_t = """Selina und Merle üben das Lösen von Gleichungen.
Für eine Gleichung finden beide Mädchen nicht nur eine, sondern unendlich viele
Lösungen. Merle sagt: 'Es gibt auch Gleichungen mit unendlich vielen Lösungen. In
diese kann man für x jede beliebige Zahl einsetzen und es entsteht immer eine wahre
Aussage.' """

a14_1_q = """Notiere eine Gleichung, auf die Merles Beschreibung zutrifft."""

# ===================================================================================================================================================

a9_1_t = """Die 24 Schülerinnen und Schüler einer achten Klasse haben
für die Adventszeit einen gemeinsamen Adventskalender mit
24 Geschenken angefertigt.
Jeder legt ein Kärtchen mit seinem Namen in einen Lostopf.
Ab dem ersten Dezember wird täglich ein Name gezogen, die
zugehörige Person erhält das jeweilige Geschenk. Ihr Name
kann nun nicht mehr gezogen werden.
Die Ziehungen für Samstag und Sonntag werden am Montag
nachgeholt.
Die erste Ziehung passiert am 01.12. an einem Freitag."""

a9_1_q = """Carina fragt sich am 01.12., wie wahrscheinlich es ist, dass sie heute das Geschenk
bekommen wird.
Gib diese Wahrscheinlichkeit an."""

# ===================================================================================================================================================

iM2641902_text = {'iM2641903_1_0': a22_3_t,
                  'iM5662901_0': a9_1_t,
                  'iM2672802': a16_2_t,
                  'iM4620701_0': a13_2_t,
                  'iM2700801_1_0': a25_1_t,
                  'iM4620702_0_1': a13_1_t,
                  'iM4640402_0': a14_1_t,
                  'iM2641902_1_0': a22_2_t,
                  'iM2702701': a17_1_t}

iM2641902_question = {'iM2641903_1_0': a22_3_q,
                      'iM5662901_0': a9_1_q,
                      'iM2672802': a16_2_q,
                      'iM4620701_0': a13_2_q,
                      'iM2700801_1_0': a25_1_q,
                      'iM4620702_0_1': a13_1_q,
                      'iM4640402_0': a14_1_q,
                      'iM2641902_1_0': a22_2_q,
                      'iM2702701': a17_1_q}

# ===================================================================================================================================================
