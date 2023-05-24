import os
from threading import Thread
import uuid
from flask import Flask, request
from flask_httpauth import HTTPTokenAuth
from dotenv import load_dotenv

from academic_paper import to_academic_paper
from notes import to_notes
from tokens import manage_gpt_4_token_balance

load_dotenv()

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

global processed_academic_papers
processed_academic_papers = {}


def async_to_notes(paper, uuid):
    try:
        notes = to_notes(paper)
        os.unlink(paper.name)
        processed_academic_papers[uuid] = notes
        print("Notes: ", notes)
    except Exception as e:
        print("Error: ", e)
        processed_academic_papers[uuid] = "Error: " + str(e)

@auth.verify_token
def verify_token(token):
    return token == os.getenv("API_TOKEN")

@app.route("/academic_papers/to_notes", methods=["POST"])
@auth.login_required
def upload():
    file = request.files.get("file")
    if not file:
        return "No file selected", 400
    
    id = str(uuid.uuid4())
    
    paper = to_academic_paper(file)
    process_thread = Thread(target=async_to_notes, args=(paper, id), daemon=True)
    process_thread.start()
    
    return {"id": id}, 200

@app.route("/academic_papers/to_notes", methods=["GET"])
@auth.login_required
def retrieve():
    uuid = request.args.get("id")
    if not uuid:
        return "No ID provided", 400
    if uuid not in processed_academic_papers:
        return "No such file processed", 404
    
    notes = processed_academic_papers.pop(uuid)
    return notes, 200

token_manager_thread = Thread(target=manage_gpt_4_token_balance, daemon=True)
token_manager_thread.start()
