import os

def run_script(script_name):
    os.system(f"python {script_name}")

if __name__ == "__main__":
    # Rodar noticias.py
    run_script("noticias.py")

    # Rodar ai_analyzer.py
    run_script("ai_analyzer.py")

    # Rodar testgraphic.py
    run_script("testgraphic.py")


#Este código é responsável apenas pela utilização correta do todo.
#Utilizando apenas este é possível rodar todo o código pois ele
#"automatiza" os códigos abrindo um por um em sua ordem.