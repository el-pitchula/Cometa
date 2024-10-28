from src.interface import ImageProcessingApp
import tkinter as tk

def main():
    # Inicializa a janela principal do Tkinter
    root = tk.Tk()
    
    # Instancia a aplicação de processamento de imagens
    app = ImageProcessingApp(root)
    
    # Inicia o loop da interface gráfica
    root.mainloop()

if __name__ == "__main__":
    main()
