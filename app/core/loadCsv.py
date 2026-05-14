import pandas as pd

class LoadCsv:
    
    def __init__(self):
        print("LoadCsv sınıfı başlatıldı.")
    
    def load_csv(self):    
        # CSV dosyasını oku
        df = pd.read_csv("data/raw/siparisler_ham.csv")
        print("CSV dosyası başarıyla yüklendi.")
        return df
    
LoadCsv = LoadCsv() # nesne oluşturuldu    