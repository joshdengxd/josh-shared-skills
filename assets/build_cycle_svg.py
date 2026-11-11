import os
W,H=1190,760
SANS="Inter,'Segoe UI',Helvetica,Arial,sans-serif"
MONO="ui-monospace,SFMono-Regular,Consolas,Menlo,monospace"
F='font-family="%s"'%SANS
DASH='stroke-dasharray="5 4"'
o=[];a=o.append
a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="Delivery cycle: refine, build and evaluate, ship, investigate with data, foundations">'%(W,H,W,H))
mk=""
for i,c in (("ar","#57606a"),("ab","#1F6FEB"),("at","#0E8A8A"),("ag","#2EA44F"),("ap","#6B4FBB"),("ao","#E36209")):
    mk+='<marker id="%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>'%(i,c)
a('<defs><filter id="sh" x="-10%%" y="-10%%" width="120%%" height="130%%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#1f2328" flood-opacity="0.10"/></filter><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#F6F8FA"/></linearGradient>%s</defs>'%mk)
a('<rect x="0.5" y="0.5" width="%d" height="%d" rx="18" fill="url(#bg)" stroke="#D0D7DE"/>'%(W-1,H-1))
a('<text x="40" y="48" %s font-size="22" font-weight="700" fill="#1f2328">Delivery cycle</text>'%F)
a('<text x="40" y="72" %s font-size="13" fill="#57606a">From a vague ticket to a production release. Independent agents check the work. A human takes every irreversible step.</text>'%F)
def panel(x,y,w,h,n,t,c,f):
    a('<rect x="%d" y="%d" width="%d" height="%d" rx="14" fill="%s" stroke="%s" stroke-opacity="0.35"/>'%(x,y,w,h,f,c))
    a('<circle cx="%d" cy="%d" r="12" fill="%s"/><text x="%d" y="%d" %s font-size="13" font-weight="700" fill="#fff" text-anchor="middle">%s</text>'%(x+26,y+28,c,x+26,y+33,F,n))
    a('<text x="%d" y="%d" %s font-size="12.5" font-weight="700" letter-spacing="1.2" fill="%s">%s</text>'%(x+46,y+33,F,c,t))
def card(x,y,w,h,t,s,c,mono=True,fill="#fff"):
    ff=MONO if mono else SANS
    a('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" stroke="%s" stroke-opacity="0.55" filter="url(#sh)"/>'%(x,y,w,h,fill,c))
    a('<rect x="%d" y="%d" width="4" height="%d" rx="2" fill="%s"/>'%(x+1,y+10,h-20,c))
    ty=y+24 if s else y+h/2+5
    a('<text x="%d" y="%s" font-family="%s" font-size="15" font-weight="700" fill="#1f2328">%s</text>'%(x+18,ty,ff,t))
    if s:
        for i,p in enumerate(s.split("|")):
            a('<text x="%d" y="%d" %s font-size="12" fill="#57606a">%s</text>'%(x+18,y+42+i*15,F,p))
def line(d,m="ar",dash=False,c="#57606a"):
    a('<path d="%s" fill="none" stroke="%s" stroke-width="1.6" %s marker-end="url(#%s)"/>'%(d,c,DASH if dash else "",m))
def label(x,y,t,c,anchor="middle"):
    a('<text x="%d" y="%d" %s font-size="11.5" font-weight="600" fill="%s" text-anchor="%s">%s</text>'%(x,y,F,c,anchor,t))
OR,BL,TL,PU,GR,GY="#E36209","#1F6FEB","#0E8A8A","#6B4FBB","#2EA44F","#57606a"
# panels row
panel(40,100,200,300,"1","REFINE",OR,"#FFF8F0")
panel(270,100,420,300,"2","BUILD, EVALUATE, IMPROVE",BL,"#F3F8FF")
panel(720,100,430,300,"4","SHIP",PU,"#F8F4FF")
def proc(y,t):
    a('<rect x="60" y="%d" width="160" height="34" rx="17" fill="#fff" stroke="%s" stroke-dasharray="4 3"/><text x="140" y="%d" %s font-size="12" fill="#57606a" text-anchor="middle">%s</text>'%(y,OR,y+22,F,t))
proc(150,"Epic / feature")
proc(194,"Spec: agent drafts")
proc(238,"Tickets: breakdown")
line("M140 184 L140 192","ao",False,OR)
line("M140 228 L140 236","ao",False,OR)
line("M140 272 L140 296","ao",False,OR)
card(60,298,160,64,"ticket-refine","Spec + criteria|User approves draft",OR)
label(140,386,"dashed: process, no skill yet",OR)
card(290,156,380,58,"implement-with-score-gate","Worktree, implement, fresh subagent scores 0-10",BL)
card(290,230,380,58,"verify-against-criteria","Post-task hook: read-only verdict + evidence",BL)
card(290,304,380,58,"live-env-local-test","Post-task hook: real environment, local build",BL)
line("M220 330 C255 330 255 185 288 185","ao",False,OR)
line("M670 259 L682 259 L682 185 L672 185","ab",True,BL)
label(530,386,"not passing: findings go back, new scorer each round","#1F6FEB")
a('<rect x="740" y="156" width="390" height="44" rx="22" fill="#6B4FBB" filter="url(#sh)"/><text x="935" y="183" %s font-size="14" font-weight="700" fill="#fff" text-anchor="middle">You review and merge the PR</text>'%F)
card(740,224,185,64,"deploy-to-staging","Explicit tag, GitOps sync|You confirm",PU)
card(945,224,185,64,"prod-release-gate","Stop after each step|Canary go / no-go",PU)
line("M670 333 C710 333 710 178 738 178","ab",False,BL)
label(712,320,"PASS",BL,"start")
line("M935 200 L835 222","ap",False,PU)
line("M925 256 L943 256","ap",False,PU)
a('<text x="935" y="330" %s font-size="12" fill="#57606a" text-anchor="middle">Production actions are always done by a human.</text>'%F)
# batch band
a('<rect x="270" y="420" width="420" height="84" rx="14" fill="#F1FAFA" stroke="%s" stroke-opacity="0.45"/>'%TL)
a('<circle cx="296" cy="448" r="12" fill="%s"/><text x="296" y="453" %s font-size="13" font-weight="700" fill="#fff" text-anchor="middle">3</text><text x="316" y="453" %s font-size="12.5" font-weight="700" letter-spacing="1.2" fill="%s">RUN IT AT SCALE</text>'%(TL,F,F,TL))
a('<text x="290" y="478" font-family="%s" font-size="15" font-weight="700" fill="#1f2328">issue-batch-drain</text>'%MONO)
a('<text x="290" y="496" %s font-size="12" fill="#57606a">One group at a time: fresh implementer, then fresh verifier</text>'%F)
line("M480 418 L480 402","at",True,TL)
label(492,413,"each group runs box 2",TL,"start")
# investigate
panel(40,530,1110,84,"5","INVESTIGATE WITH DATA",GR,"#F3FBF4")
card(60,566,250,38,"log-analysis","",GR)
a('<text x="330" y="591" %s font-size="12.5" fill="#57606a">debug  ·  size a change  ·  check an assumption  ·  evidence for a proposal  ·  baseline  ·  monitor  ·  A/B tests</text>'%F)
line("M140 530 L140 402","ag",True,GR)
label(152,470,"evidence for specs and design",GR,"start")
line("M935 530 L935 402","ag",True,GR)
label(947,470,"canary and debugging",GR,"start")
line("M1060 402 L1060 528","ag",True,GR)
label(1072,470,"monitor, A/B results",GR,"start")
# foundations
panel(40,640,1110,84,"6","FOUNDATIONS",GY,"#F6F8FA")
card(60,676,150,38,"wrap-up","",GY)
card(226,676,270,38,"agent-context-template","",GY)
a('<text x="516" y="701" %s font-size="12.5" fill="#57606a">every session ends with what worked saved as memory; every repo starts with the right rules</text>'%F)
a('</svg>')
out=os.path.join(os.path.dirname(os.path.abspath(__file__)),"cycle.svg")
open(out,"w",encoding="utf-8").write("\n".join(o))
