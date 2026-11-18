from vpython import *
# 두근두근 물리 1편 관성 — 실습 「컬링 스톤, 방해를 0까지 줄여 보기」 (숫자는 모두 설명용이에요)

# ===== 1. 바꿔 볼 숫자: 고친 뒤 다시 실행해 보세요 =====
출발_빠르기 = 4        # 손 떼는 선을 지날 때 스톤의 빠르기 (m/s)
줄어드는_빠르기 = 1    # 1초 동안 줄어드는 빠르기 (m/s): 4, 2, 0.5, 0으로 바꿔 보세요
시간간격 = 1 / 600     # 한 걸음에 걸리는 시간 (초): 1초를 600걸음으로 잘게 나눠요

# ===== 2. 법칙: 한 걸음마다 빠르기와 위치를 조금씩 고쳐요 =====
def 한_걸음(빠르기, 위치):
    빠르기 = 빠르기 - 줄어드는_빠르기 * 시간간격   # 방해가 있는 만큼만 빠르기가 줄어들어요
    if 빠르기 < 0:
        빠르기 = 0                                 # 방해는 멈추게 할 뿐, 뒤로 밀지는 않아요
    위치 = 위치 + 빠르기 * 시간간격                # 지금 빠르기로 한 걸음만큼 가요
    return 빠르기, 위치
# 줄어드는_빠르기가 0이면 빠르기를 바꾸는 것이 없으니 빠르기는 그대로예요.

# ===== 3. 아래는 경기장을 그리고 버튼을 만드는 코드예요 (읽지 않아도 돼요) =====
과녁_자리 = 21.5       # 손 떼는 선에서 과녁 한가운데까지 (m)
경기장_끝 = 44         # 손 떼는 선에서 경기장 끝까지 (m)
얼음색 = vector(0.93, 0.97, 1)

scene.background = vector(0.88, 0.93, 0.98)
scene.forward = vector(0, -0.6, -1)
scene.center = vector(8, 0, 0)
scene.range = 7
scene.ambient = color.gray(0.55)
distant_light(direction=vector(0.3, -1, -0.5), color=color.gray(0.4))
for x in range(0, 경기장_끝 + 1, 8):                 # 경기장 천장 조명 (8 m마다)
    local_light(pos=vector(x, 5, 0), color=vector(1, 0.96, 0.88), intensity=0.85)

# 경기장: 바닥, 양옆 벽, 가운데 선, 손 떼는 선, 과녁
바닥 = box(pos=vector(경기장_끝 / 2 - 1.5, -0.1, 0), size=vector(경기장_끝 + 3, 0.2, 4.4), texture=textures.ice, color=얼음색)
for z in (-2.3, 2.3):
    box(pos=vector(경기장_끝 / 2 - 1.5, 0.05, z), size=vector(경기장_끝 + 3, 0.3, 0.2), color=vector(0.97, 0.98, 1))
box(pos=vector(경기장_끝 / 2 - 1.5, 0.001, 0), size=vector(경기장_끝 + 3, 0.002, 0.03), color=vector(0.2, 0.2, 0.25))
box(pos=vector(0, 0.006, 0), size=vector(0.12, 0.012, 4.4), color=color.red)
label(pos=vector(0, -1.0, 2.6), text='손 떼는 선', color=color.red, height=14)
for 차례, 반지름, 색 in ((0, 1.83, vector(0.2, 0.45, 0.9)), (1, 1.22, color.white), (2, 0.61, vector(0.9, 0.2, 0.25)), (3, 0.15, color.white)):
    cylinder(pos=vector(과녁_자리, 0.002 + 0.003 * 차례, 0), axis=vector(0, 0.003, 0), radius=반지름, color=색)
box(pos=vector(과녁_자리, 0.015, 0), size=vector(0.03, 0.004, 4.4), color=vector(0.2, 0.2, 0.25))
label(pos=vector(과녁_자리, 1.0, -2.2), text=f'과녁 ({과녁_자리} m)', color=vector(0.2, 0.3, 0.7), height=13)
for m in range(0, 경기장_끝 + 1, 2):
    box(pos=vector(m, 0.01, 2.05), size=vector(0.04, 0.02, 0.25), color=color.black)
    if m <= 16 or m % 8 == 0:
        label(pos=vector(m, -0.4, 2.6), text=f'{m} m', color=color.black, height=11)

# 스톤: 화강암 몸통 + 빨간 손잡이 (잘 보이게 실제보다 크게 그렸어요)
몸통 = cylinder(pos=vector(0, 0.02, 0), axis=vector(0, 0.28, 0), radius=0.5, texture=textures.granite, color=vector(0.85, 0.85, 0.88))
띠 = cylinder(pos=vector(0, 0.13, 0), axis=vector(0, 0.05, 0), radius=0.505, color=vector(0.35, 0.35, 0.4))
뚜껑 = cylinder(pos=vector(0, 0.3, 0), axis=vector(0, 0.03, 0), radius=0.42, color=vector(0.55, 0.55, 0.6))
기둥 = box(pos=vector(0, 0.38, 0), size=vector(0.1, 0.14, 0.1), color=color.red)
손잡이 = box(pos=vector(0, 0.46, 0), size=vector(0.7, 0.08, 0.13), color=color.red)
스톤 = compound([몸통, 띠, 뚜껑, 기둥, 손잡이])
스톤_높이 = 스톤.pos.y
attach_light(스톤, offset=vector(0, 2, 0.8), color=vector(1, 0.95, 0.85), intensity=1.2)   # 스톤을 따라다니는 조명
빠르기_글자 = label(pos=vector(0, 1.3, 0), text=f'{출발_빠르기:.1f} m/s', color=color.black, height=16)
바닥_글자 = label(pos=vector(8, 3.2, -2), text='', color=vector(0.2, 0.2, 0.3), height=14)
알림 = label(pos=vector(8, -1.5, 2.4), text='[스톤 밀기]를 누르세요', color=color.blue, height=15)

def 바닥_바꾸기(값):                               # 숫자에 맞는 바닥으로 바꿔요(카펫 · 나무 마루 · 얼음)
    if 값 == 4:
        이름 = '카펫'
    elif 값 == 2:
        이름 = '나무 마루'
    elif 값 == 1:
        이름 = '얼음'
    elif 값 == 0.5:
        이름 = '비질로 닦은 얼음'
    elif 값 == 0:
        이름 = '방해 없음 (생각 실험)'
    else:
        이름 = '직접 정한 바닥'
    if 값 > 3:
        바닥.texture, 바닥.color = textures.rough, vector(0.75, 0.25, 0.32)
    elif 값 > 1.5:
        바닥.texture, 바닥.color = textures.wood, color.white
    else:
        바닥.texture, 바닥.color = textures.ice, 얼음색
    바닥.shininess = 1 if 값 <= 0.5 else 0.6       # 닦을수록 반짝여요
    바닥_글자.text = f'바닥: {이름} — 1초에 {값} m/s씩 줄어요'

바닥_바꾸기(줄어드는_빠르기)
달리는_중 = False
빠르기 = 출발_빠르기
위치 = 0
걸음 = 0
지난_자리 = 0
이번_점 = []                                       # 이번에 찍은 점
지난_점 = []                                       # 지난번에 찍은 점 (연하게 남겨 간격을 비교해요)

def 스톤_밀기(b):
    global 달리는_중, 빠르기, 위치, 걸음, 지난_자리
    for 점 in 이번_점:
        점.opacity = 0.25
    지난_점.extend(이번_점)
    이번_점.clear()
    달리는_중, 빠르기, 위치, 걸음, 지난_자리 = True, 출발_빠르기, 0, 0, 0
    스톤.pos, 빠르기_글자.pos = vector(0, 스톤_높이, 0), vector(0, 1.3, 0)
    빠르기_글자.text = f'{출발_빠르기:.1f} m/s'
    scene.center = vector(8, 0, 0)
    알림.text = '출발!'
def 지우기(b):
    for 점 in 지난_점 + 이번_점:
        점.visible = False
    지난_점.clear()
    이번_점.clear()
def 슬라이더(s):                                   # 슬라이더는 코드의 숫자를 대신 바꿔 주는 보조 도구예요
    global 줄어드는_빠르기
    줄어드는_빠르기 = s.value
    값_글자.text = f'{s.value} m/s'
    바닥_바꾸기(s.value)

button(text='스톤 밀기', bind=스톤_밀기)
button(text='점 지우기', bind=지우기)
scene.caption = '1초 동안 줄어드는 빠르기: '
값_글자 = wtext(text=f'{줄어드는_빠르기} m/s')
slider(min=0, max=4, step=0.25, value=줄어드는_빠르기, length=240, bind=슬라이더)

초당_걸음 = round(1 / 시간간격)                   # 1초에 몇 걸음인지 나타내요 (지금은 600)
while True:
    rate(60)                                       # 화면은 1초에 60번 다시 그려요
    for i in range(max(1, 초당_걸음 // 60)):       # 화면을 다시 그리는 사이에 1/60초 동안의 걸음을 계산해요
        if not 달리는_중:
            break
        빠르기, 위치 = 한_걸음(빠르기, 위치)
        걸음 = 걸음 + 1
        if 걸음 % 초당_걸음 == 0:                  # 1초마다 점 하나, 소리 한 번
            이번_점.append(sphere(pos=vector(위치, 0.08, 0), radius=0.12, color=color.blue))
            play_sound(660, 0.08, 'sine', 0.2)
        if 빠르기 == 0:
            달리는_중 = False
            if 위치 <= 과녁_자리:
                알림.text = f'멈춘 거리: {위치:.1f} m (과녁 한가운데까지 {과녁_자리 - 위치:.1f} m)'
            else:
                알림.text = f'멈춘 거리: {위치:.1f} m (과녁 한가운데를 {위치 - 과녁_자리:.1f} m 지났어요)'
        elif 위치 > 경기장_끝:
            달리는_중 = False
            알림.text = f'경기장 끝을 지났어요. 아직 멈추지 않았어요 (빠르기 {빠르기:.1f} m/s)'
    if 위치 != 지난_자리:                           # 이번에 움직였을 때만 화면을 고쳐요
        스톤.pos = vector(위치, 스톤_높이, 0)
        스톤.rotate(angle=-(위치 - 지난_자리) * 0.3, axis=vector(0, 1, 0))   # 컬링 스톤은 천천히 돌며 미끄러져요
        지난_자리 = 위치
        빠르기_글자.pos = vector(위치, 1.3, 0)
        빠르기_글자.text = f'{빠르기:.1f} m/s'
        if 위치 > scene.center.x + 6:              # 스톤이 화면 오른쪽 끝에 가까워지면 화면이 따라가요
            scene.center = vector(위치 - 6, 0, 0)
    알림.pos = scene.center + vector(0, -1.5, 2.4)
    바닥_글자.pos = scene.center + vector(0, 3.2, -2)
