# systems/combat.py
import pygame
from typing import List

from interfaces import ICombatSystem, Entity, AnimationState
from gameplay.player import Player
from gameplay.boss import Boss
from .physics import PhysicsSystem

class CombatSystem(ICombatSystem):
    def __init__(self, physics_system: PhysicsSystem):
        self.physics_system = physics_system

    def update(self, player: Player, enemies: List[Boss]):
        if player.state == AnimationState.DEAD:
            return

        for boss in enemies:
            if boss.state == AnimationState.DEAD:
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
                # 成功下劈后触发pogo弹跳
                if player.state == AnimationState.ATTACK_DOWN:
                    player.pogo_bounce()