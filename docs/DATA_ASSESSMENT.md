# Data assessment: NMC/MCI Competency-Based UG Curriculum (2018), Vols I-III

## Source
- 3 PDFs, 690 pages. Embedded text layer used (more accurate than OCR on a test page); no OCR needed.
- Parsed with a row-anchored layout parser (code + Domain/Level/Core tokens per row).

## Output
| file | content |
|---|---|
| competencies.csv / .jsonl | 2,893 unique competencies, one row per code (JSONL adds a `text` field for NLP use) |
| integration_links.csv | 1,932 cross-listings (same competency repeated under another subject as vertical/horizontal integration) |

## Volume
- Raw parsed rows: 4,759 -> 2,893 unique codes (1,866 duplicates removed; owner-subject row preferred)
- 23 subjects, 408 topics, 126 distinct action verbs, median 13 words/competency (max 102)

## Labels / class balance
- level_max: KH 1,803 (62%), SH 830 (29%), K 189 (7%), P 66 (2%), S 5 (<1%)  -> highly imbalanced; merge S into SH if modelling
- core: 2,570 core (89%) vs 323 non-core
- domain: K 1,887; S 621; K|S 243; A|C 40; C 24; A 21; K|S|A|C 17; S|C 9 (multi-hot dom_K/S/A/C provided)
- Largest subjects: IM 501, AN 408, PE 397, PA 178, FM 150; smallest RD 13, RT 16, DE 23

## Splits
- `split` column = deterministic hash of topic_id (train 2,274 / val 305 / test 314). Split by topic, not row, to avoid leakage from near-identical sibling competencies within a topic.

## Quality checks
- Automated spot check against source text, 200 random rows (code, level, core, text prefix): 196/200 pass (98%).
- qc_flags set on 148 rows (5%): long_text (22), integration_garbled (26), no_assessment (78), no_teaching_method (25), short_text, spurious_subject (1 noise row 'PF', from the contributors list - drop it).
- Topic names missing in clinical volumes' row lines were back-filled from the topic header by topic_id (0 missing now).
- 32 competencies share identical text with another code (legitimate repeats across subjects).

## Known limitations
- vertical/horizontal integration columns are the weakest fields (layout drift, wrapped text); treat as noisy, rely on integration_links.csv for subject links.
- Teaching/assessment methods are keyword-extracted into multi-hot columns (tl_*, as_*); free text kept alongside. Wrapped cells are jumbled in the PDF, so a few rows may carry extra/missing labels.
- n_procedures_to_certify only populated for 37 rows; certifiable procedures are otherwise listed in separate tables not modelled here.
- Counts per topic header ("Number of competencies") were not reconciled against parsed counts.
- Competency IDs with letter suffixes or odd formats were parsed with a generic pattern; a few may be missed.

## Update: coverage audit (second pass)
First pass captured 2,893 codes; an audit against the PDFs found 56 more, now included (total 2,949 unique competencies).
Causes: indented rows missed by the row detector; domain/level typos in the source ("A and C", "KH /", "K/H"); codes split across lines or mistyped ("PE27 1", "PA 17.1", "PA`18.2", "PF27.21"); 17 rows with garbled text layers transcribed from page images.
Verified against each topic's stated competency count. Genuinely absent from the PDFs: PA22.3, SU26.2, FM2.15.
Corrections to figures above: 5,296 questions (2,949 competencies); the spurious `PF` row is now PE27.21.
