import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import re


def extract_number(segment_string):
    match = re.search(r'\d+', segment_string)
    if match:
        return int(match.group(0))
    return None

class MouseEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'MouseEvent(x={self.x}, y={self.y})'

class Segment:
    def __init__(self, segment_id, x, y, name, is_master):
        self.segment_id = segment_id
        self.x = x
        self.y = y
        self.name = name
        self.is_master = is_master

    def __repr__(self):
        return (f"Segment(ID={self.segment_id}, X={self.x}, Y={self.y}, "
                f"Name={self.name}, IsMaster={self.is_master})")

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    segments = root.findall(".//Group[@ID='Segments']/Group")
    segment_list = []

    for segment in segments:
        segment_id = segment.attrib['ID']
        x_property = segment.find("Property[@ID='X']")
        y_property = segment.find("Property[@ID='Y']")
        name_property = segment.find("Property[@ID='Name']")
        is_master_property = segment.find("Property[@ID='IsMaster']")

        x_value = x_property.get('Value') if x_property is not None else None
        y_value = y_property.get('Value') if y_property is not None else None
        name_value = name_property.get('Value') if name_property is not None else None
        is_master_value = is_master_property.get('Value') if is_master_property is not None else None

        segment_instance = Segment(segment_id, x_value, y_value, name_value, is_master_value)
        segment_list.append(segment_instance)

    return segment_list

def setup_plot(segment_list):
    fig, ax = plt.subplots()
    key_points = []
    markers = []
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'cyan']
    default_colors = colors.copy()
    squares = []

    for segment in segment_list:
        if segment.x is not None and segment.y is not None:
            x = float(segment.x) * 0.24
            y = float(segment.y) * 0.24
            size = 0.24

            x_index = int(segment.x)
            color_index = int(x_index // 3) % len(colors)
            color = colors[color_index]

            for i in range(2):
                for j in range(2):
                    small_x = x + (i * size / 2)
                    small_y = y + (j * size / 2)

                    corners = [
                        (small_x, small_y),
                        (small_x + size / 2, small_y),
                        (small_x, small_y + size / 2),
                        (small_x + size / 2, small_y + size / 2),
                        (small_x + size / 4, small_y + size / 4)
                    ]

                    key_points.extend(corners)

                    square_patch = plt.Rectangle((small_x, small_y), size / 2, size / 2, fill=True,
                                                  edgecolor='black', facecolor=color)
                    ax.add_patch(square_patch)

                    squares.append({
                        'patch': square_patch,
                        'original_color': color,
                        'segment_id': extract_number(segment.segment_id),
                        'position': (small_x, small_y)
                    })

                    if i == 0 and j == 0:
                        ax.text(small_x + size / 4, small_y + size / 4, extract_number(segment.segment_id),
                                ha='center', va='center', fontsize=12, color='white')

    text = ax.text(0, 0, '', fontsize=12, color='black')

    def on_move(event):
        if event.inaxes:
            mouse_x, mouse_y = event.xdata, event.ydata
            closest_point = None
            min_distance = float('inf')

            for point in key_points:
                distance = np.sqrt((mouse_x - point[0]) ** 2 + (mouse_y - point[1]) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point

            if min_distance < 0.1:
                text.set_position(closest_point)
                text.set_text(f'({closest_point[0]:.2f}, {closest_point[1]:.2f})')

                if markers:
                    for marker in markers:
                        marker.remove()
                    markers.clear()

                marker = ax.plot(closest_point[0], closest_point[1], 'ro', markersize=8)
                markers.append(marker[0])
            else:
                text.set_text('')

            fig.canvas.draw_idle()

    def on_click(event):
        global click_color_index

        if event.inaxes:
            mouse_x, mouse_y = event.xdata, event.ydata

            def contain_point(rect, point):
                left_bottom_x = rect.get_x()
                left_bottom_y = rect.get_y()
                right_top_x = left_bottom_x + rect.get_width()
                right_top_y = left_bottom_y + rect.get_height()

                return (point.x > left_bottom_x and point.x < right_top_x) and (point.y > left_bottom_y and point.y < right_top_y)

            for square in squares:
                rect = square['patch']
                mouse_event = MouseEvent(mouse_x, mouse_y)
                if contain_point(rect, mouse_event):
                    new_color = colors[click_color_index % len(colors)]
                    click_color_index += 1
                    rect.set_facecolor(new_color)
                    fig.canvas.draw_idle()
                    break

    fig.canvas.mpl_connect('motion_notify_event', on_move)
    fig.canvas.mpl_connect('button_press_event', on_click)

    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal', adjustable='box')

    plt.show()

def main():
    segment_list = parse_xml('CfgLayout.layout6d')
    setup_plot(segment_list)

if __name__ == "__main__":
    click_color_index = 0
    main()
