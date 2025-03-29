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
