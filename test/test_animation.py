import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from game.core.animation_system import AnimationSystem
from game.interfaces import Entity, EntityType, Vector2

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 创建动画系统
animation_system = AnimationSystem()

# 加载 idle 动画
for i in range(9):
    frame = pygame.image.load(f"assets/sprites/player/idle/{i}.PNG").convert_alpha()
    animation_system.load_animation("player_idle", frame, 9, 0.1)

# 创建玩家实体
player = Entity(EntityType.PLAYER, Vector2(400, 300))

# 开始播放动画
animation_system.play_animation(player, "player_idle", True)

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    dt = clock.tick(60) / 1000.0
    
    # 更新动画
    animation_system.update(dt)
    
    # 绘制
    screen.fill((0, 0, 0))
    current_frame = animation_system.get_current_frame(player)
    if current_frame:
        screen.blit(current_frame, (player.position.x, player.position.y))
    
    pygame.display.flip()