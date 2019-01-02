from flask import Flask
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visites = redis.incr("compteur")
    except RedisError:
        visites = "<i>Erreur de connection Redis, compteur desactive</i>"

    html = "<h3>Bonjour {nom}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visites:</b> {visites} <br/>" \
           "<p>Abonne toi!</p>"
    return html.format(nom=os.getenv("NOM", "youtube"), hostname=socket.gethostname(), visites=visites)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
