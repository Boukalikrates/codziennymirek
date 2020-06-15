# codziennymirek

Skrypt do wyszukiwania użytkownika wykop.pl o zadanym numerze w rankingu i wysyłania o tym wpisu.

Używany do codziennego wpisu na stronie https://www.wykop.pl/tag/codzienny2137mirek/

## Wymagania 
* Python 3.5
* biblioteki: requests, json
* Inkscape 0.92
* cron (opcjonalnie)

## Instalacja
Skrypt zaprojektowany do działania na Debianie 9.5 korzysta z komend `wget` i `rm` oraz zakłada, że Inkscape jest zainstalowany w domyślnej lokalizacji. W przypadku innej konfiguracji skrypt trzeba zmodyfikować.

Przed pierwszym uruchomieniem należy uzyskać dostęp do api wykop.pl. W tym celu należy:
* wejść na https://www.wykop.pl/dla-programistow/nowa-aplikacja/
* stworzyć aplikację z uprawnieniami `login` i `microblog`
* otrzymany otrzymany klucz, sekret i lkucz użytkownika skopiować do pliku `credentials.json`

