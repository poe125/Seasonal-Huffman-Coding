import os
import matplotlib.pyplot as plt
import seaborn as sns

# ファイル名とラベル（季節別のファイル名を指定）
files = {
    # "no compression": {
    #     "spring": "output/uncompressed/spring.txt",
    #     "summer": "output/uncompressed/summer.txt",
    #     "fall": "output/uncompressed/fall.txt",
    #     "winter": "output/uncompressed/winter.txt"
    # },
    "seasonal huffman unweighted": {
        "spring": "output/huffman_unweighed/spring.txt",
        "summer": "output/huffman_unweighed/summer.txt",
        "fall": "output/huffman_unweighed/fall.txt",
        "winter": "output/huffman_unweighed/winter.txt"
    },
    "seasonal huffman weighted": {
        "spring": "output/huffman_weighed/spring.txt",
        "summer": "output/huffman_weighed/summer.txt",
        "fall": "output/huffman_weighed/fall.txt",
        "winter": "output/huffman_weighed/winter.txt"
    },
    "all season huffman unweighted": {
        "spring": "output/allseason_huffman_unweighed/spring.txt",
        "summer": "output/allseason_huffman_unweighed/summer.txt",
        "fall":   "output/allseason_huffman_unweighed/fall.txt",
        "winter": "output/allseason_huffman_unweighed/winter.txt"
    },
    "all season huffman weighted": {
        "spring": "output/allseason_huffman_weighed/spring.txt",
        "summer": "output/allseason_huffman_weighed/summer.txt",
        "fall":   "output/allseason_huffman_weighed/fall.txt",
        "winter": "output/allseason_huffman_weighed/winter.txt"
    },
    "zip compression": {
        "spring": "output/zip_compression/spring.zip",
        "summer": "output/zip_compression/summer.zip",
        "fall": "output/zip_compression/fall.zip",
        "winter": "output/zip_compression/winter.zip"
    }
}

# サイズ取得（バイト）
sizes = {method: {season: os.path.getsize(fname) for season, fname in season_files.items()} for method, season_files in files.items()}

# グラフ描画
fig, axes = plt.subplots(1, 4, figsize=(20, 5), sharey=True)

# 色リスト
# 色リスト（より見やすい色に変更）
colors =['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854']

method_labels = [
    "seasonal\nhuffman\nunweighted",  
    "seasonal\nhuffman\nweighted", 
    "all season\nhuffman\nunweighted",  
    "all season\nhuffman\nweighted",  
    "zip\ncompression"  
]
for i, season in enumerate(["spring", "summer", "fall", "winter"]):
    ax = axes[i]
    season_sizes = [sizes[method].get(season, 0) for method in files.keys()]
    ax.bar(files.keys(), season_sizes, color=colors)
    ax.set_title(f"{season.capitalize()}")
    ax.set_ylabel("File Size (bytes)")
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # 数値ラベルを追加
    for j, size in enumerate(season_sizes):
        ax.text(j, size + 50, f"{size}B", ha='center', fontsize=10)

    ax.set_xticklabels(method_labels)
    
plt.tight_layout()
plt.show()
