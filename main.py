from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks, Request, Response, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any
import sys
from fastapi.responses import JSONResponse
import shutil
import os
from image_processing import image_to_text
from audio_processing import audio_to_text
from prompt import issue_type_prompt
from llama_calling import call_llama
from location import get_help

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost:5173",  # your frontend domain (for development)
    "https://your-frontend-domain.com",  # production frontend domain
    "https://maintestkindme.netlify.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDIO_DIR = "uploads/audio"
IMAGE_DIR = "uploads/images"

# Create directories if they don't exist
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Hello, Mumbai-Hacks!"}

@app.post("/upload/")
async def upload(file: UploadFile = File(None), help_text: str = Form(None),latitude: float = Query(...),longitude: float = Query(...)):
    if not file and not help_text:
        raise HTTPException(status_code=400, detail="Either a file or text is required.")
    
    text = None
    
    if file:
        # Identify the content type of the file
        content_type = file.content_type

        if content_type.startswith("audio/"):
            # Handle audio file
            audio_file_path = os.path.join(AUDIO_DIR, file.filename)
            with open(audio_file_path, "wb") as audio_file:
                audio_file.write(await file.read())
            print("audio saved")
            print(audio_file_path)
            text = audio_to_text(audio_file_path)
            print(" ")
            print("---------------------------------------------")
            print(text)
        
        elif content_type.startswith("image/"):
            # Handle image file
            image_file_path = os.path.join(IMAGE_DIR, file.filename)
            with open(image_file_path, "wb") as image_file:
                image_file.write(await file.read())
            print("image saved")
            print(image_file_path)
            text = image_to_text(image_file_path)
            print("---------------------------------------------")
            print(text)
        
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only audio or image files are allowed.")
        
    else:
        text = help_text
    
    issue = issue_type_prompt.replace("{text_blob}", text)
    print(" ")
    print("------------------------------------------------------")
    print(issue)
    llama_response = call_llama(issue)
    print(" ")
    print("-------------------------------------------------------")
    print(llama_response)
    first_aid = llama_response["first_aid_advice"]
    place_type = llama_response["place_type"]
    help_type = get_help(latitude, longitude, place_type)
    print(" ")
    print("--------------------------------------------------------")
    print(help_type)

    response = {
        "category": place_type,
        "first aid": first_aid,
        "locations": help_type
    }
    return response

    
    