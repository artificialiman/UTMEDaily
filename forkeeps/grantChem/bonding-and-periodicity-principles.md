# BONDING & PERIODICITY

Four instruments run underneath everything in this book, and this chapter is where they're formally introduced together for the first time: the **Periodic Table**, the **Activity Series**, the **Electronegativity Scale**, and the **pH Scale**. Every gate you've read in Atom, Organic, and Compound Chemistry was quietly borrowing from one of these four. This chapter hands you the instruments themselves.

---

## 0. THE BONDING GATE — decided by one number

Before an atom picks isotope, ion, or molecule (Book 3's opening gate), something even earlier decides *how* two atoms will combine at all — and that decision is made by electronegativity difference, not by guesswork.

```
GATE → Electronegativity difference (ΔEN) between the two atoms
   ΔEN > 1.7      → Ionic bond    (electron transferred, not shared)
   0.4 < ΔEN < 1.7 → Polar covalent (shared unequally)
   ΔEN < 0.4      → Nonpolar covalent (shared equally)
   Metal + Metal   → Metallic bond (electrons delocalized, not owned by either atom)
```

One number, four outcomes. Nothing about bonding is arbitrary — it's arithmetic on a scale you're about to be handed.

---

## I. THE PERIODIC TABLE — instrument one

### The Gate

```
GATE → Period (horizontal row: same number of electron shells) / Group (vertical column: same number of valence electrons)
```

| Direction | What stays constant | What changes |
|---|---|---|
| Across a period (left → right) | Number of shells | Nuclear charge increases, atomic radius shrinks, electronegativity rises |
| Down a group (top → bottom) | Number of valence electrons | Number of shells increases, atomic radius grows, electronegativity falls |

### Trends, as constants you can look up rather than derive

| Property | Trend across a period | Trend down a group | Why |
|---|---|---|---|
| Atomic radius | Decreases | Increases | More protons pull the same-shell electrons in tighter; more shells push outward |
| Ionization energy | Increases | Decreases | Tighter grip = harder to remove an electron; more shells = outer electron is farther from the pull |
| Electronegativity | Increases | Decreases | Same tighter-grip logic, now applied to an electron it doesn't even own yet |
| Metallic character | Decreases | Increases | Metallic character is just "how easily it gives an electron away" — the mirror of ionization energy |

Relationship one-liner: **every trend on this table is the same nuclear-charge-versus-shell-count tug of war, read four different ways.** You are not memorizing four separate trends. You are memorizing one tug of war and reading its scoreboard four times.

---

## II. THE ELECTRONEGATIVITY SCALE — instrument two

Pauling's scale runs roughly 0.7 (francium, barely holds onto anything) to 4.0 (fluorine, holds onto everything, including electrons that aren't technically its own).

| Element | Electronegativity (Pauling) |
|---|---|
| Fluorine | 4.0 |
| Oxygen | 3.5 |
| Chlorine | 3.0 |
| Nitrogen | 3.0 |
| Carbon | 2.5 |
| Hydrogen | 2.1 |
| Sodium | 0.9 |
| Francium | 0.7 |

This single table is what Section 0's bonding gate actually runs on. Na (0.9) + Cl (3.0) gives ΔEN = 2.1 → ionic, which is exactly why NaCl behaves the way Compound Chemistry describes salts behaving (giant lattice, high melting point, conducts molten or dissolved). C (2.5) + H (2.1) gives ΔEN = 0.4 → borderline nonpolar covalent, which is exactly why every hydrocarbon in Organic is nonpolar and insoluble in water.

**The scale isn't background information for this chapter. It's the number every other chapter's chemistry was already running on.**

---

## III. IONIC BONDING — electron transfer

```
Na → Na+ + e⁻          (loses an electron, becomes a cation)
Cl + e⁻ → Cl⁻           (gains an electron, becomes an anion)
Na+ + Cl⁻ → NaCl        (electrostatic attraction, giant lattice)
```

| Property of ionic compounds | Why |
|---|---|
| High melting/boiling point | Strong electrostatic attraction throughout the whole lattice, not just between one pair |
| Conducts electricity molten or dissolved, not solid | Ions need to be free to move; locked in a solid lattice, they can't |
| Brittle | A shove misaligns the lattice, bringing like charges next to like charges, which repel and shatter the structure |

---

## IV. METALLIC BONDING — the sea of electrons

```
Metal atoms → positive ion cores + delocalized (shared, unowned) electrons
```

No single electron belongs to any one atom — they move freely through the whole structure, which is the direct cause of every "obvious" metal property:

| Property | Caused by |
|---|---|
| Conducts electricity (solid or molten) | Delocalized electrons are already free to move — no melting or dissolving required |
| Malleable and ductile | Ion cores can slide past each other without breaking a specific bond — the sea of electrons holds them together regardless of position |
| Lustrous | Free electrons absorb and re-emit light at the surface |

This is also the missing half of Compound Chemistry's alloy explanation: an alloy jams different-sized ion cores into that same sea, and the sliding that normally allows malleability gets physically obstructed — same electron sea, blocked movement, harder metal.

---

## V. INTERMOLECULAR FORCES — the weak grip between covalent molecules

Covalent bonds hold atoms together *inside* a molecule. Something else — much weaker — holds separate molecules to each other, and that "something else" is the real reason Organic's boiling-point table behaves the way it does.

| Force | Strength (weakest to strongest) | Present in |
|---|---|---|
| Van der Waals (induced dipole) | Weakest | All molecules — the only force in nonpolar hydrocarbons |
| Dipole-dipole | Medium | Polar molecules (unequal electronegativity, ΔEN between 0.4–1.7) |
| Hydrogen bonding | Strongest intermolecular force | O–H, N–H, F–H — water, alcohols, ammonia |

Relationship one-liner: **hydrocarbon boiling points rise with chain length (Organic, Section I) because longer chains have more surface area for Van der Waals grip — it was never about the C-C bonds themselves, which never break during boiling. Boiling breaks the grip between molecules, not the bonds within them.** Water's unusually high boiling point for its tiny size is hydrogen bonding doing exactly the same job, just with a much stronger grip.

---

## VI. THE ACTIVITY SERIES — instrument three

A ranked list of metals by how readily they give up electrons — which means it's really just ionization energy (Section I) turned into a practical, memorizable order.

```
K > Na > Ca > Mg > Al > Zn > Fe > Pb > (H) > Cu > Ag > Au
(Potassium, Sodium, Calcium, Magnesium, Aluminum, Zinc, Iron, Lead, Hydrogen, Copper, Silver, Gold)
```

### What the series predicts, as an operation

```
displacement reaction: A + BC → AC + B      (only happens if A is ABOVE B on the series)
```

| Reaction | Happens? | Why |
|---|---|---|
| Zn + CuSO4 → ZnSO4 + Cu | Yes | Zn sits above Cu — Zn gives up electrons more readily |
| Cu + ZnSO4 → no reaction | No | Cu sits below Zn — can't take the position from a metal more willing to hold on |

Hydrogen's placement mid-series isn't decorative — it's the exact line predicting which metals react with dilute acid to release H2 gas (everything above hydrogen does; everything below it doesn't, which is why copper never fizzes in dilute HCl no matter how long you wait).

The series is also the extraction difficulty table in disguise: metals above carbon can't be extracted by carbon reduction (too reactive, need electrolysis instead — sodium, aluminum); metals below carbon can be reduced by carbon directly in a blast furnace (iron). One ranking, two completely different practical consequences.

---

## VII. THE pH SCALE — instrument four

Already used throughout Compound Chemistry without being formally introduced. Here it is, in full:

```
0 ―――――――――――――― 7 ―――――――――――――― 14
STRONG ACID    WEAK ACID   NEUTRAL   WEAK BASE    STRONG BASE
```

| pH range | Character | Example |
|---|---|---|
| 0–2 | Strong acid | HCl, H2SO4 (concentrated) |
| 3–6 | Weak acid | Vinegar (~2.5), black coffee (~5) |
| 7 | Neutral | Pure water |
| 8–11 | Weak base | Baking soda solution (~9) |
| 12–14 | Strong base | NaOH, KOH |

pH is a logarithmic scale, not a linear one — a jump from pH 3 to pH 2 is a tenfold increase in H+ concentration, not a small step. This is the constant underneath every hydrolysis prediction Compound Chemistry's Section V made: "acidic" or "basic" was never a vague description, it was always a position on this exact number line, and the strong-acid-weak-base / weak-acid-strong-base predictions in that table are just predicting which side of 7 the resulting salt's number lands on.

pH only measures what's still dissolved, though — it says nothing about what came *out* of the reaction as a separate substance. Compound Chemistry's Salt Scale (Section III) runs perpendicular to this one, straight through the neutral axis at 7, ranking salts from mineral precipitate at the bottom to ester at the top. Two axes, one crossing point, two different questions about the same reaction.

---

## THE FOUR INSTRUMENTS, TOGETHER

| Instrument | What it ranks | What it predicts |
|---|---|---|
| Periodic Table | Atomic radius, ionization energy, electronegativity, metallic character — all by position | Which bonding gate an element will walk through |
| Electronegativity Scale | How strongly an atom holds electrons | Ionic vs covalent, polar vs nonpolar, the exact ΔEN cutoff |
| Activity Series | How readily a metal gives up electrons | Displacement reactions, acid reactivity, extraction method |
| pH Scale | H+ concentration, logarithmically | Acid/base strength, hydrolysis outcome, correct indicator choice |

None of these four are separate tools you consult independently. The Periodic Table generates the Electronegativity Scale's values. The Electronegativity Scale predicts where a metal sits on the Activity Series. The Activity Series predicts which acid reactions release hydrogen at all — the reactions the pH Scale then measures the aftermath of. Four instruments, one chain, each one built on the number the last one produced.
