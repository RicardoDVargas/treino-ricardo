"""Rig e primitivas para as ilustrações do Treino Ricardo (tema galáctico).
Figuras: capsulas conicas + articulações em forma de estrela + músculo-alvo iluminado."""
import math, random

W, H, FLOOR = 480, 222, 190
TORSO, THIGH, SHIN, UA, FA, NECK, HEADR = 46, 38, 38, 27, 25, 6, 9.5
GOLD, LAV, DEEP = '#f2cf8a', '#a99bdc', '#2a1d63'

def pt(a, ang, l):
    r = math.radians(ang); return (a[0] + l*math.cos(r), a[1] + l*math.sin(r))

def ik(a, t, l1, l2, side):
    dx, dy = t[0]-a[0], t[1]-a[1]
    d = math.hypot(dx, dy); d = max(min(d, l1+l2-0.05), abs(l1-l2)+0.05)
    base = math.atan2(dy, dx)
    A = math.acos(max(-1, min(1, (l1*l1 + d*d - l2*l2)/(2*l1*d))))
    ang = base + side*A
    mid = (a[0]+l1*math.cos(ang), a[1]+l1*math.sin(ang))
    end = (a[0]+d*math.cos(base), a[1]+d*math.sin(base))
    return mid, end

def f(v): return f'{v:.1f}'.rstrip('0').rstrip('.')

def capsule(a, b, ra, rb, fill, extra=''):
    dx, dy = b[0]-a[0], b[1]-a[1]; d = math.hypot(dx, dy) or 1
    ux, uy = dx/d, dy/d; nx, ny = -uy, ux
    p1 = (a[0]+nx*ra, a[1]+ny*ra); p2 = (b[0]+nx*rb, b[1]+ny*rb)
    p3 = (b[0]-nx*rb, b[1]-ny*rb); p4 = (a[0]-nx*ra, a[1]-ny*ra)
    return (f'<path d="M{f(p1[0])} {f(p1[1])}L{f(p2[0])} {f(p2[1])}A{f(rb)} {f(rb)} 0 0 0 {f(p3[0])} {f(p3[1])}'
            f'L{f(p4[0])} {f(p4[1])}A{f(ra)} {f(ra)} 0 0 0 {f(p1[0])} {f(p1[1])}Z" fill="{fill}" {extra}/>')

FILL55 = 'fill-opacity=".55"'
BODY = 'url(#body)'; LIMB = 'url(#limb)'; BODY_FAR = '#4a3399'
EDGE = 'stroke="#fff" stroke-opacity=".45" stroke-width=".9"'

class Fig:
    def __init__(self, kind):
        self.kind = kind; self.J = {}; self.far = []; self.mid = []; self.near = []; self.top = []

    # ---------- desenhos comuns ----------
    def node(self, p, r=1.9):
        self.top.append(f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="{f(r*2.3)}" fill="#fff" fill-opacity=".16"/>'
                        f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="{f(r)}" fill="#fff"/>')

    def limb(self, lst, pts, radii, fill=LIMB, nodes=True, hand=False):
        for i in range(len(pts)-1):
            lst.append(capsule(pts[i], pts[i+1], radii[i], radii[i+1], fill, EDGE))
        if hand:
            lst.append(f'<circle cx="{f(pts[-1][0])}" cy="{f(pts[-1][1])}" r="4.1" fill="{fill}" {EDGE}/>')
        if nodes:
            for p in pts[:-1] if not hand else pts[:-1]: self.node(p)

    def hl(self, a, b, t0=0.2, t1=0.8, r=6, off=0):
        A, B = self.J[a], self.J[b]
        dx, dy = B[0]-A[0], B[1]-A[1]; d = math.hypot(dx, dy) or 1
        nx, ny = -dy/d, dx/d
        p = (A[0]+dx*t0+nx*off, A[1]+dy*t0+ny*off); q = (A[0]+dx*t1+nx*off, A[1]+dy*t1+ny*off)
        self.top.append(f'<g filter="url(#glow)" opacity=".95">{capsule(p, q, r, r, "url(#hot)")}</g>'
                        f'{capsule(p, q, r*.55, r*.55, "#fff0cf", FILL55)}')

    def hl_dot(self, p, r=8):
        self.top.append(f'<g filter="url(#glow)"><circle cx="{f(p[0])}" cy="{f(p[1])}" r="{f(r)}" fill="url(#hot)"/></g>'
                        f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="{f(r*.45)}" fill="#fff0cf" fill-opacity=".6"/>')

    def svg(self):
        return ''.join(self.far) + ''.join(self.mid) + ''.join(self.near) + ''.join(self.top)

def _arm_pts(S, spec, ua_len=UA, fa_len=FA):
    if 'to' in spec:
        el, wr = ik(S, spec['to'], ua_len, fa_len, spec.get('side', 1))
    else:
        el = pt(S, spec['ua'], ua_len); wr = pt(el, spec['fa'], fa_len)
    return el, wr

def _leg_pts(Hp, spec):
    if 'to' in spec:
        kn, an = ik(Hp, spec['to'], THIGH, SHIN, spec.get('side', -1))
    else:
        kn = pt(Hp, spec['th'], THIGH); an = pt(kn, spec['sh'], SHIN)
    return kn, an

def side(hip=None, shoulder=None, torso=-90, arm=None, leg=None, arm2=None, leg2=None,
         head=None, ft=0, ft2=None, bare_torso=False):
    """Figura de perfil virada para a direita. Ângulos: 0=direita, 90=baixo, -90=cima."""
    g = Fig('side')
    if hip is None: hip = (shoulder[0]-TORSO*math.cos(math.radians(torso)), shoulder[1]-TORSO*math.sin(math.radians(torso)))
    if shoulder is None: shoulder = pt(hip, torso, TORSO)
    hd = torso if head is None else head
    hc = pt(shoulder, hd, NECK + HEADR)
    g.J.update(hip=hip, sh=shoulder, head=hc)
    # pernas
    def leg_draw(spec, lst, fill, ftt, tag):
        kn, an = _leg_pts(hip, spec)
        toe = pt(an, ftt, 13)
        g.J['kn'+tag], g.J['an'+tag], g.J['toe'+tag] = kn, an, toe
        g.limb(lst, [hip, kn, an], [8.8, 6.3, 4.3], fill, nodes=(lst is not g.far))
        lst.append(capsule(an, toe, 4, 2.9, fill, EDGE if lst is not g.far else ''))
    def arm_draw(spec, lst, fill, tag):
        el, wr = _arm_pts(shoulder, spec)
        g.J['el'+tag], g.J['wr'+tag] = el, wr
        g.limb(lst, [shoulder, el, wr], [6.2, 4.9, 3.7], fill, nodes=(lst is not g.far), hand=True)
    if leg2: leg_draw(leg2, g.far, BODY_FAR, ft if ft2 is None else ft2, '2')
    if arm2: arm_draw(arm2, g.far, BODY_FAR, '2')
    # tronco + cabeça
    g.mid.append(capsule(hip, shoulder, 10.2, 12, BODY, EDGE))
    g.mid.append(capsule(shoulder, pt(shoulder, hd, NECK+2), 3.8, 3.4, BODY))
    g.mid.append(f'<circle cx="{f(hc[0])}" cy="{f(hc[1])}" r="{HEADR}" fill="url(#limb)" {EDGE}/>')
    g.node(shoulder); g.node(hip)
    if leg: leg_draw(leg, g.near, LIMB, ft, '')
    if arm: arm_draw(arm, g.near, LIMB, '')
    return g

def front(cx, hip_y, arm=None, arm2='mirror', leg=None, leg2='mirror', sy=None, ua_len=UA, fa_len=FA, sw=16, hw=9):
    """Figura de frente. Ângulos do braço/perna DIREITO da tela; o esquerdo é espelhado."""
    g = Fig('front')
    sy = hip_y - TORSO if sy is None else sy
    g.J.update(hip=(cx, hip_y), sh=(cx, sy), head=(cx, sy-NECK-HEADR))
    g.mid.append(f'<path d="M{f(cx-sw)} {f(sy+2)}L{f(cx+sw)} {f(sy+2)}L{f(cx+hw+1)} {f(hip_y)}L{f(cx-hw-1)} {f(hip_y)}Z" '
                 f'fill="url(#body)" stroke="url(#body)" stroke-width="9" stroke-linejoin="round"/>')
    g.mid.append(capsule((cx, sy), (cx, sy-NECK-2), 3.8, 3.4, BODY))
    hc = g.J['head']
    g.mid.append(f'<circle cx="{f(hc[0])}" cy="{f(hc[1])}" r="{HEADR}" fill="url(#limb)" {EDGE}/>')
    def mir(p): return (2*cx-p[0], p[1])
    def arm_draw(spec, sgn, tag):
        S = (cx+sgn*sw, sy+3)
        if spec.get('mirror_in'): pass
        if 'to' in spec:
            tgt = spec['to'] if sgn > 0 else mir(spec['to'])
            el, wr = ik(S, tgt, ua_len, fa_len, spec.get('side', 1)*sgn)
        else:
            ua_, fa_ = (spec['ua'], spec['fa']) if sgn > 0 else (180-spec['ua'], 180-spec['fa'])
            el = pt(S, ua_, ua_len*spec.get('sc', 1)); wr = pt(el, fa_, fa_len*spec.get('sc', 1))
        g.J['el'+tag], g.J['wr'+tag], g.J['s'+tag] = el, wr, S
        g.limb(g.near, [S, el, wr], [6.3, 5, 3.8], LIMB, hand=True)
    def leg_draw(spec, sgn, tag):
        Hp = (cx+sgn*hw, hip_y)
        if 'to' in spec:
            tgt = spec['to'] if sgn > 0 else mir(spec['to'])
            kn, an = ik(Hp, tgt, THIGH, SHIN, spec.get('side', -1)*sgn)
        else:
            th_, sh_ = (spec['th'], spec['sh']) if sgn > 0 else (180-spec['th'], 180-spec['sh'])
            kn = pt(Hp, th_, THIGH*spec.get('sc', 1)); an = pt(kn, sh_, SHIN)
        g.J['kn'+tag], g.J['an'+tag], g.J['h'+tag] = kn, an, Hp
        g.limb(g.mid, [Hp, kn, an], [8.4, 6.2, 4.3], LIMB)
        toe = (an[0]+sgn*5, an[1]+3)
        g.mid.append(capsule(an, toe, 4, 3, LIMB, EDGE))
    if leg:
        leg_draw(leg, 1, 'R'); leg_draw(leg2 if isinstance(leg2, dict) else leg, -1, 'L')
    if arm:
        arm_draw(arm, 1, 'R'); arm_draw(arm2 if isinstance(arm2, dict) else arm, -1, 'L')
    g.node((cx, hip_y))
    return g

# ---------- equipamento ----------
class Eq:
    def __init__(self): self.back = []; self.front = []
    def line(self, a, b, w=2.2, c=LAV, op=1, dash=None, layer='back', cap='round'):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        getattr(self, layer).append(f'<path d="M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}" stroke="{c}" stroke-width="{w}" stroke-linecap="{cap}" opacity="{op}"{d} fill="none"/>')
    def poly(self, pts, w=2.2, c=LAV, fill='none', layer='back', op=1):
        d = 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts)
        getattr(self, layer).append(f'<path d="{d}" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round" fill="{fill}" opacity="{op}"/>')
    def pad(self, x, y, w, h, r=4, layer='back'):
        getattr(self, layer).append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="{DEEP}" stroke="#7a69cc" stroke-width="1.4"/>')
    def thick(self, a, b, w=9, layer='back'):
        self.line(a, b, w+2.4, '#7a69cc', layer=layer); self.line(a, b, w, DEEP, layer=layer)
    def plate(self, p, r=14, layer='front'):
        getattr(self, layer).append(f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="{r}" fill="#2a1d63" fill-opacity=".55" stroke="#d8d0f7" stroke-width="2.6"/>'
                                    f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="{f(r*.3)}" fill="#d8d0f7"/>')
    def db(self, p, r=7, layer='front'): self.plate(p, r, layer)
    def bar(self, a, b, plate=11, layer='front'):
        self.line(a, b, 3, '#d8d0f7', layer=layer)
        for p, s in ((a, 1), (b, -1)):
            self.line((p[0], p[1]-plate), (p[0], p[1]+plate), 5, '#d8d0f7', layer=layer)
    def dumbbell_h(self, p, ang=0, ln=16, plate=6, layer='front'):
        a = pt(p, ang, -ln/2); b = pt(p, ang, ln/2)
        self.line(a, b, 2.6, '#d8d0f7', layer=layer)
        for q in (a, b):
            n = (math.cos(math.radians(ang+90)), math.sin(math.radians(ang+90)))
            self.line((q[0]-n[0]*plate, q[1]-n[1]*plate), (q[0]+n[0]*plate, q[1]+n[1]*plate), 4.4, '#d8d0f7', layer=layer)
    def cable(self, a, b, layer='back'): self.line(a, b, 1.5, GOLD, 0.9, layer=layer)
    def pulley(self, p, r=5, layer='back'):
        getattr(self, layer).append(f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="{r}" fill="{DEEP}" stroke="{GOLD}" stroke-width="1.6"/>')
    def stack(self, x, y0, y1, w=16):
        self.back.append(f'<rect x="{f(x)}" y="{f(y0)}" width="{w}" height="{f(y1-y0)}" rx="3" fill="{DEEP}" stroke="#7a69cc" stroke-width="1.2"/>')
        yy = y0+7
        while yy < y1-3:
            self.back.append(f'<path d="M{f(x+2)} {f(yy)}H{f(x+w-2)}" stroke="#7a69cc" stroke-width="1" opacity=".7"/>'); yy += 7
    def svg(self): return ''.join(self.back)

DEFS = f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1e1250"/><stop offset=".55" stop-color="#150d38"/><stop offset="1" stop-color="#241058"/></linearGradient>
<radialGradient id="neb1" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#8b5cf6" stop-opacity=".30"/><stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/></radialGradient>
<radialGradient id="neb2" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#d36bd0" stop-opacity=".16"/><stop offset="1" stop-color="#d36bd0" stop-opacity="0"/></radialGradient>
<linearGradient id="body" gradientUnits="userSpaceOnUse" x1="0" y1="20" x2="0" y2="190"><stop offset="0" stop-color="#b7a2ff"/><stop offset="1" stop-color="#6d49df"/></linearGradient>
<linearGradient id="limb" gradientUnits="userSpaceOnUse" x1="0" y1="20" x2="0" y2="190"><stop offset="0" stop-color="#f1e9ff"/><stop offset="1" stop-color="#a98bff"/></linearGradient>
<radialGradient id="hot"><stop offset="0" stop-color="#ffe3a6"/><stop offset=".6" stop-color="#f6a4e6"/><stop offset="1" stop-color="#c26dd6"/></radialGradient>
<linearGradient id="floor" x1="0" x2="1"><stop offset="0" stop-color="#b9a8ff" stop-opacity="0"/><stop offset=".5" stop-color="#b9a8ff" stop-opacity=".55"/><stop offset="1" stop-color="#b9a8ff" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.6"/></filter>
</defs>'''

def panel(eq, fig, mirror=False, zoom=1.0):
    body = ''.join(eq.back) + fig.svg() + ''.join(eq.front)
    if zoom != 1.0: body = f'<g transform="translate(120 {FLOOR}) scale({zoom}) translate(-120 {-FLOOR})">{body}</g>'
    if mirror: body = f'<g transform="translate(240 0) scale(-1 1)">{body}</g>'
    return body

def compose(name, p0, p1, mirror0=False, mirror1=False, shadow=(120, 190), seed=1):
    rnd = random.Random(name)
    stars = ''
    for _ in range(26):
        x, y, r = rnd.uniform(6, 474), rnd.uniform(6, 160), rnd.choice([.5, .7, .9, 1.2])
        stars += f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="#fff" opacity="{rnd.choice([.2,.3,.45,.6])}"/>'
    sh = ''.join(f'<ellipse cx="{x}" cy="{FLOOR+1}" rx="46" ry="4" fill="#000" opacity=".28"/>' for x in (120, 360))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{DEFS}'
            f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
            f'<ellipse cx="120" cy="96" rx="130" ry="100" fill="url(#neb1)"/><ellipse cx="370" cy="110" rx="140" ry="90" fill="url(#neb2)"/>{stars}'
            f'<path d="M18 {FLOOR}H462" stroke="url(#floor)" stroke-width="1.4"/>{sh}'
            f'<path d="M240 24V{FLOOR-4}" stroke="#b9a8ff" stroke-opacity=".14" stroke-dasharray="2 5"/>'
            f'<g>{p0}</g><g transform="translate(240 0)">{p1}</g>'
            f'<g transform="translate(240 98)"><circle r="13" fill="#1c1050" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>'
            f'<path d="M-3.5-4.5 2.5 0-3.5 4.5" fill="none" stroke="{GOLD}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>'
            f'</svg>')
