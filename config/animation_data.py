"""
这个文件包含了从C++源代码中提取的、所有动画的硬编码数据。
这是我们新的“真值来源”。
"""

# C++中的 frameinterval 单位似乎是 1/60 秒 (帧)
# 我们在Pygame中用秒，所以需要转换。1帧 = 1/60秒 ≈ 0.0167秒
FRAME_TIME = 1 / 60.0

PLAYER_ANIMATIONS = {
    "idle": {
        "left": {
            "path_template": "resource/img/hollow knight/Idle/{}.PNG",
            "frame_count": 9,
            "frame_intervals": [4, 4, 4, 4, 4, 4, 4, 4, 4],
            "displacements": [(0, 0)] * 9, # C++代码中未指定，默认为0
            "loop": True,
        },
        "right": {
            "path_template": "resource/img/hollow knight/IdleR/{}.PNG",
            "frame_count": 9,
            "frame_intervals": [4, 4, 4, 4, 4, 4, 4, 4, 4],
            "displacements": [(0, 0)] * 9,
            "loop": True,
        }
    },
    "walk": {
        "left": {
            "path_template": "resource/img/hollow knight/Walk/{}.PNG",
            "frame_count": 8,
            "frame_intervals": [2, 2, 2, 2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 8, # C++代码中指定为0
            "loop": True,
        },
        "right": {
            "path_template": "resource/img/hollow knight/WalkR/{}.PNG",
            "frame_count": 8,
            "frame_intervals": [2, 2, 2, 2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 8,
            "loop": True,
        }
    },
    "dash": {
        "left": {
            "path_template": "resource/img/hollow knight/Dash/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [1, 1, 1, 3, 3],
            "displacements": [(-45, 0), (-45, 0), (-45, 0), (-45, 0), (-45, 0)],
            "loop": False,
            "next_state": "idle",
            "effects": [
                { "name": "dash_effect", "frame": 0, "offset": {"x": 20, "y": -40} },
                { "name": "dash_effect", "frame": 1, "offset": {"x": 24, "y": -40} },
                { "name": "dash_effect", "frame": 2, "offset": {"x": 28, "y": -40} },
                { "name": "dash_effect", "frame": 3, "offset": {"x": 32, "y": -40} }
            ]
        },
        "right": {
            "path_template": "resource/img/hollow knight/DashR/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [1, 1, 1, 3, 3],
            "displacements": [(45, 0), (45, 0), (45, 0), (45, 0), (45, 0)],
            "loop": False,
            "next_state": "idle",
            "effects": [
                { "name": "dash_effect", "frame": 0, "offset": {"x": -20, "y": -40} },
                { "name": "dash_effect", "frame": 1, "offset": {"x": -24, "y": -40} },
                { "name": "dash_effect", "frame": 2, "offset": {"x": -28, "y": -40} },
                { "name": "dash_effect", "frame": 3, "offset": {"x": -32, "y": -40} }
            ]
        }
    },
    "attack1": {
        "left": {
            "path_template": "resource/img/hollow knight/Attack/Attack/1/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 1, 2, 2, 2],
            "displacements": [(0, 0), (0, 0), (0, 0), (-2, 0), (0, 0)],
            "loop": False,
            "next_state": "ready_to_combo",
            "effects": [
                { "name": "attack1_slash_effect", "frame": 0, "offset": {"x": -50, "y": 0} }
            ]
        },
        "right": {
            "path_template": "resource/img/hollow knight/AttackR/Attack/1/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 1, 2, 2, 2],
            "displacements": [(0, 0), (0, 0), (0, 0), (2, 0), (0, 0)],
            "loop": False,
            "next_state": "ready_to_combo",
            "effects": [
                { "name": "attack1_slash_effect", "frame": 0, "offset": {"x": 50, "y": 0} }
            ]
        }
    },
    "attack2": {
        "left": {
            "path_template": "resource/img/hollow knight/Attack/Attack/2/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 1, 2, 2, 2],
            "displacements": [(0, 0), (0, 0), (0, 0), (-2, 0), (0, 0)],
            "loop": False,
            "next_state": "idle",
             "effects": [
                { "name": "attack2_slash_effect", "frame": 0, "offset": {"x": -50, "y": 0} }
            ]
        },
        "right": {
            "path_template": "resource/img/hollow knight/AttackR/Attack/2/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 1, 2, 2, 2],
            "displacements": [(0, 0), (0, 0), (0, 0), (2, 0), (0, 0)],
            "loop": False,
            "next_state": "idle",
             "effects": [
                { "name": "attack2_slash_effect", "frame": 0, "offset": {"x": 50, "y": 0} }
            ]
        }
    },
    "attack_up": {
        "left": {
            "path_template": "resource/img/hollow knight/Attack/AttackUp/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 5,
            "loop": False,
            "next_state": "idle",
            "effects": [
                { "name": "attack_up_slash_effect", "frame": 0, "offset": {"x": 0, "y": -50} }
            ]
        },
        "right": {
            "path_template": "resource/img/hollow knight/AttackR/AttackUp/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 5,
            "loop": False,
            "next_state": "idle",
            "effects": [
                { "name": "attack_up_slash_effect", "frame": 0, "offset": {"x": 0, "y": -50} }
            ]
        }
    },
    "attack_down": {
        "left": {
            "path_template": "resource/img/hollow knight/Attack/AttackDown/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 5,
            "loop": False,
            "next_state": "idle",
            "effects": [
                { "name": "attack_down_slash_effect", "frame": 0, "offset": {"x": 0, "y": 50} }
            ]
        },
        "right": {
            "path_template": "resource/img/hollow knight/AttackR/AttackDown/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 5,
            "loop": False,
            "next_state": "idle",
            "effects": [
                { "name": "attack_down_slash_effect", "frame": 0, "offset": {"x": 0, "y": 50} }
            ]
        }
    },
    "jump_start": {
        "left": {
            "path_template": "resource/img/hollow knight/Jump/Start/{}.PNG",
            "frame_count": 9,
            "frame_intervals": [2, 2, 2, 2, 2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 9,
            "loop": False,
            "next_state": "jump_loop"
        },
        "right": {
            "path_template": "resource/img/hollow knight/JumpR/Start/{}.PNG",
            "frame_count": 9,
            "frame_intervals": [2, 2, 2, 2, 2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 9,
            "loop": False,
            "next_state": "jump_loop"
        }
    },
    "jump_loop": {
         "left": {
            "path_template": "resource/img/hollow knight/Jump/Loop/{}.PNG",
            "frame_count": 3,
            "frame_intervals": [2, 2, 2],
            "displacements": [(0, 0)] * 3,
            "loop": True,
        },
        "right": {
            "path_template": "resource/img/hollow knight/JumpR/Loop/{}.PNG",
            "frame_count": 3,
            "frame_intervals": [2, 2, 2],
            "displacements": [(0, 0)] * 3,
            "loop": True,
        }
    },
    "hurt": {
        "left": {
            "path_template": "resource/img/hollow knight/Damage/{}.PNG",
            "frame_count": 6,
            "frame_intervals": [4, 4, 4, 4, 4, 4],
            "displacements": [(-5, -10)] + [(0,0)]*5, # Add knockback on first frame
            "loop": False,
            "next_state": "idle"
        },
        "right": {
            "path_template": "resource/img/hollow knight/DamageR/{}.PNG",
            "frame_count": 6,
            "frame_intervals": [4, 4, 4, 4, 4, 4],
            "displacements": [(5, -10)] + [(0,0)]*5, # Add knockback on first frame
            "loop": False,
            "next_state": "idle"
        }
    },
     "damage": {
        "left": {
            "path_template": "resource/img/hollow knight/Damage/{}.png", # 修正为不带前导0的动作动画
            "frame_count": 6,
            "frame_intervals": [4, 4, 4, 4, 4, 4],
            "displacements": [(0, 0)] * 6, # 击退效果由速度脉冲处理，dmove清零
            "loop": False,
            "next_state": "idle",
            "effects": [
                { "name": "player_hurt_effect", "frame": 0, "offset": {"x": 0, "y": -50} }
            ]
        },
        "right": {
            "path_template": "resource/img/hollow knight/DamageR/{}.png", # 修正为不带前导0的动作动画
            "frame_count": 6,
            "frame_intervals": [4, 4, 4, 4, 4, 4],
            "displacements": [(0, 0)] * 6, # 击退效果由速度脉冲处理，dmove清零
            "loop": False,
            "next_state": "idle",
            "effects": [
                { "name": "player_hurt_effect", "frame": 0, "offset": {"x": 0, "y": -50} }
            ]
        }
    }
}

EFFECT_ANIMATIONS = {
    "player_hurt_effect": {
        "left": {
            "path_template": "resource/img/hollow knight/Damage/0{}.png", # 修正路径格式
            "frame_count": 3,
            "frame_intervals": [3, 3, 3],
            "displacements": [(0, 0)] * 3,
            "loop": False,
        },
        "right": {
            "path_template": "resource/img/hollow knight/Damage/0{}.png", # 修正路径格式
            "frame_count": 3,
            "frame_intervals": [3, 3, 3],
            "displacements": [(0, 0)] * 3,
            "loop": False,
        }
    },
    "dash_effect": {
        "left": {
            "path_template": "resource/img/hollow knight/DashEffect/{}.png",
            "frame_count": 4,
            "frame_intervals": [4, 4, 4, 4],
            "displacements": [(0, 0)] * 4,
            "loop": False
        },
        "right": {
            "path_template": "resource/img/hollow knight/DashEffectR/{}.png",
            "frame_count": 4,
            "frame_intervals": [4, 4, 4, 4],
            "displacements": [(0, 0)] * 4,
            "loop": False
        }
    },
    "attack1_slash_effect": {
        "left": {
            "path_template": "resource/img/hollow knight/Attack/Attack/1/0{}.png",
            "frame_count": 2,
            "frame_intervals": [3, 3],
            "displacements": [(0, 0)] * 2,
            "loop": False
        },
        "right": {
            "path_template": "resource/img/hollow knight/AttackR/Attack/1/0{}.png",
            "frame_count": 2,
            "frame_intervals": [3, 3],
            "displacements": [(0, 0)] * 2,
            "loop": False
        }
    },
    "attack2_slash_effect": {
        "left": {
            "path_template": "resource/img/hollow knight/Attack/Attack/2/0{}.png",
            "frame_count": 2,
            "frame_intervals": [3, 3],
            "displacements": [(0, 0)] * 2,
            "loop": False
        },
        "right": {
            "path_template": "resource/img/hollow knight/AttackR/Attack/2/0{}.png",
            "frame_count": 2,
            "frame_intervals": [3, 3],
            "displacements": [(0, 0)] * 2,
            "loop": False
        }
    },
    "attack_up_slash_effect": {
        "left": {
            "path_template": "resource/img/hollow knight/Attack/AttackUp/0{}.png",
            "frame_count": 2,
            "frame_intervals": [3, 3],
            "displacements": [(0, 0)] * 2,
            "loop": False
        },
        "right": {
            "path_template": "resource/img/hollow knight/AttackR/AttackUp/0{}.png",
            "frame_count": 2,
            "frame_intervals": [3, 3],
            "displacements": [(0, 0)] * 2,
            "loop": False
        }
    },
    "attack_down_slash_effect": {
        "left": {
            "path_template": "resource/img/hollow knight/Attack/AttackDown/0{}.png",
            "frame_count": 2,
            "frame_intervals": [3, 3],
            "displacements": [(0, 0)] * 2,
            "loop": False
        },
        "right": {
            "path_template": "resource/img/hollow knight/AttackR/AttackDown/0{}.png",
            "frame_count": 2,
            "frame_intervals": [3, 3],
            "displacements": [(0, 0)] * 2,
            "loop": False
        }
    },
    "hit_effect": {
        "left": {
            "path_template": "resource/img/hollow knight/AttackEffect/Attack/0{}.png",
            "frame_count": 5,
            "frame_intervals": [3, 3, 3, 3, 3],
            "displacements": [(0, 0)] * 5,
            "loop": False
        },
        "right": {
            "path_template": "resource/img/hollow knight/AttackEffect/AttackR/0{}.png",
            "frame_count": 5,
            "frame_intervals": [3, 3, 3, 3, 3],
            "displacements": [(0, 0)] * 5,
            "loop": False
        }
    },
    "boss_dash_effect": {
        "left": {
            "path_template": "resource/img/hollow knight/Boss/Dash/{}.png",
            "frame_names": ["00", "01", "02", "03"],
            "frame_intervals": [4, 4, 4, 4],
            "displacements": [(0, 0)] * 4,
            "loop": False
        },
        "right": {
            "path_template": "resource/img/hollow knight/Boss/DashR/{}.png",
            "frame_names": ["00", "01", "02", "03"],
            "frame_intervals": [4, 4, 4, 4],
            "displacements": [(0, 0)] * 4,
            "loop": False
        }
    },
    "boss_jump_final_effect": {
        "left": {
            "path_template": "resource/img/hollow knight/Boss/JumpFinal/Effects/{}.png",
            "frame_names": [
                "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", 
                "010", "011", "012", "013", "014", "015", "016", "017"
            ],
            "frame_intervals": [4] * 18,
            "displacements": [(0, 0)] * 18,
            "loop": False,
            "damage": 1
        },
        "right": {
            "path_template": "resource/img/hollow knight/Boss/JumpFinalR/Effects/{}.png",
            "frame_names": [
                "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", 
                "010", "011", "012", "013", "014", "015", "016"
            ],
            "frame_intervals": [4] * 17,
            "displacements": [(0, 0)] * 17,
            "loop": False,
            "damage": 1
        }
    }
}


BOSS_ANIMATIONS = {
    "idle": {
        "left": {
            "path_template": "resource/img/hollow knight/Boss/Idle/{}.png",
            "frame_names": ["0", "1"],
            "frame_intervals": [12, 12],
            "displacements": [(0, 0)] * 2,
            "loop": True
        },
        "right": {
            "path_template": "resource/img/hollow knight/Boss/IdleR/{}.png",
            "frame_names": ["0", "1"],
            "frame_intervals": [12, 12],
            "displacements": [(0, 0)] * 2,
            "loop": True
        }
    },
    "walk": {
        "left": {
            "path_template": "resource/img/hollow knight/Boss/Walk/{}.png",
            "frame_names": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            "frame_intervals": [3] * 11,
            "displacements": [(0, 0)] * 11,
            "loop": True
        },
        "right": {
            "path_template": "resource/img/hollow knight/Boss/WalkR/{}.png",
            "frame_names": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            "frame_intervals": [3] * 11,
            "displacements": [(0, 0)] * 11,
            "loop": True
        }
    },
    "jump": {
        "left": {
            "path_template": "resource/img/hollow knight/Boss/Jump/{}.png",
            "frame_names": [
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", 
                "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
                "26", "27", "28"
            ],
            "frame_intervals": [3] * 29,
            "displacements": [(0, 0)] * 29,
            "loop": False,
            "next_state": "idle"
        },
        "right": {
            "path_template": "resource/img/hollow knight/Boss/JumpR/{}.png",
            "frame_names": [
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", 
                "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
                "26", "27", "28"
            ],
            "frame_intervals": [3] * 29,
            "displacements": [(0, 0)] * 29,
            "loop": False,
            "next_state": "idle"
        }
    },
    "dash": {
        "left": {
            "path_template": "resource/img/hollow knight/Boss/Dash/{}.png",
            "frame_names": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
            "frame_intervals": [3] * 12,
            "displacements": [(-20, 0)] * 12,
            "loop": False,
            "next_state": "idle",
            "effects": [
                { "name": "boss_dash_effect", "frame": 2, "offset": {"x": 0, "y": -20} }
            ]
        },
        "right": {
            "path_template": "resource/img/hollow knight/Boss/DashR/{}.png",
            "frame_names": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
            "frame_intervals": [3] * 12,
            "displacements": [(20, 0)] * 12,
            "loop": False,
            "next_state": "idle",
            "effects": [
                { "name": "boss_dash_effect", "frame": 2, "offset": {"x": 0, "y": -20} }
            ]
        }
    },
    "jump_dash": {
        "left": {
            "path_template": "resource/img/hollow knight/Boss/JumpDash/{}.png",
            "frame_names": [
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", 
                "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
                "26", "27", "28"
            ],
            "frame_intervals": [3] * 29,
            "displacements": [(0, 0)] * 29,
            "loop": False,
            "next_state": "idle"
        },
        "right": {
            "path_template": "resource/img/hollow knight/Boss/JumpDashR/{}.png",
            "frame_names": [
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", 
                "14", "15", "16", "17", "18", "19", "20", "21", "22", "220", "23", "24", 
                "25", "26", "27", "28"
            ],
            "frame_intervals": [3] * 30,
            "displacements": [(0, 0)] * 30,
            "loop": False,
            "next_state": "idle"
        }
    },
    "jump_final_air": {
        "left": {
            "path_template": "resource/img/hollow knight/Boss/JumpFinal/{}.png",
            "frame_names": [
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", 
                "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
                "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
                "38", "39", "40", "41", "42", "43", "44", "45"
            ],
            "frame_intervals": [4] * 46,
            "displacements": [(0, 0)] * 46,
            "loop": False,
            "next_state": "idle",
            "effects": [
                { "name": "boss_jump_final_effect", "frame": 7, "offset": {"x": 0, "y": 25} }
            ]
        },
        "right": {
            "path_template": "resource/img/hollow knight/Boss/JumpFinalR/{}.png",
            "frame_names": [
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", 
                "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
                "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
                "38", "39", "40", "41", "42", "43", "44", "45"
            ],
            "frame_intervals": [4] * 46,
            "displacements": [(0, 0)] * 46,
            "loop": False,
            "next_state": "idle",
             "effects": [
                { "name": "boss_jump_final_effect", "frame": 7, "offset": {"x": 0, "y": 25} }
            ]
        }
    },
    "jump_final_ground": {
        "left": {
            "path_template": "resource/img/hollow knight/Boss/JumpFinal/{}.png",
            "frame_names": [
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
                "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
                "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
                "38", "39", "40", "41", "42", "43", "44", "45"
            ],
            "frame_intervals": [4] * 46,
            "displacements": [(0, 0)] * 46,
            "loop": False,
            "next_state": "idle"
        },
        "right": {
            "path_template": "resource/img/hollow knight/Boss/JumpFinalR/{}.png",
            "frame_names": [
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
                "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
                "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
                "38", "39", "40", "41", "42", "43", "44", "45"
            ],
            "frame_intervals": [4] * 46,
            "displacements": [(0, 0)] * 46,
            "loop": False,
            "next_state": "idle"
        }
    }
}
# TODO: 以后我们还会在这里添加 BOSS_ANIMATIONS 和 EFFECT_ANIMATIONS
# C++ 代码中的特效是和攻击动画绑定的，我们需要一个新的系统来处理
# 暂时将特效数据注释掉，后续再整合
"""
EFFECT_DATA = {
    "player_dash_left": {
        "path_template": "resource/img/hollow knight/DashEffect/{}.png",
        "frame_count": 4,
        "displacements": [(20, -100), (24, -100), (28, -100), (32, -100)]
    },
    "player_dash_right": {
        "path_template": "resource/img/hollow knight/DashEffectR/{}.png",
        "frame_count": 4,
        "displacements": [(-430, -100), (-426, -100), (-422, -100), (-418, -100)]
    },
    ...
}
""" 