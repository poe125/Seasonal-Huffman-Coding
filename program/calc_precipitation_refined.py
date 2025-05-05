import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import math

# ------------------------
# データ読み込み
# ------------------------
kyoto_df = pd.read_csv("data/kyoto_data.csv", encoding='shift_jis', skiprows=3)
yamagata_df = pd.read_csv("data/yamagata_data.csv", encoding='shift_jis', skiprows=3)
sakata_df = pd.read_csv("data/sakata_data.csv", encoding='shift_jis', skiprows=3)
suzu_df = pd.read_csv("data/suzu_data.csv", encoding='shift_jis', skiprows=3)
wajima_df = pd.read_csv("data/wajima_data.csv", encoding='shift_jis', skiprows=3)

# ------------------------
# 初期処理
# ------------------------
def preprocess_weather_data(df, label):
    df = df[['年月日時', '気温(℃)', '相対湿度(％)', '降水量(mm)']].copy()
    df['年月日時'] = pd.to_datetime(df['年月日時'], errors='coerce')
    df = df.dropna(subset=['年月日時'])
    df = df.dropna()  # 気温・湿度・降水量すべてにNaNがないように
    df['flood_label'] = label
    return df

kyoto_df.columns = kyoto_df.columns.str.strip()
yamagata_df.columns = yamagata_df.columns.str.strip()
sakata_df.columns = sakata_df.columns.str.strip()
suzu_df.columns = suzu_df.columns.str.strip()
wajima_df.columns = wajima_df.columns.str.strip()

kyoto_clean = preprocess_weather_data(kyoto_df, label=0)  # 通常時

# ------------------------
# 降水量基準の洪水データ抽出
# ------------------------
def extract_flood_by_rain(df, threshold=10.0):
    clean = preprocess_weather_data(df, label=1)
    flood = clean[clean['降水量(mm)'] >= threshold].copy()
    return flood

yamagata_flood = extract_flood_by_rain(yamagata_df)
sakata_flood = extract_flood_by_rain(sakata_df)
suzu_flood = extract_flood_by_rain(suzu_df)
wajima_flood = extract_flood_by_rain(wajima_df)

# ------------------------
# 結合 & 学習
# ------------------------
combined_df = pd.concat([
    kyoto_clean,
    yamagata_flood,
    sakata_flood,
    suzu_flood,
    wajima_flood
], ignore_index=True)

X = combined_df[['気温(℃)', '相対湿度(％)']]
y = combined_df['flood_label']

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

# ------------------------
# 評価 & 結果
# ------------------------
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print("Model Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# ------------------------
# 洪水確率の計算関数
# ------------------------
def flood_probability(temp, humd, coef, intercept):
    z = coef[0][0] * temp + coef[0][1] * humd + intercept[0]
    p = 1 / (1 + math.exp(-z))
    return p

# テスト
sample_temp = 16.6
sample_humd = 83
p = flood_probability(sample_temp, sample_humd, model.coef_, model.intercept_)
print(f"Flood probability = {p:.4f} ({p*100:.2f}%)")

print(f"京都データ: {kyoto_df.shape[0]} 行")
print(f"山形データ: {yamagata_df.shape[0]} 行")
print(f"酒田データ: {sakata_df.shape[0]} 行")
print(f"鈴データ: {suzu_df.shape[0]} 行")
print(f"輪島データ: {wajima_df.shape[0]} 行")

# 降水量が10mm以上のデータが正しく抽出されているか確認
print("京都の降水量10mm以上:", kyoto_df[kyoto_df['降水量(mm)'] >= 10].shape[0])
print("山形の降水量10mm以上:", yamagata_df[yamagata_df['降水量(mm)'] >= 10].shape[0])
print("酒田の降水量10mm以上:", sakata_df[sakata_df['降水量(mm)'] >= 10].shape[0])
print("鈴の降水量10mm以上:", suzu_df[suzu_df['降水量(mm)'] >= 10].shape[0])
print("輪島の降水量10mm以上:", wajima_df[wajima_df['降水量(mm)'] >= 10].shape[0])

combined_df = pd.concat([kyoto_clean, yamagata_flood, sakata_flood, suzu_flood, wajima_flood], ignore_index=True)
print(f"統合されたデータ行数: {combined_df.shape[0]}")
print("統合後、洪水ラベルのカウント: \n", combined_df['flood_label'].value_counts())

# 統合されたデータの洪水ラベルのカウント
print("統合後、洪水ラベルのカウント:")
print(combined_df['flood_label'].value_counts())

print("京都のデータでflood_label = 1の数:", kyoto_clean['flood_label'].sum())
print("山形のデータでflood_label = 1の数:", yamagata_flood['flood_label'].sum())
print("酒田のデータでflood_label = 1の数:", sakata_flood['flood_label'].sum())
print("鈴のデータでflood_label = 1の数:", suzu_flood['flood_label'].sum())
print("輪島のデータでflood_label = 1の数:", wajima_flood['flood_label'].sum())

# 統合後のデータのサンプルを表示
print(combined_df.head(20))  # 最初の20行を確認
