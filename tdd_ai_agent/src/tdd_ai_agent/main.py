import os
import uvicorn
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from tdd_ai_agent.agent import generate_tests

# Carregar variáveis de ambiente do .env
load_dotenv()

app = FastAPI(title="TDD AI Agent API",
            description="API for generating unit tests using AI",
            version="1.0.0")

@app.post("/generate-tests")
async def generate_unit_tests(file: UploadFile = None, code: str = Form(None)):
    try:
        if file:
            content = (await file.read()).decode("utf-8")
        elif code:
            content = code
        else:
            return JSONResponse({"error": "No code provided"}, status_code=400)

        tests = generate_tests(content)
        return {"generated_tests": tests}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/")
def root():
    return {"message": "TDD AI Agent API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
