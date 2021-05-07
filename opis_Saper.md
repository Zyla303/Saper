<h2>13. Saper</h2> 
(<a href="https://pl.wikipedia.org/wiki/Saper_(gra_komputerowa)">https://pl.wikipedia.org/wiki/Saper_(gra_komputerowa))
<br/><br/>
Git hub: <a href="https://github.com/Zyla303/Saper">Szymon Żylski</a>
<br/>
<h3> Opis zadania </h3>
<p>Główne okno zawiera dwa pola tekstowe do wprowadzenia rozmiaru planszy (n na m pól), plansze o wymiarach n na m pól 
(np. siatka przycisków), pole tekstowe na wprowadzenie liczby min na planszy, liczbę oznaczonych pól, liczbę min na planszy
oraz przycisk rozpoczecia nowej gry.</p>
<p>Wprowadzenie mniejszego rozmiaru planszy niż 2x2 lub większego niż 15x15, liczby min mniejszej niż 0 lub wiekszej niż m*n
powoduje wyświetlenie komunikatu o błędzie. Nie można rozpocząć gry dopóki te parametry nie są poprawne. Walidacja danych 
powinna wykorzystywać mechanizm wyjątków</p>
<p>Na pcozątku gry na losowych polach umieszczane jest tyle min ile wskazano w polu tekstowym (każde mozliwe rozłożenie 
min jest równie prawdopodobne).</p>
<p>Po kliknięciu lewym przyciskiem na pole:</p>
<ul>
<li>Jeśli jest tam mina, wyświetlana jest wiadomość o przegranej i gra się kończy,</li>
<li>Jeśli w sąsiedztwie pola są miny, na przycisku wyświetlana jest ich liczba, a pole dezaktywuje się,</li>
<li>W przeciwnym razie sąsiednie pola są sprawdzane tak jakby zostały kliknięte, a pole dezaktywuję się.</li>
</ul>
<p>Po kliknięciu prawym przysciskiem pole może zostać oznaczone "tu jest mina", po ponownym kliknięciu oznaczenie zmiena
się na "tu może być mina", a po kolejnym kliknięciu oznaczenie znika.</p>
<p>Gra kończy się po kliknięciu wszystkich pól bez min, lub oznaczeniu "tu jest mina" wszystkich pól z minami (i
żadnych innych).</p>
<p>Po naciśnięciu kolejno klawiszy x, y, z. z. y, pola pod którymi są miny stają się ciemniejsze (<a href="https://en.wikipedia.org/wiki/Xyzzy_(computing)#Other_computer_games_and_media">https://en.wikipedia.org/wiki/Xyzzy_(computing)#Other_computer_games_and_media</a>)</p>

<h3> Testy </h3>
<p>1. Próba rozpoczęcia gry z rozmiarem planszy i liczbą min: (1 na 1; 1), (5 na 1; 2), (4 na 1; 2),
(20 na 500; 12), (5 na 6; -4), (3 na 3; 10), (1 na 10; 5) - oczekiwane komunikaty o błędzie. Wprowadzenie rozmiarów
planszy 8 na 8 i liczby min równej 12 na potrzeby kolejnych testów.</p>
<p>2. Kliknięcie pola, wyświetla się liczba min w sąsiedztwie pola.</p>
<p>3. Kliknięcie pola, wyświetla się mina, gra się kończy.</p>
<p>4. Kliknięcie pola, brak min w sąsiedztwie - oczekiwane automatyczne sprawdzenie sąsiadów, aż do wyznaczenia
obszaru wyznaczonego przez pola sąsiadujące z minami lub krawędzie planszy.</p>
<p>5. Oznaczenie pola jako "tu jest mina" - licznik oznaczonych powinien wzrosnąć o 1.</p>
<p>6. Oznaczenie pola jako "tu może być mina".</p>
<p>7. Oznaczenie pola, odznaczenie go, ponowne oznaczenie i ponowne odznaczenie - licznik oznaczonych powinien się 
odpowiednio aktualizować.</p>
<p>8. Wygranie gry przez kliknięcie wszystkich pól bez min.</p>
<p>9. Wygranie gry przez oznaczenie wszystkich pól z minami (można skorzystać z kodu xyzzy).</p>
<p>10. Próba oznaczenia sprawdzonego pola - oczekiwane niepowodzenie.</p>
<p>11. Sprawdzenie kilku pól bez min, oznaczenie pól "tu jest mina", rozoczęcie nowej gry - licznik min powinien się zakutalizować,
a pola zresetować.</p>
<p>12. Wpisanie kodu xyzzy, zresetowanie gry - wszystkie pola powinny odzyskać standardowy kolor.</p>