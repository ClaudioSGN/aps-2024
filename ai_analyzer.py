import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import json

# Load the dataset from JSON
def load_dataset(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        df = pd.DataFrame(data)
        if 'label' in df:
            df['label'] = df['label'].apply(lambda x: 0 if x == 'good' else 1 if x == 'bad' else 2)
        return df

# Main function to preprocess, train, and evaluate
def train_and_evaluate(train_file):
    df_train = load_dataset(train_file)
    print("Label distribution:\n", df_train['label'].value_counts())

    if len(df_train['label'].unique()) < 2:
        print("Not enough classes to train a model. Please check the dataset.")
        return

    df_train['text'] = df_train['title'] + " " + df_train.get('introducao', '')
    X_train, X_test, y_train, y_test = train_test_split(df_train['text'], df_train['label'], test_size=0.2, random_state=42, stratify=df_train['label'])

    vectorizer = TfidfVectorizer()
    X_train_transformed = vectorizer.fit_transform(X_train)
    X_test_transformed = vectorizer.transform(X_test)

    qda = QuadraticDiscriminantAnalysis()
    qda.fit(X_train_transformed.toarray(), y_train)

    predictions = qda.predict(X_test_transformed.toarray())
    accuracy = accuracy_score(y_test, predictions)

    return qda, vectorizer

# Function to load new data and predict, saving percentages to JSON
def predict_new_data(model, vectorizer, new_data_file):
    df_new = load_dataset(new_data_file)
    df_new['text'] = df_new['title'] + " " + df_new.get('introducao', '')
    X_new_transformed = vectorizer.transform(df_new['text'])
    predictions = model.predict(X_new_transformed.toarray())
    df_new['predicted_label'] = ['good' if label == 0 else 'bad' for label in predictions]

    # Calculate percentages
    good_count = sum(df_new['predicted_label'] == 'good')
    bad_count = sum(df_new['predicted_label'] == 'bad')
    total = len(df_new)
    percentages = {
        "Good News Percentage": f"{good_count / total * 100:.2f}%",
        "Bad News Percentage": f"{bad_count / total * 100:.2f}%"
    }

    # Save to JSON
    with open('results.json', 'w', encoding='utf-8') as file:
        json.dump(percentages, file, ensure_ascii=False, indent=4)

# Paths to the datasets
train_data_file = 'news_data_train.json'  # Path to the training data
new_data_file = 'news_data.json'  # Path to the new, unlabeled data

# Train the model and get the vectorizer
model, vectorizer = train_and_evaluate(train_data_file)

# Predict on new data and save percentages to JSON
predict_new_data(model, vectorizer, new_data_file)
