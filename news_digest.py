import requests
from bs4 import BeautifulSoup
from datetime import date

def get_bbc_headlines():
    url = "https://www.bbc.com/news"

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []

    for link in soup.find_all("a", href=True):

        text = link.get_text(strip=True)

        href = link["href"]

        if len(text) > 30 and "/news/" in href:

            if href.startswith("/"):
                href = "https://www.bbc.com" + href

            item = {
                "headline": text,
                "link": href,
                "time": str(date.today())
            }

            if item not in headlines:
                headlines.append(item)

        if len(headlines) == 5:
            break

    return headlines

def get_hackernews_headlines():
    url = "https://news.ycombinator.com/"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []

    for link in soup.select(".titleline a"):

        text = link.get_text(strip=True)

        if "." in text:
             continue

        headlines.append({
            "headline": link.get_text(strip=True),
            "link": link.get("href"),
            "time": str(date.today())
        })

        if len(headlines) == 5:
            break

    return headlines

def get_hindu_headlines():
    url = "https://www.thehindu.com/news/"

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []

    for article in soup.select("h3.title a"):

        text = article.get_text(strip=True)
        href = article.get("href")

        if text and href:

            headlines.append({
                "headline": text,
                "link": href,
                "time": str(date.today())
            })

        if len(headlines) == 5:
            break

    return headlines

bbc = get_bbc_headlines()
hn = get_hackernews_headlines()
hindu = get_hindu_headlines()

news_data = {
    "BBC": bbc,
    "Hacker News": hn,
    "The Hindu": hindu
}

print("\nNEWS DATA DICTIONARY\n")
print(news_data)

today = date.today()

html = f"""
<html>
<body style="font-family: Arial, sans-serif; background:#f4f6f9; padding:20px;">

<div style="max-width:800px; margin:auto; background:white;
border-radius:12px; overflow:hidden;
box-shadow:0 2px 10px rgba(0,0,0,0.1);">

<div style="background:#0f172a; color:white; padding:20px;">
<h1 style="margin:0;">📰 Daily News Digest</h1>
<p style="margin-top:8px;">{today}</p>
<p>Top headlines from multiple sources</p>
</div>

<div style="padding:20px;">
"""
for source, headlines in news_data.items():

    html += f"""
<h2 style="color:#0f172a;
border-bottom:2px solid #e5e7eb;
padding-bottom:5px;">
{source}
</h2>
<ul>
"""

    for item in headlines:

        if isinstance(item, dict):

            html += f"""
            <li style="margin-bottom:12px;">
                <a href="{item['link']}"
                   style="color:#2563eb;text-decoration:none;">
                   {item['headline']}
                </a>
                <br>
                <small style="color:#666;">
                    Published: {item['time']}
                </small>
            </li>
            """

        else:

            html += f"""
            <li>
                {item}
                <br>
                <small style="color:#666;">
                    Retrieved: {today}
                </small>
            </li>
            """

    html += "</ul>"

html += """
<hr style="border:none;border-top:1px solid #ddd;">

<p style="color:#666;font-size:14px;text-align:center;">
Daily News Digest • Automated Web Scraping and Email Reporting System
</p>


</div>
</div>

</body>
</html>
"""

with open("news_digest.html", "w", encoding="utf-8") as file:
    file.write(html)

print("HTML news digest created!") 

print("\nBBC HEADLINES\n")

for headline in bbc:
    print("-", headline)

print("\nHACKER NEWS HEADLINES\n")

for headline in hn:
    print("-", headline)

print("\nTHE HINDU HEADLINES\n")

for headline in hindu:
    print("-", headline)