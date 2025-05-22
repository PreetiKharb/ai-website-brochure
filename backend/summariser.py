import requests
from bs4 import BeautifulSoup
import openai

class WebsiteSummariser:
    def __init__(self, url: str, model="gpt-3.5-turbo"):
        self.url = url
        self.model = model

    def extract_text(self) -> str:
        """Extracts and cleans main content from website."""
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        }
        page = requests.get(self.url, headers= headers)
        soup = BeautifulSoup(page.text, "html.parser")
        for tag in soup(["nav", "footer", "header", "script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        # Filter out very short lines (likely to be boilerplate)
        lines = [line for line in text.splitlines() if len(line.strip()) > 40]
        return "\n".join(lines)

    def split_chunks(self, text: str, max_tokens=2000) -> list:
        """Splits text into chunks for LLM context window."""
        max_chars = max_tokens * 4  # approx 1 token = 4 chars
        lines = text.split('\n')
        chunks, chunk = [], ""
        for line in lines:
            if len(chunk) + len(line) + 1 > max_chars:
                chunks.append(chunk)
                chunk = ""
            chunk += line + "\n"
        if chunk.strip():
            chunks.append(chunk)
        return chunks

    def summarise_chunk(self, chunk: str) -> str:
        """Summarises a single chunk using OpenAI."""
        prompt = (
            f"Summarise the following website content. "
            "Focus on the key information and ignore irrelevant details:\n\n"
            f"{chunk}"
        )
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarises website content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5,
        )
        return response["choices"][0]["message"]["content"]

    def summarise(self) -> str:
        """Full pipeline: extract, chunk, summarise recursively."""
        text = self.extract_text()
        chunks = self.split_chunks(text)
        summaries = [self.summarise_chunk(chunk) for chunk in chunks]
        if len(summaries) > 1:
            combined = "\n\n".join(summaries)
            return self.summarise_chunk(combined)
        return summaries[0] if summaries else "Could not extract main content."
    @staticmethod
    def get_brochure_user_prompt(company_name, url, details):
        user_prompt = f"""
        You are a world-class copywriter.
        Create a beautiful 1-page brochure in Markdown for a company called "{company_name}".
        Use the following extracted website content to infer their mission, offering, value proposition, and what makes them unique.

        Company Name: {company_name}
        Website: {url}

        Website Content:
        {details}

        Your brochure should include sections:
        - About Us
        - What We Offer
        - Why Choose Us
        - (and any other relevant sections you infer)
        Format it as Markdown. Make it concise, engaging, and professional.
        """
        # Optionally, truncate details if too long
        if len(user_prompt) > 6000:
            user_prompt = user_prompt[:6000]
        return user_prompt

    def generate_brochure_markdown(self, company_name, url):
        details = self.extract_text()
        prompt = self.get_brochure_user_prompt(company_name, url, details)
        # Call OpenAI with this prompt
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=900,
            temperature=0.6,
        )
        return response.choices[0].message.content
