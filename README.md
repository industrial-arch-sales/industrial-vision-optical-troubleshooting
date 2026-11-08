# Industrial Vision & Optical Troubleshooting: VMT / Eisenmann 3D Vision Recovery & Risk Architecture

## 📌 Visão Geral do Projeto (Executive Summary)
Repositório técnico focado no diagnóstico de causa raiz, modelagem matemática de erros, análise de risco sistêmico (FMEA de longo prazo) e recuperação de ativos ópticos em sistemas de visão computacional 3D (Eisenmann/VMT) aplicados a células robóticas de pintura automotiva (*Clear Coat* / Verniz).

O projeto soluciona uma taxa de imprecisão geométrica inicial de **46.1%** que forçava o CLP a operar crônica e perigosamente em malha aberta (*Bypass*) em modelos críticos de carrocerias. A intervenção elimina um risco de CAPEX de **R$ 149.500,00** em substituição desnecessária de hardware e mitiga passivos ocultos de conformidade e garantia de longo prazo através de polimento químico-mecânico com Óxido de Cério e reengenharia de procedimento padrão.

---

## 🔍 O Problema de Campo & Diagnóstico de Causa Raiz
- **Sintoma Crítico:** Logs de erro recorrentes no sistema indicando `Result inaccurate` e desvios de deformação métrica atingindo picos de `8.5 mm` em células robotizadas Yaskawa.
- **Causa Raiz Física (Abrasão Destrutiva):** Agressão contínua à lente de borossilicato (Dureza **5.5 Mohs**) devido ao procedimento operacional histórico de limpeza com mantas abrasivas de óxido de alumínio (Dureza **9.0 Mohs** / *Scotch-Brite*). 
- **Efeito Óptico (*Haze* e Difração):** Os micro-sulcos gerados na superfície provocam espalhamento da luz (descrito pela física de rugosidade RMS e dispersão Harvey-Shack), gerando retenção por capilaridade de verniz poliuretano curado ($n \approx 1.5$). Isso corrompe os vetores de translação e rotação 6DOF, criando falsos positivos e "bordas fantasmas" que impedem o alinhamento geométrico perfeito pelo VMT.

---

## 🏛️ Análise de Risco Sistêmico & O Passivo Oculto

### 1. A Ilusão da Amostragem e o Cego Regulatório (Auditoria Interna vs. Externa)
* **Viés de Amostragem Interna:** As auditorias de qualidade internas operam sob severa restrição de tempo, limitando-se a verificar os **mesmos pontos padronizados (superfícies planas e de fácil acesso)** onde o robô executa o leque sem desvios severos.
* **A Blindspot Geométrica:** Os desvios de micragem e erros 6DoF não ocorrem nas áreas planas, mas nas **zonas de alta curvatura e transições complexas** da carroceria. O uso continuado de *Bypass* oculta a degradação do VMT, gerando variações invisíveis na espessura do filme polimérico.
* **Passivo Oculto de Longo Prazo (1 a 2 Anos):** Defeitos de micragem em superfícies curvas não aparecem no *flash-off* imediato (erros superficiais menores são mascarados pelo polimento estético de linha). O risco real manifesta-se em campo após a entrega ao cliente: degradação precoce da proteção UV, delaminação, falha no perfil de cura sob estufa e microfissuramentos por tensão térmica, abrindo margem para multas pesadas e contestações em auditorias externas (ex: VDA 6.3 / ISO).

### 2. A Irracionalidade do Procedimento Manual Legado (*O Banquinho e o Scotch-Brite*)
* **Inviabilidade Ergonômica:** O protocolo anterior exigia que o operador utilizasse um suporte improvisado (*banquinho*) para tentar alcançar o painel óptico, cobrindo apenas uma fração restrita ($1/4$ a $2/4$) da área efetiva de visibilidade.
* **Destruição Metalúrgica Cruzada:** O uso de *Scotch-Brite* (Dureza 9.0) contra o borossilicato (Dureza 5.5) é um erro estrutural de engenharia: o abrasivo consome a matriz vítrea em vez de remover o verniz catalisado.
* **Inviabilidade de *Downtime* para Retrofit Físico:** Parar a linha de montagem automotiva para realizar a troca completa de subsistemas ópticos ou redesenhar a infraestrutura da célula geraria perdas financeiras intoleráveis por inatividade.

---

## 🛠️ Stack Tecnológica & Competências Aplicadas
- **Visão Computacional & OpenCV:** Processamento de imagem, binarização, operações morfológicas e análise de difração e degradação de bordas (*Canny / Edge Loss*).
- **Engenharia de Automação & Robótica:** Integração de CLPs Siemens, arquitetura de malha fechada/aberta e robôs de pintura industrial Yaskawa.
- **Engenharia de Confiabilidade & Análise de Riscos:** Mitigação de passivos ocultos, otimização de CAPEX e conformidade com padrões metrológicos automotivos.

---

## 💻 PoC: Simulação de Degradação Óptica e Efeito Haze (`haze_simulation.py`)
Script em Python desenvolvido para simular computacionalmente o impacto da difração de luz (*haze*) e quantificar a perda de integridade nas features de alinhamento 6DoF:

```python
import cv2
import numpy as np

def simulate_optical_haze(image_path, severity=15):
    """
    Simula o efeito de difração (Haze) causado por micro-sulcos em lentes ópticas
    e avalia a degradação na detecção de bordas para algoritmos 6DoF em células VMT.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        # Mock sintético de geometria de carroceria se a imagem de teste não existir
        img = np.zeros((300, 500), dtype=np.uint8)
        cv2.rectangle(img, (150, 100), (350, 200), 255, -1)
    
    # Simulação do espalhamento óptico (efeito catarata / haze)
    kernel_size = severity * 2 + 1
    haze = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    degraded = cv2.addWeighted(img, 0.6, haze, 0.4, 0)
    
    # Detecção de bordas Canny (simulando a extração de features do VMT)
    edges_clean = cv2.Canny(img, 100, 200)
    edges_degraded = cv2.Canny(degraded, 100, 200)
    
    # Métricas de perda de definição de borda
    loss_ratio = 1.0 - (np.count_nonzero(edges_degraded) / max(1, np.count_nonzero(edges_clean)))
    estimated_spatial_error_mm = loss_ratio * 12.5
    
    print(f"[VMT Simulation] Perda de nitidez de borda estimada: {loss_ratio * 100:.2f}%")
    print(f"[VMT Metrology] Desvio métrico espacial projetado no robô: {estimated_spatial_error_mm:.2f} mm")
    
    return degraded, edges_degraded

if __name__ == "__main__":
    simulate_optical_haze("sample_lens.png", severity=10)

```

---

## 📐 Conclusão Pragmática da Intervenção

A substituição de procedimentos empíricos pelo polimento químico-mecânico in-situ com **Óxido de Cério ($CeO_2$)** representa a solução ótima (Pareto 80/20):

1. **Restauração Óptica Instantânea:** Recupera a transmitância a níveis $>98\%$ sem paradas prolongadas de linha.
2. **Eliminação do Risco Contratual:** Força o retorno do CLP à malha fechada, garantindo a uniformidade de micragem em áreas de alta curvatura e blindando a planta contra auditorias externas rigorosas.
3. **Proteção Patrimonial:** Preserva os ativos existentes e elimina desperdícios de CAPEX.
