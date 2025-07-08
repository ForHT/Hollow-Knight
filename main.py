# main.py (最终修正版 - 解决所有已知问题)
import pygame, sys, math, random
from animation import Animation
from actor import Actor
from animation_name import AnimationName
from vector2 import Vector2
from point import Point

pygame.init(); pygame.mixer.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1440, 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hollow Knight - Python Remake")
clock = pygame.time.Clock()
Background, EMPTYBLOOD, SOUL, OPENGROUND, TITLE, LOGO, PRESS_TO_START, PLAYAGAIN, COIN, MONEY = (None,)*10
PLAYER_IDLE, PLAYER_WALK, PLAYER_DASH, PLAYER_JUMPSTART, PLAYER_ATTACK, PLAYER_UPATTACK, PLAYER_JUMPLOOP, PLAYER_ATTACKTWICE, PLAYER_DOUBLEJUMP, PLAYER_DOWNATTACK, PLAYER_DAMAGE, PLAYER_ATTACKHIT = ([Animation(), Animation()] for _ in range(12))
PLAYER_JUMPLAND, PLAYER_DEATH = Animation(), Animation()
B_IDLE, B_JUMPDASH, B_WALK, B_THROWSIDE, B_JUMP, B_DASH, B_LAND, B_JUMPFINAL = ([Animation(), Animation()] for _ in range(8))
BLOOD, BLOOD_DAMAGE, ARROR = Animation(), Animation(), [Animation(), Animation()]
CurrentEnemyAnimation, CurrentPlayerAnimation, CurrentPlayerLoopAnimation = Animation(), Animation(), Animation()
nullanimation = Animation(); nullanimation.animationname = AnimationName.NU
Player = Actor(200, 680); testenemy = Actor(1000, 585)
scenemanager = 0; shootdirection, normal_shootdirection = Vector2(), Vector2()

def get_direction(p1,p2): return Vector2(p2.x-p1.x, p2.y-p1.y)
def get_normal_direction(p1,p2): return get_direction(p1,p2).normalize()
def putimage_1(x,y,img):
    if img: screen.blit(img,(x,y))
def RotateImage_Alpha(pImg,rad): return pygame.transform.rotate(pImg,-math.degrees(rad))
def attack_judger(player,enemy):
    if enemy.UnHurtableTime > 0: return False
    pa,ea=CurrentPlayerAnimation,CurrentEnemyAnimation
    if ea.animationname == AnimationName.NU or not ea.frame_list: return False
    if pa.animationname in [AnimationName.PLAYER_ATTACK0,AnimationName.PLAYER_UPATTACK0,AnimationName.PLAYER_ATTACKTWICE0]:
        if not pa.Effects or len(pa.Effects)==0 or pa.Effects[0].get_width() <= 1: return False
        w1,h1=pa.Effects[0].get_size()
        w2,h2=ea.frame_list[ea.current_frameidx].get_width()-50,ea.frame_list[ea.current_frameidx].get_height()-50
        ec_x,ec_y = player.position.x+pa.dmove[pa.current_frameidx][0]+(2*player.Facing_Right-1)*w1/2, player.position.y+pa.dmove[pa.current_frameidx][1]+h1/2
        en_x,en_y = enemy.position.x+w2/2,enemy.position.y+h2/2
        if (player.Facing_Right*2-1)*get_direction(player.position,enemy.position).vx >= 0:
            if abs(en_x-ec_x)<(w1+w2)/2 and abs(en_y-ec_y)<(h1+h2)/2: return True
        return False
    elif pa.animationname == AnimationName.PLAYER_DOWNATTACK0:
        return 0<=player.position.y-enemy.position.y<=550 and -100<=player.position.x-enemy.position.x<=150
    return False
def attacked_judger(player,enemy):
    if player.UnHurtableTime > 0: return False
    p_img,e_img=None,None
    if CurrentPlayerAnimation.animationname!=AnimationName.NU and CurrentPlayerAnimation.frame_list: p_img=CurrentPlayerAnimation.frame_list[CurrentPlayerAnimation.current_frameidx]
    elif CurrentPlayerLoopAnimation.animationname!=AnimationName.NU and CurrentPlayerLoopAnimation.frame_list: p_img=CurrentPlayerLoopAnimation.frame_list[CurrentPlayerLoopAnimation.current_frameidx]
    if CurrentEnemyAnimation.animationname!=AnimationName.NU and CurrentEnemyAnimation.frame_list: e_img=CurrentEnemyAnimation.frame_list[CurrentEnemyAnimation.current_frameidx]
    if not p_img or not e_img: return False
    p_rect=pygame.Rect(player.position.x,player.position.y,p_img.get_width(),p_img.get_height())
    e_rect=pygame.Rect(enemy.position.x,enemy.position.y,e_img.get_width(),e_img.get_height())
    if CurrentEnemyAnimation.animationname==AnimationName.B_JUMPFINAL0 and 21<=CurrentEnemyAnimation.current_frameidx<=36: e_rect.inflate_ip(200,220)
    else: e_rect.inflate_ip(-180,-160)
    return p_rect.colliderect(e_rect)
def gravity_collide(player,enemy):
    player.speed.vy+=player.gravity;player.position.y+=player.speed.vy/30
    enemy.speed.vy+=enemy.gravity;enemy.position.y+=enemy.speed.vy/30
    if player.position.y>680:player.speed.vy=0;player.position.y=680
    if enemy.position.y>585:enemy.speed.vy=0;enemy.position.y=585
    if CurrentPlayerAnimation.animationname==AnimationName.PLAYER_DASH0:player.speed.vy=0
    if CurrentPlayerAnimation.animationname==AnimationName.PLAYER_DOWNATTACK0 and player.position.y==680:player.speed.vy=-30
    if CurrentEnemyAnimation.animationname==AnimationName.B_JUMPFINAL0 and 15<=CurrentEnemyAnimation.current_frameidx<=33: enemy.gravity=0;enemy.speed.vy=0;enemy.speed.vx=0
    elif CurrentEnemyAnimation.animationname==AnimationName.B_JUMPFINAL0:enemy.speed.vy=0;enemy.gravity=4
def music_player(sounds,music_cd):
    a,b=CurrentPlayerAnimation,CurrentEnemyAnimation
    if a.animationname!=AnimationName.NU and a.frame_list and a.current_frameidx<len(a.tmp_interval) and a.tmp_interval[a.current_frameidx]==a.frameinterval[a.current_frameidx]:
        if a.animationname==AnimationName.PLAYER_ATTACK0:sounds["attackhit" if attack_judger(Player,testenemy) else "attack1"].play()
        elif a.animationname==AnimationName.PLAYER_ATTACKTWICE0:sounds["attack2"].play()
        elif a.animationname==AnimationName.PLAYER_UPATTACK0:sounds["attackup"].play()
        elif a.animationname==AnimationName.PLAYER_DOWNATTACK0:sounds["attack1"].play()
        elif a.animationname==AnimationName.PLAYER_DAMAGE0:sounds["playerdamage"].play()
    if music_cd==0 and b.animationname!=AnimationName.NU and b.frame_list and b.current_frameidx<len(b.tmp_interval) and b.tmp_interval[b.current_frameidx]==b.frameinterval[b.current_frameidx]:
        if b.animationname not in [AnimationName.B_WALK0,AnimationName.B_IDLEL0,AnimationName.B_IDLER0,AnimationName.B_LAND0]:
            if b.animationname==AnimationName.B_JUMP0:sounds[random.choice(["haha","henhen"])].play()
            else:sounds[random.choice(["aidito","ha","gadama","heigali","higali","xiao"])].play()
            return 90
    return music_cd
def draw_actor_anim(actor,anim):
    global CurrentPlayerAnimation,CurrentEnemyAnimation
    if not anim or not anim.frame_list or anim.current_frameidx>=len(anim.frame_list): return
    idx=anim.current_frameidx
    actor.position.x+=anim.dmove[idx][0];actor.position.y+=anim.dmove[idx][1]
    anim.tmp_interval[idx]-=1
    putimage_1(actor.position.x,actor.position.y,anim.frame_list[idx])
    if anim.Effects and idx>=anim.StartFrame:
        m=min(len(anim.Effects)-1,idx-anim.StartFrame)
        if 0<=m<len(anim.Erelative) and 0<=m<len(anim.Effects):putimage_1(actor.position.x+anim.Erelative[m].vx,actor.position.y+anim.Erelative[m].vy,anim.Effects[m])
    if anim.PlayHitAnimation and anim.HitEffects:
        m=min(len(anim.HitEffects)-1,idx-anim.HitStartFrame)
        if 0<=m<len(anim.HitErelative) and 0<=m<len(anim.HitEffects):putimage_1(actor.position.x+anim.HitErelative[m].vx,actor.position.y+anim.HitErelative[m].vy,anim.HitEffects[m])
    if anim.tmp_interval[idx]<=0:
        actor.position.x+=anim.relative[idx].vx;actor.position.y+=anim.relative[idx].vy
        anim.current_frameidx+=1
        if anim.current_frameidx>=anim.frame_num:
            if anim.canloop:anim.current_frameidx=anim.loop_index;anim.tmp_interval=anim.frameinterval[:]
            else:
                if anim is CurrentPlayerAnimation:CurrentPlayerAnimation=nullanimation.copy()
                elif anim is CurrentEnemyAnimation:CurrentEnemyAnimation=nullanimation.copy()
                anim.PlayHitAnimation=False
def draw_ui_anim(anim,x,y):
    if not anim or not anim.frame_list: return
    idx=anim.current_frameidx;anim.tmp_interval[idx]-=1
    putimage_1(x+anim.dmove[idx][0],y+anim.dmove[idx][1],anim.frame_list[idx])
    if anim.tmp_interval[idx]<=0:
        anim.current_frameidx+=1
        if anim.current_frameidx>=anim.frame_num:
            anim.current_frameidx=anim.loop_index if anim.canloop else 0
            anim.tmp_interval=anim.frameinterval[:]

def main():
    global Background,EMPTYBLOOD,SOUL,OPENGROUND,TITLE,LOGO,PRESS_TO_START,PLAYAGAIN,COIN,MONEY,Player,testenemy,scenemanager,CurrentEnemyAnimation,CurrentPlayerAnimation,CurrentPlayerLoopAnimation,shootdirection,normal_shootdirection
    try:
        COIN=pygame.image.load("assets/UI/coin.png").convert_alpha();MONEY=pygame.image.load("assets/UI/money.png").convert_alpha();PLAYAGAIN=pygame.image.load("assets/UI/playagain.png").convert_alpha();Background=pygame.image.load("assets/img/hollow knight/background.png").convert()
        sounds={"bgm":"assets/music/Hornet.mp3","attack1":pygame.mixer.Sound("assets/music/Player/sword_1.wav"),"attack2":pygame.mixer.Sound("assets/music/Player/sword_2.wav"),"attackhit":pygame.mixer.Sound("assets/music/Player/sword_hit.wav"),"attackup":pygame.mixer.Sound("assets/music/Player/sword_up.wav"),"playerdamage":pygame.mixer.Sound("assets/music/Player/player_damage.wav"),"aidito":pygame.mixer.Sound("assets/music/Boss/aidito.mp3"),"gadama":pygame.mixer.Sound("assets/music/Boss/gadama.mp3"),"ha":pygame.mixer.Sound("assets/music/Boss/ha.mp3"),"haha":pygame.mixer.Sound("assets/music/Boss/haha.mp3"),"heigali":pygame.mixer.Sound("assets/music/Boss/heigali.mp3"),"henhen":pygame.mixer.Sound("assets/music/Boss/henhen.mp3"),"higali":pygame.mixer.Sound("assets/music/Boss/higali.mp3"),"xiao":pygame.mixer.Sound("assets/music/Boss/xiao.mp3"),"open":pygame.mixer.Sound("assets/music/Boss/open.mp3"),"hea":pygame.mixer.Sound("assets/music/Boss/hea.mp3"),"Title":"assets/UI/Title.mp3","Confirm":pygame.mixer.Sound("assets/UI/Confirm.mp3")}
    except (pygame.error, FileNotFoundError) as e:print(f"FATAL: Asset loading failed: {e}");return
    
    PLAYER_IDLE[0].load_animation("assets/img/hollow knight/Idle/%d.PNG",9,AnimationName.PLAYER_IDLE0);PLAYER_IDLE[0].canloop=True;PLAYER_IDLE[0].frameinterval=[4]*9;PLAYER_IDLE[0].tmp_interval=PLAYER_IDLE[0].frameinterval[:]
    PLAYER_IDLE[1].load_animation("assets/img/hollow knight/IdleR/%d.PNG",9,AnimationName.PLAYER_IDLE0);PLAYER_IDLE[1].canloop=True;PLAYER_IDLE[1].frameinterval=[4]*9;PLAYER_IDLE[1].tmp_interval=PLAYER_IDLE[1].frameinterval[:]
    PLAYER_WALK[0].load_animation("assets/img/hollow knight/Walk/%d.PNG",8,AnimationName.PLAYER_WALKL0);PLAYER_WALK[0].canloop=True;PLAYER_WALK[0].loop_index=3;PLAYER_WALK[0].frameinterval=[2]*8;PLAYER_WALK[0].tmp_interval=PLAYER_WALK[0].frameinterval[:]
    PLAYER_WALK[1].load_animation("assets/img/hollow knight/WalkR/%d.PNG",8,AnimationName.PLAYER_WALKR0);PLAYER_WALK[1].canloop=True;PLAYER_WALK[1].loop_index=3;PLAYER_WALK[1].frameinterval=[2]*8;PLAYER_WALK[1].tmp_interval=PLAYER_WALK[1].frameinterval[:]
    PLAYER_DASH[0].load_animation("assets/img/hollow knight/Dash/%d.PNG",5,AnimationName.PLAYER_DASH0);PLAYER_DASH[0].load_effect("assets/img/hollow knight/DashEffect/%d.png",0,4,4);[PLAYER_DASH[0].Erelative.append(Vector2(20+4*i,-100)) for i in range(4)];PLAYER_DASH[0].frameinterval=[1,1,1,3,3];PLAYER_DASH[0].tmp_interval=PLAYER_DASH[0].frameinterval[:];PLAYER_DASH[0].dmove=[[-45,0]]*5
    PLAYER_DASH[1].load_animation("assets/img/hollow knight/DashR/%d.PNG",5,AnimationName.PLAYER_DASH0);PLAYER_DASH[1].load_effect("assets/img/hollow knight/DashEffectR/%d.png",0,4,4);[PLAYER_DASH[1].Erelative.append(Vector2(-100-PLAYER_DASH[1].Effects[i].get_width()+4*i,-100)) for i in range(4)];PLAYER_DASH[1].frameinterval=[1,1,1,3,3];PLAYER_DASH[1].tmp_interval=PLAYER_DASH[1].frameinterval[:];PLAYER_DASH[1].dmove=[[45,0]]*5;PLAYER_DASH[1].relative=[Vector2(-75,0),Vector2(15,0),Vector2(15,0),Vector2(45,0),Vector2(25,0)]
    PLAYER_ATTACK[0].load_animation("assets/img/hollow knight/Attack/Attack/1/%d.PNG",5,AnimationName.PLAYER_ATTACK0);PLAYER_ATTACK[0].load_effect("assets/img/hollow knight/Attack/Attack/1/%d.png",3,4,2,name_indices=range(3,5));PLAYER_ATTACK[0].frameinterval=[2,1,2,2,2];PLAYER_ATTACK[0].tmp_interval=PLAYER_ATTACK[0].frameinterval[:];PLAYER_ATTACK[0].dmove[3][0]=-2;PLAYER_ATTACK[0].CD=45;PLAYER_ATTACK[0].Erelative=[Vector2(-165,20),Vector2(-135,30)]
    PLAYER_ATTACK[1].load_animation("assets/img/hollow knight/AttackR/Attack/1/%d.PNG",5,AnimationName.PLAYER_ATTACK0);PLAYER_ATTACK[1].load_effect("assets/img/hollow knight/AttackR/Attack/1/%d.png",3,4,2,name_indices=range(3,5));PLAYER_ATTACK[1].frameinterval=[2,1,2,2,2];PLAYER_ATTACK[1].tmp_interval=PLAYER_ATTACK[1].frameinterval[:];PLAYER_ATTACK[1].dmove[3][0]=2;PLAYER_ATTACK[1].CD=30;PLAYER_ATTACK[1].Erelative=[Vector2(90,20),Vector2(50,25)]
    PLAYER_ATTACKTWICE[0].load_animation("assets/img/hollow knight/Attack/Attack/2/%d.png",5,AnimationName.PLAYER_ATTACKTWICE0);PLAYER_ATTACKTWICE[0].load_effect("assets/img/hollow knight/Attack/Attack/2/%d.png",2,3,2,name_indices=range(2,4));PLAYER_ATTACKTWICE[0].frameinterval=[2,1,2,2,2];PLAYER_ATTACKTWICE[0].tmp_interval=PLAYER_ATTACKTWICE[0].frameinterval[:];PLAYER_ATTACKTWICE[0].dmove[3][0]=-2;PLAYER_ATTACKTWICE[0].CD=45;PLAYER_ATTACKTWICE[0].Erelative=[Vector2(-145,5),Vector2(-60,-55)]
    PLAYER_ATTACKTWICE[1].load_animation("assets/img/hollow knight/AttackR/Attack/2/%d.png",5,AnimationName.PLAYER_ATTACKTWICE0);PLAYER_ATTACKTWICE[1].load_effect("assets/img/hollow knight/AttackR/Attack/2/%d.png",2,3,2,name_indices=range(2,4));PLAYER_ATTACKTWICE[1].frameinterval=[2,1,2,2,2];PLAYER_ATTACKTWICE[1].tmp_interval=PLAYER_ATTACKTWICE[1].frameinterval[:];PLAYER_ATTACKTWICE[1].dmove[3][0]=2;PLAYER_ATTACKTWICE[1].CD=45;PLAYER_ATTACKTWICE[1].Erelative=[Vector2(5,-5),Vector2(-60,-65)]
    PLAYER_UPATTACK[0].load_animation("assets/img/hollow knight/Attack/AttackUp/%d.PNG",5,AnimationName.PLAYER_UPATTACK0);PLAYER_UPATTACK[0].load_effect("assets/img/hollow knight/Attack/AttackUp/%d.png",2,4,2,name_indices=range(2,4));PLAYER_UPATTACK[0].frameinterval=[2]*5;PLAYER_UPATTACK[0].tmp_interval=PLAYER_UPATTACK[0].frameinterval[:];PLAYER_UPATTACK[0].CD=20;PLAYER_UPATTACK[0].Erelative=[Vector2(-50,-145),Vector2(10,-95)]
    PLAYER_UPATTACK[1].load_animation("assets/img/hollow knight/AttackR/AttackUp/%d.PNG",5,AnimationName.PLAYER_UPATTACK0);PLAYER_UPATTACK[1].load_effect("assets/img/hollow knight/AttackR/AttackUp/%d.png",2,4,2,name_indices=range(2,4));PLAYER_UPATTACK[1].frameinterval=[2]*5;PLAYER_UPATTACK[1].tmp_interval=PLAYER_UPATTACK[1].frameinterval[:];PLAYER_UPATTACK[1].CD=20;PLAYER_UPATTACK[1].Erelative=[Vector2(-50,-145),Vector2(-110,-95)]
    PLAYER_JUMPSTART[0].load_animation("assets/img/hollow knight/Jump/Start/%d.PNG",9,AnimationName.PLAYER_JUMPSTART0);PLAYER_JUMPSTART[0].frameinterval=[2]*9;PLAYER_JUMPSTART[0].tmp_interval=PLAYER_JUMPSTART[0].frameinterval[:]
    PLAYER_JUMPSTART[1].load_animation("assets/img/hollow knight/JumpR/Start/%d.PNG",9,AnimationName.PLAYER_JUMPSTART0);PLAYER_JUMPSTART[1].frameinterval=[2]*9;PLAYER_JUMPSTART[1].tmp_interval=PLAYER_JUMPSTART[1].frameinterval[:]
    PLAYER_JUMPLOOP[0].load_animation("assets/img/hollow knight/Jump/Loop/%d.PNG",3,AnimationName.PLAYER_JUMPLOOP0);PLAYER_JUMPLOOP[0].canloop=True;PLAYER_JUMPLOOP[0].frameinterval=[2]*3;PLAYER_JUMPLOOP[0].tmp_interval=PLAYER_JUMPLOOP[0].frameinterval[:]
    PLAYER_JUMPLOOP[1].load_animation("assets/img/hollow knight/JumpR/Loop/%d.PNG",3,AnimationName.PLAYER_JUMPLOOP0);PLAYER_JUMPLOOP[1].canloop=True;PLAYER_JUMPLOOP[1].frameinterval=[2]*3;PLAYER_JUMPLOOP[1].tmp_interval=PLAYER_JUMPLOOP[1].frameinterval[:]
    PLAYER_DOWNATTACK[0].load_animation("assets/img/hollow knight/Attack/AttackDown/%d.PNG",5,AnimationName.PLAYER_DOWNATTACK0);PLAYER_DOWNATTACK[0].load_effect("assets/img/hollow knight/Attack/AttackDown/%d.png",2,4,2,name_indices=range(2,4));PLAYER_DOWNATTACK[0].frameinterval=[2]*5;PLAYER_DOWNATTACK[0].tmp_interval=PLAYER_DOWNATTACK[0].frameinterval[:];PLAYER_DOWNATTACK[0].CD=20;PLAYER_DOWNATTACK[0].Erelative=[Vector2(-35,0),Vector2(5,0)]
    PLAYER_DOWNATTACK[1].load_animation("assets/img/hollow knight/AttackR/AttackDown/%d.PNG",5,AnimationName.PLAYER_DOWNATTACK0);PLAYER_DOWNATTACK[1].load_effect("assets/img/hollow knight/AttackR/AttackDown/%d.png",2,4,2,name_indices=range(2,4));PLAYER_DOWNATTACK[1].frameinterval=[2]*5;PLAYER_DOWNATTACK[1].tmp_interval=PLAYER_DOWNATTACK[1].frameinterval[:];PLAYER_DOWNATTACK[1].CD=20;PLAYER_DOWNATTACK[1].Erelative=[Vector2(0,0),Vector2(-50,0)]
    PLAYER_DAMAGE[0].load_animation("assets/img/hollow knight/Damage/%d.PNG",6,AnimationName.PLAYER_DAMAGE0);PLAYER_DAMAGE[0].load_effect("assets/img/hollow knight/Damage/0%d.PNG",0,6,3);PLAYER_DAMAGE[0].frameinterval=[4]*6;PLAYER_DAMAGE[0].tmp_interval=PLAYER_DAMAGE[0].frameinterval[:];PLAYER_DAMAGE[0].CD=45
    PLAYER_DAMAGE[1].load_animation("assets/img/hollow knight/DamageR/%d.PNG",6,AnimationName.PLAYER_DAMAGE0);PLAYER_DAMAGE[1].load_effect("assets/img/hollow knight/Damage/0%d.PNG",0,6,3);PLAYER_DAMAGE[1].frameinterval=[4]*6;PLAYER_DAMAGE[1].tmp_interval=PLAYER_DAMAGE[1].frameinterval[:];PLAYER_DAMAGE[1].CD=45
    for i in range(3):PLAYER_DAMAGE[0].Effects[i]=RotateImage_Alpha(PLAYER_DAMAGE[0].Effects[i],-math.pi/6);PLAYER_DAMAGE[1].Effects[i]=RotateImage_Alpha(PLAYER_DAMAGE[1].Effects[i],math.pi/6);PLAYER_DAMAGE[0].Erelative.append(Vector2(-290,-150));PLAYER_DAMAGE[1].Erelative.append(Vector2(-290,-150))
    PLAYER_ATTACK[0].load_hit_effect("assets/img/hollow knight/Attack/Attack/1/%d.png",0,4,5,name_indices=range(3,8));PLAYER_ATTACK[1].load_hit_effect("assets/img/hollow knight/AttackR/Attack/1/%d.png",0,4,5,name_indices=range(3,8));[PLAYER_ATTACK[0].HitErelative.append(Vector2(-340,-80)) for _ in range(5)];[PLAYER_ATTACK[1].HitErelative.append(Vector2(-60,-80)) for _ in range(5)]
    PLAYER_ATTACKTWICE[0].load_hit_effect("assets/img/hollow knight/Attack/Attack/2/%d.png",0,4,5,name_indices=range(2,7));PLAYER_ATTACKTWICE[1].load_hit_effect("assets/img/hollow knight/AttackR/Attack/2/%d.png",0,4,5,name_indices=range(2,7));[PLAYER_ATTACKTWICE[0].HitErelative.append(Vector2(-340,-80)) for _ in range(5)];[PLAYER_ATTACKTWICE[1].HitErelative.append(Vector2(-60,-80)) for _ in range(5)]
    PLAYER_DOWNATTACK[0].load_hit_effect("assets/img/hollow knight/Attack/AttackDown/%d.png",0,4,5,name_indices=range(2,7));PLAYER_DOWNATTACK[1].load_hit_effect("assets/img/hollow knight/AttackR/AttackDown/%d.png",0,4,5,name_indices=range(2,7));[PLAYER_DOWNATTACK[0].HitErelative.append(Vector2(-240,70)) for _ in range(5)];[PLAYER_DOWNATTACK[1].HitErelative.append(Vector2(-200,70)) for _ in range(5)]
    PLAYER_DEATH.load_animation("assets/img/hollow knight/Death/%d.png",10,AnimationName.PLAYER_DEATH0)
    B_WALK[0].load_animation("assets/img/hollow knight/Boss/Walk/%d.png",11,AnimationName.B_WALK0);B_WALK[1].load_animation("assets/img/hollow knight/Boss/WalkR/%d.png",11,AnimationName.B_WALK0);[(B_WALK[0].frameinterval.append(2),B_WALK[0].dmove.append([-12,0]),B_WALK[1].dmove.append([12,0])) for _ in range(11)];B_WALK[0].tmp_interval=B_WALK[0].frameinterval[:];B_WALK[1].frameinterval=B_WALK[0].frameinterval[:];B_WALK[1].tmp_interval=B_WALK[0].tmp_interval[:]
    B_JUMPDASH[0].load_animation("assets/img/hollow knight/Boss/JumpDash/%d.png",29,AnimationName.B_JUMPDASH0);B_JUMPDASH[0].frameinterval=[2]*4+[1]*9+[3]*9+[20]+[1]*6;B_JUMPDASH[0].tmp_interval=B_JUMPDASH[0].frameinterval[:]
    B_JUMPDASH[1].load_animation("assets/img/hollow knight/Boss/JumpDashR/%d.png",29,AnimationName.B_JUMPDASH0);B_JUMPDASH[1].frameinterval=[2]*4+[1]*9+[2]*9+[15]+[1]*6;B_JUMPDASH[1].tmp_interval=B_JUMPDASH[1].frameinterval[:]
    B_IDLE[0].load_animation("assets/img/hollow knight/Boss/Idle/%d.png",2,AnimationName.B_IDLEL0);B_IDLE[0].canloop=True;B_IDLE[0].frameinterval=[4,4];B_IDLE[0].tmp_interval=B_IDLE[0].frameinterval[:]
    B_IDLE[1].load_animation("assets/img/hollow knight/Boss/IdleR/%d.png",2,AnimationName.B_IDLER0);B_IDLE[1].canloop=True;B_IDLE[1].frameinterval=[4,4];B_IDLE[1].tmp_interval=B_IDLE[1].frameinterval[:]
    B_LAND[0].load_animation("assets/img/hollow knight/Boss/Land/%d.png",6,AnimationName.B_LAND0,start_index=23);B_LAND[0].frameinterval=[2]*6;B_LAND[0].tmp_interval=B_LAND[0].frameinterval[:]
    B_LAND[1].load_animation("assets/img/hollow knight/Boss/LandR/%d.png",6,AnimationName.B_LAND0,start_index=23);B_LAND[1].frameinterval=[2]*6;B_LAND[1].tmp_interval=B_LAND[1].frameinterval[:]
    B_JUMP[0].load_animation("assets/img/hollow knight/Boss/Jump/%d.png",29,AnimationName.B_JUMP0);B_JUMP[0].frameinterval=[2]*13+[1]*5+[2]*11;B_JUMP[0].tmp_interval=B_JUMP[0].frameinterval[:]
    B_JUMP[1].load_animation("assets/img/hollow knight/Boss/JumpR/%d.png",29,AnimationName.B_JUMP0);B_JUMP[1].frameinterval=B_JUMP[0].frameinterval[:];B_JUMP[1].tmp_interval=B_JUMP[0].tmp_interval[:]
    B_DASH[0].load_animation("assets/img/hollow knight/Boss/Dash/%d.png",12,AnimationName.B_DASH0);B_DASH[0].load_effect("assets/img/hollow knight/Boss/Dash/%d.png",9,11,3,name_indices=range(9,12));
    B_DASH[1].load_animation("assets/img/hollow knight/Boss/DashR/%d.png",12,AnimationName.B_DASH0);B_DASH[1].load_effect("assets/img/hollow knight/Boss/DashR/%d.png",9,11,3,name_indices=range(9,12))
    B_DASH[0].Erelative=[Vector2(140,90),Vector2(140,-20),Vector2(200,-20)];B_DASH[1].Erelative=[Vector2(-120,90),Vector2(-250,-20),Vector2(-250,-20)];B_DASH[0].frameinterval=[2]*11+[20];B_DASH[0].dmove[11][0]=-35;B_DASH[1].dmove[11][0]=35;B_DASH[0].tmp_interval=B_DASH[0].frameinterval[:];B_DASH[1].frameinterval=B_DASH[0].frameinterval[:];B_DASH[1].tmp_interval=B_DASH[0].tmp_interval[:]
    B_JUMPFINAL[0].load_animation("assets/img/hollow knight/Boss/JumpFinal/%d.png",45,AnimationName.B_JUMPFINAL0);B_JUMPFINAL[0].load_effect("assets/img/hollow knight/Boss/JumpFinal/Effects/%d.png",20,38,18,name_indices=range(20,38))
    B_JUMPFINAL[1].load_animation("assets/img/hollow knight/Boss/JumpFinalR/%d.png",45,AnimationName.B_JUMPFINAL0);B_JUMPFINAL[1].load_effect("assets/img/hollow knight/Boss/JumpFinalR/Effects/%d.png",20,38,18,name_indices=range(20,38))
    B_JUMPFINAL[0].frameinterval=[2]*13+[1]*5+[2]*27;B_JUMPFINAL[0].CD=30;B_JUMPFINAL[0].Erelative=[Vector2(-80,-50)]*18;B_JUMPFINAL[1].frameinterval=B_JUMPFINAL[0].frameinterval[:];B_JUMPFINAL[1].CD=30;B_JUMPFINAL[1].Erelative=B_JUMPFINAL[0].Erelative[:];B_JUMPFINAL[0].tmp_interval=B_JUMPFINAL[0].frameinterval[:];B_JUMPFINAL[1].tmp_interval=B_JUMPFINAL[1].frameinterval[:]
    BLOOD.load_animation("assets/img/hollow knight/UI/Blood/%d.png",6,AnimationName.BLOOD0);BLOOD.frameinterval=[120,3,3,3,3,3];BLOOD.tmp_interval=BLOOD.frameinterval[:];BLOOD.canloop=True
    EMPTYBLOOD=pygame.image.load("assets/img/hollow knight/UI/Blood/empty.png").convert_alpha()
    BLOOD_DAMAGE.load_animation("assets/img/hollow knight/UI/Blood/Damage/%d.png",6,AnimationName.BLOOD_DAMAGE0);BLOOD_DAMAGE.frameinterval=[15,3,3,3,3,3];BLOOD_DAMAGE.tmp_interval=BLOOD_DAMAGE.frameinterval[:];BLOOD_DAMAGE.dmove=[[-7,-27],[-3,-27],[-4,-10],[-2,0],[-3,0],[0,0]]
    SOUL=pygame.image.load("assets/img/hollow knight/UI/Blood/00.png").convert_alpha()
    
    running = True
    while running:
        if scenemanager == 0:
            OPENGROUND=pygame.image.load("assets/UI/openground.png").convert();TITLE=pygame.image.load("assets/UI/title_chinese.png").convert_alpha();LOGO=pygame.image.load("assets/UI/Team Cherry Logo_large.png").convert_alpha();PRESS_TO_START=pygame.image.load("assets/UI/press_to_start.png").convert_alpha();ARROR[0].load_animation("assets/UI/Arror/%d.png",10,AnimationName.ARROR0);ARROR[1].load_animation("assets/UI/ArrorR/%d.png",10,AnimationName.ARROR0);pygame.mixer.music.load(sounds["Title"]);pygame.mixer.music.play(-1)
            waiting=True
            while waiting:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:waiting=False;running=False
                    if event.type==pygame.KEYDOWN:waiting=False
                screen.blit(OPENGROUND,(0,0));putimage_1(720-TITLE.get_width()/2,100,TITLE);putimage_1(1180,720,LOGO);putimage_1(720-PRESS_TO_START.get_width()/2,720,PRESS_TO_START);pygame.display.flip();clock.tick(60)
            if not running:break
            pygame.mixer.music.stop();sounds["Confirm"].play()
            for i in range(10):screen.blit(OPENGROUND,(0,0));putimage_1(720-TITLE.get_width()/2,100,TITLE);putimage_1(1180,720,LOGO);putimage_1(720-PRESS_TO_START.get_width()/2,720,PRESS_TO_START);putimage_1(720-PRESS_TO_START.get_width()/2-ARROR[0].frame_list[0].get_width(),705,ARROR[0].frame_list[i]);putimage_1(720+PRESS_TO_START.get_width()/2,705,ARROR[1].frame_list[i]);pygame.display.flip();pygame.time.delay(33)
            pygame.time.delay(300);scenemanager=1
        elif scenemanager == 1:
            Player.HP=7;testenemy.HP=50;Player.position=Point(200,680);testenemy.position=Point(1000,585);Player.UnHurtableTime=0;testenemy.UnHurtableTime=0;testenemy.gravity=0;MusicCD=90;PublicCD=20
            CDs={'B_WALK':0,'B_JUMPDASH':0,'B_JUMP':0,'B_DASH':0,'B_JUMPFINAL':0,'PLAYER_DASH':0,'PLAYER_ATTACK':0,'PLAYER_UPATTACK':0,'PLAYER_ATTACKTWICE':0,'PLAYER_DOWNATTACK':0,'PLAYER_DAMAGE':0}
            CurrentPlayerAnimation=nullanimation.copy();CurrentPlayerLoopAnimation=PLAYER_IDLE[1].copy();CurrentEnemyAnimation=B_IDLE[0].copy();pygame.mixer.music.load(sounds["bgm"]);pygame.mixer.music.play(-1);sounds["open"].play()
            game_running=True
            while game_running:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:game_running=False;running=False
                if not Player.HP or not testenemy.HP:game_running=False;break
                for key in CDs:CDs[key]=max(0,CDs[key]-1)
                Player.UnHurtableTime=max(0,Player.UnHurtableTime-1);testenemy.UnHurtableTime=max(0,testenemy.UnHurtableTime-1);PublicCD=max(0,PublicCD-1);MusicCD=max(0,MusicCD-1)
                operation=Player.messagedealer()
                if not(CurrentPlayerAnimation.animationname==AnimationName.PLAYER_DAMAGE0 and CurrentPlayerAnimation.current_frameidx<=3):
                    isok=CurrentPlayerAnimation.animationname==AnimationName.NU
                    if operation==6 and isok: Player.speed.vy=-43;CurrentPlayerAnimation=PLAYER_JUMPSTART[Player.Facing_Right].copy()
                    elif operation==2 and isok and CDs['PLAYER_ATTACK']==0: CurrentPlayerAnimation=PLAYER_ATTACK[Player.Facing_Right].copy();CDs['PLAYER_ATTACK']=30;CDs['PLAYER_ATTACKTWICE']=45
                    elif operation==2 and not isok and CurrentPlayerAnimation.animationname==AnimationName.PLAYER_ATTACK0 and 0<CDs['PLAYER_ATTACKTWICE']<=30: CurrentPlayerAnimation=PLAYER_ATTACKTWICE[Player.Facing_Right].copy();CDs['PLAYER_ATTACKTWICE']=0
                    elif operation==4 and isok and CDs['PLAYER_DASH']==0: CurrentPlayerAnimation=PLAYER_DASH[Player.Facing_Right].copy();CDs['PLAYER_DASH']=30
                    elif operation==5 and isok and CDs['PLAYER_UPATTACK']==0: CurrentPlayerAnimation=PLAYER_UPATTACK[Player.Facing_Right].copy();CDs['PLAYER_UPATTACK']=20
                    elif operation==7 and isok and CDs['PLAYER_DOWNATTACK']==0: CurrentPlayerAnimation=PLAYER_DOWNATTACK[Player.Facing_Right].copy();CDs['PLAYER_DOWNATTACK']=20
                    elif operation==1 and isok:
                        if CurrentPlayerLoopAnimation.animationname not in [AnimationName.PLAYER_WALKL0,AnimationName.PLAYER_WALKR0] or (CurrentPlayerLoopAnimation.animationname==AnimationName.PLAYER_WALKR0 and not Player.Facing_Right) or (CurrentPlayerLoopAnimation.animationname==AnimationName.PLAYER_WALKL0 and Player.Facing_Right):CurrentPlayerLoopAnimation=PLAYER_WALK[Player.Facing_Right].copy()
                    elif operation==0 and isok:
                        if CurrentPlayerLoopAnimation.animationname!=AnimationName.PLAYER_IDLE0:CurrentPlayerLoopAnimation=PLAYER_IDLE[Player.Facing_Right].copy()
                    if isok and Player.speed.vy>0:CurrentPlayerLoopAnimation=PLAYER_JUMPLOOP[Player.Facing_Right].copy()
                    if Player.speed.vy==0 and not isok and CurrentPlayerAnimation.animationname!=AnimationName.PLAYER_DASH0:Player.speed.vx=0
                    if CurrentPlayerAnimation.animationname==AnimationName.PLAYER_DASH0:Player.speed.vx=0
                if PublicCD==0 and CurrentEnemyAnimation.animationname in [AnimationName.NU,AnimationName.B_IDLEL0,AnimationName.B_IDLER0]:
                    choices=[k for k,v in {'walk_close':abs(get_direction(testenemy.position,Player.position).vx)<150 and CDs['B_WALK']==0,'walk_far':abs(get_direction(testenemy.position,Player.position).vx)>500 and CDs['B_WALK']==0,'jump':CDs['B_JUMP']==0,'jumpdash':CDs['B_JUMPDASH']==0,'dash':CDs['B_DASH']==0,'jumpfinal':CDs['B_JUMPFINAL']==0}.items() if v]
                    if choices:
                        action=random.choice(choices);testenemy.Facing_Right=get_direction(testenemy.position,Player.position).vx>0
                        if action=='walk_close':CurrentEnemyAnimation=B_WALK[not testenemy.Facing_Right].copy();CDs['B_WALK']=75;PublicCD=30
                        elif action=='walk_far':CurrentEnemyAnimation=B_WALK[testenemy.Facing_Right].copy();CDs['B_WALK']=75;PublicCD=30
                        elif action=='jump':testenemy.gravity=3;testenemy.speed.vy=-60;normal_shootdirection=get_normal_direction(testenemy.position,Player.position);B_JUMP[testenemy.Facing_Right].dmove=[[0,0]]*3+[[10*normal_shootdirection.vx,0]]*26;CurrentEnemyAnimation=B_JUMP[testenemy.Facing_Right].copy();CDs['B_JUMP']=60;PublicCD=50
                        elif action=='jumpdash':testenemy.gravity=0;testenemy.speed.vy=0;shootdirection=get_direction(testenemy.position,Player.position);normal_shootdirection=get_normal_direction(testenemy.position,Player.position);B_JUMPDASH[testenemy.Facing_Right].dmove=[[0,0]]*3+[[10*normal_shootdirection.vx,-75]]*5+[[0,0]]*14+[[shootdirection.vx/22,30]]*1+[[0,0]]*6;CurrentEnemyAnimation=B_JUMPDASH[testenemy.Facing_Right].copy();CDs['B_JUMPDASH']=120;PublicCD=50
                        elif action=='dash':CurrentEnemyAnimation=B_DASH[testenemy.Facing_Right].copy();CDs['B_DASH']=50;PublicCD=50
                        elif action=='jumpfinal':testenemy.gravity=4;testenemy.speed.vy=-60;normal_shootdirection=get_normal_direction(testenemy.position,Player.position);B_JUMPFINAL[testenemy.Facing_Right].dmove=[[0,0]]*3+[[25*normal_shootdirection.vx,0]]*12+[[0,0]]*30;CurrentEnemyAnimation=B_JUMPFINAL[testenemy.Facing_Right].copy();CDs['B_JUMPFINAL']=240;PublicCD=120
                elif CurrentEnemyAnimation.animationname==AnimationName.NU:CurrentEnemyAnimation=B_IDLE[get_direction(testenemy.position,Player.position).vx>0].copy()
                if CurrentPlayerAnimation.animationname!=AnimationName.NU:CurrentPlayerLoopAnimation=nullanimation.copy()
                if attack_judger(Player,testenemy):testenemy.UnHurtableTime=12;Player.position.x+=-(2*Player.Facing_Right-1)*60;testenemy.HP-=1;CurrentPlayerAnimation.PlayHitAnimation=True;sounds["attackhit"].play()
                if CurrentPlayerAnimation.animationname==AnimationName.PLAYER_DOWNATTACK0:Player.speed.vy=-40
                if attacked_judger(Player,testenemy):Player.UnHurtableTime=45;CurrentPlayerAnimation=PLAYER_DAMAGE[get_direction(testenemy.position,Player.position).vx<0].copy();Player.speed.vy=-25;Player.HP-=1
                Player.position.x+=Player.speed.vx
                if CurrentEnemyAnimation.animationname not in [AnimationName.B_WALK0,AnimationName.B_DASH0,AnimationName.B_JUMPDASH0,AnimationName.B_JUMP0,AnimationName.B_JUMPFINAL0]:testenemy.position.x+=testenemy.speed.vx
                gravity_collide(Player,testenemy);MusicCD=music_player(sounds,MusicCD)
                Player.position.x=max(140,min(Player.position.x,1320-(CurrentPlayerAnimation.maxwidth if CurrentPlayerAnimation.animationname!=AnimationName.NU else CurrentPlayerLoopAnimation.maxwidth)))
                testenemy.position.x=max(90,min(testenemy.position.x,1360-(CurrentEnemyAnimation.maxwidth if CurrentEnemyAnimation.animationname!=AnimationName.NU else B_IDLE[0].maxwidth)))
                screen.blit(Background,(0,0));putimage_1(210,140,COIN);putimage_1(270,145,MONEY);draw_actor_anim(testenemy,CurrentEnemyAnimation);putimage_1(53,40,SOUL)
                for i in range(7):putimage_1(200+65*i,70,EMPTYBLOOD)
                for i in range(int(Player.HP)):putimage_1(200+65*i,70,BLOOD.frame_list[BLOOD.current_frameidx])
                BLOOD.tmp_interval[BLOOD.current_frameidx]-=1
                if BLOOD.tmp_interval[BLOOD.current_frameidx]<=0:BLOOD.current_frameidx=(BLOOD.current_frameidx+1)%BLOOD.frame_num;BLOOD.tmp_interval=BLOOD.frameinterval[:]
                if BLOOD_DAMAGE.current_frameidx>0 or (BLOOD_DAMAGE.current_frameidx==0 and BLOOD_DAMAGE.tmp_interval[0]<15) or (CurrentPlayerAnimation.animationname==AnimationName.PLAYER_DAMAGE0 and CurrentPlayerAnimation.current_frameidx==0):draw_ui_anim(BLOOD_DAMAGE,200+65*int(Player.HP),70)
                if CurrentPlayerAnimation.animationname!=AnimationName.NU:draw_actor_anim(Player,CurrentPlayerAnimation)
                else:draw_actor_anim(Player,CurrentPlayerLoopAnimation)
                pygame.display.flip();clock.tick(45)
            pygame.mixer.music.stop()
            if Player.HP<=0:
                sounds["playerdamage"].play()
                for i in range(10):screen.blit(Background,(0,0));putimage_1(testenemy.position.x,testenemy.position.y,B_IDLE[testenemy.Facing_Right].frame_list[0]);[putimage_1(200+65*j,70,EMPTYBLOOD) for j in range(7)];putimage_1(Player.position.x,Player.position.y,PLAYER_DEATH.frame_list[i]);pygame.display.flip();pygame.time.delay(1000//15)
                pygame.time.delay(200);scenemanager=2
            elif testenemy.HP<=0:
                sounds["hea"].play();CurrentEnemyAnimation=B_IDLE[testenemy.Facing_Right].copy()
                for _ in range(15):gravity_collide(Player,testenemy);screen.blit(Background,(0,0));draw_actor_anim(testenemy,CurrentEnemyAnimation);putimage_1(Player.position.x,Player.position.y,PLAYER_IDLE[Player.Facing_Right].frame_list[0]);pygame.display.flip();pygame.time.delay(1000//30)
                pygame.time.delay(400);scenemanager=2
        elif scenemanager==2:
            screen.fill((0,0,0));putimage_1(SCREEN_WIDTH/2-PLAYAGAIN.get_width()/2,SCREEN_HEIGHT/2-PLAYAGAIN.get_height()/2,PLAYAGAIN);pygame.display.flip()
            waiting=True
            while waiting:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:waiting=False;running=False
                    if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                        mx,my=event.pos
                        if 560<mx<660 and 420<my<500:sounds["Confirm"].play();pygame.time.delay(200);scenemanager=1;waiting=False
                        elif 780<mx<880 and 420<my<500:scenemanager=3;waiting=False
        elif scenemanager==3:running=False
    pygame.quit();sys.exit()

if __name__ == '__main__':
    main()