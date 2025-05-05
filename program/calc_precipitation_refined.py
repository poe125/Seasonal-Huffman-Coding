import os
import glob
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import math

# ------------------------
# データ前処理関数
# ------------------------
def preprocess_weather_data(df, label):
    df = df[['年月日時', '気温(℃)', '相対湿度(％)', '降水量(mm)']].copy()
    df['年月日時'] = pd.to_datetime(df['年月日時'], errors='coerce')
    df = df.dropna(subset=['年月日時'])
    df = df.dropna()  # 気温・湿度・降水量すべてにNaNがないように
    df['flood_label'] = label
    return df

# ------------------------
# 洪水データの一括読み込み
# ------------------------
def load_flood_data_from_folder(folder_path, threshold=10.0):
    flood_dfs = []
    for file_path in glob.glob(os.path.join(folder_path, "*.csv")):
        try:
            df = pd.read_csv(file_path, encoding='shift_jis', skiprows=3)
            df.columns = df.columns.str.strip()
            location = os.path.basename(file_path).split('.')[0]
            print(f"[INFO] Loading {location}...")

            clean_df = preprocess_weather_data(df, label=1)
            flood_df = clean_df[clean_df['降水量(mm)'] >= threshold].copy()
            flood_dfs.append(flood_df)
            print(f" - Total rows: {df.shape[0]}, Flood rows: {flood_df.shape[0]}")
        except Exception as e:
            print(f"[ERROR] Failed to process {file_path}: {e}")

    return pd.concat(flood_dfs, ignore_index=True)

# ------------------------
# 洪水確率の計算関数
# ------------------------
def flood_probability(temp, humd, coef, intercept):
    z = coef[0][0] * temp + coef[0][1] * humd + intercept[0]
    p = 1 / (1 + math.exp(-z))
    return p

# ------------------------
# メイン処理
# ------------------------

# 京都（通常時）データの読み込み
kyoto_df = pd.read_csv("data/kyoto_data.csv", encoding='shift_jis', skiprows=3)
kyoto_df.columns = kyoto_df.columns.str.strip()
kyoto_clean = preprocess_weather_data(kyoto_df, label=0)

# 洪水データをまとめて読み込み
flood_df = load_flood_data_from_folder("data/has_flood", threshold=10.0)

# 結合
combined_df = pd.concat([kyoto_clean, flood_df], ignore_index=True)

# モデル学習
X = combined_df[['気温(℃)', '相対湿度(％)']]
y = combined_df['flood_label']

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

# モデル評価
y_pred = model.predict(X_test)
print("\n=== 分類レポート ===")
print(classification_report(y_test, y_pred))
print("Model Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# テストデータで確率計算
sample_temp = 9
sample_humd = 100
p = flood_probability(sample_temp, sample_humd, model.coef_, model.intercept_)
print(f"\nSample Flood Probability = {p:.4f} ({p*100:.2f}%)")

# 統計表示
print("\n=== 統計情報 ===")
print(f"京都のデータ行数: {kyoto_df.shape[0]}")
print(f"洪水データの総行数: {flood_df.shape[0]}")
print(f"統合されたデータ行数: {combined_df.shape[0]}")
print("洪水ラベルのカウント:\n", combined_df['flood_label'].value_counts())

# データサンプル確認
print("\n=== データサンプル ===")
print(combined_df.head(20))
