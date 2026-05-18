import pandas as pd
from flask import Flask, render_template, request
from preprocess import load_dataset
import joblib

app = Flask(__name__)

df = load_dataset()

rules_df = joblib.load(
    'models/apriori_rules.pkl'
)

clustered_df = pd.read_csv(
    'data/clustered_patients.csv'
)

@app.route('/')
def dashboard():

    total_patients = len(df)

    high_risk_cases = len(
        df[df['severity'] == 'Severe']
    )

    disease_categories = df['disease_category'].nunique()

    states_covered = df['state'].nunique()

    disease_counts = (
        df['disease_category']
        .value_counts()
        .to_dict()
    )

    severity_counts = (
        df['severity']
        .value_counts()
        .to_dict()
    )

    region_disease_map = (

        df.groupby(['region', 'disease_category'])
        .size()
        .unstack(fill_value=0)

    )

    return render_template(

        'dashboard.html',

        total_patients=total_patients,

        high_risk_cases=high_risk_cases,

        disease_categories=disease_categories,

        states_covered=states_covered,

        disease_counts=disease_counts,

        severity_counts=severity_counts,

        region_disease_map=
        region_disease_map.to_dict()
    )

@app.route('/risk-checker')
def risk_checker():

    return render_template(
        'risk_checker.html',
        prediction=None
    )

@app.route('/predict', methods=['POST'])
def predict():

    age = int(request.form['age'])

    bmi = float(request.form['bmi'])

    region = request.form['region']

    urban_rural = request.form['urban_rural']

    smoking_status = request.form['smoking_status']

    alcohol_use = request.form['alcohol_use']

    comorbidity = request.form['comorbidity']

    season = request.form['season']

    symptoms = request.form['symptoms'].lower()

    risk_score = 0

    explanations = []

    predicted_disease = "General Infection"

    disease_category = "Infectious"

    if (
        'vomiting' in symptoms and
        'fever' in symptoms
    ):

        predicted_disease = "Diarrhea"

        disease_category = "Waterborne"

    elif (
        'rash' in symptoms and
        'joint pain' in symptoms
    ):

        predicted_disease = "Chikungunya"

        disease_category = "Vector-Borne"

    elif (
        'chest pain' in symptoms and
        'shortness of breath' in symptoms
    ):

        predicted_disease = "Hypertension"

        disease_category = "Chronic"

    if age >= 60:

        risk_score += 2

        explanations.append(
            "Elderly patients have higher severe outcome probability."
        )

    if bmi >= 30:

        risk_score += 2

        explanations.append(
            "High BMI increases chronic disease complications."
        )

    if smoking_status == 'Current':

        risk_score += 2

        explanations.append(
            "Smoking history increases respiratory and cardiac risk."
        )

    if alcohol_use == 'Regular':

        risk_score += 1

        explanations.append(
            "Regular alcohol consumption increases treatment complexity."
        )

    if comorbidity != 'None':

        risk_score += 2

        explanations.append(
            f"Existing comorbidity detected: {comorbidity}."
        )

    if (
        region == 'East' and
        season == 'Monsoon'
    ):

        risk_score += 2

        explanations.append(
            "Eastern monsoon regions show high waterborne disease frequency."
        )

    if urban_rural == 'Rural':

        risk_score += 1

        explanations.append(
            "Rural healthcare access limitations may delay treatment."
        )

    similar_patients = df[
        df['disease_category'] == disease_category
    ]

    matched_count = len(similar_patients)

    severe_count = len(

        similar_patients[
            similar_patients['severity'] == 'Severe'
        ]
    )

    severe_percentage = 0

    if matched_count > 0:

        severe_percentage = round(

            (
                severe_count / matched_count
            ) * 100,

            1
        )

        if severe_percentage >= 60:

            risk_score += 2

        elif severe_percentage >= 40:

            risk_score += 1

    explanations.append(
        f"Matched {matched_count} historical patients from dataset."
    )

    explanations.append(
        f"{severe_percentage}% of similar patients had Severe outcomes."
    )

    cluster_profile = "Urban Low-Risk Group"

    if (
        region == 'East' and
        urban_rural == 'Rural'
    ):

        cluster_profile = "Rural Severe Waterborne Cluster"

    elif (
        bmi >= 30 and
        smoking_status == 'Current'
    ):

        cluster_profile = "Chronic Lifestyle Risk Cluster"

    if risk_score >= 7:

        severity = "Severe"

        risk_level = "HIGH RISK"

        treatment = (
            "Immediate hospitalization and diagnostic testing recommended."
        )

        hospitalization = "Hospitalization Required"

    elif risk_score >= 4:

        severity = "Moderate"

        risk_level = "MEDIUM RISK"

        treatment = (
            "Clinical monitoring and specialist consultation recommended."
        )

        hospitalization = "Medical Observation Recommended"

    else:

        severity = "Mild"

        risk_level = "LOW RISK"

        treatment = (
            "Standard treatment and preventive care recommended."
        )

        hospitalization = "Home Care Possible"

    return render_template(

        'risk_checker.html',

        prediction={

            'risk_level': risk_level,

            'severity': severity,

            'predicted_disease': predicted_disease,

            'disease_category': disease_category,

            'treatment': treatment,

            'hospitalization': hospitalization,

            'cluster_profile': cluster_profile,

            'explanations': explanations
        }
    )

@app.route('/rules')
def rules():

    top_rules = []

    for _, row in rules_df.head(20).iterrows():

        top_rules.append({

            'antecedents': ', '.join(
                list(row['antecedents'])
            ),

            'consequents': ', '.join(
                list(row['consequents'])
            ),

            'support': round(row['support'], 2),

            'confidence': round(row['confidence'], 2),

            'lift': round(row['lift'], 2)
        })

    return render_template(
        'rules.html',
        rules=top_rules
    )

@app.route('/clusters')
def clusters():

    cluster_profiles = []

    unique_clusters = sorted(
        clustered_df['cluster'].unique()
    )

    for cluster_id in unique_clusters:

        cluster_data = clustered_df[
            clustered_df['cluster'] == cluster_id
        ]

        avg_age = round(
            cluster_data['age'].mean(),
            1
        )

        avg_bmi = round(
            cluster_data['bmi'].mean(),
            1
        )

        dominant_disease = (
            cluster_data['disease_category']
            .mode()[0]
        )

        dominant_region = (
            cluster_data['region']
            .mode()[0]
        )

        severe_percentage = round(

            (
                len(
                    cluster_data[
                        cluster_data['severity'] == 'Severe'
                    ]
                )

                /

                len(cluster_data)

            ) * 100,

            1
        )

        if severe_percentage >= 60:

            risk_level = "HIGH RISK"

        elif severe_percentage >= 35:

            risk_level = "MEDIUM RISK"

        else:

            risk_level = "LOW RISK"

        cluster_profiles.append({

            'cluster_id': cluster_id,

            'patient_count': len(cluster_data),

            'avg_age': avg_age,

            'avg_bmi': avg_bmi,

            'dominant_disease': dominant_disease,

            'dominant_region': dominant_region,

            'severe_percentage': severe_percentage,

            'risk_level': risk_level
        })

    age_severity = (
        clustered_df
        .groupby('severity')['age']
        .mean()
        .to_dict()
    )

    smoking_severity = (
        clustered_df
        .groupby(['smoking_status', 'severity'])
        .size()
        .unstack(fill_value=0)
        .to_dict()
    )

    alcohol_severity = (
        clustered_df
        .groupby(['alcohol_use', 'severity'])
        .size()
        .unstack(fill_value=0)
        .to_dict()
    )

    region_disease = (
        clustered_df
        .groupby(['region', 'disease_category'])
        .size()
        .unstack(fill_value=0)
        .to_dict()
    )

    return render_template(

        'clusters.html',

        clusters=cluster_profiles,

        age_severity=age_severity,

        smoking_severity=smoking_severity,

        alcohol_severity=alcohol_severity,

        region_disease=region_disease
    )

if __name__ == '__main__':

    app.run(debug=True)