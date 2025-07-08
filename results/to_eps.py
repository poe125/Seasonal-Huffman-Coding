from PIL import Image

input_file = "final_experimental_result.png"
output_file = "final_experimental_result.eps"

# 画像を開く
img = Image.open(input_file)

# RGBAやPモードだった場合、RGBに変換する
if img.mode in ("RGBA", "P"):
    img = img.convert("RGB")

# EPS形式で保存
img.save(output_file, format='EPS')

print("EPS変換 完了！→", output_file)
