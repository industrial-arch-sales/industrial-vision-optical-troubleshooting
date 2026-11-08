import numpy as np

def evaluate_coating_integrity(estimated_error_mm, target_thickness_um=40.0, tolerance_pct=10.0):
    """
    Valida se o desvio espacial gerado pelo erro óptico compromete 
    a micragem do Clear Coat e força o CLP a operar em malha aberta.
    """
    max_allowed_error = target_thickness_um * (tolerance_pct / 100.0)
    
    print(f"[Metrology Validator] Desvio Espacial Calculado: {estimated_error_mm:.2f} mm")
    print(f"[Metrology Validator] Tolerância Máxima Admissível: {max_allowed_error:.2f} um equivalentes")
    
    if estimated_error_mm > (max_allowed_error * 0.1):
        print("[ALERTA CRÍTICO] Integridade do processo comprometida! Risco de sub-espessura ou escorridos.")
        print("[AÇÃO RECOMENDADA] Ativar polimento com Óxido de Cério (CeO2) e restaurar malha fechada.")
        return False
    
    print("[STATUS] Processo estável dentro da faixa nominal.")
    return True

if __name__ == "__main__":
    # Simula validação com base em um desvio projetado de 2.5 mm
    evaluate_coating_integrity(estimated_error_mm=2.5)
