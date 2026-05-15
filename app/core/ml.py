from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def toplam_tahmin_modeli(df):

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
    
    

def kategori_tahmin_modeli(df):

    df_ml = df.copy()

    df_ml["kategori"] = df_ml["kategori"].fillna("Diğer")

    df_ml["kategori_code"] = (
        df_ml["kategori"]
        .astype("category")
        .cat.codes
    )

    X = df_ml[["fiyat", "adet"]]
    y = df_ml["kategori_code"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier()

    model.fit(X_train, y_train)

    tahmin = model.predict(X_test)

    skor = accuracy_score(y_test, tahmin)

    return {
        "dogruluk_orani": round(skor * 100, 2)
    }    