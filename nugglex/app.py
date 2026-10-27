from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, jsonify
from rag import NuggleXRAG

app = Flask(__name__)
rag = NuggleXRAG()  # PDF is loaded + indexed once at startup

GITHUB = "https://github.com/mirzamuhammadarizbaig"


@app.context_processor
def inject():
    return {"github": GITHUB}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/thanks")
def thanks():
    return render_template("thanks.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    q = (data.get("message") or "").strip()
    if not q:
        return jsonify(reply="Type something first 😄"), 400
    try:
        return jsonify(reply=rag.answer(q, data.get("history")))
    except Exception as e:
        print("Chat error:", e)
        return jsonify(reply="Oops, my brain glitched. Try again in a sec."), 500


if __name__ == "__main__":
    app.run(debug=True)
