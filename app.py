from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "API teste!"})

@app.route('/teste/<nome>')
def teste(nome):
    return jsonify({"teste": f"Eai paizao, {nome}!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
