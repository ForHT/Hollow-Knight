# systems/combat.py
import pygame
from typing import List

from interfaces import ICombatSystem, Entity, Vector2
from gameplay.player import Player
from gameplay.boss import Boss
from core.animation_system import VFXManager
from core.audio_manager import AudioManager
from .physics import PhysicsSystem

class CombatSystem(ICombatSystem):
    def __init__(self, physics_system: PhysicsSystem, vfx_manager: VFXManager, audio_manager: AudioManager):
        self.physics_system = physics_system
        self.vfx_manager = vfx_manager
        self.audio_manager = audio_manager

    def update(self, player: Player, enemies: List[Boss]):
        if player.state == "dead":
            return

        # 1. 玩家受到特效攻击的伤害
        for effect in self.vfx_manager.effects:
            effect_hitbox = effect.get_attack_hitbox()
            if player.invincible_timer <= 0 and effect_hitbox and effect_hitbox.colliderect(player.hitbox):
                if hasattr(effect, 'damage'):
                    player.take_damage(effect.damage)

        for boss in enemies:
            if boss.state == "dead":
                continue

            # 1. 玩家受到Boss的身体接触伤害
            if player.invincible_timer <= 0 and self.physics_system.check_collision(player, boss):
                player.take_damage(boss.body_damage)

            # 2. 玩家受到Boss攻击的伤害
            boss_attack_box = boss.get_attack_hitbox()
            if player.invincible_timer <= 0 and boss_attack_box and boss_attack_box.colliderect(player.hitbox):
                player.take_damage(boss.attack_power)
            
            # 3. Boss受到玩家攻击的伤害
            player_attack_box = player.get_attack_hitbox()
            if boss.invincible_timer <= 0 and player_attack_box and player_attack_box.colliderect(boss.hitbox):
                boss.take_damage(player.attack_power)
                self.audio_manager.play_sound("attack_hit")
                
                # 创建命中特效
                self.vfx_manager.create_effect(
                    pos=Vector2(boss.hitbox.center), 
                    animation_name="hit_effect",
                    facing_right=player.facing_right
                )

                # 成功下劈后触发pogo弹跳
                if player.state == "attack_down":
                    player.pogo_bounce()