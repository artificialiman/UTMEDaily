#!/usr/bin/env python3
"""
build.py — GrantApp AI UTME Quiz Generator
Fisher-Yates shuffle done HERE in Python at build time.
JS has NOTHING to do with question loading or option shuffling.
All routing via plain href links. Zero JS routing.
"""

import random
import os
import re as _re
from copy import deepcopy

# ──────────────────────────────────────────────────────────────
# QUESTION DATA
# ──────────────────────────────────────────────────────────────

RAW_QUESTIONS = {

"Mathematics": [
  {"text":"If 0.000456 is written in standard form as 4.56 × 10ⁿ, what is n?","options":{"A":"-4","B":"-3","C":"-2","D":"3"},"answer":"A","explanation":"Move decimal right for negative powers. 0.000456 = 4.56 × 10⁻⁴","exception":"The count starts AFTER the first non-zero digit."},
  {"text":"Simplify: (√2 + √3)(√2 − √3)","options":{"A":"-1","B":"1","C":"5","D":"√6"},"answer":"A","explanation":"Difference of squares: (a+b)(a−b) = a² − b². Result = 2 − 3 = −1.","exception":"Students expect positive result when both surds are positive."},
  {"text":"If log₁₀ 2 = 0.3010, find log₁₀ 0.02","options":{"A":"-1.699","B":"-0.699","C":"0.699","D":"1.699"},"answer":"A","explanation":"log(0.02) = log(2 × 10⁻²) = 0.3010 − 2 = −1.699.","exception":"Logarithms of numbers < 1 are NEGATIVE, not undefined."},
  {"text":"What is the remainder when 2x³ + 3x² − 5x + 7 is divided by (x + 2)?","options":{"A":"-11","B":"3","C":"11","D":"21"},"answer":"D","explanation":"Remainder theorem: f(−2) = −16 + 12 + 10 + 7 = 21.","exception":"Use x = −2, not +2, because divisor is (x + 2)."},
  {"text":"Solve: |2x − 3| = 5","options":{"A":"x = −1 or x = 4","B":"x = 1 or x = 4","C":"x = −1 only","D":"x = 4 only"},"answer":"A","explanation":"|a| = b gives a = ±b. So 2x − 3 = 5 OR 2x − 3 = −5, giving x = 4 or x = −1.","exception":"TWO solutions exist, not one."},
  {"text":"If sin θ = 3/5 and θ is acute, find cos θ","options":{"A":"3/5","B":"4/5","C":"5/3","D":"5/4"},"answer":"B","explanation":"cos θ = √(1 − sin²θ) = √(1 − 9/25) = √(16/25) = 4/5.","exception":"cos θ is positive ONLY because θ is acute."},
  {"text":"Find the nth term of: 3, 7, 11, 15 ...","options":{"A":"3n + 1","B":"4n − 1","C":"4n + 1","D":"3n + 4"},"answer":"B","explanation":"AP: Tₙ = a + (n−1)d = 3 + 4(n−1) = 4n − 1.","exception":"Verify: when n = 1, 4(1) − 1 = 3 ✓"},
  {"text":"Evaluate: ∛(−27)","options":{"A":"−3","B":"3","C":"Undefined","D":"±3"},"answer":"A","explanation":"Cube roots of negative numbers ARE defined. ∛(−27) = −3.","exception":"Odd roots preserve sign; only even roots require non-negative radicands."},
  {"text":"If 3ˣ = 27ˣ⁻², find x","options":{"A":"2","B":"3","C":"4","D":"6"},"answer":"B","explanation":"3ˣ = (3³)ˣ⁻² = 3³ˣ⁻⁶. Equate: x = 3x − 6, so x = 3.","exception":"This only works because bases are equal."},
  {"text":"A binary operation * is defined by a * b = a² − b². Calculate 3 * 2","options":{"A":"1","B":"5","C":"13","D":"25"},"answer":"B","explanation":"3 * 2 = 3² − 2² = 9 − 4 = 5.","exception":"* here does not mean multiplication."},
  {"text":"Find the inverse of f(x) = (2x + 1)/(x − 3)","options":{"A":"(3x + 1)/(x − 2)","B":"(3x − 1)/(x − 2)","C":"(x − 3)/(2x + 1)","D":"(2x − 1)/(x + 3)"},"answer":"A","explanation":"Swap x and y, solve for y: f⁻¹(x) = (3x + 1)/(x − 2).","exception":"Domain excludes x = 2 (division by zero)."},
  {"text":"How many diagonals does a regular hexagon have?","options":{"A":"6","B":"9","C":"12","D":"15"},"answer":"B","explanation":"Formula: n(n−3)/2. For n=6: 6(3)/2 = 9.","exception":"Total line segments = n(n−1)/2 = 15; diagonals exclude the 6 sides."},
  {"text":"If P = {1,2,3} and Q = {2,3,4}, find n(P ∪ Q)","options":{"A":"2","B":"3","C":"4","D":"6"},"answer":"C","explanation":"P ∪ Q = {1,2,3,4}, n = 4. Using formula: 3 + 3 − 2 = 4.","exception":"Don't count repeated elements."},
  {"text":"Differentiate y = x³ − 3x² + 2 with respect to x","options":{"A":"3x² − 3x","B":"3x² − 6x","C":"x² − 6x","D":"3x³ − 6x²"},"answer":"B","explanation":"Power rule: dy/dx = 3x² − 6x.","exception":"Constant term (2) disappears; derivative of constant = 0."},
  {"text":"Convert 234₅ to base 10","options":{"A":"54","B":"64","C":"69","D":"119"},"answer":"C","explanation":"2(25) + 3(5) + 4(1) = 50 + 15 + 4 = 69.","exception":"In base 5, digits must be 0–4; a digit ≥5 is invalid."},
  {"text":"Find the median of: 2, 8, 6, 4, 10","options":{"A":"4","B":"6","C":"8","D":"10"},"answer":"B","explanation":"Order: 2, 4, 6, 8, 10. Middle value = 6.","exception":"For even count, median = average of two middle values."},
  {"text":"Simplify: (x² − 9)/(x² + 6x + 9)","options":{"A":"(x − 3)/(x + 3)","B":"(x + 3)/(x − 3)","C":"1","D":"(x − 3)/(x + 3)²"},"answer":"A","explanation":"Factor: (x−3)(x+3)/(x+3)² = (x−3)/(x+3).","exception":"x ≠ −3 (domain restriction)."},
  {"text":"A rectangle has length (x + 3) and width (x − 2). Find the area","options":{"A":"x² + x − 6","B":"x² − x − 6","C":"x² + 5x − 6","D":"x² − 6"},"answer":"A","explanation":"Area = (x+3)(x−2) = x² − 2x + 3x − 6 = x² + x − 6.","exception":"Expand fully; middle terms do not cancel."},
  {"text":"In a class of 40, 24 like Math, 16 like English, 8 like both. How many like neither?","options":{"A":"0","B":"4","C":"8","D":"12"},"answer":"C","explanation":"n(M∪E) = 24 + 16 − 8 = 32. Neither = 40 − 32 = 8.","exception":"Include/Exclusion principle is essential here."},
  {"text":"Find the sum of the first 10 terms of: 2 + 4 + 6 + 8 ...","options":{"A":"90","B":"100","C":"110","D":"120"},"answer":"C","explanation":"Sₙ = n/2(2a + (n−1)d) = 5(4+18) = 110."},
  {"text":"If the mean of 4, 7, x, 10, 9 is 8, find x","options":{"A":"8","B":"9","C":"10","D":"11"},"answer":"C","explanation":"Sum = 5 × 8 = 40. 4+7+x+10+9 = 30+x = 40, so x = 10."},
  {"text":"Factorize: 6x² + 7x − 3","options":{"A":"(2x + 3)(3x − 1)","B":"(3x − 1)(2x + 3)","C":"(2x − 1)(3x + 3)","D":"(6x − 1)(x + 3)"},"answer":"A","explanation":"Product = −18, sum = 7. 6x² + 9x − 2x − 3 = (3x−1)(2x+3)."},
  {"text":"Evaluate: ∫(3x² + 2x)dx","options":{"A":"x³ + x² + C","B":"6x + 2 + C","C":"x³ + x + C","D":"3x³ + 2x² + C"},"answer":"A","explanation":"∫xⁿ dx = xⁿ⁺¹/(n+1). ∫3x² = x³; ∫2x = x². Total: x³ + x² + C.","exception":"Always add constant C for indefinite integrals."},
  {"text":"A circle has equation x² + y² = 25. What is the radius?","options":{"A":"5","B":"10","C":"25","D":"√5"},"answer":"A","explanation":"Standard form x² + y² = r². r² = 25, so r = 5.","exception":"r = √25 = 5, not 25."},
  {"text":"If 4x − 3 ≤ 13, find the range of x","options":{"A":"x ≤ 4","B":"x ≥ 4","C":"x ≤ −4","D":"x ≥ −4"},"answer":"A","explanation":"4x ≤ 16, x ≤ 4.","exception":"Inequality sign only flips when dividing/multiplying by a negative number."},
  {"text":"Find the equation of a line with gradient 2 passing through (1, 3)","options":{"A":"y = 2x + 1","B":"y = 2x − 1","C":"y = 2x + 3","D":"y = x + 2"},"answer":"A","explanation":"y − y₁ = m(x − x₁): y − 3 = 2(x − 1), y = 2x + 1.","exception":"Substitute the given point, not the origin."},
  {"text":"How many ways can 5 students be arranged in a row?","options":{"A":"5","B":"20","C":"60","D":"120"},"answer":"D","explanation":"5! = 5 × 4 × 3 × 2 × 1 = 120.","exception":"Permutation (order matters) ≠ combination (order irrelevant)."},
  {"text":"A bag contains 3 red and 2 blue balls. A ball is drawn at random. P(red) =","options":{"A":"2/5","B":"3/5","C":"1/2","D":"3/2"},"answer":"B","explanation":"P(red) = 3/(3+2) = 3/5.","exception":"Probability must be between 0 and 1; 3/2 is impossible."},
  {"text":"The angles of a triangle are in ratio 1:2:3. Find the largest angle","options":{"A":"30°","B":"60°","C":"90°","D":"120°"},"answer":"C","explanation":"Sum = 180°. Parts: 1+2+3 = 6. Largest = (3/6) × 180 = 90°.","exception":"Sum of triangle angles is always 180°, not 360°."},
  {"text":"Calculate the volume of a cylinder with radius 7cm and height 10cm (π = 22/7)","options":{"A":"440 cm³","B":"1540 cm³","C":"220 cm³","D":"4400 cm³"},"answer":"B","explanation":"V = πr²h = (22/7) × 49 × 10 = 22 × 70 = 1540 cm³.","exception":"Use r², not r; a common error is computing πrh instead."},
  {"text":"If y varies directly as x and y = 12 when x = 4, find y when x = 7","options":{"A":"18","B":"21","C":"24","D":"28"},"answer":"B","explanation":"y = kx. k = 12/4 = 3. y = 3 × 7 = 21."},
  {"text":"Express 0.1̄ (0.111...) as a fraction","options":{"A":"1/9","B":"1/10","C":"1/11","D":"10/99"},"answer":"A","explanation":"Let x = 0.111... Then 10x = 1.111... Subtract: 9x = 1, x = 1/9.","exception":"0.1̄ ≠ 1/10. Only 0.1 (terminating) equals 1/10."},
  {"text":"Find the value of x in the equation 2^(x+1) = 32","options":{"A":"3","B":"4","C":"5","D":"6"},"answer":"B","explanation":"32 = 2⁵. So x+1 = 5, x = 4.","exception":"Express both sides as powers of the same base first."},
  {"text":"The gradient of a line perpendicular to y = 3x + 5 is","options":{"A":"3","B":"1/3","C":"−1/3","D":"−3"},"answer":"C","explanation":"Perpendicular gradient = −1/m = −1/3.","exception":"Product of perpendicular gradients = −1. Not the negative, but the negative reciprocal."},
  {"text":"Simplify: 2log 5 + log 4 − log 2","options":{"A":"log 25","B":"log 50","C":"log 48","D":"log 100"},"answer":"B","explanation":"2log5 = log25. log25 + log4 − log2 = log(25 × 4 / 2) = log(50).","exception":"log addition = multiplication; log subtraction = division of arguments."},
],

"Biology": [
  {"text":"The organelle responsible for protein synthesis in a cell is?","options":{"A":"Mitochondrion","B":"Ribosome","C":"Golgi apparatus","D":"Lysosome"},"answer":"B"},
  {"text":"Which of the following is not a characteristic of living things?","options":{"A":"Reproduction","B":"Growth","C":"Crystallization","D":"Respiration"},"answer":"C"},
  {"text":"In Mendelian genetics, the phenotypic ratio of a monohybrid cross is?","options":{"A":"1:2:1","B":"3:1","C":"9:3:3:1","D":"1:1"},"answer":"B"},
  {"text":"The process by which green plants manufacture their food is called?","options":{"A":"Respiration","B":"Photosynthesis","C":"Transpiration","D":"Translocation"},"answer":"B"},
  {"text":"Which blood vessel carries oxygenated blood from the lungs to the heart?","options":{"A":"Pulmonary artery","B":"Pulmonary vein","C":"Aorta","D":"Vena cava"},"answer":"B"},
  {"text":"The enzyme that breaks down starch to maltose is?","options":{"A":"Pepsin","B":"Lipase","C":"Amylase","D":"Trypsin"},"answer":"C"},
  {"text":"Heterozygous organisms have?","options":{"A":"Two identical alleles","B":"Two different alleles","C":"No alleles","D":"Multiple alleles"},"answer":"B"},
  {"text":"The part of the brain that controls balance and posture is the?","options":{"A":"Cerebrum","B":"Cerebellum","C":"Medulla oblongata","D":"Hypothalamus"},"answer":"B"},
  {"text":"Nitrogen fixation in leguminous plants is carried out by?","options":{"A":"Fungi","B":"Viruses","C":"Bacteria","D":"Algae"},"answer":"C"},
  {"text":"The male reproductive organ in a flower is the?","options":{"A":"Stigma","B":"Style","C":"Ovary","D":"Stamen"},"answer":"D"},
  {"text":"Which of the following is an excretory organ in humans?","options":{"A":"Heart","B":"Kidney","C":"Stomach","D":"Pancreas"},"answer":"B"},
  {"text":"The loss of water from plant leaves through stomata is called?","options":{"A":"Guttation","B":"Transpiration","C":"Translocation","D":"Osmosis"},"answer":"B"},
  {"text":"Sickle cell anaemia is caused by?","options":{"A":"Vitamin deficiency","B":"Bacterial infection","C":"Gene mutation","D":"Viral infection"},"answer":"C"},
  {"text":"The trophic level that contains the most energy in a food chain is?","options":{"A":"Primary consumers","B":"Secondary consumers","C":"Producers","D":"Decomposers"},"answer":"C"},
  {"text":"Which of the following hormones regulates blood sugar level?","options":{"A":"Insulin","B":"Thyroxine","C":"Adrenaline","D":"Testosterone"},"answer":"A"},
  {"text":"The vascular tissue that transports water in plants is?","options":{"A":"Phloem","B":"Xylem","C":"Cambium","D":"Epidermis"},"answer":"B"},
  {"text":"In humans, gaseous exchange occurs in the?","options":{"A":"Trachea","B":"Bronchi","C":"Alveoli","D":"Larynx"},"answer":"C"},
  {"text":"Which of the following is a parasitic relationship?","options":{"A":"Tick on cow","B":"Bee and flower","C":"Lichen","D":"Rhizobium and legume"},"answer":"A"},
  {"text":"The functional unit of the kidney is called?","options":{"A":"Neuron","B":"Nephron","C":"Axon","D":"Dendrite"},"answer":"B"},
  {"text":"Phototropism in plants is a response to?","options":{"A":"Light","B":"Water","C":"Gravity","D":"Touch"},"answer":"A"},
  {"text":"The liquid part of blood is called?","options":{"A":"Serum","B":"Plasma","C":"Lymph","D":"Hemoglobin"},"answer":"B"},
  {"text":"In which part of the alimentary canal does most digestion occur?","options":{"A":"Mouth","B":"Stomach","C":"Small intestine","D":"Large intestine"},"answer":"C"},
  {"text":"The process by which organisms of the same species compete for limited resources is called?","options":{"A":"Interspecific competition","B":"Intraspecific competition","C":"Predation","D":"Parasitism"},"answer":"B"},
  {"text":"Which of the following is a sex-linked character?","options":{"A":"Height","B":"Skin color","C":"Hemophilia","D":"Body weight"},"answer":"C"},
  {"text":"The theory of evolution by natural selection was proposed by?","options":{"A":"Gregor Mendel","B":"Charles Darwin","C":"Louis Pasteur","D":"Robert Hooke"},"answer":"B"},
  {"text":"Vegetative propagation in plants involves?","options":{"A":"Seeds","B":"Spores","C":"Roots, stems or leaves","D":"Pollen"},"answer":"C"},
  {"text":"Which vitamin is essential for blood clotting?","options":{"A":"Vitamin A","B":"Vitamin C","C":"Vitamin D","D":"Vitamin K"},"answer":"D"},
  {"text":"The chamber of the heart that pumps blood to the lungs is the?","options":{"A":"Left atrium","B":"Left ventricle","C":"Right atrium","D":"Right ventricle"},"answer":"D"},
  {"text":"In ecology, organisms that feed on dead organic matter are called?","options":{"A":"Producers","B":"Consumers","C":"Decomposers","D":"Parasites"},"answer":"C"},
  {"text":"The chromosome number in human somatic cells is?","options":{"A":"23","B":"46","C":"92","D":"12"},"answer":"B"},
  {"text":"Which of the following is a method of asexual reproduction?","options":{"A":"Binary fission","B":"Fertilization","C":"Pollination","D":"Conjugation"},"answer":"A"},
  {"text":"The green pigment in plants responsible for photosynthesis is?","options":{"A":"Carotene","B":"Xanthophyll","C":"Chlorophyll","D":"Anthocyanin"},"answer":"C"},
  {"text":"In Mendel's experiment, the trait expressed in the F1 generation is called?","options":{"A":"Recessive","B":"Dominant","C":"Codominant","D":"Intermediate"},"answer":"B"},
  {"text":"The enzyme pepsin functions in which pH range?","options":{"A":"Alkaline","B":"Neutral","C":"Acidic","D":"Any pH"},"answer":"C"},
  {"text":"Which of the following is an adaptation for flight in birds?","options":{"A":"Heavy bones","B":"Feathers","C":"Four legs","D":"Teeth"},"answer":"B"},
],

"Chemistry": [
  {"text":"An element X has atomic number 17 and mass number 35. The number of neutrons is:","options":{"A":"17","B":"18","C":"35","D":"52"},"answer":"B","explanation":"Neutrons = mass number - atomic number = 35 - 17 = 18.","exception":"Isotopes of same element have different neutron counts but same atomic number."},
  {"text":"Which electronic configuration violates Hund's rule?","options":{"A":"1s2 2s2 2p6","B":"1s2 2s2 2p4 (up-down up up)","C":"1s2 2s2 2p4 (up-down up-down up)","D":"1s2 2s2 2p3 (up up up)"},"answer":"C","explanation":"Hund's rule: electrons singly occupy orbitals before pairing. Option C pairs prematurely.","exception":"Maximum multiplicity (unpaired electrons) gives lowest energy."},
  {"text":"The ion with electronic configuration 1s2 2s2 2p6 could be:","options":{"A":"Na+ only","B":"F- only","C":"Both Na+ and F-","D":"Neither"},"answer":"C","explanation":"Both have 10 electrons (isoelectronic with Ne). Na loses 1e-, F gains 1e-.","exception":"Isoelectronic species have same electron count but different nuclear charges."},
  {"text":"Electronegativity increases across a period because:","options":{"A":"Nuclear charge increases, atomic radius decreases","B":"Shielding increases","C":"Atomic radius increases","D":"Ionization energy decreases"},"answer":"A","explanation":"More protons pull electrons stronger; smaller size means closer to nucleus.","exception":"Noble gases often excluded from electronegativity trends."},
  {"text":"Which statement about first ionization energies is correct?","options":{"A":"Mg > Na (IE increases across period)","B":"Na > Mg","C":"They are equal","D":"Cannot be determined"},"answer":"A","explanation":"IE generally increases across period. Mg > Na.","exception":"Actual exceptions: Al < Mg (subshell), O < N (pairing energy)."},
  {"text":"Noble gases are unreactive because:","options":{"A":"Full valence shell (stable octet)","B":"High electronegativity","C":"Large atomic radius","D":"Low ionization energy"},"answer":"A","explanation":"ns2np6 configuration is stable.","exception":"Xe and Kr CAN form compounds with highly electronegative F."},
  {"text":"The bond angle in water (104.5°) is less than methane (109.5°) because:","options":{"A":"Lone pairs repel more than bonding pairs","B":"Oxygen is more electronegative","C":"Hydrogen bonding","D":"Water is polar"},"answer":"A","explanation":"VSEPR: lone pair-lone pair > lone pair-bond > bond-bond repulsion.","exception":"NH3 (107°) also compressed from tetrahedral but less than H2O."},
  {"text":"Which molecule is nonpolar despite having polar bonds?","options":{"A":"CO2 (linear, symmetrical)","B":"H2O","C":"NH3","D":"HCl"},"answer":"A","explanation":"CO2: two C=O bonds cancel (linear geometry).","exception":"CCl4 also nonpolar (tetrahedral symmetry) despite polar C-Cl bonds."},
  {"text":"The hybridization of carbon in CO2 is:","options":{"A":"sp","B":"sp2","C":"sp3","D":"sp3d"},"answer":"A","explanation":"Linear geometry = sp hybridization (2 regions of electron density).","exception":"Same carbon can have different hybridizations: CH4 (sp3), C2H4 (sp2), C2H2 (sp)."},
  {"text":"Resonance structures of benzene show:","options":{"A":"Electrons are delocalized (not fixed double bonds)","B":"Molecule oscillates between structures","C":"Double bonds alternate rapidly","D":"Two different compounds exist"},"answer":"A","explanation":"Resonance = single structure with delocalized electrons, NOT equilibrium between forms."},
  {"text":"Hydrogen bonding is strongest between:","options":{"A":"F-H...F (most electronegative)","B":"O-H...O","C":"N-H...N","D":"C-H...O"},"answer":"A","explanation":"Strength: F-H > O-H > N-H (electronegativity trend).","exception":"O-H bonds in water are more biologically important despite F-H being stronger."},
  {"text":"The pH of 0.01 M HCl is:","options":{"A":"2","B":"1","C":"0.01","D":"12"},"answer":"A","explanation":"pH = -log[H+] = -log(10-2) = 2.","exception":"Very concentrated acids (>1M) can have negative pH."},
  {"text":"A buffer solution resists pH change because:","options":{"A":"Contains weak acid and its conjugate base","B":"Contains strong acid","C":"Is neutral","D":"Has high concentration"},"answer":"A","explanation":"Buffer: HA/A- pair. Absorbs added H+ or OH-.","exception":"Buffers only effective within ±1 pH unit of pKa."},
  {"text":"The pH at equivalence point in strong acid-strong base titration is:","options":{"A":"7","B":"Less than 7","C":"Greater than 7","D":"Depends on concentrations"},"answer":"A","explanation":"Neutral salt formed (NaCl from HCl + NaOH).","exception":"Weak acid-strong base gives pH >7; strong acid-weak base gives pH <7 at equivalence."},
  {"text":"At higher temperature, Kw (= [H+][OH-] = 10-14 at 25°C):","options":{"A":"Increases (ionization is endothermic)","B":"Decreases","C":"Stays constant","D":"Becomes zero"},"answer":"A","explanation":"Water ionization is endothermic; Le Chatelier predicts increase with temperature.","exception":"Neutral pH at 60°C is ~6.5 (not 7) because Kw increases."},
  {"text":"The oxidation number of Cr in K2Cr2O7 is:","options":{"A":"+6","B":"+7","C":"+12","D":"+14"},"answer":"A","explanation":"2(+1) + 2x + 7(-2) = 0, so x = +6.","exception":"Maximum oxidation state usually equals group number; Cr in Group 6 can reach +6."},
  {"text":"In the reaction 2Fe2+ → 2Fe3+ + 2e-, iron is:","options":{"A":"Oxidized (loses electrons)","B":"Reduced","C":"Oxidizing agent","D":"Unchanged"},"answer":"A","explanation":"Oxidation = loss of electrons (OIL RIG). Fe2+ is reducing agent."},
  {"text":"The standard hydrogen electrode is assigned:","options":{"A":"E° = 0.00 V (reference point)","B":"E° = 1.00 V","C":"E° = -1.00 V","D":"E° = +0.76 V"},"answer":"A","explanation":"SHE is reference; all other potentials measured relative to it."},
  {"text":"In galvanic cell, the anode is:","options":{"A":"Negative electrode (oxidation occurs)","B":"Positive electrode","C":"Where reduction occurs","D":"Made of copper"},"answer":"A","explanation":"Anode = oxidation = negative in galvanic cell.","exception":"In electrolytic cell, anode is POSITIVE (but still oxidation site)."},
  {"text":"Faraday's law: mass deposited is proportional to:","options":{"A":"Charge passed (Q = nF)","B":"Current only","C":"Voltage","D":"Resistance"},"answer":"A","explanation":"m is proportional to Q. Specifically: m = (Q × M)/(n × F).","exception":"Time matters through Q = It; doubling current OR doubling time doubles mass."},
  {"text":"Haber process produces ammonia at:","options":{"A":"High pressure, moderate temperature, Fe catalyst","B":"Low pressure, high temperature","C":"Room conditions","D":"High temperature only"},"answer":"A","explanation":"N2 + 3H2 = 2NH3 (exothermic). Le Chatelier: high P favors products.","exception":"Equilibrium position vs rate conflict requires optimization at ~450°C."},
  {"text":"In N2 + 3H2 = 2NH3, adding more N2:","options":{"A":"Shifts equilibrium right (more NH3)","B":"Shifts left","C":"No effect on equilibrium","D":"Stops reaction"},"answer":"A","explanation":"Le Chatelier: system counteracts change by consuming added N2.","exception":"Kp unchanged; only position shifts, not equilibrium constant."},
  {"text":"The equilibrium constant Kc for 2A = B is 4. For B = 2A, Kc is:","options":{"A":"0.25 (1/4)","B":"4","C":"16","D":"2"},"answer":"A","explanation":"Reversing reaction inverts K: K_reverse = 1/K_forward.","exception":"Multiplying equation by n raises K to power n."},
  {"text":"A reaction is spontaneous if:","options":{"A":"ΔG < 0","B":"ΔH < 0","C":"ΔS > 0","D":"All of the above always"},"answer":"A","explanation":"Gibbs: ΔG = ΔH - TΔS. Spontaneous when ΔG < 0.","exception":"Endothermic reactions CAN be spontaneous if ΔS is large and positive."},
  {"text":"Diamond is harder than graphite because:","options":{"A":"3D network of strong C-C bonds vs 2D layers","B":"Diamond has metallic bonding","C":"Graphite has ionic bonding","D":"Diamond has more electrons"},"answer":"A","explanation":"Diamond: sp3, tetrahedral. Graphite: sp2, layered with weak van der Waals between layers.","exception":"Graphite conducts electricity (delocalized electrons in layers); diamond doesn't."},
  {"text":"The melting point of NaCl (ionic) is higher than I2 (molecular) because:","options":{"A":"Ionic bonds stronger than van der Waals forces","B":"NaCl has more atoms","C":"I2 is covalent","D":"NaCl is soluble in water"},"answer":"A","explanation":"Ionic > covalent network > metallic > polar molecular > nonpolar molecular (general trend)."},
  {"text":"Transition metals show variable oxidation states because:","options":{"A":"d electrons participate in bonding","B":"They are large atoms","C":"They are metals","D":"They conduct electricity"},"answer":"A","explanation":"d electrons have similar energy to s electrons; can lose different numbers.","exception":"Scandium and zinc show mainly +3 and +2 respectively."},
  {"text":"Which is a Lewis acid?","options":{"A":"BF3 (electron deficient)","B":"NH3","C":"H2O","D":"OH-"},"answer":"A","explanation":"Lewis acid = electron pair acceptor. BF3 has empty orbital.","exception":"Broader than Bronsted (proton transfer); includes species without H+."},
  {"text":"The pH of 10-8 M HCl is approximately:","options":{"A":"7 (water ionization dominates)","B":"Exactly 8","C":"Exactly -8","D":"14"},"answer":"A","explanation":"At very low acid concentration, water's H+ (10-7 M) becomes significant.","exception":"Can't ignore water ionization when acid concentration < 10-6 M."},
  {"text":"Effusion rate of gas A is twice that of gas B. If M_A = 4, then M_B is:","options":{"A":"16","B":"8","C":"2","D":"1"},"answer":"A","explanation":"Graham's law: rate is proportional to 1/sqrt(M). 2 = sqrt(M_B/4), so M_B = 16."},
  {"text":"Real gases deviate from ideal behavior at:","options":{"A":"High pressure and low temperature","B":"Low pressure and high temperature","C":"All conditions equally","D":"Never deviate"},"answer":"A","explanation":"High P: volume of molecules matters. Low T: intermolecular forces matter."},
  {"text":"The van der Waals equation corrects ideal gas law for:","options":{"A":"Molecular volume (b) and intermolecular forces (a)","B":"Temperature only","C":"Pressure only","D":"Chemical reactions"},"answer":"A","explanation":"(P + a/V2)(V - b) = RT. a corrects pressure, b corrects volume."},
  {"text":"Charcoal adsorbs gases because:","options":{"A":"High surface area (porous structure)","B":"It is black","C":"It is solid","D":"It is carbon"},"answer":"A","explanation":"Adsorption (surface) vs absorption (volume). Activated charcoal has huge surface area."},
  {"text":"A catalyst increases reaction rate by:","options":{"A":"Lowering activation energy","B":"Increasing temperature","C":"Increasing concentration","D":"Shifting equilibrium"},"answer":"A","explanation":"Catalyst provides alternative pathway with lower Ea.","exception":"Catalyst doesn't change ΔH, ΔG, or equilibrium position."},
  {"text":"Rate = k[A]2[B]. If [A] doubles and [B] triples, rate:","options":{"A":"Increases 12x (2² × 3)","B":"Increases 6x","C":"Doubles","D":"Triples"},"answer":"A","explanation":"Rate_new = k(2[A])2(3[B]) = 4 × 3 × k[A]2[B] = 12 × Rate_old."},
],

"English": [
  {"text":"Choose the word that is OPPOSITE in meaning to \"ubiquitous\"","options":{"A":"Rare","B":"Common","C":"Frequent","D":"Universal"},"answer":"A","explanation":"Ubiquitous means present everywhere. Opposite = rare."},
  {"text":"Choose the option with the same vowel sound as the underlined letters in \"blood\"","options":{"A":"Flood","B":"Food","C":"Mood","D":"Good"},"answer":"A","explanation":"\"Blood\" /blud/ rhymes with \"flood\" /flud/, both have /u/ sound."},
  {"text":"In the sentence \"The committee has submitted its report,\" the verb \"has\" agrees with:","options":{"A":"Committee (singular collective noun)","B":"Members (implied plural)","C":"Report (object)","D":"Either A or B"},"answer":"A","explanation":"Collective nouns take singular verbs when acting as a unit.","exception":"British English often uses plural verbs for collectives."},
  {"text":"Identify the literary device: \"The classroom was a zoo\"","options":{"A":"Simile","B":"Metaphor","C":"Personification","D":"Hyperbole"},"answer":"B","explanation":"Direct comparison without like/as = metaphor."},
  {"text":"Which sentence uses \"lie\" correctly?","options":{"A":"I will lay down for a nap","B":"The book is laying on the table","C":"Yesterday, I lay down to rest","D":"The hen has laid five eggs"},"answer":"C","explanation":"Lie (recline) is intransitive: lie/lay/lain. Lay (put down) is transitive: lay/laid/laid."},
  {"text":"Choose the correctly punctuated sentence:","options":{"A":"The teacher said, \"homework is due tomorrow\".","B":"The teacher said, \"Homework is due tomorrow.\"","C":"The teacher said \"Homework is due tomorrow.\"","D":"The teacher said: \"homework is due tomorrow.\""},"answer":"B","explanation":"Comma before quote, capital letter starts quote, period inside closing quote."},
  {"text":"Identify the error: \"Neither the students nor the teacher were present\"","options":{"A":"Subject-verb disagreement","B":"Pronoun error","C":"Tense error","D":"No error"},"answer":"A","explanation":"With neither...nor, verb agrees with NEAREST subject. Teacher (singular) requires was."},
  {"text":"The prefix \"bi-\" in \"biannual\" means:","options":{"A":"Once every two years","B":"Twice a year","C":"Half a year","D":"Two years long"},"answer":"B","explanation":"Biannual = twice yearly.","exception":"Biennial = every two years. These are commonly confused."},
  {"text":"Choose the word with correct spelling:","options":{"A":"Occured","B":"Occurred","C":"Ocurred","D":"Occureed"},"answer":"B","explanation":"Double the final consonant before -ed when: stressed final syllable ends in CVC."},
  {"text":"In \"The faster you run, the sooner you'll arrive,\" the structure is:","options":{"A":"Comparative correlation","B":"Conditional clause","C":"Superlative comparison","D":"Parallel structure"},"answer":"A","explanation":"The + comparative...the + comparative shows correlation."},
  {"text":"Identify the sentence with correct pronoun usage:","options":{"A":"Between you and I, he's wrong","B":"He gave the gift to my wife and I","C":"The secret is between you and me","D":"Myself and John will attend"},"answer":"C","explanation":"After prepositions, use objective case (me/him/her)."},
  {"text":"The word \"sanction\" can mean:","options":{"A":"To approve OR to penalize","B":"Only to approve","C":"Only to penalize","D":"To ignore"},"answer":"A","explanation":"Sanction is an auto-antonym—means both approve AND punish."},
  {"text":"Which uses the subjunctive mood correctly?","options":{"A":"If I was rich, I'd travel","B":"I wish I was taller","C":"If he were here, he'd help","D":"She acts like she was the boss"},"answer":"C","explanation":"Subjunctive uses were for all persons in contrary-to-fact conditions."},
  {"text":"Identify the dangling modifier:","options":{"A":"Walking home, the rain started","B":"While walking home, I felt raindrops","C":"The rain started as I walked home","D":"I walked home in the rain"},"answer":"A","explanation":"Walking home illogically modifies rain (rain can't walk)."},
  {"text":"The word \"egregious\" originally meant \"remarkably good\" but now means \"remarkably bad.\" This is:","options":{"A":"Amelioration","B":"Pejoration","C":"Generalization","D":"Specialization"},"answer":"B","explanation":"Pejoration = word becomes more negative over time."},
  {"text":"In \"She is taller than I,\" the implied ending is:","options":{"A":"Than I am","B":"Than me","C":"Than I be","D":"Either A or B"},"answer":"A","explanation":"After than in formal writing, use subject case when verb is implied."},
  {"text":"Choose the sentence with correct parallel structure:","options":{"A":"She likes reading, to write, and painting","B":"She likes to read, writing, and to paint","C":"She likes reading, writing, and painting","D":"She likes to read, to write, and painting"},"answer":"C","explanation":"Parallel elements must have same grammatical form (all gerunds or all infinitives)."},
  {"text":"The phrase \"I could care less\" is:","options":{"A":"Correct and means indifference","B":"Incorrect; should be \"couldn't care less\"","C":"Regional variation, both acceptable","D":"Means extreme caring"},"answer":"B","explanation":"Logically, couldn't care less means zero care possible."},
  {"text":"Identify the oxymoron:","options":{"A":"Deafening silence","B":"Very unique","C":"Hot coffee","D":"Fast car"},"answer":"A","explanation":"Oxymoron combines contradictory terms. Silence can't be loud."},
  {"text":"In passive voice, the sentence \"The cat chased the mouse\" becomes:","options":{"A":"The mouse was chased by the cat","B":"The mouse is chased by the cat","C":"The cat was chasing the mouse","D":"The mouse has been chased"},"answer":"A","explanation":"Passive: object becomes subject, verb becomes be + past participle."},
  {"text":"The word \"literally\" is increasingly used to mean:","options":{"A":"Figuratively (opposite of original meaning)","B":"Only in literal sense","C":"Approximately","D":"Exactly"},"answer":"A","explanation":"Literally now often intensifies figurative statements."},
  {"text":"Choose the sentence with correct comma usage:","options":{"A":"The red, old, car broke down","B":"The old red car broke down","C":"The old, red car broke down","D":"The, old, red, car broke down"},"answer":"C","explanation":"Coordinate adjectives (interchangeable order) need commas."},
  {"text":"The error in \"Irregardless of the cost, we'll proceed\" is:","options":{"A":"\"Irregardless\" is non-standard","B":"Comma splice","C":"Wrong preposition","D":"No error"},"answer":"A","explanation":"Irregardless is double negative (ir- + -less). Standard form: regardless."},
  {"text":"In \"The data is conclusive,\" the subject-verb agreement is:","options":{"A":"Correct (modern usage)","B":"Incorrect; should be \"data are\"","C":"Regional variation","D":"Either acceptable"},"answer":"D","explanation":"Data is Latin plural of datum. Modern usage treats it as singular mass noun."},
  {"text":"Identify the malapropism: \"Texas has a large Portuguese population\"","options":{"A":"Portuguese (should be \"populace\")","B":"Large (wrong word)","C":"Texas (wrong place)","D":"No error"},"answer":"A","explanation":"Malapropism substitutes similar-sounding wrong word."},
  {"text":"The sentence \"Whom did you see?\" is:","options":{"A":"Formally correct","B":"Archaic and incorrect","C":"Missing auxiliary verb","D":"Conversationally wrong"},"answer":"A","explanation":"Whom is object case (direct object of see)."},
  {"text":"Choose the correct verb form: \"If I _____ known, I would have come\"","options":{"A":"have","B":"had","C":"would have","D":"has"},"answer":"B","explanation":"Past perfect in if clause pairs with would have in main clause (third conditional)."},
  {"text":"The phrase \"beg the question\" traditionally means:","options":{"A":"To raise a question","B":"To avoid answering","C":"To assume what you're trying to prove (circular reasoning)","D":"To ask formally"},"answer":"C","explanation":"Beg the question is logical fallacy (petitio principii)."},
  {"text":"In \"She is one of those teachers who inspire students,\" the verb \"inspire\" is:","options":{"A":"Correct (agrees with \"teachers\")","B":"Incorrect; should be \"inspires\"","C":"Either acceptable","D":"Subjunctive mood"},"answer":"A","explanation":"Who refers to teachers (plural antecedent), so inspire (plural verb)."},
  {"text":"Identify the split infinitive:","options":{"A":"To boldly go where no one has gone","B":"To go boldly where no one has gone","C":"Boldly to go where no one has gone","D":"Both B and C"},"answer":"A","explanation":"Adverb between to and verb = split infinitive."},
  {"text":"The word \"presently\" means:","options":{"A":"Currently OR soon","B":"Only currently","C":"Only soon","D":"In the past"},"answer":"A","explanation":"Presently means soon (traditional) OR now (American usage)."},
  {"text":"Choose the correct form: \"Neither of the answers _____ correct\"","options":{"A":"is","B":"are","C":"were","D":"be"},"answer":"A","explanation":"Neither is singular pronoun, takes singular verb."},
  {"text":"In \"The house was engulfed in flames,\" the phrase \"in flames\" functions as:","options":{"A":"Adverbial phrase","B":"Adjectival phrase","C":"Noun phrase","D":"Prepositional object"},"answer":"A","explanation":"In flames describes how/in what state house was engulfed (modifies verb)."},
  {"text":"The sentence \"We was ready to leave\" contains:","options":{"A":"Dialect grammar (nonstandard but systematic)","B":"Random error","C":"Code-switching","D":"Correct grammar"},"answer":"A","explanation":"We was appears in some English dialects."},
  {"text":"Identify the zeugma: \"She broke his car and his heart\"","options":{"A":"\"Broke\" applies literally and figuratively","B":"Parallel structure","C":"Metaphor only","D":"No rhetorical device"},"answer":"A","explanation":"Zeugma uses one word in two senses simultaneously."},
],

"Government": [
  {"text":"A system of government where power is concentrated in the hands of one person is called?","options":{"A":"Democracy","B":"Oligarchy","C":"Autocracy","D":"Aristocracy"},"answer":"C"},
  {"text":"The fundamental law of a country is called the?","options":{"A":"Constitution","B":"Decree","C":"Act","D":"Statute"},"answer":"A"},
  {"text":"The principle of separation of powers was proposed by?","options":{"A":"John Locke","B":"Baron de Montesquieu","C":"Jean Jacques Rousseau","D":"Thomas Hobbes"},"answer":"B"},
  {"text":"In a federal system of government, powers are shared between?","options":{"A":"The president and legislature","B":"Central and regional governments","C":"Military and civilians","D":"Political parties"},"answer":"B"},
  {"text":"The right to vote in an election is called?","options":{"A":"Franchise","B":"Referendum","C":"Plebiscite","D":"Initiative"},"answer":"A"},
  {"text":"Which organ of government interprets laws?","options":{"A":"Executive","B":"Legislature","C":"Judiciary","D":"Civil service"},"answer":"C"},
  {"text":"A government elected by the people is called?","options":{"A":"Monarchy","B":"Theocracy","C":"Democracy","D":"Plutocracy"},"answer":"C"},
  {"text":"The Nigeria independence was achieved in?","options":{"A":"1959","B":"1960","C":"1963","D":"1966"},"answer":"B"},
  {"text":"The concept of checks and balances prevents?","options":{"A":"Abuse of power","B":"Democracy","C":"Rule of law","D":"Separation of powers"},"answer":"A"},
  {"text":"A system where citizens vote directly on laws is called?","options":{"A":"Representative democracy","B":"Direct democracy","C":"Presidential democracy","D":"Parliamentary democracy"},"answer":"B"},
  {"text":"The head of state in a parliamentary system is usually?","options":{"A":"The prime minister","B":"The president","C":"The monarch or president","D":"The speaker"},"answer":"C"},
  {"text":"Public opinion is best expressed through?","options":{"A":"The military","B":"Mass media","C":"The police","D":"Civil servants"},"answer":"B"},
  {"text":"A law made by the legislature is called?","options":{"A":"Decree","B":"Edict","C":"Act","D":"Order"},"answer":"C"},
  {"text":"The process of a bill becoming a law involves?","options":{"A":"First reading only","B":"Presidential assent only","C":"Three readings and assent","D":"Second reading only"},"answer":"C"},
  {"text":"Which of the following is a feature of democracy?","options":{"A":"One-party system","B":"Free and fair elections","C":"Military rule","D":"Dictatorship"},"answer":"B"},
  {"text":"The two-party system is practiced in?","options":{"A":"Nigeria","B":"United States","C":"China","D":"Russia"},"answer":"B"},
  {"text":"The Nigerian constitution is regarded as supreme because?","options":{"A":"It is written","B":"It is rigid","C":"All laws must conform to it","D":"It is federal"},"answer":"C"},
  {"text":"Local government is the?","options":{"A":"First tier of government","B":"Second tier of government","C":"Third tier of government","D":"Fourth tier of government"},"answer":"C"},
  {"text":"The process of removing a president from office is called?","options":{"A":"Impeachment","B":"Recall","C":"Dissolution","D":"Suspension"},"answer":"A"},
  {"text":"Universal adult suffrage means?","options":{"A":"Only men can vote","B":"Only women can vote","C":"All qualified adults can vote","D":"Only educated people can vote"},"answer":"C"},
  {"text":"In Nigeria, citizenship can be acquired by?","options":{"A":"Birth only","B":"Registration only","C":"Birth, registration or naturalization","D":"Marriage only"},"answer":"C"},
  {"text":"The principle that no one is above the law is called?","options":{"A":"Separation of powers","B":"Rule of law","C":"Checks and balances","D":"Judicial review"},"answer":"B"},
  {"text":"A political party that wins election and forms government is called?","options":{"A":"Opposition party","B":"Ruling party","C":"Minority party","D":"Coalition party"},"answer":"B"},
  {"text":"The first executive president of Nigeria was?","options":{"A":"Nnamdi Azikiwe","B":"Tafawa Balewa","C":"Shehu Shagari","D":"Olusegun Obasanjo"},"answer":"C"},
  {"text":"Proportional representation is a system of?","options":{"A":"Government","B":"Electoral system","C":"Checks and balances","D":"Separation of powers"},"answer":"B"},
  {"text":"Delegated legislation is made by?","options":{"A":"The legislature","B":"The executive","C":"The judiciary","D":"Political parties"},"answer":"B"},
  {"text":"A referendum is used to?","options":{"A":"Elect leaders","B":"Approve or reject a proposal","C":"Impeach leaders","D":"Form government"},"answer":"B"},
  {"text":"The civil service is part of the?","options":{"A":"Legislature","B":"Judiciary","C":"Executive","D":"Electoral body"},"answer":"C"},
  {"text":"A bi-cameral legislature has?","options":{"A":"One house","B":"Two houses","C":"Three houses","D":"Four houses"},"answer":"B"},
  {"text":"The Clifford constitution introduced?","options":{"A":"Elective principle","B":"Federal system","C":"Independence","D":"Republic"},"answer":"A"},
  {"text":"Public corporations are established to?","options":{"A":"Make profits only","B":"Provide essential services","C":"Compete with private sector","D":"Employ civil servants"},"answer":"B"},
  {"text":"The supreme law-making body in Nigeria is?","options":{"A":"The Supreme Court","B":"The President","C":"The National Assembly","D":"State Assembly"},"answer":"C"},
  {"text":"Political socialization is the process of?","options":{"A":"Forming political parties","B":"Learning political values","C":"Voting in elections","D":"Governing a state"},"answer":"B"},
  {"text":"The first military coup in Nigeria occurred in?","options":{"A":"1960","B":"1963","C":"1966","D":"1967"},"answer":"C"},
  {"text":"Fundamental human rights are entrenched in the?","options":{"A":"Criminal code","B":"Constitution","C":"Electoral act","D":"Civil service rules"},"answer":"B"},
],

"Literature": [
  {"text":"A story passed down orally from generation to generation is called?","options":{"A":"Legend","B":"Myth","C":"Folklore","D":"Epic"},"answer":"C"},
  {"text":"The use of exaggeration for emphasis in literature is called?","options":{"A":"Metaphor","B":"Simile","C":"Hyperbole","D":"Personification"},"answer":"C"},
  {"text":"A play written to be performed is called?","options":{"A":"Prose","B":"Drama","C":"Poetry","D":"Novel"},"answer":"B"},
  {"text":"The main character in a literary work is called the?","options":{"A":"Antagonist","B":"Protagonist","C":"Narrator","D":"Author"},"answer":"B"},
  {"text":"Which of the following wrote \"Things Fall Apart\"?","options":{"A":"Wole Soyinka","B":"Chinua Achebe","C":"Ngugi wa Thiong'o","D":"Amos Tutuola"},"answer":"B"},
  {"text":"A figure of speech that makes a comparison using \"like\" or \"as\" is?","options":{"A":"Metaphor","B":"Simile","C":"Alliteration","D":"Onomatopoeia"},"answer":"B"},
  {"text":"The repetition of initial consonant sounds in a line of poetry is called?","options":{"A":"Assonance","B":"Consonance","C":"Alliteration","D":"Rhyme"},"answer":"C"},
  {"text":"A poem of fourteen lines is called a?","options":{"A":"Ballad","B":"Sonnet","C":"Ode","D":"Elegy"},"answer":"B"},
  {"text":"The atmosphere or feeling created in a literary work is called?","options":{"A":"Theme","B":"Mood","C":"Tone","D":"Setting"},"answer":"B"},
  {"text":"In drama, words spoken by a character that other characters cannot hear are called?","options":{"A":"Monologue","B":"Dialogue","C":"Soliloquy","D":"Aside"},"answer":"D"},
  {"text":"The central idea or message of a literary work is the?","options":{"A":"Plot","B":"Theme","C":"Setting","D":"Conflict"},"answer":"B"},
  {"text":"Who wrote \"The Lion and the Jewel\"?","options":{"A":"Chinua Achebe","B":"Wole Soyinka","C":"J.P. Clark","D":"Christopher Okigbo"},"answer":"B"},
  {"text":"A long narrative poem about heroic deeds is called?","options":{"A":"Epic","B":"Ballad","C":"Lyric","D":"Sonnet"},"answer":"A"},
  {"text":"The pattern of stressed and unstressed syllables in poetry is called?","options":{"A":"Rhyme","B":"Rhythm","C":"Meter","D":"Alliteration"},"answer":"C"},
  {"text":"Giving human qualities to non-human things is called?","options":{"A":"Simile","B":"Metaphor","C":"Personification","D":"Hyperbole"},"answer":"C"},
  {"text":"The time and place in which a story occurs is called the?","options":{"A":"Plot","B":"Theme","C":"Setting","D":"Conflict"},"answer":"C"},
  {"text":"A sad poem written to mourn someone's death is called?","options":{"A":"Ode","B":"Elegy","C":"Sonnet","D":"Ballad"},"answer":"B"},
  {"text":"The narrator who knows everything about all characters is called?","options":{"A":"First person","B":"Second person","C":"Third person limited","D":"Third person omniscient"},"answer":"D"},
  {"text":"The opposition between characters or forces in a story is called?","options":{"A":"Theme","B":"Plot","C":"Conflict","D":"Setting"},"answer":"C"},
  {"text":"Who wrote \"The Trials of Brother Jero\"?","options":{"A":"Wole Soyinka","B":"Chinua Achebe","C":"Cyprian Ekwensi","D":"Femi Osofisan"},"answer":"A"},
  {"text":"A literary work that uses symbols to represent ideas is using?","options":{"A":"Imagery","B":"Symbolism","C":"Irony","D":"Allegory"},"answer":"B"},
  {"text":"The voice that tells a story is called the?","options":{"A":"Author","B":"Narrator","C":"Protagonist","D":"Character"},"answer":"B"},
  {"text":"A play that ends happily is called a?","options":{"A":"Tragedy","B":"Comedy","C":"Melodrama","D":"Farce"},"answer":"B"},
  {"text":"The repetition of vowel sounds in nearby words is called?","options":{"A":"Alliteration","B":"Consonance","C":"Assonance","D":"Rhyme"},"answer":"C"},
  {"text":"In drama, a long speech by one character is called a?","options":{"A":"Dialogue","B":"Monologue","C":"Aside","D":"Prologue"},"answer":"B"},
  {"text":"The author of \"The Palm-Wine Drinkard\" is?","options":{"A":"Chinua Achebe","B":"Amos Tutuola","C":"Wole Soyinka","D":"Gabriel Okara"},"answer":"B"},
  {"text":"A story that teaches a moral lesson, often with animals as characters, is called?","options":{"A":"Parable","B":"Fable","C":"Allegory","D":"Myth"},"answer":"B"},
  {"text":"The turning point in a story is called the?","options":{"A":"Exposition","B":"Rising action","C":"Climax","D":"Resolution"},"answer":"C"},
  {"text":"Words that sound like their meaning are examples of?","options":{"A":"Alliteration","B":"Onomatopoeia","C":"Simile","D":"Metaphor"},"answer":"B"},
  {"text":"Who wrote \"The Beautiful Ones Are Not Yet Born\"?","options":{"A":"Ayi Kwei Armah","B":"Chinua Achebe","C":"Ngugi wa Thiong'o","D":"Wole Soyinka"},"answer":"A"},
  {"text":"The use of words in a way opposite to their literal meaning is called?","options":{"A":"Paradox","B":"Irony","C":"Satire","D":"Sarcasm"},"answer":"B"},
  {"text":"A short story that teaches a moral or religious lesson is called a?","options":{"A":"Parable","B":"Fable","C":"Legend","D":"Myth"},"answer":"A"},
  {"text":"The organization of events in a story is called the?","options":{"A":"Setting","B":"Theme","C":"Plot","D":"Mood"},"answer":"C"},
  {"text":"In poetry, a group of lines forming a unit is called a?","options":{"A":"Verse","B":"Stanza","C":"Canto","D":"Couplet"},"answer":"B"},
  {"text":"The author of \"Death and the King's Horseman\" is?","options":{"A":"Chinua Achebe","B":"Wole Soyinka","C":"J.P. Clark","D":"John Pepper Clark"},"answer":"B"},
],

"CRS": [
  {"text":"According to Genesis, on which day did God create man?","options":{"A":"Fourth day","B":"Fifth day","C":"Sixth day","D":"Seventh day"},"answer":"C"},
  {"text":"The first murder in the Bible was committed by?","options":{"A":"Abel","B":"Cain","C":"Adam","D":"Seth"},"answer":"B"},
  {"text":"God made a covenant with Abraham to?","options":{"A":"Make him rich","B":"Give him many descendants","C":"Make him king","D":"Give him wisdom"},"answer":"B"},
  {"text":"Moses received the Ten Commandments on Mount?","options":{"A":"Sinai","B":"Carmel","C":"Horeb","D":"Zion"},"answer":"A"},
  {"text":"The wisest king in the Old Testament was?","options":{"A":"David","B":"Solomon","C":"Saul","D":"Rehoboam"},"answer":"B"},
  {"text":"The prophet who was swallowed by a big fish was?","options":{"A":"Elijah","B":"Elisha","C":"Jonah","D":"Hosea"},"answer":"C"},
  {"text":"Jesus was born in the town of?","options":{"A":"Nazareth","B":"Jerusalem","C":"Bethlehem","D":"Capernaum"},"answer":"C"},
  {"text":"How many disciples did Jesus have?","options":{"A":"Ten","B":"Eleven","C":"Twelve","D":"Thirteen"},"answer":"C"},
  {"text":"The first miracle Jesus performed was?","options":{"A":"Healing the blind","B":"Turning water to wine","C":"Feeding 5000","D":"Walking on water"},"answer":"B"},
  {"text":"The disciple who betrayed Jesus was?","options":{"A":"Peter","B":"John","C":"Judas Iscariot","D":"Thomas"},"answer":"C"},
  {"text":"Jesus was crucified at a place called?","options":{"A":"Bethany","B":"Golgotha","C":"Gethsemane","D":"Bethesda"},"answer":"B"},
  {"text":"The greatest commandment according to Jesus is to?","options":{"A":"Give to the poor","B":"Love God and neighbor","C":"Pray always","D":"Fast regularly"},"answer":"B"},
  {"text":"Pentecost occurred how many days after Jesus' ascension?","options":{"A":"Seven days","B":"Ten days","C":"Forty days","D":"Fifty days"},"answer":"B"},
  {"text":"The first martyr of the Christian church was?","options":{"A":"Peter","B":"Paul","C":"Stephen","D":"James"},"answer":"C"},
  {"text":"Paul was originally called?","options":{"A":"Simon","B":"Saul","C":"Samuel","D":"Solomon"},"answer":"B"},
  {"text":"The fruit of the Spirit includes?","options":{"A":"Love, joy, peace","B":"Power, might, strength","C":"Wisdom, knowledge, understanding","D":"Faith, hope, charity"},"answer":"A"},
  {"text":"The parable of the lost sheep teaches about?","options":{"A":"God's judgment","B":"God's love for sinners","C":"The end times","D":"Baptism"},"answer":"B"},
  {"text":"Who baptized Jesus?","options":{"A":"Peter","B":"John the Baptist","C":"James","D":"Andrew"},"answer":"B"},
  {"text":"The shortest verse in the Bible is?","options":{"A":"God is love","B":"Jesus wept","C":"Pray always","D":"Be holy"},"answer":"B"},
  {"text":"King David committed adultery with?","options":{"A":"Abigail","B":"Bathsheba","C":"Michal","D":"Tamar"},"answer":"B"},
  {"text":"The Good Samaritan parable teaches about?","options":{"A":"Prayer","B":"Fasting","C":"Love for neighbor","D":"Tithing"},"answer":"C"},
  {"text":"Jesus raised Lazarus after he had been dead for?","options":{"A":"One day","B":"Two days","C":"Three days","D":"Four days"},"answer":"D"},
  {"text":"The garden where Jesus prayed before his arrest was?","options":{"A":"Eden","B":"Gethsemane","C":"Paradise","D":"Calvary"},"answer":"B"},
  {"text":"Peter denied Jesus how many times?","options":{"A":"Once","B":"Twice","C":"Three times","D":"Four times"},"answer":"C"},
  {"text":"The book of Acts was written by?","options":{"A":"Matthew","B":"Mark","C":"Luke","D":"John"},"answer":"C"},
  {"text":"The wages of sin is?","options":{"A":"Poverty","B":"Death","C":"Sickness","D":"Sadness"},"answer":"B"},
  {"text":"In the beginning was the?","options":{"A":"Earth","B":"Heaven","C":"Word","D":"Light"},"answer":"C"},
  {"text":"The Beatitudes are found in?","options":{"A":"Mark","B":"Luke","C":"John","D":"Matthew"},"answer":"D"},
  {"text":"The conversion of Paul occurred on the road to?","options":{"A":"Jerusalem","B":"Damascus","C":"Antioch","D":"Rome"},"answer":"B"},
  {"text":"The Lord's Prayer begins with?","options":{"A":"Give us this day","B":"Our Father in heaven","C":"Forgive us our sins","D":"Thy kingdom come"},"answer":"B"},
  {"text":"Jesus fasted for how many days?","options":{"A":"Seven days","B":"Fourteen days","C":"Thirty days","D":"Forty days"},"answer":"D"},
  {"text":"The woman at the well was from?","options":{"A":"Galilee","B":"Judea","C":"Samaria","D":"Bethany"},"answer":"C"},
  {"text":"Faith without works is?","options":{"A":"Strong","B":"Weak","C":"Dead","D":"Alive"},"answer":"C"},
  {"text":"The love of God is described as?","options":{"A":"Conditional","B":"Limited","C":"Unconditional","D":"Temporary"},"answer":"C"},
  {"text":"The first church was established in?","options":{"A":"Rome","B":"Antioch","C":"Jerusalem","D":"Ephesus"},"answer":"C"},
],

"Commerce": [
  {"text":"Commerce is primarily concerned with?","options":{"A":"Production of goods","B":"Distribution of goods and services","C":"Manufacturing","D":"Agriculture"},"answer":"B"},
  {"text":"A document that shows ownership of shares in a company is called?","options":{"A":"Debenture","B":"Certificate","C":"Invoice","D":"Receipt"},"answer":"B"},
  {"text":"The middleman between producers and retailers is called?","options":{"A":"Wholesaler","B":"Agent","C":"Broker","D":"Factor"},"answer":"A"},
  {"text":"Home trade is divided into?","options":{"A":"Import and export","B":"Wholesale and retail","C":"Entrepot and export","D":"Coastal and inland"},"answer":"B"},
  {"text":"An insurance policy that covers goods in transit is?","options":{"A":"Fire insurance","B":"Life insurance","C":"Marine insurance","D":"Motor insurance"},"answer":"C"},
  {"text":"The document that acknowledges receipt of goods for shipment is?","options":{"A":"Bill of lading","B":"Invoice","C":"Waybill","D":"Manifest"},"answer":"A"},
  {"text":"A cheque that can only be paid into a bank account is?","options":{"A":"Open cheque","B":"Crossed cheque","C":"Bearer cheque","D":"Order cheque"},"answer":"B"},
  {"text":"The principle of insurance that restores the insured to their former position is?","options":{"A":"Utmost good faith","B":"Insurable interest","C":"Indemnity","D":"Proximate cause"},"answer":"C"},
  {"text":"Invisible trade refers to trade in?","options":{"A":"Goods","B":"Services","C":"Commodities","D":"Raw materials"},"answer":"B"},
  {"text":"A business owned by one person is called?","options":{"A":"Partnership","B":"Sole proprietorship","C":"Corporation","D":"Cooperative"},"answer":"B"},
  {"text":"The central bank of Nigeria is?","options":{"A":"First Bank","B":"Union Bank","C":"Central Bank of Nigeria","D":"Access Bank"},"answer":"C"},
  {"text":"A document sent by a seller to inform the buyer of goods dispatched is?","options":{"A":"Invoice","B":"Advice note","C":"Debit note","D":"Credit note"},"answer":"B"},
  {"text":"The difference between the cost price and selling price of goods is?","options":{"A":"Discount","B":"Profit or loss","C":"Commission","D":"Interest"},"answer":"B"},
  {"text":"Which of the following is a direct service?","options":{"A":"Banking","B":"Insurance","C":"Transportation","D":"Warehousing"},"answer":"C"},
  {"text":"A business where liability is limited to the amount invested is?","options":{"A":"Partnership","B":"Sole proprietorship","C":"Limited liability company","D":"Cooperative"},"answer":"C"},
  {"text":"The fastest means of communication is?","options":{"A":"Telephone","B":"Letter","C":"Telegram","D":"Fax"},"answer":"A"},
  {"text":"Grouping of goods according to quality and size is called?","options":{"A":"Branding","B":"Grading","C":"Packaging","D":"Labeling"},"answer":"B"},
  {"text":"An agreement to buy or sell goods at a future date is?","options":{"A":"Cash transaction","B":"Credit transaction","C":"Forward contract","D":"Spot transaction"},"answer":"C"},
  {"text":"The reward for entrepreneurship is?","options":{"A":"Wages","B":"Salary","C":"Profit","D":"Interest"},"answer":"C"},
  {"text":"A person who brings buyers and sellers together is?","options":{"A":"Wholesaler","B":"Retailer","C":"Agent","D":"Broker"},"answer":"D"},
  {"text":"Import duty is paid on goods?","options":{"A":"Exported","B":"Imported","C":"Manufactured locally","D":"Consumed locally"},"answer":"B"},
  {"text":"The document that lists goods sent by post is?","options":{"A":"Parcel post","B":"Waybill","C":"Invoice","D":"Dispatch note"},"answer":"B"},
  {"text":"Which of the following is a function of a wholesaler?","options":{"A":"Selling in small quantities","B":"Buying in large quantities","C":"Manufacturing goods","D":"Advertising to final consumers"},"answer":"B"},
  {"text":"Money kept in a bank that earns interest is kept in?","options":{"A":"Current account","B":"Savings account","C":"Fixed deposit","D":"Loan account"},"answer":"B"},
  {"text":"The practice of selling the same product at different prices in different markets is called?","options":{"A":"Price discrimination","B":"Price control","C":"Price fixing","D":"Price war"},"answer":"A"},
  {"text":"A warehouse where imported goods are kept without paying duty is called?","options":{"A":"Public warehouse","B":"Private warehouse","C":"Bonded warehouse","D":"Cold storage"},"answer":"C"},
  {"text":"The person who provides insurance cover is called?","options":{"A":"Insured","B":"Insurer","C":"Broker","D":"Agent"},"answer":"B"},
  {"text":"Advertising that promotes a particular brand is?","options":{"A":"Competitive advertising","B":"Informative advertising","C":"Persuasive advertising","D":"Generic advertising"},"answer":"A"},
  {"text":"A person who buys and sells shares on behalf of others is?","options":{"A":"Broker","B":"Jobber","C":"Dealer","D":"Agent"},"answer":"A"},
  {"text":"The removal of government control over business activities is called?","options":{"A":"Nationalization","B":"Privatization","C":"Commercialization","D":"Deregulation"},"answer":"D"},
  {"text":"Which of the following is not a means of payment?","options":{"A":"Cash","B":"Cheque","C":"Invoice","D":"Credit card"},"answer":"C"},
  {"text":"E-commerce refers to?","options":{"A":"Traditional trading","B":"Electronic trading","C":"Foreign trade","D":"Domestic trade"},"answer":"B"},
  {"text":"The document sent to a debtor requesting payment is?","options":{"A":"Invoice","B":"Receipt","C":"Statement of account","D":"Debit note"},"answer":"C"},
  {"text":"A market where shares are bought and sold is?","options":{"A":"Money market","B":"Capital market","C":"Foreign exchange market","D":"Commodity market"},"answer":"B"},
  {"text":"Consumer protection aims to?","options":{"A":"Increase prices","B":"Protect sellers","C":"Safeguard consumers' interests","D":"Reduce production"},"answer":"C"},
],

"Accounting": [
  {"text":"The systematic recording of business transactions is called?","options":{"A":"Auditing","B":"Book-keeping","C":"Accounting","D":"Costing"},"answer":"B"},
  {"text":"The accounting equation is?","options":{"A":"Assets = Liabilities + Capital","B":"Assets = Capital - Liabilities","C":"Liabilities = Assets + Capital","D":"Capital = Assets - Liabilities"},"answer":"A"},
  {"text":"Which of the following is a current asset?","options":{"A":"Land","B":"Building","C":"Cash","D":"Goodwill"},"answer":"C"},
  {"text":"The double entry principle states that?","options":{"A":"Every transaction has two entries","B":"Every debit has a credit","C":"Assets equal liabilities","D":"Income equals expenses"},"answer":"B"},
  {"text":"A business document that lists goods supplied with their prices is?","options":{"A":"Receipt","B":"Invoice","C":"Voucher","D":"Statement"},"answer":"B"},
  {"text":"Depreciation is charged on?","options":{"A":"Current assets","B":"Fixed assets","C":"Intangible assets","D":"All assets"},"answer":"B"},
  {"text":"The excess of current assets over current liabilities is called?","options":{"A":"Net profit","B":"Working capital","C":"Capital employed","D":"Gross profit"},"answer":"B"},
  {"text":"Bad debts are debts that are?","options":{"A":"Not yet due","B":"Overdue","C":"Irrecoverable","D":"Recoverable"},"answer":"C"},
  {"text":"Gross profit is calculated as?","options":{"A":"Sales minus cost of goods sold","B":"Sales minus all expenses","C":"Revenue minus capital","D":"Assets minus liabilities"},"answer":"A"},
  {"text":"A trial balance is prepared to?","options":{"A":"Determine profit","B":"Check arithmetical accuracy","C":"Calculate depreciation","D":"Value stock"},"answer":"B"},
  {"text":"Which of the following is a liability?","options":{"A":"Cash","B":"Debtors","C":"Creditors","D":"Stock"},"answer":"C"},
  {"text":"The accounting period is usually?","options":{"A":"Monthly","B":"Quarterly","C":"Annually","D":"Weekly"},"answer":"C"},
  {"text":"Accrued expenses are expenses that are?","options":{"A":"Paid in advance","B":"Outstanding","C":"Prepaid","D":"Cancelled"},"answer":"B"},
  {"text":"The straight-line method of depreciation charges?","options":{"A":"Equal amounts each year","B":"Reducing amounts each year","C":"Increasing amounts each year","D":"Variable amounts each year"},"answer":"A"},
  {"text":"Cash discount is given for?","options":{"A":"Prompt payment","B":"Bulk purchase","C":"Trade purposes","D":"Goodwill"},"answer":"A"},
  {"text":"Which account is credited when goods are sold on credit?","options":{"A":"Cash account","B":"Sales account","C":"Purchases account","D":"Debtors account"},"answer":"B"},
  {"text":"The book of original entry for credit sales is the?","options":{"A":"Cash book","B":"Sales journal","C":"Purchases journal","D":"General journal"},"answer":"B"},
  {"text":"Carriage inwards is added to?","options":{"A":"Sales","B":"Purchases","C":"Capital","D":"Liabilities"},"answer":"B"},
  {"text":"A provision for doubtful debts is created to?","options":{"A":"Write off bad debts","B":"Anticipate bad debts","C":"Recover debts","D":"Increase debtors"},"answer":"B"},
  {"text":"Net profit is transferred to?","options":{"A":"Trading account","B":"Profit and loss account","C":"Capital account","D":"Balance sheet"},"answer":"C"},
  {"text":"The document sent to a customer who returns goods is?","options":{"A":"Debit note","B":"Credit note","C":"Invoice","D":"Receipt"},"answer":"B"},
  {"text":"Opening stock plus purchases minus closing stock equals?","options":{"A":"Gross profit","B":"Net profit","C":"Cost of goods sold","D":"Sales"},"answer":"C"},
  {"text":"Petty cash is used for?","options":{"A":"Large payments","B":"Small routine expenses","C":"Capital expenditure","D":"Loan repayment"},"answer":"B"},
  {"text":"The purpose of financial statements is to?","options":{"A":"Comply with law","B":"Show financial position","C":"Calculate tax","D":"Attract investors"},"answer":"B"},
  {"text":"Assets purchased for long-term use are called?","options":{"A":"Current assets","B":"Fixed assets","C":"Liquid assets","D":"Fictitious assets"},"answer":"B"},
  {"text":"The bank reconciliation statement is prepared to?","options":{"A":"Find bank balance","B":"Agree cashbook with bank statement","C":"Calculate interest","D":"Record cheques"},"answer":"B"},
  {"text":"Revenue expenditure is?","options":{"A":"Capital in nature","B":"For fixed assets","C":"For day-to-day expenses","D":"Long-term"},"answer":"C"},
  {"text":"Drawings by the owner reduce?","options":{"A":"Assets","B":"Liabilities","C":"Capital","D":"Revenue"},"answer":"C"},
  {"text":"The current ratio measures?","options":{"A":"Profitability","B":"Liquidity","C":"Efficiency","D":"Solvency"},"answer":"B"},
  {"text":"Goodwill is classified as?","options":{"A":"Current asset","B":"Fixed asset","C":"Intangible asset","D":"Tangible asset"},"answer":"C"},
  {"text":"A debit balance in the cash book means?","options":{"A":"Bank overdraft","B":"Cash at bank","C":"Cash shortage","D":"Bank loan"},"answer":"B"},
  {"text":"The journal is used to record?","options":{"A":"Cash transactions","B":"Credit transactions","C":"Non-routine transactions","D":"All transactions"},"answer":"C"},
  {"text":"Stock valuation is based on?","options":{"A":"Cost price only","B":"Selling price only","C":"Lower of cost and net realizable value","D":"Average price"},"answer":"C"},
  {"text":"Creditors are found in the?","options":{"A":"Trading account","B":"Profit and loss account","C":"Balance sheet","D":"Cash book"},"answer":"C"},
  {"text":"The accounting concept that requires revenue to be recognized when earned is?","options":{"A":"Matching concept","B":"Realization concept","C":"Going concern concept","D":"Consistency concept"},"answer":"B"},
],

}  # end RAW_QUESTIONS


# ──────────────────────────────────────────────────────────────
# FISHER-YATES SHUFFLE (Python, at build time — JS does nothing)
# ──────────────────────────────────────────────────────────────

def fisher_yates_shuffle_options(question, rng):
    q = deepcopy(question)
    labels = ['A', 'B', 'C', 'D']
    original_answer = q['answer']
    pairs = [(lbl, q['options'][lbl]) for lbl in labels]

    n = len(pairs)
    for i in range(n - 1, 0, -1):
        j = rng.randint(0, i)
        pairs[i], pairs[j] = pairs[j], pairs[i]

    new_options = {}
    new_answer = None
    for new_idx, (orig_label, text) in enumerate(pairs):
        new_label = labels[new_idx]
        new_options[new_label] = text
        if orig_label == original_answer:
            new_answer = new_label

    q['options'] = new_options
    q['answer'] = new_answer
    return q


def prepare_questions(subject_name, raw_qs, rng):
    result = []
    for i, q in enumerate(raw_qs, start=1):
        shuffled = fisher_yates_shuffle_options(q, rng)
        shuffled['id'] = i
        shuffled['subject'] = subject_name
        result.append(shuffled)
    return result


# ──────────────────────────────────────────────────────────────
# JS SERIALIZER
# ──────────────────────────────────────────────────────────────

def esc(s):
    s = str(s).replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', '')
    return s


def questions_to_js(questions):
    lines = ['const QUESTIONS = [']
    for q in questions:
        opts = q['options']
        expl = esc(q.get('explanation', ''))
        exc  = esc(q.get('exception', ''))
        text = esc(q['text'])
        subj = esc(q['subject'])
        lines.append("  {")
        lines.append(f"    id: {q['id']}, subject: '{subj}',")
        lines.append(f"    text: '{text}',")
        lines.append(f"    options: {{ A: '{esc(opts['A'])}', B: '{esc(opts['B'])}', C: '{esc(opts['C'])}', D: '{esc(opts['D'])}' }},")
        lines.append(f"    answer: '{q['answer']}',")
        if expl:
            lines.append(f"    explanation: '{expl}',")
        if exc:
            lines.append(f"    exception: '{exc}',")
        lines.append("  },")
    lines.append('];')
    return '\n'.join(lines)


# ──────────────────────────────────────────────────────────────
# HTML TEMPLATE
# ──────────────────────────────────────────────────────────────

def build_quiz_html(title, subject_display, back_href, duration_seconds, questions_js):
    mins = duration_seconds // 60
    secs = duration_seconds % 60
    timer_display = f"{mins}:{secs:02d}"
    total_q = len(_re.findall(r'\bid:\s*\d+', questions_js))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>{title} — JAMB Practice · GrantApp AI</title>
    <link rel="stylesheet" href="quiz-styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body class="quiz-body">

<!-- QUESTIONS: Fisher-Yates shuffled at build time by build.py. JS loads nothing. -->
<script>
const DURATION = {duration_seconds};

{questions_js}
</script>

<!-- Fixed Header -->
<header class="quiz-header">
    <div class="quiz-header-container">

        <div class="quiz-header-left">
            <button class="btn-icon" id="menuBtn" aria-label="Menu">
                <i class="fas fa-bars"></i>
            </button>
            <div class="subject-info">
                <div class="subject-name" id="subjectName">{subject_display}</div>
                <div class="subject-meta">Question <span id="currentQuestionNum">1</span> of <span id="totalQuestions">{total_q}</span></div>
            </div>
        </div>

        <div class="quiz-timer-container" id="quizTimerContainer">
            <div class="timer-progress-ring">
                <svg viewBox="0 0 60 60">
                    <circle cx="30" cy="30" r="26" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="4"/>
                    <circle id="timerProgressCircle" cx="30" cy="30" r="26" fill="none"
                            stroke="var(--accent)" stroke-width="4"
                            stroke-dasharray="163.36" stroke-dashoffset="0"
                            transform="rotate(-90 30 30)" stroke-linecap="round"/>
                </svg>
            </div>
            <div class="timer-icon"><i class="fas fa-clock"></i></div>
            <div class="timer-display" id="timerDisplay">{timer_display}</div>
        </div>

        <div class="quiz-header-right">
            <button class="btn-icon" id="calculatorBtn" aria-label="Calculator">
                <i class="fas fa-calculator"></i>
            </button>
            <button class="btn btn-sm btn-danger" id="submitBtn">Submit</button>
        </div>
    </div>
</header>

<div class="quiz-container">

    <aside class="quiz-sidebar" id="quizSidebar">
        <div class="sidebar-header">
            <h3>Navigator</h3>
            <button class="btn-icon btn-close-sidebar" id="closeSidebar" aria-label="Close">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="sidebar-stats">
            <div class="stat-item">
                <div class="stat-value" id="answeredCount">0</div>
                <div class="stat-label">Done</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="unansweredCount">{total_q}</div>
                <div class="stat-label">Left</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="flaggedCount">0</div>
                <div class="stat-label">Flagged</div>
            </div>
        </div>
        <div class="question-palette" id="questionPalette"></div>
        <div class="sidebar-legend">
            <div class="legend-item"><span class="legend-dot current"></span> Current</div>
            <div class="legend-item"><span class="legend-dot answered"></span> Answered</div>
            <div class="legend-item"><span class="legend-dot flagged"></span> Flagged</div>
            <div class="legend-item"><span class="legend-dot"></span> Unanswered</div>
        </div>
        <div style="padding:1rem;border-top:1px solid var(--border,#1e1e2e);margin-top:auto;">
            <a href="{back_href}"
               class="btn btn-secondary"
               style="width:100%;text-align:center;text-decoration:none;display:block;"
               onclick="return confirm('Leave quiz? Progress will be lost.')">
                &#8592; Back
            </a>
        </div>
    </aside>

    <main class="quiz-main">
        <div class="question-card" id="questionCard">
            <div class="question-header">
                <div class="question-number">Question <span id="questionNumber">1</span></div>
                <button class="btn-flag" id="flagBtn" aria-label="Flag">
                    <i class="far fa-flag"></i> Flag
                </button>
            </div>
            <div class="question-text" id="questionText">Loading...</div>
            <div class="options-container" id="optionsContainer"></div>
            <div class="question-explanation hidden" id="questionExplanation">
                <div class="explanation-header"><i class="fas fa-lightbulb"></i> Explanation</div>
                <div class="explanation-content" id="explanationContent"></div>
            </div>
        </div>

        <div class="quiz-navigation">
            <button class="btn btn-secondary" id="prevBtn" disabled>
                <i class="fas fa-arrow-left"></i> Previous
            </button>
            <button class="btn btn-secondary" id="clearBtn">
                <i class="fas fa-eraser"></i> Clear
            </button>
            <button class="btn btn-primary" id="nextBtn">
                Next <i class="fas fa-arrow-right"></i>
            </button>
        </div>
    </main>
</div>

<div class="mobile-palette-trigger" id="mobilePaletteBtn">
    <i class="fas fa-th"></i> <span>Questions</span>
</div>

<!-- Submit Modal -->
<div class="modal-overlay hidden" id="submitModal">
    <div class="modal">
        <div class="modal-header">
            <h3>Submit Test?</h3>
            <button class="btn-icon" id="closeSubmitModal"><i class="fas fa-times"></i></button>
        </div>
        <div class="modal-body">
            <div class="submit-summary">
                <div class="summary-item"><span class="summary-label">Total</span><span class="summary-value" id="modalTotalQuestions">{total_q}</span></div>
                <div class="summary-item"><span class="summary-label">Answered</span><span class="summary-value answered-text" id="modalAnsweredCount">0</span></div>
                <div class="summary-item"><span class="summary-label">Unanswered</span><span class="summary-value warning-text" id="modalUnansweredCount">{total_q}</span></div>
                <div class="summary-item"><span class="summary-label">Time Left</span><span class="summary-value" id="modalTimeRemaining">{timer_display}</span></div>
            </div>
            <div class="warning-message">
                <i class="fas fa-exclamation-triangle"></i>
                <span>You cannot change answers after submission.</span>
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" id="cancelSubmitBtn">Cancel</button>
            <button class="btn btn-danger" id="confirmSubmitBtn"><i class="fas fa-check"></i> Submit</button>
        </div>
    </div>
</div>

<!-- Time Up Modal -->
<div class="modal-overlay hidden" id="timeUpModal">
    <div class="modal">
        <div class="modal-header"><h3>&#8987; Time's Up!</h3></div>
        <div class="modal-body">
            <p style="color:var(--muted);font-size:0.9rem;">Your time has run out. Answers recorded.</p>
        </div>
        <div class="modal-footer">
            <button class="btn btn-primary" id="viewResultsBtn">View Results</button>
        </div>
    </div>
</div>

<!-- Calculator Modal -->
<div class="modal-overlay hidden" id="calculatorModal">
    <div class="modal calculator-modal">
        <div class="modal-header">
            <h3>Calculator</h3>
            <button class="btn-icon" id="closeCalculatorModal"><i class="fas fa-times"></i></button>
        </div>
        <div class="modal-body">
            <div class="calculator">
                <input type="text" class="calculator-display" id="calcDisplay" value="0" readonly>
                <div class="calculator-buttons">
                    <button class="calc-btn" data-action="clear">C</button>
                    <button class="calc-btn" data-action="delete">&#8592;</button>
                    <button class="calc-btn" data-action="divide">&#247;</button>
                    <button class="calc-btn" data-action="multiply">&#215;</button>
                    <button class="calc-btn" data-value="7">7</button>
                    <button class="calc-btn" data-value="8">8</button>
                    <button class="calc-btn" data-value="9">9</button>
                    <button class="calc-btn" data-action="subtract">&#8722;</button>
                    <button class="calc-btn" data-value="4">4</button>
                    <button class="calc-btn" data-value="5">5</button>
                    <button class="calc-btn" data-value="6">6</button>
                    <button class="calc-btn" data-action="add">+</button>
                    <button class="calc-btn" data-value="1">1</button>
                    <button class="calc-btn" data-value="2">2</button>
                    <button class="calc-btn" data-value="3">3</button>
                    <button class="calc-btn calc-equals" data-action="equals" style="grid-row:span 2">=</button>
                    <button class="calc-btn" data-value="0" style="grid-column:span 2">0</button>
                    <button class="calc-btn" data-value=".">.</button>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="quiz-app.js"></script>
</body>
</html>"""


# ──────────────────────────────────────────────────────────────
# CLUSTER & INDIVIDUAL SUBJECT DEFINITIONS
# ──────────────────────────────────────────────────────────────

INDIVIDUAL_SUBJECTS = {
    "quiz-biology":    {"subject": "Biology",     "duration": 900,  "back": "science_clusters.html"},
    "quiz-chemistry":  {"subject": "Chemistry",   "duration": 900,  "back": "science_clusters.html"},
    "quiz-english":    {"subject": "English",     "duration": 900,  "back": "index.html"},
    "quiz-government": {"subject": "Government",  "duration": 900,  "back": "art_clusters.html"},
    "quiz-literature": {"subject": "Literature",  "duration": 900,  "back": "art_clusters.html"},
    "quiz-crs":        {"subject": "CRS",         "duration": 900,  "back": "art_clusters.html"},
    "quiz-commerce":   {"subject": "Commerce",    "duration": 900,  "back": "commercial_clusters.html"},
    "quiz-accounting": {"subject": "Accounting",  "duration": 900,  "back": "commercial_clusters.html"},
}

CLUSTERS = {
    "quiz-science-mepc": {
        "title": "Science — MEPC",
        "display": "Science: MEPC",
        "use_subjects": ["Mathematics", "English", "Chemistry"],
        "duration": 3600,
        "back": "science_clusters.html",
    },
    "quiz-science-bepc": {
        "title": "Science — BEPC",
        "display": "Science: BEPC",
        "use_subjects": ["Biology", "English", "Chemistry"],
        "duration": 3600,
        "back": "science_clusters.html",
    },
    "quiz-arts-a": {
        "title": "Arts Cluster A",
        "display": "Arts Cluster A",
        "use_subjects": ["English", "Literature", "Government", "CRS"],
        "duration": 3600,
        "back": "art_clusters.html",
    },
    "quiz-commerce-a": {
        "title": "Commercial Cluster A",
        "display": "Commercial Cluster A",
        "use_subjects": ["English", "Commerce", "Accounting", "Government"],
        "duration": 3600,
        "back": "commercial_clusters.html",
    },
}


# ──────────────────────────────────────────────────────────────
# MAIN BUILD
# ──────────────────────────────────────────────────────────────

def main():
    rng = random.Random(42)
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    generated = []

    # Individual subject pages
    for filename, cfg in INDIVIDUAL_SUBJECTS.items():
        subj = cfg["subject"]
        if subj not in RAW_QUESTIONS:
            print(f"  SKIP {filename} — no question data for {subj}")
            continue
        questions = prepare_questions(subj, RAW_QUESTIONS[subj], rng)
        js = questions_to_js(questions)
        html = build_quiz_html(
            title=subj,
            subject_display=subj,
            back_href=cfg["back"],
            duration_seconds=cfg["duration"],
            questions_js=js
        )
        path = os.path.join(output_dir, f"{filename}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  OK  {filename}.html  ({len(questions)}q)")
        generated.append(f"{filename}.html")

    # Cluster combo pages
    for filename, cfg in CLUSTERS.items():
        combined = []
        q_id = 1
        for subj in cfg["use_subjects"]:
            if subj not in RAW_QUESTIONS:
                print(f"      NOTE: {subj} not available for {filename}")
                continue
            qs = prepare_questions(subj, RAW_QUESTIONS[subj], rng)
            for q in qs:
                q['id'] = q_id
                q_id += 1
            combined.extend(qs)
        if not combined:
            print(f"  SKIP {filename} — no questions")
            continue
        js = questions_to_js(combined)
        html = build_quiz_html(
            title=cfg["title"],
            subject_display=cfg["display"],
            back_href=cfg["back"],
            duration_seconds=cfg["duration"],
            questions_js=js
        )
        path = os.path.join(output_dir, f"{filename}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  OK  {filename}.html  ({len(combined)}q)")
        generated.append(f"{filename}.html")

    print(f"\nBuilt {len(generated)} files in ./{output_dir}/")


if __name__ == "__main__":
    main()
