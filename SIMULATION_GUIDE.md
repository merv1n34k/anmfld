# Drop-seq Microfluidics Simulation Guide — ANSYS Fluent

## 1. Chip Geometry Summary

The full chip contains **26 generators**. For the 2D CFD simulation, we model **one generator unit cell** using `generator_cropped.dxf`. The full chip (`dropseq_chip.dxf`) and single generator (`generator.dxf`) are shown in the paper for context.

### Channel Dimensions

The chip uses **4 distinct channel widths**. All channels share a **depth of 125 um**.

| Feature | Width (um) | DXF raw | Used for |
|---|---|---|---|
| Narrow channels | **50** | 1.27 | Side water inlets (w), oil inlet channels |
| Delivery channels | **78** | 1.98 | Horizontal oil/water delivery after 90° turns |
| **Nozzle throat** | **93.7** | 2.38 | Flow-focusing constriction (25% narrower than main) |
| Main channel | **125** | 3.175 | Center inlet (w+b), merged aqueous, downstream, serpentine |

DXF scaling factor: × 39.37 (raw DXF units → um). Channel depth = 125 um (square for main channel).

### Junction Type: Symmetric Flow-Focusing

**Flow topology (top to bottom):**

```
   Inlet(w)   Inlet(w+b)   Inlet(w)      ← 3 water inlets from top
   50 um       125 um       50 um
     |           |            |
     └───78um────┤────78um────┘            ← water merge via T-junctions
                 |                            (side water feeds into center)
   oil(78um) ────┤──── oil(78um)           ← flow-focusing junction
                 |                            (oil from both sides, perpendicular)
              ┌──┤──┐
              │93.7µ│                      ← THROAT — droplet pinch-off zone
              └──┤──┘                         (length ~62.5 um)
                 |
            125 um channel                 ← downstream vertical channel
                 |
                 └─── serpentine ──→ OUTLET ← zigzag (3.5 periods) → right side
```

### Junction Details

| Parameter | Value | Notes |
|---|---|---|
| Throat width | 93.7 um | 25% constriction from 125 um |
| Throat length | ~62.5 um | Vertical extent of narrowest section |
| Convergence half-angle | ~26.6° from horizontal (63.4° from axis) | Symmetric |
| Constriction ratio | 1.33:1 | 125/93.7 |

### Water Merge Region

The 3 water inlets combine **before** the oil junction:
- Center inlet (w+b): 125 um wide, flows straight down
- Left inlet (w): 50 um wide, curves 90° via arcs into 78 um horizontal channel, enters center channel via T-junction
- Right inlet (w): mirror of left
- Combined aqueous stream (125 um) continues ~78 um further before meeting oil

### Oil Entry

Two oil channels approach **vertically from below**, then turn **90° via arcs** into **horizontal channels** (78 um wide) that enter the junction perpendicular to the aqueous flow:
- Left oil: enters from the left at the junction
- Right oil: enters from the right (mirror)

### Serpentine (Downstream)

| Parameter | Value |
|---|---|
| Channel width | 125 um |
| Pattern | V-shaped zigzag, ~36.6° diagonals |
| Periods | 3.5 |
| Amplitude (peak-to-valley) | ~203 um |
| Total path length | ~1880 um |
| Exit | Right side → outlet |

---

## 2. Material Properties

### 2.1 Continuous Phase: Bio-Rad EvaGreen Droplet Generation Oil

Bio-Rad Droplet Generation Oil for EvaGreen (Cat. #1864005/1864006) is based on **HFE-7500** (3M Novec 7500, CAS 297730-93-9) with **Bis-Krytox-PEG** triblock copolymer surfactant at ~2.5 mM [1].

| Property | Value | Unit | Reference |
|---|---|---|---|
| Density (25°C) | **1614** | kg/m³ | 3M Novec 7500 TDS [2]; Rausch et al. 2015 [3] |
| Dynamic viscosity (25°C) | **1.24 × 10⁻³** | Pa·s | 3M TDS (ν = 0.77 cSt × ρ) [2] |
| Kinematic viscosity (25°C) | 7.7 × 10⁻⁷ | m²/s | 3M TDS [2] |

> The surfactant (~2.5 mM Bis-Krytox-PEG) does not significantly alter bulk density or viscosity of HFE-7500.

### 2.2 Dispersed Phase: Water + 5% Pluronic F68 + 1% BSA (20 mg/mL)

| Property | Value | Unit | Reference |
|---|---|---|---|
| Density (25°C) | **1015** | kg/m³ | Gradzielski et al. 2025 [4] (interpolated) |
| Dynamic viscosity (25°C) | **3.0 × 10⁻³** | Pa·s | Gradzielski et al. 2025 [4]; Monkos 1996 [5] |

**Density estimation**: 5% Pluronic F68 solution ≈ 1008-1010 kg/m³ (interpolated between 4% and 10% data from [4]), + 20 mg/mL BSA (partial specific volume 0.735 mL/g) adds ~5 kg/m³ → **~1015 kg/m³**.

**Viscosity estimation**: 5% P188 at 25°C ≈ 2.3-2.5 mPa·s (interpolated from [4]: 4% = 2.3 mPa·s, 10% = 4.5 mPa·s at 20°C, adjusted for temperature). BSA at 20 mg/mL adds ~15-30% relative viscosity increase [5] → combined **~3.0 mPa·s** at 25°C. Newtonian at these concentrations.

### 2.3 Interfacial Tension (Oil-Water)

| System | σ (mN/m) | Reference |
|---|---|---|
| HFE-7500 / pure water (bare) | 49.5 ± 0.5 | Brosseau et al. 2014 [6] |
| HFE-7500 + 2.2% PEG-Krytox / PBS | 0.54 | Calhoun et al. 2022 [7] |
| HFE-7500 + PFPE-PEG reference / water at CMC | 5.1 | Scanga et al. 2018 [8] |
| **Bio-Rad oil / (water + 5% P-F68 + BSA)** | **≈ 3.0** | **Estimated from [7,8]** |

> **Use σ = 3.0 × 10⁻³ N/m (3.0 mN/m)**. The Bio-Rad oil contains PFPE-PEG surfactant (equilibrium IFT 0.5-5 mN/m depending on aqueous composition [7,8]). We use 3.0 mN/m as a conservative mid-range estimate accounting for dynamic adsorption effects during high-frequency droplet generation.

### 2.4 Dynabeads M280 Streptavidin (analytical only — NOT in CFD)

| Property | Value | Unit | Reference |
|---|---|---|---|
| Diameter | 2.8 | um | Invitrogen datasheet [9] |
| Density | ~1400 | kg/m³ | Invitrogen datasheet [9] |
| Concentration (in w+b inlet) | 325 | beads/uL | System spec |

> Beads (2.8 um) are ~40× smaller than droplets. Not modeled in CFD. Bead statistics calculated analytically via Poisson distribution (Section 7.7).

---

## 3. Flow Rate Calculations

### 3.1 Flow Rates Per Generator

All flow rates are **per generator**. Each generator is independently controlled by Fluigent flow units. The 2 oil channels share one tubing line (flow splits equally). The 2 side water channels also share one tubing line.

| Tubing line | Pump flow rate | Splits into | Per-channel flow | Channel width |
|---|---|---|---|---|
| Oil | **250 uL/min** | 2 channels | **125 uL/min** each | 50 um |
| Water w/o beads | **67 uL/min** | 2 channels | **33.5 uL/min** each | 50 um |
| Water w/ beads | **67 uL/min** | 1 channel | **67 uL/min** | 125 um |

| Aggregate | Value | Unit |
|---|---|---|
| Total oil (Q_oil) | **250** | uL/min |
| Total water (Q_aq) | **134** | uL/min (67 + 33.5 × 2) |
| Total flow | **384** | uL/min |
| Flow ratio Q_oil / Q_aq | **1.87** | — |

### 3.2 Conversion to SI

| Parameter | Value | SI | Unit |
|---|---|---|---|
| Q_oil total | 250 uL/min | **4.167 × 10⁻⁹** | m³/s |
| Q_oil per channel | 125 uL/min | **2.083 × 10⁻⁹** | m³/s |
| Q_w+b (center) | 67 uL/min | **1.117 × 10⁻⁹** | m³/s |
| Q_w (each side) | 33.5 uL/min | **5.583 × 10⁻¹⁰** | m³/s |
| Q_aq total | 134 uL/min | **2.233 × 10⁻⁹** | m³/s |

### 3.3 Inlet Velocities (for Boundary Conditions)

Velocity = Q / (Width × Depth):

| Inlet | Channel size (W × D) | Velocity | Unit |
|---|---|---|---|
| Water center (w+b) | 125 × 125 um | **0.0715** | m/s (71.5 mm/s) |
| Water side (w), each | 50 × 125 um | **0.0893** | m/s (89.3 mm/s) |
| Oil, each channel | 50 × 125 um | **0.3333** | m/s (333.3 mm/s) |

**At the flow-focusing junction** (oil in 78 um delivery channels):

| Location | Channel size | Velocity |
|---|---|---|
| Oil at junction entry | 78 × 125 um | **0.2137 m/s** (213.7 mm/s) |
| Combined aqueous | 125 × 125 um | **0.1429 m/s** (142.9 mm/s) |
| **At throat** (all fluids) | 93.7 × 125 um | **0.547 m/s** (547 mm/s) |

### 3.4 Dimensionless Numbers

Evaluated at the **oil delivery channel** entering the junction (78 × 125 um, D_h = 96.1 um):

| Parameter | Formula | Value | Interpretation |
|---|---|---|---|
| Re_oil | ρ_oil × v × D_h / µ_oil | **26.7** | Laminar |
| Ca_oil | µ_oil × v / σ | **0.088** | Dripping regime (high end) |
| We_oil | ρ_oil × v² × D_h / σ | **2.37** | Inertia becoming relevant |

At the **throat** (93.7 × 125 um, D_h = 107.3 um):

| Parameter | Value | Notes |
|---|---|---|
| Re_throat | ~51 | Based on mixture velocity, laminar |
| Ca_throat | ~0.23 | Transition/jetting, confined |

> **Flow regime**: Ca_oil ≈ 0.09 places the system at the **dripping-to-jetting transition** [13], consistent with high-frequency droplet generation (~4000 Hz). The flow is fully laminar (Re << 2300) but not creeping — inertial effects are non-negligible at the throat.

---

## 4. ANSYS Fluent Setup — Step by Step

### 4.1 Geometry (SpaceClaim or DesignModeler)

**Import `generator_cropped.dxf`:**
1. Open SpaceClaim → File → Import → `generator_cropped.dxf`
2. Scale geometry so that the main channel width = **125 um** (scale factor from DXF: × 39.37, then convert to working units)
3. Verify key dimensions: side channels = 50 um, throat = 93.7 um
4. Create a 2D surface ("Fill" or "Surface from edges")
5. Create **Named Selections** for boundaries:
   - `inlet_water_beads` — center water+beads inlet (top, 125 um wide)
   - `inlet_water_left` — left plain water inlet (top, 50 um wide)
   - `inlet_water_right` — right plain water inlet (top, 50 um wide)
   - `inlet_oil_left` — left oil inlet (bottom-left, 50 um wide)
   - `inlet_oil_right` — right oil inlet (bottom-right, 50 um wide)
   - `outlet` — serpentine exit (right side)
   - `walls` — all remaining edges

> **Note for 2D**: The simulation domain may include the full cropped geometry or be further trimmed to just the junction + sufficient upstream/downstream. Including the serpentine is recommended for realistic outlet pressure conditions.

### 4.2 Meshing

| Parameter | Value | Notes |
|---|---|---|
| Mesh type | Quadrilateral dominant | Better for VOF interface tracking |
| Element size (global) | 5 um | General channel regions |
| Element size (throat/junction) | **2 um** | Critical droplet formation zone |
| Element size (throat core) | **1 um** | Interface capture refinement |
| Inflation layers | 5-8 layers | Near walls |
| First layer height | 0.5-1 um | Resolve near-wall flow |
| Growth rate | 1.2 | Gradual transition |
| Total elements (estimated) | 100,000-250,000 | Including serpentine |

**Mesh quality targets:**
- Orthogonal quality > 0.7
- Skewness < 0.5
- Aspect ratio < 5

**Refinement zones:**
1. **Junction/throat** — finest mesh (1-2 um), droplet formation
2. **First 500 um downstream** — fine mesh (2-3 um), droplet detachment
3. **Serpentine** — medium mesh (3-5 um), droplet transport

After meshing in Fluent:
- **Scale mesh**: Mesh → Scale → multiply ALL coordinates by **1e-6** (um → meters)

### 4.3 Fluent General Settings

| Setting | Value |
|---|---|
| Solver type | Pressure-Based |
| Time | **Transient** |
| 2D Space | Planar |
| Gravity | Off (Bo << 1 at microscale) |

### 4.4 Multiphase Model (VOF)

Navigate: **Models → Multiphase → Volume of Fluid**

| Setting | Value | Notes |
|---|---|---|
| Scheme | **Implicit** | Stable with Geo-Reconstruct, allows larger time steps |
| Number of phases | **2** | Oil + Water (see note below) |
| Body force formulation | **Implicit body force** | Stability with surface tension |
| Interface modeling | **Sharp** | |
| Volume fraction cutoff | 1 × 10⁻⁶ | Default |
| Courant number | 0.25 | For VOF interface tracking stability |

> **Why 2 phases, not 3?** All 3 aqueous streams have identical physical properties. The bead content (2.8 um particles at low concentration) does not affect bulk flow properties. Model as a single "water" phase. Bead statistics are computed analytically from the dilution ratio.

**Phase definitions:**
- Phase 1 (Primary): **Oil** (Bio-Rad EvaGreen oil) — continuous phase
- Phase 2 (Secondary): **Water** (5% Pluronic F68 + 1% BSA) — dispersed phase

**Phase interaction:**
- Surface tension coefficient: **3.0 × 10⁻³ N/m** (3.0 mN/m)
- Surface tension model: **Continuum Surface Force (CSF)** [10]
- Wall adhesion: **Enable**

### 4.5 Material Definitions

Create two custom materials (Materials → Create/Edit):

**Material 1: biorad-evagreen-oil** (assign to Phase 1)

| Property | Value | Reference |
|---|---|---|
| Density | 1614 kg/m³ | [2,3] |
| Viscosity | 1.24 × 10⁻³ Pa·s | [2] |

**Material 2: water-pluronic-bsa** (assign to Phase 2)

| Property | Value | Reference |
|---|---|---|
| Density | 1015 kg/m³ | [4,5] |
| Viscosity | 3.0 × 10⁻³ Pa·s | [4,5] |

### 4.6 Boundary Conditions

| Boundary | Type | Phase 1 (oil) | Phase 2 (water) |
|---|---|---|---|
| `inlet_oil_left` | Velocity inlet | v = **0.3333 m/s**, VF = **1** | VF = **0** |
| `inlet_oil_right` | Velocity inlet | v = **0.3333 m/s**, VF = **1** | VF = **0** |
| `inlet_water_beads` | Velocity inlet | (backflow VF = 0) | v = **0.0715 m/s**, VF = **1** |
| `inlet_water_left` | Velocity inlet | (backflow VF = 0) | v = **0.0893 m/s**, VF = **1** |
| `inlet_water_right` | Velocity inlet | (backflow VF = 0) | v = **0.0893 m/s**, VF = **1** |
| `outlet` | Pressure outlet | Gauge pressure = **0 Pa** | Backflow VF = 0 |
| `walls` | Wall | No-slip | Contact angle = **150°** |

**Contact angle:** HFE-7500 preferentially wets PDMS/glass walls. Water contact angle ~150° (through water phase) ensures oil remains continuous along walls [11].

### 4.7 Solver Settings

| Setting | Value | Notes |
|---|---|---|
| Pressure-velocity coupling | **PISO** | Recommended for transient VOF |
| Pressure discretization | **PRESTO!** | Recommended for VOF with surface tension |
| Momentum | **Second Order Upwind** | |
| Volume fraction | **Geo-Reconstruct** | Sharpest interface [12] |
| Transient formulation | **First Order Implicit** | Stable |

**Under-relaxation factors:**

| Parameter | Value |
|---|---|
| Pressure | 0.3 |
| Density | 1.0 |
| Body forces | 1.0 |
| Momentum | 0.7 |

### 4.8 Solution Initialization

1. **Initialize** entire domain with **oil** (Phase 1 VF = 1, Phase 2 VF = 0)
2. Use **Standard Initialization**
3. Set velocity = 0 everywhere, pressure = 0
4. **Patch** aqueous inlet channels with water (VF = 1) — the three top channels (from inlets down to the oil T-junction) should be pre-filled with water, matching the real priming procedure

### 4.9 Time Stepping

| Parameter | Value | Notes |
|---|---|---|
| Time step method | **Variable** | Controlled by global Courant number |
| Global Courant number | **0.25** | For VOF interface tracking stability |
| OR fixed time step | **2 × 10⁻⁷ s** (0.2 us) | Alternative (smaller than before due to higher velocities) |
| Max iterations per step | 20-30 | Per time step |
| Total simulation time | **0.005-0.01 s** (5-10 ms) | ~20-40 droplets for statistics |

**Timing:**
- At ~4000 Hz → one droplet every ~250 us
- 20 droplets = 5 ms + ~1-2 ms startup
- **Total: ~7-10 ms simulation time**
- Note: higher velocities require smaller time steps than previously estimated

### 4.10 Monitors and Data Export

1. **Residual monitor** — default; continuity + x/y-velocity
2. **Volume fraction monitor** — at a cross-section ~500-1000 um downstream of throat. Water VF vs time → droplet frequency
3. **Pressure monitor** — at each inlet surface → pressure drop
4. **Velocity monitor** — at throat centerline

**Animation:** contour plots of water volume fraction, saved every 50-100 steps.

---

## 5. Post-Processing

### 5.1 Simulation Quality Metrics (paper Section 6.1)

| Metric | Target |
|---|---|
| RMS residuals | All < 10⁻⁴ per time step |
| Max Courant number | < 1 (ideally < 0.5) |
| Mass conservation error | < 1% |
| Periodic state | Consistent droplet size after 5+ droplets |

### 5.2 System Parameters (paper Section 6.2)

- **Pressure field** — contour at the junction showing pressure distribution
- **Velocity field** — contour + vectors at the throat
- **Pressure drop** — total inlet-to-outlet
- **TKE** — not applicable (laminar, Re < 100); note absence of turbulence

### 5.3 Droplet Parameters (paper Section 6.3)

Measure after periodic steady state (discard first 3-5 droplets):

| Parameter | Method | Expected |
|---|---|---|
| Length (L_d) | Front-to-back of water slug | 100-150 um |
| Width (W_d) | Max perpendicular width | ~93-125 um (confined) |
| Frequency (f) | 1/(time between droplets) | ~4000 Hz |
| Spacing | Center-to-center | Varies |
| CV | StdDev(L_d)/Mean(L_d) × 100% | < 15% |

### 5.4 Droplet Volume Estimation

For confined slug/plug droplets:
- V_d ≈ (π/4) × W_d² × (L_d − W_d/3) — cylinder + hemispherical caps
- Or: V_d ≈ L_d × W_d × D × 0.75 — rectangular with shape correction
- D = channel depth = 125 um

---

## 6. Design of Experiments (DoE)

### 6.1 Factors and Levels

**Factor 1: Oil flow rate**

| Level | Q_oil (uL/min) | v_oil (m/s) per channel | Ratio |
|---|---|---|---|
| Low | 150 | 0.200 | 0.60× |
| Center | **250** | **0.333** | **1.0×** |
| High | 400 | 0.533 | 1.60× |

**Factor 2: Water flow rate (pump settings)**

The water w+b pump and water w/o beads pump are varied together proportionally. At baseline: w+b = 67, w/o beads = 67 (split to 33.5 each side).

| Level | Q_w+b (uL/min) | Q_w (uL/min, total) | Q_aq total | v_w_center (m/s) | Ratio |
|---|---|---|---|---|---|
| Low | 40 | 40 | 80 | 0.0427 | 0.60× |
| Center | **67** | **67** | **134** | **0.0715** | **1.0×** |
| High | 100 | 100 | 200 | 0.1067 | 1.49× |

**Factor 3: Bead concentration (analytical only)**

| Level | C_beads (beads/uL) |
|---|---|
| Low | 150 |
| Center | **325** |
| High | 500 |

### 6.2 Experimental Matrix (3² = 9 CFD runs)

| Run | Q_oil (uL/min) | Q_aq (uL/min) | v_oil (m/s) | v_w_center (m/s) | Q_oil/Q_aq |
|---|---|---|---|---|---|
| 1 | 150 | 80 | 0.200 | 0.0427 | 1.88 |
| 2 | 150 | 134 | 0.200 | 0.0715 | 1.12 |
| 3 | 150 | 200 | 0.200 | 0.1067 | 0.75 |
| 4 | 250 | 80 | 0.333 | 0.0427 | 3.13 |
| **5** | **250** | **134** | **0.333** | **0.0715** | **1.87** |
| 6 | 250 | 200 | 0.333 | 0.1067 | 1.25 |
| 7 | 400 | 80 | 0.533 | 0.0427 | 5.00 |
| 8 | 400 | 134 | 0.533 | 0.0715 | 2.99 |
| 9 | 400 | 200 | 0.533 | 0.1067 | 2.00 |

**Run 5 = baseline.** Run 3 has Q_oil/Q_aq < 1, which may produce instability — useful for mapping operating window boundaries.

**For each run, extract:** L_d, W_d, f, CV, V_d.
**Then calculate Poisson stats** at 3 bead concentrations → 27 analytical data points.

### 6.3 Response Surface Plots (paper Section 6.5)

1. **Droplet length** vs (Q_oil, Q_aq)
2. **Generation frequency** vs (Q_oil, Q_aq)
3. **CV** vs (Q_oil, Q_aq)
4. **Monoclonal fraction P(1)** vs (Q_oil, Q_aq) at C = 325 beads/uL
5. **Lambda (λ)** vs (Q_aq, C_beads) at Q_oil = 250 uL/min

---

## 7. Theoretical Equations (paper Section 2.3)

### 7.1 Reynolds Number

$$Re = \frac{\rho \cdot v \cdot D_h}{\mu}$$

$D_h = \frac{2wh}{w + h}$ for rectangular channels. For square (125×125): $D_h = 125$ um.

### 7.2 Capillary Number

$$Ca = \frac{\mu_c \cdot v_c}{\sigma}$$

Ca governs droplet regime: Ca < 10⁻² → squeezing; 10⁻² < Ca < 0.1 → dripping; Ca > 0.1 → jetting [13].

### 7.3 Weber Number

$$We = \frac{\rho_c \cdot v_c^2 \cdot D_h}{\sigma} = Re \cdot Ca$$

### 7.4 Flow Rate Ratio

$$\phi = \frac{Q_d}{Q_c} = \frac{Q_{aq}}{Q_{oil}}$$

### 7.5 Droplet Size Scaling (Garstecki et al., 2006)

For squeezing regime in flow-focusing [13]:

$$\frac{L_d}{w_c} = 1 + \alpha \cdot \frac{Q_d}{Q_c}$$

where $\alpha$ is geometry-dependent (typically 1-3).

### 7.6 Droplet Generation Frequency

$$f = \frac{Q_d}{V_d}$$

### 7.7 Poisson Distribution for Bead Encapsulation

$$P(k) = \frac{\lambda^k \cdot e^{-\lambda}}{k!}$$

**Bead dilution**: only the center aqueous inlet carries beads. The effective concentration in the droplet is diluted by mixing with the two side water streams:

$$C_{eff} = C_{inlet} \times \frac{Q_{w+b}}{Q_{aq,total}} = 325 \times \frac{67}{134} = 162.5 \text{ beads/uL}$$

$$\lambda = C_{eff} \cdot V_d$$

### 7.8 Estimated Poisson Statistics at Baseline

C_eff = 162.5 beads/uL, estimated V_d ≈ 524 pL (for ~100 um sphere):

$$\lambda = 162.5 \times 5.24 \times 10^{-4} = 0.085$$

| k (beads) | P(k) | % | Interpretation |
|---|---|---|---|
| 0 | 0.918 | 91.8% | Empty |
| 1 | 0.078 | 7.8% | Monoclonal (target) |
| 2 | 0.003 | 0.3% | Doublet |
| ≥3 | <0.001 | <0.1% | Multiplet |

> Low loading (λ ≈ 0.085) ensures near-zero polyclonal contamination. Increasing bead concentration or droplet volume raises the monoclonal fraction.

### 7.9 VOF Governing Equations

**Continuity:** $\nabla \cdot \vec{v} = 0$

**Momentum:**
$$\frac{\partial (\rho \vec{v})}{\partial t} + \nabla \cdot (\rho \vec{v} \vec{v}) = -\nabla p + \nabla \cdot [\mu(\nabla \vec{v} + \nabla \vec{v}^T)] + \vec{F}_{sf}$$

**Volume fraction transport:** $\frac{\partial \alpha_q}{\partial t} + \vec{v} \cdot \nabla \alpha_q = 0$

**Mixture properties:** $\rho = \alpha_1 \rho_1 + \alpha_2 \rho_2, \quad \mu = \alpha_1 \mu_1 + \alpha_2 \mu_2$

**Surface tension (CSF) [10]:** $\vec{F}_{sf} = \sigma \kappa \nabla \alpha_q$

where $\kappa = -\nabla \cdot \hat{n}$ is interface curvature, $\hat{n} = \nabla \alpha_q / |\nabla \alpha_q|$.

---

## 8. Convergence and Quality

### 8.1 During Simulation

| Check | Criterion | Action if failed |
|---|---|---|
| Residuals | All < 10⁻⁴ per time step | Reduce time step, adjust under-relaxation |
| Courant number | Max < 1 | Reduce time step |
| Mass imbalance | < 1% | Check mesh, reduce time step |
| Periodicity | Consistent droplet size after 5+ | Continue simulation |

### 8.2 Mesh Independence Study

Run baseline (Run 5) at 3 resolutions:

| Mesh | Throat element size | Est. elements |
|---|---|---|
| Coarse | 5 um | ~30,000 |
| Medium | 2 um | ~120,000 |
| Fine | 1 um | ~450,000 |

Report mesh independence if medium→fine difference < 5% in L_d and f.

---

## 9. References

[1] Bio-Rad, US Patent US20140302503A1. Confirms HFE-7500 + Bis-Krytox-PEG surfactant.

[2] 3M, "Novec 7500 Engineered Fluid — Product Information." Technical Data Sheet.

[3] Rausch, M.H. et al. (2015). "Density, Surface Tension, and Kinematic Viscosity of HFE-7000, HFE-7100, HFE-7200, HFE-7300, and HFE-7500." *J. Chem. Eng. Data*, 60(12), 3759-3765. DOI: 10.1021/acs.jced.5b00691.

[4] Gradzielski, M. et al. (2025). "Influence of Parameters Used to Prepare Sterile Solutions of Poloxamer 188 on Their Physicochemical Properties." PMC11722941.

[5] Monkos, K. (1996). "Viscosity of BSA aqueous solutions as a function of temperature and concentration." *Int. J. Biol. Macromol.*, 18, 61-68. PubMed: 8852754.

[6] Brosseau, Q. et al. (2014). "Microfluidic Dynamic Interfacial Tensiometry." *Soft Matter*, 10(17), 3066-3076. DOI: 10.1039/C3SM52543K.

[7] Calhoun, S. et al. (2022). "Systematic characterization of double emulsion droplet volumes and stability." *Lab on a Chip*, 22, 2315-2330. DOI: 10.1039/D2LC00229A.

[8] Scanga, R. et al. (2018). "Click chemistry approaches for PEG-based fluorinated surfactants." *RSC Advances*, 8, 12960. DOI: 10.1039/C8RA01254G.

[9] Invitrogen/Thermo Fisher, "Dynabeads M-280 Streptavidin" Product Datasheet.

[10] Brackbill, J.U. et al. (1992). "A continuum method for modeling surface tension." *J. Comput. Phys.*, 100(2), 335-354.

[11] Baret, J.-C. (2012). "Surfactants in droplet-based microfluidics." *Lab on a Chip*, 12, 422-433.

[12] Hirt, C.W. & Nichols, B.D. (1981). "Volume of fluid (VOF) method for dynamics of free boundaries." *J. Comput. Phys.*, 39(1), 201-225.

[13] Garstecki, P. et al. (2006). "Formation of droplets and bubbles in a microfluidic T-junction." *Lab on a Chip*, 6(3), 437-446.

[14] Macosko, E.Z. et al. (2015). "Highly Parallel Genome-wide Expression Profiling Using Nanoliter Droplets." *Cell*, 161(5), 1202-1214.

[15] Meng, Z. et al. (2021). "Numerical Simulation and Experimental Verification of Droplet Generation in Microfluidic Digital PCR Chip." *Micromachines*, 12(4), 409. DOI: 10.3390/mi12040409.

---

## 10. Quick Checklist

- [ ] Import `generator_cropped.dxf`, scale channel width to 125 um
- [ ] Name 5 inlets: `inlet_water_beads`, `inlet_water_left`, `inlet_water_right`, `inlet_oil_left`, `inlet_oil_right`
- [ ] Name `outlet` and `walls`
- [ ] Mesh: quad-dominant, 1-2 um at throat, 5 um elsewhere
- [ ] Scale mesh to meters (×10⁻⁶) in Fluent
- [ ] VOF: 2 phases, implicit, Geo-Reconstruct
- [ ] Materials: oil (ρ=1614, µ=1.24e-3), water-mix (ρ=1015, µ=3.0e-3)
- [ ] IFT: σ = 3.0 × 10⁻³ N/m
- [ ] BCs: oil v=0.333, water-center v=0.0715, water-side v=0.0893
- [ ] Contact angle = 150°
- [ ] Initialize with oil
- [ ] Variable time stepping, Courant = 0.25
- [ ] Monitors: VF downstream, pressure at inlets
- [ ] Mesh independence (3 levels)
- [ ] 9 DoE runs
- [ ] Extract L_d, W_d, f, CV per run
- [ ] Poisson stats at 3 bead concentrations
- [ ] Response surface plots
