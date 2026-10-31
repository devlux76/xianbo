import re,glob,json,statistics as st,random
def parse(f):
    t=open(f,encoding='utf-8').read(); out={}
    for m in re.finditer(r'^## Q(\d+)\. .*?\n\n(.*?)\n\n\*(\d+)s',t,re.S|re.M): out[int(m[1])]=(m[2].strip(),int(m[3]))
    return out
sets={'q8-suyuan':sorted(glob.glob('runs/q8-sysex-s*--suyuan-nolabel-xianbo--nothink.md')),
      'q8-nolens':sorted(glob.glob('runs/q8-sysex-s*--nolens-xianbo--nothink.md')),
      'haiku-suyuan':sorted(glob.glob('runs/haiku-s*--suyuan-nolabel-xianbo.md')),
      'haiku-nolens':sorted(glob.glob('runs/haiku-s*--nolens-xianbo.md'))}
P={k:[parse(f) for f in v] for k,v in sets.items()}
for k,v in P.items():
    w=[len(a.split()) for r in v for a,_ in r.values()]; s=[d for r in v for _,d in r.values()]
    print(f'{k:13} n={len(w):2} words median {st.median(w):4.0f} max {max(w):4}  sec median {st.median(s):4.0f} total/run {sum(s)/len(v)/60:5.1f} min')
random.seed(31); pairs=[]; key=[]
for m in ('q8','haiku'):
    for i,(a,b) in enumerate(zip(P[m+'-suyuan'],P[m+'-nolens'])):
        for q in range(1,8):
            flip=random.random()<.5; x,y=(b[q][0],a[q][0]) if flip else (a[q][0],b[q][0])
            pairs.append((m,i+1,q,x,y)); key.append({'id':len(pairs),'model':m,'sample':i+1,'q':q,'A':'nolens' if flip else 'suyuan'})
order=list(range(len(pairs))); random.shuffle(order)
Q=open('xianbo.py',encoding='utf-8').read(); 
with open('judging/pairs.md','w') as f:
    for n in order:
        m,s,q,x,y=pairs[n]; f.write(f'### Pair {n+1} (Q{q})\n**A:** {x}\n\n**B:** {y}\n\n')
json.dump(key,open('judging/key.json','w'))
