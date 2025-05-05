import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

kyoto_df = pd.read_csv("data/kyoto_data.csv", encoding='shift_jis', skiprows=3)
yamagata_df = pd.read_csv("data/yamagata_data.csv", encoding='shift_jis', skiprows=3)
sakata_df = pd.read_csv("data/sakata_data.csv", encoding='shift_jis', skiprows=3)
suzu_df = pd.read_csv("data/suzu_data.csv", encoding='shift_jis', skiprows=3)
wajima_df = pd.read_csv("data/wajima_data.csv", encoding='shift_jis', skiprows=3)

# 列名の整形と確認
kyoto_df.columns = kyoto_df.columns.str.strip()
yamagata_df.columns = yamagata_df.columns.str.strip()
sakata_df.columns = sakata_df.columns.str.strip()
suzu_df.columns = suzu_df.columns.str.strip()
wajima_df.columns = wajima_df.columns.str.strip()

kyoto_df.columns, yamagata_df.columns, sakata_df.columns, suzu_df.columns, wajima_df.columns

# 必要なカラムだけ抽出し、日付変換
def preprocess_weather_data(df, label):
    df = df[['年月日時', '気温(℃)', '相対湿度(％)', '降水量(mm)']].copy()
    df['年月日時'] = pd.to_datetime(df['年月日時'], errors='coerce')
    df = df.dropna(subset=['年月日時'])  # 無効な日時は削除
    df['flood_label'] = label
    return df

# 京都（通常）→ 洪水なし = 0
kyoto_clean = preprocess_weather_data(kyoto_df, label=0)

def has_flood(df, month, date):
    clean = preprocess_weather_data(df, label=1)
    flood = clean[
    (clean['年月日時'].dt.month == month) &
    (clean['年月日時'].dt.day.isin([date, date+1, date+2]))
    ].copy()
    return flood

yamagata_flood = has_flood(yamagata_df, 7, 24)
sakata_flood = has_flood(sakata_df, 7, 24)
suzu_flood = has_flood(suzu_df, 9, 20)
wajima_flood = has_flood(suzu_df, 9, 20)

# データ統合
combined_df = pd.concat([kyoto_clean, yamagata_flood, sakata_flood, suzu_flood, wajima_flood], ignore_index=True)

combined_df.head()

# 特徴量と目的変数
X = combined_df[['気温(℃)', '相対湿度(％)']]
y = combined_df['flood_label']

# 学習データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

# ロジスティック回帰モデル
model = LogisticRegression()
model.fit(X_train, y_train)

# 予測＆レポート
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

print(model.coef_)   # [a, b]
print(model.intercept_)  # c

import math

def flood_probability(temp, humd, coef, intercept):
    z = coef[0][0] * temp + coef[0][1] * humd + intercept[0]
    p = 1 / (1 + math.exp(-z))
    return p

p = flood_probability(16.6, 83, model.coef_, model.intercept_)
print(f"Flood probability = {p:.4f} ({p*100:.2f}%)")

