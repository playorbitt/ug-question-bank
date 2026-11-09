"""Generate public/questions.json from the 2024 CBME dataset + the 2018-vs-2024 comparison (run from repo root)."""
import json,csv,re
rows=[json.loads(l) for l in open('data/competencies_2024.jsonl')]
chg={}
for r in csv.DictReader(open('data/comparison_2018_vs_2024.csv',encoding='utf-8')):
    if r['code_2024']: chg[r['code_2024']]=r['status']
LABEL={'identical':'Unchanged','minor_edit':'Minor edit','reworded':'Reworded','added_in_2024':'New in 2024'}
LV={'K':'Knows','KH':'Knows how','S':'Shows','SH':'Shows how','P':'Performs'}
WR=re.compile(r'written|tutorial|short note|mcq|essay|application|assignment|question',re.I)
VV=re.compile(r'viva',re.I)
SK=re.compile(r'skill|osce|ospe|log ?book|observation|practical|simulation|checklist|document|scenario|exercise|case|rubric',re.I)
qs=[];i=0
for r in rows:
    if not r['level_max']: lvl,lvn='','Not stated'
    else: lvl,lvn=r['level_max'],LV[r['level_max']]
    t=r['competency_text'].strip().rstrip('.'); t=t[0].upper()+t[1:]
    if len(t.split())<3: t='Discuss '+t[0].lower()+t[1:]
    a=r['assessment']; kinds=[]
    if WR.search(a): kinds.append(('Written',t+'.'))
    if VV.search(a): kinds.append(('Viva','Viva: '+t+'.'))
    if SK.search(a) or lvl in('SH','P','S'): kinds.append(('Practical/Skill','Skill station: '+t+'.'))
    if not kinds: kinds.append(('Written',t+'.'))
    for k,q in kinds:
        i+=1
        qs.append({'id':f"Q{i:05d}",'code':r['code'],'subj':r['subject_code'],'subject':r['subject'],'topic':r['topic'],'type':k,'q':q,'level':lvl,'levelName':lvn,'domains':r['domains'],'core':r['core'] if r['core']!='' else -1,'tl':r['teaching_learning'],'chg':LABEL.get(chg.get(r['code']),'No 2018 match'),'page':r['source_page_pdf']})
json.dump(qs,open('public/questions.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(rows),'competencies ->',len(qs),'questions')
