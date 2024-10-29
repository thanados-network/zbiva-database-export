class Citation:
    def __init__(self, data: dict[str, str]) -> None:
        self.id_ = data["id"]
        self.pages = data['pages']
        self.description = data['description']
        self.origin_literature_id = data['literature_id']
        self.place_id = data['place_id']

    def __repr__(self) -> str:
        return str(self.__dict__)

    def get_pages(self) -> str:
        return self.pages.replace(' ', '')

    def get_csv_data(self) -> str:
        pages = self.pages.replace(' ',      '').replace(';', ':') \
            if self.pages else ''
        return f"literature_{self.origin_literature_id};{pages}"
