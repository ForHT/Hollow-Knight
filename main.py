import pygame
import math
from enum import Enum
import sys

# ==============================================================================
# 0. Pygame 初始化和全局常量
# ==============================================================================
pygame.init()
pygame.mixer.init()

# 屏幕尺寸
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("自制版空洞骑士 - Python 复刻")
clock = pygame.time.Clock()

# 颜色
BLACK = (0, 0, 0)

# ==============================================================================
# 1. 基础数据结构翻译 (Point.h, Vector2.h, AnimationName.h)
# ==============================================================================

class Point:
    """严格翻译 C++ Point 类"""
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Vector2:
    """严格翻译 C++ Vector2 类"""
    def __init__(self, vx=0.0, vy=0.0):
        self.vx = float(vx)
        self.vy = float(vy)

class AnimationName(Enum):
    """严格翻译 C++ AnimationName 枚举"""
    NU = 0
    PLAYER_IDLE0 = 1
    PLAYER_WALKL0 = 2
    PLAYER_WALKR0 = 3
    PLAYER_DASH0 = 4
    PLAYER_JUMPSTART0 = 5
    PLAYER_ATTACK0 = 6
    PLAYER_UPATTACK0 = 7
    PLAYER_JUMPLOOP0 = 8
    PLAYER_ATTACKTWICE0 = 9
    PLAYER_DOUBLEJUMP0 = 10
    PLAYER_DOWNATTACK0 = 11
    PLAYER_DAMAGE0 = 12
    PLAYER_ATTACKHIT0 = 13
    PLAYER_DEATH0 = 14
    B_IDLEL0 = 15
    B_IDLER0 = 16
    B_JUMPDASH0 = 17
    B_WALK0 = 18
    B_THROWSIDE0 = 19
    B_JUMP0 = 20
    B_DASH0 = 21
    B_LAND0 = 22
    B_JUMPFINAL0 = 23
    BLOOD0 = 24
    BLOOD_DAMAGE0 = 25
    ARROR0 = 26

# ==============================================================================
# 2. 动画类翻译 (AnimationA.h/cpp, Animation.h/cpp)
# ==============================================================================

class AnimationA:
    """严格翻译 C++ AnimationA 基类"""
    def __init__(self):
        self.maxwidth = 0.0
        self.maxheight = 0.0
        self.frame_list = []
        self.frame_num = 0
        self.CD = 0
        self.dmove = []
        self.frameinterval = []
        self.tmp_interval = []

    def LoadAnimationA(self, path_format, frame_number):
        # C++中使用TCHAR和_stprintf_s，Python中用f-string和路径格式化
        # C++使用'\'作为路径分隔符，Python为了跨平台使用'/'
        path_format = path_format.replace('\\', '/')

        self.frame_num = frame_number
        self.dmove = [[0.0, 0.0] for _ in range(frame_number)]
        self.frameinterval = [0] * frame_number
        self.tmp_interval = [0] * frame_number
        self.frame_list = []

        for i in range(self.frame_num):
            try:
                # 模拟_stprintf_s(path_file, path, i)
                full_path = path_format % i
                # Pygame 的 load 支持透明 PNG，这比 EasyX 强大
                frame = pygame.image.load(full_path).convert_alpha()
                if frame.get_width() > self.maxwidth:
                    self.maxwidth = frame.get_width()
                if frame.get_height() > self.maxheight:
                    self.maxheight = frame.get_height()
                self.frame_list.append(frame)
            except pygame.error as e:
                print(f"Error loading image {full_path}: {e}")
                # 加载一张占位图以防程序崩溃
                placeholder = pygame.Surface((100, 100), pygame.SRCALPHA)
                placeholder.fill((255, 0, 255)) # 用亮紫色表示缺失
                self.frame_list.append(placeholder)

class Animation(AnimationA):
    """严格翻译 C++ Animation 派生类"""
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
        self.StartFrame = 0
        self.EndFrame = 0

        self.HitEffects = []
        self.HitErelative = []
        self.PlayHitAnimation = False
        self.HitStartFrame = 0
        self.HitEndFrame = 0

    def LoadAnimation(self, path, frame_num, name):
        super().LoadAnimationA(path, frame_num)
        self.animationname = name
        self.relative = [Vector2(0, 0) for _ in range(frame_num)]

    def LoadEffect(self, path_format, start, end, num):
        self.Effects = []
        self.Erelative = [Vector2(0,0) for _ in range(num)]
        path_format = path_format.replace('\\', '/')
        for i in range(num):
            full_path = path_format % i
            try:
                img = pygame.image.load(full_path).convert_alpha()
                self.Effects.append(img)
            except pygame.error as e:
                print(f"Error loading effect image {full_path}: {e}")
                placeholder = pygame.Surface((50, 50), pygame.SRCALPHA)
                placeholder.fill((255, 0, 255))
                self.Effects.append(placeholder)
        self.StartFrame = start
        self.EndFrame = end
    
    def LoadHitEffect(self, path_format, start, end, num):
        self.HitEffects = []
        self.HitErelative = [Vector2(0,0) for _ in range(num)]
        path_format = path_format.replace('\\', '/')
        for i in range(num):
            full_path = path_format % i
            try:
                img = pygame.image.load(full_path).convert_alpha()
                self.HitEffects.append(img)
            except pygame.error as e:
                print(f"Error loading hit effect image {full_path}: {e}")
                placeholder = pygame.Surface((50, 50), pygame.SRCALPHA)
                placeholder.fill((255, 0, 255))
                self.HitEffects.append(placeholder)
        self.HitStartFrame = start
        self.HitEndFrame = end

    def copy(self):
        # C++的拷贝构造函数在Python中需要手动实现一个方法
        new_anim = Animation()
        new_anim.maxwidth = self.maxwidth
        new_anim.maxheight = self.maxheight
        new_anim.CD = self.CD
        new_anim.frame_num = self.frame_num
        new_anim.animationname = self.animationname
        new_anim.point = Point(self.point.x, self.point.y)
        new_anim.current_frameidx = self.current_frameidx
        new_anim.canloop = self.canloop
        new_anim.loop_index = self.loop_index
        # 深拷贝列表内容
        new_anim.dmove = [list(row) for row in self.dmove]
        new_anim.frameinterval = list(self.frameinterval)
        new_anim.tmp_interval = list(self.tmp_interval)
        new_anim.relative = [Vector2(v.vx, v.vy) for v in self.relative]
        # 图像和特效是共享的，只拷贝引用
        new_anim.frame_list = self.frame_list 
        new_anim.Effects = self.Effects
        new_anim.Erelative = [Vector2(v.vx, v.vy) for v in self.Erelative]
        new_anim.StartFrame = self.StartFrame
        new_anim.EndFrame = self.EndFrame
        new_anim.HitEffects = self.HitEffects
        new_anim.HitErelative = [Vector2(v.vx, v.vy) for v in self.HitErelative]
        new_anim.HitStartFrame = self.HitStartFrame
        new_anim.HitEndFrame = self.HitEndFrame
        return new_anim

# ==============================================================================
# 3. 角色类翻译 (Actor.h/cpp)
# ==============================================================================

class Actor:
    """严格翻译 C++ Actor 类"""
    def __init__(self, nx=0.0, ny=0.0):
        self.gravity = 2.5
        self.acceleration = 0.0
        self.speed = Vector2(0, 0)
        self.attackdir = Vector2(0, 0)
        self.position = Point(nx, ny)
        self.HP = 3
        self.CanBeHurt = True
        self.UnHurtableTime = 0 # C++里是10，但逻辑在主循环里设置
        self.Facing_Right = True # 1 for right, 0 for left

    def messagedealer(self):
        keys = pygame.key.get_pressed()
        key_w = keys[pygame.K_w]
        key_s = keys[pygame.K_s]
        key_x = keys[pygame.K_x]
        key_c = keys[pygame.K_c]
        key_z = keys[pygame.K_z]
        key_up = keys[pygame.K_UP]
        key_down = keys[pygame.K_DOWN]
        key_left = keys[pygame.K_LEFT]
        key_right = keys[pygame.K_RIGHT]

        # 1-to-1 translation of the if/else logic
        if (key_w and key_x) or (key_x and key_up):
            return 5  # 上劈
        if (key_s and key_x) or (key_x and key_down):
            return 7  # 下劈
        if key_left and key_x:
            self.Facing_Right = False
            return 2  # 平砍
        elif key_right and key_x:
            self.Facing_Right = True
            return 2  # 平砍
        if key_x:
            return 2 # 平砍
        if key_c and key_left:
            self.Facing_Right = False
            return 3 # 冲刺特判
        if key_c and key_right:
            self.Facing_Right = True
            return 3 # 冲刺特判
        if key_c:
            return 4 # 冲刺
        if (key_left and key_z and self.position.y >= 680) or \
        (key_right and key_z and self.position.y >= 680):
            return 6 # 跳跃
        if key_left:
            if key_left and key_right:
                self.speed.vx = 0
                return 0 # 静止
            self.Facing_Right = False
            self.speed.vx = -10
            return 1 # 走
        if key_right:
            if key_left and key_right:
                self.speed.vx = 0
                return 0 # 静止
            self.Facing_Right = True
            self.speed.vx = 10
            return 1 # 走
        if key_z and self.position.y >= 680:
            return 6 # 跳跃
        
        self.speed.vx = 0
        return 0 # 静止

# ==============================================================================
# 4. 全局函数和工具翻译 (main.cpp)
# ==============================================================================

def get_normal_direction(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    module = math.sqrt(dx**2 + dy**2)
    if module == 0:
        return Vector2(0, 0)
    return Vector2(dx / module, dy / module)

def get_direction(p1, p2):
    return Vector2(p2.x - p1.x, p2.y - p1.y)

def putimage_alpha(x, y, surface):
    """
    C++中的putimage_1使用了AlphaBlend，在Pygame中，
    加载带alpha通道的png并直接blit就是这个效果。
    """
    screen.blit(surface, (x, y))

def rotate_image_alpha(p_img, radian, bkcolor=BLACK):
    """
    严格翻译C++的RotateImage_Alpha函数在Python中效率极低。
    Pygame有内置的高性能旋转函数pygame.transform.rotate，其效果
    在视觉上与原函数目标一致（旋转图片并调整画布大小以容纳）。
    我们将使用Pygame的函数作为直接替代，这在功能上是等价的。
    注意：Pygame的角度是逆时针为正，单位是度。
    """
    degrees = math.degrees(radian)
    # Pygame的旋转是围绕中心点进行的，并且会自动调整图像大小
    return pygame.transform.rotate(p_img, degrees)

# ==============================================================================
# 5. 全局变量和资源加载
# ==============================================================================

# 加载单张图片
try:
    Background = pygame.image.load("img/hollow knight/background.png").convert()
    COIN = pygame.image.load("UI/coin.png").convert_alpha()
    MONEY = pygame.image.load("UI/money.png").convert_alpha()
    PLAYAGAIN = pygame.image.load("UI/playagain.png").convert_alpha()
    EMPTYBLOOD = pygame.image.load("img/hollow knight/UI/Blood/empty.png").convert_alpha()
    SOUL = pygame.image.load("img/hollow knight/UI/Blood/00.png").convert_alpha()
    OPENGROUND = pygame.image.load("UI/openground.png").convert()
    TITLE = pygame.image.load("UI/title_chinese.png").convert_alpha()
    LOGO = pygame.image.load("UI/Team Cherry Logo_large.png").convert_alpha()
    PRESS_TO_START = pygame.image.load("UI/press_to_start.png").convert_alpha()
except pygame.error as e:
    print(f"FATAL: Could not load essential UI images. Error: {e}")
    sys.exit()


# 模拟C++中的mciSendString，加载声音
try:
    MUSIC_BGM = "music/Hornet.mp3"
    MUSIC_TITLE = "UI/Title.mp3"
    SOUND_CONFIRM = pygame.mixer.Sound("UI/Confirm.mp3")
    SOUND_ATTACK1 = pygame.mixer.Sound("music/Player/sword_1.wav")
    SOUND_ATTACK2 = pygame.mixer.Sound("music/Player/sword_2.wav")
    SOUND_ATTACK_HIT = pygame.mixer.Sound("music/Player/sword_hit.wav")
    SOUND_ATTACK_UP = pygame.mixer.Sound("music/Player/sword_up.wav")
    SOUND_PLAYER_DAMAGE = pygame.mixer.Sound("music/Player/player_damage.wav")
    
    # Boss sounds
    BOSS_SOUNDS = {
        "aidito": pygame.mixer.Sound("music/Boss/aidito.mp3"),
        "dagama": pygame.mixer.Sound("music/Boss/gadama.mp3"),
        "ha": pygame.mixer.Sound("music/Boss/ha.mp3"),
        "haha": pygame.mixer.Sound("music/Boss/haha.mp3"),
        "heigali": pygame.mixer.Sound("music/Boss/heigali.mp3"),
        "henhen": pygame.mixer.Sound("music/Boss/henhen.mp3"),
        "higali": pygame.mixer.Sound("music/Boss/higali.mp3"),
        "xiao": pygame.mixer.Sound("music/Boss/xiao.mp3"),
        "open": pygame.mixer.Sound("music/Boss/open.mp3"),
        "hea": pygame.mixer.Sound("music/Boss/hea.mp3"),
    }
except pygame.error as e:
    print(f"Warning: Could not load some sound files. Error: {e}")


# 游戏角色实例
Player = Actor(200, 680)
testenemy = Actor(1000, 585)

# 动画实例
PLAYER_IDLE = [Animation(), Animation()]
PLAYER_WALK = [Animation(), Animation()]
PLAYER_DASH = [Animation(), Animation()]
PLAYER_JUMPSTART = [Animation(), Animation()]
PLAYER_ATTACK = [Animation(), Animation()]
PLAYER_UPATTACK = [Animation(), Animation()]
PLAYER_JUMPLOOP = [Animation(), Animation()]
PLAYER_ATTACKTWICE = [Animation(), Animation()]
PLAYER_DOWNATTACK = [Animation(), Animation()
]
PLAYER_DAMAGE = [Animation(), Animation()]
PLAYER_DEATH = Animation()

B_IDLE = [Animation(), Animation()]
B_JUMPDASH = [Animation(), Animation()]
B_WALK = [Animation(), Animation()]
B_JUMP = [Animation(), Animation()]
B_DASH = [Animation(), Animation()]
B_LAND = [Animation(), Animation()]
B_JUMPFINAL = [Animation(), Animation()]

BLOOD = Animation()
BLOOD_DAMAGE = Animation()
ARROR = [Animation(), Animation()]

# 当前动画状态的全局变量 (严格遵循C++的设计)
CurrentPlayerAnimation = Animation()
CurrentPlayerLoopAnimation = Animation()
CurrentEnemyAnimation = Animation()
nullanimation = Animation() # 用于重置

# --- 动画数据加载 (完整版) ---

# PLAYER_IDLE
PLAYER_IDLE[0].LoadAnimation("img/hollow knight/Idle/%d.PNG", 9, AnimationName.PLAYER_IDLE0)
PLAYER_IDLE[0].canloop = True
PLAYER_IDLE[0].loop_index = 0
PLAYER_IDLE[0].frameinterval = [4] * 9
PLAYER_IDLE[1].LoadAnimation("img/hollow knight/IdleR/%d.PNG", 9, AnimationName.PLAYER_IDLE0)
PLAYER_IDLE[1].canloop = True
PLAYER_IDLE[1].loop_index = 0
PLAYER_IDLE[1].frameinterval = [4] * 9

# PLAYER_WALK
PLAYER_WALK[0].LoadAnimation("img/hollow knight/Walk/%d.PNG", 8, AnimationName.PLAYER_WALKL0)
PLAYER_WALK[0].canloop = True
PLAYER_WALK[0].loop_index = 3
PLAYER_WALK[0].frameinterval = [2] * 8
PLAYER_WALK[1].LoadAnimation("img/hollow knight/WalkR/%d.PNG", 8, AnimationName.PLAYER_WALKR0)
PLAYER_WALK[1].canloop = True
PLAYER_WALK[1].loop_index = 3
PLAYER_WALK[1].frameinterval = [2] * 8

# PLAYER_DASH
PLAYER_DASH[0].LoadAnimation("img/hollow knight/Dash/%d.PNG", 5, AnimationName.PLAYER_DASH0)
PLAYER_DASH[0].LoadEffect("img/hollow knight/DashEffect/%d.png", 0, 4, 4)
for i in range(4):
    PLAYER_DASH[0].Effects[i] = pygame.transform.scale(PLAYER_DASH[0].Effects[i], (400, 600))
    PLAYER_DASH[0].Erelative[i] = Vector2(20 + 4 * i, -100)
PLAYER_DASH[0].frameinterval = [1, 1, 1, 3, 3]
for i in range(5): PLAYER_DASH[0].dmove[i][0] = -45
PLAYER_DASH[0].CD = 0

PLAYER_DASH[1].LoadAnimation("img/hollow knight/DashR/%d.PNG", 5, AnimationName.PLAYER_DASH0)
PLAYER_DASH[1].LoadEffect("img/hollow knight/DashEffectR/%d.png", 0, 4, 4)
for i in range(4):
    PLAYER_DASH[1].Effects[i] = pygame.transform.scale(PLAYER_DASH[1].Effects[i], (600, 800))
    PLAYER_DASH[1].Erelative[i] = Vector2(-430 + 4 * i, -100)
PLAYER_DASH[1].frameinterval = [1, 1, 1, 3, 3]
for i in range(5): PLAYER_DASH[1].dmove[i][0] = 45
PLAYER_DASH[1].CD = 0

# PLAYER_ATTACK
PLAYER_ATTACK[0].LoadAnimation("img/hollow knight/Attack/Attack/1/%d.PNG", 5, AnimationName.PLAYER_ATTACK0)
PLAYER_ATTACK[0].LoadEffect("img/hollow knight/Attack/Attack/1/0%d.png", 3, 4, 2)
PLAYER_ATTACK[0].frameinterval = [2, 1, 2, 2, 2]
PLAYER_ATTACK[0].dmove[3][0] = -2
PLAYER_ATTACK[0].Erelative[0] = Vector2(-165, 20); PLAYER_ATTACK[0].Erelative[1] = Vector2(-135, 30)
PLAYER_ATTACK[0].CD = 45
PLAYER_ATTACK[0].LoadHitEffect("img/hollow knight/AttackEffect/Attack/0%d.png", 0, 4, 5)
for i in range(5): PLAYER_ATTACK[0].HitErelative[i] = Vector2(-340, -80)

PLAYER_ATTACK[1].LoadAnimation("img/hollow knight/AttackR/Attack/1/%d.PNG", 5, AnimationName.PLAYER_ATTACK0)
PLAYER_ATTACK[1].LoadEffect("img/hollow knight/AttackR/Attack/1/0%d.png", 3, 4, 2)
PLAYER_ATTACK[1].frameinterval = [2, 1, 2, 2, 2]
PLAYER_ATTACK[1].dmove[3][0] = 2
PLAYER_ATTACK[1].Erelative[0] = Vector2(90, 20); PLAYER_ATTACK[1].Erelative[1] = Vector2(50, 25)
PLAYER_ATTACK[1].CD = 30
PLAYER_ATTACK[1].LoadHitEffect("img/hollow knight/AttackEffect/AttackR/0%d.png", 0, 4, 5)
for i in range(5): PLAYER_ATTACK[1].HitErelative[i] = Vector2(-60, -80)

# PLAYER_ATTACKTWICE
PLAYER_ATTACKTWICE[0].LoadAnimation("img/hollow knight/Attack/Attack/2/%d.png", 5, AnimationName.PLAYER_ATTACKTWICE0)
PLAYER_ATTACKTWICE[0].LoadEffect("img/hollow knight/Attack/Attack/2/0%d.png", 2, 3, 2)
PLAYER_ATTACKTWICE[0].frameinterval = [2, 1, 2, 2, 2]; PLAYER_ATTACKTWICE[0].dmove[3][0] = -2
PLAYER_ATTACKTWICE[0].Erelative[0] = Vector2(-145, 5); PLAYER_ATTACKTWICE[0].Erelative[1] = Vector2(-60, -55)
PLAYER_ATTACKTWICE[0].CD = 45
PLAYER_ATTACKTWICE[0].LoadHitEffect("img/hollow knight/AttackEffect/Attack/0%d.png", 0, 4, 5)
for i in range(5): PLAYER_ATTACKTWICE[0].HitErelative[i] = Vector2(-340, -80)

PLAYER_ATTACKTWICE[1].LoadAnimation("img/hollow knight/AttackR/Attack/2/%d.png", 5, AnimationName.PLAYER_ATTACKTWICE0)
PLAYER_ATTACKTWICE[1].LoadEffect("img/hollow knight/AttackR/Attack/2/0%d.png", 2, 3, 2)
PLAYER_ATTACKTWICE[1].frameinterval = [2, 1, 2, 2, 2]; PLAYER_ATTACKTWICE[1].dmove[3][0] = -2
PLAYER_ATTACKTWICE[1].Erelative[0] = Vector2(5, -5); PLAYER_ATTACKTWICE[1].Erelative[1] = Vector2(-60, -65)
PLAYER_ATTACKTWICE[1].CD = 45
PLAYER_ATTACKTWICE[1].LoadHitEffect("img/hollow knight/AttackEffect/AttackR/0%d.png", 0, 4, 5)
for i in range(5): PLAYER_ATTACKTWICE[1].HitErelative[i] = Vector2(-60, -80)

# PLAYER_UPATTACK
PLAYER_UPATTACK[0].LoadAnimation("img/hollow knight/Attack/AttackUp/%d.PNG", 5, AnimationName.PLAYER_UPATTACK0)
PLAYER_UPATTACK[0].LoadEffect("img/hollow knight/Attack/AttackUp/0%d.png", 2, 4, 2)
PLAYER_UPATTACK[0].frameinterval = [2] * 5; PLAYER_UPATTACK[0].CD = 20
PLAYER_UPATTACK[0].Erelative[0] = Vector2(-50, -145); PLAYER_UPATTACK[0].Erelative[1] = Vector2(10, -95)

PLAYER_UPATTACK[1].LoadAnimation("img/hollow knight/AttackR/AttackUp/%d.PNG", 5, AnimationName.PLAYER_UPATTACK0)
PLAYER_UPATTACK[1].LoadEffect("img/hollow knight/AttackR/AttackUp/0%d.png", 2, 4, 2)
PLAYER_UPATTACK[1].frameinterval = [2] * 5; PLAYER_UPATTACK[1].CD = 20
PLAYER_UPATTACK[1].Erelative[0] = Vector2(-50, -145); PLAYER_UPATTACK[1].Erelative[1] = Vector2(-110, -95)

# PLAYER_JUMPSTART
PLAYER_JUMPSTART[0].LoadAnimation("img/hollow knight/Jump/Start/%d.PNG", 9, AnimationName.PLAYER_JUMPSTART0)
PLAYER_JUMPSTART[0].frameinterval = [2] * 9; PLAYER_JUMPSTART[0].canloop = False
PLAYER_JUMPSTART[1].LoadAnimation("img/hollow knight/JumpR/Start/%d.PNG", 9, AnimationName.PLAYER_JUMPSTART0)
PLAYER_JUMPSTART[1].frameinterval = [2] * 9; PLAYER_JUMPSTART[1].canloop = False

# PLAYER_JUMPLOOP
PLAYER_JUMPLOOP[0].LoadAnimation("img/hollow knight/Jump/Loop/%d.PNG", 3, AnimationName.PLAYER_JUMPLOOP0)
PLAYER_JUMPLOOP[0].frameinterval = [2] * 3; PLAYER_JUMPLOOP[0].canloop = True; PLAYER_JUMPLOOP[0].loop_index = 0
PLAYER_JUMPLOOP[1].LoadAnimation("img/hollow knight/JumpR/Loop/%d.PNG", 3, AnimationName.PLAYER_JUMPLOOP0)
PLAYER_JUMPLOOP[1].frameinterval = [2] * 3; PLAYER_JUMPLOOP[1].canloop = True; PLAYER_JUMPLOOP[1].loop_index = 0

# PLAYER_DOWNATTACK
PLAYER_DOWNATTACK[0].LoadAnimation("img/hollow knight/Attack/AttackDown/%d.PNG", 5, AnimationName.PLAYER_DOWNATTACK0)
PLAYER_DOWNATTACK[1].LoadAnimation("img/hollow knight/AttackR/AttackDown/%d.PNG", 5, AnimationName.PLAYER_DOWNATTACK0)
PLAYER_DOWNATTACK[0].LoadEffect("img/hollow knight/Attack/AttackDown/0%d.PNG", 2, 4, 2)
PLAYER_DOWNATTACK[1].LoadEffect("img/hollow knight/AttackR/AttackDown/0%d.PNG", 2, 4, 2)
PLAYER_DOWNATTACK[0].frameinterval = [2] * 5; PLAYER_DOWNATTACK[1].frameinterval = [2] * 5
PLAYER_DOWNATTACK[0].CD = 20; PLAYER_DOWNATTACK[1].CD = 20
PLAYER_DOWNATTACK[0].Erelative[0] = Vector2(-35, 0); PLAYER_DOWNATTACK[0].Erelative[1] = Vector2(5, 0)
PLAYER_DOWNATTACK[1].Erelative[0] = Vector2(-35, 0); PLAYER_DOWNATTACK[1].Erelative[1] = Vector2(-50, 0)
PLAYER_DOWNATTACK[0].LoadHitEffect("img/hollow knight/AttackEffect/Attack/0%d.png", 0, 4, 5)
PLAYER_DOWNATTACK[1].LoadHitEffect("img/hollow knight/AttackEffect/AttackR/0%d.png", 0, 4, 5)
for i in range(5): PLAYER_DOWNATTACK[0].HitErelative[i] = Vector2(-240, 70)
for i in range(5): PLAYER_DOWNATTACK[1].HitErelative[i] = Vector2(-200, 70)

# PLAYER_DAMAGE
PLAYER_DAMAGE[0].LoadAnimation("img/hollow knight/Damage/%d.PNG", 6, AnimationName.PLAYER_DAMAGE0)
PLAYER_DAMAGE[1].LoadAnimation("img/hollow knight/DamageR/%d.PNG", 6, AnimationName.PLAYER_DAMAGE0)
PLAYER_DAMAGE[0].LoadEffect("img/hollow knight/Damage/0%d.PNG", 0, 6, 3)
PLAYER_DAMAGE[1].LoadEffect("img/hollow knight/Damage/0%d.PNG", 0, 6, 3)
for i in range(3):
    PLAYER_DAMAGE[0].Effects[i] = rotate_image_alpha(PLAYER_DAMAGE[0].Effects[i], -math.pi / 6)
    PLAYER_DAMAGE[1].Effects[i] = rotate_image_alpha(PLAYER_DAMAGE[1].Effects[i], math.pi / 6)
    PLAYER_DAMAGE[0].Erelative[i] = Vector2(-290, -150)
    PLAYER_DAMAGE[1].Erelative[i] = Vector2(-290, -150)
PLAYER_DAMAGE[0].frameinterval = [4] * 6; PLAYER_DAMAGE[1].frameinterval = [4] * 6
PLAYER_DAMAGE[0].CD = 45; PLAYER_DAMAGE[1].CD = 45

# PLAYER_DEATH
PLAYER_DEATH.LoadAnimation("img/hollow knight/Death/%d.png", 10, AnimationName.PLAYER_DEATH0)
PLAYER_DEATH.frameinterval = [int(1000/15)] * 10 # This is a guess based on sleep logic

# B_WALK
B_WALK[0].LoadAnimation("img/hollow knight/Boss/Walk/%d.png", 11, AnimationName.B_WALK0)
B_WALK[1].LoadAnimation("img/hollow knight/Boss/WalkR/%d.png", 11, AnimationName.B_WALK0)
for i in range(11): B_WALK[0].frameinterval[i] = 2; B_WALK[0].dmove[i][0] = -12
for i in range(11): B_WALK[1].frameinterval[i] = 2; B_WALK[1].dmove[i][0] = 12

# B_JUMPDASH
B_JUMPDASH[0].LoadAnimation("img/hollow knight/Boss/JumpDash/%d.png", 29, AnimationName.B_JUMPDASH0)
B_JUMPDASH[0].frameinterval = [2]*4 + [1]*9 + [3]*8 + [20] + [1]*6
B_JUMPDASH[1].LoadAnimation("img/hollow knight/Boss/JumpDashR/%d.png", 29, AnimationName.B_JUMPDASH0)
B_JUMPDASH[1].frameinterval = [2]*4 + [1]*9 + [2]*8 + [15] + [1]*6

# B_IDLE
B_IDLE[0].LoadAnimation("img/hollow knight/Boss/Idle/%d.png", 2, AnimationName.B_IDLEL0)
B_IDLE[1].LoadAnimation("img/hollow knight/Boss/IdleR/%d.png", 2, AnimationName.B_IDLER0)
B_IDLE[0].frameinterval = [4]*2; B_IDLE[1].frameinterval = [4]*2
B_IDLE[0].canloop = True; B_IDLE[1].canloop = True

# B_LAND
B_LAND[0].LoadAnimation("img/hollow knight/Boss/Land/%d.png", 6, AnimationName.B_LAND0)
B_LAND[1].LoadAnimation("img/hollow knight/Boss/LandR/%d.png", 6, AnimationName.B_LAND0)
B_LAND[0].frameinterval = [2]*6; B_LAND[1].frameinterval = [2]*6

# B_JUMP
B_JUMP[0].LoadAnimation("img/hollow knight/Boss/Jump/%d.png", 29, AnimationName.B_JUMP0)
B_JUMP[1].LoadAnimation("img/hollow knight/Boss/JumpR/%d.png", 29, AnimationName.B_JUMP0)
B_JUMP[0].frameinterval = [2]*13 + [1]*5 + [2]*11
B_JUMP[1].frameinterval = B_JUMP[0].frameinterval[:]

# B_DASH
B_DASH[0].LoadAnimation("img/hollow knight/Boss/Dash/%d.png", 12, AnimationName.B_DASH0)
B_DASH[1].LoadAnimation("img/hollow knight/Boss/DashR/%d.png", 12, AnimationName.B_DASH0)
B_DASH[0].LoadEffect("img/hollow knight/Boss/Dash/0%d.png", 9, 11, 4)
B_DASH[1].LoadEffect("img/hollow knight/Boss/DashR/0%d.png", 9, 11, 4)
B_DASH[0].Erelative[0] = Vector2(140, 90); B_DASH[0].Erelative[1] = Vector2(140, -20); B_DASH[0].Erelative[2] = Vector2(200, -20); B_DASH[0].Erelative[3] = Vector2(200, -20)
B_DASH[1].Erelative[0] = Vector2(-120, 90); B_DASH[1].Erelative[1] = Vector2(-250, -20); B_DASH[1].Erelative[2] = Vector2(-250, -20); B_DASH[1].Erelative[3] = Vector2(-250, -20)
B_DASH[0].frameinterval = [2]*11 + [20]; B_DASH[1].frameinterval = [2]*11 + [20]
B_DASH[0].dmove[11][0] = -35; B_DASH[1].dmove[11][0] = 35

# B_JUMPFINAL
B_JUMPFINAL[0].LoadAnimation("img/hollow knight/Boss/JumpFinal/%d.png", 45, AnimationName.B_JUMPFINAL0)
B_JUMPFINAL[1].LoadAnimation("img/hollow knight/Boss/JumpFinalR/%d.png", 45, AnimationName.B_JUMPFINAL0)
B_JUMPFINAL[0].LoadEffect("img/hollow knight/Boss/JumpFinal/Effects/0%d.png", 20, 38, 18)
B_JUMPFINAL[1].LoadEffect("img/hollow knight/Boss/JumpFinalR/Effects/0%d.png", 20, 38, 18)
B_JUMPFINAL[0].frameinterval = [2]*13 + [1]*5 + [2]*27; B_JUMPFINAL[1].frameinterval = B_JUMPFINAL[0].frameinterval[:]
B_JUMPFINAL[0].CD = 30; B_JUMPFINAL[1].CD = 30
for i in range(18): B_JUMPFINAL[0].Erelative[i] = Vector2(-80, -50); B_JUMPFINAL[1].Erelative[i] = Vector2(-80, -50)

# UI Animations
BLOOD.LoadAnimation("img/hollow knight/UI/Blood/%d.png", 6, AnimationName.BLOOD0)
BLOOD.frameinterval = [120, 3, 3, 3, 3, 3]
BLOOD.canloop = True; BLOOD.loop_index = 0
BLOOD_DAMAGE.LoadAnimation("img/hollow knight/UI/Blood/Damage/%d.png", 6, AnimationName.BLOOD_DAMAGE0)
BLOOD_DAMAGE.frameinterval = [15, 3, 3, 3, 3, 3]; BLOOD_DAMAGE.canloop = False
BLOOD_DAMAGE.dmove[0] = [-7, -27]; BLOOD_DAMAGE.dmove[1] = [-3, -27]; BLOOD_DAMAGE.dmove[2] = [-4, -10]
BLOOD_DAMAGE.dmove[3] = [-2, 0]; BLOOD_DAMAGE.dmove[4] = [-3, 0]

ARROR[0].LoadAnimation("UI/Arror/%d.png", 10, AnimationName.ARROR0)
ARROR[1].LoadAnimation("UI/ArrorR/%d.png", 10, AnimationName.ARROR0)
ARROR[0].frameinterval = [2] * 10; ARROR[1].frameinterval = [2] * 10

# ==============================================================================
# 6. Game Logic Functions (main.cpp)
# ==============================================================================

# IMPORTANT: The following functions modify global state variables.
# This is a direct translation of the C++ design.

def attack_judger(player, enemy):
    global CurrentPlayerAnimation, CurrentEnemyAnimation
    if enemy.UnHurtableTime == 0:
        player_anim_name = CurrentPlayerAnimation.animationname
        if CurrentEnemyAnimation.animationname == AnimationName.NU:
            return False
        
        # Simplified AABB check based on the C++ logic
        if player_anim_name in [AnimationName.PLAYER_ATTACK0, AnimationName.PLAYER_UPATTACK0, AnimationName.PLAYER_ATTACKTWICE0]:
            if not CurrentPlayerAnimation.frame_list: return False
            
            # This logic is complex and relies on effect sizes. We'll approximate with sprite sizes.
            effect_w = CurrentPlayerAnimation.Effects[0].get_width()
            effect_h = CurrentPlayerAnimation.Effects[0].get_height()
            enemy_w = CurrentEnemyAnimation.frame_list[CurrentEnemyAnimation.current_frameidx].get_width() - 50
            enemy_h = CurrentEnemyAnimation.frame_list[CurrentEnemyAnimation.current_frameidx].get_height() - 50

            # C++ code for EffectCenter has a bug in y-coord calculation
            facing_mult = 1 if player.Facing_Right else -1
            effect_center_x = player.position.x + CurrentPlayerAnimation.dmove[0][0] + facing_mult * effect_w / 2
            effect_center_y = player.position.y + CurrentPlayerAnimation.dmove[0][1] + effect_h / 2
            
            enemy_center_x = enemy.position.x + enemy_w / 2
            enemy_center_y = enemy.position.y + enemy_h / 2

            relative_vx = enemy.position.x - player.position.x
            if (facing_mult * relative_vx) >= 0:
                dx = abs(enemy_center_x - effect_center_x)
                dy = abs(enemy_center_y - effect_center_y)
                if dx < (effect_w + enemy_w) / 2 and dy < (effect_h + enemy_h) / 2:
                    print("Hit ok!")
                    return True
            return False
            
        elif player_anim_name == AnimationName.PLAYER_DOWNATTACK0:
            dy = player.position.y - enemy.position.y
            dx = player.position.x - enemy.position.x
            if 0 <= dy <= 550 and -100 <= dx <= 150:
                return True
            return False
    return False

def attacked_judger(player, enemy):
    global CurrentPlayerAnimation, CurrentPlayerLoopAnimation, CurrentEnemyAnimation
    
    player_anim = CurrentPlayerAnimation if CurrentPlayerAnimation.animationname != AnimationName.NU else CurrentPlayerLoopAnimation
    enemy_anim = CurrentEnemyAnimation

    if player_anim.animationname == AnimationName.NU or enemy_anim.animationname == AnimationName.NU:
        return False
    if not player_anim.frame_list or not enemy_anim.frame_list:
        return False

    w1 = player_anim.frame_list[player_anim.current_frameidx].get_width()
    h1 = player_anim.frame_list[player_anim.current_frameidx].get_height()
    w2 = enemy_anim.frame_list[enemy_anim.current_frameidx].get_width()
    h2 = enemy_anim.frame_list[enemy_anim.current_frameidx].get_height()

    player_center = Point(player.position.x + w1 / 2, player.position.y + h1 / 2)
    enemy_center = Point(enemy.position.x + w2 / 2, enemy.position.y + h2 / 2)
    
    dx = abs(player_center.x - enemy_center.x)
    dy = abs(player_center.y - enemy_center.y)

    # Simplified logic based on C++ code's hardcoded values
    if enemy_anim.animationname == AnimationName.B_JUMPFINAL0 and 21 <= enemy_anim.current_frameidx <= 36:
        if dx < (w1 + w2) / 2 + 100 and dy < (h1 + h2) / 2 + 110 and player.UnHurtableTime == 0:
            return True
    else:
        if dx < (w1 + w2) / 2 - 90 and dy < (h1 + h2) / 2 - 80 and player.UnHurtableTime == 0:
            return True
            
    return False

def gravity_collide(player, enemy):
    global CurrentPlayerAnimation, CurrentEnemyAnimation
    
    player.speed.vy += player.gravity
    player.position.y += player.speed.vy / 30  # Division by 30 seems to be a frame rate adjustment
    enemy.speed.vy += enemy.gravity
    enemy.position.y += enemy.speed.vy / 30

    if player.position.y > 680:
        player.speed.vy = 0
        player.position.y = 680
    if enemy.position.y > 585:
        # enemy.speed.vy = 0 # C++ code sets position but not speed, likely a bug. Adding this.
        enemy.position.y = 585

    if CurrentPlayerAnimation.animationname == AnimationName.PLAYER_DASH0:
        player.speed.vy = 0
    if CurrentPlayerAnimation.animationname == AnimationName.PLAYER_DOWNATTACK0 and player.position.y == 680:
        player.speed.vy = -30
        
    if CurrentEnemyAnimation.animationname == AnimationName.B_JUMPFINAL0 and 15 <= CurrentEnemyAnimation.current_frameidx <= 33:
        enemy.gravity = 0
        enemy.speed.vy = 0
        enemy.speed.vx = 0
    elif CurrentEnemyAnimation.animationname == AnimationName.B_JUMPFINAL0:
        enemy.gravity = 4

def drawplayer(actor, current_anim):
    global nullanimation
    if current_anim.animationname == AnimationName.NU or not current_anim.frame_list:
        return False # 动画未播放，返回False

    # Decrement timer and advance frame
    idx = current_anim.current_frameidx
    # 安全检查，防止索引越界
    if idx >= len(current_anim.tmp_interval) or idx >= len(current_anim.dmove) or idx >= len(current_anim.frame_list):
        return True # 如果索引有问题，也当作动画结束

    current_anim.tmp_interval[idx] -= 1
    
    # Apply intra-frame movement
    dx = current_anim.dmove[idx][0]
    dy = current_anim.dmove[idx][1]
    actor.position.x += dx
    actor.position.y += dy
    
    # Draw main sprite
    putimage_alpha(actor.position.x, actor.position.y, current_anim.frame_list[idx])
    
    # Draw effects
    if current_anim.Effects and idx >= current_anim.StartFrame:
        effect_idx = min(len(current_anim.Effects) - 1, idx - current_anim.StartFrame)
        if effect_idx < len(current_anim.Erelative): # 另一个安全检查
            pos = current_anim.Erelative[effect_idx]
            putimage_alpha(actor.position.x + pos.vx, actor.position.y + pos.vy, current_anim.Effects[effect_idx])

    # Draw hit effects
    if current_anim.PlayHitAnimation and current_anim.HitEffects and idx >= current_anim.HitStartFrame:
        hit_effect_idx = min(len(current_anim.HitEffects) - 1, idx - current_anim.HitStartFrame)
        if hit_effect_idx < len(current_anim.HitErelative): # 安全检查
            pos = current_anim.HitErelative[hit_effect_idx]
            putimage_alpha(actor.position.x + pos.vx, actor.position.y + pos.vy, current_anim.HitEffects[hit_effect_idx])

    if current_anim.tmp_interval[idx] <= 0:
        # Apply end-of-frame movement
        if idx < len(current_anim.relative): # 安全检查
            actor.position.x += current_anim.relative[idx].vx
            actor.position.y += current_anim.relative[idx].vy
        
        current_anim.current_frameidx += 1
        
        # Reset timers for next use IF it loops
        if current_anim.current_frameidx < current_anim.frame_num:
             # 只有在动画还没结束时，才可能需要重置计时器（虽然这个逻辑有点怪）
             # 为了安全，我们只在循环时重置
             pass
        else:
             # 重新加载计时器，以备下次使用或循环
             current_anim.tmp_interval = list(current_anim.frameinterval)

        if current_anim.current_frameidx >= current_anim.frame_num:
            if current_anim.canloop:
                current_anim.current_frameidx = current_anim.loop_index
                return False # 循环动画永不结束
            else:
                # 动画播放完毕，重置它的帧索引以备下次使用
                current_anim.current_frameidx = 0
                # 返回True，告诉主循环这个一次性动画结束了！
                return True
    
    return False # 动画还在播放，返回False

def drawUI(current_anim, x, y):
    # Similar to drawplayer, but for UI elements
    if current_anim.animationname == AnimationName.NU or not current_anim.frame_list:
        return
    
    idx = current_anim.current_frameidx
    if idx >= len(current_anim.tmp_interval): return

    current_anim.tmp_interval[idx] -= 1
    
    putimage_alpha(x + current_anim.dmove[idx][0], y + current_anim.dmove[idx][1], current_anim.frame_list[idx])
    
    if current_anim.tmp_interval[idx] <= 0:
        current_anim.current_frameidx += 1
        current_anim.tmp_interval = list(current_anim.frameinterval)
        
        if current_anim.current_frameidx >= current_anim.frame_num:
            if current_anim.canloop:
                current_anim.current_frameidx = current_anim.loop_index
            else:
                current_anim.current_frameidx = 0 # Reset for next time
    
# ==============================================================================
# 7. Main Game Loop (main.cpp)
# ==============================================================================
scenemanager = 0
running = True

while running:
    # --- SCENE 0: TITLE SCREEN ---
    if scenemanager == 0:
        pygame.mixer.music.load(MUSIC_TITLE)
        pygame.mixer.music.play(-1) # -1 for looping
        
        title_running = True
        while title_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    title_running = False
                if event.type == pygame.KEYDOWN:
                    title_running = False # Exit on any key press
            
            screen.blit(OPENGROUND, (0,0))
            putimage_alpha(720 - TITLE.get_width() / 2, 100, TITLE)
            putimage_alpha(1180, 720, LOGO)
            putimage_alpha(720 - PRESS_TO_START.get_width() / 2, 720, PRESS_TO_START)
            
            pygame.display.flip()
            clock.tick(60)

        if not running: break
            
        SOUND_CONFIRM.play()
        
        # Arrow animation
        for i in range(10):
            screen.blit(OPENGROUND, (0,0))
            putimage_alpha(720 - TITLE.get_width() / 2, 100, TITLE)
            putimage_alpha(1180, 720, LOGO)
            putimage_alpha(720 - PRESS_TO_START.get_width() / 2, 720, PRESS_TO_START)
            putimage_alpha(720 - PRESS_TO_START.get_width()/2 - ARROR[0].frame_list[0].get_width(), 705, ARROR[0].frame_list[i])
            putimage_alpha(720 + PRESS_TO_START.get_width()/2, 705, ARROR[1].frame_list[i])
            pygame.display.flip()
            pygame.time.wait(int(1000/30))

        pygame.time.wait(300)
        pygame.mixer.music.stop()
        scenemanager = 1

    # --- SCENE 1: GAMEPLAY ---
    if scenemanager == 1:
        # Reset game state
        Player.HP = 7
        testenemy.HP = 50
        Player.position = Point(200, 680)
        testenemy.position = Point(1000, 585)
        
        # Reset animations
        CurrentPlayerAnimation = nullanimation.copy()
        CurrentPlayerLoopAnimation = nullanimation.copy()
        CurrentEnemyAnimation = nullanimation.copy()
        
        # Reset CDs
        PublicCD = 20
        # ... Other CD resets would go here ...
        
        pygame.mixer.music.load(MUSIC_BGM)
        pygame.mixer.music.play(-1)
        if "open" in BOSS_SOUNDS: BOSS_SOUNDS["open"].play()
        
        game_running = True
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_running = False
            
            if Player.HP <= 0 or testenemy.HP <= 0:
                game_running = False
                continue

            # --- UPDATE LOGIC (Directly translated from C++ main loop) ---
            
            # 1. Update Timers/CDs
            if Player.UnHurtableTime > 0: Player.UnHurtableTime -= 1
            if PublicCD > 0: PublicCD -= 1
            # Python中对象是引用，所以可以直接修改CD值
            if PLAYER_DASH[0].CD > 0: PLAYER_DASH[0].CD -= 1; PLAYER_DASH[1].CD -= 1
            if PLAYER_ATTACK[0].CD > 0: PLAYER_ATTACK[0].CD -= 1; PLAYER_ATTACK[1].CD -= 1
            if PLAYER_UPATTACK[0].CD > 0: PLAYER_UPATTACK[0].CD -= 1; PLAYER_UPATTACK[1].CD -= 1
            if PLAYER_ATTACKTWICE[0].CD > 0: PLAYER_ATTACKTWICE[0].CD -= 1; PLAYER_ATTACKTWICE[1].CD -= 1
            if PLAYER_DOWNATTACK[0].CD > 0: PLAYER_DOWNATTACK[0].CD -= 1; PLAYER_DOWNATTACK[1].CD -= 1
            if PLAYER_DAMAGE[0].CD > 0: PLAYER_DAMAGE[0].CD -= 1; PLAYER_DAMAGE[1].CD -= 1
            
            # ... update enemy CDs ...

            # 2. Player Input and State Machine (修正版 - 拆分 if-elif)
            operation = Player.messagedealer()

            # # 新增调试信息：
            # if operation == 6:
            #     print(f"Jump key pressed! Player Y Speed: {Player.speed.vy}, Player Y Pos: {Player.position.y}")
            
            # 伤害状态下不接受输入
            if CurrentPlayerAnimation.animationname == AnimationName.PLAYER_DAMAGE0 and CurrentPlayerAnimation.current_frameidx <= 3:
                pass
            else:
                # C++的逻辑是多个独立的if，而不是if-elif链，这里严格复刻
                if operation == 0: # Idle
                    if CurrentPlayerLoopAnimation.animationname != AnimationName.PLAYER_IDLE0:
                        CurrentPlayerLoopAnimation = PLAYER_IDLE[Player.Facing_Right].copy()
                
                if operation == 1: # Walk
                    if CurrentPlayerLoopAnimation.animationname not in [AnimationName.PLAYER_WALKL0, AnimationName.PLAYER_WALKR0] or \
                       (CurrentPlayerLoopAnimation.animationname == AnimationName.PLAYER_WALKR0 and not Player.Facing_Right) or \
                       (CurrentPlayerLoopAnimation.animationname == AnimationName.PLAYER_WALKL0 and Player.Facing_Right):
                        CurrentPlayerLoopAnimation = PLAYER_WALK[Player.Facing_Right].copy()

                isok = CurrentPlayerAnimation.animationname not in [AnimationName.PLAYER_ATTACK0, AnimationName.PLAYER_DOWNATTACK0, AnimationName.PLAYER_DASH0, AnimationName.PLAYER_UPATTACK0, AnimationName.PLAYER_ATTACKTWICE0]
                
                if Player.speed.vy == 0 and CurrentPlayerAnimation.animationname in [AnimationName.PLAYER_ATTACK0, AnimationName.PLAYER_UPATTACK0, AnimationName.PLAYER_ATTACKTWICE0, AnimationName.PLAYER_DOWNATTACK0]:
                    Player.speed.vx = 0

                # 这是一个独立的判断，必须在跳跃判断之前
                if Player.speed.vy > 0.1 and isok: # Falling
                    CurrentPlayerLoopAnimation = PLAYER_JUMPLOOP[Player.Facing_Right].copy()

                if operation == 2: # Attack
                    if isok and PLAYER_ATTACK[0].CD <= 0:
                        CurrentPlayerAnimation = PLAYER_ATTACK[Player.Facing_Right].copy()
                        PLAYER_ATTACK[0].CD = 30
                        PLAYER_ATTACKTWICE[0].CD = 45
                    elif PLAYER_ATTACKTWICE[0].CD > 0 and PLAYER_ATTACKTWICE[0].CD <= 30:
                        CurrentPlayerAnimation = PLAYER_ATTACKTWICE[Player.Facing_Right].copy()
                        PLAYER_ATTACKTWICE[0].CD = 0

                if operation == 4 or operation == 3: # Dash
                    if PLAYER_DASH[0].CD <= 0:
                        if (Player.position.y < 680 and isok) or CurrentPlayerAnimation.animationname == AnimationName.NU:
                           CurrentPlayerAnimation = PLAYER_DASH[Player.Facing_Right].copy()
                           PLAYER_DASH[0].CD = 30
                    elif operation == 3 and CurrentPlayerAnimation.animationname != AnimationName.PLAYER_DASH0:
                        if CurrentPlayerLoopAnimation.animationname not in [AnimationName.PLAYER_WALKL0, AnimationName.PLAYER_WALKR0] or \
                           (CurrentPlayerLoopAnimation.animationname == AnimationName.PLAYER_WALKR0 and not Player.Facing_Right) or \
                           (CurrentPlayerLoopAnimation.animationname == AnimationName.PLAYER_WALKL0 and Player.Facing_Right):
                            CurrentPlayerLoopAnimation = PLAYER_WALK[Player.Facing_Right].copy()
                        Player.speed.vx = 10 * (1 if Player.Facing_Right else -1)

                if operation == 5 and PLAYER_UPATTACK[0].CD <= 0: # Up Attack
                    if (Player.position.y <= 680 and isok) or CurrentPlayerAnimation.animationname == AnimationName.NU:
                        CurrentPlayerAnimation = PLAYER_UPATTACK[Player.Facing_Right].copy()
                        PLAYER_UPATTACK[0].CD = 20

                if operation == 6: # Jump
                    if CurrentPlayerAnimation.animationname == AnimationName.NU and Player.position.y >= 680:
                        Player.speed.vy = -43
                        CurrentPlayerAnimation = PLAYER_JUMPSTART[Player.Facing_Right].copy()

                if operation == 7 and PLAYER_DOWNATTACK[0].CD <= 0: # Down Attack
                    if (Player.position.y <= 680 and isok) or CurrentPlayerAnimation.animationname == AnimationName.NU:
                        CurrentPlayerAnimation = PLAYER_DOWNATTACK[Player.Facing_Right].copy()
                        PLAYER_DOWNATTACK[0].CD = 20
                
                if CurrentPlayerAnimation.animationname == AnimationName.PLAYER_DASH0:
                    Player.speed.vx = 0

            # Stop loop animations if a one-shot animation is playing
            if CurrentPlayerAnimation.animationname != AnimationName.NU:
                CurrentPlayerLoopAnimation = nullanimation.copy()
                
            # Update player position based on speed (C++ had this in a weird spot)
            Player.position.x += Player.speed.vx
            # Player.position.y += Player.speed.vy; # This is handled by gravity_collide

            # 3. Enemy AI (完整版 - 修正)
            if PublicCD <= 0:
                # 模拟C++的while循环决策，但只尝试决策一次，防止死循环
                if CurrentEnemyAnimation.animationname in [AnimationName.NU, AnimationName.B_IDLEL0, AnimationName.B_IDLER0]:
                    import random
                    
                    # 决策逻辑开始
                    decision_made = False
                    
                    vx_dist = abs(get_direction(testenemy.position, Player.position).vx)

                    # C++代码的逻辑很乱，我们尝试严格复刻其意图
                    # 1. 尝试走路
                    if vx_dist < 150 and B_WALK[0].CD <= 0:
                        testenemy.Facing_Right = get_direction(testenemy.position, Player.position).vx < 0
                        CurrentEnemyAnimation = B_WALK[1 if testenemy.Facing_Right else 0].copy()
                        B_WALK[0].CD = 75
                        PublicCD = 30
                        decision_made = True
                    elif vx_dist > 500 and B_WALK[0].CD <= 0:
                        testenemy.Facing_Right = get_direction(testenemy.position, Player.position).vx > 0
                        CurrentEnemyAnimation = B_WALK[1 if testenemy.Facing_Right else 0].copy()
                        B_WALK[0].CD = 75
                        PublicCD = 30
                        decision_made = True

                    # 2. 如果不走路，尝试随机技能
                    if not decision_made:
                        # 循环尝试最多10次，防止死循环
                        for _ in range(10): 
                            index = random.randint(0, 3)
                            if index == 0 and B_JUMP[0].CD <= 0:
                                testenemy.gravity = 3
                                testenemy.speed.vy = -60
                                normal_shootdirection = get_normal_direction(testenemy.position, Player.position)
                                for i in range(3, 29):
                                    B_JUMP[0].dmove[i][0] = 10 * normal_shootdirection.vx
                                    B_JUMP[1].dmove[i][0] = 10 * normal_shootdirection.vx
                                testenemy.Facing_Right = get_direction(testenemy.position, Player.position).vx >= 0
                                CurrentEnemyAnimation = B_JUMP[1 if testenemy.Facing_Right else 0].copy()
                                B_JUMP[0].CD = 60
                                PublicCD = 50
                                decision_made = True
                                break # 决策完成，跳出尝试循环
                            
                            elif index == 1 and B_JUMPDASH[0].CD <= 0:
                                testenemy.gravity = 0; testenemy.speed.vy = 0
                                shootdirection = get_direction(testenemy.position, Player.position)
                                normal_shootdirection = get_normal_direction(testenemy.position, Player.position)
                                for i in range(3, 8):
                                    B_JUMPDASH[0].dmove[i][0] = 10 * normal_shootdirection.vx
                                    B_JUMPDASH[1].dmove[i][0] = 10 * normal_shootdirection.vx
                                    B_JUMPDASH[0].dmove[i][1] = -75
                                    B_JUMPDASH[1].dmove[i][1] = -75
                                B_JUMPDASH[0].dmove[22][1] = 30; B_JUMPDASH[1].dmove[22][1] = 30
                                B_JUMPDASH[0].dmove[22][0] = shootdirection.vx / 22
                                B_JUMPDASH[1].dmove[22][0] = shootdirection.vx / 22
                                testenemy.Facing_Right = get_direction(testenemy.position, Player.position).vx >= 0
                                CurrentEnemyAnimation = B_JUMPDASH[1 if testenemy.Facing_Right else 0].copy()
                                B_JUMPDASH[0].CD = 120
                                PublicCD = 50
                                decision_made = True
                                break

                            elif index == 2 and B_DASH[0].CD <= 0:
                                testenemy.Facing_Right = get_direction(testenemy.position, Player.position).vx >= 0
                                CurrentEnemyAnimation = B_DASH[1 if testenemy.Facing_Right else 0].copy()
                                B_DASH[0].CD = 50
                                PublicCD = 50
                                decision_made = True
                                break

                            elif index == 3 and B_JUMPFINAL[0].CD <= 0:
                                testenemy.gravity = 4; testenemy.speed.vy = -60
                                normal_shootdirection = get_normal_direction(testenemy.position, Player.position)
                                testenemy.Facing_Right = get_direction(testenemy.position, Player.position).vx >= 0
                                for i in range(3, 15):
                                    B_JUMPFINAL[1 if testenemy.Facing_Right else 0].dmove[i][0] = 25 * normal_shootdirection.vx
                                CurrentEnemyAnimation = B_JUMPFINAL[1 if testenemy.Facing_Right else 0].copy()
                                B_JUMPFINAL[0].CD = 240
                                PublicCD = 120
                                decision_made = True
                                break

            # 如果AI没有做出任何动作，则切换到站立
            elif CurrentEnemyAnimation.animationname == AnimationName.NU:
                facing_right = get_direction(testenemy.position, Player.position).vx >= 0
                CurrentEnemyAnimation = B_IDLE[1 if facing_right else 0].copy()

            # 4. Physics and Collisions
            gravity_collide(Player, testenemy)
            
            if attack_judger(Player, testenemy):
                testenemy.UnHurtableTime = 12
                testenemy.HP -= 1
                if CurrentPlayerAnimation.animationname in [AnimationName.PLAYER_ATTACK0, AnimationName.PLAYER_ATTACKTWICE0, AnimationName.PLAYER_DOWNATTACK0]:
                     CurrentPlayerAnimation.PlayHitAnimation = True
                SOUND_ATTACK_HIT.play()

            if attacked_judger(Player, testenemy):
                Player.UnHurtableTime = 45
                Player.HP -= 1
                Player.speed.vy = -25
                CurrentPlayerAnimation = PLAYER_DAMAGE[0 if get_direction(testenemy.position, Player.position).vx < 0 else 1].copy()
                SOUND_PLAYER_DAMAGE.play()


            # --- DRAWING ---
            screen.blit(Background, (0, 0))
            
            # Draw Enemy
            if CurrentEnemyAnimation.animationname != AnimationName.NU:
                is_enemy_anim_finished = drawplayer(testenemy, CurrentEnemyAnimation)
                if is_enemy_anim_finished:
                    CurrentEnemyAnimation = nullanimation.copy()
            
            # Draw Player
            active_player_anim = CurrentPlayerAnimation if CurrentPlayerAnimation.animationname != AnimationName.NU else CurrentPlayerLoopAnimation
            
            # 只有在有动画可画的时候才画
            if active_player_anim.animationname != AnimationName.NU:
                is_player_anim_finished = drawplayer(Player, active_player_anim)
                
                # 如果播放的是一次性动画且它结束了
                if active_player_anim is CurrentPlayerAnimation and is_player_anim_finished:
                    CurrentPlayerAnimation = nullanimation.copy()
                    CurrentPlayerAnimation.PlayHitAnimation = False # Reset hit effect flag

            # Draw UI
            putimage_alpha(210, 140, COIN)
            putimage_alpha(270, 145, MONEY)
            putimage_alpha(53, 40, SOUL)
            for i in range(7):
                putimage_alpha(200 + 65 * i, 70, EMPTYBLOOD)
            for i in range(Player.HP):
                putimage_alpha(200 + 65 * i, 70, BLOOD.frame_list[BLOOD.current_frameidx])

            drawUI(BLOOD, 0, 0) # Update blood animation timer
            if Player.UnHurtableTime > 0 or (CurrentPlayerAnimation.animationname == AnimationName.PLAYER_DAMAGE0):
                 drawUI(BLOOD_DAMAGE, 200 + 65 * Player.HP, 70)


            pygame.display.flip()
            clock.tick(45) # Original code uses a mix of 45 and 60 FPS logic. Sticking to 45.

        # After game loop ends (win/lose)
        pygame.mixer.music.stop()
        if Player.HP <= 0:
            # Player death animation
            scenemanager = 2
        elif testenemy.HP <= 0:
            # Enemy death sequence
            scenemanager = 2
            
    # --- SCENE 2: PLAY AGAIN ---
    if scenemanager == 2:
        screen.fill(BLACK)
        putimage_alpha(720 - PLAYAGAIN.get_width() / 2, 450 - PLAYAGAIN.get_height() / 2, PLAYAGAIN)
        pygame.display.flip()
        
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    menu_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click
                        mx, my = event.pos
                        # Yes button rect approx: (560, 420) to (660, 500)
                        if 560 < mx < 660 and 420 < my < 500:
                            SOUND_CONFIRM.play()
                            scenemanager = 1
                            menu_running = False
                        # No button rect approx: (780, 420) to (880, 500)
                        elif 780 < mx < 880 and 420 < my < 500:
                            scenemanager = 3 # Exit
                            menu_running = False

    # --- SCENE 3: EXIT ---
    if scenemanager == 3:
        running = False


pygame.quit()
sys.exit()