# Microfluidic Droplet Generation CFD Simulation

CFD simulation of droplet generation in a Drop-seq flow-focusing microfluidic chip for monoclonal bead encapsulation using ANSYS Fluent (2D VOF).

## Structure

- `SIMULATION_GUIDE.md` — material properties, flow parameters, dimensionless numbers, DoE matrix
- `FLUENT_SETUP.md` — step-by-step ANSYS Fluent setup (click-by-click)
- `PAPER_DRAFT.md` — conference paper draft with placeholder values
- `dxf_to_step.py` — converts chip DXF geometry to STEP for ANSYS import
- `pyproject.toml` — Python dependencies (cadquery, ezdxf)

## System

- **Chip**: 26-generator Drop-seq, 125 um channel depth, flow-focusing junction
- **Oil**: Bio-Rad EvaGreen Generation Oil (HFE-7500 + PFPE-PEG surfactant)
- **Aqueous**: water + 5% Pluronic F68 + 1% BSA
- **Target**: ~4000 Hz droplet generation, 100-120 um diameter, CV < 15%

## DXF to STEP

```
uv sync
uv run python dxf_to_step.py
```

Reads `generator.dxf` from the project root.
