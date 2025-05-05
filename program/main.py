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
file_paths_fall_table = [path for path in glob.glob("data/fall/*.csv") if os.path.isfile(path)]
file_paths_winter_table = [path for path in glob.glob("data/winter/*.csv") if os.path.isfile(path)]
file_paths_allseason_table = [path for path in glob.glob("data/all_season/*.csv") if os.path.isfile(path)]

file_path_test_spring = "data/spring/nago_data.csv"
file_path_test_summer = "data/summer/suzu_data.csv"
file_path_test_fall = "data/fall/hikone_data.csv"
file_path_test_winter = "data/winter/nagoya_data.csv"

df_list_spring_table = []
df_list_summer_table = []
df_list_fall_table = []
df_list_winter_table = []
df_list_allseason = []

coef = [[0.79935496, 0.45529708]]
intercept =[-57.14600964]

def main():
    # 90%以上の時のみのdata file
    for file_path in file_paths_allseason_table:
        print(file_path)
        df = read_data(file_path)
        if df is None:
            return
        df_list_allseason.append(df)
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
    for file_path in file_paths_fall_table:
        print(file_path)
        df = read_data(file_path)
        if df is None:
            return
        df_list_fall_table.append(df)
    for file_path in file_paths_winter_table:
        print(file_path)
        df = read_data(file_path)
        if df is None:
            return
        df_list_winter_table.append(df)
        
    df_test_spring = read_data(file_path_test_spring)
    if df_test_spring is None:
            return
    df_test_summer = read_data(file_path_test_summer)
    if df_test_summer is None:
            return
    df_test_fall = read_data(file_path_test_fall)
    if df_test_fall is None:
            return
    df_test_winter = read_data(file_path_test_winter)
    if df_test_winter is None:
            return
        
    # 頻度分布の取得
    huffman_temp_table_allseasonw, huffman_humd_table_allseasonw           = return_huffman_table(df_list_allseason)
    huffman_temp_table_allseason,  huffman_humd_table_allseason = return_unweighted_huffman_table(df_list_allseason)
    
    huffman_temp_table_springw, huffman_humd_table_springw           = return_huffman_table(df_list_spring_table)
    huffman_temp_table_spring,  huffman_humd_table_spring = return_unweighted_huffman_table(df_list_spring_table)
    
    huffman_temp_table_summerw, huffman_humd_table_summerw           = return_huffman_table(df_list_summer_table)
    huffman_temp_table_summer,  huffman_humd_table_summer = return_unweighted_huffman_table(df_list_summer_table)
    
    huffman_temp_table_fallw, huffman_humd_table_fallw           = return_huffman_table(df_list_fall_table)
    huffman_temp_table_fall,  huffman_humd_table_fall = return_unweighted_huffman_table(df_list_fall_table)
    
    huffman_temp_table_winterw, huffman_humd_table_winterw           = return_huffman_table(df_list_winter_table)
    huffman_temp_table_winter,  huffman_humd_table_winter = return_unweighted_huffman_table(df_list_winter_table)
    
    print('HUFFMAN TABLE with weight')
    print('ALL SEASON')
    print('temperature: \n' , huffman_temp_table_allseasonw)
    print('humidity: \n' ,    huffman_humd_table_allseasonw)
    print('SPRING')
    print('temperature: \n' , huffman_temp_table_springw)
    print('humidity: \n' ,    huffman_humd_table_springw)
    print('SUMMER')
    print('temperature: \n' , huffman_temp_table_summerw)
    print('humidity: \n' ,    huffman_humd_table_summerw)
    print('FALL')
    print('temperature: \n' , huffman_temp_table_fallw)
    print('humidity: \n' ,    huffman_humd_table_fallw)
    print('WINTER')
    print('temperature: \n' , huffman_temp_table_winterw)
    print('humidity: \n' ,    huffman_humd_table_winterw)
    
    print('HUFFMAN TABLE')
    print('ALL SEASON')
    print('temperature: \n' , huffman_temp_table_allseason)
    print('humidity: \n' ,    huffman_humd_table_allseason)
    print('SPRING')
    print('temperature: \n' , huffman_temp_table_spring)
    print('humidity: \n' ,    huffman_humd_table_spring)
    print('SUMMER')
    print('temperature: \n' , huffman_temp_table_summer)
    print('humidity: \n' ,    huffman_humd_table_summer)
    print('FALL')
    print('temperature: \n' , huffman_temp_table_fall)
    print('humidity: \n' ,    huffman_humd_table_fall)
    print('WINTER')
    print('temperature: \n' , huffman_temp_table_winter)
    print('humidity: \n' ,    huffman_humd_table_winter)
    
    
    #--------------------ALLSEASON-------------------------#
    encode_critical_data(df_test_summer,huffman_temp_table_allseasonw,huffman_humd_table_allseasonw,
    coef,intercept,output_file_path="output/allseason_huffman_weighed/summer.txt")
    encode_critical_data(df_test_summer,huffman_temp_table_allseason,huffman_humd_table_allseason,
    coef,intercept,output_file_path="output/allseason_huffman_unweighed/summer.txt") 
    
    encode_critical_data(df_test_spring,huffman_temp_table_allseasonw,huffman_humd_table_allseasonw,
    coef,intercept,output_file_path="output/allseason_huffman_weighed/spring.txt")
    encode_critical_data(df_test_spring,huffman_temp_table_allseason,huffman_humd_table_allseason,
    coef,intercept,output_file_path="output/allseason_huffman_unweighed/spring.txt") 
    
    encode_critical_data(df_test_fall,huffman_temp_table_allseasonw,huffman_humd_table_allseasonw,
    coef,intercept,output_file_path="output/allseason_huffman_weighed/fall.txt")
    encode_critical_data(df_test_fall,huffman_temp_table_allseason,huffman_humd_table_allseason,
    coef,intercept,output_file_path="output/allseason_huffman_unweighed/fall.txt") 
    
    encode_critical_data(df_test_winter,huffman_temp_table_allseasonw,huffman_humd_table_allseasonw,
    coef,intercept,output_file_path="output/allseason_huffman_weighed/winter.txt")
    encode_critical_data(df_test_winter,huffman_temp_table_allseason,huffman_humd_table_allseason,
    coef,intercept,output_file_path="output/allseason_huffman_unweighed/winter.txt") 
    
    #---------------------------SPRING----------------------------#
    encode_critical_data(df_test_spring,huffman_temp_table_springw,huffman_humd_table_springw,
    coef,intercept,output_file_path="output/huffman_weighed/spring.txt")
    encode_critical_data(df_test_spring,huffman_temp_table_spring,huffman_humd_table_spring,
    coef,intercept,output_file_path="output/huffman_unweighed/spring.txt")
    
    # 無圧縮2進数形式データ出力
    output_path = 'output/uncompressed/spring.txt'
    export_raw_binary_if_flood(df_test_spring, output_path, coef, intercept)
    
    #--------------------------SUMMER--------------------#
    encode_critical_data(df_test_summer,huffman_temp_table_summerw,huffman_humd_table_summerw,
    coef,intercept,output_file_path="output/huffman_weighed/summer.txt")
    encode_critical_data(df_test_summer,huffman_temp_table_summer,huffman_humd_table_summer,
    coef,intercept,output_file_path="output/huffman_unweighed/summer.txt")
    
    # 無圧縮2進数形式データ出力
    output_path = 'output/uncompressed/summer.txt'
    export_raw_binary_if_flood(df_test_summer, output_path, coef, intercept)
    
    #--------------------------FALL--------------------#
    encode_critical_data(df_test_fall,huffman_temp_table_fallw,huffman_humd_table_fallw,
    coef,intercept,output_file_path="output/huffman_weighed/fall.txt")
    encode_critical_data(df_test_fall,huffman_temp_table_fall,huffman_humd_table_fall,
    coef,intercept,output_file_path="output/huffman_unweighed/fall.txt")
    
    # 無圧縮2進数形式データ出力
    output_path = 'output/uncompressed/fall.txt'
    export_raw_binary_if_flood(df_test_fall, output_path, coef, intercept)
    
    #--------------------------WINTER--------------------#
    encode_critical_data(df_test_winter,huffman_temp_table_winterw,huffman_humd_table_winterw,
    coef,intercept,output_file_path="output/huffman_weighed/winter.txt")
    encode_critical_data(df_test_winter,huffman_temp_table_winter,huffman_humd_table_winter,
    coef,intercept,output_file_path="output/huffman_unweighed/winter.txt")
    
    # 無圧縮2進数形式データ出力
    output_path = 'output/uncompressed/winter.txt'
    export_raw_binary_if_flood(df_test_winter, output_path, coef, intercept)

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
    