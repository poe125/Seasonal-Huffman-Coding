# About
This repository contains the implementation of seasonal Huffman coding, a data compression method designed for efficiently sending flood data through LoRaWAN. While the primary use case is flood data, the methods can be applied to other types of data compression as well.

These codes were used for the paper submitted to **COMPSAFE 2025**.

# Usage
1. Create Huffman Tree:
Use huffman.py to generate Huffman codes for your data.

2. Flood Probability Check:
Use send_if_flood.py to calculate flood probabilities and determine whether to send data.

# References
- Seasonal Huffman Coding for LoRaWAN data transmission (https://sigos.ipsj.or.jp/event/comsys2024/posters/ComSys_2024_poster_10.pdf)
- Japan Meteorological Agency datasets (https://www.data.jma.go.jp/risk/obsdl/index.php#)
  The flood data used in this repository is obtained from the Japan Meteorological Agency.
