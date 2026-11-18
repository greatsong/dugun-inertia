from vpython import *
# 두근두근 물리 1편 관성 — 실습 「방해를 0까지 내려 보기」 (숫자는 모두 설명용이에요)

# ===== 1. 바꿔 볼 숫자: 고친 뒤 다시 실행해 보세요 =====
출발_빠르기 = 4        # 손 떼는 선을 지날 때의 빠르기 (m/s)
줄어드는_빠르기 = 4    # 1초 동안 줄어드는 빠르기 (m/s): 2, 1, 0.5, 0으로 바꿔 보세요
시간간격 = 1 / 600     # 한 걸음에 걸리는 시간 (초): 1초를 600걸음으로 잘게 나눠요

# ===== 2. 법칙: 한 걸음마다 빠르기와 위치를 조금씩 고쳐요 =====
def 한_걸음(빠르기, 위치):
    빠르기 = 빠르기 - 줄어드는_빠르기 * 시간간격   # 방해가 있는 만큼만 빠르기가 줄어들어요
    if 빠르기 < 0:
        빠르기 = 0                                 # 방해는 멈추게 할 뿐, 뒤로 밀지는 않아요
    위치 = 위치 + 빠르기 * 시간간격                # 지금 빠르기로 한 걸음만큼 가요
    return 빠르기, 위치
# 줄어드는_빠르기가 0이면 빠르기를 바꾸는 것이 없으니 빠르기는 그대로예요.

# ===== 3. 아래는 화면을 그리고 버튼을 만드는 코드예요 (읽지 않아도 돼요) =====
scene.background = vector(0.95, 0.95, 0.98)
scene.forward = vector(0, -0.35, -1)
scene.center = vector(8, 0, 0)
scene.range = 7
box(pos=vector(31, -0.1, 0), size=vector(66, 0.2, 1.6), color=vector(0.75, 0.7, 0.62))
box(pos=vector(0, 0.3, 0), size=vector(0.05, 0.6, 1.6), color=color.red)
label(pos=vector(0, 1.0, 0), text='손 떼는 선', color=color.red, height=14)
for m in range(0, 63, 2):
    box(pos=vector(m, 0.01, 0.75), size=vector(0.04, 0.02, 0.2), color=color.black)
    if m <= 16 or m % 8 == 0:
        label(pos=vector(m, -0.7, 0.8), text=f'{m} m', color=color.black, height=11)
원반 = cylinder(pos=vector(0, 0, 0), axis=vector(0, 0.15, 0), radius=0.4, color=color.orange)
빠르기_글자 = label(pos=vector(0, 1.6, 0), text=f'{출발_빠르기:.1f} m/s', color=color.black, height=16)
알림 = label(pos=vector(8, -2.2, 0), text='[내보내기]를 누르세요', color=color.blue, height=15)
상태 = {'달림': False, '이번점': [], '지난점': []}

def 내보내기(b):
    for 점 in 상태['이번점']:
        점.opacity = 0.25                          # 지난번 점은 연하게 남겨 점 간격을 비교해요
    상태['지난점'] += 상태['이번점']
    상태.update(이번점=[], 달림=True, 빠르기=출발_빠르기, 위치=0, 걸음=0)
    scene.center, 알림.pos = vector(8, 0, 0), vector(8, -2.2, 0)
    알림.text = f'1초 동안 줄어드는 빠르기 {줄어드는_빠르기} m/s'
def 지우기(b):
    for 점 in 상태['지난점'] + 상태['이번점']:
        점.visible = False
    상태.update(지난점=[], 이번점=[])
def 슬라이더(s):                                   # 슬라이더는 코드의 숫자를 대신 바꿔 주는 보조 도구예요
    global 줄어드는_빠르기
    줄어드는_빠르기 = s.value
    값_글자.text = f'{s.value} m/s'

button(text='내보내기', bind=내보내기)
button(text='점 지우기', bind=지우기)
scene.caption = '1초 동안 줄어드는 빠르기: '
값_글자 = wtext(text=f'{줄어드는_빠르기} m/s')
slider(min=0, max=4, step=0.25, value=줄어드는_빠르기, length=240, bind=슬라이더)

초당_걸음 = round(1 / 시간간격)                   # 1초에 몇 걸음인지 나타내요 (지금은 600)
while True:
    rate(60)                                       # 화면은 1초에 60번 다시 그려요
    for i in range(max(1, 초당_걸음 // 60)):       # 화면을 다시 그리는 사이에 1/60초 동안의 걸음을 계산해요
        if not 상태['달림']:
            break
        상태['빠르기'], 상태['위치'] = 한_걸음(상태['빠르기'], 상태['위치'])
        상태['걸음'] += 1
        x = 상태['위치']
        if 상태['걸음'] % 초당_걸음 == 0:            # 1초마다 점 하나, 소리 한 번
            상태['이번점'].append(sphere(pos=vector(x, 0.1, 0), radius=0.13, color=color.blue))
            play_sound(660, 0.08, 'sine', 0.2)
        if 상태['빠르기'] == 0:
            상태['달림'] = False
            알림.text = f'멈춘 거리: {x:.1f} m'
        elif x > 62 or x < -5:
            상태['달림'] = False
            알림.text = '길 끝을 지났어요. 아직 멈추지 않았어요'
    if 상태.get('걸음'):
        x = 상태['위치']
        원반.pos, 빠르기_글자.pos = vector(x, 0, 0), vector(x, 1.6, 0)
        빠르기_글자.text = f"{상태['빠르기']:.1f} m/s"
        if x > scene.center.x + 7:                 # 원반이 화면 오른쪽 끝에 가까워지면 화면이 따라가요
            scene.center, 알림.pos = vector(x - 7, 0, 0), vector(x - 7, -2.2, 0)
