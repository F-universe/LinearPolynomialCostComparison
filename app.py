import io
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, send_file
import numpy as np
import time

# Set Matplotlib to the "Agg" backend to avoid threading issues
plt.switch_backend('Agg')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Read the dataset from the form (5 rows of x and y values)
        dataset = []
        for i in range(5):
            x = float(request.form.get(f"x{i}"))
            y = float(request.form.get(f"y{i}"))
            dataset.append((x, y))

        # Coefficients for the linear model
        a0 = float(request.form.get("a0", 1) or 1)
        a1 = float(request.form.get("a1", 1) or 1)

        # Coefficients for the polynomial model
        b0 = float(request.form.get("b0", 1) or 1)
        b1 = float(request.form.get("b1", 1) or 1)
        b2 = float(request.form.get("b2", 1) or 1)

        # Calculate predictions and residuals for the linear model
        linear_calculations = []
        cost_linear = 0
        for x, y in dataset:
            predicted_linear = a0 + a1 * x
            linear_residual = y - predicted_linear
            squared_linear_residual = linear_residual ** 2
            cost_linear += squared_linear_residual
            linear_calculations.append({
                "x": x, "y": y, "predicted": predicted_linear,
                "residual": linear_residual, "squared_residual": squared_linear_residual
            })

        # Calculate predictions and residuals for the polynomial model
        polynomial_calculations = []
        cost_polynomial = 0
        for x, y in dataset:
            predicted_polynomial = b0 + b1 * x + b2 * (x ** 2)
            polynomial_residual = y - predicted_polynomial
            squared_polynomial_residual = polynomial_residual ** 2
            cost_polynomial += squared_polynomial_residual
            polynomial_calculations.append({
                "x": x, "y": y, "predicted": predicted_polynomial,
                "residual": polynomial_residual, "squared_residual": squared_polynomial_residual
            })

        # Determine the best model
        best_model = "Linear Model" if cost_linear < cost_polynomial else "Polynomial Model"

        # Calculate timestamp to avoid cache
        timestamp = int(time.time())

        # Pass data to the template for display
        return render_template("index.html", dataset=dataset, cost_linear=cost_linear,
                               cost_polynomial=cost_polynomial, best_model=best_model,
                               linear_calculations=linear_calculations,
                               polynomial_calculations=polynomial_calculations,
                               a0=a0, a1=a1, b0=b0, b1=b1, b2=b2, timestamp=timestamp)
    return render_template("index.html", timestamp=int(time.time()))

@app.route("/plot/<int:plot_type>")
def plot(plot_type):
    # Get parameters from the query string with default values
    try:
        a0 = float(request.args.get("a0", 1) or 1)
        a1 = float(request.args.get("a1", 1) or 1)
        b0 = float(request.args.get("b0", 1) or 1)
        b1 = float(request.args.get("b1", 1) or 1)
        b2 = float(request.args.get("b2", 1) or 1)
        x_values = [float(x) for x in request.args.getlist("x")]
        y_values = [float(y) for y in request.args.getlist("y")]
    except ValueError:
        return "Parameter error: ensure that coefficients and x/y values are numbers.", 400

    fig, ax = plt.subplots()

    # Plot the original dataset
    if plot_type == 1:
        ax.scatter(x_values, y_values, color="blue", label="Dataset")
        ax.set_title("Original Dataset Points")
        ax.legend()

    # Linear function with dataset points
    elif plot_type == 2:
        y_linear = [a0 + a1 * x for x in x_values]
        ax.plot(x_values, y_linear, color="red", label="Linear Model")
        ax.scatter(x_values, y_values, color="blue", label="Dataset")
        ax.set_title("Linear Model and Dataset Points")
        ax.legend()

    # Polynomial function with dataset points
    elif plot_type == 3:
        y_polynomial = [b0 + b1 * x + b2 * (x ** 2) for x in x_values]
        ax.plot(x_values, y_polynomial, color="green", label="Polynomial Model")
        ax.scatter(x_values, y_values, color="blue", label="Dataset")
        ax.set_title("Polynomial Model and Dataset Points")
        ax.legend()

    # Save the plot as a PNG image
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close(fig)
    return send_file(img, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
