from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Route for API
@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello, World!"})

# Route for UI
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
