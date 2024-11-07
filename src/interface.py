import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing with AI and Filters")
        self.root.state("zoomed")  # Abre a janela maximizada em tela cheia
        
        # Configura o estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TButton", background="#4e4e4e", foreground="white", font=("Helvetica", 12, "bold"))
        style.configure("TLabel", background="#2e2e2e", foreground="white", font=("Helvetica", 12))
        
        # Frame principal para divisão das áreas
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Painel esquerdo para controles e ajustes
        control_panel = ttk.Frame(main_frame, width=250, relief="sunken", padding=10)
        control_panel.pack(side="left", fill="y")
        
        # Área central para exibição das imagens
        display_panel = ttk.Frame(main_frame, padding=10)
        display_panel.pack(side="left", fill="both", expand=True)

        # Barra de status
        self.status_label = ttk.Label(self.root, text="Welcome to Image Processing App", anchor="w")
        self.status_label.pack(side="bottom", fill="x")

        # Controles no Painel de Controle
        ttk.Label(control_panel, text="Image Processing Options").pack(pady=5)
        
        load_button = ttk.Button(control_panel, text="Load Image", command=self.load_image)
        load_button.pack(fill="x", pady=5)
        
        filter_button = ttk.Button(control_panel, text="Apply Butterworth Filter", command=self.apply_butterworth_filter)
        filter_button.pack(fill="x", pady=5)
        
        ai_button = ttk.Button(control_panel, text="Run AI Model", command=self.run_ai_model)
        ai_button.pack(fill="x", pady=5)
        
        # Slider para ajuste de parâmetros de filtro
        ttk.Label(control_panel, text="Filter Frequency Cutoff").pack(pady=5)
        self.cutoff_slider = ttk.Scale(control_panel, from_=1, to=100, orient="horizontal")
        self.cutoff_slider.set(50)
        self.cutoff_slider.pack(fill="x", pady=5)

        # Configuração de Exibição de Imagem
        self.original_label = ttk.Label(display_panel, text="Original Image")
        self.original_label.pack(pady=5)
        
        self.processed_label = ttk.Label(display_panel, text="Processed Image")
        self.processed_label.pack(pady=5)

        self.original_canvas = tk.Canvas(display_panel, width=400, height=400, bg="gray")
        self.original_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        self.processed_canvas = tk.Canvas(display_panel, width=400, height=400, bg="gray")
        self.processed_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Inicializa as variáveis
        self.original_image = None
        self.processed_image = None

    def load_image(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if image_path:
            self.original_image = Image.open(image_path)
            self.display_image(self.original_image, self.original_canvas)
            self.status_label.config(text="Image loaded successfully")

    def apply_butterworth_filter(self):
        if self.original_image is None:
            messagebox.showerror("Error", "Please load an image first.")
            return

        # Aplica o filtro Butterworth
        self.processed_image = self.butterworth_filter(self.original_image, cutoff=self.cutoff_slider.get())
        self.display_image(self.processed_image, self.processed_canvas)
        self.status_label.config(text="Butterworth filter applied")

    def butterworth_filter(self, image, cutoff):
        # Convertendo a imagem para escala de cinza
        img_gray = np.array(image.convert("L"))
        
        # Transformada de Fourier
        f_transform = np.fft.fftshift(np.fft.fft2(img_gray))
        rows, cols = img_gray.shape
        crow, ccol = rows // 2, cols // 2

        # Filtro Butterworth
        mask = np.zeros((rows, cols), dtype=np.float32)
        for i in range(rows):
            for j in range(cols):
                d = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
                mask[i, j] = 1 / (1 + (d / cutoff) ** (2 * 2))
                # if (passa-alta)

        filtered_shifted = f_transform * mask
        f_ishift = np.fft.ifftshift(filtered_shifted)
        img_back = np.abs(np.fft.ifft2(f_ishift))
        filtered_image = Image.fromarray(np.uint8(img_back)).convert("RGB")
        
        return filtered_image

    def run_ai_model(self):
        if self.original_image is None:
            messagebox.showerror("Error", "Please load an image first.")
            return
        
        # Placeholder para execução de modelo de IA
        self.status_label.config(text="Running AI model...")
        self.processed_image = self.original_image  # Substitua pela saída real do modelo de IA
        self.display_image(self.processed_image, self.processed_canvas)
        self.status_label.config(text="AI model executed")

    def display_image(self, image, canvas):
        canvas.image = ImageTk.PhotoImage(image.resize((400, 400)))
        canvas.create_image(0, 0, anchor="nw", image=canvas.image)

# Cria a janela principal e inicializa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
