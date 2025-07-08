import os
import pygame
from typing import Dict, Optional

class ResourceManager:
    def __init__(self):
        """��ʼ����Դ������"""
        self.sprite_sheets = {}  # �洢�����
        self.sounds = {}        # �洢��Ч

    def load_sprite_sheet(self, name: str, path: str) -> pygame.Surface:
        """���ؾ����"""
        image = pygame.image.load(path)
        self.sprite_sheets[name] = image
        return image

    def get_sprite_sheet(self, name: str) -> Optional[pygame.Surface]:
        """��ȡ�Ѽ��صľ����"""
        return self.sprite_sheets.get(name)

    def load_sound(self, path: str) -> pygame.mixer.Sound:
        """������Ч"""
        sound = pygame.mixer.Sound(path)
        self.sounds[path] = sound
        return sound 