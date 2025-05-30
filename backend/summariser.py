import os
import requests
import json
from typing import Dict, Any
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import openai
import re

from prompts import (
    system_prompt_links,
    system_prompt_brochure,
    get_links_user_prompt,
    get_brochure_user_prompt
)

# --- Environment & Config ---
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if not (api_key and api_key.startswith('sk-') and len(api_key) > 10):
    raise RuntimeError("OpenAI API key is missing or looks invalid.")

openai.api_key = api_key
MODEL = 'gpt-4o-mini'

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )
}

# --- Web Scraping ---

class Website:
    """Represents a scraped website with content and links."""

    def __init__(self, url: str):
        self.url = url
        self.title, self.text, self.links = self._scrape(url)

    def _scrape(self, url: str):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            return "No title found", "", []

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string.strip() if soup.title else "No title found"
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""
        links = [link.get('href') for link in soup.find_all('a') if link.get('href')]
        return title, text, links

    def get_contents(self) -> str:
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

# --- Helper Functions ---

def links_to_markdown(links_json: Dict[str, Any]) -> str:
    """Convert extracted links into a Markdown section."""
    if not links_json.get("links"):
        return ""
    lines = ["## Useful Links\n"]
    for link in links_json["links"]:
        display_name = link.get("type", "Link").replace("_", " ").title()
        url = link.get("url", "")
        lines.append(f"- [{display_name}]({url})")
    return "\n".join(lines)

def get_links(url: str) -> Dict[str, Any]:
    website = Website(url)
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt_links()},
            {"role": "user", "content": get_links_user_prompt(website)},
        ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    return json.loads(result)

def get_all_details(url: str) -> str:
    """Aggregate landing and relevant pages, append pretty Markdown links."""
    result = "Landing page:\n"
    main_site = Website(url)
    result += main_site.get_contents()
    links = get_links(url)
    for link in links.get("links", []):
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    result += "\n\n" + links_to_markdown(links)
    return result

def create_brochure(company_name: str, url: str, lang: str) -> str:
    """Call OpenAI to create the brochure markdown."""
    all_details = get_all_details(url)
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt_brochure()},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url, lang, all_details)},
        ],
    )
    result = response.choices[0].message.content
    markdown = strip_code_block(result)
    # Step 2: Translate if needed
    if lang != "en":
        markdown = translate_text(markdown, lang)
    return markdown

def strip_code_block(text: str) -> str:
    """Remove ```json ... ``` or ```markdown ... ``` blocks if present."""
    pattern = r"^```(?:\w+\n)?(.*)```$"
    match = re.match(pattern, text.strip(), re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def translate_text(text, target_lang):
    language_map = {
        "en": "English",
        "hi": "Hindi",
        "es": "Spanish"
    }
    language_str = language_map.get(target_lang, "English")
    prompt = (
        f"Translate the following text to {language_str}:\n\n{text}\n\n"
        "Respond only with the translated text."
    )
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful translation assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1200,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()