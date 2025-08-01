from flask import Flask, render_template_string, redirect, url_for
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configurar modo de numeración BCM (o BOARD si preferís)
GPIO.setmode(GPIO.BCM)

# Diccionario con los nombres de cada lugar y su pin GPIO correspondiente
LEDS = {
    "habitacion1": 17,
    "habitacion2": 27,
    "bano": 22,
    "cocina": 23
}

# Template HTML
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Control de Luces</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding-top: 40px; }
        .room { margin: 20px; }
        button { padding: 10px 25px; font-size: 16px; margin: 5px; }
    </style>
</head>
<body>
    <h1>💡 Control de Luces</h1>
    {% for nombre, estado in estados.items() %}
        <div class="room">
            <h2>{{ nombre.capitalize() }}: <strong>{{ "ENCENDIDA" if estado else "APAGADA" }}</strong></h2>
            <form method="POST" action="{{ url_for('accion', room=nombre, action='encender') }}">
                <button type="submit">Encender</button>
            </form>
            <form method="POST" action="{{ url_for('accion', room=nombre, action='apagar') }}">
                <button type="submit">Apagar</button>
            </form>
        </div>
    {% endfor %}
</body>
</html>
"""

# Inicializar todos los pines como salida
for pin in LEDS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
@app.route("/")
def index():
    estados = {nombre: GPIO.input(pin) for nombre, pin in LEDS.items()}
    return render_template_string(html, estados=estados)


@app.route("/<lugar>/<accion>", methods=["POST"])
def accion(lugar, accion):
    if lugar in LEDS:
        pin = LEDS[lugar]
        estado = GPIO.HIGH if accion == "encender" else GPIO.LOW
        GPIO.output(pin, estado)
        return f"Luz de {lugar} {'encendida' if estado == GPIO.HIGH else 'apagada'}", 200
    else:
        return "Lugar no válido", 404

@app.route("/")
def inicio():
    return "Servidor de control de luces activo"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
