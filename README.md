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
Przy końcu rzutu każdą z kostek, możemy dodać różne modyfikatory, które wpływają na ostateczny wynik, lub na sposób wyświetlania wyniku.
{cp} - symbole porównania: '<', '>', '<=', '>=', '=', '<>', '!='
Poza modyfikatorem Target Success/Failure, symbole porównania są opcjonalne
**Wszystkie dostępne modyfikatory, wraz z ich priorytetem:**
- Min (min{n}) - Traktuje każdy rzut poniżej podanej wartości jako tę wartość. Priorytet 1
- Max (max{n}) - Traktuje każdy rzut powyżej podanej wartości jako tę wartość. Priorytet 2
- Exploding (!{cp}) - Jeśli wyrzucisz najwyższą możliwą wartość, rzucasz jeszcze raz, a wynik dodajesz do poprzedniego. Priorytet 3
- Penetrating (!p{cp}) - Wariant Exploding, taki, że każdy wybuchający rzut ma odjęte 1 od wyniku.
- Re-Roll/Re-Roll Once (r{cp}/ro{cp}) - Przerzuca konkretny wynik (domyślnie 1). Priorytet 4
- Unique/Unique Once (u{cp}/uo{cp}) - Przerzuca kostki, tak żeby uniknąć powtórzeń. Priorytet 5
- Keep (k{n}/kh{n}/kl{n}) - Zatrzymuje określoną liczbę najgorszych/najlepszych rzutów. Priorytet 6
- Drop (d{n}/dh{n}/dl{n}) - Pozbywa się określonej liczby najgorszych/najlepszych rzutów. Priorytet 7
- Target Success/Failure ({cp}f{cp}) - Zwraca liczbę kostek spełniającą dany warunek oraz (opcjonalnie) niespełniającą drugiego warunku. Priorytet 8
- Critical Success/Failure (cs{cp}) - (wizualne) Specjalnie oznacza rzuty kostką które uznajemy za krytyczny sukces lub porażkę. Priorytet 9(success), Priorytet 10(failure)
- Sorting (s/sa/sd) - (wizualne) Sortuje wyrzucone kostki. Priorytet 11

#### Operacje matematyczne
- Program obsługuje także podstawowe operacje matematyczne (dodawanie, odejmowanie, mnożenie, dzielenie, potęgowanie), nawiasy, oraz podstawowe funkcje trygonometryczne (sin, cos, tan, cot)

## Formalna Gramatyka i Tokeny
Nasz parser opiera się na gramatyce zapisanej w formacie EBNF, przetwarzanej przy pomocy biblioteki Lark.

#### 1. Typ gramatyki (Hierarchia Chomsky'ego)
Zastosowana przez nas gramatyka to **gramatyka bezkontekstowa (Typ 2 w hierarchii Chomsky'ego)**. 

#### 2. Tokeny
- Liczby: `INT`, `NUMBER`, `SIGNED_NUMBER`
- Operatory matematyczne: `+`, `-`, `*`, `/`, `**`, `%`
- Symbole kości i modyfikatory
- Operatory logiczne/porównania: `<`, `>`, `<=`, `>=`, `=`, `<>`, `!=`
- Znaki specjalne: `(`, `)`

#### 3. Definicja Gramatyki
**Symbol startowy: `statement`**

**Główne Nieterminale:**
- `statement` – ciąg wartości połączonych operatorami matematycznymi
- `value` – pojedyncza wartość, która może być modyfikatorem, rzutem kością, lub wyrażeniem w nawiasach
- `dice_throw` – struktura rzutu, definiująca liczbę, rodzaj kości oraz opcjonalny ciąg modyfikatorów
- `modifier` – stała wartość liczbowa lub wynik funkcji trygonometrycznej
- `operator` – rozpoznaje użyty operator arytmetyczny
- Oraz nieterminale pomocnicze (np. `explode`, `reroll`)

**Uproszczony zapis głównych reguł produkcji:**
statement  -> value (operator value)*
value      -> modifier | dice_throw | "(" statement ")"
dice_throw -> n_rolls "d" n_faces (modyfikatory)*
modifier   -> (minus? mod_num) | funkcja_trygonometryczna
operator   -> "**" | "+" | "-" | "*" | "/" | "%"

## Instrukcja uruchomienia
- Przed uruchomieniem programu należy zainstalować bibliotekę Lark
- Program uruchamiany jest standardowo, poprzez plik 'main.py'

## Przykłady użycia
- 
- 
