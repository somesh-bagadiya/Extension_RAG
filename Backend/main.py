from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from text_processor_crew.src.text_processor_crew.crew import TextProcessorCrew

app = FastAPI()

# Configure CORS to allow requests from the Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://bimciljmockmmenihkjongkbpnmomphl"],  # Replace with your extension ID
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for the text data
class TextData(BaseModel):
    content: str

@app.post("/process-text/")
async def process_text(data: TextData):
    print("Received text:", data.content)  # For debugging
    uncleaned_text = data.content
    # Process the text data as needed, here we just return a confirmation message
    # run(uncleaned_text)
    return {"message": "Text received successfully.", "content_length": len(data.content)}

# def run(uncleaned_text):
#     inputs = {'text_data': uncleaned_text}
#     print("Type of inputs:", type(inputs))
#     results = TextProcessorCrew().crew().kickoff(inputs=inputs)
#     for result in results:
#         print(result)

