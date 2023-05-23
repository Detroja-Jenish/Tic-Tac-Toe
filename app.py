from flask import Flask, render_template, redirect, request, session,jsonify, Response
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdf"


change = True
move = 0
isFile = False
fileName = "Kahan.jpg"
count = 0

def event_stream():
    global change,move
    
    # TODO: handle client disconnection.
    if change :#for message in pubsub.listen():
        message = {} 
        print("from Event")
        
        yield 'data: %s\n\n' % move

def get_player():
    
    global count
    count += 1
    print(count)
    if count>10:
        count = 5
        print('data: Rakshit\n\n')
        yield 'data: %s\n\n' % "rakshit"

@app.route("/game-setting")
def gameSetting():
    return render_template("gameSetting.html")

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")
    return redirect("/game")

@app.route("/game")
def game():
    return render_template("tic-tac-toe.html", user=session["user"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        session["user"] = request.form["user"]
        return redirect("/game")

@app.route("/moved")
def moved():
    global change,move
    move = request.args.get("move")
    change = True
    return jsonify({"done":"true"})


@app.route("/isMoved")
def isMoved():
    message = event_stream()
    print(message)
    res =Response(message, mimetype="text/event-stream")
    return res

@app.route("/isAnyPlayer")
def isAnyPlayer():
    message = get_player()
    print(message)
    res =Response(message, mimetype="text/event-stream")
    return res

@app.route("/upload",methods=["POST"])
def upload():
    #photo       = request.files['file'];
    #photoName   = secure_filename(photo.filename);
    #photopath = f"templates/{photoName}"
    #photo.save(photoPath)
    #isFile = True
    #fileName = photoPath
    isFile = True
    return render_template("file.html")

if __name__ == "__main__":
    app.debug = True
    app.run(threaded=True, host="0.0.0.0", port="3000")