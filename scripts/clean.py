import locale

import pandas as pd
import numpy as np
from scipy import stats

# bu programda tarih ve saat türkçe dile uygun olmalıdır.
locale.setlocale(locale.LC_TIME, "tr_TR.UTF-8")

# Kapsamlı eksik değer raporu
def eksik_raporu(df):
    eksik = df.isnull().sum()
    eksik_oran = df.isnull().mean() * 100
    rapor = pd.DataFrame({
        "Eksik Sayı": eksik,
        "Oran (%)":   eksik_oran.round(2),
        "Veri Tipi":  df.dtypes
    })
    return rapor[rapor["Eksik Sayı"] > 0].sort_values("Oran (%)", ascending=False)

# Kirli e-ticaret verisi simülasyonu
rng = np.random.default_rng(42)
n = 500

siparisler_ham = pd.DataFrame({
    "siparis_id":   list(range(10001, 10001+n)) + [10050, 10100],  # Duplikasyon
    "musteri_adi":  (["ahmet yılmaz", "AYŞE KAYA", "Mehmet  Demir", " Fatma Şahin"] * 126)[:n+2],
    "sehir":        (["istanbul", "Ankara", "İZMİR", "bursa", "Istanbul"] * 101)[:n+2],
    "fiyat":        list(rng.uniform(50, 5000, n).round(2)) + [-999, 99999],  # Aykırı değerler
    "adet":         list(rng.integers(1, 10, n)) + [1, 1],
    "tarih":        list(pd.date_range("2024-01-01", periods=n, freq="3h")) + [pd.NaT, pd.NaT],
    "kategori":     list(rng.choice(["Elektronik","Giyim","Ev","?","N/A"], n)) + ["Ev","Giyim"]
})

# Eksik değer simülasyonu
siparisler_ham.loc[rng.choice(n, 40), "fiyat"] = np.nan
siparisler_ham.loc[rng.choice(n, 20), "musteri_adi"] = np.nan
siparisler_ham.loc[rng.choice(n, 15), "kategori"] = np.nan

#print(f"Ham veri şekli: {siparisler_ham.shape}")
#siparisler_ham.info()

# öncesinde siparisler_ham csv dosyasına kaydet
# siparisler_ham.to_csv("data/raw/siparisler_ham.csv", index=False)

# siparisler_ham.csv dosyasını oku
siparisler_ham = pd.read_csv("data/raw/siparisler_ham.csv")

# copy
df = siparisler_ham.copy()

# fiyat değerleri hatalı, string yada 0 dan küçük yada boş olanları 0 ile doldur
df["fiyat"] = pd.to_numeric(df["fiyat"], errors="coerce").fillna(50)
df.loc[df["fiyat"] < 0, "fiyat"] = 50

# ---- Kategorik: Mod (en sık değer) ----
mod_kategori = df["kategori"].mode()[0]
print(f"Kategori sütununun modu: {mod_kategori}")

# Müşteri adlarında problem varsa defult değer olarak "Bilinmiyor" yaz
df["musteri_adi"] = df["musteri_adi"].fillna("Bilinmiyor")

# yenilenen satırların sayısı - duplikasyonları kaldır
duplikasyon_sayisi = df.duplicated(subset=["siparis_id"]).sum()
print(f"Duplikasyon sayısı: {duplikasyon_sayisi}")

# siparis_id si aynı olan satırları kaldır
df = df.drop_duplicates(subset=["siparis_id"])

# Duplikasyonları tespit et
print(f"Toplam satır: {len(df)}")
print(f"Duplike satır: {df.duplicated().sum()}")

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

eksik_raporu = eksik_raporu(df)
print("Eksik Değer Raporu:\n", eksik_raporu)

# tarih formatını gün, ay, yıl olarak güncelle
df["tarih"] = pd.to_datetime(df["tarih"], errors="coerce").dt.strftime("%d-%m-%Y %H:%M:%S")

# tarihlerdeki aylarda rakam yerine ay adını türkçe olarak yaz
df["tarih"] = pd.to_datetime(df["tarih"], errors="coerce").dt.strftime("%d-%B-%Y %H:%M:%S")


# temiz sipariş verisini csv dosyasına kaydet
df.to_csv("data/raw/siparisler_temiz.csv", index=False)
