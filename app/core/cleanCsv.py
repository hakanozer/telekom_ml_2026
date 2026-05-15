import locale

import pandas as pd
import numpy as np
from scipy import stats
from difflib import SequenceMatcher
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ..core.ml import kategori_tahmin_modeli, toplam_tahmin_modeli

from scripts.clean import benzer_kategori

class cleanCsv:
    
    def __init__(self):
        print("cleanCsv sınıfı başlatıldı.")
        
        # -----------------------------
    # JSON SAFE CONVERTER
    # -----------------------------
    def _safe_list(self, values):
        return [
            float(v) if isinstance(v, (np.floating, np.integer)) else v
            for v in values
        ]

    def _modern_palette(self, n):
        palette = [
            "#6366F1", "#8B5CF6", "#EC4899", "#22C55E",
            "#F59E0B", "#06B6D4", "#EF4444", "#14B8A6",
            "#A855F7", "#84CC16"
        ]
        return [palette[i % len(palette)] for i in range(n)]

    def _build_chartjs(self, chart_type, title, labels, data, label):
        return {
            "type": chart_type,
            "title": title,
            "labels": labels,
            "datasets": [
                {
                    "label": label,
                    "data": self._safe_list(data),
                    "backgroundColor": self._modern_palette(len(labels)),
                    "borderRadius": 8
                }
            ]
        }    
    
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
        
        chartjs_1 = self.kategori_bazli_toplam_satis_chartjs(df)
        chartjs_2 = self.son_ay_en_cok_alim_yapan_musteriler_chartjs(df)
        chartjs_3 = self.en_cok_satilan_10_sehir_chartjs(df)
        
        # ML Data Hazırlığı
        ml_sonuclari = {
            "toplam_tahmin_tl": toplam_tahmin_modeli(df),
            "kategori_tahmin_modeli_yuzde": kategori_tahmin_modeli(df)
        }
        
        # çıktı { "data": df, "grafikler": [grafik_1, grafik_2, grafik_3] } şeklinde olacak
        jsonData = df.to_dict(orient="records")
        dict = {
            "ml_sonuclari": ml_sonuclari,
            "grafikler": [grafik_1, grafik_2, grafik_3],
            "chartjs_grafikler": [chartjs_1, chartjs_2, chartjs_3],
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
    
    def kategori_bazli_toplam_satis_chartjs(self, df):
        kategori_toplam = (
            df.groupby("kategori")["toplam"]
            .sum()
            .sort_values(ascending=False)
        )

        return self._build_chartjs(
            chart_type="bar",
            title="Kategori Bazlı Toplam Satış",
            labels=kategori_toplam.index.tolist(),
            data=kategori_toplam.values.tolist(),
            label="Toplam Satış"
        )
        
    def son_ay_en_cok_alim_yapan_musteriler_chartjs(self, df):
        df["tarih_dt"] = pd.to_datetime(
            df["tarih"],
            format="%d-%B-%Y %H:%M:%S",
            errors="coerce"
        )

        max_tarih = df["tarih_dt"].max()
        son_ay_df = df[df["tarih_dt"] >= (max_tarih - pd.Timedelta(days=30))]

        musteri_toplam = (
            son_ay_df.groupby("musteri_adi")["toplam"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )

        return self._build_chartjs(
            chart_type="bar",
            title="Son 30 Gün En Çok Harcayan 5 Müşteri",
            labels=musteri_toplam.index.tolist(),
            data=musteri_toplam.values.tolist(),
            label="Toplam Harcama"
        )
        
    def en_cok_satilan_10_sehir_chartjs(self, df):
        sehir_toplam = (
            df.groupby("sehir")["adet"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        return {
            "type": "doughnut",
            "title": "En Çok Satış Yapılan 10 Şehir",
            "labels": sehir_toplam.index.tolist(),
            "datasets": [
                {
                    "label": "Satış Adedi",
                    "data": self._safe_list(sehir_toplam.values.tolist()),
                    "backgroundColor": self._modern_palette(len(sehir_toplam)),
                    "borderWidth": 0
                }
            ]
        }  
