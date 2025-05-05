import pandas as pd

def to_binary_string(value, bit_length=16):
    """小数も含む値を整数スケールで2進数化（例: 23.5 → 2350 → 2進数）"""
    scaled = int(round(value * 100))  # 小数2桁まで残すようにスケーリング
    return format(scaled, f'0{bit_length}b')  # 指定ビット長で0埋め

def export_raw_binary(df, output_file_path):
    """気温と湿度を2進数に変換し、改行区切りで出力。NaNはスキップし、改行回数を表示。"""
    line_count = 0

    with open(output_file_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            temp = row['気温(℃)']
            humd = row['相対湿度(％)']
            
            if pd.isna(temp) or pd.isna(humd):
                continue  # 欠損値はスキップ
            
            temp_bin = to_binary_string(temp)
            humd_bin = to_binary_string(humd)
            f.write(temp_bin + ' ' + humd_bin + '\n')
            line_count += 1

    print(f"書き出し完了：{output_file_path}")
    print(f"raw dataの総送信回数：{line_count}")
