import matplotlib.pyplot as plt

# 改行回数データ
data = {
    'Spring': {'Huffman Weighted': 69, 'Huffman Unweighted': 69},
    'Summer': {'Huffman Weighted': 63, 'Huffman Unweighted': 63},
    'Fall': {'Huffman Weighted': 12, 'Huffman Unweighted': 12},
    'Winter': {'Huffman Weighted': 0,  'Huffman Unweighted': 0}
}

seasons = list(data.keys())
weighted = [data[season]['Huffman Weighted'] for season in seasons]
unweighted = [data[season]['Huffman Unweighted'] for season in seasons]

x = range(len(seasons))
bar_width = 0.35

plt.bar([i - bar_width/2 for i in x], weighted, width=bar_width, label='Huffman Weighted')
plt.bar([i + bar_width/2 for i in x], unweighted, width=bar_width, label='Huffman Unweighted')

plt.xlabel('Season')
plt.ylabel('Number of Line Breaks (Chunks Sent)')
plt.title('Number of Chunks Sent per Season (Flood Probability >= 0.9)')
plt.xticks(x, seasons)
plt.legend()
plt.tight_layout()
plt.grid(True, linestyle='--', alpha=0.6)

plt.show()
