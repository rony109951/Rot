# app.py
from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
DATA_FILE = "data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {"pages": {}, "offers": []}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route("/")
def home():
    return render_template("home.html", pages=data["pages"], offers=data["offers"])

@app.route("/page/<page_id>")
def page_view(page_id):
    page = data["pages"].get(page_id, {"title":"صفحة غير موجودة", "content":""})
    return render_template("page.html", page=page, page_id=page_id)

@app.route("/edit_page/<page_id>", methods=["POST"])
def edit_page(page_id):
    content = request.form.get("content", "")
    if page_id in data["pages"]:
        data["pages"][page_id]["content"] = content
        save_data()
    return redirect(url_for("page_view", page_id=page_id))

@app.route("/add_offer", methods=["POST"])
def add_offer():
    title = request.form.get("title","")
    image_url = request.form.get("image_url","")
    data["offers"].append({"title":title, "image":image_url})
    save_data()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
