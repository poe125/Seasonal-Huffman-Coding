import math
import pandas as pd

# 洪水確率の計算関数
def flood_probability(temp, humd, coef, intercept):
    z = coef[0][0] * temp + coef[0][1] * humd + intercept[0]
    p = 1 / (1 + math.exp(-z))
    return p

# 2進数に変換する関数（100倍して16bitで表現）
def to_binary_string(value, bit_length=16):
    scaled = int(round(value * 100))
    return format(scaled, f'0{bit_length}b')

# メイン処理：確率70%以上のデータのみ書き出す
def export_raw_binary_if_flood(df, output_file_path, coef, intercept):
    line_count = 0

    with open(output_file_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            temp = row['気温(℃)']
            humd = row['相対湿度(％)']
            
            if pd.isna(temp) or pd.isna(humd):
                continue

            prob = flood_probability(temp, humd, coef, intercept)

            if prob >= 0.9 and prob <= 1:
                # print(prob)
                # print(temp)
                # print(humd)
                temp_bin = to_binary_string(temp)
                humd_bin = to_binary_string(humd)
                f.write(temp_bin + humd_bin + '\n')
                line_count += 1

    print(f"洪水確率90%以上の無圧縮データ点数（送信回数）：{line_count}")
    print(f"出力完了：{output_file_path}")
