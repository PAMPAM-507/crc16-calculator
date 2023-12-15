

import tkinter as tk
from tkinter import filedialog
import binascii
import os

import sys

class Form1:
    def __init__(self, root):
        self.root = root
        root.title("CRC16")
        
        self.lbl_polynomial = tk.Label(root, text="Polynomial")
        self.lbl_polynomial.grid(row=0, column=2, padx=5, pady=5)

        self.txt_polynomial = tk.Entry(root)
        self.txt_polynomial.insert(0, "0x8005")  # CRC-16-IBM
        self.txt_polynomial.grid(row=0, column=1, padx=5, pady=5)

        self.txt_file_path = tk.Entry(root)
        self.txt_file_path.grid(row=1, column=1, padx=5, pady=5)

        self.txt_result = tk.Entry(root)
        self.txt_result.grid(row=4, column=1, padx=5, pady=5)

        self.btn_browse = tk.Button(root, text="Browse", command=self.browse)
        self.btn_browse.grid(row=1, column=2, padx=5, pady=5)

        self.btn_calculate = tk.Button(root, text="Calculate", command=self.calculate)
        self.btn_calculate.grid(row=2, column=1, padx=5, pady=5)

    def calculate_crc16(self, data, polynomial, initial_value=0, xor_out=0):
        crc = initial_value

        for byte_value in data:
            data_byte = byte_value
            crc ^= (data_byte << 8)
            
            for _ in range(8):
                if (crc & 0x8000) != 0:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc <<= 1
            # print(crc)

        return crc ^ xor_out

    def browse(self):
        file_path = filedialog.askopenfilename()
        self.txt_file_path.delete(0, tk.END)
        self.txt_file_path.insert(0, file_path)

    def calculate(self):
        file_path = self.txt_file_path.get()

        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found")

        with open(file_path, 'rb') as file:
            data = file.read()

            # print(data)

        polynomial = int(self.txt_polynomial.get(), 16)

        crc16 = self.calculate_crc16(data, polynomial)
        # print(hex(crc16))

        crc16 = int((str(hex(crc16))[0]+str(hex(crc16))[1]+str(hex(crc16))[-4:]), 16)
        
        self.txt_result.delete(0, tk.END)
        self.txt_result.insert(0, f"{crc16:04X}")



if __name__ == "__main__":
    root = tk.Tk()
    app = Form1(root)
    root.mainloop()

