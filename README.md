# LineUp Index Explorer

This prototype serves an explanation-first LineUp.js view of `index/03-outputs/Final_Index.csv`.

## Run locally

```bash
cd index/tools/lineup-index-explorer
PIPENV_VENV_IN_PROJECT=1 pipenv run app
```

Then open:

```text
http://127.0.0.1:8010/
```

Set `PORT` to run another copy:

```bash
PORT=8011 PIPENV_VENV_IN_PROJECT=1 pipenv run app
```

## What This Version Shows

- A local browser view of the final LT4CR index CSV.
- A compact explanation header focused on the five index pillars.
- A LineUp ranking sorted by `weighted_index` and grouped by `Region`.
- Raw CSV data served from the existing `index/03-outputs` folder.

## Prototype Notes

This version uses CDN-hosted LineUp.js assets so the repository does not need to vendor the upstream
LineUp.js source or build artifacts. The data itself is served locally from this project.
