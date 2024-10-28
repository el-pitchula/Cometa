import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from image_loader import load_and_display_image
from image_processing import process_image

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Processamento de Imagens Astronômicas")
        self.image_label = tk.Label(root, text="Nenhuma imagem carregada")
        self.image_label.pack(pady=10)

        self.original_image = None
        self.filtered_image = None

        self.btn_load = tk.Button(root, text="Carregar Imagem", command=self.load_image)
        self.btn_load.pack(pady=5)

        self.filter_var = tk.StringVar(value="Gaussian")
        self.filter_options = ttk.Combobox(root, textvariable=self.filter_var, values=["Gaussian", "Mediana", "Fourier"])
        self.filter_options.pack(pady=5)

        self.btn_apply_filter = tk.Button(root, text="Aplicar Filtro", command=self.apply_filter)
        self.btn_apply_filter.pack(pady=5)

        self.btn_save = tk.Button(root, text="Salvar Imagem Filtrada", command=self.save_image)
        self.btn_save.pack(pady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.original_image = load_and_display_image(file_path)
            self.display_image(self.original_image, "Imagem Original")
            self.filtered_image = None

    def apply_filter(self):
        if self.original_image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada!")
            return

        filter_type = self.filter_var.get()
        self.filtered_image = process_image(self.original_image, filter_type)
        self.display_image(self.filtered_image, f"Imagem Filtrada ({filter_type})")

    def display_image(self, img_array, title):
        img = Image.fromarray(img_array)
        img = img.resize((400, 300), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk
        self.image_label.config(text=title)

    def save_image(self):
        if self.filtered_image is None:
            messagebox.showwarning("Aviso", "Aplique um filtro antes de salvar!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.filtered_image, cv2.COLOR_RGB2BGR))
            messagebox.showinfo("Informação", "Imagem salva com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
