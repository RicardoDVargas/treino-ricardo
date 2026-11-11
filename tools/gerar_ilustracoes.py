"""Gera app/images/*.svg (29 ilustrações, painéis início → fim).
Uso:  python tools/gerar_ilustracoes.py
Cada exercício é uma função ex_<id>(s) com s=0 (início) ou s=1 (fim/movimento)."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from rig import *

CX = 120
def stance(hip, spread=13):
    return dict(to=(hip[0]-spread*.5, 186)), dict(to=(hip[0]+spread, 186))
def seat_front(e, hip_y, back_top):
    e.pad(CX-30, hip_y+4, 60, 9, 4)
    e.pad(CX-22, back_top, 44, hip_y+8-back_top, 6)

def ex_press(s):
    e = Eq(); e.pad(56, 152, 136, 9); e.line((82, 161), (82, 190)); e.line((172, 161), (172, 190))
    e.line((64, 84), (64, 152), 2); e.line((56, 84), (72, 84), 3)
    g = side(shoulder=(104, 140), torso=180, leg=dict(th=10, sh=95),
             arm=dict(ua=20, fa=-90) if s == 0 else dict(ua=-85, fa=-90))
    g.hl('hip', 'sh', .08, .5, 7.5, off=5); e.plate(g.J['wr'], 15)
    return e, g

def ex_incline(s):
    e = Eq(); sh_ = (107.5, 115.5)
    e.thick((128, 176), (82, 128), 9); e.thick((118, 162), (172, 162), 8); e.line((150, 168), (150, 190)); e.line((104, 168), (104, 190))
    g = side(shoulder=sh_, torso=-135, leg=dict(th=-5, sh=88),
             arm=dict(ua=25, fa=-80) if s == 0 else dict(ua=-50, fa=-45))
    g.hl('hip', 'sh', .45, .95, 7, off=5); e.db(g.J['wr'], 9)
    return e, g

def ex_fly(s):
    e = Eq(); e.pad(56, 152, 136, 9); e.line((82, 161), (82, 190)); e.line((172, 161), (172, 190))
    g = side(shoulder=(104, 140), torso=180, leg=dict(th=10, sh=95),
             arm=dict(ua=-90, fa=-90) if s == 0 else dict(ua=62, fa=-100))
    g.hl('hip', 'sh', .08, .5, 6.5, off=5); e.db(g.J['wr'], 8)
    return e, g

def ex_peck(s):
    hip_y = 138; e = Eq(); g = front(CX, hip_y, leg=dict(th=90, sh=90, sc=.3),
        arm=dict(ua=-10, fa=-80) if s == 0 else dict(ua=38, fa=-80, sc=.62))
    seat_front(e, hip_y, g.J['sh'][1]-6)
    for k in ('wrR', 'wrL'):
        w = g.J[k]; e.thick((w[0], w[1]-13), (w[0], w[1]+9), 6, layer='front')
    for sgn in (1, -1):
        e.line((CX+sgn*58, g.J['sh'][1]-26), (CX+sgn*58, g.J['sh'][1]+30), 1.6, op=.5)
    g.hl_dot((CX+8, g.J['sh'][1]+12), 8); g.hl_dot((CX-8, g.J['sh'][1]+12), 8)
    return e, g

def ex_scott(s):
    e = Eq(); hip = (96, 146)
    g = side(hip=hip, torso=-82, leg=dict(th=-3, sh=92),
             arm=dict(ua=52, fa=56) if s == 0 else dict(ua=52, fa=-122))
    sh_ = g.J['sh']
    e.pad(66, 156, 70, 8); e.line((100, 164), (100, 190)); e.line((70, 164), (70, 190))
    p0 = (sh_[0]+8, sh_[1]-2); p1 = (sh_[0]+52, sh_[1]+50)
    e.thick(p0, p1, 9); e.line((p1[0], p1[1]), (p1[0]-4, 190), 2.2)
    g.hl('sh', 'el', .25, .95, 5, off=-3)
    e.db(g.J['wr'], 7)
    return e, g

def ex_curl(s):
    e = Eq(); hip_y = 110
    g = front(CX, hip_y, leg=dict(th=86, sh=94),
              arm=dict(ua=82, fa=90) if s == 0 else dict(ua=82, fa=-100))
    for k in ('wrR', 'wrL'): e.dumbbell_h(g.J[k], 0, 15, 5.5)
    g.hl('sR', 'elR', .2, .95, 5.2, off=0); g.hl('sL', 'elL', .2, .95, 5.2, off=0)
    return e, g

def ex_lateral(s):
    e = Eq(); hip_y = 110
    g = front(CX, hip_y, leg=dict(th=86, sh=94),
              arm=dict(ua=98, fa=105) if s == 0 else dict(ua=-4, fa=-2), arm2=dict(ua=95, fa=92))
    e.stack(206, 36, 186); e.line((214, 30), (214, 36), 2); p = (213, 174); e.pulley(p)
    e.cable(p, g.J['wrR'])
    g.hl_dot(g.J['sR'], 9); e.line((g.J['wrR'][0]-2, g.J['wrR'][1]-6), (g.J['wrR'][0]-2, g.J['wrR'][1]+6), 4, '#d8d0f7', layer='front')
    return e, g

def ex_reverse(s):
    hip_y = 138; e = Eq()
    g = front(CX, hip_y, leg=dict(th=90, sh=90, sc=.3),
              arm=dict(to=(CX+6, g_sy(hip_y)+26), side=-1) if s == 0 else dict(ua=-6, fa=-4))
    seat_front(e, hip_y, g.J['sh'][1]+2)
    for k in ('wrR', 'wrL'):
        w = g.J[k]; e.thick((w[0], w[1]-9), (w[0], w[1]+9), 6, layer='front')
        e.line((CX, g.J['sh'][1]-28), (w[0], w[1]), 1.6, op=.45)
    g.hl_dot((g.J['sR'][0]+3, g.J['sR'][1]-2), 8); g.hl_dot((g.J['sL'][0]-3, g.J['sL'][1]-2), 8)
    return e, g
def g_sy(hip_y): return hip_y - TORSO

def ex_shoulder(s):
    hip_y = 138; e = Eq(); g = front(CX, hip_y, leg=dict(th=90, sh=90, sc=.3),
        arm=dict(ua=-6, fa=-88) if s == 0 else dict(ua=-68, fa=-100))
    seat_front(e, hip_y, g.J['sh'][1]-6)
    for k in ('wrR', 'wrL'): e.dumbbell_h(g.J[k], 0, 20, 6.5)
    g.hl_dot(g.J['sR'], 9); g.hl_dot(g.J['sL'], 9)
    return e, g

def ex_pull(s):
    hip_y = 138; e = Eq(); g = front(CX, hip_y, leg=dict(th=90, sh=90, sc=.3),
        arm=dict(ua=-65, fa=-80) if s == 0 else dict(ua=62, fa=-85))
    seat_front(e, hip_y, g.J['sh'][1]+2)
    wl, wr = g.J['wrL'], g.J['wrR']; e.line((wl[0]-8, wl[1]-1), (wr[0]+8, wr[1]-1), 3.4, '#d8d0f7', layer='front')
    e.pulley((CX, 16)); e.cable((CX, 16), (CX, wl[1]-1)); e.line((CX-26, 16), (CX+26, 16), 1.6, op=.4)
    for sgn in (1, -1):
        sy = g.J['sh'][1]; g.hl_dot((CX+sgn*14, sy+16), 8)
    return e, g

def ex_row(s):
    e = Eq(); hip = (92, 146)
    g = side(hip=hip, torso=-76 if s == 0 else -97, leg=dict(to=(158, 176)),
             arm=dict(ua=10, fa=10) if s == 0 else dict(ua=108, fa=-3), ft=-70)
    e.pad(60, 156, 64, 8); e.line((100, 164), (100, 190)); e.thick((170, 190), (170, 138), 6)
    e.stack(214, 92, 186); p = (206, 168); e.pulley(p)
    w = g.J['wr']; e.cable(p, (w[0]+4, w[1]))
    e.line((w[0]+2, w[1]-8), (w[0]+2, w[1]+8), 4, '#d8d0f7', layer='front')
    g.hl('hip', 'sh', .25, .9, 6.5, off=-6)
    return e, g

def ex_pulldown(s):
    e = Eq(); g = side(hip=(116, 112), torso=-80, leg=dict(to=(126, 186)),
        arm=dict(ua=-48, fa=-48) if s == 0 else dict(ua=82, fa=82))
    e.stack(206, 44, 186); e.line((214, 20), (214, 44), 2); p = (190, 22); e.pulley(p); e.line(p, (214, 22), 2)
    w = g.J['wr']; e.cable(p, w); e.line((w[0]-2, w[1]-7), (w[0]-2, w[1]+7), 4, '#d8d0f7', layer='front')
    g.hl('hip', 'sh', .3, .9, 6.5, off=-6)
    return e, g

def ex_triceps(s):
    e = Eq(); g = side(hip=(110, 110), torso=-83, leg=dict(to=(118, 186)),
        arm=dict(ua=94, fa=-14) if s == 0 else dict(ua=94, fa=76))
    e.stack(206, 44, 186); p = (188, 22); e.pulley(p); e.line(p, (214, 22), 2)
    w = g.J['wr']; e.cable(p, (w[0]+3, w[1]-3))
    e.line((w[0]-3, w[1]-4), (w[0]+9, w[1]-4), 4, '#d8d0f7', layer='front')
    g.hl('sh', 'el', .12, .9, 4.8, off=3)
    return e, g

def ex_french(s):
    e = Eq(); g = side(hip=(130, 110), torso=-90, leg=dict(to=(138, 186)),
        arm=dict(ua=-82, fa=118) if s == 0 else dict(ua=-82, fa=-78))
    e.stack(8, 44, 186); p = (34, 176); e.pulley(p); e.line((16, 38), (16, 44), 2)
    w = g.J['wr']; e.cable(p, w)
    e.line((w[0]-6, w[1]), (w[0]+6, w[1]), 4, '#d8d0f7', layer='front')
    g.hl('sh', 'el', .12, .9, 4.8, off=3)
    return e, g

def ex_lyingcurl(s):
    e = Eq(); e.pad(40, 150, 170, 9); e.line((62, 159), (62, 190)); e.line((188, 159), (188, 190))
    g = side(hip=(120, 138), torso=180, head=190, arm=dict(ua=162, fa=178),
             leg=dict(th=0, sh=0) if s == 0 else dict(th=0, sh=-104), ft=0 if s == 0 else -14)
    a = g.J['an']; e.plate((a[0]-3, a[1]), 6, layer='front')
    g.hl('hip', 'kn', .15, .95, 6.2, off=-4); g.hl('kn', 'an', .1, .55, 4.8, off=-3)
    return e, g

def seated_leg(s, flexed_first):
    e = Eq(); hip = (88, 142)
    ext = dict(th=-4, sh=15); flx = dict(th=-4, sh=100)
    spec = (flx if flexed_first else ext) if s == 0 else (ext if flexed_first else flx)
    g = side(hip=hip, torso=-100, leg=spec, arm=dict(ua=62, fa=18))
    e.pad(58, 152, 84, 8); e.line((70, 160), (70, 190)); e.line((128, 160), (128, 190))
    e.thick((76, 150), (67, 92), 9)
    kn = g.J['kn']; e.thick((kn[0]-30, kn[1]-12), (kn[0]-4, kn[1]-12), 6, layer='back')
    a = g.J['an']; e.plate((a[0]-4, a[1]+3), 6, layer='front')
    return e, g, hip

def ex_seatedcurl(s):
    e, g, _ = seated_leg(s, flexed_first=False); g.hl('hip', 'kn', .2, .95, 6.2, off=4); return e, g
def ex_extensor(s):
    e, g, _ = seated_leg(s, flexed_first=True); g.hl('hip', 'kn', .2, .95, 6.2, off=-4); g.hl('kn', 'an', .1, .45, 4.2, off=-3); return e, g

def ex_legpress(s):
    e = Eq(); hip = (104, 160); d = -45
    tgt = pt(hip, d, 54 if s == 0 else 72)
    g = side(hip=hip, torso=-135, leg=dict(to=tgt, side=-1), arm=dict(ua=80, fa=30), ft=-135)
    e.line((62, 186), (208, 40), 1.8, op=.5); e.line((74, 190), (214, 50), 1.8, op=.3)
    e.thick((126, 178), (74, 126), 9); e.thick((96, 170), (136, 170), 7)
    an = g.J['an']; q = pt(an, d, 9); perp = (math.cos(math.radians(45)), math.sin(math.radians(45)))
    e.thick((q[0]-perp[0]*26, q[1]-perp[1]*26), (q[0]+perp[0]*26, q[1]+perp[1]*26), 6, layer='front')
    g.hl('hip', 'kn', .2, .95, 6.4, off=5)
    return e, g

def ex_hip(s):
    e = Eq(); S = (98, 139); e.pad(40, 148, 66, 42, 6)
    hip = pt(S, 32 if s == 0 else -6, TORSO)
    g = side(shoulder=S, torso=(32 if s == 0 else -6) + 180, head=205, leg=dict(to=(174, 186)),
             arm=dict(ua=60, fa=10), ft=0)
    e.plate((hip[0], hip[1]-9), 14)
    g.hl_dot((hip[0]-3, hip[1]+3), 9)
    return e, g

def ex_squat(s):
    e = Eq(); X = 111
    e.line((X, 14), (X, 188), 1.8, op=.45); e.line((X-9, 14), (X-9, 188), 1.2, op=.25)
    if s == 0: hip = (112, 110); torso = -90
    else: hip = (91, 134); torso = -66
    g = side(hip=hip, torso=torso, leg=dict(to=(126, 186)), head=torso-12 if s else -90,
             arm=dict(to=(g_pt(hip, torso)[0]+14, g_pt(hip, torso)[1]-8), side=1))
    sh_ = g.J['sh']; e.plate((sh_[0]-5, sh_[1]-1), 12, layer='back')
    g.hl('hip', 'kn', .15, .95, 6.6, off=-5)
    return e, g
def g_pt(hip, torso): return pt(hip, torso, TORSO)

def ex_rdl(s):
    e = Eq()
    if s == 0: hip = (122, 110); torso = -90; leg = dict(th=90, sh=90)
    else: hip = (100, 114); torso = -22; leg = dict(to=(122, 186))
    S = pt(hip, torso, TORSO)
    tgt = (S[0]+4, S[1]+52) if s == 0 else (S[0]+3, S[1]+52)
    g = side(hip=hip, torso=torso, leg=leg, head=torso-14 if s else -90, arm=dict(to=tgt, side=1))
    e.plate((g.J['wr'][0]+2, g.J['wr'][1]+(8 if s == 0 else 8)), 13)
    g.hl_dot((hip[0]-5, hip[1]+2), 9); g.hl('hip', 'kn', .35, .95, 5.5, off=4)
    return e, g

def ex_cavalinho(s):
    e = Eq(); hip = (90, 126)
    g = side(hip=hip, torso=-52, leg=dict(to=(112, 186)), head=-60,
             arm=dict(to=(176, 150), side=1) if s == 0 else dict(to=(130, 108), side=1))
    e.thick((142, 70), (160, 134), 10); e.line((150, 138), (168, 190), 2.2); e.thick((92, 186), (152, 186), 5)
    w = g.J['wr']; e.line((w[0]-1, w[1]-8), (w[0]-1, w[1]+8), 4, '#d8d0f7', layer='front')
    e.line((w[0]+1, w[1]), (196, 170), 2, op=.7) ; e.pulley((196, 170))
    g.hl('hip', 'sh', .3, .95, 6.6, off=-6)
    return e, g

def ex_crossover(s):
    e = Eq(); hip_y = 110; sy = hip_y - TORSO
    g = front(CX, hip_y, leg=dict(th=86, sh=94),
              arm=dict(to=(CX+56, sy+10), side=1) if s == 0 else dict(to=(CX+7, sy+36), side=-1))
    for sgn in (1, -1):
        x = CX+sgn*104
        e.stack(x-8, 40, 186); p = (x-sgn*10, sy+4); e.pulley(p)
        w = g.J['wrR'] if sgn > 0 else g.J['wrL']; e.cable(p, w)
    g.hl_dot((CX+11, sy+14), 8); g.hl_dot((CX-11, sy+14), 8)
    return e, g

def ex_adductor(s):
    hip_y = 138; e = Eq()
    leg = dict(th=25, sh=92, sc=.8) if s == 0 else dict(th=72, sh=90, sc=.34)
    g = front(CX, hip_y, leg=leg, arm=dict(ua=72, fa=82))
    seat_front(e, hip_y, g.J['sh'][1]-6)
    for k in ('knR', 'knL'):
        kx, ky = g.J[k]; sgn = 1 if k == 'knR' else -1
        e.thick((kx+sgn*9, ky-9), (kx+sgn*9, ky+11), 7, layer='front')
    g.hl('hR', 'knR', .25, .9, 6.2, off=3); g.hl('hL', 'knL', .25, .9, 6.2, off=-3)
    return e, g

def ex_calf(s):
    e = Eq(); B = (142, 174.4)
    ft = -18 if s == 0 else 42
    an = (B[0]-13*math.cos(math.radians(ft)), B[1]-13*math.sin(math.radians(ft)))
    hip = (an[0], an[1]-76)
    e.pad(110, 178, 50, 12, 3)
    g = side(hip=hip, torso=-90, leg=dict(th=90, sh=90), ft=ft, arm=dict(ua=70, fa=-60))
    sh_ = g.J['sh']; e.thick((sh_[0]-8, sh_[1]-1), (sh_[0]+8, sh_[1]-1), 8, layer='mid' if False else 'back')
    e.line((sh_[0]+14, sh_[1]-2), (sh_[0]+14, 16), 2.2); e.pad(sh_[0]-4, 8, 36, 8, 3)
    g.hl('kn', 'an', .1, .9, 5.2, off=3)
    return e, g

def ex_seatedcalf(s):
    e = Eq(); ft = -14 if s == 0 else 40
    an = (130, 177 if s == 0 else 168); kn = (130, an[1]-38); hip = (92, kn[1])
    e.pad(112, 178, 50, 12, 3); e.pad(56, 152, 70, 8); e.line((70, 160), (70, 190))
    g = side(hip=hip, torso=-90, leg=dict(th=0, sh=90), ft=ft, arm=dict(ua=70, fa=20))
    k = g.J['kn']; e.thick((k[0]-18, k[1]-9), (k[0]+8, k[1]-9), 9, layer='front'); e.line((k[0]-4, k[1]-14), (k[0]-4, 36), 2.2)
    e.stack(190, 70, 186)
    g.hl('kn', 'an', .1, .9, 5.2, off=3)
    return e, g

def ex_deadbug(s):
    e = Eq(); e.line((26, 189), (214, 189), 4, DEEP); e.line((26, 189), (214, 189), 1.2, '#7a69cc')
    leg_t = dict(th=-90, sh=0)
    g = side(hip=(132, 178), torso=180, head=186, arm=dict(ua=-90, fa=-90),
             arm2=dict(ua=-90, fa=-90) if s == 0 else dict(ua=-173, fa=-176),
             leg=leg_t if s == 0 else dict(th=-14, sh=-6),
             leg2=dict(th=-84, sh=6) if s == 0 else dict(th=-90, sh=0), ft=-80 if s == 0 else 0)
    g.hl('hip', 'sh', .2, .85, 6.4, off=4)
    return e, g

def ex_plank(s):
    e = Eq(); th = 8.1; S = (68, 157)
    hip = pt(S, th, TORSO)
    g = side(shoulder=S, torso=th+180, head=186, leg=dict(th=th, sh=th), ft=55, arm=dict(ua=90, fa=0))
    e.line((26, 189), (214, 189), 1.4, '#7a69cc', op=.6)
    if s == 1:
        e.line((50, 150), (212, 170), 1.4, GOLD, .9, dash='3 5')
        g.hl('hip', 'sh', .15, .85, 6.4, off=-5)
    return e, g

def ex_sideplank(s):
    e = Eq(); S = (66, 134); th = 21.5 if s == 1 else 12
    g = side(shoulder=S, torso=th+180, head=th+180-14, leg=dict(th=th, sh=th), ft=15,
             arm=dict(ua=90, fa=90), arm2=dict(ua=-90, fa=-90))
    e.line((26, 189), (214, 189), 1.4, '#7a69cc', op=.6)
    if s == 1: e.line((54, 128), (206, 178), 1.4, GOLD, .9, dash='3 5')
    g.hl('hip', 'sh', .2, .9, 6, off=5 if s else 5)
    return e, g

EXERCISES = [n[3:] for n in dir() if n.startswith('ex_')]
MIRROR = set()
# poses deitadas ocupam pouca altura: ampliadas para preencher o quadro
ZOOM = {'deadbug': 1.15, 'plank': 1.2, 'sideplank': 1.15, 'lyingcurl': 1.15, 'press': 1.15, 'fly': 1.15, 'hip': 1.12, 'incline': 1.08}

def build(name, outdir):
    fn = globals()['ex_'+name]
    parts = []
    for s in (0, 1):
        eq, fig = fn(s)[:2]
        parts.append(panel(eq, fig, mirror=name in MIRROR, zoom=ZOOM.get(name, 1.0)))
    svg = compose(name, parts[0], parts[1])
    (outdir/f'{name}.svg').write_text(svg, encoding='utf-8')

if __name__ == '__main__':
    out = Path(__file__).resolve().parent.parent / 'app' / 'images'
    out.mkdir(exist_ok=True)
    names = sys.argv[1:] or EXERCISES
    for n in names: build(n, out)
    print('OK:', len(names), 'ilustrações geradas em', out)
