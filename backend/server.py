from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
from fastapi.responses import FileResponse
import openai
import os
from dotenv import load_dotenv
from models import SummariseRequest, SummariseResponse, BrochureRequest
from summariser import WebsiteSummariser
from pdf_utils import generate_pdf_brochure
import tempfile

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.environ.get("OPENAI_API_KEY")
@app.post("/summarise", response_model=SummariseResponse)
async def summarise(req: SummariseRequest):
    summariser = WebsiteSummariser(req.url)
    summary = summariser.summarise()
    return SummariseResponse(summary=summary)

@app.post("/brochure")
async def brochure(req: BrochureRequest):
    company_name = req.title or "The Company"
    summariser = WebsiteSummariser(req.url)
    brochure_markdown = summariser.generate_brochure_markdown(company_name, req.url)
    return {"markdown": brochure_markdown}



