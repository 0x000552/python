"""
Create a scale-dependent visualization of two points
"""


def viz_two_points(x=13.2, y=17.3, value=14.7, scale=10):
    if value < x or x > y:
        raise ValueError("Argument rule: value > x and x < y")
    step = (y - x) / scale
    v_pos = round((value - x) / step)
    print(f"[{'*':->{v_pos}}{']':->{scale-v_pos+1}}")


viz_two_points()
viz_two_points(x=10, y=99, value=99, scale=100)
viz_two_points(x=100, y=99, value=99, scale=100)
