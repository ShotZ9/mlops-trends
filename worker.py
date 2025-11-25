import time
import subprocess

def safe_run(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)

if __name__ == "__main__":
    while True:
        print("=== Running hourly trends scraping ===")
        
        safe_run(["dvc", "pull", "-r", "b2remote"])
        safe_run(["dvc", "repro"])
        safe_run(["dvc", "push", "-r", "b2remote"])

        print("=== Done. Sleeping 24 hour ===")
        time.sleep(3600 * 24)
