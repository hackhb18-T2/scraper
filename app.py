from flask import Flask, render_template, jsonify
from json import dumps
import json
import scraper
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/product/<int:ean>")

def getEan(ean):

    product = scraper.findEan(ean)
    rueckgabe = []
    for prod in product:
        rueckgabe.append(prod.getDic())

    return jsonify(rueckgabe)



if __name__ == '__main__':
    app.run()
