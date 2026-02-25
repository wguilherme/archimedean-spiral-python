import matplotlib.pyplot as plt

from spiral import SpiralParams, generate_spiral

params = SpiralParams(r_start=40, r_end=95, turns=30)
points = generate_spiral(params)

x_points = [p[0] for p in points]
y_points = [p[1] for p in points]

plt.figure(figsize=(7, 7))
plt.plot(x_points, y_points, linewidth=0.3, color='black')
plt.axis('equal')
plt.axis('off')
plt.tight_layout()
plt.show()
