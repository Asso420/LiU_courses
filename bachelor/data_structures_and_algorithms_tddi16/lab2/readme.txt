Bildmatchning
=============

- Ungefärligt antal timmar spenderade på labben (valfritt):


- Vad är tidskomplexiteten på "slow.cpp" och din implementation av "fast.cpp",
  uttryckt i antalet bilder (n).

slow:O(n^2) (kommer behöva jämföra varje bild med varandra en och en så kommer i princip köra genom alla bilder i två for loopar)
fast: O(n)  (Kommer köra genom alla bilder en gång där den sätter de i rätt plats i hashmapen sen iterera genom mappen för att skriva ut dupliceringar alltså n+n 
             Det blir det som medelfall eftersom det kan hända att det blir att alla bilder matchar så behöver köra genom mapppen en gång men då kör report_match
             funktionen genom de alla matchningarna)


- Hur lång tid tar det att köra "slow.cpp" respektive "fast.cpp" på de olika
  datamängderna?
  Tips: Använd flaggan "--nowindow" för enklare tidsmätning.
  Tips: Det är okej att uppskatta tidsåtgången för de fall du inte orkar vänta
  på att de blir klara.
  Tips: Vid uppskattning av körtid för "slow.cpp" är det en bra idé att beräkna
  tiden det tar att läsa in (och skala ner) bilderna separat från tiden det tar att
  jämföra bilderna. (Varför?)

|--------+-----------+----------+----------|
|        | inläsning | slow.cpp | fast.cpp |
|--------+-----------+----------+----------|
| tiny   |    154 ms |   242 ms |   124 ms |
| small  |   2431 ms |   2638 ms|   833 ms |
| medium |   11896 ms|  13095 ms|  6066 ms |
| large  |  96577 ms | 604101 ms|  84947 ms|
|--------+-----------+----------+----------|


- Testa olika värden på "summary_size" (exempelvis mellan 6 och 10). Hur
  påverkar detta vilka dubbletter som hittas i datamängden "large"?
  
  Mängden matches ändras då man kan hitta mindre matches som man hittade förut eller vid ett stort 
  data så hittar man matches som man inte hittade förut alltså "accuracy" ändras. 
  Till exempel ändrar man så kan man hitta i medium matchning mellan två bilder när det ska finnas tre bilder som matchas. 

- Algoritmen som implementeras i "compute_summary" kan ses som att vi beräknar
  en hash av en bild. Det är dock inte helt lätt att hitta en bra sådan funktion
  som helt motsvarar vad vi egentligen är ute efter. Vilken eller vilka
  egenskaper behöver "compute_summary" ha för att vi ska kunna lösa problemet i
  labben? Tycker du att den givna funktionen uppfyller dessa egenskaper?

  Vi hade givet summary_size 8 som ska funka för vårat data men våran compute _summary kan ha haft en funktion
  som räknar en bilds original size om vi antar att alla bilder är lika stora. Då kan man göra en shrink utan att 
  behöva tänka på ändra brightness (R,G,B) när vi gör shrink för mycket och ändrar resultatet med matchningarna. Detta kan hjälpa
  oss då utveckla vidare koden till att hantera olika storlekar på bilderna. 



- Ser du några problem med metoden som används i labben? Kan du komma på andra
  metoder att hitta bilder som är "ungefär" lika? Vad har de för för- och
  nackdelar jämfört med den som föreslås i labben? (Testa gärna om du har idéer)

Eftersom vi håller på genomför brightness så kan man ta det ett steg ner och jämföra RGB direkt alltså alla tre värderna 
men det gör saker lite mer komplicerat med tanken på hur man ska jämföra för tar man de tre värderna plusat ihop direkt och jämför 
så får man problem som att 255,0,0 är samma som 0,0255 även då de är två helt olika färger därför krävs det mer komplicerat jämförelese. 

