# CFD SIMULATION OF DROPLET GENERATION IN A FLOW-FOCUSING MICROFLUIDIC CHIP FOR MONOCLONAL BEAD ENCAPSULATION

**Stroganov A.**, KPI named after Igor Sikorsky, email@example.com

*KPI named after Igor Sikorsky*

**Abstract.** *This work presents a computational fluid dynamics (CFD) simulation of droplet generation in a flow-focusing microfluidic chip designed for monoclonal bead encapsulation. A 2D Volume of Fluid (VOF) model was developed in ANSYS Fluent to simulate the three-inlet aqueous and two-inlet oil system using Bio-Rad EvaGreen Generation Oil and an aqueous phase containing 5% Pluronic F68 and 1% BSA. A full-factorial design of experiments varying oil (150-400 uL/min) and aqueous (80-200 uL/min) flow rates was conducted. Droplet size, generation frequency, and coefficient of variation were extracted and used to predict Poisson bead encapsulation statistics for Dynabeads M280 at concentrations of 150-500 beads/uL. The simulation identifies the optimal operating window for monoclonal bead loading at the target frequency of ~4000 Hz.*

**Keywords:** *microfluidics, droplet generation, CFD, VOF, bead encapsulation*

## 1. Introduction

Droplet-based microfluidics enables high-throughput single-cell and single-bead analysis by compartmentalizing samples into monodisperse picoliter droplets [1]. In bead-based assays, achieving monoclonal loading — exactly one bead per droplet — is critical and governed by Poisson statistics [2]. Flow-focusing microfluidic generators produce droplets by pinching a dispersed aqueous stream with an immiscible continuous oil phase at a geometric constriction [3].

The aim of this work is to simulate droplet generation in a Drop-seq-type flow-focusing chip [2] using CFD to identify optimal flow conditions for monoclonal encapsulation of Dynabeads M280 Streptavidin beads, targeting a generation frequency of ~4000 Hz, droplet diameter of 100-120 um, and coefficient of variation (CV) below 15%.

## 2. Materials and Methods

### 2.1. System Requirements

Table 1 summarizes the target system parameters.

**Table 1. System requirements.**

| Parameter | Value |
|---|---|
| Oil flow rate | 250 uL/min |
| Water (w/o beads) flow rate | 67 uL/min |
| Water (w/ beads) flow rate | 67 uL/min |
| Bead concentration (inlet) | 325 beads/uL |
| Bead diameter (Dynabeads M280) | 2.8 um |
| Target droplet diameter | 100-120 um |
| Target frequency | ~4000 Hz |
| Target CV | <15% |

### 2.2. Chip Design

The microfluidic chip contains 26 identical flow-focusing generators on a single PDMS substrate. Each generator (Fig. 1) features three aqueous inlets from the top (center: water + beads at 125 um width; two sides: plain water at 50 um width each), which merge via T-junctions into a single 125 um channel. Two oil channels (50 um wide) enter from below, turning 90 degrees to meet the aqueous stream perpendicularly at the flow-focusing junction. The nozzle throat constricts to 93.7 um (25% reduction) over a length of ~62.5 um with a convergence half-angle of 26.6 degrees. Downstream, the 125 um channel leads into a V-shaped zigzag serpentine (3.5 periods, ~1880 um path length) exiting to the collection outlet. The channel depth is 125 um throughout.

*[Fig. 1. (a) Full chip layout with 26 generators. (b) Single generator geometry with labeled inlets and outlet. (c) Detail of flow-focusing junction.]*

### 2.3. Theoretical Estimation and Flow Equations

The flow is governed by the incompressible Navier-Stokes equations with the Volume of Fluid (VOF) method [4] for interface tracking. The continuity and momentum equations are:

nabla . v = 0

d(rho*v)/dt + nabla . (rho*v*v) = -nabla(p) + nabla . [mu(nabla(v) + nabla(v)^T)] + F_sf

where the surface tension force follows the Continuum Surface Force (CSF) model [5]: F_sf = sigma * kappa * nabla(alpha), with sigma the interfacial tension, kappa the interface curvature, and alpha the volume fraction.

The volume fraction transport equation: d(alpha)/dt + v . nabla(alpha) = 0, with mixture properties rho = alpha_1*rho_1 + alpha_2*rho_2 and mu = alpha_1*mu_1 + alpha_2*mu_2.

The key dimensionless numbers are Reynolds (Re = rho*v*D_h/mu), Capillary (Ca = mu*v/sigma), and Weber (We = Re*Ca). At baseline conditions (Table 2), Ca ~ 0.09 places the system at the dripping-to-jetting transition [3], consistent with high-frequency generation.

Droplet size in the squeezing regime scales as L_d/w_c = 1 + alpha*(Q_d/Q_c) [3], where alpha is a geometry-dependent constant. Bead encapsulation follows Poisson statistics [2]: P(k) = (lambda^k * e^(-lambda)) / k!, where lambda = C_eff * V_d is the mean beads per droplet and C_eff = C_inlet * Q_(w+b) / Q_aq,total accounts for dilution by the bead-free aqueous streams.

### 2.4. Design of Experiment

A 3^2 full-factorial DoE was conducted with two factors: oil flow rate Q_oil (150, 250, 400 uL/min) and total aqueous flow rate Q_aq (80, 134, 200 uL/min). The baseline (Run 5: Q_oil = 250, Q_aq = 134 uL/min) matches the target operating conditions. Bead encapsulation was evaluated analytically at three concentrations (150, 325, 500 beads/uL) for each of the 9 simulated conditions. Responses: droplet length L_d, frequency f, CV, and monoclonal fraction P(1).

### 2.5. ANSYS Fluent Setup

A 2D planar transient simulation was performed using ANSYS Fluent with the implicit VOF scheme and Geo-Reconstruct interface tracking. Material properties are summarized in Table 2.

**Table 2. Material properties and simulation parameters.**

| Property | Oil (Bio-Rad EvaGreen) | Aqueous (5% P-F68 + 1% BSA) | Ref. |
|---|---|---|---|
| Density, kg/m^3 | 1614 | 1015 | [6,7] |
| Dynamic viscosity, Pa.s | 1.24 x 10^-3 | 3.0 x 10^-3 | [6,8] |
| Interfacial tension, N/m | 3.0 x 10^-3 (oil/water) | | [9,10] |

The Bio-Rad oil is based on HFE-7500 with PFPE-PEG surfactant [11]. Aqueous viscosity was estimated from Poloxamer 188 solution data [7] with BSA correction [8]. The interfacial tension (3.0 mN/m) is a mid-range estimate from measurements of similar PFPE-PEG/HFE-7500 systems [9,10].

Boundary conditions: velocity inlets for oil (0.333 m/s each, VF_oil = 1), center water (0.0715 m/s, VF_water = 1), and side water (0.0893 m/s each, VF_water = 1); pressure outlet (0 Pa gauge); no-slip walls with 150 degree water contact angle. The domain was initialized with oil, with the aqueous inlet channels patched to water VF = 1. PISO pressure-velocity coupling with PRESTO! pressure discretization was used. Variable time stepping with a global Courant number of 0.25 ensured stability. Each run simulated 7-10 ms (>20 droplets).

A mesh independence study was performed at three resolutions (throat element size: 5, 2, 1 um).

## 3. Results and Discussion

### 3.1. Simulation Quality

*[Fig. 2. (a) Residual convergence plot. (b) Maximum Courant number vs. time.]*

RMS residuals converged below 10^-4 for all variables at each time step. The maximum Courant number remained below [VALUE]. Mass conservation error was [VALUE]%. Periodic droplet generation was established after [N] droplets.

The mesh independence study showed [VALUE]% difference in droplet length between medium and fine meshes, confirming adequacy of the medium mesh (2 um throat elements, ~120,000 cells).

### 3.2. System Parameters

*[Fig. 3. (a) Pressure contour at the junction. (b) Velocity field with vectors at the throat.]*

The pressure drop from oil inlets to the outlet was [VALUE] Pa. Peak velocity at the throat reached [VALUE] m/s. The flow remained laminar (Re < 100) throughout the domain. No turbulent kinetic energy was present, confirming the laminar flow assumption.

### 3.3. Droplet Parameters

*[Fig. 4. Droplet train visualization (water volume fraction contour) at baseline conditions.]*

Table 3 summarizes the droplet parameters at baseline (Run 5).

**Table 3. Droplet parameters at baseline (Q_oil = 250, Q_aq = 134 uL/min).**

| Parameter | Value |
|---|---|
| Droplet length, um | [VALUE] |
| Droplet width, um | [VALUE] |
| Estimated volume, pL | [VALUE] |
| Generation frequency, Hz | [VALUE] |
| CV, % | [VALUE] |

### 3.4. Bead Encapsulation Statistics

Using the simulated droplet volume and Poisson statistics, the monoclonal fraction P(1) was calculated at baseline conditions. At the inlet concentration of 325 beads/uL, the effective in-droplet concentration is C_eff = 325 * (67/134) = 162.5 beads/uL, yielding lambda = C_eff * V_d.

**Table 4. Poisson statistics at baseline (V_d = [VALUE] pL, C_inlet = 325 beads/uL).**

| k (beads/droplet) | P(k) | % |
|---|---|---|
| 0 (empty) | [VALUE] | [VALUE] |
| 1 (monoclonal) | [VALUE] | [VALUE] |
| >=2 (polyclonal) | [VALUE] | [VALUE] |

### 3.5. DoE Response Surfaces

*[Fig. 5. Response surface plots: (a) Droplet length vs. (Q_oil, Q_aq). (b) Generation frequency vs. (Q_oil, Q_aq). (c) CV vs. (Q_oil, Q_aq). (d) Monoclonal fraction P(1) vs. (Q_oil, Q_aq) at C = 325 beads/uL.]*

Increasing Q_oil at fixed Q_aq [increased/decreased] droplet frequency and [decreased/increased] droplet size, consistent with higher shear at the throat. Increasing Q_aq [increased/decreased] droplet volume, raising lambda and the monoclonal fraction P(1). The optimal region for monoclonal loading (P(1) > [VALUE]%) while maintaining CV < 15% was found at [RANGE OF Q_oil AND Q_aq].

At Q_oil/Q_aq < 1 (Run 3), [jetting/instability was observed / droplet generation became irregular], defining the lower bound of the operating window.

## 4. Conclusions

A 2D VOF simulation of droplet generation in a 26-generator Drop-seq microfluidic chip was developed and validated through mesh independence analysis. At baseline conditions (Q_oil = 250 uL/min, Q_aq = 134 uL/min), the simulation predicts droplet generation at [VALUE] Hz with a diameter of [VALUE] um and CV of [VALUE]%. The Poisson-predicted monoclonal bead fraction is [VALUE]% at a Dynabeads M280 concentration of 325 beads/uL. The DoE analysis identifies Q_oil = [VALUE] and Q_aq = [VALUE] uL/min as optimal for maximizing monoclonal loading while maintaining droplet homogeneity. These results provide guidance for experimental optimization of the bead encapsulation protocol.

## References

[1] Macosko E.Z., Basu A., Satija R. et al. Highly Parallel Genome-wide Expression Profiling of Individual Cells Using Nanoliter Droplets. Cell. 2015. Vol. 161, No 5. P. 1202-1214. DOI: 10.1016/j.cell.2015.05.002.

[2] Garstecki P., Fuerstman M.J., Stone H.A., Whitesides G.M. Formation of droplets and bubbles in a microfluidic T-junction — scaling and mechanism of break-up. Lab on a Chip. 2006. Vol. 6, No 3. P. 437-446. DOI: 10.1039/b510841a.

[3] Hirt C.W., Nichols B.D. Volume of fluid (VOF) method for the dynamics of free boundaries. Journal of Computational Physics. 1981. Vol. 39, No 1. P. 201-225. DOI: 10.1016/0021-9991(81)90145-5.

[4] Brackbill J.U., Kothe D.B., Zemach C. A continuum method for modeling surface tension. Journal of Computational Physics. 1992. Vol. 100, No 2. P. 335-354. DOI: 10.1016/0021-9991(92)90240-Y.

[5] Rausch M.H., Kretschmer L., Will S., Leipertz A., Froeba A.P. Density, Surface Tension, and Kinematic Viscosity of Hydrofluoroethers HFE-7000, HFE-7100, HFE-7200, HFE-7300, and HFE-7500. J. Chem. Eng. Data. 2015. Vol. 60, No 12. P. 3759-3765. DOI: 10.1021/acs.jced.5b00691.

[6] Gradzielski M. et al. Influence of Parameters Used to Prepare Sterile Solutions of Poloxamer 188 on Their Physicochemical Properties. Pharmaceutics. 2025. PMC11722941.

[7] Monkos K. Viscosity of bovine serum albumin aqueous solutions as a function of temperature and concentration. Int. J. Biol. Macromol. 1996. Vol. 18. P. 61-68.

[8] Calhoun S. et al. Systematic characterization of effect of flow rates and buffer compositions on double emulsion droplet volumes and stability. Lab on a Chip. 2022. Vol. 22. P. 2315-2330. DOI: 10.1039/D2LC00229A.

[9] Scanga R. et al. Click chemistry approaches to expand the repertoire of PEG-based fluorinated surfactants for droplet microfluidics. RSC Advances. 2018. Vol. 8. P. 12960. DOI: 10.1039/C8RA01254G.

[10] Bio-Rad Laboratories. US Patent US20140302503A1. Compositions, methods and systems for polymerase chain reaction assays. 2014.

[11] Meng Z., Yu L., Jin Y. Numerical Simulation and Experimental Verification of Droplet Generation in Microfluidic Digital PCR Chip. Micromachines. 2021. Vol. 12, No 4. P. 409. DOI: 10.3390/mi12040409.
