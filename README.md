# UG Medical Question Bank
5,296 written, viva and skill-station prompts generated from the 2,949 competencies of the MCI/NMC Competency Based UG Curriculum (2018, Vols I-III). Prompts carry no answer key; each cites its source code and page.

- `public/` static site (no build step), `public/questions.json` data
- `data/competencies.csv|jsonl` cleaned competency dataset; `docs/DATA_ASSESSMENT.md` quality report
- Deploy: `vercel --prod` (outputDirectory is `public`)

## Coverage audit (vs source PDFs)
Cross-checked against every code in the PDF text and each topic's stated "Number of competencies": 2,949 unique competencies captured.
Not present in the PDFs themselves (numbered but absent): PA22.3, SU26.2, FM2.15. 17 rows were transcribed manually from page images (`qc_flags` = `manual_transcription`) and a few source code typos were normalised (e.g. `PF27.21` -> `PE27.21`, `PA 17.1`, `CM 20.3`).
Regenerate questions: `python3 scripts/make_questions.py`.
