import numpy as np
import matplotlib.pyplot as plt

# Paramètres de la simulation
size = 100  # Taille de la grille
angles = np.linspace(0, np.pi, 5)  # Angles d'éclairage

# Création de la surface initiale (simulant une peinture)
z = np.sin(np.linspace(0, 4 * np.pi, size)).reshape((size, 1)) * np.sin(np.linspace(0, 4 * np.pi, size)).reshape((1, size))

# Fonction pour simuler l'éclairage de la surface
def illuminate_surface(z, angle):
    nx, ny = np.gradient(z)
    nz = np.ones_like(z)
    norm = np.sqrt(nx**2 + ny**2 + nz**2)
    nx /= norm
    ny /= norm
    nz /= norm
    lx = np.cos(angle)
    ly = 0
    lz = np.sin(angle)
    intensity = lx * nx + ly * ny + lz * nz
    intensity[intensity < 0] = 0
    return intensity

# Capturer les images sous différents éclairages
images = []
for angle in angles:
    images.append(illuminate_surface(z, angle))

# Affichage des images capturées sous différents éclairages
fig, axes = plt.subplots(1, len(images), figsize=(15, 5))
for i, img in enumerate(images):
    axes[i].imshow(img, cmap='gray')
    axes[i].set_title(f'Éclairage angle {np.rad2deg(angles[i]):.0f}°')
    axes[i].axis('off')
plt.show()

# Fonction pour reconstruire la surface à partir des images capturées
def reconstruct_surface(images, angles):
    n = len(images)  # Nombre de sources lumineuses
    A = np.zeros((n, 2))
    b = np.zeros(n)
    height, width = images[0].shape
    surface = np.zeros((height, width))

    for i in range(n):
        angle = angles[i]
        A[i, 0] = np.cos(angle)
        A[i, 1] = np.sin(angle)

    for y in range(height):
        for x in range(width):
            for i in range(n):
                b[i] = images[i][y, x]

            # Résolution du système linéaire pour obtenir les gradients
            gradients, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
            surface[y, x] = np.linalg.norm(gradients)

    return surface

# Reconstruction de la surface
reconstructed_surface = reconstruct_surface(images, angles)

# Affichage de la surface initiale définie
fig = plt.figure(figsize=(15, 7))
ax = fig.add_subplot(121, projection='3d')
x = np.linspace(0, 1, size)
y = np.linspace(0, 1, size)
x, y = np.meshgrid(x, y)
ax.plot_surface(x, y, z, cmap='viridis')
ax.set_title("Surface initiale définie")

# Affichage de la surface reconstruite
ax = fig.add_subplot(122, projection='3d')
ax.plot_surface(x, y, reconstructed_surface, cmap='viridis')
ax.set_title("Surface reconstruite")
plt.show()
