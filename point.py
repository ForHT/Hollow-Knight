# point.py
class Point:
    """位置坐标，附带move函数"""
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def move(self, dx, dy):
        """移动，右下为正"""
        self.x += dx
        self.y += dy