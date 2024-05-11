import os

# Ensure that all scripts are in the same directory as the main script or adjust the path accordingly.

def run_script(script_name):
    os.system(f"python {script_name}")

if __name__ == "__main__":
    # Run noticias.py
    run_script("noticias.py")

    # Run ai_analyzer.py
    run_script("ai_analyzer.py")

    # Run testgraphic.py
    run_script("testgraphic.py")
