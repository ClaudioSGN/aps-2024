import pandas as pd  # Importa a biblioteca pandas para manipulação de dados
import json  # Importa a biblioteca json para carregar e salvar dados em formato JSON
import re  # Importa a biblioteca de expressões regulares para limpeza de texto
from sklearn.feature_extraction.text import TfidfVectorizer  # Importa o vetorizador TF-IDF para conversão de texto em vetor
from sklearn.decomposition import TruncatedSVD  # Importa SVD truncado para redução de dimensionalidade
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis  # Importa LDA para análise discriminante linear
from sklearn.model_selection import train_test_split  # Importa função para dividir dados em treino e teste
from sklearn.pipeline import make_pipeline  # Importa função para criar pipelines de processamento
from sklearn.metrics import accuracy_score  # Importa função para calcular a acurácia da predição

# Função para carregar dataset a partir de um arquivo JSON
def load_dataset(filename):
    with open(filename, 'r', encoding='utf-8') as file:  # Abre o arquivo JSON
        data = json.load(file)  # Carrega os dados do arquivo JSON
        df = pd.DataFrame(data)  # Converte os dados para um DataFrame do pandas
        if 'label' in df:  # Verifica se a coluna 'label' existe
            # Converte os labels para valores numéricos: 'good' -> 0, 'bad' -> 1, outros -> 2
            df['label'] = df['label'].apply(lambda x: 0 if x == 'good' else 1 if x == 'bad' else 2)
        return df  # Retorna o DataFrame

# Função para limpar o texto
def clean_text(text):
    text = re.sub(r'\W', ' ', str(text))  # Remove caracteres não alfanuméricos
    text = text.lower()  # Converte o texto para minúsculas
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)  # Remove palavras isoladas de uma letra
    text = re.sub(r'\s+', ' ', text, flags=re.I)  # Remove espaços extras
    return text  # Retorna o texto limpo

# Função para treinar e avaliar o modelo
def train_and_evaluate(dataset_path):
    df_train = load_dataset(dataset_path)  # Carrega o dataset de treino
    # Cria uma nova coluna 'text' combinando 'title' e 'introducao'
    df_train['text'] = df_train['title'] + " " + df_train.get('introducao', '')
    df_train['text'] = df_train['text'].apply(clean_text)  # Aplica limpeza no texto
    if len(df_train['label'].unique()) < 2:  # Verifica se há pelo menos duas classes para treinamento
        print("Insufficient classes for training.")  # Imprime mensagem de erro se houver classes insuficientes
        return None  # Retorna None
    # Divide o dataset em treino e teste
    x_train, x_test, y_train, y_test = train_test_split(df_train['text'], df_train['label'], test_size=0.2,
                                                        random_state=42, stratify=df_train['label'])
    tfidf_vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))  # Cria um vetorizador TF-IDF
    svd = TruncatedSVD(n_components=100)  # Cria um transformador SVD truncado
    lda = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')  # Cria um classificador LDA
    clf = make_pipeline(tfidf_vectorizer, svd, lda)  # Cria um pipeline com as etapas acima
    clf.fit(x_train, y_train)  # Treina o modelo com os dados de treino
    predictions = clf.predict(x_test)  # Realiza previsões com os dados de teste
    accuracy = accuracy_score(y_test, predictions)  # Calcula a acurácia das previsões
    print(f"Accuracy: {accuracy}")  # Imprime a acurácia
    return clf  # Retorna o modelo treinado

# Função para prever novos dados e salvar os resultados
def predict_new_data(model, analysis_data_path, result_filename, news_filename):
    df_new = load_dataset(analysis_data_path)  # Carrega o novo dataset para análise
    # Cria uma nova coluna 'text' combinando 'title' e 'introducao'
    df_new['text'] = df_new['title'] + " " + df_new.get('introducao', '')
    df_new['text'] = df_new['text'].apply(clean_text)  # Aplica limpeza no texto
    predictions = model.predict(df_new['text'])  # Faz previsões com o modelo treinado
    # Adiciona as previsões ao DataFrame
    df_new['predicted_label'] = ['good' if label == 0 else 'bad' for label in predictions]
    # Cria uma lista de dicionários com título e previsão
    detailed_results = [{'title': row['title'], 'prediction': row['predicted_label']} for index, row in
                        df_new.iterrows()]
    good_count = sum(df_new['predicted_label'] == 'good')  # Conta o número de previsões 'good'
    bad_count = sum(df_new['predicted_label'] == 'bad')  # Conta o número de previsões 'bad'
    total = len(df_new)  # Conta o total de previsões
    # Calcula as porcentagens de previsões 'good' e 'bad'
    percentages = {"Boas": f"{good_count / total * 100:.2f}%", "Ruins": f"{bad_count / total * 100:.2f}%"}
    # Salva as porcentagens em um arquivo JSON
    with open(result_filename, 'w', encoding='utf-8') as file:
        json.dump(percentages, file, ensure_ascii=False, indent=4)
    # Salva os resultados detalhados em um arquivo JSON
    with open(news_filename, 'w', encoding='utf-8') as file:
        json.dump(detailed_results, file, ensure_ascii=False, indent=4)

# Caminho do arquivo de dados de treino
train_data_file_path = 'json/news_data_train.json'
trained_model = train_and_evaluate(train_data_file_path)  # Treina o modelo com os dados de treino
if trained_model:  # Verifica se o modelo foi treinado com sucesso
    for i in range(1, 6):  # Itera de 1 a 5
        file_name = f'json/dia{i}.json'  # Gera o nome do arquivo de entrada
        result_file_name = f'json/dia{i}result.json'  # Gera o nome do arquivo de saída de resultados
        news_file_name = f'json/dia{i}news.json'  # Gera o nome do arquivo de saída de notícias
        # Realiza previsões para os novos dados e salva os resultados
        predict_new_data(trained_model, file_name, result_file_name, news_file_name)

    # Realiza previsões para o arquivo news_data.json e salva os resultados
    predict_new_data(trained_model, 'json/news_data.json', 'json/results.json', 'json/results_prediction.json')
