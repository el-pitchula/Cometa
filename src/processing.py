import numpy as np
from scipy import fftpack
from scipy.ndimage import gaussian_filter

def aplicar_filtro_butterworth(imagem, cutoff=30, ordem=2):
    h, w = imagem.shape[:2]
    u, v = np.meshgrid(range(w), range(h))
    d = np.sqrt((u - w//2)**2 + (v - h//2)**2)
    butterworth_filter = 1 / (1 + (d / cutoff)**(2 * ordem))
    imagem_fft = fftpack.fft2(imagem)
    imagem_fft_shift = fftpack.fftshift(imagem_fft)
    imagem_filtrada = fftpack.ifftshift(imagem_fft_shift * butterworth_filter)
    return np.abs(fftpack.ifft2(imagem_filtrada))

def aplicar_filtro_fourier(imagem):
    imagem_fft = fftpack.fft2(imagem)
    imagem_fft_shift = fftpack.fftshift(imagem_fft)
    return np.abs(fftpack.ifft2(imagem_fft_shift))
