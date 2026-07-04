# METALLURGY, INDUSTRY & ENVIRONMENT

One question decides which pocket you're in: what state did nature hand you the raw material in?

```
GATE → Mineral ore (solid, locked in rock) / Crude extract (liquid or gas, needs separation not extraction) / Natural solution (already dissolved in water)
```

This isn't three unrelated industries wearing one chapter title. It's the same "how do I get the useful thing out of the thing nature gave me" question, asked three times, and the answer each time depends entirely on which physical state you started with.

---

## I. MINERAL ORE — the solid route

An ore is a rock rich enough in a compound of a metal to be worth extracting from. Which extraction method works is not a choice — it's dictated entirely by where the metal sits on the Activity Series (Bonding & Periodicity, Section VI).

### The Gate

```
GATE → Where does the metal sit on the Activity Series?
   Above carbon (K, Na, Ca, Mg, Al)   → Electrolysis (too reactive for anything but raw electron transfer to work)
   Around/below carbon (Zn, Fe, Pb, Cu) → Carbon reduction (cheaper — let carbon do the electron-stealing)
   Bottom of series (Ag, Au)            → Found native, or simple thermal decomposition — barely needs "extracting" at all
```

| Ore | Metal | Method | Why this method |
|---|---|---|---|
| Bauxite (Al2O3) | Aluminum | Electrolysis | Above carbon — carbon can't out-compete it for electrons |
| Hematite (Fe2O3) | Iron | Carbon reduction, blast furnace | Below carbon — carbon happily takes the oxygen instead |
| Galena (PbS) | Lead | Roasting then carbon reduction | Below carbon, but needs converting to oxide first |
| Native gold | Gold | Physical separation only | Bottom of series — barely reacts with anything, least of all needs "winning" from a compound |

Relationship one-liner: **extraction method was never a separate fact to memorize per metal — it's the Activity Series read as a purchasing decision. You spend the cheapest method (carbon) wherever it's strong enough to win, and only pay for electrolysis where nothing cheaper can out-compete the metal for its own electrons.**

### The Blast Furnace, as an operation

```
INPUT: iron ore (Fe2O3) + coke (C) + limestone (CaCO3), hot air blast
STEP 1: C + O2 → CO2
STEP 2: CO2 + C → 2CO                          (carbon monoxide, the real reducing agent)
STEP 3: Fe2O3 + 3CO → 2Fe + 3CO2               (iron won, oxygen lost)
STEP 4: CaCO3 → CaO + CO2                      (limestone decomposes)
STEP 5: CaO + SiO2 → CaSiO3 (slag)             (removes sand/silica impurity)
OUTPUT: molten iron (sinks, tapped off) + slag (floats, tapped off separately)
```

Nothing here is new chemistry. Step 3 is a displacement reaction exactly like Bonding & Periodicity's Activity Series table predicted — carbon monoxide simply is more willing to hold oxygen than iron is, at blast furnace temperature.

---

## II. CRUDE EXTRACT — the liquid/gas route

Petroleum was already covered as a separation problem (Organic, Section VI) — long chains condense low, short chains rise high, fractional distillation sorts by boiling point. This pocket is what happens *after* sorting: what industry does with the fractions and the gases sitting alongside them.

### Petrochemicals — the industry built on the fractions

```
naphtha (short-chain fraction) --(cracking, heat + catalyst)--> shorter alkanes + alkenes
```

Cracking is Organic's addition/pi-bond logic run backward for profit: a long, low-value saturated chain is broken to manufacture the short, high-value unsaturated ones (ethene, propene) that feed straight into Organic Section V's addition polymerization — polyethene, polypropene, all downstream of one cracked bond.

### Natural gas as feedstock — the Haber Process

Natural gas isn't only a fuel fraction — it's the hydrogen source for the single largest manufactured chemical by volume worldwide: ammonia.

```
N2 + 3H2 ⇌ 2NH3        (Haber Process — reversible, equilibrium favored by high pressure, moderate heat, iron catalyst)
```

| Source of reactant | Where it comes from |
|---|---|
| N2 | Fractional distillation of liquid air |
| H2 | Natural gas (crude extract, this pocket) or electrolysis of water |

Ammonia's onward use closes a loop already opened in Compound Chemistry: NH3 + HNO3 → NH4NO3, ammonium nitrate, a fertilizer — an acid-base neutralization (Compound Chemistry, Section I) running at industrial scale to feed the same soil that grows the crop a WAEC Agricultural Science paper might ask about next door.

### Sulfur, recovered in the same refining stream — the Contact Process

Petroleum refining strips sulfur out of crude oil as a purification step, and that recovered sulfur becomes the raw material for the second-largest manufactured chemical:

```
S + O2 → SO2
2SO2 + O2 ⇌ 2SO3        (Contact Process — vanadium(V) oxide catalyst)
SO3 + H2SO4 → H2S2O7    (oleum, then diluted)
H2S2O7 + H2O → 2H2SO4
```

Sulfuric acid produced this way is the acid sitting behind roughly every category in Compound Chemistry's Section I acid table — car batteries, fertilizer manufacture, and a large share of industrial salt preparation all trace back to this one crude-extract byproduct.

---

## III. NATURAL SOLUTION — the dissolved route

Seawater and brine are natural solutions dense with dissolved ions, and extracting from them means running electrolysis or precipitation directly on what's already dissolved — no ore-crushing, no fractionating column, because nature already did the dissolving step for you.

| Target | Source | Method |
|---|---|---|
| NaCl | Evaporated seawater/brine | Simple evaporation (Compound Chemistry, Section VIII) |
| Bromine | Seawater | Chlorine gas displaces bromide — Cl2 + 2Br⁻ → Br2 + 2Cl⁻, a straightforward Activity Series displacement, chlorine ranking above bromine |
| Magnesium | Seawater | Precipitated as Mg(OH)2 using lime, then electrolysis of the molten chloride |

### Water hardness — a natural solution's inconvenient extra dissolved ions

```
GATE → Temporary hardness (Ca(HCO3)2, Mg(HCO3)2 dissolved) / Permanent hardness (CaSO4, MgSO4 dissolved)
   Temporary → removed by boiling: Ca(HCO3)2 → CaCO3 (precipitates) + H2O + CO2
   Permanent → boiling does nothing — needs ion exchange or washing soda (Na2CO3) to precipitate the Ca2+/Mg2+ out
```

The one-liner: **hardness was never a separate topic from Compound Chemistry's solubility rules — it's the same "which salts stay dissolved" table, showing up uninvited in your kettle instead of your test tube.**

---

## IV. ENVIRONMENTAL CHEMISTRY — where all three routes leave a residue

### Corrosion — rusting as an electrochemical reaction, not just "iron getting old"

```
Fe → Fe2+ + 2e⁻                          (iron oxidizes)
O2 + 2H2O + 4e⁻ → 4OH⁻                    (oxygen, dissolved in surface water, is reduced)
Fe2+ + 2OH⁻ → Fe(OH)2 → (further oxidation) → Fe2O3·xH2O   (rust)
```

Rusting needs both water and oxygen present together — remove either and the reaction stalls, which is the entire logic behind every rust-prevention method:

| Method | How it works |
|---|---|
| Painting/greasing | Physical barrier — blocks water and oxygen from reaching the iron at all |
| Galvanizing (zinc coating) | Zinc sits above iron on the Activity Series — it corrodes preferentially, sacrificing itself so the iron underneath doesn't have to |
| Sacrificial anode | Same logic as galvanizing, deliberately attached rather than coated — a block of magnesium wired to a ship's hull, giving up its own electrons so the hull's iron keeps them |

Every prevention method on this table is the Activity Series again — corrosion resistance was never a separate property, it's reactivity ranking applied to "which metal loses electrons first."

### Acid rain — the oxide gate, rained on

```
SO2 + H2O → H2SO3           (from Contact Process feedstock combustion, or fuel oil impurities)
NO2 + H2O → HNO3 + NO       (from vehicle engines, high-temperature N2 + O2 combination)
```

This is Compound Chemistry's oxide gate (Section 0) running involuntarily in the atmosphere: an acidic nonmetal oxide meeting water, forming an acid, exactly as predicted — except the "beaker" this time is a rain cloud, and the runoff lands on soil, lakes, and limestone buildings instead of a test tube.

---

## V. THE ELEMENTAL CYCLES — carbon, nitrogen, hydrogen, and water, moving in circles

Nothing in this chapter's industrial processes actually consumes an element. Every atom mined, cracked, or fixed is borrowed from a cycle that was already running before industry started, and returned to it afterward — usually through the exact same reaction types already named in this book.

### Carbon cycle

```
Photosynthesis:  6CO2 + 6H2O → C6H12O6 + 6O2       (carbon fixed into a molecule, by a plant)
Respiration:     C6H12O6 + 6O2 → 6CO2 + 6H2O       (the same equation, reversed, inside an animal)
Combustion:      hydrocarbon + O2 → CO2 + H2O       (Organic, Section I — the same reversal, industrial-speed)
```

Fossil fuel — the crude extract this whole chapter's Section II runs on — is carbon that photosynthesis fixed millions of years ago and combustion is only now returning. Burning petroleum isn't a new release of carbon into the world. It's an old withdrawal from a very slow bank, cashed out at a much faster rate than it was deposited.

### Nitrogen cycle

```
Fixation:        N2 + 3H2 → 2NH3        (Haber Process, Section II — industrial fixation)
                 N2 + O2 → 2NO           (lightning — natural fixation, same nitrogen, different energy source)
Nitrification:   NH3 → NO2⁻ → NO3⁻       (bacterial oxidation, soil-based)
Denitrification: NO3⁻ → N2               (bacterial reduction, returns nitrogen to the atmosphere)
```

The Haber Process was never an industrial invention of new chemistry — it's humans doing, in a pressurized vessel, what lightning and soil bacteria already do slowly and for free. The fertilizer that follows (Section II) just re-enters the same cycle at the nitrification step, one stage further along than a bacterium would have delivered it.

### Hydrogen and water cycle

```
Evaporation:    H2O (liquid) → H2O (gas)
Condensation:   H2O (gas) → H2O (liquid)
Electrolysis:   2H2O → 2H2 + O2            (industrial hydrogen source, alternative to natural gas)
```

Hydrogen doesn't really run its own independent cycle at this level — it rides inside the water cycle almost entirely, only breaking free industrially when electrolysis or steam-reforming natural gas splits it out on purpose for the Haber Process (Section II) to consume again. The natural solution pocket (Section III) and this cycle are the same water, read at two different speeds — evaporation and condensation over oceans, or a kettle boiling over a stove. It's the same sun and the same water this book opened on: a student standing on a beach was never outside this cycle, she was standing inside the exact process that's been described in equations for three pages.

Relationship one-liner: **every cycle in this section is a reaction this book already named, just missing the part where the product eventually turns back into the reactant.** Combustion, fixation, and electrolysis were never endpoints — they're one direction of an arrow that was always meant to run both ways.

---

## THE COMPLETE HIERARCHY, RESTATED

```
RAW MATERIAL STATE
   ↓
GATE → ORE (solid) / CRUDE EXTRACT (liquid-gas) / NATURAL SOLUTION (dissolved)
   ↓ (ore)                          ↓ (crude extract)                    ↓ (natural solution)
Activity Series decides         Cracking, Haber, Contact —           Electrolysis/precipitation on
extraction method                each one an existing reaction        what's already dissolved;
(Bonding & Periodicity VI)       type (addition, equilibrium,         hardness = solubility rules
                                 acid-base) run at industrial scale   (Compound Chemistry VIII)
   ↓                                    ↓                                    ↓
                    ENVIRONMENTAL RESIDUE — corrosion (Activity Series, reversed)
                    and acid rain (oxide gate, Compound Chemistry Section 0, involuntary)
```

Three extraction routes, four industrial processes, two environmental consequences — and not one new chemical idea among them. Every reaction in this chapter is a gate this book already opened, run once more at a scale large enough to show up on a factory floor or a rained-on rooftop instead of a test tube.
