# animation.py
import pygame
from animation_a import AnimationA
from animation_name import AnimationName
from point import Point
from vector2 import Vector2

class Animation(AnimationA):
    def __init__(self):
        super().__init__()
        self.animationname = AnimationName.NU
        self.point = Point()
        self.current_frameidx = 0
        self.canloop = False
        self.loop_index = 0
        self.relative = []
        self.Effects = []
        self.Erelative = []
        self.HitEffects = []
        self.HitErelative = []
        self.PlayHitAnimation = False
        self.StartFrame = 0
        self.HitStartFrame = 0
        self.EndFrame = 0
        self.HitEndFrame = 0

    def load_animation(self, path, frame_num, name, start_index=0):
        self.load_animation_a(path, frame_num, start_index)
        self.animationname = name
        self.relative = [Vector2(0, 0) for _ in range(frame_num)]

    def load_effect(self, path, start, end, num, name_indices=None):
        self.Effects = []
        self.Erelative = [Vector2() for _ in range(num)]
        indices_to_load = name_indices if name_indices is not None else range(num)

        for i in indices_to_load:
            path_file = path.replace('\\', '/') % i
            try:
                img = pygame.image.load(path_file).convert_alpha()
                self.Effects.append(img)
            # *** 关键修正：同时捕获 FileNotFoundError 和 pygame.error ***
            except (pygame.error, FileNotFoundError) as e:
                print(f"WARNING: Could not load effect '{path_file}'. Using a placeholder. Error: {e}")
                placeholder = pygame.Surface((50, 50), pygame.SRCALPHA)
                placeholder.fill((255, 0, 255, 128))
                self.Effects.append(placeholder)

        while len(self.Effects) < num: self.Effects.append(pygame.Surface((1,1), pygame.SRCALPHA))
        self.StartFrame = start
        self.EndFrame = end

    def load_hit_effect(self, path, start, end, num, name_indices=None):
        self.HitEffects = []
        self.HitErelative = [Vector2() for _ in range(num)]
        indices_to_load = name_indices if name_indices is not None else range(num)
        for i in indices_to_load:
            path_file = path.replace('\\', '/') % i
            try:
                img = pygame.image.load(path_file).convert_alpha()
                self.HitEffects.append(img)
            # *** 关键修正：同时捕获 FileNotFoundError 和 pygame.error ***
            except (pygame.error, FileNotFoundError) as e:
                print(f"WARNING: Could not load hit effect '{path_file}'. Using a placeholder. Error: {e}")
                placeholder = pygame.Surface((50, 50), pygame.SRCALPHA)
                placeholder.fill((255, 0, 255, 128))
                self.HitEffects.append(placeholder)
        while len(self.HitEffects) < num: self.HitEffects.append(pygame.Surface((1,1), pygame.SRCALPHA))
        self.HitStartFrame = start
        self.HitEndFrame = end

    def copy(self):
        new_anim = Animation()
        for key, value in self.__dict__.items():
            if isinstance(value, list): setattr(new_anim, key, value[:])
            else: setattr(new_anim, key, value)
        new_anim.tmp_interval = self.tmp_interval[:]
        return new_anim