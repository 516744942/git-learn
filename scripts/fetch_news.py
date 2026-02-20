import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup

def fetch_huggingface_daily_papers():
    """Fetch top papers from Hugging Face Daily Papers API."""
    try:
        print("正在获取 Hugging Face 每日论文...")
        url = "https://huggingface.co/api/daily_papers"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        papers = response.json()
        
        result = []
        for paper in papers[:5]:  # 取前 5 篇
            title = paper.get("title", "No Title")
            paper_id = paper.get("id", "")
            url = f"https://huggingface.co/papers/{paper_id}" if paper_id else "#"
            # API 不直接提供摘要，通常需要进一步抓取，这里保留标题
            result.append({
                "title": title,
                "url": url,
                "summary": "点击链接查看详细内容"
            })
        return result
    except Exception as e:
        print(f"Error fetching HF papers: {e}")
        return []

def fetch_hackernews_ai():
    """Fetch AI related stories from Hacker News using Algolia API."""
    try:
        print("正在获取 Hacker News AI 热点...")
        # 搜索过去 24 小时内包含 AI 的热门文章
        url = "https://hn.algolia.com/api/v1/search?query=AI&tags=story&numericFilters=created_at_i>0"
        # 实际使用时可以动态计算时间戳，这里简化逻辑
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        hits = response.json().get("hits", [])
        
        result = []
        for hit in hits[:5]:
            result.append({
                "title": hit.get("title"),
                "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                "score": hit.get("points", 0)
            })
        return result
    except Exception as e:
        print(f"Error fetching HN: {e}")
        return []

def fetch_github_trending():
    """Fetch GitHub trending repositories using BeautifulSoup."""
    try:
        print("正在获取 GitHub 今日热门项目...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        url = "https://github.com/trending"
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        repos = soup.select("article.Box-row")
        
        result = []
        for repo in repos[:5]:
            title_tag = repo.select_one("h2 a")
            title = title_tag.get_text(strip=True).replace(" ", "")
            link = "https://github.com" + title_tag["href"]
            
            desc_tag = repo.select_one("p")
            description = desc_tag.get_text(strip=True) if desc_tag else "No description provided."
            
            star_tag = repo.select_one("a.Link--muted") # 通常第一个是总 Star
            stars = star_tag.get_text(strip=True) if star_tag else "0"
            
            result.append({
                "title": title,
                "url": link,
                "description": description,
                "stars": stars
            })
        return result
    except Exception as e:
        print(f"Error fetching GitHub Trending: {e}")
        return []

def generate_briefing():
    """Aggregate and format the briefing."""
    hf_papers = fetch_huggingface_daily_papers()
    hn_stories = fetch_hackernews_ai()
    gh_trending = fetch_github_trending()
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    markdown_report = f"# 🤖 AI 每日简报 - {date_str}\n\n"
    
    if hf_papers:
        markdown_report += "## 📄 每日精选论文 (Hugging Face)\n"
        for paper in hf_papers:
            markdown_report += f"- **[{paper['title']}]({paper['url']})**: {paper['summary']}\n"
        markdown_report += "\n"
    
    if gh_trending:
        markdown_report += "## 🔥 GitHub 今日热门项目\n"
        for repo in gh_trending:
            markdown_report += f"- **[{repo['title']}]({repo['url']})** (⭐ {repo['stars']}): {repo['description']}\n"
        markdown_report += "\n"
    
    if hn_stories:
        markdown_report += "## 🚀 Hacker News 热点\n"
        for story in hn_stories:
            markdown_report += f"- **[{story['title']}]({story['url']})** (热度: {story['score']})\n"
        
    return markdown_report

if __name__ == "__main__":
    report = generate_briefing()
    print(report)
    # Save to file for backward compatibility (optional if using module import)
    with open("daily_briefing.md", "w") as f:
        f.write(report)
