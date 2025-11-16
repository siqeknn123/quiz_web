from flask import Flask, render_template
from db.crud import get_quizes

app = Flask(__name__)

@app.route("/")
def index():
    quizes = get_quizes()
    return render_template("index.html", quizes_list=quizes)

@app.route("/test")
def test():
    return "<h1>Test</h1>"

@app.route("/result")
def result():
    return "<h1>Result</h1>"






if __name__ == '__main__':
    app.run()

