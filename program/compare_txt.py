import os
import matplotlib.pyplot as plt

# ファイル名とラベル（あらかじめ処理後のファイルを保存しておく）
files = {
    "no compression": "output/uncompressed_binary.txt",
    "huffman humidity": "output/encoded_humd_huff.txt",
    "uncompressed send if flood": "output/uncompressed_if_flood.txt",
    "zip compression": "output/compressed.zip"
}

# サイズ取得（バイト）
sizes = [os.path.getsize(fname) for fname in files.values()]

# グラフ描画
plt.figure(figsize=(8, 5))
plt.bar(files.keys(), sizes, color=['skyblue', 'salmon', 'lightgreen', 'gray'])
plt.title("各方式による圧縮サイズ比較", fontsize=14)
plt.ylabel("ファイルサイズ (bytes)", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 数値ラベルも表示
for i, size in enumerate(sizes):
    plt.text(i, size + 50, f"{size}B", ha='center', fontsize=10)

plt.tight_layout()
plt.show()
