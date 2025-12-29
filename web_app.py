from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")


def ask_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Assistant Web"
    }

    data = {
        "model": "google/gemma-3-27b-it:free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "choices" not in result:
        return "AI could not generate a response."

    text = result["choices"][0]["message"]["content"]
    text = text.replace("**", "").replace("*", "")
    return text


@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    task = ""

    if request.method == "POST":

        #  AI REQUEST
        if "user_input" in request.form:
            task = request.form["task"]
            text = request.form["user_input"]

            if task == "question":
                prompt = f"Answer the question in a detailed and structured way:\n{text}"
            elif task == "summary":
                prompt = f"Summarize the following text clearly:\n{text}"
            elif task == "creative":
                prompt = f"Write detailed creative content on:\n{text}"
            elif task == "advice":
                prompt = f"Give detailed advice in a friendly tone:\n{text}"

            output = ask_ai(prompt)

        #  FEEDBACK SUBMISSION
        elif "feedback" in request.form:
            feedback = request.form["feedback"]
            task = request.form["task_name"]

            with open("feedback_web.txt", "a") as f:
                f.write(f"Time: {datetime.now()} | Task: {task} | Feedback: {feedback}\n")

    return render_template("index.html", output=output, task=task)


if __name__ == "__main__":
    app.run(debug=True)
