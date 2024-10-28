import cv2
import numpy as np

def load_and_display_image(filepath):
    image = cv2.imread(filepath)
    if image is None:
        raise ValueError("A imagem não foi encontrada ou o caminho está incorreto.")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
