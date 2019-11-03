from flask import Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def display():
    return "Looks like it works!"

if __name__=='__main__':
    app.run(host="0.0.0.0", port="5000")