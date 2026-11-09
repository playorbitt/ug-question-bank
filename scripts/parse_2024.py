import re,json,collections
W='/tmp/claude-0/-home-claude/e92aff11-3822-5985-abba-4ce5ce7b495f/scratchpad/'
CODE=re.compile(r'^([A-Z]{2})\s?[`]?(\d+)\s?[.]\s?(\d+)([A-Z]?)\*?(?=\s|$)')
TOK=re.compile(r'(?:\s{2,}|\s)(A and C|[KSAC](?:\s*[/,]\s*[KSAC])*)\s{2,}((?:KH|SH|K|S|P|H)(?:\s*[/,]\s*(?:KH|SH|K|S|P|H))*)\s{1,}(Y|N|y|n)(?=\s|$)')
HDR=re.compile(r'Number\s+COMPETENCY')
SUBJ=re.compile(r'\(CODE:\s*([A-Z]{2})\)')
TOT=re.compile(r'\(Topics\s*=\s*(\d+),\s*Competencies\s*=\s*(\d+)\)')
TOP=re.compile(r'^\s*Topic:?\s*(\d*)\s*[:\-]?\s*(.*?)\s{2,}Number of [Cc]ompetencies:?\s*\(?\s*(\d+)')
def chunks(s,off):
    return [(m.start()+off,m.group().strip()) for m in re.finditer(r'\S+(?:\s\S+)*',s)]
def run():
    pages=open(W+'n24/g24.txt').read().split('\f')
    rows=[];subj='';topic='';tot={};stated_topic={};cur=None;pos=None;block=[];tail=None;tail_on=False
    def flush():
        nonlocal cur,tail,tail_on
        if cur:
            rows.append(cur)
            tail=cur if (len(cur.get('competency',''))<60 and not cur.get('competency','').rstrip().endswith('.')) else None
            tail_on=False; cur=None
    for i,pg in enumerate(pages):
        pno=472+i; flush()
        for line in pg.split('\n'):
            if not line.strip(): flush(); block=[]; continue
            if HDR.search(line): flush(); continue
            m=SUBJ.search(line)
            if m: flush(); subj=m.group(1); continue
            m=TOT.search(line)
            if m: tot[subj]=(int(m.group(1)),int(m.group(2))); continue
            t=TOP.match(line)
            if t: flush(); topic=t.group(2).strip(' -:'); continue
            ind=len(line)-len(line.lstrip()); body=line[ind:]
            c=CODE.match(body) if ind<14 else None
            if c:
                flush(); tail=None; tm=TOK.search(line)
                if not tm:
                    lo=re.search(r'\s{2,}(Y|N)(?=\s)',line)
                    if lo:
                        pre=line[:lo.start()]; ps=[(m.start(),m.group()) for m in re.finditer(r'\S+(?:\s\S+)*',pre)]
                        # ps[0] is code+text; trailing short chunks are domain/level
                        tail=[x for x in ps[1:] if len(x[1])<=12]
                        txt=ps[0][1] if ps else ''
                        dom=lev=''
                        if len(tail)>=2: dom,lev=tail[-2][1],tail[-1][1]
                        elif len(tail)==1: dom=tail[0][1]
                        ctk=tail[0][0] if tail else lo.start()
                        cur={'code':f'{c.group(1)}{c.group(2)}.{c.group(3)}{c.group(4)}','subject_code':subj,'topic':topic,'page':pno,'competency':line[ind+c.end():ctk].strip(),
                             'domain':dom or 'UNK','level':lev or 'UNK','core':lo.group(1),'star':False,'loose':True,'cols':[[p2,[x]] for p2,x in chunks(line[lo.end():],lo.end())],'ctok':ctk}
                        continue
                    cur={'code':f'{c.group(1)}{c.group(2)}.{c.group(3)}{c.group(4)}','subject_code':subj,'topic':topic,'page':pno,'competency':line[ind+c.end():].strip(),'pending':True,'star':'*' in body[:c.end()],'cols':[],'ctok':0,'lines':1}; continue
                comp=line[ind+c.end():tm.start(1)].strip()
                if len(comp)<12 and block:
                    pre=' '.join(x[:tm.start(1)].strip() for x in block if x[:tm.start(1)].strip())
                    comp=(pre+' '+comp).strip()
                block=[]
                rest=line[tm.end():]
                ch=chunks(rest,tm.end())
                cur={'code':f'{c.group(1)}{c.group(2)}.{c.group(3)}{c.group(4)}','subject_code':subj,'topic':topic,'page':pno,'competency':comp,
                     'domain':('A/C' if tm.group(1)=='A and C' else re.sub(r'\s','',tm.group(1))),'level':re.sub(r'\s','',tm.group(2)),'core':tm.group(3).upper(),
                     'star':'*' in body[:c.end()],'cols':[[p,[x]] for p,x in ch],'ctok':tm.start(1)}
                continue
            if cur is None:
                if line.strip().isdigit(): continue
                if tail is not None and not block and not tail_on:
                    seg=line[:tail['ctok']].strip() if tail.get('ctok') else ''
                    if seg and seg[0].islower(): tail_on=True
                    else: tail=None
                if tail is not None and tail_on:
                    seg=line[:tail['ctok']].strip()
                    if seg: tail['competency']=(tail['competency']+' '+seg).strip()
                    continue
                block.append(line)
                continue
            if line.strip().isdigit(): flush(); continue
            if cur.get('pending'):
                tm=TOK.search(line)
                if tm and cur['lines']<=4:
                    pre=line[:tm.start(1)].strip()
                    if pre: cur['competency']+=' '+pre
                    cur.update({'domain':tm.group(1),'level':tm.group(2),'core':tm.group(3).upper(),'ctok':tm.start(1),'pending':False,'late_token':True})
                    cur['cols']=[[p,[x]] for p,x in chunks(line[tm.end():],tm.end())]
                    continue
                if cur['lines']<=4:
                    cur['competency']+=' '+line.strip(); cur['lines']+=1; continue
                cur=None; continue
            if line[:cur['ctok']].strip(): cur['competency']+=' '+line[:cur['ctok']].strip()
            for p,x in chunks(line[cur['ctok']:],cur['ctok']):
                best=None
                for col in cur['cols']:
                    if col[0]-4<=p: best=col
                if best is None: cur['cols'].append([p,[x]])
                else: best[1].append(x)
    flush()
    out=[]
    for r in rows:
        if r.get('pending'): r['parse_failed']=True; r['raw']=r['competency'][:200]; out.append(r); continue
        cols=[(p,' '.join(x)) for p,x in r.pop('cols')]; r.pop('ctok'); r.pop('lines',None); r.pop('pending',None)
        r['domain']=re.sub(r'[\s,]+','/',re.sub(r'\s*([/,])\s*',r'/',r['domain'])).strip('/').replace('A/and/C','A/C'); r['level']=re.sub(r'\s*[/,]\s*','/',r['level'])
        r['teaching_learning']=cols[0][1] if cols else ''
        r['assessment']=cols[1][1] if len(cols)>1 else ''
        n=''
        for p,x in cols[2:]:
            if re.fullmatch(r'\d+|-|NIL',x): n=x
        r['n_procedures_to_certify']='' if n in('-','NIL') else n
        out.append(r)
    return out,tot
if __name__=='__main__':
    out,tot=run()
    json.dump({'rows':out,'tot':tot},open(W+'n24/rows24.json','w'))
    ok=[r for r in out if not r.get('parse_failed')]
    print(len(out),'ok',len(ok),'failed',len(out)-len(ok),'unique',len({r['code'] for r in ok}))
    print(tot)
    c=collections.Counter(r['subject_code'] for r in ok if r['code'].startswith(r['subject_code']))
    print({k:(c[k],tot.get(k)) for k in tot})
