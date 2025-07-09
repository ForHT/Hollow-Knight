import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.animation_system import AnimationSystem
from interfaces import Entity, EntityType, Vector2, GameState, AnimationState
from config.states import PLAYER_ANIMATIONS, PLAYER_STATE_MACHINE, ANIMATION_PATHS, EFFECT_ANIMATIONS
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

# 初始化实体
player: Player = Player(pos=Vector2(200, PLAYER_GROUND_Y), size=(50, 80))
current_state = AnimationState.IDLE
dash_effect_entity = Effect(pos=Vector2(player.position.x, player.position.y))
boss: Boss = Boss(pos=Vector2(800, 585), size=(100, 150))
entities: list = [player, boss]
for entity in entities:
    physics_system.add_entity(entity) 

"""待封装：加载实体资源""" 
# 加载所有玩家动画
for state, config in PLAYER_ANIMATIONS.items():
    frames_path = ANIMATION_PATHS["player"][state]  # 更新路径获取方式
    for frame in range(config["frames"]):
        path = frames_path.format(frame=frame)
        try:
            frame_surface = pygame.image.load(path).convert_alpha()
            animation_system.load_animation(
                f"player_{state}", 
                frame_surface, 
                config["frames"], 
                config["frame_time"]
            )
        except pygame.error as e:
            print(f"Error loading animation frame: {path}")
            print(f"Error details: {e}")

# 加载所有特效动画
for effect, config in EFFECT_ANIMATIONS.items():
    frames_path = ANIMATION_PATHS["effects"][effect]  # 修改这里，使用正确的路径结构
    for frame in range(config["frames"]):
        path = frames_path.format(frame=frame)
        try:
            frame_surface = pygame.image.load(path).convert_alpha()
            animation_system.load_animation(
                effect,
                frame_surface, 
                config["frames"], 
                config["frame_time"]
            )
        except pygame.error as e:
            print(f"Error loading effect frame: {path}")
            print(f"Path attempted: {path}")

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
        player.update(keys)
        dash_effect_entity.position = player.position
        boss.update(player.position)
        physics_system.update()
        combat_system.update(player, [boss])
        # 更新动画
        animation_system.play_animation(player, f"{player.state}".lower(), PLAYER_ANIMATIONS[f"{player.state}".lower()]["loop"])
        animation_system.play_animation(dash_effect_entity, "dash_effect", EFFECT_ANIMATIONS["dash_effect"]["loop"])
        animation_system.update(dt)

        if player.health <= 0:
            game_state = GameState.GAME_OVER
        elif boss.health <= 0:
            game_state = GameState.VICTORY

    # 绘制
    screen.fill((0, 0, 0))
    current_frame = animation_system.get_current_frame(player)
    if current_frame:
        screen.blit(current_frame, (player.position.x, player.position.y))
    current_frame = animation_system.get_current_frame(dash_effect_entity)
    if current_frame:
        screen.blit(current_frame, (dash_effect_entity.position.x, dash_effect_entity.position.y))
    
    if game_state == GameState.PLAYING:
        for entity in entities:
            entity.draw(screen, Vector2(0,0))
        draw_player_health(player)
        # 绘制调试用的攻击框
        if player.state in [AnimationState.ATTACK, AnimationState.ATTACK_UP, AnimationState.ATTACK_DOWN]:
            player_attack = player.get_attack_hitbox()
            if player_attack:
                pygame.draw.rect(screen, (255, 255, 0), player_attack, 2)
    
    pygame.display.flip()
    sys.exit()