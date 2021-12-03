from fastapi import FastAPI, Request
from src.main import getQuestionsAndAnswersFromText
import random

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/")
async def getQuestionsAndAnswers(info : Request):
    req_info = await info.json()
    # print(req_info)
    qAnswers = list(getQuestionsAndAnswersFromText(req_info["text"]).values())
    print(qAnswers, type (qAnswers))

    counter = 1
    response = []

    for qAns in random.sample(qAnswers, min(10, len(qAnswers))):
        question = {
            "id": counter,
            "body": qAns[0],
            "answer": qAns[1]
        }
        counter += 1
        response.append(question)

    return {
        "questions": response
    }