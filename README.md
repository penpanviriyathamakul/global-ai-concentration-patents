# AI patents by country (draft)

Question: Which countries lead AI patenting, and how has their share of world AI patents changed from 2010 to 2024?

## Structure

- `app.py`: entry point and page navigation
- `pages/1_patents.py`: the Patents page
- `src/views.py`: the rendering function for the page
- `src/data.py`: data build and validation
- `data/`: sample and processed data
- `docs/data_notes.md`: data notes
- `dashboard.yml`: manifest (subject still needs confirming)

## Run

    export DASHBOARD_SAMPLE_MODE=1
    streamlit run app.py

## Rebuild and validate

    export DASHBOARD_SAMPLE_MODE=1
    python -m src.data
    python -m src.data --validate

Python 3.11 is required. Install with `pip install -r requirements.txt`.
