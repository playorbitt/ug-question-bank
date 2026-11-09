# NMC CBME 2018 vs 2024: comparison

**Sources:** 2018 = MCI *Competency Based UG Curriculum*, Vols I-III. 2024 = *NMC Compendium 2024, Vol. 2*, pages 472-938 (the CBME Guidelines **re-issued 12/09/2024**; the 31/08/2024 version at pp. 1-470 was withdrawn on 05/09/2024 and is not used).

## Headline

- 2018: **2,949** competencies. 2024: **2,624** (-325, 11% fewer).
- Matched in both: **2,029** (1,065 identical text, 295 minor edits, 669 reworded).
- **Removed in 2024: 920**; **new in 2024: 595**.
- Among matched pairs: code changed 966, level (K/KH/S/SH/P) changed 134, core flag changed 48.
- Subjects in 2018 but **not in the 2024 text**: Respiratory Medicine (47), Physical Medicine & Rehabilitation (43), Dentistry (23), Radiotherapy (16). Psychiatry shrinks from 117 to 17 (its heading states 17); Pediatrics 405 -> 253.

## By subject

| Subject | 2018 | 2024 | Identical | Minor edit | Reworded | Removed | New |
|---|---:|---:|---:|---:|---:|---:|---:|
| Anaesthesiology | 46 | 51 | 40 | 3 | 2 | 1 | 6 |
| Biochemistry | 92 | 82 | 12 | 1 | 29 | 50 | 40 |
| Community Medicine | 107 | 136 | 70 | 8 | 23 | 6 | 35 |
| Dentistry | 23 | 0 | 0 | 0 | 0 | 23 | 0 |
| Dermatology, Venereology & Leprosy | 73 | 48 | 7 | 1 | 11 | 54 | 29 |
| Forensic Medicine & Toxicology | 162 | 157 | 62 | 33 | 35 | 32 | 27 |
| General Medicine | 506 | 529 | 220 | 75 | 130 | 81 | 104 |
| General Surgery | 132 | 132 | 96 | 7 | 25 | 4 | 4 |
| Human Anatomy | 409 | 413 | 284 | 36 | 73 | 16 | 20 |
| Microbiology | 54 | 73 | 0 | 2 | 20 | 32 | 51 |
| Obstetrics & Gynaecology | 126 | 142 | 63 | 23 | 37 | 3 | 19 |
| Ophthalmology | 60 | 59 | 6 | 0 | 19 | 35 | 34 |
| Orthopaedics | 39 | 39 | 8 | 8 | 16 | 7 | 7 |
| Otorhinolaryngology (ENT) | 76 | 63 | 11 | 6 | 35 | 24 | 11 |
| Pathology | 181 | 181 | 77 | 23 | 55 | 26 | 26 |
| Pediatrics | 405 | 253 | 86 | 64 | 79 | 176 | 24 |
| Pharmacology | 85 | 92 | 4 | 0 | 22 | 59 | 66 |
| Physical Medicine & Rehabilitation | 43 | 0 | 0 | 0 | 0 | 43 | 0 |
| Physiology | 137 | 136 | 19 | 5 | 58 | 55 | 54 |
| Psychiatry | 117 | 17 | 0 | 0 | 0 | 117 | 17 |
| Radiodiagnosis | 13 | 21 | 0 | 0 | 0 | 13 | 21 |
| Radiotherapy | 16 | 0 | 0 | 0 | 0 | 16 | 0 |
| Respiratory Medicine | 47 | 0 | 0 | 0 | 0 | 47 | 0 |

## How matching was done (read before relying on the numbers)

Codes were renumbered between editions (966 matched pairs have a different code), so competencies were matched by **text similarity within each subject** (TF-IDF cosine on word 1-2-grams, one-to-one greedy assignment, threshold 0.45; IM->GM and BI->BC mapped). Thresholds: identical = same text ignoring case/punctuation; minor edit >= 0.85; reworded 0.45-0.85. This is a heuristic: a few 'reworded' pairs may really be different competencies and a few 'removed'/'new' pairs may be heavy rewrites. The full pair list is in `data/comparison_2018_vs_2024.csv` for review.

## 2024 extraction audit

Parsed from the PDF text layer and checked against each subject's own heading total / topic counts:

| Subject | Heading total | Captured |
|---|---:|---:|
| AN | 413 | 413 |
| BC | 84 | 82 |
| DR | 48 | 48 |
| FM | 158 | 157 |
| GM | 525 | 529 |
| MI | 74 | 73 |
| PA | 182 | 181 |
| PH | 92 | 92 |
| PS | 17 | 17 |
| PY | 136 | 136 |

Captured can differ from a stated total because the PDF's own counts and numbering are inconsistent (e.g. GM9 states 21 but lists 17; BC14.1, PA29.1, MI8.3, FM2.12, GM8.9, SU26.2 are numbered gaps, and GM has more rows than its heading states). 20 rows had their text cleaned of column bleed, 32 rows were transcribed or corrected from page images (see `qc_flags`), 6 rows have a blank core flag in the source and 1 (GM11.5) has no domain or level in the source.

## Known limitations
- 2024 teaching-learning and assessment columns are less reliable than text/level/core (vertically-centred cells in some tables); they are used only to pick the question type.
- 2024 uses new subject codes (GM, BC) and new abbreviations (LGT, SGT, SDL, CBL, ...).
- Subjects like Emergency Medicine PG (pp. 939-973) are out of scope.
