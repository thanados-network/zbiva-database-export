from typing import Any

class Literature:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id_ = data.get('id')
        self.autor = data.get('autor')
        self.title = data.get('title')
        self.publication = data.get('publication')
        self.date = data.get('date')
        self.location = data.get('location')
        self.pages = data.get('pages')
        self.signature = data.get('signature')
        self.pdf_link = data.get('pdf_link')
        self.doi = data.get('doi')
        self.name = self.get_name()
        self.description = self.get_description()
        self.type_ids = '4' if self.publication else '5'

    def __repr__(self) -> str:
        return str(self.__dict__)

    def get_csv_data(self) -> dict[str, Any]:
        return {
            'id': f'literature_{self.id_}',
            'name': self.name,
            'type_ids': self.type_ids,
            'description': self.description}

    # Get name, problem is, if no Autor | publication | title exist
    # And if first word is e.g. (ed.) etc.
    def get_name(self) -> str:
        date = self.date or 'Unknown'
        if self.autor:
            autor = self.autor.replace('(ed.)', '').replace(',', '').strip()
            name = f"{autor.split(' ')[0]} {date}"
        elif self.publication:

            name = f"{self.publication.split(' ')[0]} {date}"
        elif self.title:
            name = f"{self.title.split(' ')[0]} {date}"
        else:
            name = f"Unknown {date}"

        return name.replace('(', '').replace(')', '').strip()

    def get_description(self) -> str:
        def get_autor() -> str:
            autor = ''
            if self.autor:
                autor = self.autor + ','
            return autor.replace('\n', '').strip()

        def get_title() -> str:
            title = ''
            if self.title:
                title = f"{self.title}."
            return title.replace('\n', '').strip()

        def get_publication() -> str:
            publication = ''
            if self.publication and self.autor:
                publication = f' In: {self.publication}'
            elif self.publication:
                publication = self.publication
            return publication.replace('\n', '').strip()

        def get_location_date() -> str:
            date = self.date or ''
            location = self.location or ''
            if self.publication:
                location_date = f'({date})'
            else:
                location_date = f'({location} {date})'
            return location_date.replace('\n', '').strip()

        def get_pages() -> str:
            pages = ''
            if self.pages:
                pages = f' {self.pages}'
            return pages.replace('\n', '')

        def get_pdf_link() -> str:
            pdf_link = ''
            if self.pdf_link:
                pdf_link = f'\n{self.pdf_link}'
            return pdf_link

        def get_signature() -> str:
            signature = ''
            if self.signature:
                signature = f'\n{self.signature}'
            return signature

        def get_doi() -> str:
            doi = ''
            if self.doi:
                doi = f'\n{self.doi}'
            return doi

        citation = (f"{get_autor()} {get_title()}"
                    f"{get_publication()} {get_location_date()}{get_pages()}.")
        references = get_pdf_link() + get_doi() + get_signature()
        return citation + references
