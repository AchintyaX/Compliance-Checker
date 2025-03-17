from llama_index.readers.web import SimpleWebPageReader
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import openai

load_dotenv(".env")
loader = SimpleWebPageReader(html_to_text=True)

class ComplianceCheck(BaseModel):
    """
    ComplianceCheck Model
    compliance_rule: The compliance rule that was checked
    compliant: A boolean indicating if the compliance rule was met
    reason: A string indicating the reason why the compliance rule was met or not
    """
    compliance_rule: str
    compliant: bool
    reason: str

class ComplianceAnalysis(BaseModel):
    compliance_checks: List[ComplianceCheck]

class ComplianceList(BaseModel):
    compliance_list: List[str]

def load_url(url):
    documents = loader.load_data(urls=[url])
    return documents[0].text

def extract_compliance(doc_txt):
    openai_client = openai.OpenAI()
    messages = [
        {"role": "system", "content": "You are a compliance expert, you would be provided with a document and you are to identify the compliance requirements in the document."},
        {"role": "user", "content": doc_txt}
    ]
    response = openai_client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=messages, 
        temperature=0.0,
        response_format= ComplianceList
    )
    response = response.to_dict()
    compliance_list = response['choices'][0]['message']['parsed']
    return compliance_list