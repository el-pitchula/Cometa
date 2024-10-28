from PIL import Image
import numpy as np

def carregar_imagem(caminho):
    imagem = Image.open(caminho).convert('L')
    return np.array(imagem)

def salvar_imagem(imagem, caminho):
    imagem = Image.fromarray(imagem)
    imagem.save(caminho)
