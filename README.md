# TAforFMDocs

## Input Data - Selektion & Export

### Dokumente

- **Suchkriterien** * bei Kind-ID, Fall-ID und MBSVision (oberes gelbes Feld), = zweimal bei Testeintrag
- **Export** 54 917 Dokumente (240518)
- **Ausschluss von Empfehlungen** 35 967 Dokumente, = minus 35% (240525)

### Texte

- 19374 Texte (vereinte Dokumente pro Fall), d.h. 1.85 Dokumente ohne die Empfehlung pro Kind

### Diagnosenlisten

- **Suchkriterien** bei Fall_ID und Diagnosen im Fall, = bei Testeintrag
- **Export** 16 491 Diagnoselisten (eine Liste pro Fall) (240610)

### Modell Input Data

9 740 Kombinationen von Text und hot-encoded Diagnosen (auf Fall-Ebene)

### Modellheuristik - welche Vorraussagengüte erwarte ich?

Bei den Fällen im Jahr 2023 war es so, dass total 48% der Fälle aufgrund der Dokumente,
also ohne das Kind zusätzlich zu sehen, entschieden wurden. Das kann in den vorderen Jahren natürlich anders
gewesen sein, trotzdem bleibt wohl **50%** die obere Schranke für ein Modell, mehr wird nicht zu erreichen sein.

Bzw. - wird mehr erreicht, dann liegt es daran, dass noch zu viele Dokumente als Input genommen wurden, welche zum
Zeitpunkt der Entscheidung noch gar nicht vorhanden waren...



