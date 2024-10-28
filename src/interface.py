import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from utils import carregar_imagem, salvar_imagem

def criar_interface(modelo, filtro_butterworth, filtro_fourier):
    root = tk.Tk()
    root.title("Processamento de Imagens Astronômicas")
    
    def carregar_e_exibir_imagem():
        file_path = filedialog.askopenfilename()
        imagem = carregar_imagem(file_path)
        imagem_label.config(text=f"Imagem Carregada: {file_path}")

    def aplicar_filtro(filtro):
        resultado = filtro(imagem)
        salvar_imagem(resultado, "imagem_filtrada.png")
        resultado_label.config(text="Filtro aplicado com sucesso!")

    imagem_label = ttk.Label(root, text="Carregar uma imagem")
    imagem_label.pack()
    
    carregar_btn = ttk.Button(root, text="Carregar Imagem", command=carregar_e_exibir_imagem)
    carregar_btn.pack()
    
    filtro_butter_btn = ttk.Button(root, text="Aplicar Filtro Butterworth", command=lambda: aplicar_filtro(filtro_butterworth))
    filtro_butter_btn.pack()
    
    filtro_fourier_btn = ttk.Button(root, text="Aplicar Filtro Fourier", command=lambda: aplicar_filtro(filtro_fourier))
    filtro_fourier_btn.pack()

    resultado_label = ttk.Label(root, text="")
    resultado_label.pack()
    
    root.mainloop()
