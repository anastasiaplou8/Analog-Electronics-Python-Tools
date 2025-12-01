"""
Push–Pull Class-B Output Stage Analyzer 
---------------------------------------

Step 1:
    Theoretical calculations for Uin = 10 Vp-p
    (max undistorted output, class-B push-pull).

Step 2 & 3:
    General calculator where you can enter "measured" values
    (Uin, Uout, VR2_dc) as if you were turning the potentiometer
    in the lab and observing the oscilloscope / multimeter.

    For each case it calculates:
    - Pout
    - PDC
    - PD (per transistor)
    - efficiency (eta)
    - Av = Uout_pp / Uin_pp

Author: Anastasia Plou
"""

import math

# ================================
# Common circuit parameters
# ================================
VCC = 10.0       # supply voltage (V)
RL  = 15.0       # load resistor (ohm)
R1  = 1e3        # upper bias resistor (ohm)
R2  = 1e3        # lower bias resistor (ohm)

# For step 1 we assume ideal class-B with
# maximum undistorted output swing:
# Uout_pp(max) ≈ VCC


# =========================================
# STEP 1: Theoretical calculations (Uin=10 Vp-p)
# =========================================
def step1_theoretical():
    print("\n==============================")
    print(" STEP 1 – THEORETICAL (Uin = 10 Vp-p)")
    print("==============================")

    Uin_pp  = 10.0            # given by the exercise (generator)
    Uout_pp = VCC             # for ideal class-B, max undistorted ≈ VCC

    Vpeak = Uout_pp / 2.0
    Vrms  = Vpeak / math.sqrt(2.0)

    # Output power
    Pout = Vrms**2 / RL  # [W]

    # Load / transistor currents
    I_peak = Vpeak / RL             # peak load current
    I_av   = I_peak / math.pi       # average current of the conducting transistor

    # Bias current through R1+R2 (from VCC to ground)
    Ibias = VCC / (R1 + R2)         # [A]

    # Total DC current from supply
    Idc = I_av + Ibias

    # DC power from supply
    Pdc = VCC * Idc

    # Power dissipation per transistor
    # Pdc = Pout + 2*PD  ->  PD = (Pdc - Pout)/2
    Pd_each = (Pdc - Pout) / 2.0

    # Efficiency
    eta = Pout / Pdc

    print(f"VCC       = {VCC:.2f} V")
    print(f"RL        = {RL:.2f} Ω")
    print(f"Uin_pp    = {Uin_pp:.2f} Vp-p")
    print(f"Uout_pp   = {Uout_pp:.2f} Vp-p (max undistorted)")
    print()
    print(f"Vpeak     = {Vpeak:.2f} V")
    print(f"Vrms      = {Vrms:.3f} V")
    print(f"I_peak    = {I_peak*1e3:.1f} mA")
    print(f"I_av      = {I_av*1e3:.1f} mA  (per transistor)")
    print(f"Ibias     = {Ibias*1e3:.1f} mA")
    print(f"IDC       = {Idc*1e3:.1f} mA  (total from supply)")
    print()
    print(f"Pout      = {Pout*1e3:.1f} mW")
    print(f"PDC       = {Pdc*1e3:.1f} mW")
    print(f"PD_each   = {Pd_each*1e3:.1f} mW  (per transistor)")
    print(f"η         = {eta*100:.1f} %  (efficiency)")
    print()
    print("Theoretical max efficiency for class-B: η_max = π/4 ≈ 78.5 %")


# =========================================
# Generic analyzer for Steps 2 & 3
# =========================================
def analyze_case(label, Uin_pp, Uout_pp, V_R2_dc):
    """
    Analyze a push–pull case using "measured" values.

    Parameters
    ----------
    label : str
        Name of the case (e.g. 'Step 2', 'Step 3 – best bias').
    Uin_pp : float
        Input signal amplitude in Vp-p (as set on generator).
    Uout_pp : float
        Measured output amplitude on RL in Vp-p.
    V_R2_dc : float
        Measured DC voltage across R2 (in volts).
        Used to compute Ibias = V_R2_dc / R2.
    """

    print("\n==============================")
    print(f" {label}")
    print("==============================")

    # 1. Basic voltages & currents
    Vpeak = Uout_pp / 2.0
    Vrms  = Vpeak / math.sqrt(2.0)

    I_peak = Vpeak / RL        # peak load current
    I_av   = I_peak / math.pi  # average current of conducting transistor

    Ibias  = V_R2_dc / R2      # bias current (through R2)
    Idc    = I_av + Ibias      # total DC from supply (as in exercise)

    # 2. Powers
    Pout   = Vrms**2 / RL      # output power on RL
    Pdc    = VCC * Idc         # DC power from supply

    # protect against division by zero just in case
    if Pdc > 0:
        Pd_each = (Pdc - Pout) / 2.0
        eta     = Pout / Pdc
    else:
        Pd_each = 0.0
        eta     = 0.0

    # 3. Voltage gain
    if Uin_pp > 0:
        Av = Uout_pp / Uin_pp
    else:
        Av = 0.0

    # 4. Print results
    print(f"Uin_pp    = {Uin_pp:.2f} Vp-p")
    print(f"Uout_pp   = {Uout_pp:.2f} Vp-p")
    print(f"V_R2_dc   = {V_R2_dc:.2f} V  (across R2)")
    print()
    print(f"Vpeak     = {Vpeak:.2f} V")
    print(f"Vrms      = {Vrms:.3f} V")
    print(f"I_peak    = {I_peak*1e3:.1f} mA")
    print(f"I_av      = {I_av*1e3:.1f} mA  (per transistor)")
    print(f"Ibias     = {Ibias*1e3:.1f} mA")
    print(f"IDC       = {Idc*1e3:.1f} mA  (total from supply)")
    print()
    print(f"Pout      = {Pout*1e3:.1f} mW")
    print(f"PDC       = {Pdc*1e3:.1f} mW")
    print(f"PD_each   = {Pd_each*1e3:.1f} mW  (per transistor)")
    print(f"η         = {eta*100:.1f} %  (efficiency)")
    print(f"Av        = {Av:.2f}  (voltage gain Uout_pp / Uin_pp)")
    print()

    # Simple qualitative hint about crossover:
    # if Uout_pp is much smaller than a "linear" expectation,
    # or waveform on scope shows dent around 0V, then crossover is present.
    if Av < 0.8:  # purely indicative threshold
        print("Hint: Low gain – likely strong crossover or clipping.")
    else:
        print("Hint: Gain looks reasonable – check waveform for remaining distortion.")


# =========================================
# Example usage
# =========================================
if __name__ == "__main__":
    # --- Step 1 theoretical ---
    step1_theoretical()

    # --- Step 2 example (you can edit numbers) ---
    # Suppose in the lab we set:
    # Uin_pp = 5 Vp-p, measured Uout_pp = 4 Vp-p,
    # DC voltage on R2 = 2.0 V (just an example).
    analyze_case(
        label="Step 2 – Example measurement",
        Uin_pp=5.0,
        Uout_pp=4.0,
        V_R2_dc=2.0
    )

    # --- Step 3 example (after adjusting potentiometer for best bias) ---
    # You can change these numbers to match your own measurements.
    analyze_case(
        label="Step 3 – Example (adjusted bias)",
        Uin_pp=5.0,
        Uout_pp=6.0,
        V_R2_dc=3.5
    )
