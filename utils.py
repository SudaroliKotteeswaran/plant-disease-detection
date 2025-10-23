import os
import json
import logging
from PIL import Image
import numpy as np

logging.basicConfig(level=logging.INFO, filename='logs/cropcli.log',
                    format='%(asctime)s %(levelname)s: %(message)s')

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def ensure_dirs():
    for d in ['models','logs','data']:
        os.makedirs(d, exist_ok=True)

def load_image_as_array(path, target_size=(224,224)):
    try:
        img = Image.open(path).convert('RGB')
        img = img.resize(target_size)
        arr = np.array(img)
        return arr
    except Exception as e:
        logging.error(f"load_image_as_array error for {path}: {e}")
        raise

def print_table(rows, col_widths=None):
    # rows: list of lists (table)
    if not rows: 
        return
    if col_widths is None:
        col_widths = [max(len(str(cell)) for cell in col) + 2 for col in zip(*rows)]
    for r in rows:
        line = ""
        for i, cell in enumerate(r):
            w = col_widths[i] if i < len(col_widths) else 20
            line += str(cell).ljust(w)
        print(line)
