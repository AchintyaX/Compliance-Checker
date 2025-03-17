# Compliance Checker

Compliance Checker tool, given a compliance page checks whether a given page meets the compliance requirement.
- Take a webpage as the input and it has to check the content in the page against a compliance policy
- Return the findings (non-compliant results) in the response

## Setup
1. In the `.env` file add your OpenAI key 
2. run `docker build -t compliance_checker`
3. run `docker run -p 8000:8000 docker.io/library/compliance_checker`


## Dev-Setup
1. `pip install --upgrade pip`
2. `pip install poetry`
3. `python server.py` 

You can find the container running on port 8000 and find the docs at `/docs` route
## Implementation Details

The Webpage is downloaded and parsed using the `SimpleWebPageReader` from LlamaIndex

The tool uses `gpt-4o` LLM by OpenAI, Given a page which has compliance URL 
the tool first extracts the facts and creates a compliance checklist.
The Function also uses LRU cache, since compliance docs are going to be changed less often.

There are 2 methods of compliance checks - 

### Base Compliance Checker 
Given the facts, the base checker returns which of the given facts are compliant and which are not
also it provides a reason behind why the compliance is met or not

### Chain Compliance Checker 
Given the facts, the chain checker first prepares a chain of thought in the input page which is an initial thought analysis
using the facts and the intitial analysis we pass them and get the compliance check results in the same format as base Compliance checker


