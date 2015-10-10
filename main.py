from flask import Flask

PORT = 5000
app = Flask(__name__)

@app.route("/")
def main():
    return "Hello Fintech!"

if __name__ == "__main__":
    app.run(port=PORT, debug=True)
