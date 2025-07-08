# vector2.py
import math

class Vector2:
    """二维向量:x轴向右为正，y轴向下为正"""
    def __init__(self, vx=0.0, vy=0.0):
        self.vx = float(vx)
        self.vy = float(vy)

    def __repr__(self):
        return f"Vector2({self.vx}, {self.vy})"

    def get_module(self):
        """计算向量的模长"""
        return math.sqrt(self.vx**2 + self.vy**2)

    def normalize(self):
        """返回单位化的新向量"""
        module = self.get_module()
        if module == 0:
            return Vector2(0, 0)
        return Vector2(self.vx / module, self.vy / module)