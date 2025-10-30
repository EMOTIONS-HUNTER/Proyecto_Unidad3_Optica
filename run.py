import subprocess
import os

def run_Streamlit():
    script_path = os.path.join(os.path.dirname(__file__), "main.py") 
    subprocess.run(["streamlit", "run", script_path])
    
if __name__ == "__main__":
    run_Streamlit()
