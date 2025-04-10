import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
import time

model_path = os.path.join("model", "letter_cnn.h5")
model = load_model(model_path)

try:
    data = np.load("model/dataset/letter_dataset.npz")
except FileNotFoundError:
    print("Dataset not found. Please run model/dataset/create_dataset.py to create it.")
    raise

class_names = data["classes"]

def segment_letters_and_boxes(img_array, threshold=0.99):
    """
    Rozdělí obrázek na jednotlivé sub-obrázky písmen
    Vrátí list sub-obrázků (np.array) a bounding boxy (rmin, cmin, rmax, cmax)
    
    - img_array: 2D numpy pole
    - threshold=0.99: 99% pixelů ve sloupci musí být bílých, aby se považoval za mezeru
    """
    height, width = img_array.shape
    
    blank_columns = []
    for x in range(width):
        col = img_array[:, x]

        white_ratio = np.mean(col > 0.95)
        if white_ratio >= threshold:
            blank_columns.append(x)
    
    segments = []
    start_col = 0

    blank_columns.append(width)

    for bc in blank_columns:
        if bc - start_col > 10:  
            sub_img = img_array[:, max(0, start_col) : min(bc, width)]

            cropped, (rmin, cmin, rmax, cmax) = crop_to_bounding_box_with_coords(sub_img, start_col)
            segments.append((cropped, (rmin, cmin, rmax, cmax)))
        start_col = bc + 1

    return segments

def crop_to_bounding_box_with_coords(sub_img, col_offset=0, margin=30):
    """ 
    Ořízne 2D pole podle nejkrajnějších černých pixelů a přidá bílé pozadí
    """
    rows = np.any(sub_img < 0.95, axis=1) 
    cols = np.any(sub_img < 0.95, axis=0) 
    h, w = sub_img.shape
    if not np.any(rows) or not np.any(cols):
        return sub_img, (0, col_offset, h-1, col_offset+w-1)

    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    rmin = max(0, rmin - margin)
    rmax = min(rmax + margin, h - 1)
    cmin = max(0, cmin - margin)
    cmax = min(cmax + margin, w - 1)
    cropped = sub_img[rmin:rmax+1, cmin:cmax+1]

    Rmin = rmin
    Rmax = rmax
    Cmin = cmin + col_offset
    Cmax = cmax + col_offset

    box_h = rmax - rmin + 1
    box_w = cmax - cmin + 1
    box_size = max(box_h, box_w)

    square = np.ones((box_size, box_size), dtype=np.float32) 
    y_offset = (box_size - box_h) // 2
    x_offset = (box_size - box_w) // 2
    square[y_offset:y_offset + box_h, x_offset:x_offset + box_w] = cropped
    cropped = square

    return cropped, (Rmin, Cmin, Rmax, Cmax)

def predict_word_from_image(img_array, expected_word=None):
    """
    Posílá obrázek do modelu a ten vrátí rozpoznané písmeno
    """
    segments = segment_letters_and_boxes(img_array, threshold=0.99)
    recognized_word = ""

    for i, (sub_img_cropped, (rmin, cmin, rmax, cmax)) in enumerate(segments):
        pil_img = Image.fromarray((sub_img_cropped * 255).astype("uint8"))
        
        pil_img = pil_img.resize((28, 28))
        sub_arr = np.array(pil_img).astype("float32") / 255.0
        sub_arr = sub_arr.reshape((1, 28, 28, 1))
        pred = model.predict(sub_arr)
        class_idx = np.argmax(pred, axis=1)[0]
        predicted_letter = class_names[class_idx]
        recognized_word += predicted_letter

    return recognized_word
