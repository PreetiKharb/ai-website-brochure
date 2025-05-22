# AI Website Brochure Generator

A modern, full-stack application that leverages OpenAI’s GPT to automatically **summarise the content of any website** and **generate a beautifully formatted, downloadable brochure (Markdown & PDF) in seconds.**

---

## 🚀 **How It Works**

1. **Paste any website URL.**
2. **Choose the summary style** (Plain, Engaging, or Fun).
3. **Click "Generate"** to instantly receive an AI-powered summary and a suggested brochure.
4. **Edit the Markdown brochure** directly in your browser, or preview how it looks.
5. **Download a clean PDF**—ready to share with clients, investors, or your team!

---

## 📺 **Demo Video**

> **Click to watch:** > [![Demo Video](./screenshot.png)](https://link-to-your-demo.com)
>
> _(Or drag your recording here, or upload to YouTube/Loom and link it)_

---

## ✨ **Features**

- **Modern MUI + React Frontend:** Mobile-friendly, responsive, clean UI.
- **Python FastAPI Backend:** Robust, async, well-structured OOP code.
- **OpenAI GPT Integration:** Summarise and transform any website into a business-ready brochure.
- **Markdown Editor:** Edit and preview the brochure before exporting.
- **PDF Export:** One-click, ready-to-share PDF downloads.
- **Automatic Company Name Detection:** (Planned) — keep the UI minimal and smart!
- **Error handling:** Handles network/LLM/website failures gracefully.

---

## 🛠️ **Tech Stack**

- **Frontend:** React, TypeScript, Material UI, React-Markdown, html2pdf.js
- **Backend:** FastAPI, Python, OpenAI API, BeautifulSoup, Requests
- **PDF Generation:** html2pdf.js (frontend)
- **AI Model:** OpenAI GPT-3.5 or GPT-4o

---

## 💻 **How to Run Locally**

```bash
# Clone the repo
git clone https://github.com/PreetiKharb/ai-website-brochure.git
cd ai-website-brochure

# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env           # Add your OpenAI API key to .env
uvicorn server:app --reload

# Frontend setup (in a new terminal)
cd ../frontend
npm install
npm run dev
```

- The frontend will run at `http://localhost:5173`
- The backend will run at `http://127.0.0.1:8000`

---

## 🖼️ **Screenshots**

| Home/URL Entry      | Brochure Editor/Preview | PDF Download        |
| ------------------- | ----------------------- | ------------------- |
| ![](./screens1.png) | ![](./screens2.png)     | ![](./screens3.png) |

---

## ✍️ **How it works (Visual Flow)**

1. **User enters URL and picks style.**
2. **Frontend sends request to FastAPI backend.**
3. **Backend scrapes and cleans the website content.**
4. **Content is chunked and sent to OpenAI for recursive summarisation.**
5. **Brochure is generated in Markdown by OpenAI.**
6. **Frontend displays editable Markdown and preview.**
7. **User can download a PDF version instantly.**

---

## 📝 **Why this is cool (use cases)**

- For founders/startups to create a “one-pager” from their website in seconds.
- For consultants/marketers to quickly understand and present client sites.
- For engineers to see real-world LLM, web scraping, and PDF export in action.

---

## 🙏 **Credit & Inspiration**

Built by [Preeti Kharb](https://github.com/PreetiKharb).
LLM engineering inspiration from [ed-donner/llm_engineering](https://github.com/ed-donner/llm_engineering).

---

## 📦 **Contributing**

PRs and stars welcome!
For improvements, open an issue or submit a PR.

---

## 📜 **License**

[MIT](./LICENSE) (or your preferred license)

---
