import pandas as pd
import heapq
import glob
import os
from huffman import read_data, return_huffman_table, return_unweighted_huffman_table, encode_critical_data
from send_if_flood import export_raw_binary_if_flood
# from runlength import count_continued_num, get_count_freq, runlength
# from original_data import print_df

file_paths_spring_table = [path for path in glob.glob("data/spring/*.csv") if os.path.isfile(path)]
file_paths_summer_table = [path for path in glob.glob("data/summer/*.csv") if os.path.isfile(path)]
file_paths_autumn_table = [path for path in glob.glob("data/fall/*.csv") if os.path.isfile(path)]
file_paths_winter_table = [path for path in glob.glob("data/winter/*.csv") if os.path.isfile(path)]

file_path_test = "data/has_flood/wajima_data.csv"

df_list_spring_table = []
df_list_summer_table = []
df_list_autumn_table = []
df_list_winter_table = []

coef = [[1.36340201, 0.1514873]]
intercept =[-39.16394441]

def main():
    # 90%以上の時のみのdata file
    for file_path in file_paths_spring_table:
        print(file_path)
        df = read_data(file_path)
        if df is None:
            return
        df_list_spring_table.append(df)
    for file_path in file_paths_summer_table:
        print(file_path)
        df = read_data(file_path)
        if df is None:
            return
        df_list_summer_table.append(df)
    for file_path in file_paths_autumn_table:
        print(file_path)
        df = read_data(file_path)
        if df is None:
            return
        df_list_autumn_table.append(df)
    for file_path in file_paths_winter_table:
        print(file_path)
        df = read_data(file_path)
        if df is None:
            return
        df_list_winter_table.append(df)
    
    # 頻度分布の取得
    huffman_temp_table_springw, huffman_humd_table_springw           = return_huffman_table(df_list_spring_table)
    huffman_temp_table_spring,  huffman_humd_table_spring = return_unweighted_huffman_table(df_list_spring_table)
    
    huffman_temp_table_summerw, huffman_humd_table_summerw           = return_huffman_table(df_list_summer_table)
    huffman_temp_table_summer,  huffman_humd_table_summer = return_unweighted_huffman_table(df_list_summer_table)
    
    huffman_temp_table_autumnw, huffman_humd_table_autumnw           = return_huffman_table(df_list_autumn_table)
    huffman_temp_table_autumn,  huffman_humd_table_autumn = return_unweighted_huffman_table(df_list_autumn_table)
    
    huffman_temp_table_winterw, huffman_humd_table_winterw           = return_huffman_table(df_list_winter_table)
    huffman_temp_table_winter,  huffman_humd_table_winter = return_unweighted_huffman_table(df_list_winter_table)
    
    print('HUFFMAN TABLE with weight')
    print('SPRING')
    print('temperature: \n' , huffman_temp_table_springw)
    print('humidity: \n' ,    huffman_humd_table_springw)
    print('SUMMER')
    print('temperature: \n' , huffman_temp_table_summerw)
    print('humidity: \n' ,    huffman_humd_table_summerw)
    print('FALL')
    print('temperature: \n' , huffman_temp_table_autumnw)
    print('humidity: \n' ,    huffman_humd_table_autumnw)
    print('WINTER')
    print('temperature: \n' , huffman_temp_table_winterw)
    print('humidity: \n' ,    huffman_humd_table_winterw)
    
    print('HUFFMAN TABLE')
    print('SPRING')
    print('temperature: \n' , huffman_temp_table_spring)
    print('humidity: \n' ,    huffman_humd_table_spring)
    print('SUMMER')
    print('temperature: \n' , huffman_temp_table_summer)
    print('humidity: \n' ,    huffman_humd_table_summer)
    print('FALL')
    print('temperature: \n' , huffman_temp_table_autumn)
    print('humidity: \n' ,    huffman_humd_table_autumn)
    print('WINTER')
    print('temperature: \n' , huffman_temp_table_winter)
    print('humidity: \n' ,    huffman_humd_table_winter)
    
    
    
    #-------------------------------------------------------#
      
    # # データフレームをハフマン符号化
    # encodtemp_output_path = 'output/encoded_temp_huff.txt'
    # encodhumd_output_path = 'output/encoded_humd_huff.txt'
    
    encode_critical_data(df,huffman_temp_table_springw,huffman_humd_table_springw,
    coef,intercept,output_file_path="output/spring_huffman_weighted.txt")
    encode_critical_data(df,huffman_temp_table_spring,huffman_humd_table_spring,
    coef,intercept,output_file_path="output/spring_huffman_unweighted.txt")
    
    # 無圧縮2進数形式データ出力
    output_path = 'output/uncompressed_if_flood.txt'
    export_raw_binary_if_flood(df, output_path, coef, intercept)
    
main()

    # c_num = count_continued_num(encoded_data)
    # count_data = get_count_freq(c_num)
    # nodes = []
    # chars = list(count_data.keys())
    # freq = count_data
    # output_file_path = "runlength_output.txt"
    # runlength_table = huffman(nodes, chars, freq, output_file_path)
    # print("Huffman Codes:", runlength_table)
    
    # encoded_path = 'encoded_runlength.txt'
    # print(f"データをエンコード中...")
    # runlength(runlength_table, c_num, encoded_path)
    # print("エンコード完了")
    