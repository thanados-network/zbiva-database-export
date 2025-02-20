import csv

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

date_format = "%d.%m.%Y"


import pandas as pd
from datetime import datetime

class Entry:
    def __init__(self, text, nr, begin, end, name, origin, diagnose, age, died):
        self.text = text
        self.nr = nr
        self.begin = begin
        self.end = end
        self.name = name
        self.origin = origin
        self.diagnose = diagnose
        self.age = age
        self.died = died

def parse_csv(file_path: str):
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8', dtype=str)
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    df['Beginn'] = pd.to_datetime(
        df['Beginn'],
        format='%d.%m.%Y',
        errors='coerce')
    df['Ende'] = pd.to_datetime(
        df['Ende'],
        format='%d.%m.%Y',
        errors='coerce')

    return [
        Entry(
            text=row['Originaltext'],
            nr=row['Nr.'],
            begin=row['Beginn'],
            end=row['Ende'],
            name=row['Name'] if pd.notna(row['Name']) else '',
            origin=row['Herkunft'] if pd.notna(row['Herkunft']) else '',
            diagnose=row['Diagnose'] if pd.notna(row['Diagnose']) else None,
            age=row['Alter'] if pd.notna(row['Alter']) else None,
            died=bool(pd.notna(row['Verst.']))
        ) for _, row in df.iterrows()]





class Source:

    def __init__(self, entry: Entry):
        self.nr = entry.nr
        self.name = f'Patient record {self.nr}'
        self.text = entry.text
        self.openatlas_id = 0


class Person:

    def __init__(self, entry: Entry):
        self.nr = entry.nr
        self.name = entry.name
        self.openatlas_id = 0
        self.begin = entry.begin
        self.end = entry.end
        self.age = int(entry.age) if entry.age else None
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

class Activity:

    def __init__(self, entry: Entry):
        self.person = Person(entry)
        self.source = Source(entry)
        self.nr = entry.nr
        self.name = f'Patient visit {self.nr} of {self.person.name}'
        self.begin = entry.begin
        self.end = entry.end
        self.diagnose = entry.diagnose


if __name__ == "__main__":
    entries = parse_csv('patientinnenbuch.csv')
    persons = [Person(e) for e in entries]
    sources = [Source(e) for e in entries]
    diagnoses = [e.diagnose for e in entries if e.diagnose]
    l= sorted(set(diagnoses), key=lambda s: s.lower())
    for i in l:
        print(f'* {i}')





