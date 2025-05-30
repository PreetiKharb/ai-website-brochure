from pydantic import BaseModel

class SummariseRequest(BaseModel):
    url: str

class SummariseResponse(BaseModel):
    summary: str

class BrochureRequest(BaseModel):
    url: str
    title: str = "Website Brochure"
    lang: str