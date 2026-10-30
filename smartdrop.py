
import tkinter as tk
from tkinter import messagebox
from math import sqrt
from itertools import permutations
from time import perf_counter
import matplotlib.pyplot as plt

# COLOURS
BLUE = "#1565C0"
DARK_BLUE = "#0D2D63"
YELLOW = "#FFC928"
GREEN = "#159B72"
PURPLE = "#7545D6"
RED = "#EF476F"
WHITE = "#FFFFFF"
BG = "#F4F7FC"
TEXT = "#17345C"

# DELIVERY LOCATIONS
locations = [
    (10, 10),
    (20, 15),
    (35, 25),
    (25, 40),
    (10, 45)
]

location_names = [
    "Warehouse", "Customer A", "Customer B",
    "Customer C", "Customer D"
]

location_colours = [BLUE, RED, GREEN, "#F28C18", PURPLE]


# DISTANCE CALCULATION
def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def route_distance(route, matrix):
    total = 0
    for i in range(len(route) - 1):
        total += matrix[route[i]][route[i + 1]]
    return total


def create_distance_matrix(points):
    size = len(points)
    matrix = [[0] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            matrix[i][j] = distance(points[i], points[j])

    return matrix


# NEAREST NEIGHBOR ALGORITHM
def nearest_neighbor(matrix):
    n = len(matrix)
    route = [0]
    unvisited = set(range(1, n))

    while unvisited:
        current = route[-1]
        nearest = min(
            unvisited,
            key=lambda city: matrix[current][city]
        )
        route.append(nearest)
        unvisited.remove(nearest)

    route.append(0)
    return route


# 2-OPT ALGORITHM
def two_opt(route, matrix):
    best_route = route[:]
    improved = True

    while improved:
        improved = False

        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                new_route = (
                    best_route[:i]
                    + best_route[i:j + 1][::-1]
                    + best_route[j + 1:]
                )

                if route_distance(new_route, matrix) < route_distance(
                    best_route, matrix
                ):
                    best_route = new_route
                    improved = True

    return best_route


# BRUTE FORCE ALGORITHM
def brute_force(matrix):
    n = len(matrix)
    best_route = None
    best_distance = float("inf")

    for order in permutations(range(1, n)):
        route = [0] + list(order) + [0]
        current_distance = route_distance(route, matrix)

        if current_distance < best_distance:
            best_distance = current_distance
            best_route = route

    return best_route, best_distance


# ROUTE GRAPH
def show_route_graph(route):
    x_values = [locations[i][0] for i in route]
    y_values = [locations[i][1] for i in route]

    plt.figure(figsize=(8, 5))

    plt.plot(
        x_values, y_values,
        marker="o", linewidth=2.5,
        markersize=9, color="#1685E8"
    )

    for i, (x, y) in enumerate(locations):
        plt.scatter(
            x, y, s=140,
            color=location_colours[i],
            edgecolors="white",
            linewidths=2,
            zorder=3
        )

        plt.annotate(
            location_names[i],
            (x, y),
            xytext=(7, 8),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold"
        )

    plt.title(
        "SMARTDROP - Delivery Route",
        fontsize=15,
        fontweight="bold"
    )
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()


# MAIN WINDOW
root = tk.Tk()
root.title("SMARTDROP - Delivery Route Optimization")
root.geometry("1050x650")
root.minsize(850, 560)
root.configure(bg=BG)

# HEADER
header = tk.Frame(root, bg=DARK_BLUE)
header.pack(fill="x")

tk.Label(
    header,
    text="SMARTDROP",
    font=("Arial", 22, "bold"),
    fg=YELLOW,
    bg=DARK_BLUE
).pack(pady=(8, 1))

tk.Label(
    header,
    text="E-Commerce Delivery Route Optimization",
    font=("Arial", 10),
    fg=WHITE,
    bg=DARK_BLUE
).pack(pady=(0, 8))

tk.Label(
    root,
    text="SMARTER ROUTES  |  FASTER DELIVERIES",
    font=("Arial", 10, "bold"),
    fg=BLUE,
    bg=BG
).pack(pady=6)


# DASHBOARD LAYOUT
dashboard = tk.Frame(root, bg=BG)
dashboard.pack(fill="both", expand=True, padx=10, pady=3)

dashboard.grid_rowconfigure(0, weight=1)
dashboard.grid_columnconfigure(0, weight=1, uniform="panels")
dashboard.grid_columnconfigure(1, weight=2, uniform="panels")
dashboard.grid_columnconfigure(2, weight=1, uniform="panels")


# LEFT PANEL: LOCATIONS AND BUTTONS
left_panel = tk.Frame(
    dashboard,
    bg=WHITE,
    highlightbackground="#D5E3F5",
    highlightthickness=1
)
left_panel.grid(
    row=0, column=0,
    sticky="nsew", padx=(0, 6)
)

tk.Label(
    left_panel,
    text="DELIVERY LOCATIONS",
    font=("Arial", 11, "bold"),
    fg=BLUE,
    bg=WHITE
).pack(pady=(10, 7))

for i, name in enumerate(location_names):
    row_bg = "#EAF4FF" if i == 0 else "#F8FAFE"
    row = tk.Frame(left_panel, bg=row_bg)
    row.pack(fill="x", padx=8, pady=3)

    tk.Label(
        row,
        text="●",
        font=("Arial", 14, "bold"),
        fg=location_colours[i],
        bg=row_bg
    ).pack(side="left", padx=6, pady=5)

    tk.Label(
        row,
        text=name,
        font=("Arial", 9, "bold"),
        fg=TEXT,
        bg=row_bg,
        anchor="w"
    ).pack(side="left", fill="x", expand=True)

    x, y = locations[i]

    tk.Label(
        row,
        text=f"({x}, {y})",
        font=("Arial", 8),
        fg=TEXT,
        bg=row_bg
    ).pack(side="right", padx=5)

tk.Label(
    left_panel,
    text="DELIVERY BOX",
    font=("Arial", 12, "bold"),
    fg=YELLOW,
    bg=WHITE
).pack(pady=10)


# MIDDLE PANEL: ALGORITHM RESULTS
middle_panel = tk.Frame(dashboard, bg=BG)
middle_panel.grid(
    row=0, column=1,
    sticky="nsew", padx=6
)

tk.Label(
    middle_panel,
    text="ALGORITHM RESULTS",
    font=("Arial", 13, "bold"),
    fg=DARK_BLUE,
    bg=BG
).pack(pady=(2, 8))

result_labels = {}


def create_result_card(title, colour, number):
    card = tk.Frame(
        middle_panel,
        bg=WHITE,
        highlightbackground=colour,
        highlightthickness=2
    )
    card.pack(fill="x", pady=4)

    tk.Label(
        card,
        text=f"{number}   {title}",
        font=("Arial", 10, "bold"),
        fg=colour,
        bg=WHITE,
        anchor="w"
    ).pack(fill="x", padx=9, pady=(6, 2))

    route_label = tk.Label(
        card,
        text="Route: Not calculated yet",
        font=("Arial", 8),
        fg=TEXT,
        bg=WHITE,
        anchor="w",
        justify="left",
        wraplength=350
    )
    route_label.pack(fill="x", padx=9, pady=2)

    distance_label = tk.Label(
        card,
        text="Distance: -- units",
        font=("Arial", 9, "bold"),
        fg=TEXT,
        bg=WHITE,
        anchor="w"
    )
    distance_label.pack(fill="x", padx=9, pady=2)

    time_label = tk.Label(
        card,
        text="Execution time: -- seconds",
        font=("Arial", 8),
        fg=TEXT,
        bg=WHITE,
        anchor="w"
    )
    time_label.pack(fill="x", padx=9, pady=(2, 6))

    result_labels[title] = (
        route_label, distance_label, time_label
    )


create_result_card("Nearest Neighbor", BLUE, "1")
create_result_card("2-Opt Optimization", GREEN, "2")
create_result_card("Brute Force", PURPLE, "3")

summary_label = tk.Label(
    middle_panel,
    text="Click Calculate Best Route to begin.",
    font=("Arial", 9, "bold"),
    fg=PURPLE,
    bg="#EEE8FF",
    wraplength=350,
    pady=7
)
summary_label.pack(fill="x", pady=6)


# RIGHT PANEL: DELIVERY PLAN
right_panel = tk.Frame(
    dashboard,
    bg=WHITE,
    highlightbackground="#D5E3F5",
    highlightthickness=1
)
right_panel.grid(
    row=0, column=2,
    sticky="nsew", padx=(6, 0)
)

tk.Label(
    right_panel,
    text="YOUR DELIVERY PLAN",
    font=("Arial", 11, "bold"),
    fg=PURPLE,
    bg=WHITE,
    wraplength=180
).pack(pady=(12, 10))

tk.Label(
    right_panel,
    text="Visit every customer and return to the warehouse.",
    font=("Arial", 9),
    fg=TEXT,
    bg=WHITE,
    wraplength=180,
    justify="center"
).pack(pady=5)

tk.Label(
    right_panel,
    text="HOW IT WORKS",
    font=("Arial", 10, "bold"),
    fg=BLUE,
    bg=WHITE
).pack(pady=(15, 7))

for item in [
    "1. Calculate distances",
    "2. Find a delivery route",
    "3. Improve the route",
    "4. Compare algorithms"
]:
    tk.Label(
        right_panel,
        text=item,
        font=("Arial", 9),
        fg=TEXT,
        bg=WHITE,
        anchor="w",
        wraplength=180
    ).pack(fill="x", padx=10, pady=6)


# BUTTON STYLE
def make_button(parent, text, colour, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=colour,
        fg=WHITE,
        activebackground=DARK_BLUE,
        activeforeground=WHITE,
        font=("Arial", 9, "bold"),
        relief="flat",
        cursor="hand2",
        padx=5,
        pady=7
    )


# CALCULATE AND DISPLAY RESULTS
def show_results():
    try:
        matrix = create_distance_matrix(locations)

        start = perf_counter()
        nn_route = nearest_neighbor(matrix)
        nn_time = perf_counter() - start
        nn_dist = route_distance(nn_route, matrix)

        start = perf_counter()
        opt_route = two_opt(nn_route, matrix)
        opt_time = perf_counter() - start
        opt_dist = route_distance(opt_route, matrix)

        start = perf_counter()
        exact_route, exact_dist = brute_force(matrix)
        brute_time = perf_counter() - start

        results = [
            ("Nearest Neighbor", nn_route, nn_dist, nn_time),
            ("2-Opt Optimization", opt_route, opt_dist, opt_time),
            ("Brute Force", exact_route, exact_dist, brute_time)
        ]

        for title, route, dist, elapsed in results:
            route_text = " -> ".join(
                location_names[i] for i in route
            )

            route_label, distance_label, time_label = (
                result_labels[title]
            )

            route_label.config(text=f"Route: {route_text}")
            distance_label.config(
                text=f"Distance: {dist:.2f} units"
            )
            time_label.config(
                text=f"Execution time: {elapsed:.6f} seconds"
            )

        summary_label.config(
            text=f"Shortest distance: {exact_dist:.2f} units\n"
                 "Brute Force finds the exact optimum."
        )

        print("\n========== SMARTDROP RESULTS ==========")

        for title, route, dist, elapsed in results:
            print(f"\n{title}")
            print(
                "Route:",
                " -> ".join(location_names[i] for i in route)
            )
            print(f"Distance: {dist:.2f} units")
            print(f"Execution time: {elapsed:.6f} seconds")

    except Exception as error:
        messagebox.showerror("Error", str(error))


# DISPLAY THE BEST ROUTE GRAPH
def display_best_route():
    matrix = create_distance_matrix(locations)
    route, _ = brute_force(matrix)
    show_route_graph(route)


# BUTTONS
make_button(
    left_panel,
    "Calculate Best Route",
    BLUE,
    show_results
).pack(fill="x", padx=10, pady=(5, 5))

make_button(
    left_panel,
    "View Route Graph",
    GREEN,
    display_best_route
).pack(fill="x", padx=10, pady=5)

make_button(
    left_panel,
    "Exit",
    RED,
    root.destroy
).pack(fill="x", padx=10, pady=5)


# FOOTER
tk.Label(
    root,
    text="Efficient Delivery  |  Optimal Routes  |  Happier Customers",
    font=("Arial", 9, "bold"),
    fg=DARK_BLUE,
    bg=YELLOW,
    pady=7
).pack(fill="x", side="bottom")


# START APPLICATION
root.mainloop()
