from flask import Flask, render_template_string, redirect, url_for
import RPi.GPIO as GPIO

# Pines GPIO asignados a cada ambiente
LEDS = {
    "habitacion1": 4,
    "habitacion2": 17,
    "bano": 27,
    "cocina": 22,
}

# Inicializar GPIO
GPIO.setmode(GPIO.BCM)
for pin in LEDS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

app = Flask(__name__)

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

@app.route("/")
def index():
    estados = {nombre: GPIO.input(pin) for nombre, pin in LEDS.items()}
    return render_template_string(html, estados=estados)

@app.route("/<room>/<action>", methods=["POST"])
def accion(room, action):
    pin = LEDS.get(room)
    if pin is not None:
        GPIO.output(pin, GPIO.HIGH if action == "encender" else GPIO.LOW)
    return redirect(url_for("index"))

@app.teardown_appcontext
def cleanup(exception=None):
    GPIO.cleanup()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
