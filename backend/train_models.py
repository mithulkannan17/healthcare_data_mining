import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    classification_report
)

from sklearn.cluster import KMeans

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

df = pd.read_csv(
    'data/indian_diseases_dataset.csv'
)

df = df.fillna('Unknown')

classification_df = df[[
    'age',
    'bmi',
    'region',
    'urban_rural',
    'smoking_status',
    'alcohol_use',
    'severity'
]].copy()

encoders = {}

for col in classification_df.columns:

    if classification_df[col].dtype != 'int64' and classification_df[col].dtype != 'float64':

        le = LabelEncoder()

        classification_df[col] = le.fit_transform(
            classification_df[col].astype(str)
        )

        encoders[col] = le

X = classification_df.drop(
    columns=['severity']
)

y = classification_df['severity']

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(

    X_scaled,
    y,

    test_size=0.2,

    random_state=42
)

knn = KNeighborsClassifier(
    n_neighbors=5
)

knn.fit(
    X_train,
    y_train
)

y_pred = knn.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    average='weighted'
)

recall = recall_score(
    y_test,
    y_pred,
    average='weighted'
)

print("\nKNN Classification Results\n")

print(f"Accuracy : {accuracy:.2f}")

print(f"Precision: {precision:.2f}")

print(f"Recall   : {recall:.2f}")

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        y_pred
    )
)

metrics = {

    'accuracy': round(accuracy * 100, 2),

    'precision': round(precision * 100, 2),

    'recall': round(recall * 100, 2)
}

joblib.dump(

    metrics,

    'models/model_metrics.pkl'
)

joblib.dump(
    knn,
    'models/knn_model.pkl'
)

joblib.dump(
    scaler,
    'models/scaler.pkl'
)

joblib.dump(
    encoders,
    'models/encoders.pkl'
)

cluster_df = df[[
    'age',
    'bmi',
    'smoking_status',
    'alcohol_use',
    'severity',
    'region',
    'disease_category'
]].copy()

cluster_visual_df = cluster_df.copy()

cluster_encoded_df = cluster_df.copy()

for col in cluster_encoded_df.columns:

    if cluster_encoded_df[col].dtype != 'int64' and cluster_encoded_df[col].dtype != 'float64':

        le = LabelEncoder()

        cluster_encoded_df[col] = le.fit_transform(
            cluster_encoded_df[col].astype(str)
        )

cluster_scaler = StandardScaler()

cluster_scaled = cluster_scaler.fit_transform(
    cluster_encoded_df
)

kmeans = KMeans(

    n_clusters=4,

    random_state=42,

    n_init=10
)

clusters = kmeans.fit_predict(
    cluster_scaled
)

cluster_visual_df['cluster'] = clusters

joblib.dump(
    kmeans,
    'models/kmeans_model.pkl'
)

cluster_visual_df.to_csv(
    'data/clustered_patients.csv',
    index=False
)

symptom_dummies = (
    df['symptoms']
    .str.get_dummies(sep=', ')
)

disease_dummies = pd.get_dummies(
    df['disease_category']
)

basket = pd.concat(
    [symptom_dummies, disease_dummies],
    axis=1
)

basket = basket.astype(bool)

frequent_items = apriori(

    basket,

    min_support=0.05,

    use_colnames=True
)

rules = association_rules(

    frequent_items,

    metric='confidence',

    min_threshold=0.6
)

rules = rules.sort_values(

    by='lift',

    ascending=False
)

joblib.dump(

    rules,

    'models/apriori_rules.pkl'
)

print("\nK-Means Clustering Complete\n")

print(cluster_df.head())

print("\nAssociation Rules Generated\n")

print(rules.head())