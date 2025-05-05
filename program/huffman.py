import pandas as pd
import numpy as np
import heapq
import math
from collections import Counter
from send_if_flood import flood_probability

class Node: 
    def __init__(self, freq, symbol, left=None, right=None): 
        self.freq = freq 
        self.symbol = symbol 
        self.left = left 
        self.right = right 
        self.huff = '' 
  
    def __lt__(self, nxt): 
        return self.freq < nxt.freq

def read_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='shift_jis', skiprows=3)
    except Exception as e:
        print("Error reading the CSV file:", e)
        return None

    df.columns = df.columns.str.strip()

    #気温、相対湿度のみdfに入れる    
    selected_columns = ['気温(℃)', '相対湿度(％)']
    df = df[selected_columns]
    df = df.dropna(how='all')

    # dfの中身を表示
    # print(df)
    return df

def make_shared_table(temp_freq, humd_freq):
    """
    temperature と humidity の両方の範囲を共通で符号化する
    """
    # temperature の符号を先に作成
    temp_sorted_freq = temp_freq.sort_values(ascending=False)
    temp_symbols = [str(i) for i in temp_sorted_freq.index]
    
    nodes = []
    for x in range(len(temp_sorted_freq)):
        heapq.heappush(nodes, Node(temp_sorted_freq.values[x], temp_symbols[x]))
    
    # ハフマン符号を生成
    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)
        
        left.huff = 0
        right.huff = 1
        
        # 新しいノードを作成しキューに戻す
        new_node = Node(left.freq + right.freq, left.symbol + right.symbol, left, right)
        heapq.heappush(nodes, new_node)
    
    # 生成されたハフマン符号
    huffman_table = build_huffman_table(nodes[0])

    # humidity の符号を temperature と同じ順序で割り当て
    humd_sorted_freq = humd_freq.sort_values(ascending=False)
    humd_symbols = [str(i) for i in humd_sorted_freq.index]
    
    # 既存の temperature 符号に基づいて humidity 符号を設定
    humd_huffman_table = {}
    for i, symbol in enumerate(humd_symbols):
        # temperature と同じ順番で符号を割り当てる
        humd_huffman_table[symbol] = huffman_table[temp_symbols[i]]
    
    return huffman_table, humd_huffman_table

def return_unweighted_huffman_table(df_list):
    all_temp_bins = []
    all_humd_bins = []

    for df in df_list:
        temp_bins, humd_bins = get_bins(df)
        all_temp_bins.extend(temp_bins)
        all_humd_bins.extend(humd_bins)

    # 重みなし頻度計算
    temp_freq_series = pd.Series(all_temp_bins).value_counts().sort_index()
    humd_freq_series = pd.Series(all_humd_bins).value_counts().sort_index()
    
    # print('temp freq series (unweighted):\n', temp_freq_series)

    # 共通テーブル生成
    temp_huffman_table, humd_huffman_table = make_shared_table(temp_freq_series, humd_freq_series)

    return temp_huffman_table, humd_huffman_table


def return_huffman_table(df_list):
    all_temp_freq = {}
    all_humd_freq = {}
    coef = [[1.36340201, 0.1514873]]
    intercept =[-39.16394441]
    for df in df_list:
        temp_bins, humd_bins = get_bins(df)

        # 洪水確率に基づく重みを計算
        weights = df.apply(
            lambda row: 2 if flood_probability(row['気温(℃)'], row['相対湿度(％)'], coef, intercept) >= 0.9 else 1,
            axis=1
        )

        temp_bins_series = pd.Series(temp_bins.values, index=df.index)
        humd_bins_series = pd.Series(humd_bins.values, index=df.index)

        # temp/humd ごとにグループ化して重み付き頻度を集計
        temp_freq = temp_bins_series.groupby(temp_bins_series, observed=False).apply(lambda grp: weights[grp.index].sum())
        humd_freq = humd_bins_series.groupby(humd_bins_series, observed=False).apply(lambda grp: weights[grp.index].sum())

        # 全体に加算
        for k, v in temp_freq.items():
            all_temp_freq[k] = all_temp_freq.get(k, 0) + v
        for k, v in humd_freq.items():
            all_humd_freq[k] = all_humd_freq.get(k, 0) + v

    # Series に変換してソート
    temp_freq_series = pd.Series(all_temp_freq).sort_index()
    humd_freq_series = pd.Series(all_humd_freq).sort_index()
    
    # print('temp freq series:\n',temp_freq_series)

    # 共通テーブルを生成
    temp_huffman_table, humd_huffman_table = make_shared_table(temp_freq_series, humd_freq_series)

    return temp_huffman_table, humd_huffman_table

def get_bins(df):
    nbins = 5 
    min_temp = int(df['気温(℃)'].min() - 5)
    max_temp = int(df['気温(℃)'].max() + 6)
    min_humd = max(0, int(df['相対湿度(％)'].min() - 20))
    max_humd = 100

    temp_bins_range = np.linspace(min_temp, max_temp, nbins + 1)
    humd_bins_range = np.linspace(min_humd, max_humd, nbins + 1)

    # 温度と湿度のヒストグラムを作成し、頻度分布を計算
    temperature_bins = pd.cut(df['気温(℃)'], bins=temp_bins_range)
    humidity_bins = pd.cut((df['相対湿度(％)']), bins=humd_bins_range)
    
    print('temp bins\n', temperature_bins)
    print('humd bins\n', humidity_bins)
    
    return temperature_bins, humidity_bins

def make_table(freq):
    nodes = []
    chars = [str(b) for b in freq.index]
    
    for x in range(len(freq)):
        heapq.heappush(nodes, Node(freq.values[x], chars[x]))
    
    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)
        
        left.huff = 0
        right.huff = 1
        
        # 新しいノードを作成しキューに戻す
        new_node = Node(left.freq + right.freq, left.symbol + right.symbol, left, right)
        heapq.heappush(nodes, new_node)
        
    huffman_table = build_huffman_table(nodes[0])    
    return huffman_table

def print_nodes_to_file(node, val='', output_file=None): 
    # huffman code for current node 
    new_val = val + str(node.huff) 
  
    # if node is not an edge node 
    if node.left: 
        print_nodes_to_file(node.left, new_val, output_file) 
    if node.right: 
        print_nodes_to_file(node.right, new_val, output_file) 
  
    # if node is edge node then display and save its huffman code 
    if not node.left and not node.right: 
        output = f"{node.symbol} -> {new_val}\n"
        print(output.strip())
        if output_file:
            output_file.write(output)

def huffman(nodes, chars, freq, output_file_path):
    # freq が Counter の場合は Pandas の Series に変換
    if isinstance(freq, Counter):
        freq = pd.Series(freq)
        
    #ノードを初期化
    nodes = []
    
    # ノードを優先度付きキューに追加
    for x in range(len(freq)):
        heapq.heappush(nodes, Node(freq.values[x], chars[x]))
    
    # ハフマン木を構築
    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)
        
        left.huff = 0
        right.huff = 1
        
        # 新しいノードを作成しキューに戻す
        new_node = Node(left.freq + right.freq, left.symbol + right.symbol, left, right)
        heapq.heappush(nodes, new_node)
    
    # ハフマン木を生成し、ハフマンコードを取得
    huffman_table = build_huffman_table(nodes[0])
    
    # 出力ファイルにノードと頻度を記録
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Character Frequencies:\n")
        for char, frequency in zip(chars, freq.values):
            output_file.write(f"{char}: {frequency}\n")
        output_file.write("\nHuffman Tree:\n")
        print_nodes_to_file(nodes[0], output_file=output_file)
    
    return huffman_table

def get_huffman_code_for_value(value, huffman_table):
    for range_key in huffman_table:
        lower, upper = map(float, range_key.strip('()[]').split(','))
        if lower < value <= upper:
            return huffman_table[range_key]
    return ""

def encode_critical_data(df, temp_table, humd_table, coef, intercept, output_file_path):
    def flood_probability(temp, humd, coef, intercept):
        z = coef[0][0] * temp + coef[0][1] * humd + intercept[0]
        p = 1 / (1 + math.exp(-z))
        return p

    buffer = ""  # ビット列を貯めておく
    writing = False  # 書き込み中かどうか

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for _, row in df.iterrows():
            temp = row['気温(℃)']
            humd = row['相対湿度(％)']
            prob = flood_probability(temp, humd, coef, intercept)

            if prob >= 0.9:
                temp_code = get_huffman_code_for_value(temp, temp_table)
                humd_code = get_huffman_code_for_value(humd, humd_table)

                if temp_code and humd_code:
                    buffer += temp_code + humd_code
                    writing = True

                    # 改行判定：11バイト（88ビット）を超えたら改行
                    while len(buffer) >= 88:
                        output_file.write(buffer[:88] + '\n')
                        buffer = buffer[88:]

            elif writing:
                # 書き込み中にflood_probが閾値以下になったら改行してリセット
                if buffer:
                    output_file.write(buffer + '\n')
                buffer = ""
                writing = False

        # 最後にバッファが残っていれば書き出す
        if buffer:
            output_file.write(buffer + '\n')
            
    temp_table.clear()
    humd_table.clear()




def build_huffman_table(node, val='', huffman_table=None):
    """
    ハフマン木を巡回し、シンボルと対応する2進数コードの辞書を構築する。
    """
    if huffman_table is None:
        huffman_table = {}
    
    new_val = val + str(node.huff)
    
    if node.left:
        build_huffman_table(node.left, new_val, huffman_table)
    if node.right:
        build_huffman_table(node.right, new_val, huffman_table)
    
    if not node.left and not node.right:
        huffman_table[node.symbol] = new_val
    return huffman_table
