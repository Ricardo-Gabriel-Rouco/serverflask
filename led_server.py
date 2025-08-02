from flask import Flask, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configurar modo de numeración BCM (o BOARD si preferís)
GPIO.setmode(GPIO.BCM)

# Diccionario con los nombres de cada lugar y su pin GPIO correspondiente
luces = {
    "habitacion1": 17,
    "habitacion2": 27,
    "bano": 22,
    "cocina": 4
}

# Inicializar todos los pines como salida
for pin in luces.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/<lugar>/<accion>", methods=["POST"])
def accion(lugar, accion):
    if lugar in luces:
        pin = luces[lugar]
        estado = GPIO.HIGH if accion == "encender" else GPIO.LOW
        GPIO.output(pin, estado)
        return f"Luz de {lugar} {'encendida' if estado == GPIO.HIGH else 'apagada'}", 200
    else:
        return "Lugar no válido", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
