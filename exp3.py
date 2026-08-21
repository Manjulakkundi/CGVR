import numpy as np
import matplotlib.pyplot as plt
import math


# ==========================================================
# TRANSFORMATION MATRICES
# ==========================================================

def translation(tx, ty):
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=float)


def rotation(angle):
    theta = math.radians(angle)

    return np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta),  math.cos(theta), 0],
        [0, 0, 1]
    ], dtype=float)


def scaling(sx, sy):
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ], dtype=float)


def reflection_x():
    return np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ], dtype=float)


def reflection_y():
    return np.array([
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ], dtype=float)


def reflection_y_equals_x():
    return np.array([
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ], dtype=float)


def shearing(shx, shy):
    return np.array([
        [1, shx, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ], dtype=float)


# ==========================================================
# APPLY MATRIX
# ==========================================================

def apply_transformation(points, matrix):

    homogeneous = np.hstack(
        (points, np.ones((len(points), 1)))
    )

    result = (matrix @ homogeneous.T).T

    return result[:, :2]


# ==========================================================
# INPUT POINTS
# ==========================================================

def get_points():

    n = int(input("\nEnter number of vertices: "))

    points = []

    for i in range(n):

        print(f"\nVertex {i + 1}")

        x = float(input("Enter X coordinate: "))
        y = float(input("Enter Y coordinate: "))

        points.append([x, y])

    return np.array(points, dtype=float)


# ==========================================================
# DISPLAY GRAPH
# ==========================================================

def display(original, transformed, title):

    original_closed = np.vstack([original, original[0]])
    transformed_closed = np.vstack([transformed, transformed[0]])

    plt.figure(figsize=(8, 6))

    plt.plot(
        original_closed[:, 0],
        original_closed[:, 1],
        'b-o',
        label="Original"
    )

    plt.plot(
        transformed_closed[:, 0],
        transformed_closed[:, 1],
        'r-o',
        label="Transformed"
    )

    plt.axhline(0)
    plt.axvline(0)

    plt.xlabel("X")
    plt.ylabel("Y")

    plt.title(title)

    plt.grid(True)
    plt.legend()
    plt.axis("equal")

    plt.show()


# ==========================================================
# MAIN PROGRAM
# ==========================================================

print("=" * 60)
print("        EXPERIMENT 3")
print("  IMPLEMENTATION OF 2D TRANSFORMATIONS")
print("     USING HOMOGENEOUS COORDINATES")
print("=" * 60)


while True:

    # ------------------------------------------------------
    # MENU FIRST
    # ------------------------------------------------------

    print("\n" + "=" * 50)
    print("        TRANSFORMATION MENU")
    print("=" * 50)

    print("1. Translation")
    print("2. Rotation")
    print("3. Scaling")
    print("4. Reflection")
    print("5. Shearing")
    print("6. Exit")

    choice = int(input("\nEnter your choice: "))


    # ======================================================
    # EXIT
    # ======================================================

    if choice == 6:

        print("\nExperiment completed successfully!")
        break


    # ======================================================
    # INVALID CHOICE
    # ======================================================

    if choice not in [1, 2, 3, 4, 5]:

        print("\nInvalid choice!")
        continue


    # ======================================================
    # GET VERTICES AFTER MENU
    # ======================================================

    points = get_points()


    # ======================================================
    # TRANSLATION
    # ======================================================

    if choice == 1:

        print("\n--- TRANSLATION ---")

        tx = float(input("Enter Tx: "))
        ty = float(input("Enter Ty: "))

        matrix = translation(tx, ty)

        transformed = apply_transformation(
            points,
            matrix
        )

        title = "2D Translation"


    # ======================================================
    # ROTATION
    # ======================================================

    elif choice == 2:

        print("\n--- ROTATION ---")

        angle = float(
            input("Enter rotation angle (degrees): ")
        )

        print("\n1. Rotation about Origin")
        print("2. Rotation about Arbitrary Pivot")

        rchoice = int(
            input("Enter your choice: ")
        )

        if rchoice == 1:

            matrix = rotation(angle)

        else:

            px = float(input("Enter pivot X: "))
            py = float(input("Enter pivot Y: "))

            T1 = translation(-px, -py)
            R = rotation(angle)
            T2 = translation(px, py)

            matrix = T2 @ R @ T1

        transformed = apply_transformation(
            points,
            matrix
        )

        title = "2D Rotation"


    # ======================================================
    # SCALING
    # ======================================================

    elif choice == 3:

        print("\n--- SCALING ---")

        sx = float(input("Enter Sx: "))
        sy = float(input("Enter Sy: "))

        matrix = scaling(sx, sy)

        transformed = apply_transformation(
            points,
            matrix
        )

        title = "2D Scaling"


    # ======================================================
    # REFLECTION
    # ======================================================

    elif choice == 4:

        print("\n--- REFLECTION ---")

        print("1. Reflection about X-axis")
        print("2. Reflection about Y-axis")
        print("3. Reflection about y = x")

        rchoice = int(
            input("Enter your choice: ")
        )

        if rchoice == 1:

            matrix = reflection_x()
            title = "Reflection about X-axis"

        elif rchoice == 2:

            matrix = reflection_y()
            title = "Reflection about Y-axis"

        elif rchoice == 3:

            matrix = reflection_y_equals_x()
            title = "Reflection about y = x"

        else:

            print("Invalid reflection choice!")
            continue

        transformed = apply_transformation(
            points,
            matrix
        )


    # ======================================================
    # SHEARING
    # ======================================================

    elif choice == 5:

        print("\n--- SHEARING ---")

        shx = float(input("Enter Shx: "))
        shy = float(input("Enter Shy: "))

        matrix = shearing(shx, shy)

        transformed = apply_transformation(
            points,
            matrix
        )

        title = "2D Shearing"


    # ======================================================
    # DISPLAY MATRIX
    # ======================================================

    print("\nTransformation Matrix:")
    print(matrix)


    # ======================================================
    # DISPLAY COORDINATES
    # ======================================================

    print("\nOriginal Coordinates:")

    for i, point in enumerate(points):
        print(
            f"Vertex {i + 1}: "
            f"({point[0]:.2f}, {point[1]:.2f})"
        )


    print("\nTransformed Coordinates:")

    for i, point in enumerate(transformed):
        print(
            f"Vertex {i + 1}: "
            f"({point[0]:.2f}, {point[1]:.2f})"
        )


    # ======================================================
    # GRAPH
    # ======================================================

    display(
        points,
        transformed,
        title
    )