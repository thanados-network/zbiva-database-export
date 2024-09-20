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

    def __repr__(self) -> str:
        return str(self.__dict__)

    # Get name, problem is, if no Autor | publication | title exist
    def get_name(self) -> str:
        if self.autor:
            name = f"{self.autor.split(' ')[0]} {self.date}"
        elif self.publication:
            name = f"{self.publication.split(' ')[0]} {self.date}"
        elif self.title:
            name = f"{self.title.split(' ')[0]} {self.date}"
        else:
            name = f"Unknown {self.date}"
        return name

    def get_description(self) -> str:
        return f"""{self.autor + ',' or ''} {self.title or ''} {'. In: ' + self.publication + ',' or ''} """
