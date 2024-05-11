import pandas as pd #Importa a biblioteca pandas para manipulação de dados
from sklearn.feature_extraction.text import TfidfVectorizer #Importa o vetorizador TF-IDF para converter texto em um vetor numérico
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis #Importa o classificador Análise Discriminante Quadrática
from sklearn.model_selection import train_test_split #Importa função para dividir dados em conjuntos de treino e teste
from sklearn.metrics import accuracy_score #Importa função para calcular a acurácia de previsões
import json #Importa a biblioteca para manipulação de arquivos JSON

#Define função para carregar dados de um arquivo JSON
def load_dataset(filename):
    with open(filename, 'r', encoding='utf-8') as file: #Abre o arquivo JSON para leitura
        data = json.load(file) #Carrega os dados JSON
        df = pd.DataFrame(data) #Converte os dados em um DataFrame do pandas
        if 'label' in df: #Verifica se a coluna 'label' existe no DataFrame
            df['label'] = df['label'].apply(lambda x: 0 if x == 'good' else 1 if x == 'bad' else 2) #Codifica rótulos como números
        return df #Retorna o DataFrame processado

#Define função principal para preprocessamento e treinamento
def train_and_evaluate(train_file):
    df_train = load_dataset(train_file) #Carrega os dados de treinamento
    print("Label distribution:\n", df_train['label'].value_counts()) #Exibe a distribuição das classes

    if len(df_train['label'].unique()) < 2: #Checa se há pelo menos duas classes
        print("Not enough classes to train a model. Please check the dataset.") #Mensagem de erro se não houver classes suficientes
        return

    df_train['text'] = df_train['title'] + " " + df_train.get('introducao', '') #Combina títulos com introduções para formar o texto
    X_train, X_test, y_train, y_test = train_test_split(df_train['text'], df_train['label'], test_size=0.2, random_state=42, stratify=df_train['label']) #Divide os dados em conjuntos de treino e teste

    vectorizer = TfidfVectorizer() #Instancia o vetorizador TF-IDF
    X_train_transformed = vectorizer.fit_transform(X_train) #Transforma e ajusta o vetorizador ao conjunto de treino
    X_test_transformed = vectorizer.transform(X_test) #Transforma o conjunto de teste

    qda = QuadraticDiscriminantAnalysis() #Instancia o classificador QDA
    qda.fit(X_train_transformed.toarray(), y_train) #Treina o classificador no conjunto de treino

    predictions = qda.predict(X_test_transformed.toarray()) #Faz previsões no conjunto de teste
    accuracy = accuracy_score(y_test, predictions) #Calcula a acurácia das previsões

    return qda, vectorizer #Retorna o modelo treinado e o vetorizador

#Define função para predição em novos dados
def predict_new_data(model, vectorizer, new_data_file):
    df_new = load_dataset(new_data_file) #Carrega novos dados
    df_new['text'] = df_new['title'] + " " + df_new.get('introducao', '') #Prepara o texto
    X_new_transformed = vectorizer.transform(df_new['text']) #Transforma o texto
    predictions = model.predict(X_new_transformed.toarray()) #Faz previsões
    df_new['predicted_label'] = ['good' if label == 0 else 'bad' for label in predictions] #Decodifica previsões para 'good(bom)' ou 'bad(ruim)'

    #Calcula e salva as porcentagens de notícias boas e ruins
    good_count = sum(df_new['predicted_label'] == 'good')
    bad_count = sum(df_new['predicted_label'] == 'bad')
    total = len(df_new)
    percentages = {
        "Noticias Boas": f"{good_count / total * 100:.2f}%",
        "Noticias Ruins": f"{bad_count / total * 100:.2f}%"
    }
    with open('results.json', 'w', encoding='utf-8') as file:
        json.dump(percentages, file, ensure_ascii=False, indent=4)

#Define os caminhos dos arquivos de dados
train_data_file = 'news_data_train.json' #Arquivo de treino
new_data_file = 'news_data.json' #Arquivo de novos dados

#Treina o modelo e obtém o vetorizador
model, vectorizer = train_and_evaluate(train_data_file)

#Prediz e salva as porcentagens de novas notícias
predict_new_data(model, vectorizer, new_data_file)


#Este código faz a classificação automática de notícias como "boas" ou "ruins"
#usando machine learning. Utilizando a biblioteca 'pandas' para lidar com os dados,
#a biblioteca, 'TfidfVectorizer' para transformar os textos em vetores numéricos e
# o modelo 'QDA' para fazer a classificação. Já a função 'load_dataset' carrega e organiza
#os dados de um arquivo JSON em um DataFrame, convertendo rótulos em números.
#A 'train_and_evaluate' treina o modelo com esses dados, aplica TF-IDF e 
#verifica a precisão. A função 'predict_new_data' utiliza o modelo para classificar novas
#notícias e calcula a porcentagem de notícias "boas" e "ruins", salvando tudo em um JSON.
#Este código automatiza a coleta e análise de notícias, tornando fácil acompanhar tendências de conteúdo.