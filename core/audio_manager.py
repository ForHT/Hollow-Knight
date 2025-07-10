import pygame
from typing import Dict

class AudioManager:
    """一个全面的音频管理器，负责加载和播放音效与音乐。"""
    def __init__(self):
        # 初始化pygame的音频混合器
        pygame.mixer.init()
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_path: Dict[str, str] = {}
        
    def load_sounds(self):
        """加载所有在C++代码中定义的音效。"""
        # 玩家音效
        self.sounds["attack1"] = pygame.mixer.Sound("resource/music/Player/sword_1.wav")
        self.sounds["attack2"] = pygame.mixer.Sound("resource/music/Player/sword_2.wav")
        self.sounds["attack_up"] = pygame.mixer.Sound("resource/music/Player/sword_up.wav")
        self.sounds["attack_hit"] = pygame.mixer.Sound("resource/music/Player/sword_hit.wav")
        self.sounds["player_damage"] = pygame.mixer.Sound("resource/music/Player/player_damage.wav")

        # Boss 音效
        self.sounds["boss_open"] = pygame.mixer.Sound("resource/music/Boss/open.mp3")
        self.sounds["boss_hurt"] = pygame.mixer.Sound("resource/music/Boss/hea.mp3")
        # Boss的随机语音
        self.sounds["boss_haha"] = pygame.mixer.Sound("resource/music/Boss/haha.mp3")
        self.sounds["boss_henhen"] = pygame.mixer.Sound("resource/music/Boss/henhen.mp3")
        self.sounds["boss_aidito"] = pygame.mixer.Sound("resource/music/Boss/aidito.mp3")
        self.sounds["boss_ha"] = pygame.mixer.Sound("resource/music/Boss/ha.mp3")
        self.sounds["boss_gadama"] = pygame.mixer.Sound("resource/music/Boss/gadama.mp3")
        self.sounds["boss_heigali"] = pygame.mixer.Sound("resource/music/Boss/heigali.mp3")
        self.sounds["boss_higali"] = pygame.mixer.Sound("resource/music/Boss/higali.mp3")
        self.sounds["boss_xiao"] = pygame.mixer.Sound("resource/music/Boss/xiao.mp3")
        # 将随机语音放入一个列表中，方便随机抽取
        self.boss_random_vocals = [
            "boss_haha", "boss_henhen", "boss_aidito", "boss_ha",
            "boss_gadama", "boss_heigali", "boss_higali", "boss_xiao"
        ]

        # UI 音效
        self.sounds["ui_confirm"] = pygame.mixer.Sound("resource/UI/Confirm.mp3")
        
        # 存储背景音乐路径，但不立即加载
        self.music_path["title"] = "resource/UI/Title.mp3"
        self.music_path["battle"] = "resource/music/Hornet.mp3"

        print("All sounds and music paths loaded.")

    def play_sound(self, name: str):
        """播放一个已加载的音效。"""
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"Warning: Sound '{name}' not found.")

    def play_boss_random_vocal(self):
        """随机播放一句Boss的语音。"""
        import random
        sound_name = random.choice(self.boss_random_vocals)
        self.play_sound(sound_name)

    def play_music(self, name: str, loops: int = -1):
        """
        播放背景音乐。
        :param name: 音乐名称 (例如 "title", "battle")
        :param loops: 循环次数, -1表示无限循环
        """
        if name in self.music_path:
            pygame.mixer.music.load(self.music_path[name])
            pygame.mixer.music.play(loops)
        else:
            print(f"Warning: Music '{name}' not found.")

    def stop_music(self):
        """停止当前播放的背景音乐。"""
        pygame.mixer.music.stop() 