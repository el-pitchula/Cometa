import numpy as np
from filters import apply_gaussian_filter, apply_median_filter, remove_noise_fourier

def process_image(image, filter_type="Gaussian"):
    if filter_type == "Gaussian":
        return apply_gaussian_filter(image)
    elif filter_type == "Mediana":
        return apply_median_filter(image)
    elif filter_type == "Fourier":
        return remove_noise_fourier(image)
    else:
        raise ValueError(f"Filtro {filter_type} não é suportado.")
