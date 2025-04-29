from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import math
import random

app = Flask(__name__)
CORS(app)

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])
    return total

def i_hill_climbing(coord):
    ciudades = list(coord.keys())
    mejor_ruta = ciudades[:]
    random.shuffle(mejor_ruta)
    mejor_dist = evalua_ruta(mejor_ruta, coord)

    for _ in range(10):  # Iteraciones externas
        ruta = ciudades[:]
        random.shuffle(ruta)
        mejora = True
        while mejora:
            mejora = False
            dist_actual = evalua_ruta(ruta, coord)
            for i in range(len(ruta)):
                for j in range(i + 1, len(ruta)):
                    ruta_tmp = ruta[:]
                    ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                    dist = evalua_ruta(ruta_tmp, coord)
                    if dist < dist_actual:
                        ruta = ruta_tmp
                        mejora = True
                        break
                if mejora:
                    break
        nueva_dist = evalua_ruta(ruta, coord)
        if nueva_dist < mejor_dist:
            mejor_ruta = ruta
            mejor_dist = nueva_dist

    return mejor_ruta, mejor_dist

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tsp', methods=['POST'])
def tsp():
    data = request.get_json()
    coord = data.get("coord", {})
    if len(coord) < 2:
        return jsonify({"error": "Se requieren al menos 2 ciudades"}), 400
    ruta, distancia_total = i_hill_climbing(coord)
    return jsonify({"ruta": ruta, "distancia_total": round(distancia_total, 4)})

if _name_ == '_main_':
    # Obtener el puerto desde la variable de entorno, si no está presente usar el puerto 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
