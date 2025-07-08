"""
��Ϸ��������
����Э������ϵͳ������
"""
import pygame
from typing import Dict, Optional
from game.interfaces import (
    ISceneManager, 
    IResourceManager, 
    EventManager,
    IPhysicsSystem,
    IAnimationSystem,
    ICombatSystem,
    IInputHandler,
    IUIManager
)

class GameEngine:
    def __init__(self):
        """��ʼ����Ϸ����"""
        pygame.init()
        self.running = False
        self.screen: Optional[pygame.Surface] = None
        self.clock = pygame.time.Clock()
        # ϵͳ������
        self.scene_manager: Optional[ISceneManager] = None
        self.resource_manager: Optional[IResourceManager] = None
        self.physics_system: Optional[IPhysicsSystem] = None
        self.animation_system: Optional[IAnimationSystem] = None
        self.combat_system: Optional[ICombatSystem] = None
        self.input_handler: Optional[IInputHandler] = None
        self.ui_manager: Optional[IUIManager] = None
        
    def init(self, screen_width: int = 1440, screen_height: int = 900) -> None:
        """��ʼ����Ϸ���ں�ϵͳ"""
        # ��ʼ����ʾ
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Hollow Knight Clone")
        
        # TODO: ��ʼ������ϵͳ
        # self.scene_manager = SceneManager()
        # self.resource_manager = ResourceManager()
        # self.physics_system = PhysicsSystem()
        # self.animation_system = AnimationSystem()
        # self.combat_system = CombatSystem()
        # self.input_handler = InputHandler()
        # self.ui_manager = UIManager()
        
    def run(self) -> None:
        """������Ϸ��ѭ��"""
        if not self.screen:
            raise RuntimeError("Game engine not initialized. Call init() first.")
            
        self.running = True
        screen = self.screen  # ���ͼ��������Ϊ�������һ����pygame.Surface
        
        while self.running:
            # �����¼�
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    
                # UI�¼�����
                if self.ui_manager:
                    if self.ui_manager.handle_input(event):
                        continue  # UI�����˴��¼�
            
            # ���봦��
            if self.input_handler:
                self.input_handler.handle_input(events)
            
            # ������Ϸ״̬
            dt = self.clock.tick(60) / 1000.0  # ת��Ϊ��
            
            # ��˳����¸���ϵͳ
            if self.physics_system:
                self.physics_system.update(dt)
            if self.animation_system:
                self.animation_system.update(dt)
            if self.combat_system:
                self.combat_system.check_hits()
            if self.scene_manager:
                self.scene_manager.update(dt)
            if self.ui_manager:
                self.ui_manager.update({})  # TODO: ����ʵ�ʵ���Ϸ״̬
            
            # ��Ⱦ
            screen.fill((0, 0, 0))  # �����Ļ
            
            # ��˳����Ⱦ������
            if self.scene_manager:
                self.scene_manager.draw(screen)
            if self.ui_manager:
                self.ui_manager.draw(screen)
                
            pygame.display.flip()
            
    def quit(self) -> None:
        """�˳���Ϸ"""
        self.running = False
        pygame.quit() 