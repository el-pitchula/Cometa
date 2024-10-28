import numpy as np
import cv2
from scipy.fft import fft2, ifft2, fftshift

def apply_gaussian_filter(image, kernel_size=5):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def apply_median_filter(image, kernel_size=5):
    return cv2.medianBlur(image, kernel_size)

def remove_noise_fourier(image, threshold=50):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    f_transform = fft2(gray)
    f_transform_shifted = fftshift(f_transform)
    
    rows, cols = gray.shape
    crow, ccol = rows // 2 , cols // 2

    f_transform_shifted[crow-threshold:crow+threshold, ccol-threshold:ccol+threshold] = 0
    f_transform_ishift = np.fft.ifftshift(f_transform_shifted)
    img_back = ifft2(f_transform_ishift)
    img_back = np.abs(img_back)
    return cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
