import pygame
import sys
import os
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.animation_system import AnimationSystem, VFXManager
from interfaces import Entity, EntityType, Vector2, GameState
from config.animation_data import PLAYER_ANIMATIONS, EFFECT_ANIMATIONS, BOSS_ANIMATIONS
from configs import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_GROUND_Y
from systems.combat import CombatSystem
from systems.physics import PhysicsSystem
from gameplay.player import Player, Effect
from gameplay.boss import Boss

class Button:
    """一个简单的UI按钮类"""
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 50)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# 设置窗口标题
pygame.display.set_caption("Hollow Knight Clone")
game_state = GameState.START_SCREEN

# --- UI 元素 ---
font_large = pygame.font.Font(None, 120)
start_button = Button(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2, 300, 80, "Start Game", (100, 100, 100), (255, 255, 255))
restart_button = Button(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2, 300, 80, "Restart", (100, 100, 100), (255, 255, 255))
quit_button = Button(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 + 100, 300, 80, "Quit", (100, 100, 100), (255, 255, 255))

# --- 系统初始化 ---
animation_system = AnimationSystem()
physics_system = PhysicsSystem(screen.get_rect())
vfx_manager = VFXManager(animation_system)
combat_system = CombatSystem(physics_system, vfx_manager)

# 使用新的加载方法，为不同实体的动画添加前缀
animation_system.load_entity_animations("player", PLAYER_ANIMATIONS)
animation_system.load_entity_animations("effect", EFFECT_ANIMATIONS)
animation_system.load_entity_animations("boss", BOSS_ANIMATIONS)

# --- 实体变量 ---
player: Optional[Player] = None
boss: Optional[Boss] = None
entities: list = []

def reset_game():
    """重置游戏状态，重新初始化所有实体。"""
    global player, boss, entities
    
    physics_system.entities.clear()

    player = Player(pos=Vector2(200, PLAYER_GROUND_Y), size=(50, 80))
    boss = Boss(pos=Vector2(800, 585), size=(100, 150))
    entities = [player, boss]

    for entity in entities:
        physics_system.add_entity(entity)

def draw_player_health(player_instance: Player):
        """待封装：绘制玩家的血量。"""
        if not player_instance: return
        health_icon_radius = 15
        padding = 10
        start_x = 30
        start_y = 30
        for i in range(player_instance.max_health):
            x = start_x + i * (2 * health_icon_radius + padding)
            pygame.draw.circle(screen, (50, 50, 50), (x, start_y), health_icon_radius, 2)
            if i < player_instance.health:
                pygame.draw.circle(screen, (255, 255, 255), (x, start_y), health_icon_radius)

# --- 主循环 ---
while running:
    dt = clock.tick(FPS) / 1000.0
    
    # --- 事件处理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == GameState.START_SCREEN:
                if start_button.is_clicked(event.pos):
                    reset_game()
                    game_state = GameState.PLAYING
            elif game_state in [GameState.GAME_OVER, GameState.VICTORY]:
                if restart_button.is_clicked(event.pos):
                    reset_game()
                    game_state = GameState.PLAYING
                if quit_button.is_clicked(event.pos):
                    running = False

    # --- 逻辑更新 ---
    if game_state == GameState.PLAYING and player and boss:
        keys = pygame.key.get_pressed()
        player.update(keys, animation_system)
        boss.update(player.position)
        physics_system.update()
        combat_system.update(player, [boss])
        
        animation_system.play_animation("player", player, player.state)
        animation_system.play_animation("boss", boss, boss.state)

        # 更新动画系统并生成特效
        effects_to_spawn = animation_system.update(dt)
        for effect_data in effects_to_spawn:
            vfx_manager.create_effect(
                pos=effect_data["pos"], 
                animation_name=effect_data["name"],
                facing_right=effect_data["facing_right"]
            )
        
        vfx_manager.update(dt)

        if player.health <= 0:
            game_state = GameState.GAME_OVER
            if boss.health <= 0:
                game_state = GameState.VICTORY

    # --- 绘制 ---
    screen.fill((0, 0, 0))
    
    if game_state == GameState.PLAYING:
        if player and boss: # 确保实体已创建才能绘制
            # 玩家绘制
            current_frame = animation_system.get_current_frame(player)
            if current_frame:
                frame_rect = current_frame.get_rect()
                frame_rect.midbottom = (int(player.position.x), int(player.position.y))
                screen.blit(current_frame, frame_rect.topleft)
            
            # Boss绘制
            boss_current_frame = animation_system.get_current_frame(boss)
            if boss_current_frame:
                boss_frame_rect = boss_current_frame.get_rect()
                boss_frame_rect.midbottom = (int(boss.position.x), int(boss.position.y))
                screen.blit(boss_current_frame, boss_frame_rect.topleft)

            draw_player_health(player)
            
            # 绘制特效
            vfx_manager.draw(screen)

            # # --- 调试代码：绘制判定框 ---
            # # 绘制玩家的hitbox (蓝色)
            # pygame.draw.rect(screen, (0, 0, 255), player.hitbox, 2)

            # # 绘制特效的攻击hitbox (红色)
            # for effect in vfx_manager.effects:
            #     attack_box = effect.get_attack_hitbox()
            #     if attack_box:
            #         pygame.draw.rect(screen, (255, 0, 0), attack_box, 2)
            # # --- 调试代码结束 ---

            # if "attack" in player.state:
            #     player_attack = player.get_attack_hitbox()
            #     if player_attack:
            #         pygame.draw.rect(screen, (255, 255, 0), player_attack, 2)

    elif game_state == GameState.START_SCREEN:
        title_text = font_large.render("Hollow Knight", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
        screen.blit(title_text, title_rect)
        start_button.draw(screen)

    elif game_state == GameState.GAME_OVER:
        game_over_text = font_large.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
        screen.blit(game_over_text, text_rect)
        restart_button.draw(screen)
        quit_button.draw(screen)

    elif game_state == GameState.VICTORY:
        victory_text = font_large.render("You Win!", True, (255, 215, 0))
        text_rect = victory_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
        screen.blit(victory_text, text_rect)
        restart_button.draw(screen)
        quit_button.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()