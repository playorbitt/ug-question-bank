import json,re,csv,collections
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
W='/tmp/claude-0/-home-claude/e92aff11-3822-5985-abba-4ce5ce7b495f/scratchpad/'
a=[json.loads(l) for l in open(W+'out/competencies.jsonl')]
b=[json.loads(l) for l in open(W+'out/competencies_2024.jsonl')]
MAP={'IM':'GM','BI':'BC'}
NAME={'AN':'Human Anatomy','PY':'Physiology','BI':'Biochemistry','BC':'Biochemistry','PH':'Pharmacology','PA':'Pathology','MI':'Microbiology','FM':'Forensic Medicine & Toxicology','CM':'Community Medicine','IM':'General Medicine','GM':'General Medicine','CT':'Respiratory Medicine','PE':'Pediatrics','PS':'Psychiatry','DR':'Dermatology, Venereology & Leprosy','PM':'Physical Medicine & Rehabilitation','SU':'General Surgery','OP':'Ophthalmology','EN':'Otorhinolaryngology (ENT)','OG':'Obstetrics & Gynaecology','OR':'Orthopaedics','AS':'Anaesthesiology','RD':'Radiodiagnosis','RT':'Radiotherapy','DE':'Dentistry'}
for x in a: x['subject']=NAME[x['subject_code']]
for x in a: x['sub24']=MAP.get(x['subject_code'],x['subject_code'])
def norm(t): 
    t=t.lower(); t=re.sub(r'[^a-z0-9 ]',' ',t); return re.sub(r'\s+',' ',t).strip()
rows=[];matched24=set();matched18=set()
subs=sorted({x['sub24'] for x in a}|{x['subject_code'] for x in b})
for s in subs:
    A=[x for x in a if x['sub24']==s]; B=[x for x in b if x['subject_code']==s]
    if not A or not B: continue
    tv=TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True).fit([norm(x['competency_text']) for x in A+B])
    S=cosine_similarity(tv.transform([norm(x['competency_text']) for x in A]),tv.transform([norm(x['competency_text']) for x in B]))
    # exact normalized-text and code boosts
    na=[norm(x['competency_text']) for x in A]; nb=[norm(x['competency_text']) for x in B]
    for i,x in enumerate(A):
        for j,y in enumerate(B):
            if na[i]==nb[j]: S[i,j]=1.0
    pairs=sorted(((S[i,j],i,j) for i in range(len(A)) for j in range(len(B)) if S[i,j]>=0.45),reverse=True)
    ua=set();ub=set()
    for sim,i,j in pairs:
        if i in ua or j in ub: continue
        ua.add(i);ub.add(j)
        x,y=A[i],B[j]
        mapped_code=re.sub(r'^[A-Z]{2}',s,x['code'])
        st='identical' if sim>=0.999 else ('minor_edit' if sim>=0.85 else 'reworded')
        rows.append({'status':st,'subject':y['subject'],'code_2018':x['code'],'code_2024':y['code'],'similarity':round(float(sim),3),'code_changed':int(mapped_code!=y['code']),
          'level_2018':x['level_max'],'level_2024':y['level_max'],'level_changed':int(x['level_max']!=y['level_max']),'core_2018':x['core'],'core_2024':y['core'],'core_changed':int(str(x['core'])!=str(y['core']) and y['core']!=''),
          'text_2018':x['competency_text'],'text_2024':y['competency_text']})
        matched18.add(x['code']);matched24.add(y['code'])
    for i,x in enumerate(A):
        if i not in ua: rows.append({'status':'removed_in_2024','subject':x['subject'],'code_2018':x['code'],'code_2024':'','similarity':'','code_changed':'','level_2018':x['level_max'],'level_2024':'','level_changed':'','core_2018':x['core'],'core_2024':'','core_changed':'','text_2018':x['competency_text'],'text_2024':''})
    for j,y in enumerate(B):
        if j not in ub: rows.append({'status':'added_in_2024','subject':y['subject'],'code_2018':'','code_2024':y['code'],'similarity':'','code_changed':'','level_2018':'','level_2024':y['level_max'],'level_changed':'','core_2018':'','core_2024':y['core'],'core_2024_':'','core_changed':'','text_2018':'','text_2024':y['competency_text']})
# 2018-only subjects
for x in a:
    if x['sub24'] not in {y['subject_code'] for y in b}:
        rows.append({'status':'removed_in_2024','subject':x['subject'],'code_2018':x['code'],'code_2024':'','similarity':'','code_changed':'','level_2018':x['level_max'],'level_2024':'','level_changed':'','core_2018':x['core'],'core_2024':'','core_changed':'','text_2018':x['competency_text'],'text_2024':''})
cols=['status','subject','code_2018','code_2024','similarity','code_changed','level_2018','level_2024','level_changed','core_2018','core_2024','core_changed','text_2018','text_2024']
with open(W+'out/comparison_2018_vs_2024.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,cols,extrasaction='ignore');w.writeheader();w.writerows(rows)
json.dump(rows,open(W+'comparison.json','w'))
c=collections.Counter(r['status'] for r in rows);print(len(a),len(b),c)
t=collections.defaultdict(collections.Counter)
for r in rows: t[r['subject']][r['status']]+=1
for s,v in sorted(t.items()): print(s,dict(v))
m=[r for r in rows if r['status'] in('identical','minor_edit','reworded')]
print('matched',len(m),'code_changed',sum(r['code_changed'] for r in m),'level_changed',sum(r['level_changed'] for r in m),'core_changed',sum(r['core_changed'] for r in m))
