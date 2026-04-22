class Citation:
    def __init__(self, data: dict[str, str]) -> None:
        self.id_ = data["id"]
        self.pages = data['pages']
        self.description = data.get('description')
        self.origin_literature_id = data['literature_id']
        self.linked_id = data['linked_id']

    def __repr__(self) -> str:
        return str(self.__dict__)

    def get_pages(self) -> str:
        if not self.pages:
            return ""
        s = self.pages.strip()
        if (s.startswith("(") and s.endswith(")")) or \
           (s.startswith("[") and s.endswith("]")):
            s = s[1:-1].strip()
        return s.replace(' ', '')

    def get_csv_data(self) -> str:
        pages = self.get_pages().replace(';', ':')
        return f"literature_{self.origin_literature_id};{pages}"
