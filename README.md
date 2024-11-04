Linear and Polynomial Model Cost Comparison
This project allows users to compare the cost functions of two different models applied to a dataset: a linear model and a polynomial model. The aim is to help users determine which model best represents the dataset based on the cost (error) calculated for each model.

Features
Input Dataset: Users can input a dataset directly into the provided HTML form.
Model Coefficients: Users can set custom coefficients for both the linear and polynomial models.
Cost Comparison: After submitting the dataset and model coefficients, the HTML page displays the calculated cost for each model, highlighting the model with the lower cost as the best fit.
Graphical Representation: At the bottom of the page, the dataset points and the fitted curves for both the linear and polynomial models are displayed in separate plots.
Usage
Dataset Input: The user inputs a set of x and y values in the dataset section of the HTML form.
Model Coefficients: Enter the coefficients for both the linear model (a0, a1) and the polynomial model (b0, b1, b2) in the designated fields.
Submit: Press the Compare Cost Functions button to view the calculated cost for each model.
Results Display: The resulting page will show:
The cost values for both models, indicating which has the lower cost.
Detailed calculations for both models, including residuals and squared residuals for each data point.
Graphical plots of the dataset and the model curves.
Important Note
The graphical functions at the bottom of the page are currently in the stabilization phase. Users may encounter occasional bugs in the graph generation, such as layout issues or unexpected behavior. These functions will be improved in future updates.

Requirements
Python 3.x
Flask
Matplotlib
NumPy
Installation and Setup
Clone the repository.
Install the required libraries: Flask, Matplotlib, and NumPy.
bash

pip install flask matplotlib numpy
Run the application.
bash

python app.py
Access the application in a web browser at http://127.0.0.1:5000.
Future Improvements
Stabilize Graphical Output: Ensure reliable graph rendering and address known bugs.
Extended Model Support: Consider adding additional models for comparison.
Enhanced Interface: Improve form validation and user experience.
