import cv2
import numpy as np

def calculate_harvey_shack_scatter(wavelength_nm=550, rms_roughness_um=0.8):
    """Calcula o fator de espalhamento óptico (TIS) baseado na rugosidade da lente."""
    lam = wavelength_nm * 1e-3
    tis = (4 * np.pi * rms_roughness_um / lam) ** 2
    return max(0.0, min(1.0, 1.0 - np.exp(-tis)))

def advanced_vmt_haze_simulation(image_path, roughness_level=1.2):
    """Simula o impacto do haze de borossilicato na extração de bordas 6DoF."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        img = np.zeros((400, 600), dtype=np.uint8)
        cv2.rectangle(img, (150, 100), (450, 300), 200, -1)
        cv2.line(img, (150, 100), (200, 50), 200, 3)

    scatter_factor = calculate_harvey_shack_scatter(rms_roughness_um=roughness_level)
    kernel_size = int(roughness_level * 15) | 1
    haze_layer = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    degraded = cv2.addWeighted(img, 1.0 - (scatter_factor * 0.5), haze_layer, scatter_factor * 0.5, 0)

    edges_clean = cv2.Canny(img, 100, 200)
    edges_degraded = cv2.Canny(degraded, 100, 200)

    loss_ratio = 1.0 - (np.count_nonzero(edges_degraded) / max(1, np.count_nonzero(edges_clean)))
    estimated_spatial_error_mm = loss_ratio * 12.5

    print(f"[VMT Physics Engine] Fator de Espalhamento (TIS): {scatter_factor * 100:.2f}%")
    print(f"[VMT Metrology] Degradação de Arestas: {loss_ratio * 100:.2f}%")
    print(f"[VMT Metrology] Desvio Métrico Estimado no Robô: {estimated_spatial_error_mm:.2f} mm")

    return degraded, estimated_spatial_error_mm

if __name__ == "__main__":
    advanced_vmt_haze_simulation("lens_target.png", roughness_level=1.2)
