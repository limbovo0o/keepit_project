import sys  # Importuje moduł do obsługi argumentów wiersza poleceń
import urllib.request  # Importuje moduł do pobierania danych z URL
from html.parser import HTMLParser  # Importuje parser HTML z biblioteki standardowej

class ULParser(HTMLParser):  # Definiuje klasę parsera dziedziczącą po HTMLParser
    def __init__(self):
        super().__init__()  # Inicjalizuje klasę bazową
        self.ul_stack = []  # Stos do śledzenia zagnieżdżonych elementów <ul>
        self.ul_counts = []  # Lista do przechowywania liczby elementów <li> w każdym <ul>
        self.current_count = 0  # Licznik elementów <li> w aktualnym <ul>

    def handle_starttag(self, tag, attrs):  # Metoda obsługująca otwierające tagi HTML
        if tag == "ul":  # Sprawdza, czy tag to <ul>
            self.ul_stack.append(self.current_count)  # Zapisuje poprzedni licznik na stosie
            self.current_count = 0  # Resetuje licznik dla nowego <ul>
        elif tag == "li" and self.ul_stack:  # Sprawdza, czy tag to <li> i czy jesteśmy wewnątrz <ul>
            self.current_count += 1  # Zwiększa licznik <li> dla bieżącego <ul>

    def handle_endtag(self, tag):  # Metoda obsługująca zamykające tagi HTML
        if tag == "ul" and self.ul_stack:  # Sprawdza, czy tag to </ul> i czy stos nie jest pusty
            self.ul_counts.append(self.current_count)  # Zapisuje liczbę <li> w tym <ul>
            self.current_count = self.ul_stack.pop()  # Przywraca poprzednią wartość licznika

    def get_largest_ul_size(self):  # Metoda zwracająca największą liczbę elementów <li> w <ul>
        return max(self.ul_counts, default=0)  # Zwraca największą wartość lub 0 jeśli lista jest pusta


def fetch_html(url):  # Funkcja pobierająca HTML strony z podanego URL
    with urllib.request.urlopen(url) as response:  # Otwiera URL i pobiera jego zawartość
        return response.read().decode("utf-8", errors="ignore")  # Odczytuje i dekoduje treść strony


def main():  # Główna funkcja programu
    url = input("Podaj adres URL strony: ")  # Prosi użytkownika o wpisanie adresu URL
    html_content = fetch_html(url)  # Pobiera zawartość HTML strony

    parser = ULParser()  # Tworzy instancję parsera
    parser.feed(html_content)  # Przekazuje HTML do parsera
    print("Największa lista <ul> zawiera", parser.get_largest_ul_size(), "elementów <li>.")  # Wypisuje wynik


if __name__ == "__main__":  # Sprawdza, czy skrypt jest uruchomiony jako główny plik
    main()  # Uruchamia funkcję main()
