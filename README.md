O arquivo noticias.py é responsável por realizar o webscraping das notícias nos sites: G1, BBC, CNN e Exame. Após serem puxadas, o código também gera um arquivo em .JSON que posteriormente é lido pelo arquivo ai_analyzer.py.

O arquivo ai_analyzer.py é responsável por treinar a "I.A." utilizando a biblioteca Sklearn e utilizando um arquivo de notícias ficticias utilizadas apenas para o treinamento da I.A., após o treinamento a I.A. lê o arquivo .JSON que foi gerado no arquivo noticias.py, 
classifica a notícia lida como boa ou ruim e gera um arquivo em .JSON com a porcentagem de notícias ruins e notícias boas que foram lidas.

O arquivo testgraphic.py é responsável apenas por captar as informações geradas no arquivo .JSON do código ai_analyzer.py e representar a porcentagem gerada de notícias boas e ruins em um gráfico.

O arquivo main.py é responsável únicamente por iniciar os arquivos na ordem correta e de forma "automática" para que não seja necessário abrir um por um.
