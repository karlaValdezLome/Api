from flask import Flask, render_template, request, redirect, jsonify
import requests

app = Flask(__name__)

API_KEY = "3f9hknPFUPlm5kFjIJ2d75AfXmlUyU5E7M1Ktd9a"
API_URL = "https://api.nal.usda.gov/fdc/v1/"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buscar", methods=["POST"])
def buscar_alimento():
    nombre_comida = request.form.get("comida")
    
    if not nombre_comida:
        return redirect("/")
    
    try:
        params = {
            'api_key': API_KEY,
            'query': nombre_comida,
            'pageSize': 10
        }
        
        response = requests.get(f"{API_URL}foods/search", params=params)
        
        if response.status_code == 200:
            datos = response.json()
            alimentos = datos.get('foods', [])
            return render_template("index.html", alimentos=alimentos, busqueda=nombre_comida)
            
    except Exception as e:
        print(f"Error: {e}")
    
    return redirect("/")


@app.route("/api/buscar", methods=["POST"])
def api_buscar():
    nombre_comida = request.json.get("comida")
    
    if not nombre_comida:
        return jsonify({"error": "No se proporcionó el nombre del alimento"}), 400
    
    params = {
        'api_key': API_KEY,
        'query': nombre_comida,
        'pageSize': 10
    }
    
    response = requests.get(f"{API_URL}foods/search", params=params)
    
    if response.status_code == 200:
        datos = response.json()
        alimentos = datos.get('foods', [])
        return jsonify(alimentos)
    
    return jsonify({"error": "Error al consultar la API"}), 500

if __name__ == "__main__":
    app.run(debug=True)