import io
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, send_file
import numpy as np
import time

# Imposta Matplotlib al backend "Agg" per evitare problemi di threading
plt.switch_backend('Agg')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Leggi il dataset dal form (5 righe di valori x e y)
        dataset = []
        for i in range(5):
            x = float(request.form.get(f"x{i}"))
            y = float(request.form.get(f"y{i}"))
            dataset.append((x, y))

        # Coefficienti per il modello lineare
        a0 = float(request.form.get("a0", 1) or 1)
        a1 = float(request.form.get("a1", 1) or 1)

        # Coefficienti per il modello polinomiale
        b0 = float(request.form.get("b0", 1) or 1)
        b1 = float(request.form.get("b1", 1) or 1)
        b2 = float(request.form.get("b2", 1) or 1)

        # Calcolo delle predizioni e dei residui per il modello lineare
        linear_calculations = []
        cost_linear = 0
        for x, y in dataset:
            predicted_linear = a0 + a1 * x
            residuo_lineare = y - predicted_linear
            residuo_quadrato_lineare = residuo_lineare ** 2
            cost_linear += residuo_quadrato_lineare
            linear_calculations.append({
                "x": x, "y": y, "predicted": predicted_linear,
                "residuo": residuo_lineare, "residuo_quadrato": residuo_quadrato_lineare
            })

        # Calcolo delle predizioni e dei residui per il modello polinomiale
        polynomial_calculations = []
        cost_polynomial = 0
        for x, y in dataset:
            predicted_polynomial = b0 + b1 * x + b2 * (x ** 2)
            residuo_polinomiale = y - predicted_polynomial
            residuo_quadrato_polinomiale = residuo_polinomiale ** 2
            cost_polynomial += residuo_quadrato_polinomiale
            polynomial_calculations.append({
                "x": x, "y": y, "predicted": predicted_polynomial,
                "residuo": residuo_polinomiale, "residuo_quadrato": residuo_quadrato_polinomiale
            })

        # Determina il modello migliore
        best_model = "Modello Lineare" if cost_linear < cost_polynomial else "Modello Polinomiale"

        # Calcolo del timestamp per evitare cache
        timestamp = int(time.time())

        # Passa i dati al template per visualizzarli
        return render_template("index.html", dataset=dataset, cost_linear=cost_linear,
                               cost_polynomial=cost_polynomial, best_model=best_model,
                               linear_calculations=linear_calculations,
                               polynomial_calculations=polynomial_calculations,
                               a0=a0, a1=a1, b0=b0, b1=b1, b2=b2, timestamp=timestamp)
    return render_template("index.html", timestamp=int(time.time()))

@app.route("/plot/<int:plot_type>")
def plot(plot_type):
    # Ricevi i parametri dalla query string con valori predefiniti
    try:
        a0 = float(request.args.get("a0", 1) or 1)
        a1 = float(request.args.get("a1", 1) or 1)
        b0 = float(request.args.get("b0", 1) or 1)
        b1 = float(request.args.get("b1", 1) or 1)
        b2 = float(request.args.get("b2", 1) or 1)
        x_values = [float(x) for x in request.args.getlist("x")]
        y_values = [float(y) for y in request.args.getlist("y")]
    except ValueError:
        return "Errore nei parametri: assicurarsi che i coefficienti e i valori x/y siano numeri.", 400

    fig, ax = plt.subplots()

    # Grafico del dataset originale
    if plot_type == 1:
        ax.scatter(x_values, y_values, color="blue", label="Dataset")
        ax.set_title("Punti del Dataset Originale")
        ax.legend()

    # Funzione lineare con i punti del dataset
    elif plot_type == 2:
        y_linear = [a0 + a1 * x for x in x_values]
        ax.plot(x_values, y_linear, color="red", label="Modello Lineare")
        ax.scatter(x_values, y_values, color="blue", label="Dataset")
        ax.set_title("Modello Lineare e Punti del Dataset")
        ax.legend()

    # Funzione polinomiale con i punti del dataset
    elif plot_type == 3:
        y_polynomial = [b0 + b1 * x + b2 * (x ** 2) for x in x_values]
        ax.plot(x_values, y_polynomial, color="green", label="Modello Polinomiale")
        ax.scatter(x_values, y_values, color="blue", label="Dataset")
        ax.set_title("Modello Polinomiale e Punti del Dataset")
        ax.legend()

    # Salva il grafico come immagine PNG
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close(fig)
    return send_file(img, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
