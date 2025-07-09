import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.animation_system import AnimationSystem
from interfaces import Entity, EntityType, Vector2, GameState
from config.animation_data import PLAYER_ANIMATIONS
from configs import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_GROUND_Y
from systems.combat import CombatSystem
from systems.physics import PhysicsSystem
from gameplay.player import Player, Effect
from gameplay.boss import Boss

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# 设置窗口标题
pygame.display.set_caption("Hollow Knight Clone")
game_state = GameState.START_SCREEN

# 创建动画系统
animation_system = AnimationSystem()
physics_system = PhysicsSystem(screen.get_rect())
combat_system = CombatSystem(physics_system)

# 使用新的加载方法
animation_system.load_animations(PLAYER_ANIMATIONS)

# 初始化实体
player: Player = Player(pos=Vector2(200, PLAYER_GROUND_Y), size=(50, 80))
# dash_effect_entity 不再需要，特效将由新的系统处理
# boss: Boss = Boss(pos=Vector2(800, 585), size=(100, 150))
entities: list = [player] #, boss]
for entity in entities:
    physics_system.add_entity(entity) 

# """待封装：加载实体资源"""  -> 已由AnimationSystem处理
# animation_system.load_animations_from_config("player", PLAYER_ANIMATIONS, ANIMATION_PATHS["player"])
# animation_system.load_animations_from_config("", EFFECT_ANIMATIONS, ANIMATION_PATHS["effects"])

"""待封装：绘制玩家的血量。"""
def draw_player_health(player : Player):
        health_icon_radius = 15
        padding = 10
        start_x = 30
        start_y = 30
        for i in range(player.max_health):
            x = start_x + i * (2 * health_icon_radius + padding)
            # 先绘制空的血槽
            pygame.draw.circle(screen, (50, 50, 50), (x, start_y), health_icon_radius, 2)
            if i < player.health:
                # 如果有血量则填充
                pygame.draw.circle(screen, (255, 255, 255), (x, start_y), health_icon_radius)

# 设置游戏状态
game_state = GameState.PLAYING

while running:
    dt = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # --- Updates based on state ---
    if game_state == GameState.PLAYING:
        keys = pygame.key.get_pressed()
        player.update(keys, animation_system)
        # boss.update(player.position)
        physics_system.update()
        # combat_system.update(player, [boss])
        
        # 更新动画
        animation_system.play_animation(player, player.state)
        animation_system.update(dt)

        if player.health <= 0:
            game_state = GameState.GAME_OVER
        # elif boss.health <= 0:
        #     game_state = GameState.VICTORY

    # 绘制
    screen.fill((0, 0, 0))
    
    # 新的绘制逻辑
    current_frame = animation_system.get_current_frame(player)
    if current_frame:
        # Correctly calculate the top-left position for blitting
        frame_rect = current_frame.get_rect()
        frame_rect.midbottom = (int(player.position.x), int(player.position.y))
        screen.blit(current_frame, frame_rect.topleft)
    
    if game_state == GameState.PLAYING:
        # 保留调试用的绿框
        player.draw(screen, Vector2(0,0))
        # boss.draw(screen, Vector2(0,0)) # Keep boss rect for now
        draw_player_health(player)
        # 绘制调试用的攻击框
        if "attack" in player.state:
            player_attack = player.get_attack_hitbox()
            if player_attack:
                pygame.draw.rect(screen, (255, 255, 0), player_attack, 2)
    
    pygame.display.flip()