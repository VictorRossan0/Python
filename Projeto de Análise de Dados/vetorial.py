import numpy as np
import matplotlib.pyplot as plt

# Definir o campo vetorial F(x,y) = (y, x)
def F(x, y):
    return y, x

# Criar uma grade de pontos para o campo vetorial
x_vals = np.linspace(-3, 3, 20)
y_vals = np.linspace(-3, 3, 20)
X, Y = np.meshgrid(x_vals, y_vals)
U, V = F(X, Y)

# Parametrização da curva: arco da circunferência de raio 2
t = np.linspace(0, np.pi/2, 100)
curve_x = 2 * np.cos(t)
curve_y = 2 * np.sin(t)

# Plotar campo vetorial
plt.figure(figsize=(8,8))
plt.quiver(X, Y, U, V, color='blue', alpha=0.6)
plt.plot(curve_x, curve_y, 'r-', linewidth=3, label='Curva C (arco de círculo)')
plt.scatter([2, 0], [0, 2], color='red')  # Pontos inicial e final

# Configurações do gráfico
plt.xlim(-3, 3)
plt.ylim(-3, 3)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Campo vetorial F(x,y) = (y, x) e curva C')
plt.legend()
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')

plt.show()