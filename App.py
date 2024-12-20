# Conversion functions
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math


# Conversion functions
def convert_to_imperial(value_mm):
    return value_mm / 25.4


def convert_to_metric(value_inch):
    return value_inch * 25.4


# Geometry functions
def calculate_center_rectangle(x1, x2, y1, y2, z1, z2):
    """Calculate the center of a rectangle."""
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    z_center = (z1 + z2) / 2
    return x_center, y_center, z_center


def calculate_center_circle(x1, x2, y1, y2):
    """Calculate the center of a circle."""
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    return x_center, y_center


def calculate_custom_location(x1, x2, y1, y2, offset_right, offset_top):
    """Calculate custom location based on offsets."""
    x_custom = x2 - offset_right  # Offset from the right edge
    y_custom = y1 + offset_top  # Offset from the top edge
    return x_custom, y_custom


def calculate_polygon_centroid(vertices):
    """Calculate the centroid of a polygon."""
    area = 0
    cx = 0
    cy = 0

    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        temp = x1 * y2 - x2 * y1
        area += temp
        cx += (x1 + x2) * temp
        cy += (y1 + y2) * temp

    area *= 0.5
    cx /= (6 * area)
    cy /= (6 * area)
    return cx, cy


# Visualization functions
def draw_visualization(canvas, x1, x2, y1, y2, points=None, centroid=None):
    """Draw the part and calculated points on the canvas."""
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    # Handle zero dimensions to avoid division errors
    if x1 == x2 or y1 == y2:
        return

    # Set unit label
    unit_label = "mm" if xyz_unit_var.get() == "Metric (mm)" else "in"

    # Normalize coordinates to fit canvas
    part_width = abs(x2 - x1)
    part_height = abs(y2 - y1)

    # Calculate scaling factor to fit part inside canvas, leaving a margin
    margin_ratio = 0.1  # 10% margin on all sides
    available_width = width * (1 - 2 * margin_ratio)
    available_height = height * (1 - 2 * margin_ratio)

    scale_x = available_width / part_width
    scale_y = available_height / part_height
    scale = min(scale_x, scale_y)  # Use the smallest scale to ensure the part fits

    # Calculate offsets to center the part on the canvas with margin
    margin_x = width * margin_ratio
    margin_y = height * margin_ratio

    # Offsets to properly align negative coordinates within the canvas
    offset_x = margin_x - (min(x1, x2) * scale)
    offset_y = margin_y - (min(y1, y2) * scale)

    # Determine which shape to draw based on the selected type
    shape = shape_var.get()

    if shape == "Rectangle":
        # Draw rectangle
        normalized_x1 = offset_x + (x1 * scale)
        normalized_y1 = offset_y + (y1 * scale)
        normalized_x2 = offset_x + (x2 * scale)
        normalized_y2 = offset_y + (y2 * scale)

        canvas.create_rectangle(normalized_x1, normalized_y1, normalized_x2, normalized_y2, outline="blue", width=2)

        # Calculate and draw the center point for the rectangle
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        # Normalize center coordinates to fit canvas
        normalized_center_x = offset_x + (center_x * scale)
        normalized_center_y = offset_y + (center_y * scale)

        # Draw the center point
        canvas.create_oval(
            normalized_center_x - 5, normalized_center_y - 5, normalized_center_x + 5, normalized_center_y + 5, fill="red"
        )
        canvas.create_text(normalized_center_x + 10, normalized_center_y, text="Center", anchor="w", fill="red")

    elif shape == "Circle":
        # Draw circle with its diameter
        diameter = abs(x2 - x1)
        if xyz_unit_var.get() == "Imperial (inches)":
            diameter = convert_to_imperial(diameter)

        # Calculate circle's center and radius
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        radius = (diameter / 2) * scale

        # Normalize center coordinates to fit canvas
        normalized_center_x = offset_x + (center_x * scale)
        normalized_center_y = offset_y + (center_y * scale)

        # Draw the circle
        canvas.create_oval(
            normalized_center_x - radius, normalized_center_y - radius,
            normalized_center_x + radius, normalized_center_y + radius,
            outline="blue", width=2
        )

        # Draw the center point
        canvas.create_oval(
            normalized_center_x - 5, normalized_center_y - 5, normalized_center_x + 5, normalized_center_y + 5, fill="red"
        )
        canvas.create_text(normalized_center_x + 10, normalized_center_y, text="Center", anchor="w", fill="red")

        # Show the diameter label
        canvas.create_text(normalized_center_x, normalized_center_y + radius + 20,
                           text=f"Diameter: {diameter:.2f} {unit_label}", anchor="n", fill="blue")

    # Draw zero point relative to the part's coordinates
    zero_x = 0
    zero_y = 0

    # Normalize zero coordinates to fit canvas
    normalized_zero_x = offset_x + (zero_x - x1) * scale
    normalized_zero_y = offset_y + (zero_y - y1) * scale

    # Draw the zero point
    canvas.create_oval(
        normalized_zero_x - 5, normalized_zero_y - 5, normalized_zero_x + 5, normalized_zero_y + 5, fill="black"
    )
    canvas.create_text(normalized_zero_x - 10, normalized_zero_y - 10, text="Zero Point", anchor="se", fill="black")

    # Draw distances from edges if applicable
    if xyz_unit_var.get() == "Imperial (inches)":
        # Convert distances to imperial for display
        part_width = convert_to_imperial(part_width)
        part_height = convert_to_imperial(part_height)

    if shape == "Rectangle":
        # Display distances from edges for rectangles
        canvas.create_text(normalized_x1, normalized_y1 - 20, text=f"Width: {part_width:.2f} {unit_label}", anchor="w", fill="blue")
        canvas.create_text(normalized_x1, normalized_y1 - 40, text=f"Height: {part_height:.2f} {unit_label}", anchor="w", fill="blue")

    # Draw specific location points (e.g., offsets or custom locations) if specified
    if points:
        for point in points:
            x, y = point
            normalized_x = offset_x + (x * scale)
            normalized_y = offset_y + (y * scale)
            canvas.create_oval(
                normalized_x - 3, normalized_y - 3, normalized_x + 3, normalized_y + 3, fill="green"
            )





def handle_canvas_resize(event, canvas):
    try:
        # Get current input values
        x1 = float(x1_entry.get() or 0)
        x2 = float(x2_entry.get() or 0)
        y1 = float(y1_entry.get() or 0)
        y2 = float(y2_entry.get() or 0)
        points = []  # Optionally, include any points you want to draw again
        centroid = None  # Optionally, include centroid if calculated
        
        # Redraw the visualization
        draw_visualization(canvas, x1, x2, y1, y2, points=points, centroid=centroid)
    except ValueError:
        # Handle any invalid inputs gracefully during resize
        pass

# Calculation function
def calculate():
    try:
        # Get input values including Z-axis
        shape = shape_var.get()
        x1 = float(x1_entry.get() or 0)
        x2 = float(x2_entry.get() or 0)
        y1 = float(y1_entry.get() or 0)
        y2 = float(y2_entry.get() or 0)

        
        # Provide default values for z1 and z2
        z1 = 0
        z2 = 0

        # Only use user inputs for z1 and z2 if the Z-axis is enabled
        if z_axis_var.get():
            z1 = float(z1_entry.get())
            z2 = float(z2_entry.get())

        # Convert units if necessary
        if xyz_unit_var.get() == "Imperial (inches)":
            x1, x2, y1, y2, z1, z2 = map(convert_to_metric, (x1, x2, y1, y2, z1, z2))

        # Determine calculation type
        if shape == "Rectangle":
            # Always pass z1 and z2 values, even if they're default to 0
            x_center, y_center, z_center = calculate_center_rectangle(x1, x2, y1, y2, z1, z2)
            result_text = f"Rectangle Center: X={x_center:.4f}, Y={y_center:.4f}, Z={z_center:.4f}"
            draw_visualization(canvas, x1, x2, y1, y2, centroid=(x_center, y_center))

        shank_diameter = float(shank_diameter_entry.get())
        if endmill_unit_var.get() == "Imperial (inches)":
            shank_diameter = convert_to_metric(shank_diameter)

        endmill_radius = shank_diameter / 2

        # Determine calculation type for specific location or shapes
        if specific_location_var.get():
            offset_right = float(offset_right_entry.get())
            offset_top = float(offset_top_entry.get())

            # Convert offset units if necessary
            if xyz_unit_var.get() == "Imperial (inches)":
                offset_right, offset_top = map(convert_to_metric, (offset_right, offset_top))

            x_loc, y_loc = calculate_custom_location(x1, x2, y1, y2, offset_right, offset_top)
            x_loc -= endmill_radius
            y_loc -= endmill_radius
            result_text = f"Custom Location: X={x_loc:.4f}, Y={y_loc:.4f}"
            draw_visualization(canvas, x1, x2, y1, y2, points=[(x_loc, y_loc)])
        elif shape == "Rectangle":
            # Pass z1 and z2 values, even if they're default to 0
            x_center, y_center, z_center = calculate_center_rectangle(x1, x2, y1, y2, z1, z2)
            x_center -= endmill_radius
            y_center -= endmill_radius
            result_text = f"Rectangle Center: X={x_center:.4f}, Y={y_center:.4f}, Z={z_center:.4f}"
            draw_visualization(canvas, x1, x2, y1, y2, centroid=(x_center, y_center))
        elif shape == "Circle":
            x_center, y_center = calculate_center_circle(x1, x2, y1, y2)
            x_center -= endmill_radius
            y_center -= endmill_radius
            result_text = f"Circle Center: X={x_center:.4f}, Y={y_center:.4f}"
            draw_visualization(canvas, x1, x2, y1, y2, centroid=(x_center, y_center))
        elif shape == "Polygon":
            vertices = []
            for vertex in polygon_entries:
                x = float(vertex[0].get())
                y = float(vertex[1].get())
                if xyz_unit_var.get() == "Imperial (inches)":
                    x, y = convert_to_metric(x), convert_to_metric(y)
                vertices.append((x, y))

            centroid_x, centroid_y = calculate_polygon_centroid(vertices)
            centroid_x -= endmill_radius
            centroid_y -= endmill_radius
            result_text = f"Polygon Centroid: X={centroid_x:.4f}, Y={centroid_y:.4f}"
            draw_visualization(canvas, x1, x2, y1, y2, points=vertices, centroid=(centroid_x, centroid_y))
        else:
            raise ValueError("Unsupported shape")

        # Update the result label and add to history
        result_label.config(text=result_text)
        add_to_history(result_text)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Add history
def add_to_history(entry):
    history_list.insert(tk.END, entry)
    history.append(entry)

# Function to update Z-axis field visibility based on checkbox state
def update_z_fields():
    global z1_entry, z2_entry
    z_widgets = [z1_entry, z2_entry]
    for widget in z_widgets:
        if z_axis_var.get():
            widget.grid()  # Show the widget if Z-axis is enabled
        else:
            widget.grid_remove()  # Hide the widget if Z-axis is disabled

# Initially hide Z fields based on checkbox state

# Save history
def save_history():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as file:
            for item in history:
                file.write(item + "\n")
        messagebox.showinfo("Success", "History saved successfully.")


# Clear history
def clear_history():
    history.clear()
    history_list.delete(0, tk.END)


# Update GUI for shape
def update_gui(*args):
    for widget in polygon_frame.winfo_children():
        widget.grid_forget()

    if shape_var.get() == "Polygon":
        for i, vertex in enumerate(polygon_entries):
            ttk.Label(polygon_frame, text=f"Vertex {i + 1} (X, Y):").grid(row=i, column=0, padx=5, pady=5)
            vertex[0].grid(row=i, column=1, padx=5, pady=5)
            vertex[1].grid(row=i, column=2, padx=5, pady=5)
        add_vertex_button.grid(row=len(polygon_entries), column=0, padx=5, pady=5)
        remove_vertex_button.grid(row=len(polygon_entries), column=1, padx=5, pady=5)
    else:
        for widget in polygon_frame.winfo_children():
            widget.grid_forget()


# Add/remove vertices
def add_vertex():
    x_entry = ttk.Entry(polygon_frame, width=10)
    y_entry = ttk.Entry(polygon_frame, width=10)
    polygon_entries.append((x_entry, y_entry))
    update_gui()


def remove_vertex():
    if polygon_entries:
        x_entry, y_entry = polygon_entries.pop()
        x_entry.destroy()
        y_entry.destroy()
    update_gui()


# GUI setup
root = tk.Tk()
root.title("CNC Utility")
root.geometry("1000x800")
root.rowconfigure(15, weight=1)  # Make the canvas row resizable
root.columnconfigure(0, weight=1)  # Make the canvas column resizable
root.columnconfigure(1, weight=1)

# Shape selection
shape_var = tk.StringVar(value="Rectangle")
shape_var.trace("w", update_gui)
ttk.Label(root, text="Shape:").grid(row=0, column=0, padx=5, pady=5)
ttk.Combobox(root, textvariable=shape_var, values=["Rectangle", "Circle", "Polygon"], state="readonly").grid(
    row=0, column=1, padx=5, pady=5
)

# Unit selection
xyz_unit_var = tk.StringVar(value="Metric (mm)")
ttk.Label(root, text="XYZ Units:").grid(row=1, column=0, padx=5, pady=5)
ttk.Combobox(root, textvariable=xyz_unit_var, values=["Metric (mm)", "Imperial (inches)"], state="readonly").grid(
    row=1, column=1, padx=5, pady=5
)

endmill_unit_var = tk.StringVar(value="Metric (mm)")
ttk.Label(root, text="End Mill Units:").grid(row=2, column=0, padx=5, pady=5)
ttk.Combobox(root, textvariable=endmill_unit_var, values=["Metric (mm)", "Imperial (inches)"], state="readonly").grid(
    row=2, column=1, padx=5, pady=5
)

# Rectangle inputs
ttk.Label(root, text="X1 (Left Edge):").grid(row=3, column=0, padx=5, pady=5)
x1_entry = ttk.Entry(root)
x1_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(root, text="X2 (Right Edge):").grid(row=4, column=0, padx=5, pady=5)
x2_entry = ttk.Entry(root)
x2_entry.grid(row=4, column=1, padx=5, pady=5)

ttk.Label(root, text="Y1 (Top Edge):").grid(row=5, column=0, padx=5, pady=5)
y1_entry = ttk.Entry(root)
y1_entry.grid(row=5, column=1, padx=5, pady=5)

ttk.Label(root, text="Y2 (Bottom Edge):").grid(row=6, column=0, padx=5, pady=5)
y2_entry = ttk.Entry(root)
y2_entry.grid(row=6, column=1, padx=5, pady=5)

z_axis_var = tk.BooleanVar()
ttk.Checkbutton(root, text="Enable Z-Axis", variable=z_axis_var, command=lambda: update_z_fields()).grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Z inputs
ttk.Label(root, text="Z1 (Top Face):").grid(row=8, column=0, padx=5, pady=5)
z1_entry = ttk.Entry(root)
z1_entry.grid(row=8, column=1, padx=5, pady=5)

z1_entry.grid_remove()  # Initially hidden

ttk.Label(root, text="Z2 (Bottom Face):").grid(row=9, column=0, padx=5, pady=5)
z2_entry = ttk.Entry(root)
z2_entry.grid(row=9, column=1, padx=5, pady=5)

z2_entry.grid_remove()  # Initially hidden

# Shank diameter
ttk.Label(root, text="End Mill Diameter:").grid(row=10, column=0, padx=5, pady=5)
shank_diameter_entry = ttk.Entry(root)
shank_diameter_entry.grid(row=10, column=1, padx=5, pady=5)

# Offset inputs
specific_location_var = tk.BooleanVar()
ttk.Checkbutton(root, text="Use Specific Location", variable=specific_location_var).grid(row=11, column=0, columnspan=2)

ttk.Label(root, text="Offset from Right Edge:").grid(row=12, column=0, padx=5, pady=5)
offset_right_entry = ttk.Entry(root)
offset_right_entry.grid(row=12, column=1, padx=5, pady=5)

ttk.Label(root, text="Offset from Top Edge:").grid(row=13, column=0, padx=5, pady=5)
offset_top_entry = ttk.Entry(root)
offset_top_entry.grid(row=13, column=1, padx=5, pady=5)

# Polygon inputs
polygon_frame = tk.Frame(root)
polygon_frame.grid(row=14, column=0, columnspan=2, padx=5, pady=5)
polygon_entries = []

add_vertex_button = ttk.Button(polygon_frame, text="Add Vertex", command=add_vertex)
remove_vertex_button = ttk.Button(polygon_frame, text="Remove Vertex", command=remove_vertex)

# Canvas for visualization
canvas = tk.Canvas(root, bg="white")
canvas.grid(row=15, column=0, columnspan=2, pady=10, sticky="nsew")
# Add this line directly after canvas creation
canvas.bind("<Configure>", lambda event: handle_canvas_resize(event, canvas))

# History
history = []
ttk.Label(root, text="History:").grid(row=16, column=0, padx=5, pady=5, sticky="w")
history_list = tk.Listbox(root, height=10, width=50)
history_list.grid(row=17, column=0, columnspan=2, pady=5, sticky="nsew")

# Allow dynamic resizing of history and canvas
root.rowconfigure(17, weight=1)
root.rowconfigure(15, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Save and clear history buttons
ttk.Button(root, text="Save History", command=save_history).grid(row=18, column=0, padx=5, pady=5)
ttk.Button(root, text="Clear History", command=clear_history).grid(row=18, column=1, padx=5, pady=5)

# Result label
result_label = ttk.Label(root, text="Results will appear here", font=("Arial", 12))
result_label.grid(row=19, column=0, columnspan=2, pady=10)

# Calculate button
ttk.Button(root, text="Calculate", command=calculate).grid(row=20, column=0, columnspan=2, pady=10)

update_gui()
root.mainloop()
