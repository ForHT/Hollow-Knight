import pygame
import sys
from enum import Enum, auto

from configs import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_GROUND_Y
from interfaces import Vector2, AnimationState
from gameplay.player import Player
from gameplay.boss import Boss
from systems.physics import PhysicsSystem
from systems.combat import CombatSystem

class GameState(Enum):
    START_SCREEN = auto()
    PLAYING = auto()
    VICTORY = auto()
    GAME_OVER = auto()

class Button:
    def __init__(self, text, rect, color=(200, 200, 200), hover_color=(255, 255, 255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 50)

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            return True
        return False

class GameTest:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hollow Knight Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState.START_SCREEN

        self.font = pygame.font.Font(None, 74)
        self.title_font = pygame.font.Font(None, 100)

        self.start_button = Button("Start Game", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 80))
        self.restart_button = Button("Restart", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 80))
        self.exit_button = Button("Exit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 80))

        self.physics_system = PhysicsSystem(self.screen.get_rect())
        self.combat_system = CombatSystem(self.physics_system)
        
        # 通过调用reset来初始化实体
        self.player: Player
        self.boss: Boss
        self.entities: list
        self.reset_game()

    def reset_game(self):
        """将游戏重置到初始状态。"""
        self.physics_system.entities.clear()
        
        self.player = Player(pos=Vector2(200, PLAYER_GROUND_Y), size=(50, 80))
        self.boss = Boss(pos=Vector2(800, 585), size=(100, 150))
        
        self.entities = [self.player, self.boss]
        for entity in self.entities:
            self.physics_system.add_entity(entity)
        
        self.game_state = GameState.PLAYING

    def draw_player_health(self):
        """在屏幕左上角绘制玩家的血量。"""
        health_icon_radius = 15
        padding = 10
        start_x = 30
        start_y = 30
        for i in range(self.player.max_health):
            x = start_x + i * (2 * health_icon_radius + padding)
            # 先绘制空的血槽
            pygame.draw.circle(self.screen, (50, 50, 50), (x, start_y), health_icon_radius, 2)
            if i < self.player.health:
                # 如果有血量则填充
                pygame.draw.circle(self.screen, (255, 255, 255), (x, start_y), health_icon_radius)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.game_state == GameState.START_SCREEN:
                    if self.start_button.handle_event(event):
                        self.reset_game()
                elif self.game_state in [GameState.GAME_OVER, GameState.VICTORY]:
                    if self.restart_button.handle_event(event):
                        self.reset_game()
                    if self.exit_button.handle_event(event):
                        self.running = False

            # --- Updates based on state ---
            if self.game_state == GameState.PLAYING:
                keys = pygame.key.get_pressed()
                self.player.update(keys)
                self.boss.update(self.player.position)
                self.physics_system.update()
                self.combat_system.update(self.player, [self.boss])

                if self.player.health <= 0:
                    self.game_state = GameState.GAME_OVER
                elif self.boss.health <= 0:
                    self.game_state = GameState.VICTORY
            
            # --- Drawing ---
            self.screen.fill((10, 20, 30))

            if self.game_state == GameState.START_SCREEN:
                title_text = self.title_font.render("Hollow Knight Clone", True, (255, 255, 255))
                self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
                self.start_button.check_hover(mouse_pos)
                self.start_button.draw(self.screen)
            
            elif self.game_state == GameState.PLAYING:
                for entity in self.entities:
                    entity.draw(self.screen, Vector2(0,0))
                self.draw_player_health()
                # 绘制调试用的攻击框
                if self.player.state in [AnimationState.ATTACK, AnimationState.ATTACK_UP, AnimationState.ATTACK_DOWN]:
                    player_attack = self.player.get_attack_hitbox()
                    if player_attack:
                        pygame.draw.rect(self.screen, (255, 255, 0), player_attack, 2)

            elif self.game_state == GameState.GAME_OVER:
                text = self.font.render("YOU DIED", True, (255, 255, 255))
                self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4))
                self.restart_button.check_hover(mouse_pos)
                self.restart_button.draw(self.screen)
                self.exit_button.check_hover(mouse_pos)
                self.exit_button.draw(self.screen)

            elif self.game_state == GameState.VICTORY:
                text = self.font.render("VICTORY ACHIEVED", True, (255, 255, 0))
                self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4))
                self.restart_button.check_hover(mouse_pos)
                self.restart_button.draw(self.screen)
                self.exit_button.check_hover(mouse_pos)
                self.exit_button.draw(self.screen)
            
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    test_game = GameTest()
    test_game.run() 