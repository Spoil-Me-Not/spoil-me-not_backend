from flask import Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def display():
    return "Looks like it works!"

@app.route('/show=<show>', methods=['POST', 'GET'])
def addShow(show):
    print(show)
    return show

if __name__=='__main__':
    app.run(host="0.0.0.0", port="80")