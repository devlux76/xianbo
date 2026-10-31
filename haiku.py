import json,os,subprocess,sys,time
from concurrent.futures import ThreadPoolExecutor
# usage: haiku.py <lens.md> <out.md>  — the xianbo.py system prompt (lens, remembered examples, closing), each question alone, through the claude CLI.
# The CLI adds a one-line SDK preamble and an environment block; auto-memory, settings, tools and MCP are off. Sampling is the model default.
LENS,OUT=sys.argv[1:3]; MODEL='claude-haiku-5-5'
CLOSE=open('lens/xianbo-close.txt',encoding='utf-8').read().strip()
SHOTS=json.load(open('lens/examples-uncle.json',encoding='utf-8'))
REMEMBERED='昔者姪來，伯答之如此：\n'+'\n'.join(('姪曰：' if m['role']=='user' else '伯曰：')+m['content'] for m in SHOTS)
sysmsg='\n\n'.join(x for x in (open(LENS,encoding='utf-8').read().strip('\n'),REMEMBERED,CLOSE) if x)
src=open('xianbo.py',encoding='utf-8').read(); Q=eval(src[src.index('Q=[')+2:src.index(']\n',src.index('Q=['))+1])
sf=os.path.abspath(OUT+'.system.txt'); open(sf,'w',encoding='utf-8').write(sysmsg)
env={**os.environ,'CLAUDE_CODE_DISABLE_AUTO_MEMORY':'1'}
def ask(q):
    t=time.time()
    r=subprocess.run(['claude','-p','--model',MODEL,'--system-prompt-file',sf,'--tools','','--disable-slash-commands','--setting-sources','','--strict-mcp-config','--no-session-persistence',q],
                     capture_output=True,text=True,env=env,cwd=os.environ.get('CLAUDE_JOB_DIR','/tmp'),timeout=600)
    return (r.stdout.strip() or 'ERROR: '+r.stderr.strip()), time.time()-t
with ThreadPoolExecutor(4) as ex: res=list(ex.map(ask,Q))
with open(OUT,'w',encoding='utf-8') as out:
    out.write(f'# Run: {MODEL}, lens = {LENS.rsplit("/",1)[-1]}, examples in system examples-uncle.json, system ends "{CLOSE}"\n\n')
    for i,(q,(a,dt)) in enumerate(zip(Q,res),1): out.write(f'## Q{i}. {q}\n\n{a}\n\n*{dt:.0f}s wall*\n\n')
os.remove(sf)
