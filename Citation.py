class Citation:
    def __init__(self, data) -> None:
            self.id_ = data['id']
            self.pages = data['pages']
            self.description = data['description']
            self.literature_id = data['literature_id']
            self.place_id = data['place_id']

    def __repr__(self) -> str:
        return str(self.__dict__)

    def get_pages(self) -> str:
        return self.pages.replace(' ', '')
