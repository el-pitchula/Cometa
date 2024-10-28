import torch
import torch.nn as nn
from torchvision import transforms

class ModeloIA(nn.Module):
    def __init__(self):
        super(ModeloIA, self).__init__()
        self.camadas = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(16*128*128, 10)  # Exemplo para imagens 256x256
        )

    def forward(self, x):
        return self.camadas(x)

def carregar_modelo_ia():
    modelo = ModeloIA()
    modelo.load_state_dict(torch.load("models/modelo_ia.pth"))
    modelo.eval()
    return modelo

def rodar_ia(modelo, imagem):
    transformacao = transforms.Compose([transforms.ToTensor(), transforms.Resize((256, 256))])
    imagem_tensor = transformacao(imagem).unsqueeze(0)
    resultado = modelo(imagem_tensor)
    return resultado
