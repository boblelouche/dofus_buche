import matplotlib.pyplot as plt
import numpy as np

def math_function(x):
    return -20 * (0 <= x <= 0.2) - x**3 * (0.2 < x <= 0.5)

# Générer des valeurs de x
x = np.linspace(0, 1, 400)
# Calculer les valeurs de y en appliquant la fonction math_function
y = np.array([math_function(xi) for xi in x])
# Utiliser la méthode des moindres carrés pour trouver une approximation polynomiale de y
coefficients = np.polyfit(x, y, 3)
polynomial_approximation = np.poly1d(coefficients)

# Calculer les valeurs de y en utilisant l'approximation polynomiale
y_approx = polynomial_approximation(x)
print(y_approx)
def approx_function():
    x = np.linspace(0, 1, 400)
    y = np.array([math_function(xi) for xi in x])
    coefficients = np.polyfit(x, y, 3)
    polynomial_approximation = np.poly1d(coefficients)
    y_approx = polynomial_approximation(x)
    return y_approx

    
# Tracer la fonction
plt.plot(x, y, label='math_function(x)')
plt.xlabel('x')
plt.ylabel('math_function(x)')
plt.title('Graphique de la fonction math_function')
plt.legend()
plt.grid(True)
plt.show()

