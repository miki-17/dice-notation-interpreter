# dice-notation-interpreter
## Autorzy i podział prac
### Mikołaj Pasiut (498782):
- Implementacja parsera, generującego drzewo AST, przy pomocy modułu Lark.
- Dodanie pliku README.md
### Aleksey Pravilov (498780):
- Implementacja interpretera, przyjmującego drzewo AST, a zwracającego podany wynik (sumę rzutów kostkami, wraz z uwzględnionymi modyfikatorami)

## Opis projektu
Notacja stosowana w projekcie jest inspirowana notacją przedstawioną w https://dice-roller.github.io/documentation/guide/notation/.
Podstawowym zadaniem parsera+interpretera jest wykonanie rzutu kostką w formacie {n}d{m}, gdzie `n` oznacza liczbę kostek, którymi rzucamy, a `m` oznacza ile ścian ma ta kostka
#### Typy kostek:
Poza dowolną liczbą naturalną, dostępne typy kostek to:
- d% - traktowana jako d100
- dF - Kostka zwracająca -1, 0 albo 1

#### Modyfikatory
Przy końcu rzutu każdą z kostek, możemy dodać różne modyfikatory, które wpływają na ostateczny wynik, lub

## Formalna Gramatyka i Tokeny


## Instrukcja uruchomienia
- 
- 

## Przykłady użycia
- 
- 
