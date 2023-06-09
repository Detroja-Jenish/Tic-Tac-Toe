from flask import Flask, render_template, redirect, request, session,jsonify, Response
from werkzeug.utils import secure_filename
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdf"


change = True
move = 0
isFile = False
fileName = "Kahan.jpg"
count = 0
gameIds = {}
currentGames = {}

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

@app.route("/letsPlay")
def letsPlay():
    global gameIds
    print(f"from top {gameIds}")
    try:
        player_name = request.args.get("user")
        mark = request.args.get("mark")
        print(f"player = {player_name}\nmark = {mark}")
        print(gameIds)
        if(len(gameIds) == 0):
            print("blank gameIds")
            randomGameId = random.randrange(1,1000)
            gameIds[ str(randomGameId)] = {"player1" : {"name":player_name, "mark":mark, "ready" : False, "moved" : False},"responded":0}
            print(gameIds)
            return jsonify({"gameId": str(randomGameId), "playerNo" : "1"})
        
        for gameId in gameIds:
            print(gameId)
            if(len(gameIds[gameId])==2 and gameIds[gameId]["player1"]["mark"] != mark):
                gameIds[gameId]["player2"] = {"name":player_name, "mark":mark, "ready" : False, "moved" : False}
                print(gameIds)
                return jsonify({"gameId": gameId, "playerNo" : "2"})

        randomGameId = random.randrange(1,1000)
        gameIds[ str(randomGameId) ] = {"player1" : {"name":player_name, "mark":mark, "ready" : False, "moved" : False},"responded":0} 
        return jsonify({"gameId": str(randomGameId), "playerNo" : "1"})

    except:
        print("error")
        return Response(status=404)

@app.route("/clear")
def clear():
    global gameIds
    gameIds = {}
    return "done"
@app.route("/gameIds")
def getGameIds():
    global gameIds
    return gameIds

@app.route("/move/<gameId>/<playerNo>/<move>")
def moved(gameId, playerNo, move):
   global currentGames
   currentGames[gameId]["player" + playerNo]["moved"] = True
   currentGames[gameId]["player" + playerNo]["move"] = move
   return Response(status=202)

@app.route("/isMoved/<gameId>/<opponentNo>")
def isMoved(gameId, opponentNo):
    move = IsMoved(gameId, opponentNo)
    res = Response(move, mimetype="text/event-stream")
    return res

@app.route("/initializingGame/<gameId>")
def isAnyPlayer(gameId):
    player = initializing(gameId)
    print(player)
    res =Response(player, mimetype="text/event-stream")
    return res

@app.route("/iAmReady/<gameId>/<playerNo>")
def iAmReady(gameId,playerNo):
    global currentGames
    gameIds[gameId][f"player{playerNo}"]["ready"] = True
    print(gameIds[gameId][f"player{playerNo}"])
    return Response(status=202)

def IsMoved(gameId, opponentNo ):
    global currentGames
    if currentGames[gameId]["player" + opponentNo]["moved"]:
        currentGames[gameId]["player" + opponentNo]["moved"] = False
        yield "event: moved\ndata: %s\n\n" % currentGames[gameId]["player" + opponentNo]["move"]

def initializing(gameId):
    global gameIds
    len(gameIds[gameId])
    if (len( gameIds[ gameId ] ) == 3) and (gameIds[gameId]["responded"] < 2):
        print("responsed") 
        gameIds[gameId]["responded"] += 1
        yield f"event:getPlayer\ndata:{gameIds[gameId]} \n\n"
    elif (gameIds[gameId]["player1"]["ready"]) and (gameIds[gameId]["player2"]["ready"]):
        print("match begins")
        gameIds[ gameId ]["responded"] += 1
        print(((gameIds[gameId]["player1"]["ready"]) and (gameIds[gameId]["player2"]["ready"])))
        if(gameIds[ gameId ][ "responded" ] == 4):
            currentGames[ gameId ] = gameIds[gameId]
            gameIds.pop(gameId)
        yield "event: readySteadyGo\ndata: true\n\n"




if __name__ == "__main__":
    app.debug = True
    app.run(threaded=True, host="0.0.0.0", port="3000")