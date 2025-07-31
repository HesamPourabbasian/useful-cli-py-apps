import requests
from colorama import init, Fore, Style
from tabulate import tabulate

init()

base_url = "https://openlibrary.org/search.json"

def book_search(name):
    url = f"{base_url}?q={name}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"{Fore.RED}Error: Unable to fetch data. Status code: {response.status_code}{Style.RESET_ALL}")
            return None
    except requests.RequestException as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None

def print_book_table(book_data):
    if not book_data or not book_data.get('docs'):
        print(f"{Fore.YELLOW}No book information found.{Style.RESET_ALL}")
        return

    table_data = []
    headers = [
        f"{Fore.CYAN}Field{Style.RESET_ALL}",
        f"{Fore.CYAN}Value{Style.RESET_ALL}"
    ]

    book = book_data['docs'][0]

    title = book.get('title', 'Unknown Title')
    authors = ', '.join(book.get('author_name', ['Unknown Author']))
    first_publish_year = book.get('first_publish_year', 'Unknown')
    publisher = ', '.join(book.get('publisher', ['Unknown Publisher'])) if book.get('publisher') else 'Unknown Publisher'
    isbn = book.get('isbn', ['Unknown ISBN'])[0] if book.get('isbn') else 'Unknown ISBN'
    language = ', '.join(book.get('language', ['Unknown'])) if book.get('language') else 'Unknown'

    table_data.extend([
        [f"{Fore.GREEN}Title{Style.RESET_ALL}", title],
        [f"{Fore.GREEN}Author(s){Style.RESET_ALL}", authors],
        [f"{Fore.GREEN}First Publish Year{Style.RESET_ALL}", first_publish_year],
        [f"{Fore.GREEN}Publisher{Style.RESET_ALL}", publisher],
        [f"{Fore.GREEN}ISBN{Style.RESET_ALL}", isbn],
        [f"{Fore.GREEN}Language{Style.RESET_ALL}", language]
    ])

    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

def main():
    book_name = input(f"{Fore.BLUE}Enter a book name: {Style.RESET_ALL}")
    book_info = book_search(book_name)
    print_book_table(book_info)

if __name__ == "__main__":
    main()