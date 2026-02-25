# Archimedean Spiral

Gerador de espiral de Arquimedes em Python, com visualização, exportação DXF e add-in para Fusion 360.

## Estrutura

```
core/spiral.py                        # Algoritmo puro (stdlib only)
tests/test_spiral.py                  # Testes unitários
scripts/plot.py                       # Visualização matplotlib
adapters/dxf/export.py                # Exportação DXF
adapters/fusion360/ArchimedeanSpiral/ # Add-in Fusion 360
```

## Comandos

```bash
make test              # Roda os testes
make plot              # Renderiza a espiral
make dxf               # Exporta spiral.dxf
make dxf DXF_OUT=x.dxf # Saída customizada
```

## Parâmetros

| Parâmetro | Descrição |
| --- | --- |
| `r_start` | Raio interno (mm) |
| `r_end` | Raio externo (mm) — diâmetro total = `2 × r_end` |
| `turns` | Número de voltas |
| `points_per_turn` | Resolução angular (36 = bom para impressão 3D) |

## Presets

**Mini-vinyl decorativo** (diâmetro 94mm, imprimível com nozzle 0.4mm):

```
r_start=15  r_end=47  turns=32  points_per_turn=36
```

**LP real** (12", dimensões físicas — usar via DXF, não Fusion 360):

```
r_start=50  r_end=146  turns=320  points_per_turn=360
```

## Fusion 360

1. Copie `adapters/fusion360/ArchimedeanSpiral/` para a pasta de add-ins:
   - macOS: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`
   - Windows: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`
2. **Tools → Add-ins** → selecione `ArchimedeanSpiral` → **Run**
3. O comando aparece em **Solid → Create → Archimedean Spiral**

> Mantenha `turns × points_per_turn < 2000` para evitar travamento.
> Para volumes altos de pontos, use `make dxf` e importe via **Insert → Insert DXF**.
