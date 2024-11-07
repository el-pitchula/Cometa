import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
from scipy import ndimage, fftpack

class AstronomicalImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Astronomical Object Detection")
        
        # Variáveis de imagem
        self.original_image = None
        self.filtered_image = None
        
        # Interface gráfica
        self.create_widgets()
    
    def create_widgets(self):
        # Botões para carregar imagem, aplicar filtro e executar IA
        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack()
        
        self.filter_button = tk.Button(self.root, text="Apply Butterworth Filter", command=self.apply_butterworth_filter)
        self.filter_button.pack()
        
        self.ai_button = tk.Button(self.root, text="Detect Celestial Objects", command=self.run_ai_model)
        self.ai_button.pack()
        
        # Canvas para imagem original e processada
        self.original_canvas = tk.Canvas(self.root, width=300, height=300)
        self.original_canvas.pack()
        
        self.processed_canvas = tk.Canvas(self.root, width=300, height=300)
        self.processed_canvas.pack()
        
        # Rótulo de status
        self.status_label = tk.Label(self.root, text="Status: Ready")
        self.status_label.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if not file_path:
            return
        
        # Carregar a imagem original
        self.original_image = Image.open(file_path).convert("L")  # Escala de cinza
        self.display_image(self.original_image, self.original_canvas)
        self.status_label.config(text="Image loaded successfully")

    def display_image(self, image, canvas):
        # Redimensionar imagem para caber no canvas
        img = image.resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.image = img_tk

    def apply_butterworth_filter(self, cutoff=0.1, order=2):
        if self.original_image is None:
            messagebox.showerror("Error", "Please load an image first.")
            return
        
        # Converte a imagem em array para aplicar o filtro Butterworth
        img_array = np.array(self.original_image)
        
        # Calcula a transformada de Fourier da imagem
        f_transform = fftpack.fftshift(fftpack.fft2(img_array))
        
        # Cria o filtro Butterworth
        rows, cols = img_array.shape
        crow, ccol = rows // 2 , cols // 2
        u = np.arange(-crow, crow)
        v = np.arange(-ccol, ccol)
        U, V = np.meshgrid(u, v)
        D = np.sqrt(U**2 + V**2)
        
        # Define o filtro Butterworth
        butterworth_filter = 1 / (1 + (D / (cutoff * crow))**(2 * order))
        
        # Aplica o filtro Butterworth na imagem
        f_transform_filtered = f_transform * butterworth_filter
        img_filtered = fftpack.ifft2(fftpack.ifftshift(f_transform_filtered))
        img_filtered = np.abs(img_filtered)
        
        # Converte o resultado em uma imagem do PIL para exibição
        self.filtered_image = Image.fromarray(img_filtered).convert("L")
        self.display_image(self.filtered_image, self.processed_canvas)
        self.status_label.config(text="Butterworth filter applied")

    def run_ai_model(self):
        if self.filtered_image is None:
            messagebox.showerror("Error", "Please apply a filter to the image first.")
            return

        # Pré-processamento da imagem filtrada para o modelo
        img = self.filtered_image.resize((224, 224))  # Ajuste ao tamanho esperado pelo modelo
        img_array = np.array(img) / 255.0  # Normalização
        img_array = np.expand_dims(img_array, axis=-1)  # Canal único
        img_array = np.expand_dims(img_array, axis=0)  # Dimensão de batch

        # Carregar o modelo customizado para detecção astronômica
        self.status_label.config(text="Loading AI model for astronomical detection...")
        model = tf.keras.models.load_model("path_to_your_trained_model.h5")

        # Executa a detecção
        self.status_label.config(text="Detecting celestial objects...")
        prediction = model.predict(img_array)
        label = "Object Detected" if prediction[0][0] > 0.5 else "No Object Detected"

        # Atualiza o status com o resultado da IA
        self.status_label.config(text=f"AI model result: {label}")

# Inicializa a aplicação
root = tk.Tk()
app = AstronomicalImageApp(root)
root.mainloop()
