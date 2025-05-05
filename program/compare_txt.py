import os
import matplotlib.pyplot as plt

# ファイル名とラベル（季節別のファイル名を指定）
files = {
    "no compression": {
        "spring": "output/uncompressed/spring.txt",
        "summer": "output/uncompressed/summer.txt",
        "fall": "output/uncompressed/fall.txt",
        "winter": "output/uncompressed/winter.txt"
    },
    "huffman unweighted": {
        "allseason": "output/huffman_unweighed/allseason.txt",
        "spring": "output/huffman_unweighed/spring.txt",
        "summer": "output/huffman_unweighed/summer.txt",
        "fall": "output/huffman_unweighed/fall.txt",
        "winter": "output/huffman_unweighed/winter.txt"
    },
    "huffman weighted": {
        "allseason": "output/huffman_weighed/allseason.txt",
        "spring": "output/huffman_weighed/spring.txt",
        "summer": "output/huffman_weighed/summer.txt",
        "fall": "output/huffman_weighed/fall.txt",
        "winter": "output/huffman_weighed/winter.txt"
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
fig, axes = plt.subplots(1, 5, figsize=(20, 5), sharey=True)

# 色リスト
colors = ['skyblue', 'salmon', 'lightgreen', 'gray']
method_labels = [
    "no\ncompression",
    "huffman\nunweighted",  # 改行を入れる
    "huffman\nweighted",  # 改行を入れる
    "zip\ncompression"  # 改行を入れる
]
for i, season in enumerate(["allseason", "spring", "summer", "fall", "winter"]):
    ax = axes[i]
    season_sizes = [sizes[method].get(season, 0) for method in files.keys()]
    ax.bar(files.keys(), season_sizes, color=colors)
    ax.set_title(f"{season.capitalize()}")
    ax.set_xlabel("Compression Method")
    ax.set_ylabel("File Size (bytes)")
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # 数値ラベルを追加
    for j, size in enumerate(season_sizes):
        ax.text(j, size + 50, f"{size}B", ha='center', fontsize=10)

    ax.set_xticklabels(method_labels)
    
plt.tight_layout()
plt.show()
