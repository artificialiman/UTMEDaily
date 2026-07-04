# ATOM

Every other chapter in this book has been downstream of one equation. This chapter is where that equation actually lives.

```
atom     = proton + neutron + electron
nucleus  = proton + neutron              (this is the mass number)
element  = mass number + electron shells
electron = the currency of chemistry
```

Protons don't move. Neutrons don't react. Every reaction in Organic, Compound Chemistry, and Bonding & Periodicity was electrons changing hands — this chapter is where that currency is minted, and where the three routes an atom can take (isotope, ion, molecule) are shown properly instead of just named.

---

## I. SUBATOMIC PARTICLES — the constants underneath everything

| Particle | Relative mass | Relative charge | Actual mass (kg) | Location |
|---|---|---|---|---|
| Proton | 1 | +1 | 1.673 × 10⁻²⁷ | Nucleus |
| Neutron | 1 | 0 | 1.675 × 10⁻²⁷ | Nucleus |
| Electron | 1/1836 (effectively 0 for mass purposes) | −1 | 9.109 × 10⁻³¹ | Shells, around the nucleus |

Relationship one-liner: **an electron weighs almost nothing next to a proton or neutron — which is exactly why mass number only counts protons and neutrons, and why every mass calculation in this book has been safe to ignore electrons entirely. The currency of chemistry was never the heavy part of the atom.**

---

## II. ATOMIC NOTATION

```
ᴬZX          A = mass number (protons + neutrons)
             Z = atomic number (protons only — this is what makes the element what it is)
             X = element symbol
```

```
number of neutrons = mass number − atomic number
number of electrons (neutral atom) = number of protons
```

An atom is only neutral because it carries equal protons and electrons — the moment that balance breaks, you've already crossed into the ion route below.

---

## III. THE GATE — isotope, ion, molecule

```
GATE → What varies from the standard neutral atom?
   Neutron count varies, proton count fixed   → Isotope
   Electron count varies, proton count fixed   → Ion
   Nothing varies, atoms simply combine        → Molecule
```

An atom has to clear this gate before anything else about it can be classified — this is the same upstream-decides-downstream logic Compound Chemistry's oxide gate and Bonding & Periodicity's bonding gate both inherited from here.

### Isotope route

Same element, same atomic number, different mass number — same proton count, different neutron count. Chlorine exists in nature as roughly 75% Cl-35 and 25% Cl-37, which is exactly why chlorine's relative atomic mass (35.5) isn't a whole number — it's a weighted average, not a measurement of any single atom.

```
Relative atomic mass = Σ (isotope mass × % abundance) / 100
Chlorine: (35 × 75) + (37 × 25) / 100 = (2625 + 925) / 100 = 35.5
```

This single calculation is the reason periodic table masses are decimals at all — it was never sloppy measurement, it was isotopes voting in proportion to how common they are. Nuclear Chemistry's entire subject is what happens when this route goes unstable rather than sitting quietly as a natural abundance ratio.

### Ion route

```
ion = mass number − (electrons/shell)          (Book 3's original notation for the electron deficit or surplus)
cation = lost electrons, net positive           (metals — low ionization energy, Bonding & Periodicity I)
anion  = gained electrons, net negative         (nonmetals — high electronegativity, Bonding & Periodicity II)
```

| Atom | Electron configuration | Ion formed | Ion configuration |
|---|---|---|---|
| Na (11 electrons) | 2, 8, 1 | Na⁺ | 2, 8 |
| Cl (17 electrons) | 2, 8, 7 | Cl⁻ | 2, 8, 8 |
| Mg (12 electrons) | 2, 8, 2 | Mg²⁺ | 2, 8 |
| O (8 electrons) | 2, 6 | O²⁻ | 2, 8 |

Every ion on this table is chasing the same destination: a full outer shell, 8 electrons (2 for the first shell only). Sodium doesn't lose one electron by accident — it loses exactly enough to expose an already-full shell underneath. Chlorine doesn't gain seven electrons, it gains exactly one, because one is all that's missing from a full outer shell. This is the octet rule, and it's the actual mechanism behind Bonding & Periodicity's electronegativity-difference gate — atoms aren't bonding at random, every single one of them is chasing the same full-shell destination by whichever route (losing, gaining, or sharing) gets there.

### Molecule route

```
molecule = atom + atom
```

Where isotope and ion both change something about a single atom's internal count, molecule changes nothing about any individual atom — it's atoms achieving the same full-outer-shell destination by sharing instead of transferring, which is precisely the covalent side of Bonding & Periodicity's Section 0 gate. Two chlorine atoms, each one electron short of a full shell, share a pair between them and both count it toward their own total — Cl2, satisfied twice over from one shared pair.

---

## IV. ELECTRON ARRANGEMENT — the shell-filling rule underneath the whole gate

```
Shell 1: holds up to 2
Shell 2: holds up to 8
Shell 3: holds up to 8 (up to 18 for heavier elements, but 8 is the working rule at this level)
Fill innermost shell first, always
```

| Element | Protons | Electron arrangement | Valence electrons (outermost shell) |
|---|---|---|---|
| Hydrogen | 1 | 1 | 1 |
| Carbon | 6 | 2, 4 | 4 |
| Oxygen | 8 | 2, 6 | 6 |
| Sodium | 11 | 2, 8, 1 | 1 |
| Chlorine | 17 | 2, 8, 7 | 7 |
| Argon | 18 | 2, 8, 8 | 8 (already full — this is why noble gases don't react) |

Valence electron count is not a separate fact from the Periodic Table's group number — it's the same number, read from two directions. Group number gives you valence electrons directly for main-group elements; electron arrangement gives you the same number by counting up from the nucleus. Bonding & Periodicity's entire Section I trends table (atomic radius, ionization energy, electronegativity) is downstream of nothing more than how many shells an atom has and how full the outer one is — which means Bonding & Periodicity was never a separate chapter from this one. It's this chapter's electron arrangement, read as a horizontal and vertical trend instead of a per-element table.

---

## THE COMPLETE HIERARCHY, RESTATED

```
SUBATOMIC PARTICLES (proton, neutron, electron — the constants everything else is built from)
   ↓
ATOMIC NOTATION (mass number, atomic number — the bookkeeping)
   ↓
GATE → ISOTOPE / ION / MOLECULE
   ↓ (isotope)              ↓ (ion)                        ↓ (molecule)
relative atomic mass    octet rule, cation/anion,      shared electron pairs,
as weighted average      Bonding & Periodicity's         Bonding & Periodicity's
(→ Nuclear Chemistry     bonding gate (electron-          covalent gate
 if unstable)            transfer side)                   (→ Organic, Compound
                                                            Chemistry, everything
                                                            built from molecules)
   ↓
ELECTRON ARRANGEMENT (shell-filling — the mechanism behind every trend in
                       Bonding & Periodicity's Periodic Table section)
```

Every chapter in this book after this one was already written before this one was — Organic, Compound Chemistry, Bonding & Periodicity, Metallurgy, Physical Chemistry, Nuclear Chemistry. None of them needed correcting. They were all correctly derived from this equation without it ever being formally shown first. This chapter isn't the beginning because the book was written in this order — it's the beginning because everything else was already secretly obeying it.
