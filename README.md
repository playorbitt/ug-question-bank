# UG Medical Question Bank (NMC CBME 2024)
4,850 written, viva and skill-station prompts generated from the 2,624 competencies of the NMC **Competency Based Medical Education Curriculum 2024** (re-issued 12/09/2024), each tagged with how it changed from the 2018 curriculum (New / Reworded / Minor edit / Unchanged). Prompts carry no answer key; each cites its source code and PDF page. In effect there is one distinct question per competency; the written/viva/skill variants reuse the same wording.

- `public/` static site (no build step), `public/questions.json` data
- `data/competencies_2024.*` cleaned 2024 dataset (primary); `data/competencies_2018.*` 2018 dataset (subject labels fixed); `data/integration_links_2018.csv`
- `data/comparison_2018_vs_2024.csv` pair-by-pair comparison (matched, removed, new)
- `docs/COMPARISON_2018_vs_2024.md` comparison and extraction audit; `docs/DATA_ASSESSMENT.md` 2018 data assessment
- `scripts/` parsing and question-generation code. Regenerate questions: `python3 scripts/make_questions.py`
- Deploy: static, `outputDirectory` = `public`

Source: *NMC Compendium 2024, Vol. 2 (Curriculum)*, pp. 472-938. The 31/08/2024 guidelines (pp. 1-470) were withdrawn on 05/09/2024 and are not used.
