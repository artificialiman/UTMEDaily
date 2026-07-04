# PHYSICAL CHEMISTRY

Every chapter before this one answered *what* forms and *why*. This one answers three different questions about the exact same reactions: how fast, which way, and how much energy. Nothing here creates new substances — it explains the behavior of substances this book has already named.

---

## I. STATES OF MATTER & GAS LAWS

### The Gate

```
GATE → How much does intermolecular force (Bonding & Periodicity, Section V) win against particle energy?
   Force wins completely   → Solid (fixed position, vibrates only)
   Force wins partially     → Liquid (holds together, particles still move past each other)
   Force loses entirely     → Gas (particles independent, force negligible)
```

State was never a separate property to memorize per substance — it's the same intermolecular force table from Bonding & Periodicity, now read against temperature instead of against chain length. Water is liquid at room temperature because hydrogen bonding wins against room-temperature particle energy; raise the energy past boiling point and the same force loses.

### Gas laws, as constants and relationships

| Law | Relationship | Constant held |
|---|---|---|
| Boyle's Law | P1V1 = P2V2 | Temperature |
| Charles's Law | V1/T1 = V2/T2 | Pressure |
| Gay-Lussac's Law | P1/T1 = P2/T2 | Volume |
| Combined Gas Law | P1V1/T1 = P2V2/T2 | Amount of gas (moles) |
| Ideal Gas Equation | PV = nRT | Nothing — this is the general case the other three are special cases of |

### Constants worth knowing cold

| Constant | Value |
|---|---|
| Gas constant, R | 8.314 J K⁻¹ mol⁻¹ |
| Molar volume of a gas at STP | 22.4 dm³ (22,400 cm³) per mole |
| STP (Standard Temperature and Pressure) | 0°C (273 K), 1 atm (101,325 Pa) |
| Avogadro's number | 6.02 × 10²³ particles per mole |

Relationship one-liner: **Boyle's, Charles's, and Gay-Lussac's laws are not three laws — they're PV = nRT with one variable frozen each time, the same way the Periodic Table's four trends were one tug-of-war read four times.**

### Graham's Law of Diffusion

```
rate1/rate2 = √(M2/M1)          (lighter gas diffuses faster — inversely to the square root of molar mass)
```

This is why ammonia (NH3, M=17) and hydrogen chloride (HCl, M=36.5) released from opposite ends of a tube meet closer to the HCl end — the lighter gas simply outruns the heavier one, no new chemistry involved, just kinetic theory doing arithmetic on two different masses.

---

## II. ENERGETICS (THERMOCHEMISTRY)

### The Gate

```
GATE → Does the reaction release or absorb energy, net?
   Releases (products lower energy than reactants) → Exothermic, ΔH negative
   Absorbs (products higher energy than reactants)  → Endothermic, ΔH positive
```

| Reaction type | Example from earlier chapters | Sign of ΔH |
|---|---|---|
| Combustion | Organic, Section I | Exothermic — always |
| Neutralization | Compound Chemistry, Section I | Exothermic — always |
| Thermal decomposition | CaCO3 → CaO + CO2 (Compound Chemistry oxide gate) | Endothermic — always needs continuous heat |

### Bond energy — the real source of every ΔH

```
ΔH = (energy to break bonds in reactants) − (energy released forming bonds in products)
```

Breaking a bond always costs energy; forming one always releases it. This is the exact mechanism behind Bonding & Periodicity's claim that boiling breaks intermolecular grip, not covalent bonds — boiling's energy cost is tiny compared to the energy a true bond-breaking reaction like combustion demands, because you're only fighting Van der Waals forces, not sigma or pi bonds.

### Hess's Law — energy doesn't care about the route

```
ΔH(direct route) = ΔH(step 1) + ΔH(step 2) + ... (indirect route)
```

Relationship one-liner: **Hess's Law is the energetics version of the salt preparation gate — just as it didn't matter which method produced a soluble salt so long as solubility rules were obeyed, it doesn't matter which path a reaction takes so long as start and end points are the same. Total energy change is a destination, not a route.**

### Activation energy

```
reactants --(Ea, activation energy hill)--> transition state --(downhill)--> products
```

Even a strongly exothermic reaction needs an initial energy investment to start — this is why a mixture of hydrogen and oxygen sits stable at room temperature despite an enormously exothermic reaction waiting to happen the moment a spark supplies Ea.

---

## III. KINETICS — how fast, not which way

### The Gate

```
GATE → What increases the frequency or energy of successful particle collisions?
   Temperature increase   → More particles exceed Ea, AND particles collide more often
   Concentration increase → More particles per volume, more collisions per second
   Surface area increase  → More particles exposed at the reacting boundary
   Catalyst added         → Lowers Ea itself — same collisions, more of them succeed
```

| Factor | Mechanism | Does it change Ea? |
|---|---|---|
| Temperature | Faster particles, more frequent AND more energetic collisions | No — same Ea, more particles clear it |
| Concentration | More particles in the same volume | No |
| Surface area | More exposed reacting particles | No |
| Catalyst | Provides an alternative, lower-energy pathway | Yes — this is the only factor that actually changes Ea |

Relationship one-liner: **a catalyst is the only kinetic factor that cheats the activation energy hill instead of just sending more particles at it.** Every other factor listed above works by brute force — more heat, more particles, more surface. A catalyst works by shortcut.

Collision theory itself is just Section I's kinetic theory (particles in constant motion) combined with Section II's activation energy (a threshold that must be cleared) — a reaction only happens when a collision has both the right orientation and enough energy to clear Ea. Miss either condition and the collision is wasted.

---

## IV. EQUILIBRIUM — reversible reactions, and which way they lean

Every ⇌ symbol already used in this book (Haber Process, Contact Process — Metallurgy, Industry & Environment, Section II) was quietly pointing here.

### The Gate

```
GATE → Le Chatelier's Principle: a system at equilibrium, disturbed, shifts to oppose the disturbance
   Increase pressure  → Shifts toward the side with fewer gas moles
   Increase temperature → Shifts toward the endothermic direction
   Increase concentration of a reactant → Shifts toward products
   Add a catalyst → No shift — speeds up both directions equally, reaches the same equilibrium faster
```

### Reading the Haber and Contact processes as Le Chatelier in action

| Process | Equilibrium | Conditions chosen | Why |
|---|---|---|---|
| Haber | N2 + 3H2 ⇌ 2NH3 (exothermic) | High pressure, moderate (not maximum) temperature, iron catalyst | High pressure favors the side with fewer moles (2 vs 4) — pushes toward NH3. Full-maximum temperature would favor yield less (exothermic reaction shifts backward when heated) but is used anyway in moderation to keep rate acceptable — a deliberate trade between Section III's kinetics and this section's equilibrium yield |
| Contact | 2SO2 + O2 ⇌ 2SO3 (exothermic) | Moderate temperature (~450°C), vanadium(V) oxide catalyst, near-atmospheric pressure | Same trade — pure yield-maximizing conditions would be too slow to be economical; the catalyst substitutes for extreme pressure/temperature by lowering Ea directly (Section III) |

This is the one-liner worth landing here: **industrial conditions are never "the conditions equilibrium wants" — they're the conditions equilibrium and kinetics can both agree to live with.** Every real industrial process in this book is a compromise between Section III (make it fast enough to be worth running) and Section IV (make it favorable enough to be worth running), and the catalyst is usually what buys the compromise.

---

## V. ELECTROCHEMISTRY — where the Activity Series becomes measurable

### Redox — the general form of every reaction this book has already run

```
Oxidation: loss of electrons (OIL — Oxidation Is Loss)
Reduction: gain of electrons (RIG — Reduction Is Gain)
```

| Reaction from earlier chapters | Oxidation half | Reduction half |
|---|---|---|
| Displacement (Bonding & Periodicity VI) | Zn → Zn²⁺ + 2e⁻ | Cu²⁺ + 2e⁻ → Cu |
| Rusting (Metallurgy, Industry & Environment IV) | Fe → Fe²⁺ + 2e⁻ | O2 + 2H2O + 4e⁻ → 4OH⁻ |
| Extraction, carbon reduction (Metallurgy, Industry & Environment I) | C → C (in CO) loses nothing itself; CO is oxidized to CO2 | Fe³⁺ (in Fe2O3) reduced to Fe |

Every reaction this book has labeled "displacement," "extraction," or "corrosion" was already redox — this section just gives it the vocabulary and the electron-counting method it was missing.

### Electrolysis — forcing the Activity Series backward

```
GATE → At the cathode (reduction): which cation is discharged?
   Least reactive cation present (lowest on Activity Series) discharges first
GATE → At the anode (oxidation): which anion is discharged?
   Halide present → halide discharges before OH⁻
   No halide → OH⁻ discharges, releasing O2
```

| Electrolyte | Cathode product | Anode product | Why |
|---|---|---|---|
| Molten NaCl | Na (metal) | Cl2 | Molten — only Na⁺ and Cl⁻ present, no competition |
| Aqueous NaCl (brine) | H2 (not Na!) | Cl2 | H⁺ (from water) is lower on the Activity Series than Na⁺, so it discharges instead |
| Aqueous CuSO4 | Cu (metal) | O2 | Cu²⁺ is low enough to out-discharge H⁺; SO4²⁻ never discharges over OH⁻ |

Relationship one-liner: **electrolysis is the Activity Series, forced to run backward at gunpoint — instead of a reactive metal naturally giving up electrons to a less reactive one, an external current strips electrons from whatever's most reluctant to give them up, which is exactly why the position on the series still decides the outcome even though the "natural" direction has been overridden.**

### Cells — the Activity Series running forward, on purpose

```
Galvanic (voltaic) cell: spontaneous redox → generates electricity (batteries)
Electrolytic cell: electricity forced in → drives non-spontaneous redox (electrolysis, above)
```

A simple cell (e.g., zinc and copper electrodes in their salt solutions, connected by a wire and a salt bridge) generates a voltage precisely because zinc sits above copper on the Activity Series — the same displacement reaction from Section VI of Bonding & Periodicity, except the electron transfer is routed through a wire instead of happening on contact, which is the only difference between a spontaneous reaction releasing heat and one generating usable current.

---

## THE COMPLETE HIERARCHY, RESTATED

```
STATE OF MATTER (intermolecular force vs particle energy — Bonding & Periodicity V, now against temperature)
   ↓
ENERGETICS (does the reaction release or cost energy — bond-breaking vs bond-forming, Hess's Law)
   ↓
KINETICS (how fast — collision theory, activation energy, the only factor a catalyst actually cheats)
   ↓
EQUILIBRIUM (which way, and how far — Le Chatelier, the real logic behind Haber/Contact conditions)
   ↓
ELECTROCHEMISTRY (redox as the general form of displacement, extraction, and corrosion —
                   electrolysis as the Activity Series run backward, cells as it run forward)
```

Physical Chemistry doesn't introduce a new set of reactions. It hands you the three remaining questions — how fast, which way, how much energy — for every reaction this book has already named, and closes the loop by revealing that redox was the general case sitting underneath displacement, rusting, and extraction the entire time.
