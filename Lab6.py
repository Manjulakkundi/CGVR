
import numpy as np
import matplotlib.pyplot as plt

def plot_polygon(points, title):
    p = np.vstack([points, points[0]])
    plt.plot(p[:, 0], p[:, 1], marker='o')
    plt.fill(p[:, 0], p[:, 1], alpha=0.2)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)
    plt.axis('equal')
    plt.title(title)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

def apply_matrix(points, matrix):
    homogeneous = np.c_[points, np.ones(len(points))]
    transformed = (matrix @ homogeneous.T).T
    return transformed[:, :2]

def transformation_menu():
    n = int(input("Enter number of polygon vertices: "))
    points = []

    for i in range(n):
        x, y = map(float, input(f"Enter vertex {i + 1} (x y): ").split())
        points.append([x, y])

    original = np.array(points, dtype=float)
    current = original.copy()

    while True:
        print("\n--- 2D Geometric Transformations ---")
        print("1. Translation")
        print("2. Rotation about origin")
        print("3. Scaling")
        print("4. Reflection")
        print("5. Shearing")
        print("6. Rotation about arbitrary pivot")
        print("7. Reset polygon")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            tx = float(input("Enter translation tx: "))
            ty = float(input("Enter translation ty: "))
            matrix = np.array([
                [1, 0, tx],
                [0, 1, ty],
                [0, 0, 1]
            ])

        elif choice == '2':
            angle = np.radians(float(input("Enter angle in degrees: ")))
            c, s = np.cos(angle), np.sin(angle)
            matrix = np.array([
                [c, -s, 0],
                [s, c, 0],
                [0, 0, 1]
            ])

        elif choice == '3':
            sx = float(input("Enter scaling factor sx: "))
            sy = float(input("Enter scaling factor sy: "))
            matrix = np.array([
                [sx, 0, 0],
                [0, sy, 0],
                [0, 0, 1]
            ])

        elif choice == '4':
            print("1. Reflection about X-axis")
            print("2. Reflection about Y-axis")
            print("3. Reflection about origin")
            print("4. Reflection about y = x")
            print("5. Reflection about y = -x")
            r = input("Choose reflection: ")

            matrices = {
                '1': [[1, 0, 0], [0, -1, 0], [0, 0, 1]],
                '2': [[-1, 0, 0], [0, 1, 0], [0, 0, 1]],
                '3': [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
                '4': [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
                '5': [[0, -1, 0], [-1, 0, 0], [0, 0, 1]]
            }

            if r not in matrices:
                print("Invalid reflection choice.")
                continue

            matrix = np.array(matrices[r], dtype=float)

        elif choice == '5':
            shx = float(input("Enter shear factor shx: "))
            shy = float(input("Enter shear factor shy: "))
            matrix = np.array([
                [1, shx, 0],
                [shy, 1, 0],
                [0, 0, 1]
            ])

        elif choice == '6':
            px = float(input("Enter pivot x: "))
            py = float(input("Enter pivot y: "))
            angle = np.radians(float(input("Enter angle in degrees: ")))
            c, s = np.cos(angle), np.sin(angle)

            translate_to_origin = np.array([
                [1, 0, -px],
                [0, 1, -py],
                [0, 0, 1]
            ])

            rotation = np.array([
                [c, -s, 0],
                [s, c, 0],
                [0, 0, 1]
            ])

            translate_back = np.array([
                [1, 0, px],
                [0, 1, py],
                [0, 0, 1]
            ])

            matrix = translate_back @ rotation @ translate_to_origin

        elif choice == '7':
            current = original.copy()
            print("Polygon reset to original coordinates.")
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plot_polygon(original, "Original Polygon")
            plt.subplot(1, 2, 2)
            plot_polygon(current, "Reset Polygon")
            plt.tight_layout()
            plt.show()
            continue

        elif choice == '8':
            print("Program terminated.")
            break

        else:
            print("Invalid choice. Try again.")
            continue

        current = apply_matrix(current, matrix)

        print("\nTransformation Matrix:")
        print(matrix)
        print("\nTransformed Vertices:")
        print(np.round(current, 3))

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plot_polygon(original, "Original Polygon")
        plt.subplot(1, 2, 2)
        plot_polygon(current, "Transformed Polygon")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    transformation_menu()
