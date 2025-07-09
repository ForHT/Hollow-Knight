PLAYER_ANIMATIONS = {
    "idle": {
        "frames": 9,
        "frame_time": 0.1,
        "loop": True
    },
    "walk": {
        "frames": 8,
        "frame_time": 0.1,
        "loop": True
    },
    "jump_start": {
        "frames": 4,  # ����ʵ��֡������
        "frame_time": 0.08,
        "loop": False,
        "next_state": "jump_loop"  # �����һ��״̬
    },
    "jump_loop": {
        "frames": 3,  # ����ʵ��֡������
        "frame_time": 0.1,
        "loop": True,
        "interrupt_states": ["jump_land"]  # ���Ա��жϵ�״̬
    },
    "jump_land": {
        "frames": 3,  # ����ʵ��֡������
        "frame_time": 0.08,
        "loop": False,
        "next_state": "idle"  # ��غ�ص�idle״̬
    },
    "attack": {
        "frames": 4,  # ����ʵ��֡������
        "frame_time": 0.08,
        "loop": False,
        "next_state": "idle"  # ���������ص�idle
    },
    "attack_up": {
        "frames": 4,  # ����ʵ��֡������
        "frame_time": 0.08,
        "loop": False,
        "next_state": "idle"
    },
    "attack_down": {
        "frames": 4,  # ����ʵ��֡������
        "frame_time": 0.08,
        "loop": False,
        "next_state": "idle"
    },
    "dash": {
        "frames": 5,  # ����Dash�ļ����е�ͼƬ����
        "frame_time": 0.06,  # ��̶����Կ�
        "loop": False,
        "next_state": "idle"
    },
   
}
EFFECT_ANIMATIONS = {
    "dash_effect": {
        "frames": 5,  # ����ʵ��ͼƬ��������
        "frame_time": 0.05,
        "loop": False
    }
}

# �����������ʵ��Ķ�������
ENEMY_ANIMATIONS = {
    "idle": {
        "frames": 4,
        "frame_time": 0.2,
        "loop": True
    },
    # ... �������˶���
}

# ����״̬��������״̬֮��ĺϷ�ת��
PLAYER_STATE_MACHINE = {
    "idle": ["walk", "jump_start", "attack", "attack_up", "attack_down", "dash"],  # ��������ת�������ж���
    "walk": ["idle", "jump_start", "attack", "attack_up", "attack_down", "dash"],  # ���߿���ת�������ж���
    "jump_start": ["jump_loop"],  # ��Ծ��ʼ��Ȼת��ѭ��
    "jump_loop": ["jump_land", "attack", "attack_up", "attack_down"],   # ���п��Թ���
    "jump_land": ["idle"],        # ��غ�ص�����
    "attack": ["idle", "walk"],   # �����������Իص�idle��walk
    "attack_up": ["idle", "walk"],
    "attack_down": ["idle", "walk"],
    "dash": ["idle", "attack", "attack_up", "attack_down"]  # ��̿���ֱ�ӽӹ���
}

# ��Դ·������
ANIMATION_PATHS = {
    "player": {
        "idle": "assets/sprites/player/idle/{frame}.PNG",
        "walk": "assets/sprites/player/walk/{frame}.PNG",
        "jump_start": "assets/sprites/player/jump/start/{frame}.PNG",
        "jump_loop": "assets/sprites/player/jump/loop/{frame}.PNG",
        "jump_land": "assets/sprites/player/jump/land/{frame}.PNG",
        "attack": "assets/sprites/player/attack/normal/{frame}.PNG",
        "attack_up": "assets/sprites/player/attack/up/{frame}.PNG",
        "attack_down": "assets/sprites/player/attack/down/{frame}.PNG",
        "dash": "assets/sprites/player/dash/{frame}.PNG",
        "dash_effect": "assets/sprites/player/dasheffect/{frame}.png"
    },
    "enemy": "assets/sprites/enemy/{state}/{frame}.PNG",
    "effects":{
    "dash_effect": "assets/sprites/player/dasheffect/{frame}.png"
    }
}