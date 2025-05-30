# backend/prompts.py

def system_prompt_links() -> str:
    return (
        "You are provided with a list of links found on a webpage. "
        "Decide which are most relevant for a company brochure: About, Company, Careers/Jobs, etc.\n"
        "Respond in JSON like:\n"
        "{\n"
        '  "links": [\n'
        '    {"type": "about page", "url": "https://example.com/about"},\n'
        '    {"type": "careers page", "url": "https://example.com/careers"}\n'
        "  ]\n"
        "}"
    )

def system_prompt_brochure() -> str:
    return (
        "You are an assistant that analyzes the contents of relevant pages from a company website "
        "and creates a short brochure in Markdown for prospective customers, investors, and recruits. "
        "Include details of company culture, customers, and careers/jobs if available."
    )

def get_links_user_prompt(website) -> str:
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += (
        "Please decide which are relevant for a company brochure. "
        "Respond in JSON with full https URLs. Exclude Terms, Privacy, or email links.\n"
        "Links (may be relative):\n"
    )
    user_prompt += "\n".join(website.links)
    return user_prompt

def get_brochure_user_prompt(company_name: str, url: str, lang:str,  all_details: str) -> str:
    user_prompt = (
        f"You are looking at a company called: {company_name}\n"
        f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
        f"Write the brochure in {lang}.\n"
        f"{all_details}"
    )
    return user_prompt[:5_000]  # Truncate if too long