# actor.py
import pygame
from vector2 import Vector2
from point import Point

class Actor:
    def __init__(self, nx=0.0, ny=0.0):
        self.gravity = 2.5
        self.acceleration = 0.0
        self.speed = Vector2()
        self.attackdir = Vector2()
        self.position = Point(nx, ny)
        self.HP = 3
        self.CanBeHurt = True 
        self.UnHurtableTime = 0
        self.Facing_Right = True

    def messagedealer(self):
        """
        处理键盘输入并返回操作码。
        移动: A/D, 跳跃: K, 攻击: J, 冲刺: L
        *** 修正: 调整了判断优先级以修复跳跃bug ***
        """
        keys = pygame.key.get_pressed()
        
        # 新键位
        K_A, K_D = keys[pygame.K_a], keys[pygame.K_d]
        K_W, K_S = keys[pygame.K_w], keys[pygame.K_s]
        K_J, K_L, K_K = keys[pygame.K_j], keys[pygame.K_l], keys[pygame.K_k] # 攻击, 冲刺, 跳跃
        K_UP, K_DOWN = keys[pygame.K_UP], keys[pygame.K_DOWN]

        # 1. 攻击判断 (最高优先级)
        if (K_W and K_J) or (K_UP and K_J): return 5
        if (K_S and K_J) or (K_DOWN and K_J): return 7
        if K_J:
            if K_D: self.Facing_Right = True
            elif K_A: self.Facing_Right = False
            return 2

        # 2. 冲刺判断
        if K_L:
            if K_D: self.Facing_Right = True
            elif K_A: self.Facing_Right = False
            return 4 # C++代码中3和4都代表冲刺，这里统一为4

        # 3. 跳跃判断
        if K_K and self.position.y >= 680:
            return 6

        # 4. 移动判断
        if K_A:
            if K_D: # 左右同时按，不动
                self.speed.vx = 0
                return 0
            self.Facing_Right = False
            self.speed.vx = -10
            return 1
            
        if K_D:
            self.Facing_Right = True
            self.speed.vx = 10
            return 1
        
        # 5. 默认状态：静止
        self.speed.vx = 0
        return 0