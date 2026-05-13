# pandas çalışma örneği
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
n = 1000

df = pd.DataFrame({
    "siparis_id":  range(10001, 10001 + n),
    "musteri_id":  rng.integers(1, 200, n),
    "urun_id":     rng.integers(1, 50, n),
    "kategori":    rng.choice(["Elektronik", "Giyim", "Ev", "Kozmetik", "Spor"], n),
    "fiyat":       rng.uniform(50, 5000, n).round(2),
    "adet":        rng.integers(1, 10, n),
    "tarih":       pd.date_range("2024-01-01", periods=n, freq="1h"),
    "durum":       rng.choice(["Teslim", "Kargoda", "İptal", "İade"], n,
                              p=[0.70, 0.15, 0.10, 0.05])
})

# ilk 5 satırı göster
print(df.head())

# eksik değer tespiti
# df.loc[rng.choice(df.index, 50), "fiyat"] = np.nan

# fiyat alanı eksik değer olanları 0 olarak doldur
df["fiyat"].fillna(0, inplace=True)

# fiyat alanları eksik değer olanları diğer fiyatların ortalaması ile doldur
df["fiyat"].fillna(df["fiyat"].mean(), inplace=True)

# kategorilere göre ortalama fiyat
kategori_ort = df.groupby("kategori")["fiyat"].mean()
print(kategori_ort)

# fiyat alanı eskik olanın kategorisine göre ortalama fiyat ile doldur
df["fiyat"] = df.groupby("kategori")["fiyat"].transform(lambda x: x.fillna(x.mean()))

# eksik değer sayısı
print("Eksik değer sayısı:\n", df.isna().sum())

# Belirli sütunların datasını göster
ozet = df[["siparis_id", "musteri_id", "fiyat"]].head()
print(ozet)

# 1000 TL üzeri fiyatlara sahip siparişleri göster, büyükten küçüğe sıralı
yuksek_fiyat = df[df["fiyat"] > 1000].sort_values(by="fiyat", ascending=False)
print(yuksek_fiyat)

# tüm dataların fiyatlarının en yüksek ve en düşük değerlerini göre sırala
fiyat_sirali = df.sort_values(by="fiyat", ascending=False)
print(fiyat_sirali[["siparis_id", "fiyat"]].head())

# tüm bu değişimleri bir csv dosyasına kaydet
df.to_csv("data/raw/siparisler.csv", index=False)

# tüm bu değişimleri bir excel dosyasına kaydet
fiyat_sirali.to_excel("data/raw/siparisler.xlsx", index=False)