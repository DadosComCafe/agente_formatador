import zipfile
from typing import List
import pandas as pd


def handle_file(file: str) -> pd.DataFrame:
    if file.name.split(".")[-1] == "csv":
        return pd.read_csv(file)
    
    if file.name.split(".")[-1] == "xlsx":
        return pd.read_excel(file)


def handle_zip_file(zipado: str) -> List[pd.DataFrame]:
    with zipfile.ZipFile(zipado, "r") as zf:
        list_types = [file.split(".")[-1] for file in zf.namelist()]
        if len(list_types) > 1:
            print("Há arquivos em formatos distintos no zip!")
            return False
        
        for file in zf.namelist():
            ...