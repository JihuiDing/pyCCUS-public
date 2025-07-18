﻿import numpy as np 
import os

class Write_datfiles_OMVCCS():

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.params = None

    def print_test2_dat(self, fileID):
        """
        self.params is a dict or df with keywords to be the params to change.
        """

        print(f"""

** base model of Sula for pyCCUS workflow after adding OMV data
** two-way coupled geomechanics, no thermal simulation

**  ==============  INPUT/OUTPUT CONTROL  ======================

RESULTS SIMULATOR GEM

*TITLE1 'Sula CO2 Sequestration'
*TITLE2 'JD_Sula_2005 grid'
*TITLE3 'base model with OMV data'
*CASEID 'sim0'

*INUNIT	*SI	**input data units

**WPRN controls the frequency of writing data to the output print files.
*WPRN	*WELL	*TIME
*WPRN	*GRID	*TIME
*WPRN	*ITER	*BRIEF
**OUTPRN identifies what information is written to the output print file.
*OUTPRN	*WELL	*ALL
*OUTPRN *RES	*ALL
*OUTPRN *GRID	*PRES DROP SW SO SG TEMP Y 'CO2' X 'CO2' W 'CO2' OBHLOSS VISO VISG IMPL

**WSRF controls how frequently well, special history, and/or grid information is written to the output Simulation Results File.
*WSRF	*WELL		1
*WSRF	*GRID		*TIME
*WSRF	*GRIDDEFORM	*TIME
**OUTSRF identifies what information is written to the Simulation Results file.
*XDR		*ON	**External Data Representation (XDR) format to write SR2 binary file(s) 
*OUTSRF		*RES	*ALL
*OUTSRF		*WELL	*PAVG  *GHGGAS *GHGLIQ *GHGTHY *GHGSCRIT *GHGSOL *GHGAQU *GHGMNR
*OUTSRF		*GRID	*POROS *PERM *PRES *DROP *DATUMPRES *SG *SW *KRG *TEMP
					*DENG  *DENW *RHOG *RHOW *VISG *VISW *PCW  *PCG  *SALIN
					*RMOL 'CO2' *WALL *YALL *ZALL *MOLALITY 'CO2'
**					*STRESI *STRESJ *STRESK *STRESSH *STRESEFF
**					*STRAINI *STRAINJ *STRAINK *STRAINSH *STRNEPL
**					*YOUNG *POISSON *YLDSTATE *VERDSPLGEO  *VDISPL
**					*Z 'CO2' *W 'CO2' *MOLALITY 'CO2'

** Output CO2 inventory special history in mols, std volume, and mass units (from gmghg005)
** These keywords must appear on a line by itself.
*OUTSRF *SPECIAL *CO2-INV-MOLS
*OUTSRF *SPECIAL *CO2-INV-VOL
*OUTSRF *SPECIAL *CO2-INV-MASS

**This keyword activates the CO2 inventory calculations. The amount of CO2 stored in the reservoir (aquifer) under various forms.
*INVENTORY-CO2	*TOTAL

**DIARY specifies the type of timestep information printed to the screen and to the output file during a simulation.
*DIARY *CHANGES


**  ==============  GRID AND RESERVOIR DEFINITION  =================

*GRID *CORNER 107 117 79
*CORNERS   
*include ../data/gridfiles/JD_Sula_2025_flow_seed0_corners.dat

***NETGROSS	*CON 1
*NETGROSS	*IJK
1:107 1:117 1:40 0
1:107 1:117 41:79 1

***POR	*CON 0.1
***POR	*KVAR  66*0.0001  13*0.2
*POR	*ALL
*include {self.params['PORO_file']}

***PERMI	*CON 100
***PERMI	*KVAR  66*0.0001  13*500
*PERMI	*ALL
*include {self.params['PERMX_file']}
*PERMJ	*EQUALSI
***PERMK	*EQUALSI
PERMK  EQUALSI * 0.1

**TRANSF	** Adjusts transmissibilities on a fault basis

***NULL	*IJK
**1:179 1:195 1:20 1
**13 27 32 0
*NULL *ALL
*include ../data/gridfiles/JD_Sula_2025_flow_seed0_null_all.dat

*PINCHOUTARRAY *ALL
*include ../data/gridfiles/JD_Sula_2025_flow_seed0_pinchoutarray_all.dat


***VOLMOD *CON  1
***MOD
**1:100	 1:2	1:11 = 1
**1:100	 99:100 1:11 = 1
**1:2    1:100  1:11 = 1
**99:100 1:100  1:11 = 1

*CPOR  4.35e-7		** rock compressibility in /kPa
*PRPOR  100		** reference pressure for rock compressibility in kPa
***CROCKTYPE 1		** reservoir rock
**	**CP-ROCK 886	** Rock Heat Capacity in J/kg·K
**	**THCONR0 3		** Thermal conductivity of rock in J/m·s·K
**	*CPOR  4.35e-7	** rock compressibility in /kPa
**	*PRPOR  100		** reference pressure for rock compressibility in kPa
**	
***CROCKTYPE 2		** shale
**	**CP-ROCK 886	** Rock Heat Capacity in J/kg·K
**	**THCONR0 1.73	** Thermal conductivity of rock in J/m·s·K
**	*CPOR  4.35e-7	** rock compressibility in /kPa
**	*PRPOR  100		** reference pressure for rock compressibility in kPa
**
*****CTYPE *KVAR  21*2  16*1  4*2 20*1 12*2 90*1
***CTYPE *KVAR  66*2  13*1

****define heat loss to the surrounding rock in the thermal simulation
** *HEAT-LOSS *BOTTOM-TOP-BOUNDARY **Heat loss to take place from the edge, bottom and top of the reservoir
** **rockden(kg/m3)  rockcp(J/kg·K) therm-cond(J/m·s·K)
** *HLPROP 2650    886   1.73

*END-GRID


**  ==============  FLUID DEFINITIONS  ======================
**Note this section references the following templates
**GMGHG001.DAT: CO2 Sequestration Without Geochemistry
**GMGHG002.DAT: CO2 Sequestration w/o Geochemistry, Low Temperature
**GMGHG006.DAT: CO2 Sequestration With Geochemistry

**Use the Peng-Robinson equation of state to model the fluid properties of the oil and gas phases
*MODEL		*PR
*NC			2	2							**number of program and user components
*TRES		270	5	3270	110 			**reservoir depth (m | ft) and temperature (deg C | deg F)
*COMPNAME
			'CO2'          'C1'
*SG        8.1800000E-01  3.0000000E-01		**specific gravity (dimensionless), supercritical co2
*TB       -7.8450000E+01 -1.6145000E+02		**average normal boiling point (deg C | deg F)
*PCRIT     7.2800000E+01  4.5400000E+01		**critical pressure (atm | atm)
*VCRIT     9.4000000E-02  9.9000000E-02		**critical volume (m3/k-mol | m3/k-mol)
*TCRIT     3.0420000E+02  1.9060000E+02		**critical temperature (deg K | deg K)
*AC        2.2500000E-01  8.0000000E-03		**acentric factor (dimensionless)
*MW        4.4010000E+01  1.6043000E+01		**molecular weight (g/gmol | g/gmol)
*HCFLAG    0  0								**whether the user component is a hydrocarbon component

*BIN	    1.0300000E-01					**User Component Interaction Coefficients (Conditional)
*VSHIFT     0.0000000E+00  0.0000000E+00	**Volume Shift Parameters (Optional)
*VISCOR		*HZYT							**Viscosity Correlation Specification (Optional), mixing rule due to Herning and Zipperer (1936)
*MIXVC      1.0000000E+00					**Mixing rule exponent for direct calculation of hydrocarbon phase viscosities. Dimensionless
*VISVC      9.4000000E-02  9.9000000E-02	**Parameters (special values for critical volumes) used for computing the mixture critical volume (m3/kmol)				
*VISCOEFF   1.0230000E-01  2.3364000E-02  
			5.8533000E-02 -4.0758000E-02 
			9.3324000E-03					**coefficients for the Jossi, Stiel and Thodos correlation, or for the Pedersen or Modified Pedersen correlations
*OMEGA      4.5723553E-01  4.5723553E-01	**the equation of state omega-A parameter (dimensionless)
*OMEGB      7.7796074E-02  7.7796074E-02	**the equation of state omega-B parameter (dimensionless)
*PCHOR      7.8000000E+01  7.7000000E+01	**parachor (dimensionless)

*SOLUBILITY	*HENRY							**the general Henry's Law will be used in calculating the solubilities of gases in the aqueous phase
*HENRY-CORR-CO2        						**use Harvey's correlation for CO2 Henry's constant
											**this option makes the Henry's constant a function of pressure, temperature and salinity (up to 150° C and 700 bar)				

*SALINITY-CALC	*OFF						**calculation of salinity. *OFF means salinity of the aqueous phase is assumed constant
*SALINITY		*PPMWT   50000				**the salinity of the aqueous phase in terms of equivalent NaCl concentration (mg NaCl / kg brine). OMV range 35k-65k
*AQFILL 		*ON							**the aquifer is completely filled with water
*TRACE-COMP		2							**set C1 as a trace component that is not soluble in the aqueous phase and that does not flow. 
											**The role of this component is to prevent the hydrocarbon from completely disappearing from a grid-block.

DENW 1000									**mass density of the water component (kg/m3 | lb/ft3) at the reference pressure and reservoir temperature.
VISW 0.5									**Constant water viscosity (cP | cP)

***THERMAL *ON								**perform thermal simulation
**ENTHCOEF	4.7780500E+00  1.1443300E-01  
**			1.0113200E-04 -2.6494000E-08 
**			3.4706000E-12 -1.3140000E-16 
**			-5.5811400E+00  5.6483400E-01 
**			-2.8297300E-04  4.1739900E-07 
**			-1.5255760E-10  1.9588570E-14	**Coefficients for ideal enthalpy calculations. 6 coefficients are required per component.

**  ==============  ROCK-FLUID PROPERTIES  ======================

*ROCKFLUID
*RPT		**relative permeability curves will be defined by table entries.
*SWT		**Water-oil relative permeabilities (from template GMGHG006)
**Sw        krw       krow     Pcow
0.000000  0.000000  0.000000  0.000000
0.050000  0.000000  0.000000  0.000000
0.100000  0.000000  0.000000  0.000000
0.150000  0.000010  0.000000  0.000000
0.200000  0.000150  0.000000  0.000000
0.250000  0.000770  0.000000  0.000000
0.300000  0.002440  0.000000  0.000000
0.350000  0.005950  0.000000  0.000000
0.400000  0.012350  0.000000  0.000000
0.450000  0.022870  0.000000  0.000000
0.500000  0.039020  0.000000  0.000000
0.550000  0.062500  0.000000  0.000000
0.600000  0.095260  0.000000  0.000000
0.650000  0.139470  0.000000  0.000000
0.700000  0.197530  0.000000  0.000000
0.750000  0.272070  0.000000  0.000000
0.800000  0.365950  0.000000  0.000000
0.850000  0.482250  0.000000  0.000000
0.900000  0.624300  0.000000  0.000000
0.950000  0.795620  0.000000  0.000000
1.000000  1.000000  0.000000  0.000000

*SGT		**a liquid-gas relative permeability table dependent on gas saturation
**Sg        krg       krog     Pcog (from template GMGHG006)
**0.000000  0.000000  0.000000  0.000000
**0.050000  0.000080  0.000000  0.000000
**0.100000  0.000680  0.000000  0.000000
**0.150000  0.002330  0.000000  0.000000
**0.200000  0.005610  0.000000  0.000000
**0.250000  0.011140  0.000000  0.000000
**0.300000  0.019610  0.000000  0.000000
**0.350000  0.031740  0.000000  0.000000
**0.400000  0.048370  0.000000  0.000000
**0.450000  0.070420  0.000000  0.000000
**0.500000  0.098940  0.000000  0.000000
**0.550000  0.136180  0.000000  0.000000
**0.600000  0.180650  0.000000  0.000000
**0.650000  0.232750  0.000000  0.000000
**0.700000  0.307520  0.000000  0.000000
**0.750000  0.395200  0.000000  0.000000
**0.800000  0.506570  0.000000  0.000000
**0.850000  0.655620  0.000000  0.000000
**0.900000  0.954430  0.000000  0.000000
**0.950000  0.977220  0.000000  0.000000
**1.000000  1.000000  0.000000  0.000000

**Sg        krg       krog (from OMV HFU2-D-M)
0	0	0.7
8.7E-05	6E-06	0.7
0.051176	0.004419	0.7
0.10235	0.015687	0.7
0.13	0.025205	0.7
0.15353	0.033306	0.69095
0.18118	0.046117	0.68032
0.20471	0.05702	0.67127
0.23235	0.073031	0.66063
0.25588	0.086657	0.65158
0.26	0.089526	0.65
0.28353	0.10592	0.61177
0.30706	0.12231	0.57482
0.33471	0.14492	0.5314
0.35824	0.16416	0.49686
0.38588	0.18978	0.45628
0.40941	0.21159	0.4243
0.43706	0.24019	0.38672
0.46059	0.26453	0.35739
0.48824	0.29608	0.32293
0.51177	0.32293	0.29608
0.53941	0.35739	0.26453
0.56294	0.38672	0.24019
0.59059	0.4243	0.21159
0.61412	0.45628	0.18978
0.64177	0.49686	0.16416
0.66529	0.5314	0.14492
0.69294	0.57482	0.12231
0.71647	0.61177	0.10592
0.74	0.65	0.089526
0.74412	0.65158	0.086657
0.76765	0.66063	0.073031
0.79529	0.67127	0.05702
0.81882	0.68032	0.046117
0.84647	0.69095	0.033306
0.87	0.7	0.025205
0.89765	0.7	0.015687
0.94882	0.7	0.004419
0.99991	0.7	6E-06
1	0.7	0
		
***SGTI		** Imibibition liquid-gas relative permeability table dependent on gas saturation
****Sg        krg       krog	(from OMV HFU2-IMB-M)
****0	0	0.7
****8.7E-05	0	0.7
****0.054375	0	0.7
****0.10875	0	0.7
**0.13	0	0.7
**0.16313	0	0.66688
**0.18	0	0.65
**0.18438	0	0.63438
**0.2175	0	0.52365
**0.23875	0	0.45262
**0.27188	0	0.36115
**0.29313	0	0.30247
**0.32625	0	0.23019
**0.3475	0	0.18383
**0.38063	0	0.12998
**0.40188	0	0.095432
**0.435	0	0.059751
**0.45	0	0.043593
**0.45625	0.00098413	0.036861
**0.48938	0.0062	0.018182
**0.51063	0.018182	0.0062
**0.54375	0.036861	0.00098413
**0.55	0.043593	0
**0.565	0.059751	0
**0.59813	0.095432	0
**0.61938	0.12998	0
**0.6525	0.18383	0
**0.67375	0.23019	0
**0.70688	0.30247	0
**0.72813	0.36115	0
**0.76125	0.45262	0
**0.7825	0.52365	0
**0.81563	0.63438	0
**0.82	0.65	0
**0.83688	0.66688	0
**0.87	0.7	0
**0.89125	0.7	0
**0.94563	0.7	0
**0.99991	0.7	0
**1	0.7	0

*HYSKRG 0.15	** Gas Relative Permeability Hysteresis Parameter (Optional), Maximum residual gas saturation (fraction)

**Rock Density for each gridblock used in calculation of adsorption of component from the gas, aqueous, or solid asphaltene phase onto the reservoir rock
 *ROCKDEN *CON 2650	**defaut in (kg/m3)

**  ==============  INITIAL CONDITIONS  ======================

*INITIAL
**VERTICAL: pressures are determined from the hydrostatic equation and saturations from the capillary pressure tables.
**DEPTH_AVE: block saturations are to be assigned as averages of the corresponding saturations over the depth interval spanned by the grid block.
**WATER_GAS: perform gravity-capillary equilibrium initialization for reservoirs with only water and gas phases initially present.
**NOTRANZONE: the transition from the water to the gas zone is sharp
**EQUIL: With *DEPTH_AVE options, add a pressure correction to each phase (during the simulation) in order that the reservoir initially be in gravitational equilibrium.
*VERTICAL *DEPTH_AVE *WATER_GAS *NOTRANZONE *EQUIL

*ZGAS		0.0001  0.9999		**nc real numbers representing the mole fractions of the nc components in the gas cap fluid in the first initialization region.
*REFPRES	10000				**reference pressure (kPa | psi)
*REFDEPTH	1000				**depth of reference pressure (*REFPRES) (m | ft)
**TEMPER   *KVAR  204.0  208.5  213.0  220.5 **initial reservoir temperature. Any block that does not get defined by *TEMPER will take the temperature from *TRES.
*DWGC		270					**depth of water-gas contact (m | ft)
*SWINIT		*CON	1			**initial water saturation, overrides the water saturation calculated by gravity-capillary equilibrium.
*SEPARATOR	101.325  15.56		**separator pressure (kPa | psi) and temperature (deg C | deg F), default values


**  ==============  NUMERICAL CONTROL  ======================

*NUMERICAL
**Adaptive time stepping control uses an internal heuristic scheme to control the time step size based on past nsteps time steps, 
**using the internally set NORMs, maximum variable changes, maximum residual of pressure and flow equations, 
**number of Newton cycles and stability and threshold criterion for adaptive implicit switching.
**Keyword *NORM and *MAXCHANGE may be over-ridden in presence of keyword *ADTSC, unless *ADTSC *ALLOW *NORMS_MAXCHANGES is in effect.
ADTSC	100		*ON				**default nsteps=5

****Typical changes in the basic variables over a timestep. 
****The timestep size is adjusted internally such that the average change during a timestep equals the entered value.
**NORM		*PRESS		500		**pressure (kPa | psi)
**NORM		*SATUR		0.005
**NORM		*GMOLAR		0.005
**
****Maximum changes in the basic variables during Newtonian iterations.
****If any change in a variable value exceeds *MAXCHANGE, the timestep size is reduced and the timestep is repeated.
**MAXCHANGE	*PRESS		10000	**pressure (kPa | psi), defaut 10000 kPa or 1450 psia
**MAXCHANGE	*GMOLAR		0.8
**MAXCHANGE	*SATUR		0.8
**
****Specifies the criterion for judging the convergence of the Newtonian iterations.
****Two different types of convergence criterion are applied: a change criterion, in which relative changes in primary variables are checked, 
****and a residual criterion, in which the residuals of the equations being set iteratively to zero are checked. 
****If either criterion is satisfied, the iteration is judged to have converged.
**CONVERGE	*PRESS		7.E-04	**changes convergence tolerance for pressure (kPa | psia), default 3.55 kPa or 0.514 psia
**CONVERGE	*WATER		5.E-05	**relative changes convergence tolerance for water molar density (dimensionless), defaut 0.01
**CONVERGE	*TEMP		1.E-03	**relative changes convergence tolerance for temperature (°C | °F), 0.001 °C or °F
**CONVERGE	*HC			5.E-05	**relative changes convergence tolerance for a hydrocarbon component molar density (dimensionless), defaut 0.01
**CONVERGE	*MAXRES		1.E-04	**maximum scaled residual allowed for any single equation at convergence (dimensionless), defaut 0.001
**
**DTMIN		1.E-06				**minimum timestep size (days | days ), default 1.E-05 days
**DTMAX		182.5				**maximum timestep size (days | days ), default 365 days
**
**NORTH		60					**maximum number of orthogonalizations (GMRES steps) performed before resetting, which affects the amount of storage used, default 40


**  ==============  GEOMECHANIC SECTION  ====================

*GEOMECH						** Main keyword for using geomechanics module
*GEOM3D							** Using 3D finite elements
*GCOUPLING	2					** Two-way coupling: porosity is a function of P, T and total mean stress. To couple perm, perm multiplier is needed

*ITERMAXG	200					** Maximum number of linear solver iterations allowed before returning to calling routine. Defaut is 30.
*NITERGEO	100					** Maximum number of iterations allowed for solving the force balance equations. The minimum is 30.
*GCUPDATE	10					** frequency or time of updating geomechanical conditions and the resulting porosities

*GEOGRID *GCORNER 107 117 10	
*GCORNERS
*include ../data/gridfiles/JD_Sula_2025_gmc_grid.dat

** *GNULL *IJK					** Null blocks
**     13   27   32

**GPTOLMUL  0.7					**Pressure tolerance multiplier used in computing coefficients for porosity formulae, default 1
**STRESSTOL 0.07				**Maximum allowed stress difference allowed for each grid block (kPa | psi), range is 0 to 10 kPa (0 to 1.45 psi).
								**At most one of *PRESSTOL, *STRESSTOL and *POROSTOL is used.

** Note: The yielding stress has a high value to avoid plastics occuring.
***GEOROCK 1						**reservoir rock
**	*ELASTMOD		2E+07		** Elastic Young's modulus (kPa)
**	*POISSRATIO		0.3			** Poisson's ratio
**	*COHESION		1E+10		** Cohesion for Mohr-Coulomb and Drucker-Prager materials (kPa)
**	*HARDEN			0			** Hardening parameter for the linear strain hardening option (kPa).
**	*FRICANGLE		28.0		** Friction angle (degrees)
**	*BIOTSCOEF		1			** Biot's coefficient
**	*THEXPCOEF   	4E-06		** linear thermal expansion coefficient for solid rock (1/C)
**
***GEOROCK 2						** shale
**	*ELASTMOD		1E+07
**	*POISSRATIO		0.3
**	*COHESION		1E+10
**	*HARDEN			0
**	*FRICANGLE		28.0
**	*BIOTSCOEF		1
**	*THEXPCOEF   	4E-06
**
***GEOTYPE *KVAR  33*2  6*1
**use same geomechanical parameters for all formations
*ELASTMOD		{self.params['E_GPa']}
*POISSRATIO		{self.params['PR']}
*COHESION		1E+10
*HARDEN			0
*FRICANGLE		28.0
*BIOTSCOEF		1
*THEXPCOEF   	4E-06

****Assign the initial stress distribution for 3D finite elements (kPa | psi)
**			**sigma_x	sigma_y	sigma_z	sigma_xy	sigma_yz	sigma_xz
***STRESS3D	3E+04		3E+04	3E+04	0			0			0

**Assign the initial stress gradient distribution for 3D finite elements (kPa/m | psi/ft)
				**strgrd_x	strgrd_y	strgrd_z	strgrd_xy	strgrd_yz	strgrd_xz (derived from OMV data)
*STRESSGRAD3D	{self.params['sigma_x']}		{self.params['sigma_y']}		{self.params['Sv_MPa/km']}			{self.params['tau_xy']}			0			0

*PRESCBC3D	**Prescribe displacement-type boundary conditions on a nodal point of a 3D finite element
*IJK  1:107 1:117  10
**nodes    direction    displacement (m | ft)
5:8         01:03            0.0

**Enable independent graphics file (SR2) for geomechanics
*GOUTSRF  *GGRID
PRES	TEMP	GEORTYPE	YOUNG	POISSON
STRESI  STRESJ  STRESK  STRESNORM 
STRAINI STRAINJ STRAINK	STRAINVOL
VERDSPLGEO	**Vertical displacement "up" based on geomechanics, at centre of cell
VDISPL	**Vector of grid displacement
YLDSTATE **yield stress state with 0-4 indicators


**  ==============  WELL AND RECURRENT DATA  ======================

*RUN
*DATE		2030 1 1
*DTWELL		0.1						**the timestep size of the first timestep after a non-trivial well change (days | days )					
*AIMSET		*CON 1						**Sets all blocks to implicit
*AIMWELL	*WELLNN						**Sets the neighbours of active well blocks and the neighbours of the neighbours to implicit
*WELPRN		1 *WI						**Print a table of completion layer wise well index and associated key parameters for each well in the list 
										**where significant well or perforation change has occurred.
*WELL		1 'I02_4km'
*WELL		2 'I03_4km'
*WELL		3 'I04_4km'
*WELL		4 'I05_4km'
*WELL		5 'I06_4km'

***INJECTOR	1
*INJECTOR	1:5
*INCOMP		*SOLVENT  1.0  0.0			**compositions of injected fluid
*OPERATE	*MAX  *STG  2.2e+06   *CONT	**surface gas rate (m3/day | ft3/day ) constraint, equivalent to 1.48 million ton per year
***OPERATE	*MAX  *BHP  34000   *CONT	**bottom-hole pressure (kPa | psi ) constraint

***INJECTOR	'I02_4km'
***OPERATE	*MAX  *BHP  34000   *CONT	**bottom-hole pressure (kPa | psi ) constraint
***INJECTOR	'I03_4km'
***OPERATE	*MAX  *BHP  31700   *CONT	**bottom-hole pressure (kPa | psi ) constraint
***INJECTOR	'I04_4km'
***OPERATE	*MAX  *BHP  29700   *CONT	**bottom-hole pressure (kPa | psi ) constraint
***INJECTOR	'I05_4km'
***OPERATE	*MAX  *BHP  28300   *CONT	**bottom-hole pressure (kPa | psi ) constraint
***INJECTOR	'I06_4km'
***OPERATE	*MAX  *BHP  27900   *CONT	**bottom-hole pressure (kPa | psi ) constraint

*INJ-TEMP	1:5	
			5*20							**temperature of injected fluid  (C | F)
***INJ-TEMP	'I02_4km'	
**			20							**temperature of injected fluid  (C | F)
						
**well geometric characteristics used for calculating well index internally
	**direction radius(m|ft)  geometricFactor  wfrac  skin
*GEOMETRY  *K  0.09525  0.34    1.0    0.0

**In Petrel surface locations of I02_4km to I06_4km: (18, 62), (27, 54), (35, 46), (43, 38), (51, 30)
**Note in CMG j is reversed
**location of the well completion grid blocks, well indices or parameters for well index calculations
*PERF	*GEO  'I02_4km'			**GEO: geometric factor
** if jf  kf   ff (partial completion factor)
18 55 60   1.0
18 55 61   1.0
18 55 62   1.0
18 55 63   1.0
18 55 64   1.0
18 55 65   1.0
18 55 66   1.0
18 55 67   1.0
18 55 68   1.0  
18 55 69   1.0  
18 55 70   1.0  
18 55 71   1.0  
18 55 72   1.0  
18 55 73   1.0  
18 55 74   1.0  


*PERF	*GEO  'I03_4km'			**GEO: geometric factor
** if jf  kf   ff (partial completion factor)
27 63 60   1.0
27 63 61   1.0
27 63 62   1.0  
27 63 63   1.0  
27 63 64   1.0  
27 63 65   1.0  
27 63 66   1.0  
27 63 67   1.0  
27 63 68   1.0  
27 63 69   1.0  
27 63 70   1.0  
27 63 71   1.0  
27 63 72   1.0  
27 63 73   1.0  
27 63 74   1.0  
  

*PERF	*GEO  'I04_4km'			**GEO: geometric factor
** if jf  kf   ff (partial completion factor)
35 71 60   1.0 
35 71 61   1.0
35 71 62   1.0   
35 71 63   1.0  
35 71 64   1.0  
35 71 65   1.0  
35 71 66   1.0  
35 71 67   1.0  
35 71 68   1.0  
35 71 69   1.0  
35 71 70   1.0  
35 71 71   1.0  
35 71 72   1.0  
35 71 73   1.0  
35 71 74   1.0  


*PERF	*GEO  'I05_4km'			**GEO: geometric factor
** if jf  kf   ff (partial completion factor) 
43 79 60   1.0  
43 79 61   1.0  
43 79 62   1.0  
43 79 63   1.0  
43 79 64   1.0  
43 79 65   1.0  
43 79 66   1.0 
43 79 67   1.0  
43 79 68   1.0  
43 79 69   1.0  
43 79 70   1.0  
43 79 71   1.0  
43 79 72   1.0  
43 79 73   1.0  
43 79 74   1.0  
43 79 75   1.0  
43 79 76   1.0  
43 79 77   1.0  
43 79 78   1.0  
43 79 79   1.0  


*PERF	*GEO  'I06_4km'			**GEO: geometric factor
** if jf  kf   ff (partial completion factor)
51 87 64   1.0  
51 87 65   1.0  
51 87 66   1.0 
51 87 67   1.0  
51 87 68   1.0  
51 87 69   1.0  
51 87 70   1.0  
51 87 71   1.0  
51 87 72   1.0  
51 87 73   1.0  
51 87 74   1.0  
51 87 75   1.0  
51 87 76   1.0  
51 87 77   1.0  
51 87 78   1.0  
51 87 79   1.0  

*DATE 2040 1 1
*DATE 2050 1 1
*SHUTIN		1:5

*DATE 2055 1 1
*DATE 2060 1 1
*GCUPDATE	*TIME

*DATE 2150 1 1
*DATE 2250 1 1
*DATE 2450 1 1
*DATE 2650 1 1
*DATE 3050 1 1

***DATE 2550 1 1
***DATE 3050 1 1

*STOP
              """, file = fileID)


