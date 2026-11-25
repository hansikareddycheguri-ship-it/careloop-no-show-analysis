# CareLoop Clinics — No-Show Guard

**From appointment data to no-show risk prediction and AI-assisted follow-up recommendations**

## Project Overview

CareLoop Clinics wants to understand why patients miss their scheduled appointments and identify bookings that are more likely to result in no-shows.

This project builds an end-to-end data analysis pipeline that combines Python-based data cleaning, SQL analytics, machine learning, and Generative AI to help clinics make better follow-up decisions.

The central business question is:

> Which appointments are most likely to be missed, why do patients miss them, and what should CareLoop do first?

## Project Objectives

- Clean and validate raw appointment data.
- Analyse appointment and clinic-level trends using SQL.
- Build and evaluate machine learning models to predict no-show risk.
- Use Gemini to extract structured reasons from call-centre notes.
- Combine the findings into practical recommendations for clinic operations.

## Project Workflow

### Part 1 — Data Ingestion and Cleaning

The raw appointment data was processed using Python.

Key steps:
- Read and validate the original CSV files.
- Identify and separate invalid records.
- Remove duplicate appointments.
- Handle missing and invalid values.
- Create additional features for analysis and modelling.
- Enrich clinic information with temperature data from Open-Meteo.
- Export the cleaned datasets and SQL insert statements.

**Key results:**
- Raw appointment records: 1,020
- Duplicate records removed: 20
- Rows without usable date or status: 10
- Final cleaned appointments: 990
- Clinics covered: 8
- No-show appointments: 218
- Overall no-show rate: 22.0%

### Part 2 — SQL Analysis

SQL was used to analyse appointment patterns and identify factors associated with missed appointments.

The analysis covers:
- Clinic-wise appointment and no-show statistics.
- No-show rates across different booking lead-time groups.
- Monthly appointment trends.
- Clinic rankings and comparative performance.

**Key finding:**

Appointments booked more than 30 days in advance had a no-show rate of **60.5%**, compared with **16.2%** for appointments booked within 7 days.

This indicates that longer booking lead times are an important factor to consider when planning patient follow-ups.

### Part 3 — Machine Learning: No-Show Risk Prediction

Machine learning models were developed to estimate the probability that an appointment would be missed.

Models evaluated:
- Baseline classifier
- Logistic Regression
- Decision Tree
- Random Forest
- Tuned Random Forest

The models were compared using 5-fold cross-validation on the training data. Logistic Regression achieved the highest cross-validated ROC-AUC.

**Selected model:** Logistic Regression with StandardScaler in a pipeline.

**Model results:**

| Metric | Result |
|---|---:|
| Training records | 792 |
| Test records | 198 |
| Test ROC-AUC | 0.789 |
| Test precision | 0.571 |
| Test recall | 0.571 |
| Risk threshold | 0.35 |
| Test bookings flagged | 49 |

A threshold of 0.35 was selected using out-of-fold training predictions. It provides higher recall than the default threshold of 0.5, helping identify more appointments that may become no-shows.

The resulting risk scores and predictions are available in `test_risk_scores.csv`.

### Part 4 — Generative AI: Call-Note Analysis

Gemini was used to analyse the first 10 call-centre follow-up notes and extract structured information.

The workflow includes:
- Selecting the first 10 notes.
- Skipping blank notes.
- Sending non-empty notes to the Gemini API.
- Extracting structured reasons using a defined JSON schema.
- Validating responses using Pydantic.
- Comparing prompts for selected notes.
- Saving the structured results.
- Merging the extracted reasons with appointment information.

**Key findings:**

Nine readable notes were analysed. The main reason categories included:

- Forgetting or no reminder: 2
- Distance or transport: 2
- Work or schedule conflicts: 2

Both notes that mentioned forgetting were associated with appointments for which no reminder had been sent.

These findings provide useful examples of why patients miss appointments, although the small number of notes limits how broadly they can be generalised.

## Final Business Recommendations

Based on the combined findings from data analysis, SQL, machine learning, and GenAI, the following actions are recommended:

**1. Make appointment reminders a priority**

The analysis suggests that reminders are associated with lower no-show odds. In the logistic regression model, the estimated odds ratio for appointments with a reminder was approximately 0.31, holding other model features constant.

This is an association, not proof that reminders directly cause fewer no-shows. A controlled trial would be needed to establish causality.

**2. Prioritise long-lead appointments**

Appointments booked more than 30 days in advance have a substantially higher no-show rate. These bookings should receive additional reminders and follow-up attention.

**3. Use the risk model to support daily follow-ups**

The selected model can help staff identify higher-risk appointments. At the 0.35 threshold, 49 out of 198 test appointments were flagged, with a recall of 57.1%.

The front desk can use risk scores to prioritise an evening follow-up call list.

**4. Focus on clinics with higher no-show rates**

The analysis highlights the following clinics for closer monitoring:

- Gomti Nagar: 33.3% (90 appointments)
- Hadapsar: 27.3%
- Malviya Nagar: 26.8%

**5. Offer flexible alternatives**

For patients reporting distance or work-schedule difficulties, clinics can consider offering evening appointments, Saturday slots, or appointments at a nearer clinic where available.

## Repository Structure

```text
careloop-no-show-analysis/
│
├── data/
│   ├── appointments.csv
│   ├── clinics.csv
│   └── followup_notes.csv
│
├── 01_ingest_clean.ipynb
├── rejected_rows.json
├── appointments_clean.csv
├── clinics_enriched.csv
│
├── load_data.sql
├── 02_queries.sql
├── 02_sql_checks.ipynb
│
├── 03_model.ipynb
├── test_risk_scores.csv
│
├── 04_genai.ipynb
├── notes_analysed.csv
│
└── README.md
```

## Technologies Used

- **Python:** Data processing and analysis
- **Pandas and NumPy:** Data cleaning and feature engineering
- **SQL:** Data querying and analytical reporting
- **Scikit-learn:** Machine learning and model evaluation
- **Matplotlib / Seaborn:** Data visualisation
- **Gemini API:** Generative AI-based call-note analysis
- **Pydantic:** Structured output validation
- **Open-Meteo API:** Clinic weather enrichment
- **Jupyter Notebook:** Implementation and documentation
- **Git and GitHub:** Version control and project submission

## Running the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/hansikareddycheguri-ship-it/careloop-no-show-analysis.git
   cd careloop-no-show-analysis
   ```

2. Install the Python packages required by the notebooks. Refer to their import statements for the dependencies.

3. Run the notebooks in the following order:

   - `01_ingest_clean.ipynb`
   - `02_sql_checks.ipynb` (for SQL result verification)
   - `03_model.ipynb`
   - `04_genai.ipynb`

4. Execute `load_data.sql` to create and populate the SQL tables in your database, then run the queries in `02_queries.sql`.

5. For the GenAI section, provide a valid Gemini API key when prompted. The API key should not be committed to the repository.

Some generated CSV and SQL files are already included in the repository, so the notebooks can also be inspected through their saved outputs.

## Limitations

1. The call-note analysis uses only 10 notes, with 9 readable notes. This sample is too small to represent all no-show reasons across the eight clinics.
2. Data-cleaning statistics, including medians, quartiles, and outlier fences, were calculated using all 990 cleaned records before the train/test split. This creates a small possibility of data leakage.
3. The train/test split was random rather than time-based. The same patient may appear in both sets, which could make the evaluation results somewhat optimistic.
4. The data is observational. The relationship between reminders and no-shows does not establish causation.
5. The model should be treated as a decision-support tool rather than a replacement for clinic staff judgement.

## Conclusion

CareLoop's no-show problem can be approached through a combination of reliable data processing, analytical querying, predictive modelling, and AI-assisted information extraction.

The analysis identifies long booking lead times as an important risk factor, while the model provides a way to prioritise follow-ups. The call-note analysis adds context about possible reasons behind missed appointments.

The recommended starting point is to improve reminder coverage, prioritise long-lead and high-risk bookings, and use targeted follow-ups to reduce avoidable missed appointments.

---

**Project:** CareLoop Clinics — No-Show Guard  
**Repository:** [careloop-no-show-analysis](https://github.com/hansikareddycheguri-ship-it/careloop-no-show-analysis)
