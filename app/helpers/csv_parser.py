import csv
from typing import List, Dict
from io import StringIO


def parse_csv(csv_data: str) -> List[Dict[str, str]]:
    reader = csv.DictReader(StringIO(csv_data))
    return [row for row in reader]
