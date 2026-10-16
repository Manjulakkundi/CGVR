import numpy as np
import matplotlib.pyplot as plt
import math


# ==========================================================
# EXPERIMENT 4
# IMPLEMENT COMPOSITE TRANSFORMATIONS
# USING MATRIX REPRESENTATION
# ==========================================================


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
# APPLY HOMOGENEOUS TRANSFORMATION
# ==========================================================

def apply_transformation(points, matrix):

    # Convert 2D points to homogeneous coordinates
    homogeneous_points = np.hstack(
        (points, np.ones((len(points), 1)))
    )

    # Matrix multiplication
    transformed = (matrix @ homogeneous_points.T).T

    # Convert back to 2D
    return transformed[:, :2]


# ==========================================================
# INPUT POLYGON
# ==========================================================

def get_polygon():

    n = int(input("\nEnter number of vertices: "))

    points = []

    print("\nEnter polygon coordinates:")

    for i in range(n):

        print(f"\nVertex {i + 1}")

        x = float(input("Enter X coordinate: "))
        y = float(input("Enter Y coordinate: "))

        points.append([x, y])

    return np.array(points, dtype=float)


# ==========================================================
# DISPLAY RESULT
# ==========================================================

def display(original, transformed, title):

    original_closed = np.vstack([
        original,
        original[0]
    ])

    transformed_closed = np.vstack([
        transformed,
        transformed[0]
    ])

    plt.figure(figsize=(8, 6))

    # Original polygon
    plt.plot(
        original_closed[:, 0],
        original_closed[:, 1],
        'b-o',
        label="Original Polygon"
    )

    # Transformed polygon
    plt.plot(
        transformed_closed[:, 0],
        transformed_closed[:, 1],
        'r-o',
        label="Transformed Polygon"
    )

    # Coordinate axes
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

print("=" * 65)
print("          EXPERIMENT 4")
print("   IMPLEMENT COMPOSITE TRANSFORMATIONS")
print("        USING MATRIX REPRESENTATION")
print("=" * 65)


while True:

    # ======================================================
    # MENU FIRST
    # ======================================================

    print("\n" + "=" * 55)
    print("             TRANSFORMATION MENU")
    print("=" * 55)

    print("1. Translation + Rotation")
    print("2. Translation + Scaling")
    print("3. Rotation + Scaling")
    print("4. Translation + Rotation + Scaling")
    print("5. Rotation about Arbitrary Pivot + Scaling")
    print("6. Reflection + Translation")
    print("7. Shearing + Rotation")
    print("8. Custom Composite Transformation")
    print("9. Exit")

    choice = int(input("\nEnter your choice: "))


    # ======================================================
    # EXIT
    # ======================================================

    if choice == 9:

        print("\nExperiment completed successfully!")
        break


    # ======================================================
    # VALIDATE CHOICE
    # ======================================================

    if choice not in range(1, 9):

        print("\nInvalid choice!")
        continue


    # ======================================================
    # GET POLYGON AFTER MENU
    # ======================================================

    points = get_polygon()


    # ======================================================
    # TRANSLATION + ROTATION
    # ======================================================

    if choice == 1:

        print("\n--- TRANSLATION + ROTATION ---")

        tx = float(input("Enter Tx: "))
        ty = float(input("Enter Ty: "))

        angle = float(
            input("Enter rotation angle: ")
        )

        T = translation(tx, ty)
        R = rotation(angle)

        # Composite matrix
        matrix = T @ R

        title = "Translation + Rotation"


    # ======================================================
    # TRANSLATION + SCALING
    # ======================================================

    elif choice == 2:

        print("\n--- TRANSLATION + SCALING ---")

        tx = float(input("Enter Tx: "))
        ty = float(input("Enter Ty: "))

        sx = float(input("Enter Sx: "))
        sy = float(input("Enter Sy: "))

        T = translation(tx, ty)
        S = scaling(sx, sy)

        # Composite matrix
        matrix = T @ S

        title = "Translation + Scaling"


    # ======================================================
    # ROTATION + SCALING
    # ======================================================

    elif choice == 3:

        print("\n--- ROTATION + SCALING ---")

        angle = float(
            input("Enter rotation angle: ")
        )

        sx = float(input("Enter Sx: "))
        sy = float(input("Enter Sy: "))

        R = rotation(angle)
        S = scaling(sx, sy)

        # Composite matrix
        matrix = R @ S

        title = "Rotation + Scaling"


    # ======================================================
    # TRANSLATION + ROTATION + SCALING
    # ======================================================

    elif choice == 4:

        print(
            "\n--- TRANSLATION + ROTATION + SCALING ---"
        )

        tx = float(input("Enter Tx: "))
        ty = float(input("Enter Ty: "))

        angle = float(
            input("Enter rotation angle: ")
        )

        sx = float(input("Enter Sx: "))
        sy = float(input("Enter Sy: "))

        T = translation(tx, ty)
        R = rotation(angle)
        S = scaling(sx, sy)

        # Composite matrix
        matrix = T @ R @ S

        title = "Translation + Rotation + Scaling"


    # ======================================================
    # ROTATION ABOUT PIVOT + SCALING
    # ======================================================

    elif choice == 5:

        print(
            "\n--- ROTATION ABOUT PIVOT + SCALING ---"
        )

        px = float(input("Enter pivot X: "))
        py = float(input("Enter pivot Y: "))

        angle = float(
            input("Enter rotation angle: ")
        )

        sx = float(input("Enter Sx: "))
        sy = float(input("Enter Sy: "))

        # Move pivot to origin
        T1 = translation(-px, -py)

        # Rotation
        R = rotation(angle)

        # Scaling
        S = scaling(sx, sy)

        # Move pivot back
        T2 = translation(px, py)

        # Composite matrix
        matrix = T2 @ R @ S @ T1

        title = "Rotation about Pivot + Scaling"


    # ======================================================
    # REFLECTION + TRANSLATION
    # ======================================================

    elif choice == 6:

        print(
            "\n--- REFLECTION + TRANSLATION ---"
        )

        print("\nReflection options:")
        print("1. X-axis")
        print("2. Y-axis")
        print("3. y = x")

        rchoice = int(
            input("Enter reflection choice: ")
        )

        if rchoice == 1:

            F = reflection_x()

        elif rchoice == 2:

            F = reflection_y()

        elif rchoice == 3:

            F = reflection_y_equals_x()

        else:

            print("Invalid reflection choice!")
            continue

        tx = float(input("Enter Tx: "))
        ty = float(input("Enter Ty: "))

        T = translation(tx, ty)

        # Composite matrix
        matrix = T @ F

        title = "Reflection + Translation"


    # ======================================================
    # SHEARING + ROTATION
    # ======================================================

    elif choice == 7:

        print(
            "\n--- SHEARING + ROTATION ---"
        )

        shx = float(input("Enter Shx: "))
        shy = float(input("Enter Shy: "))

        angle = float(
            input("Enter rotation angle: ")
        )

        H = shearing(shx, shy)
        R = rotation(angle)

        # Composite matrix
        matrix = R @ H

        title = "Shearing + Rotation"


    # ======================================================
    # CUSTOM COMPOSITE TRANSFORMATION
    # ======================================================

    elif choice == 8:

        print(
            "\n--- CUSTOM COMPOSITE TRANSFORMATION ---"
        )

        print("\nEnter the transformations")
        print("in the order you want to apply them.")

        print("\nAvailable:")
        print("T = Translation")
        print("R = Rotation")
        print("S = Scaling")
        print("F = Reflection")
        print("H = Shearing")

        order = input(
            "\nEnter transformation sequence "
            "(example: TRS): "
        ).upper()

        matrix = np.eye(3)

        for operation in order:

            if operation == "T":

                tx = float(input("Enter Tx: "))
                ty = float(input("Enter Ty: "))

                current = translation(tx, ty)

            elif operation == "R":

                angle = float(
                    input("Enter rotation angle: ")
                )

                current = rotation(angle)

            elif operation == "S":

                sx = float(input("Enter Sx: "))
                sy = float(input("Enter Sy: "))

                current = scaling(sx, sy)

            elif operation == "F":

                print("\n1. X-axis")
                print("2. Y-axis")
                print("3. y = x")

                fchoice = int(
                    input("Enter reflection choice: ")
                )

                if fchoice == 1:
                    current = reflection_x()

                elif fchoice == 2:
                    current = reflection_y()

                elif fchoice == 3:
                    current = reflection_y_equals_x()

                else:
                    print("Invalid reflection choice!")
                    current = np.eye(3)

            elif operation == "H":

                shx = float(input("Enter Shx: "))
                shy = float(input("Enter Shy: "))

                current = shearing(shx, shy)

            else:

                print(
                    f"Unknown transformation: {operation}"
                )

                continue

            # Build composite matrix
            matrix = current @ matrix

        title = "Custom Composite Transformation"


    # ======================================================
    # APPLY FINAL COMPOSITE MATRIX
    # ======================================================

    transformed = apply_transformation(
        points,
        matrix
    )


    # ======================================================
    # DISPLAY COMPOSITE MATRIX
    # ======================================================

    print("\n" + "=" * 55)
    print("FINAL COMPOSITE TRANSFORMATION MATRIX")
    print("=" * 55)

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
    # DISPLAY GRAPH
    # ======================================================

    display(
        points,
        transformed,
        title
    )