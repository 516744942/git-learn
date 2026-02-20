import os
import sys
# 确保可以导入同目录下的脚本
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fetch_news import generate_briefing
from push_feishu import push_to_feishu

def main():
    webhook_url = os.environ.get("FEISHU_WEBHOOK_URL")
    if len(sys.argv) > 1:
        webhook_url = sys.argv[1]
    
    if not webhook_url:
        print("Error: FEISHU_WEBHOOK_URL env var or argument required.")
        return

    print("--- Starting Daily Briefing ---")
    
    # 1. 直接在内存中生成简报
    print("1. Fetching news...")
    report = generate_briefing()
    
    # 2. 直接推送简报内容
    print("2. Pushing to Feishu...")
    push_to_feishu(report, webhook_url)
    
    print("--- Briefing Complete ---")

if __name__ == "__main__":
    main()
