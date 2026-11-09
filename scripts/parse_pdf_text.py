import re,json
W='/tmp/claude-0/-home-claude/e92aff11-3822-5985-abba-4ce5ce7b495f/scratchpad/'
CODE=re.compile(r'^([A-Z]{2,3})(\d+)\.(\d+)([A-Z]?)(?=\s)')
TOK=re.compile(r'\s{2,}([KSAC](?:\s?/\s?[KSAC])*)\s+((?:KH|SH|K|S|P)(?:\s?/\s?(?:KH|SH|K|S|P))*)\s+(Y|N)(?=\s|$)')
TOK2=re.compile(r'(?:\s{2,}|\s(?=A and C))(A and C|[KSAC](?:\s?/\s?[KSAC])*)\s+((?:KH|SH|K|S|P)(?:\s?/\s?(?:KH|SH|K|S|P|H))*)\s*/?\s*(Y|N|y|n)?(?=\s|$)')
HDR=re.compile(r'Number\s+COMPETENCY\s+Domain')
TOP=re.compile(r'^\s*Topic:\s*(.*?)\s{2,}Number of competencies:\s*\(?([^)\s]*)\)?\s+Number of procedures[^(]*\(?([^)]*)\)?')
SUBJ=re.compile(r'^\s{0,10}([A-Z][A-Za-z &,\-/()]+?)\s*\(CODE:\s*([A-Z]+)\)')
def chunks(s,off=0):
    return [(m.start()+off,m.group().strip()) for m in re.finditer(r'\S+(?:\s\S+)*',s) ]
def parse(vol):
    pages=open(W+f'UG-Curriculum-Vol-{vol}.txt').read().split('\f')
    rows=[];subj=('','');topic=('','','');cur=None;hp=None
    def flush():
        nonlocal cur
        if cur: rows.append(cur); cur=None
    for pno,pg in enumerate(pages,1):
        flush()
        for line in pg.split('\n'):
            line=re.sub(r'^(\s*[A-Z]{2})[\s`]*(\d+)[\s.]+(\d+)(?=\s)',r'\1\2.\3',line)
            if HDR.search(line):
                flush(); i=line.find('Vertical'); j=line.find('Horizontal'); hp=(i,j); continue
            if not line.strip(): flush(); continue
            m=SUBJ.match(line)
            if m: flush(); subj=(m.group(1).strip(),m.group(2)); continue
            t=TOP.match(line)
            if t: flush(); topic=(t.group(1).strip(),t.group(2),t.group(3).strip()); continue
            ind=len(line)-len(line.lstrip())
            c=CODE.match(line[ind:]) if ind<12 else None
            if c:
                flush()
                tm=TOK.search(line)
                lenient=False
                if not tm:
                    tm=TOK2.search(line); lenient=True
                if not tm: continue
                comp=line[ind+c.end():tm.start()].strip()
                rest=line[tm.end():]
                ch=chunks(rest,tm.end())
                cur={'volume':vol,'page':pno,'subject':subj[0],'subject_code':subj[1],'topic':topic[0],
                 'code':c.group(0).strip(),'competency':comp,'domain':('A/C' if tm.group(1)=='A and C' else re.sub(r'\s','',tm.group(1))),'level':re.sub(r'\s','',tm.group(2)).replace('K/H','K/KH'),'core':(tm.group(3) or '').upper(),'lenient':lenient,
                 'cols':[[p,[x]] for p,x in ch],'cstart':c.end(),'ctok':tm.start(),'hp':hp}
                continue
            if cur is None: continue
            # continuation
            if line.strip().isdigit(): flush(); continue
            if cur['ctok']>0 and line[:cur['ctok']].strip():
                cur['competency']+=' '+line[:cur['ctok']].strip()
            rest=line[cur['ctok']:] if len(line)>cur['ctok'] else ''
            for p,x in chunks(rest,cur['ctok']):
                best=None
                for col in cur['cols']:
                    if col[0]-4<=p: best=col
                if best is None or not cur['cols']: cur['cols'].append([p,[x]])
                else: best[1].append(x)
    flush()
    out=[]
    for r in rows:
        cols=r.pop('cols'); hp=r.pop('hp'); r.pop('cstart'); r.pop('ctok')
        cols=[(p,' '.join(x)) for p,x in cols]
        r['teaching_learning']=cols[0][1] if cols else ''
        r['assessment']=cols[1][1] if len(cols)>1 else ''
        n=''; v=[]; h=[]
        for p,x in cols[2:]:
            if re.fullmatch(r'\d+',x): n=x
            elif hp and hp[1]>0 and p>=hp[1]-6: h.append(x)
            else: v.append(x)
        r['n_procedures_to_certify']=n; r['vertical_integration']='; '.join(v); r['horizontal_integration']='; '.join(h)
        out.append(r)
    return out
if __name__=='__main__':
    allr=[]
    for v in ['I','II','III']:
        r=parse(v);print(v,len(r));allr+=r
    json.dump(allr,open(W+'rows.json','w'))
