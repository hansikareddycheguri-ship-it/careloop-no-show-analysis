# CareLoop Clinics — No-Show Analysis

**Repository:** https://github.com/hansikareddycheguri-ship-it/careloop-no-show-analysis

**Business question:** Which appointments are most likely to be missed, why do patients miss them, and what should CareLoop do first?

## Summary (one finding per Part)

1. **Data (Part 1):** The raw export had 1,020 rows. After removing 20 duplicates and 10 rows with no usable date or status, 990 clean appointments remain, and 218 of them (22.0%) are no-shows.
2. **SQL (Part 2):** Lead time matters most. Bookings made 31+ days ahead are missed 60.5% of the time, compared with 16.2% for bookings made within a week.
3. **Model (Part 3):** Logistic regression ranks risk best (test ROC-AUC 0.789). At a 0.35 threshold it flags 49 of 198 test bookings and catches 57% of the real no-shows.
4. **GenAI (Part 4):** The 9 readable call notes split mainly into forgetting or no reminder (2), distance or transport (2) and work or schedule (2), and both "forgot" notes came from appointments where no reminder was sent.

## Recommendation

CareLoop should start with reminders and an evening call list. In the risk model, holding the other features constant, appointments with a reminder have about 69% lower odds of a no-show (odds ratio 0.31). Both call-centre notes that blamed forgetting came from appointments with no reminder, and 5 of the 10 notes overall belong to unreminded appointments. Every booking should get a reminder, especially the long-lead ones: 296 bookings (29.9%) were made more than 14 days ahead, and the rate climbs from 16.2% within a week to 30.0% at 15–30 days and 60.5% beyond 30 days. Each evening, the front desk should phone the bookings the model scores at 0.35 or above. On the test set that is about a quarter of bookings (49 of 198), and the calls reach 57% of the patients who would otherwise not turn up. Hadapsar (27.3%), Malviya Nagar (26.8%) and Gomti Nagar (33.3%, but only 90 appointments) are the clinics to watch first. For the distance and work-schedule reasons in the notes, the call can offer an evening or Saturday slot or a nearer clinic.

## Model choice

- **Model:** logistic regression, inside a pipeline with `StandardScaler`.
- **Why:** it had the highest 5-fold cross-validated ROC-AUC on the training set (0.774), ahead of the tuned random forest (0.767), the random forest (0.747) and the depth-3 tree (0.678). The choice was made without looking at the test set.
- **Threshold:** 0.35, chosen from out-of-fold training probabilities. It gave a higher F1 than 0.5 (0.489 vs 0.347) and much higher recall (0.467 vs 0.249). Recall matters because a missed warning costs an empty doctor slot, while an extra call costs a minute.
- **One test-set evaluation:** ROC-AUC 0.789, precision 0.571, recall 0.571, 49 bookings flagged. The scores are in `test_risk_scores.csv`.

## Limitations

1. **The 10 notes are only an illustration.** They are too few to show the real reasons for no-shows across all eight clinics.
2. **The cleaning statistics used every row.** The medians, quartiles and outlier fences were computed on all 990 rows before the train/test split, so the test rows had a small indirect influence. The split was also random rather than past-to-future, and the same patient can appear in both train and test, so the test scores may be slightly optimistic.
3. **The data are observational.** The reminder effect is an association, not proof that reminders cause fewer no-shows. A small trial of reminders would be needed to confirm it.

## Files

| File | What it is |
|---|---|
| `data/` | The original three CSV files, unedited |
| `part1datafoundation.ipynb` | Reading, cleaning, features, API enrichment and SQL export |
| `rejected_rows.json` | Rows rejected by the `csv` module check (Task 1.1) |
| `appointments_clean.csv` | The cleaned table: 990 rows, 16 columns |
| `clinics_enriched.csv` | The clinics with `temp_c` from Open-Meteo |
| `load_data.sql` | 998 INSERT statements (8 clinics + 990 appointments) |
| `part2_queries.sql` | All Part 2 SQL queries |
| `part2_sql_checks.ipynb` | The pandas check of the SQL clinic counts |
| `Part3_Model.ipynb` | Baseline, logistic regression, trees, random forest, tuning and threshold |
| `test_risk_scores.csv` | Risk score and flag for the 198 test bookings |
| `Part4_GenAI.ipynb` | Gemini note analysis, Pydantic validation, prompt tests and the merge |
| `notes_analysed.csv` | Structured reasons for the first 10 call notes |

The Gemini API key is typed in at run time and is not stored anywhere in this repository.
