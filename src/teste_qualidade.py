import cv2
import numpy as np
from tkinter import filedialog, Tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

def load_image():
    Tk().withdraw()
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if filename:
        return cv2.imread(filename, cv2.IMREAD_GRAYSCALE)  # Carrega em escala de cinza para facilitar o processamento
    return None

def gaussian_blur(image, kernel_size=5):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def unsharp_mask(image, strength=1.5, blur_kernel=5):
    blurred = gaussian_blur(image, kernel_size=blur_kernel)
    sharpened = cv2.addWeighted(image, 1 + strength, blurred, -strength, 0)
    return sharpened

def high_pass_filter(image, kernel_size=3):
    kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def histogram_equalization(image):
    return cv2.equalizeHist(image)

def process_image(image):
    # Passo 1: Suavização inicial
    smoothed = gaussian_blur(image)

    # Passo 2: Aplicação de Unsharp Masking para nitidez
    sharpened = unsharp_mask(smoothed)

    # Passo 3: Realce adicional com Filtro Passa-Alta
    high_pass = high_pass_filter(sharpened)

    # Passo 4: Equalização de Histograma
    final_image = histogram_equalization(high_pass)
    return final_image

# Carrega a imagem e processa
original_image = load_image()
if original_image is not None:
    processed_image = process_image(original_image)

    # Exibe antes e depois
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(original_image, cmap="gray")
    
    plt.subplot(1, 2, 2)
    plt.title("Enhanced Image")
    plt.imshow(processed_image, cmap="gray")
    plt.show()
else:
    print("Nenhuma imagem foi carregada.")
