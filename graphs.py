import numpy as np
import matplotlib.pyplot as plt

def probability_function(x, m, T=24):
    """Functie die de kans berekent om x correcte tiles achter elkaar te kiezen met m mines."""
    probability = 1
    for i in range(x):
        probability *= (T - m - i) / (T - i)
    return probability

# Maak een meshgrid van waarden voor x (correcte keuzes) en m (aantal mines)
x_values = np.arange(1, 24)  # 1 tot 10 correcte keuzes
m_values = np.arange(1, 24)  # 1 tot 23 mines

# Bereken de kansen voor alle combinaties van x en m
probabilities = np.array([[probability_function(x, m) for m in m_values] for x in x_values])

# Plot de grafiek
plt.figure(figsize=(10, 6))
for i, x in enumerate(x_values):
    plt.plot(m_values, probabilities[i], label=f"x = {x}")

plt.xlabel("Aantal correcte tiles")
plt.ylabel("Kans om x correcte tiles te kiezen")
plt.title("Kansen voor correcte keuzes in een mines-game")
plt.legend()
plt.grid(True)
plt.show()


# Aangepaste functie met limiet op exponentiële groei

def pushup_formula_limited(x, m, P0=1, target_pushups=150, total_tiles=24):
    """Bereken het aantal push-ups exponentieel, maar beperk extreme groei."""
    x_doel = total_tiles - m  # Aantal veilige keuzes

    # Beperk de groeisnelheid om extreme waarden te voorkomen
    k = np.log(target_pushups / P0) / x_doel

    # Exponentiële groei, maar met een limiet op extreme waarden
    pushups = P0 * np.exp(k * x)

    # Max limiet om te voorkomen dat het naar 1e50 gaat
    return min(pushups, target_pushups)

# Genereer nieuwe data voor de plot
pushup_values_limited = np.array([[pushup_formula_limited(x, m) for x in x_values] for m in m_values])

# Plot de aangepaste resultaten
plt.figure(figsize=(10, 6))
for i, m in enumerate(m_values):
    plt.plot(x_values, pushup_values_limited[i], label=f"m = {m}")

plt.xlabel("Aantal correcte keuzes (x)")
plt.ylabel("Push-ups")
plt.title("Exponentiële push-up groei met limiet per mijnenkeuze")
plt.legend(loc="upper left", bbox_to_anchor=(1,1))
plt.grid(True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Gegeven data
x_data_new2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
y_data_new2 = [1.12, 1.29, 1.48, 1.71, 2, 2.35, 2.79, 3.35, 4.07, 5, 6.26, 7.96, 10.35, 13.8, 18.97, 27.11, 40.66, 65.06, 113.85, 227.7, 569.25]

# Cubic spline interpolatie
cs = CubicSpline(x_data_new2, y_data_new2)

# Verkrijg de coëfficiënten van de spline (a, b, c, d) voor elk interval
for i in range(len(x_data_new2) - 1):
    x1 = x_data_new2[i]
    x2 = x_data_new2[i + 1]
    
    # De coëfficiënten voor het interval
    a = cs.c[0][i]
    b = cs.c[1][i]
    c = cs.c[2][i]
    d = cs.c[3][i]
    
    print(f"Spline voor interval ({x1}, {x2}):")
    print(f"a = {a}, b = {b}, c = {c}, d = {d}")
    print("-" * 50)


