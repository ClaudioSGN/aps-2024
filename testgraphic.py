import tkinter as tk  # Importa a biblioteca tkinter para criar interfaces gráficas
import matplotlib.pyplot as plt  # Importa a biblioteca matplotlib para criação de gráficos
import json  # Importa a biblioteca json para carregar e salvar dados em formato JSON
import socket  # Importa a biblioteca socket para manipulação de protocolos de rede
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Importa backend do matplotlib para integração com tkinter

# Função para carregar dados a partir de um arquivo JSON
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:  # Garante a codificação UTF-8
        data = json.load(file)  # Carrega os dados do arquivo JSON
    labels = list(data.keys())  # Extrai as chaves do JSON como labels
    sizes = [float(result[:-1]) for result in data.values()]  # Converte os valores do JSON em tamanhos de fatia
    return labels, sizes  # Retorna labels e tamanhos

# Função para exibir notícias do arquivo de resultado
def display_result_news(news_filename):
    news_window = tk.Toplevel(window)  # Cria uma nova janela
    news_window.title(f"Novos detalhes para: {news_filename}")  # Define o título da nova janela
    text_widget = tk.Text(news_window, wrap='word', height=20, width=80)  # Cria um widget de texto
    try:
        with open(news_filename, 'r', encoding='utf-8') as file:  # Garante a codificação UTF-8
            news_data = json.load(file)  # Carrega os dados do arquivo JSON
        if 'details' in news_data:  # Verifica se a chave 'details' está presente
            for article in news_data['details']:  # Itera sobre os artigos em 'details'
                title = article.get('title', 'Sem títulos disponíveis')  # Obtém o título do artigo
                prediction = article.get('prediction', 'Indisponível')  # Obtém a previsão do artigo
                text_widget.insert(tk.END, f"Título: {title}\nPrevisão: {prediction}\n\n")  # Insere o artigo no widget de texto
        else:
            text_widget.insert(tk.END, f"Key 'details' not found in the JSON data\n")  # Mensagem de erro se 'details' não estiver presente
    except Exception as e:
        text_widget.insert(tk.END, f"Falha em carregar as notícias parseadas: {e}\n")  # Mensagem de erro se a leitura falhar
    text_widget.config(state='disabled')  # Desabilita o widget de texto para edição
    text_widget.pack()  # Adiciona o widget de texto à janela

# Função para exibir notícias do arquivo de notícias
def display_news(news_filename):
    news_window = tk.Toplevel(window)  # Cria uma nova janela
    news_window.title(f"Novos detalhes para: {news_filename}")  # Define o título da nova janela
    text_widget = tk.Text(news_window, wrap='word', height=20, width=80)  # Cria um widget de texto
    try:
        with open(news_filename, 'r', encoding='utf-8') as file:  # Garante a codificação UTF-8
            news_data = json.load(file)  # Carrega os dados do arquivo JSON
        for article in news_data:  # Itera sobre os artigos no JSON
            title = article.get('title', 'Sem títulos disponíveis')  # Obtém o título do artigo
            prediction = article.get('prediction', 'No prediction available')  # Obtém a previsão do artigo
            text_widget.insert(tk.END, f"Title: {title}\nPrediction: {prediction}\n\n")  # Insere o artigo no widget de texto
    except Exception as e:
        text_widget.insert(tk.END, f"Falha em carregar as notícias parseadas: {e}\n")  # Mensagem de erro se a leitura falhar
    text_widget.config(state='disabled')  # Desabilita o widget de texto para edição
    text_widget.pack()  # Adiciona o widget de texto à janela

# Função para exibir notícias do arquivo results_prediction.json
def display_general_news(news_filename='json/results_prediction.json'):
    news_window = tk.Toplevel(window)  # Cria uma nova janela
    news_window.title(f"Novos detalhes para: {news_filename}")  # Define o título da nova janela
    text_widget = tk.Text(news_window, wrap='word', height=20, width=80)  # Cria um widget de texto
    try:
        with open(news_filename, 'r', encoding='utf-8') as file:  # Garante a codificação UTF-8
            news_data = json.load(file)  # Carrega os dados do arquivo JSON
        for article in news_data:  # Itera sobre os artigos no JSON
            title = article.get('title', 'Sem títulos disponíveis')  # Obtém o título do artigo
            prediction = article.get('prediction', 'No prediction available')  # Obtém a previsão do artigo
            text_widget.insert(tk.END, f"Title: {title}\nPrediction: {prediction}\n\n")  # Insere o artigo no widget de texto
    except Exception as e:
        text_widget.insert(tk.END, f"Falha em carregar as notícias parseadas: {e}\n")  # Mensagem de erro se a leitura falhar
    text_widget.config(state='disabled')  # Desabilita o widget de texto para edição
    text_widget.pack()  # Adiciona o widget de texto à janela

# Função para criar um gráfico de pizza
def create_pie_chart(labels, sizes, title):
    fig, ax = plt.subplots()  # Cria uma figura e um eixo
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)  # Cria o gráfico de pizza
    ax.axis('equal')  # Garante que o gráfico de pizza seja desenhado como um círculo
    plt.title(title)  # Define o título do gráfico
    return fig  # Retorna a figura

# Função para lidar com o clique no botão para mostrar resultados
def show_results(filename, canvas_container, news_file=None):
    # Limpa o gráfico anterior e fecha a figura anterior para evitar vazamento de memória
    for widget in canvas_container.winfo_children():
        widget.destroy()
    plt.close('all')  # Fecha todas as figuras para liberar memória

    labels, sizes = load_data(filename)  # Carrega os dados do arquivo
    fig = create_pie_chart(labels, sizes, "Analysis Results")  # Cria o gráfico de pizza
    canvas = FigureCanvasTkAgg(fig, master=canvas_container)  # Cria um canvas para o gráfico
    canvas.draw()  # Desenha o gráfico no canvas
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)  # Adiciona o canvas ao contêiner

    # Determina qual arquivo usar para exibir as notícias
    if not news_file:
        news_file = filename.replace('result', 'news')  # Substitui 'result' por 'news' no nome do arquivo

    # Cria um sub-botão para notícias
    if 'dia' in filename:
        news_btn = tk.Button(canvas_container, text="Mostrar notícias", command=lambda: display_news(news_file))
    else:
        news_btn = tk.Button(canvas_container, text="Mostrar notícias", command=lambda: display_general_news())

    news_btn.pack(side=tk.BOTTOM, pady=5)  # Adiciona o botão ao contêiner

# Função para exibir protocolo de rede
def display_network_protocol():
    protocol_window = tk.Toplevel(window)  # Cria uma nova janela
    protocol_window.title("Network Protocol")  # Define o título da nova janela
    text_widget = tk.Text(protocol_window, wrap='word', height=10, width=50)  # Cria um widget de texto
    text_widget.insert(tk.END, "Network Protocols:\n")  # Insere o texto inicial no widget

    try:
        # Cria um socket TCP
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        text_widget.insert(tk.END, "TCP socket created successfully.\n")  # Insere mensagem de sucesso

        # Cria um socket UDP
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        text_widget.insert(tk.END, "UDP socket created successfully.\n")  # Insere mensagem de sucesso

        # Obtém o nome do host e imprime
        hostname = socket.gethostname()
        text_widget.insert(tk.END, f"Hostname: {hostname}\n")  # Insere o nome do host

        # Obtém o endereço IP do host
        ip_address = socket.gethostbyname(hostname)
        text_widget.insert(tk.END, f"IP Address: {ip_address}\n")  # Insere o endereço IP

    except socket.error as e:
        text_widget.insert(tk.END, f"Socket error: {e}\n")  # Insere mensagem de erro

    text_widget.config(state='disabled')  # Desabilita o widget de texto para edição
    text_widget.pack()  # Adiciona o widget de texto à janela

# Cria a janela principal
window = tk.Tk()
window.title("Resultados")  # Define o título da janela

# Frame para botões
button_frame = tk.Frame(window)
button_frame.pack(side=tk.LEFT, fill=tk.Y)  # Posiciona o frame à esquerda

# Frame para canvas
canvas_frame = tk.Frame(window)
canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # Posiciona o frame à direita

# Gera botões dinamicamente com base nos nomes dos arquivos
file_names = [f"json/dia{i}result.json" for i in range(1, 6)] + ['json/results.json']
button_labels = [f"Dia {i}" for i in range(1, 6)] + ["Resultados Gerais"]
news_files = [f"json/dia{i}news.json" for i in range(1, 6)] + ['json/results_prediction.json']  # Arquivo de notícias específico para "Resultados Gerais"

for file_name, label, news_file in zip(file_names, button_labels, news_files):
    btn = tk.Button(button_frame, text=label,
                    command=lambda f=file_name, c=canvas_frame, n=news_file: show_results(f, c, n))
    btn.pack(side=tk.TOP, padx=10, pady=10)  # Adiciona o botão ao frame

# Adiciona botão para exibir protocolo de rede
network_btn = tk.Button(button_frame, text="Mostrar Protocolo de Rede", command=display_network_protocol)
network_btn.pack(side=tk.TOP, padx=10, pady=10)  # Adiciona o botão ao frame

window.mainloop()  # Inicia o loop principal da aplicação
