# pip install fastapi uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from agentForStockPrice import ask

app = FastAPI(
    title="Gemini Stock Agent API",
    description="FastAPI wrapper around LangChain + Gemini agent router"
)

@app.get("/ask")
async def ask_agent(question: str = Query(..., description="Your natural language question")):
    try:
        answer = ask(question)
        return JSONResponse(content={"question": question, "answer": answer})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
