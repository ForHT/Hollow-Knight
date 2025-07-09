import pygame
import sys

# Adjust the path to import from your project structure
# This assumes your root 'Hollow-Knight' folder is in the Python path
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_GROUND_Y
from interfaces import Vector2
from gameplay.player import Player
from gameplay.boss import Boss
from systems.physics import PhysicsSystem
from systems.combat import CombatSystem

class GameTest:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Physics & Combat Test")
        self.clock = pygame.time.Clock()
        self.running = True

        # Instantiate systems
        self.physics_system = PhysicsSystem(self.screen.get_rect())
        self.combat_system = CombatSystem(self.physics_system)

        # Create entities
        self.player = Player(pos=Vector2(200, PLAYER_GROUND_Y), size=(50, 80))
        self.boss = Boss(pos=Vector2(800, 585), size=(100, 150))
        
        self.entities = [self.player, self.boss]
        for entity in self.entities:
            self.physics_system.add_entity(entity)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # --- Input ---
            keys = pygame.key.get_pressed()

            # --- Update ---
            self.player.update(dt, keys)
            self.boss.update(dt, self.player.position)
            self.physics_system.update(dt)
            self.combat_system.update(self.player, [self.boss]) # Pass boss as a list

            # --- Draw ---
            self.screen.fill((10, 20, 30)) # Dark blue background

            for entity in self.entities:
                entity.draw(self.screen, Vector2(0,0)) # No camera for this test
            
            # Draw debug info
            player_attack = self.player.get_attack_hitbox()
            if player_attack:
                pygame.draw.rect(self.screen, (255, 255, 0), player_attack, 2)
            
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    test_game = GameTest()
    test_game.run()