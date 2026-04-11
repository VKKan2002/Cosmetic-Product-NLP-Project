# Investigating the Prevalence of EDCs in Popular Beauty Products

> An AI/ML and NLP pipeline for detecting **Endocrine Disrupting Chemicals (EDCs)** in skincare and cosmetic products — combining web scraping, LLM-assisted ingredient matching, and biomedical NLP for risk analysis.

---

## Project Overview

This pipeline automates three key steps: scraping ingredient lists from popular retail sites, cross-referencing those ingredients against a curated EDC database, and quantifying health risk using scientific literature from PubMed. The goal is to surface EDC exposure risks hiding in plain sight on product labels.

---

## Methodology

### Phase 1 — Data Collection (Web Scraping)
- Uses **Playwright** and **BeautifulSoup** to scrape ingredient lists from beauty products on Sephora and similar retail sites
- Raw ingredient text is cleaned and structured via the **Gemini LLM**

### Phase 2 — EDC Identification
- Scraped ingredients are cross-referenced against the **TEDX Potential Endocrine Disruptor Exchange** list
- **Gemini LLM** handles intelligent fuzzy matching to account for synonyms, IUPAC names, and complex formulations

### Phase 3 — Risk Analysis
- Identified EDCs are queried against **PubMed** to retrieve abstracts related to cancer and hormonal disruption
- **PubMedBERT** generates text embeddings; **cosine similarity** scores measure semantic relevance between retrieved literature and target health risks
- Results are visualized as boxplots per product/ingredient

---

## Repository Contents

| File | Description |
|---|---|
| `Matching_clean.ipynb` | Core ingredient parsing and TEDX EDC matching logic (clean version) |
| `Matching.ipynb` | Alternate/development version of the matching notebook |
| `UpdatedBERT_Code.ipynb` | PubMedBERT embeddings, cosine similarity scoring, and boxplot visualizations |
| `analysis_results (1).csv` | Final dataset mapping product ingredients to verified EDC names |
| `Matching_Output.docx` | Parsed output document with ingredient-to-EDC mappings |
| `edc_match_example_list.txt` | Sample EDC reference list used for testing |
| `*.pptx` | Presentation decks covering research background, workflow, limitations, and next steps |

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/VKKan2002/<repo-name>.git
cd <repo-name>
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

```bash
playwright install
```

### 4. Configure API Keys

In `Matching_clean.ipynb` and `Matching.ipynb`, replace the placeholder with your actual key:

```python
GEMINI_API_KEY = "YOUR_API_KEY"
```

> **Note:** A valid [Google Gemini API key](https://aistudio.google.com/app/apikey) is required to run the EDC matching notebooks.

---

## Requirements

```
pandas
google-generativeai
playwright
beautifulsoup4
matplotlib
seaborn
transformers
torch
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## Limitations

- Initial dataset is limited to **25 sampled products** — results are illustrative, not population-representative
- EDC matching relies on LLM inference; edge cases with novel or heavily branded ingredient names may reduce recall
- Risk scoring reflects **semantic similarity** to health-related literature, not a clinical dosage-based assessment
- Ingredient concentrations are not currently factored into risk scores

---

## Future Work

- **Dosage-based risk modeling** — incorporate ingredient concentration data for more clinically grounded risk scores
- **SciSpacy NER integration** — replace LLM-only matching with biomedical chemical entity recognition for improved precision and recall
- **Dataset expansion** — scale beyond 25 products to enable statistically meaningful prevalence estimates
- **Product category analysis** — compare EDC prevalence across product types (moisturizers, foundations, sunscreens, etc.)

---

## Authors & Acknowledgments

Developed as a collaborative research project with contributors from **Georgetown University**, **Bryn Mawr College**, and **George Mason University**, presented at the **AI CoLab Annual Scientific Meeting (2026)**.

EDC reference data sourced from the [TEDX Potential Endocrine Disruptor Exchange](https://endocrinedisruption.org/).

---

## License

This project is for academic and research purposes. Please cite appropriately if building on this work.