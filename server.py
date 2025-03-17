from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from compliance_checker import ComplianceChecker
import uvicorn
from http import HTTPStatus
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()
compliance_checker = ComplianceChecker()

class ComplianceRequest(BaseModel):
    checklist_url: str
    target_url: str
@app.get("/")
def read_root():
    return {"Hello": "Server up"}

@app.get("/health",tags=["Trending Themes"])
def health_check():
    response = {
        "status_code": HTTPStatus.OK,
        "message": HTTPStatus.OK.phrase,
        "response": True,
    }
    return JSONResponse(jsonable_encoder(response))

@app.post("/base-compliance-checker")
async def base_compliance_checker(request: ComplianceRequest):
    """
    Endpoint for base compliance checker
    """
    try:
        result = compliance_checker.base_compliance_checker(
            checklist_url=request.checklist_url,
            target_url=request.target_url
        )
        return {"compliance_checks": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chain-compliance-checker")
async def chain_compliance_checker(request: ComplianceRequest):
    """
    Endpoint for chain compliance checker
    """
    try:
        result = compliance_checker.chain_compliance_checker(
            checklist_url=request.checklist_url,
            target_url=request.target_url
        )
        return {"compliance_checks": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")