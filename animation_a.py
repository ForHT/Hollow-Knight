# animation_a.py
import pygame

class AnimationA:
    def __init__(self):
        self.maxwidth = 0.0
        self.maxheight = 0.0
        self.frame_list = []
        self.frame_num = 0
        self.TwiceCD = 0
        self.CD = 0
        self.dmove = []
        self.frameinterval = []
        self.tmp_interval = []

    def load_animation_a(self, path_format, frame_number, start_index=0):
        self.dmove = [[0.0, 0.0] for _ in range(frame_number)]
        self.tmp_interval = [0] * frame_number
        self.frameinterval = [0] * frame_number
        self.frame_num = frame_number
        
        self.frame_list = []
        for i in range(start_index, start_index + self.frame_num):
            path_file = path_format.replace('\\', '/') % i
            try:
                frame = pygame.image.load(path_file).convert_alpha()
                if frame.get_width() > self.maxwidth:
                    self.maxwidth = frame.get_width()
                if frame.get_height() > self.maxheight:
                    self.maxheight = frame.get_height()
                self.frame_list.append(frame)
            # *** 关键修正：同时捕获 FileNotFoundError 和 pygame.error ***
            except (pygame.error, FileNotFoundError) as e:
                print(f"WARNING: Could not load image '{path_file}'. Using a placeholder. Error: {e}")
                placeholder = pygame.Surface((50, 50), pygame.SRCALPHA)
                placeholder.fill((255, 0, 255, 128)) # 半透明粉色方块
                self.frame_list.append(placeholder)