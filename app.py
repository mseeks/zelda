from multiprocessing import Process
from threading import Thread
from flask import Flask, request
from dotenv import load_dotenv
from academic_paper import to_academic_paper
from notes import to_notes
from tokens import manage_gpt_4_token_balance

load_dotenv()

app = Flask(__name__)


@app.route("/academic_papers/to_notes", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    if file.filename == "":
        return "No file selected", 400

    try:
        paper = to_academic_paper(file)
        if paper is None:
            return "Invalid file type", 400
        notes = to_notes(paper)
        return notes, 200
    except Exception as e:
        return str(e), 500


thread = Thread(target=manage_gpt_4_token_balance)
thread.daemon = True
thread.start()
