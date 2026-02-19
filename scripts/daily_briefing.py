
import os
import sys
import subprocess

def main():
    webhook_url = os.environ.get("FEISHU_WEBHOOK_URL")
    if len(sys.argv) > 1:
        webhook_url = sys.argv[1]
    
    if not webhook_url:
        print("Error: FEISHU_WEBHOOK_URL env var or argument required.")
        return

    print("--- Starting Daily Briefing ---")
    
    # 1. Fetch News
    print("1. Fetching news...")
    subprocess.run(["python3", "scripts/fetch_news.py"], check=True)
    
    # 2. Push to Feishu
    print("2. Pushing to Feishu...")
    subprocess.run(["python3", "scripts/push_feishu.py", webhook_url], check=True)
    
    print("--- Briefing Complete ---")

if __name__ == "__main__":
    main()
