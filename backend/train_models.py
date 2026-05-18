import pandas as pd
import joblib

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

from kmodes.kprototypes import KPrototypes

from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

df = pd.read_csv(
    'data/indian_diseases_dataset.csv'
)

df['symptoms'] = df['symptoms'].fillna('')

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

cluster_df = df[[
    'age',
    'bmi',
    'gender',
    'region',
    'urban_rural',
    'disease_category',
    'smoking_status',
    'alcohol_use',
    'severity'
]].copy()

cluster_df = cluster_df.fillna('Unknown')

for col in cluster_df.columns:

    if cluster_df[col].dtype == 'object':

        cluster_df[col] = cluster_df[col].astype(str)

cluster_matrix = cluster_df.to_numpy()

categorical_columns = [2, 3, 4, 5, 6, 7, 8]

kproto = KPrototypes(
    n_clusters=4,
    init='Huang',
    verbose=1,
    random_state=42
)

clusters = kproto.fit_predict(
    cluster_matrix,
    categorical=categorical_columns
)

cluster_df['cluster'] = clusters

visual_df = cluster_df.copy()

encoders = {}

for col in visual_df.columns:

    if visual_df[col].dtype != 'int64' and visual_df[col].dtype != 'float64':

        le = LabelEncoder()

        visual_df[col] = le.fit_transform(
            visual_df[col].astype(str)
        )

        encoders[col] = le

scaled_features = StandardScaler().fit_transform(
    visual_df.drop(columns=['cluster'])
)

pca = PCA(n_components=2)

pca_result = pca.fit_transform(
    scaled_features
)

cluster_df['pca1'] = pca_result[:, 0]

cluster_df['pca2'] = pca_result[:, 1]

joblib.dump(
    kproto,
    'models/kprototypes.pkl'
)

cluster_df.to_csv(
    'data/clustered_patients.csv',
    index=False
)

print("K-Prototypes Clustering Complete")
print(cluster_df.head())

print("Association Rules Generated")
print(rules.head())