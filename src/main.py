from interface import criar_interface
from ia import carregar_modelo_ia
from processamento import aplicar_filtro_butterworth, aplicar_filtro_fourier

def iniciar():
    modelo = carregar_modelo_ia()  # Carrega o modelo de IA
    criar_interface(modelo, aplicar_filtro_butterworth, aplicar_filtro_fourier)

if __name__ == "__main__":
    iniciar()
