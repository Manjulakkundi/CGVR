
import numpy as np
import matplotlib.pyplot as plt

def get_value(message, default):
    value = input(f"{message} [{default}]: ").strip()
    return float(value) if value else default

print("PHONG ILLUMINATION MODEL")
print("Enter values or press Enter for defaults.")

ka = get_value("Ambient coefficient (ka)", 0.2)
kd = get_value("Diffuse coefficient (kd)", 0.7)
ks = get_value("Specular coefficient (ks)", 0.5)
shininess = get_value("Shininess exponent", 32)

lx = get_value("Light position X", 3)
ly = get_value("Light position Y", 3)
lz = get_value("Light position Z", 5)

vx = get_value("Viewer position X", 0)
vy = get_value("Viewer position Y", 0)
vz = get_value("Viewer position Z", 5)

u = np.linspace(0, 2 * np.pi, 120)
v = np.linspace(0, np.pi, 80)
U, V = np.meshgrid(u, v)

X = np.cos(U) * np.sin(V)
Y = np.sin(U) * np.sin(V)
Z = np.cos(V)

points = np.stack((X, Y, Z), axis=-1)
normals = points.copy()

def normalize(vector):
    length = np.linalg.norm(vector, axis=-1, keepdims=True)
    return vector / np.maximum(length, 1e-10)

light = np.array([lx, ly, lz])
viewer = np.array([vx, vy, vz])

L = normalize(light - points)
View = normalize(viewer - points)

NdotL = np.sum(normals * L, axis=-1)
diffuse = np.maximum(NdotL, 0)

R = normalize(2 * NdotL[..., None] * normals - L)
RdotV = np.sum(R * View, axis=-1)
specular = np.where(
    NdotL > 0,
    np.maximum(RdotV, 0) ** shininess,
    0
)

ambient_color = np.array([0.15, 0.15, 0.15])
object_color = np.array([0.2, 0.5, 0.9])
light_color = np.ones(3)

ambient = ka * ambient_color
diffuse_color = kd * diffuse[..., None] * object_color
specular_color = ks * specular[..., None] * light_color

color = ambient + diffuse_color + specular_color
color = np.clip(color, 0, 1)

face_colors = (
    color[:-1, :-1] +
    color[1:, :-1] +
    color[:-1, 1:] +
    color[1:, 1:]
) / 4

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(
    X, Y, Z,
    facecolors=face_colors,
    linewidth=0,
    antialiased=True,
    shade=False
)

ax.scatter(
    [lx], [ly], [lz],
    color="yellow", s=100, label="Light Source"
)

ax.set_title("Phong Illumination Model")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
ax.set_box_aspect([1, 1, 1])
ax.legend()

print("\nPhong Illumination Components")
print("Ambient: Constant background illumination")
print("Diffuse: Depends on the angle between light and surface")
print("Specular: Produces shiny highlights")
print("Shininess:", shininess)

plt.show()
