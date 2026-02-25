# Archimedean Spiral

Gerador de espiral de Arquimedes em Python — com adapter para Fusion 360 e exportação DXF.

## Estrutura

```
core/
  spiral.py                   # Algoritmo puro (stdlib only)
tests/
  test_spiral.py              # Testes unitários
scripts/
  plot.py                     # Visualização com matplotlib
adapters/
  dxf/
    export.py                 # Exportação para DXF (ezdxf)
  fusion360/
    ArchimedeanSpiral/        # Add-in para Fusion 360
```

## Uso rápido

```bash
make plot   # Renderiza a espiral com matplotlib
make dxf    # Exporta para spiral.dxf
make test   # Roda os testes unitários
make help   # Lista todos os comandos
```

### DXF com parâmetros customizados

```bash
# Saída customizada
make dxf DXF_OUT=meu_vinyl.dxf

# Via Python direto
python adapters/dxf/export.py --r-start 15 --r-end 47 --turns 32 mini_vinyl.dxf
```

Requer: `pip install ezdxf`

## Parâmetros

| Parâmetro | Descrição |
|---|---|
| `r_start` | Raio interno (mm) |
| `r_end` | Raio externo (mm) — o diâmetro total é `2 × r_end` |
| `turns` | Número de voltas |
| `points_per_turn` | Resolução angular — ver tabela abaixo |

### Resolução recomendada (`points_per_turn`)

| Valor | Sagitta em r=47mm | Uso |
|---|---|---|
| 24 | 0.40 mm | Fusion 360 (fitted spline interpola) |
| 36 | 0.18 mm | DXF + impressão 3D (nozzle 0.4mm) |
| 48 | 0.10 mm | DXF alta qualidade |

> **Nota:** Diâmetro total = `2 × r_end`. Para um disco de 100mm de diâmetro, use `r_end = 50mm`.

## Mini-vinyl decorativo (impressão 3D, diâmetro 94mm)

```
r_start = 15 mm   (label central)
r_end   = 47 mm   (diâmetro = 94mm, borda silenciosa de 3mm)
turns   = 32      (groove pitch ≈ 1.0mm — imprimível com nozzle 0.4mm)
```

## Adapter Fusion 360

### Instalação

1. Copie `adapters/fusion360/ArchimedeanSpiral/` para a pasta de add-ins do Fusion 360:
   - **macOS:** `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`
   - **Windows:** `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`
2. No Fusion 360: **Tools → Add-ins → Add-ins** → selecione `ArchimedeanSpiral` → **Run**
3. O comando aparece em **Solid → Create → Archimedean Spiral**

### Uso no Fusion 360

O dialog abre com os defaults do vinyl real (Neumann SX-74):

| Campo | Default |
|---|---|
| Inner Radius | 50 mm |
| Outer Radius | 146 mm |
| Turns | 25 |
| Points per Turn | 36 |

> **Limite seguro:** mantenha `turns × points_per_turn < 2000` para evitar travamento.

Após executar, clique em **Finish Sketch** — os fit points somem e apenas a curva fica visível.

## Adapter DXF

Alternativa ao Fusion 360 API: gera o arquivo localmente e importa via **Insert → Insert DXF**.
Sem limite de pontos, sem travamento.
