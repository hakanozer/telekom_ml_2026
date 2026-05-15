from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

def toplam_tahmin_modeli(self, df):

    # kategorik verileri sayısala çevir
    df_ml = df.copy()

    df_ml["kategori"] = df_ml["kategori"].astype("category").cat.codes
    df_ml["sehir"] = df_ml["sehir"].astype("category").cat.codes

    X = df_ml[["fiyat", "adet", "kategori", "sehir"]]
    y = df_ml["toplam"]

    # eğitim/test ayrımı
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    # model oluştur
    model = LinearRegression()

    # eğit
    model.fit(X_train, y_train)

    # tahmin yap
    tahminler = model.predict(X_test)

    # hata hesapla
    hata = mean_absolute_error(y_test, tahminler)

    return {
        "ortalama_hata": round(hata, 2),
        "tahminler": tahminler.tolist()
    }