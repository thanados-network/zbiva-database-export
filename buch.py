import csv

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

date_format = "%d.%m.%Y"

@dataclass
class Entry:
    text: str
    nr: int
    begin: datetime
    end: datetime
    name: str
    origin: Optional[str]
    diagnose: Optional[str]
    age: Optional[int]
    died: bool


def parse_csv(file_path: str):
    entries = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            begin = datetime.strptime(row.get('Beginn'), "%d.%m.%Y")
            end = datetime.strptime(row.get('Ende'), "%d.%m.%Y")
            entry = Entry(
                text=row.get('Originaltext'),
                nr=row['Nr.'],
                begin=begin,
                end=end,
                name=row.get('Name'),
                origin=row.get('Herkunft'),
                diagnose=row.get('Diagnose') if row['Diagnose'] else None,
                age=row.get('Alter'),
                died=True if row.get('Verst.') else False)
            entries.append(entry)
    return entries


class Source:

    def __int__(self, entry: Entry):
        self.nr = entry.nr
        self.name = f'Patient record {self.nr}'
        self.text = entry.text
        self.openatlas_id = 0



class Person:

    def __int__(self, entry: Entry):
        self.nr = entry.nr
        self.name = entry.name
        self.openatlas_id = 0
        self.begin = entry.begin
        self.end = entry.end
        self.age = entry.age
        self.died = entry.died
        self.diagnose = entry.diagnose
        self.born = self.get_born_date()

    def get_born_date(self) -> Optional[int]:
        if self.age:
            if self.end:
                return self.end.year - self.age
            elif self.begin:
                return self.begin.year - self.age
        return None





if __name__ == "__main__":
    entries = parse_csv('patientinnenbuch.csv')
    for entry in entries:
        Person(entry)
        Source(entry)
        pass
