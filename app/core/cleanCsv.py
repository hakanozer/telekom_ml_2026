import locale

import pandas as pd
import numpy as np
from scipy import stats
from difflib import SequenceMatcher
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scripts.clean import benzer_kategori

class cleanCsv:
    
    def __init__(self):
        print("cleanCsv sınıfı başlatıldı.")
    
    def clean_csv(self, df:pd.DataFrame):
        # fiyat değerleri hatalı, string yada 0 dan küçük yada boş olanları 0 ile doldur
        df["fiyat"] = pd.to_numeric(df["fiyat"], errors="coerce").fillna(50)
        df.loc[df["fiyat"] < 0, "fiyat"] = 50

        # Müşteri adlarında problem varsa defult değer olarak "Bilinmiyor" yaz
        df["musteri_adi"] = df["musteri_adi"].fillna("Bilinmiyor")

        # siparis_id si aynı olan satırları kaldır
        df = df.drop_duplicates(subset=["siparis_id"])

        # şehir map
        sehir_map = {
            "istanbul": "İstanbul",
            "Istanbul": "İstanbul",
            "ankara": "Ankara",
            "İZMİR": "İzmir",
            "bursa": "Bursa"
        }

        # şehir sütununu map ile güncelle
        df["sehir"] = df["sehir"].map(sehir_map).fillna(df["sehir"])

        # tarih formatını gün, ay, yıl olarak güncelle
        df["tarih"] = pd.to_datetime(df["tarih"], errors="coerce").dt.strftime("%d-%m-%Y %H:%M:%S")

        # tarihlerdeki aylarda rakam yerine ay adını türkçe olarak yaz
        df["tarih"] = pd.to_datetime(df["tarih"], errors="coerce").dt.strftime("%d-%B-%Y %H:%M:%S")

        # geçerli kategoriler: Elektronik, Giyim, Ev, Kozmetik, Spor
        kategoriler = ["Kozmetik", "Elektronik", "Giyim", "Ev", "Spor"]
        # benzer_kategori fonksiyonunu kullanarak kategori sütunundaki benzer kategorileri düzelt
        df["kategori"] = df["kategori"].apply(lambda x: self.benzer_kategori(x, kategoriler) if pd.notna(x) else x)

        # musteri_adi değerlerini önce küçük harfe çevir, sonra baş harflerini büyük yap
        df["musteri_adi"] = df["musteri_adi"].str.lower().str.title()

        # her satır için fiyat ile adet çarpımını yeni bir sütun olarak ekle ve sütun adına toplam de.
        # round 2 seviyesi ile fiyat ve toplam sütunlarını yuvarla
        df["toplam"] = (df["fiyat"] * df["adet"]).round(2)
        
         # JSON hatası için kritik bölüm
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna("")
        
        # kategori temizleme
        df["kategori"] = df["kategori"].replace(["", ",,", None], "Diğer")
        
        grafik_1 = self.kategori_bazli_toplam_satis(df)
        grafik_2 = self.son_ay_en_cok_alim_yapan_musteriler(df)
        grafik_3 = self.en_cok_satilan_10_sehir(df)
        
        # çıktı { "data": df, "grafikler": [grafik_1, grafik_2, grafik_3] } şeklinde olacak
        jsonData = df.to_dict(orient="records")
        dict = {
            "grafikler": [grafik_1, grafik_2, grafik_3],
            "data": jsonData
        }

        return dict
    
    
    # gönderilen kategori adına en çok benzeyen kategori adını döndüren fonksiyon
    def benzer_kategori(self, kategori, kategoriler):
        skorlar = [
            SequenceMatcher(None, kategori.lower(), k.lower()).ratio()
            for k in kategoriler
        ]
        en_benzeyen = kategoriler[skorlar.index(max(skorlar))]
        return en_benzeyen
    
    # matplotlib ile png grafikği oluşturmak için gerekli fonksiyon
    def kategori_bazli_toplam_satis(self, df):
        kategori_toplam = df.groupby("kategori")["toplam"].sum()
        plt.figure(figsize=(10, 6))
        kategori_toplam.plot(kind="bar")
        plt.title("Kategori Bazlı Toplam Satış")
        plt.xlabel("Kategori")
        plt.ylabel("Toplam")
        # sadece oluştur ve kaydet
        plt.savefig("data/raw/kategori_bazli_toplam_satis.png")
        # belleği temizle
        plt.close()
        return "kategori_bazli_toplam_satis.png"
    
    # son ay en çok alışveriş yapan 5 müşteri grafiği
    def son_ay_en_cok_alim_yapan_musteriler(self, df):

        # tarih kolonunu datetime yap
        df["tarih_dt"] = pd.to_datetime(
            df["tarih"],
            format="%d-%B-%Y %H:%M:%S",
            errors="coerce"
        )
        # geçerli tarihleri al
        max_tarih = df["tarih_dt"].max()
        # son 30 günlük veriler
        son_ay_df = df[df["tarih_dt"] >= (max_tarih - pd.Timedelta(days=30))]
        # müşteri bazlı toplam harcama
        musteri_toplam = (
            son_ay_df
            .groupby("musteri_adi")["toplam"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )
        # grafik oluştur
        plt.figure(figsize=(10, 6))
        musteri_toplam.plot(kind="bar")
        plt.title("Son Ay En Çok Alım Yapan 5 Müşteri")
        plt.xlabel("Müşteri")
        plt.ylabel("Toplam Harcama")
        plt.tight_layout()
        plt.savefig("data/raw/son_ay_en_cok_alim_yapan_5_musteri.png")
        plt.close()
        return "son_ay_en_cok_alim_yapan_5_musteri.png"  
    
    # en çok satılan 10 şehir grafiği
    def en_cok_satilan_10_sehir(self, df):

        # şehir bazlı toplam adet
        sehir_toplam = (
            df.groupby("sehir")["adet"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        # grafik oluştur
        plt.figure(figsize=(12, 6))
        sehir_toplam.plot(kind="bar")
        plt.title("En Çok Satışı Yapılan 10 Şehir")
        plt.xlabel("Şehir")
        plt.ylabel("Toplam Satış Adedi")
        plt.tight_layout()
        plt.savefig("data/raw/en_cok_satilan_10_sehir.png")
        plt.close()
        return "en_cok_satilan_10_sehir.png"