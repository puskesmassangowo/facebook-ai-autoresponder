from flask import Flask, request
import requests
import openai
from langdetect import detect, LangDetectException

app = Flask(__name__)

# Environment variables will be set by Render
import os
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Facebook webhook verification
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token", 403

    # Handle incoming comments
    data = request.json
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            if change.get("field") == "comments":
                comment_message = change["value"].get("message")
                comment_id = change["value"].get("comment_id")

                language = None
                try:
                    language = detect(comment_message)
                except LangDetectException:
                    language = None

                # If detected language is Indonesian or English, use AI; else default response
                if language in ("id", "en"):
                    reply_message = generate_ai_reply(comment_message)
                else:
                    reply_message = "Maaf ya, saya belum bisa memahami bahasa itu. Tapi terima kasih sudah berkomentar!"

                post_reply(comment_id, reply_message)
    return "ok", 200

def generate_ai_reply(message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message}]
    )
    return response["choices"][0]["message"]["content"]

def post_reply(comment_id, reply):
    url = f"https://graph.facebook.com/v19.0/{comment_id}/comments"
    payload = {
        "message": reply,
        "access_token": PAGE_ACCESS_TOKEN
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
