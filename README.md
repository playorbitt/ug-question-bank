# UG Medical Question Bank
5,184 written, viva and skill-station prompts generated from the 2,885 competencies of the MCI/NMC Competency Based UG Curriculum (2018, Vols I-III). Prompts carry no answer key; each cites its source code and page.

- `public/` static site (no build step), `public/questions.json` data
- `data/competencies.csv|jsonl` cleaned competency dataset; `docs/DATA_ASSESSMENT.md` quality report
- Deploy: `vercel --prod` (outputDirectory is `public`)
