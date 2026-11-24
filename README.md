# Cognitive load, intrinsic motivation, and academic self-efficacy

Python re-analysis of my undergraduate thesis data (N = 250 university students). The original analysis was conducted in SPSS. This repository rebuilds the scale scores from the questionnaire items and runs the main analyses in a fully scripted workflow so every step is transparent and reproducible.

## Research question

Do cognitive load and intrinsic motivation relate to academic self-efficacy among university students, and does the relationship between load and self-efficacy depend on level of motivation?

## Main findings

- All three scales showed good reliability (Cronbach’s α = .82 to .91).
- Intrinsic motivation was significantly related to academic self-efficacy.
- Cognitive load showed a significant association with intrinsic motivation.
- Cognitive load did not uniquely predict academic self-efficacy once intrinsic motivation was included.
- There was a significant interaction between cognitive load and intrinsic motivation: the link between load and self-efficacy differed according to motivation level.

All numbers are taken directly from the CSV files in the `results/` folder. The scripts that produced them are in `scripts/`.

## How to run

```bash
pip install -r requirements.txt
python scripts/01_prepare.py
python scripts/02_descriptives_reliability.py
python scripts/03_correlations.py
python scripts/04_regression.py
python scripts/05_figures.py
```

Script 01 requires the raw Excel file (`Thesis Data File.xlsx`) placed in the parent folder or the same folder as the repository. Later scripts only need the cleaned data file that script 01 creates.

## Data availability

Item-level questionnaire responses are not shared publicly because participant consent covered academic use only. The analysis pipeline and de-identified scale scores are provided here so that every reported result can be traced to the code that generated it. The dataset is available on reasonable request for verification purposes.

## Limitations

- The data are cross-sectional and based on self-report measures.
- The sample is predominantly female and middle socioeconomic status.
- Perceived cognitive load is not equivalent to experimentally manipulated load.

## Next steps

Future work could test these relationships under experimental load manipulation and examine possible mediators such as perceived competence or academic stress.
