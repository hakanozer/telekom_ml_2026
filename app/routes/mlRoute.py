from fastapi import APIRouter, HTTPException

from ..core.cleanCsv import cleanCsv
from ..core.loadCsv import LoadCsv

router = APIRouter()

# yükleyici başlatılıyor
siparisler_ham = LoadCsv.load_csv()
cleansCsv = cleanCsv()

@router.get("/report")
def ml_endpoint():
    # ML işlemleri burada yapılacak
    data = cleansCsv.clean_csv(siparisler_ham)
    # json return etmek için dataframe i dict e çevir
    return data