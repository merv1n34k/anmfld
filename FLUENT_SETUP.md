# ANSYS Fluent — Complete Click-by-Click Setup

This is a sequential walkthrough. Follow every step in order.

---

## PHASE 1: GEOMETRY (SpaceClaim)

### 1.1 Import
1. Open **ANSYS Workbench** → drag **Fluent** onto the project schematic
2. Double-click **Geometry** → SpaceClaim opens
3. **File → Import** → select `generator_cropped.dxf`
4. If prompted for units, select **Millimeters** (we will scale later)

### 1.2 Scale to Correct Dimensions
The DXF uses non-standard units. The main channel (widest) must be **0.125 mm = 125 um**.

1. Measure the main channel width in SpaceClaim (**Measure** tool)
2. Note the current width value → call it `W_current`
3. **Scale factor** = 0.125 / W_current
4. Select all geometry → **Pull** tool → **Scale** → enter the scale factor
5. Verify: main channel = 0.125 mm, side channels = 0.050 mm, throat = 0.0937 mm

### 1.3 Create 2D Surface
1. If the geometry is just lines/curves: **Design → Fill** → click inside the enclosed region → creates a surface
2. If Fill doesn't work: **Repair → Stitch** the curves first, then Fill
3. You should have a single flat surface representing the fluid domain

### 1.4 Named Selections (CRITICAL)
Select edges and assign names. Work from the image `generator_chip.png` as reference.

1. **Select** the top edge of the center channel (125 um wide) → right-click → **Create Named Selection** → name: `inlet_water_beads`
2. **Select** the top edge of the left water channel (50 um wide) → name: `inlet_water_left`
3. **Select** the top edge of the right water channel (50 um wide) → name: `inlet_water_right`
4. **Select** the bottom edge of the left oil channel (50 um wide) → name: `inlet_oil_left`
5. **Select** the bottom edge of the right oil channel (50 um wide) → name: `inlet_oil_right`
6. **Select** the exit edge of the serpentine (right side, 125 um wide) → name: `outlet`
7. **Select ALL remaining edges** → name: `walls`

### 1.5 Set 2D Analysis
1. In SpaceClaim: **Workbench** tab → **Analysis Type** → set to **2D**
2. Ensure the surface lies in the XY plane
3. Close SpaceClaim → return to Workbench

---

## PHASE 2: MESHING

Double-click **Mesh** in Workbench.

### 2.1 Global Mesh Settings
1. In the **Outline** panel, click **Mesh**
2. In the **Details** panel:
   - Physics Preference: **CFD**
   - Solver Preference: **Fluent**
   - Element Size: **5e-3 mm** (= 5 um)
   - Advanced Size Function: **Curvature**
   - Smoothing: **High**
   - Relevance Center: **Fine**

### 2.2 Quad-Dominant Method
1. Right-click **Mesh** → **Insert → Method**
2. Select the entire fluid body
3. Method: **Quadrilateral Dominant**
4. Free Face Mesh Type: **Quad/Tri**

### 2.3 Refinement Zone — Throat/Junction
1. Right-click **Mesh** → **Insert → Sizing**
2. **Scope**: select edges/faces around the junction and throat region (the convergence zone ± 200 um)
3. Element Size: **2e-3 mm** (= 2 um)

### 2.4 Refinement Zone — Throat Core
1. Right-click **Mesh** → **Insert → Sizing**
2. **Scope**: select edges of the throat walls specifically (93.7 um section)
3. Element Size: **1e-3 mm** (= 1 um)

### 2.5 Inflation (Boundary Layer)
1. Right-click **Mesh** → **Insert → Inflation**
2. **Scope**: select the fluid body
3. **Boundary**: select `walls` named selection
4. Settings:
   - Inflation Option: **First Layer Thickness**
   - First Layer Height: **5e-4 mm** (= 0.5 um)
   - Maximum Layers: **5**
   - Growth Rate: **1.2**

### 2.6 Generate Mesh
1. Right-click **Mesh** → **Generate Mesh**
2. Check statistics:
   - Target: **100,000–250,000 elements**
   - Orthogonal Quality: > 0.7 (check in **Mesh → Statistics → Mesh Metric**)
   - Maximum Skewness: < 0.5
   - Maximum Aspect Ratio: < 5
3. If quality is bad: reduce element sizes or increase smoothing iterations
4. Close meshing → return to Workbench

---

## PHASE 3: FLUENT SETUP

Double-click **Setup** in Workbench. Fluent Launcher appears.

### 3.1 Fluent Launcher Settings
- Dimension: **2D**
- Options: **Double Precision** ← IMPORTANT for VOF with surface tension
- Processing: set to available cores (parallel if possible)
- Click **OK** → Fluent opens

### 3.2 Scale Mesh to Meters
**Immediately** after Fluent opens:

1. **Domain → Mesh → Scale...**
2. Mesh Was Created In: **mm**
3. Convert To: **m**
4. Click **Scale**
5. Click **Check** → verify domain extents are in the 10⁻⁵ to 10⁻⁴ m range (i.e., tens to hundreds of microns)
6. Click **Close**

Check mesh quality:
- **Domain → Mesh → Check** → look for minimum orthogonal quality > 0.1, no negative volumes

---

## PHASE 4: GENERAL SETTINGS

### 4.1 Solver
**Setup → General**
- Solver Type: **Pressure-Based**
- Velocity Formulation: **Absolute**
- Time: **Transient**
- 2D Space: **Planar**
- Gravity: **OFF** (leave unchecked)

---

## PHASE 5: MODELS

### 5.1 Multiphase
**Setup → Models → Multiphase → Edit...**

1. Model: **Volume of Fluid**
2. VOF Sub-Models:
   - Number of Eulerian Phases: **2**
   - VOF Scheme: **Implicit**
   - Check: **Implicit Body Force**
   - Interface Modeling Type: **Sharp**
   - Volume Fraction Cutoff: **1e-06** (default)
   - Courant Number: **0.25** (still used for interface tracking stability)
3. Click **OK**

> **Why Implicit?** Implicit VOF allows larger stable time steps while still supporting Geo-Reconstruct for sharp interface tracking. Explicit VOF is slightly sharper but requires strict Co < 0.25 and tiny time steps. For this geometry with high velocity gradients at the throat, implicit provides better stability with negligible interface quality loss.

### 5.2 Viscous Model
**Setup → Models → Viscous → Edit...**
- Model: **Laminar**
- Click **OK**

(No turbulence model — Re < 100, flow is fully laminar)

### 5.3 Energy
Leave **OFF** (isothermal simulation at 25°C)

---

## PHASE 6: MATERIALS

### 6.1 Create Oil Material
**Setup → Materials → Fluid → Create/Edit...**

1. Click **Fluent Database...** → search for anything, we'll override all values
2. Or just click **Change/Create** with a new name
3. Set:
   - Name: **biorad-evagreen-oil**
   - Chemical Formula: (leave blank)
   - Density: **1614** kg/m³ → Constant
   - Viscosity: **0.00124** kg/(m·s) → Constant
   - (Ignore all other properties — not needed for isothermal incompressible)
4. Click **Change/Create** → **Close**

### 6.2 Create Aqueous Material
**Setup → Materials → Fluid → Create/Edit...**

1. Name: **water-pluronic-bsa**
2. Density: **1015** kg/m³ → Constant
3. Viscosity: **0.003** kg/(m·s) → Constant
4. Click **Change/Create** → **Close**

---

## PHASE 7: PHASES

### 7.1 Define Phases
**Setup → Models → Multiphase → Edit...**
(Or go to **Setup → Phases**)

**Phase 1 (Primary Phase):**
1. Click **phase-1** → **Edit...**
2. Name: **oil**
3. Phase Material: **biorad-evagreen-oil**
4. Click **OK**

**Phase 2 (Secondary Phase):**
1. Click **phase-2** → **Edit...**
2. Name: **water**
3. Phase Material: **water-pluronic-bsa**
4. Click **OK**

### 7.2 Phase Interaction
**Setup → Phases → Interaction...**
(Or **Setup → Models → Multiphase → Phase Interaction**)

1. **Surface Tension** tab:
   - Surface Tension Coefficient (oil-water): **0.003** N/m
   - Surface Tension Model: **Continuum Surface Force** (CSF) — default
   - Check: **Wall Adhesion**
2. Click **OK**

---

## PHASE 8: CELL ZONE CONDITIONS

**Setup → Cell Zone Conditions**

1. Click on the fluid zone → **Edit...**
2. Phase: should show oil and water
3. Ensure the zone is assigned as **fluid**
4. Leave all defaults
5. Click **OK**

---

## PHASE 9: BOUNDARY CONDITIONS

**Setup → Boundary Conditions**

Click each named boundary and configure:

### 9.1 inlet_oil_left
1. Type: **velocity-inlet**
2. Click **Edit...**
3. **Momentum** tab:
   - Velocity Magnitude: **0.3333** m/s
   - Direction: set normal to boundary (default)
4. **Multiphase** tab (or switch phase to **oil**):
   - Volume Fraction for Phase 2 (water): **0**
   - (Phase 1 (oil) = 1 automatically)
5. Click **OK**

### 9.2 inlet_oil_right
Same as inlet_oil_left:
- Velocity: **0.3333** m/s
- Water VF: **0**

### 9.3 inlet_water_beads
1. Type: **velocity-inlet**
2. **Momentum** tab:
   - Velocity Magnitude: **0.0715** m/s
3. **Multiphase** tab:
   - Switch to Phase 2 (water): Volume Fraction = **1**
   - (Or set Phase 1 backflow VF = 0)
4. Click **OK**

### 9.4 inlet_water_left
1. Type: **velocity-inlet**
2. Velocity: **0.0893** m/s
3. Water VF: **1**
4. Click **OK**

### 9.5 inlet_water_right
Same as inlet_water_left:
- Velocity: **0.0893** m/s
- Water VF: **1**

### 9.6 outlet
1. Type: **pressure-outlet**
2. **Momentum** tab:
   - Gauge Pressure: **0** Pa
   - Backflow Direction: **Normal to Boundary**
3. **Multiphase** tab:
   - Backflow Volume Fraction for Phase 2 (water): **0**
   - (Oil is the backflow phase — correct, since oil is continuous)
4. Click **OK**

> **Why 0 Pa gauge?** With velocity inlets, the outlet pressure is just a reference point — the solver computes the pressure field needed to satisfy continuity. The real backpressure from downstream resistance (collection tubing, other generators) is implicitly captured in the computed pressure drop. The absolute pressure level does not affect the flow field for incompressible fluids. If you know the actual outlet gauge pressure from Fluigent readings, you can set it here instead, but the flow results will be identical.

### 9.7 walls
1. Type: **wall**
2. Click **Edit...**
3. **Momentum** tab:
   - Wall Motion: **Stationary Wall**
   - Shear Condition: **No Slip**
4. **Multiphase** tab (Phase 2 — water):
   - Check: **Wall Adhesion**
   - Contact Angle: **150** degrees
   - (This is the water contact angle measured through the water phase. 150° = water is non-wetting, oil wets the walls.)
5. Click **OK**

---

## PHASE 10: SOLVER METHODS

**Solution → Methods**

| Setting | Value |
|---|---|
| Pressure-Velocity Coupling | **PISO** |
| Spatial Discretization — Gradient | **Least Squares Cell Based** |
| Spatial Discretization — Pressure | **PRESTO!** |
| Spatial Discretization — Momentum | **Second Order Upwind** |
| Volume Fraction | **Geo-Reconstruct** |
| Transient Formulation | **First Order Implicit** |

---

## PHASE 11: SOLVER CONTROLS

**Solution → Controls**

### Under-Relaxation Factors:

| Parameter | Value |
|---|---|
| Pressure | **0.3** |
| Density | **1** |
| Body Forces | **1** |
| Momentum | **0.7** |
| Volume Fraction | **0.5** |

### PISO Settings (under Pressure-Velocity Coupling):
- Skewness Correction: **1**
- Neighbor Correction: **1**

---

## PHASE 12: MONITORS

### 12.1 Residuals
**Solution → Monitors → Residual → Edit...**
- Print and Plot: **checked**
- Convergence Criterion for all: **1e-04**
- Click **OK**

### 12.2 Surface Monitor — Droplet Detection
**Solution → Monitors → Surface Monitors → Create...**

1. First, create a monitoring line:
   - **Surface → Create → Line/Rake...**
   - Name: **monitor_line**
   - Place it ~500-1000 um (5e-4 to 1e-3 m) downstream of the throat, perpendicular to flow
   - (You need to know the throat Y coordinate from your geometry. Place the line horizontally across the channel at that Y position.)
2. Create monitor:
   - Report Type: **Area-Weighted Average**
   - Field Variable: **Phases → Volume Fraction → water**
   - Surface: **monitor_line**
   - Check: **Plot** and **Write**
   - Write file: `vf_monitor.out`
   - Report every: **1** time step
3. Click **OK**

### 12.3 Surface Monitor — Pressure
**Solution → Monitors → Surface Monitors → Create...**

1. Report Type: **Area-Weighted Average**
2. Field Variable: **Pressure → Static Pressure**
3. Surface: **inlet_oil_left** (repeat for other inlets if desired)
4. Check: **Plot** and **Write**
5. Click **OK**

---

## PHASE 13: INITIALIZATION

**Solution → Initialization**

### 13.1 Standard Initialization (domain filled with oil)
1. Method: **Standard Initialization**
2. Compute From: **inlet_oil_left** (or All Zones)
3. Set values:
   - Gauge Pressure: **0** Pa
   - X Velocity: **0** m/s
   - Y Velocity: **0** m/s
   - **water** Volume Fraction: **0** (entire domain starts filled with oil)
4. Click **Initialize**

### 13.2 Patch Aqueous Channels with Water
The three water inlet channels must be pre-filled with water (as in reality — the aqueous lines are primed before the experiment starts).

1. **Solution → Initialization → Patch...**
2. Phase: **water**
3. Variable: **Volume Fraction**
4. Value: **1**
5. **Registers to Patch**: you need to define a region covering the aqueous channels. Two methods:

   **Method A — Adapt/Mark Cells by Region:**
   1. **Adapt → Region...** (or **Cell Registers → New → Region**)
   2. Define a bounding box that covers the three water inlet channels (from the top of the domain down to the T-junction where oil enters). Check your geometry coordinates.
   3. Click **Mark** → this creates a cell register
   4. Back in **Patch**: select the register → set water VF = 1 → click **Patch**

   **Method B — If channels are separate cell zones:**
   If the mesh was split into separate zones per channel during meshing, you can patch each zone directly.

6. Click **Patch** → Click **Close**
7. Verify: display water VF contour — the top channels (water inlets down to oil junction) should show VF = 1 (red), everything else VF = 0 (blue).

---

## PHASE 14: CALCULATION SETTINGS

**Solution → Run Calculation**

### Option A: Variable Time Stepping (RECOMMENDED)
1. Time Advancement Type: **Variable** (or Adaptive)
2. Settings:
   - Global Courant Number: **0.25**
   - (Fluent will auto-calculate the time step based on mesh size and velocity)

If your Fluent version doesn't support variable time stepping with explicit VOF, use Option B.

### Option B: Fixed Time Step
1. Time Stepping Method: **Fixed**
2. Time Step Size: **2e-07** s (= 0.2 us)
3. Verification: max velocity ~ 0.55 m/s, min cell size ~ 1e-6 m
   - Courant = v * dt / dx = 0.55 * 2e-7 / 1e-6 = 0.11 ✓ (< 0.25)

### Common Settings for Both Options:
- Max Iterations/Time Step: **25**
- Number of Time Steps: **50000** (for Option B: 50000 × 0.2 us = 10 ms)
- Reporting Interval: **1**
- Profile Update Interval: **1**

---

## PHASE 15: DATA EXPORT (SET UP BEFORE RUNNING)

### 15.1 Automatic Image/Animation Export
**Solution → Calculation Activities → Solution Animations → Create/Edit...**

1. Click **Create...**
2. Animation name: **droplets**
3. Record after every: **100** time steps
4. Display Type: **Contour**
5. Variable: **Phases → Volume Fraction → water**
6. Surface: select all interior surfaces
7. Coloring: 0 (blue, oil) to 1 (red, water)
8. Storage Type: **In Memory** or **MPEG File**
9. Click **OK**

### 15.2 Auto-Save Case/Data
**Solution → Calculation Activities → Autosave...**
- Save Every: **5000** time steps
- This creates checkpoint files in case of crash

---

## PHASE 16: RUN

1. Click **Calculate**
2. Watch:
   - Residuals should drop below 1e-4 each time step
   - Volume fraction monitor should start showing periodic oscillations after 1-2 ms
   - The animation should show water entering, oil pinching, droplets forming
3. Let it run for the full 50000 steps (10 ms) or until you have >20 periodic droplets
4. If residuals diverge: stop, reduce time step (try 1e-7 s), re-run

---

## PHASE 17: POST-PROCESSING

After the simulation completes:

### 17.1 Droplet Visualization
**Results → Graphics → Contours → Edit...**
1. Contour of: **Phases → Volume Fraction → water**
2. Display on all surfaces
3. Range: 0 to 1
4. Take screenshots at several time steps showing the droplet train

### 17.2 Pressure Field
**Results → Graphics → Contours → Edit...**
1. Contour of: **Pressure → Static Pressure**
2. Zoom into junction region

### 17.3 Velocity Field
**Results → Graphics → Contours → Edit...**
1. Contour of: **Velocity → Velocity Magnitude**
2. Overlay vectors: **Results → Graphics → Vectors → Edit...**
   - Color by: Velocity Magnitude
   - Scale: auto

### 17.4 Extract Droplet Frequency from Monitor
1. Open `vf_monitor.out` (text file) in Excel or Python
2. Plot water VF vs time
3. Count peaks → frequency = N_peaks / time_window
4. Time between peaks → period → f = 1/period

### 17.5 Measure Droplet Size
In Fluent post-processing:
1. At a specific time step with a complete droplet visible:
2. **Results → Plots → XY Plot → Edit...**
3. Y Axis: Volume Fraction of water
4. X Axis: Position along the channel centerline
5. The region where VF > 0.5 = droplet
6. Droplet length = distance between front and back of the VF > 0.5 region

Or use the contour visualization and **Measure** tool.

### 17.6 Residual Plot for Paper
**Results → Plots → Residuals** → export as image

### 17.7 Export Data for DoE
For each of the 9 DoE runs:
1. Change only the inlet velocities (recalculate from DoE table in SIMULATION_GUIDE.md Section 6.2)
2. Re-initialize, re-run
3. Record: L_d, W_d, f, CV for each run

---

## QUICK REFERENCE — ALL VALUES IN ONE PLACE

### Materials
```
Oil:    ρ = 1614 kg/m³,   µ = 0.00124 Pa·s
Water:  ρ = 1015 kg/m³,   µ = 0.003 Pa·s
IFT:    σ = 0.003 N/m
```

### Boundary Conditions
```
inlet_oil_left:      velocity-inlet,  v = 0.3333 m/s,  oil VF = 1
inlet_oil_right:     velocity-inlet,  v = 0.3333 m/s,  oil VF = 1
inlet_water_beads:   velocity-inlet,  v = 0.0715 m/s,  water VF = 1
inlet_water_left:    velocity-inlet,  v = 0.0893 m/s,  water VF = 1
inlet_water_right:   velocity-inlet,  v = 0.0893 m/s,  water VF = 1
outlet:              pressure-outlet, P = 0 Pa,         backflow oil
walls:               wall,            no-slip,          contact angle = 150°
```

### Solver
```
Pressure-Velocity:  PISO
Pressure:           PRESTO!
Momentum:           Second Order Upwind
Volume Fraction:    Geo-Reconstruct
Transient:          First Order Implicit
VOF Scheme:         Implicit
Time step:          variable (Co = 0.25) or fixed 2e-7 s
Max iter/step:      25
Total time:         0.01 s (10 ms)
```

### DoE Velocity Table (for all 9 runs)
When changing runs, update ONLY these inlet velocities:

| Run | v_oil (m/s) | v_w_center (m/s) | v_w_side (m/s) |
|-----|-------------|-------------------|----------------|
| 1   | 0.200       | 0.0427            | 0.0534         |
| 2   | 0.200       | 0.0715            | 0.0893         |
| 3   | 0.200       | 0.1067            | 0.1333         |
| 4   | 0.333       | 0.0427            | 0.0534         |
| **5** | **0.333** | **0.0715**        | **0.0893**     |
| 6   | 0.333       | 0.1067            | 0.1333         |
| 7   | 0.533       | 0.0427            | 0.0534         |
| 8   | 0.533       | 0.0715            | 0.0893         |
| 9   | 0.533       | 0.1067            | 0.1333         |

Run 5 = baseline. For each run: re-set inlet velocities → re-initialize → run 10 ms.

Note: v_w_side is calculated as v_w_center × (125/125) × (67/67) × (125/50) × (1/2).
More precisely: v_w_side = (Q_w_total/2) / (50 µm × 125 µm) and v_w_center = Q_w+b / (125 µm × 125 µm), where Q_w_total = Q_w+b (both pumps at same setting).
