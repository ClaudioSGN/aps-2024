import pandas as pd  #Importa a biblioteca Pandas para manipulação e análise de dados.
import json  #Importa a biblioteca JSON para trabalhar com dados no formato JSON.
import re  #Importa a biblioteca de expressões regulares para manipulação de texto.
from sklearn.feature_extraction.text import TfidfVectorizer  #Importa o vetorizador TF-IDF, utilizado para converter texto em uma matriz de características TF-IDF.
from sklearn.decomposition import TruncatedSVD  #Importa TruncatedSVD, usado para redução de dimensionalidade em dados esparsos.
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis  #Importa Análise Discriminante Linear (LDA) para classificação.
from sklearn.model_selection import train_test_split  #Importa função para dividir os dados em conjuntos de treino e teste.
from sklearn.pipeline import make_pipeline  #Importa função para criar um pipeline de transformações e um estimador final.
from sklearn.metrics import accuracy_score  #Importa função para calcular a acurácia da classificação.

def load_dataset(filename):
    with open(filename, 'r', encoding='utf-8') as file:  #Abre o arquivo no modo de leitura.
        data = json.load(file)  #Carrega os dados do arquivo JSON.
        df = pd.DataFrame(data)  #Converte os dados carregados em um DataFrame do Pandas.
        if 'label' in df:  #Verifica se a coluna 'label' existe no DataFrame.
            df['label'] = df['label'].apply(lambda x: 0 if x == 'good' else 1 if x == 'bad' else 2)  #Transforma as labels 'good' e 'bad' em números.
        return df  #Retorna o DataFrame processado.

def clean_text(text):
    text = re.sub(r'\W', ' ', str(text))  #Remove caracteres não-alfanuméricos do texto.
    text = text.lower()  #Converte o texto para minúsculas.
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)  #Remove caracteres isolados.
    text = re.sub(r'\s+', ' ', text, flags=re.I)  #Substitui múltiplos espaços por um único espaço.
    return text  #Retorna o texto limpo.

def train_and_evaluate(dataset_path):
    df_train = load_dataset(dataset_path)  #Carrega o dataset.
    df_train['text'] = df_train['title'] + " " + df_train.get('introducao', '')  #Combina título e introdução em uma única coluna de texto.
    df_train['text'] = df_train['text'].apply(clean_text)  #Aplica a limpeza de texto.

    print("Label distribution:\n", df_train['label'].value_counts())  #Exibe a distribuição das labels.
    if len(df_train['label'].unique()) < 2:
        print("Não há classes suficientes para treinar o modelo. Por favor cheque o dataset.")  #Verifica se há pelo menos duas classes.
        return

    x_train, x_test, y_train, y_test = train_test_split(df_train['text'], df_train['label'], test_size=0.2, random_state=42, stratify=df_train['label'])  #Divide os dados em treino e teste.

    tfidf_vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))  #Cria um vetorizador TF-IDF.
    svd = TruncatedSVD(n_components=100)  #Configura SVD para redução de dimensionalidade.
    lda = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')  #Configura a Análise Discriminante Linear.

    #Cria um pipeline com vetorização, SVD e LDA.
    clf = make_pipeline(tfidf_vectorizer, svd, lda)
    clf.fit(x_train, y_train)  #Treina o modelo nos dados de treino.

    predictions = clf.predict(x_test)  #Faz previsões no conjunto de teste.
    accuracy = accuracy_score(y_test, predictions)  #Calcula a acurácia das previsões.
    print("Accuracy:", accuracy)  #Exibe a acurácia.

    return clf  #Retorna o modelo treinado.

def predict_new_data(model, analysis_data_path):
    df_new = load_dataset(analysis_data_path)  #Carrega novos dados para análise.
    df_new['text'] = df_new['title'] + " " + df_new.get('introducao', '')  #Prepara o texto.
    df_new['text'] = df_new['text'].apply(clean_text)  #Limpa o texto.

    predictions = model.predict(df_new['text'])  #Faz previsões com o modelo.
    df_new['predicted_label'] = ['good' if label == 0 else 'bad' for label in predictions]  #Traduz as previsões numéricas para 'good' ou 'bad'.

    good_count = sum(df_new['predicted_label'] == 'good')  #Conta quantas notícias são boas.
    bad_count = sum(df_new['predicted_label'] == 'bad')  #Conta quantas notícias são ruins.
    total = len(df_new)  #Calcula o total de notícias analisadas.
    percentages = {
        "Noticias Boas": f"{good_count / total * 100:.2f}%",  #Calcula a porcentagem de notícias boas.
        "Noticias Ruins": f"{bad_count / total * 100:.2f}%"  #Calcula a porcentagem de notícias ruins.
    }
    with open('results.json', 'w', encoding='utf-8') as file:  #Abre um arquivo para salvar os resultados.
        json.dump(percentages, file, ensure_ascii=False, indent=4)  #Salva os resultados em formato JSON.

#Caminhos para os arquivos de dados.
train_data_file_path = 'news_data_train.json'
analysis_data_path = 'news_data.json'

#Treina o modelo e faz previsões.
trained_model = train_and_evaluate(train_data_file_path)
predict_new_data(trained_model, analysis_data_path)
