"""Generate public/questions.json from data/competencies.jsonl (run from repo root)."""
import json
rows=[json.loads(l) for l in open('data/competencies.jsonl')]
rows=[r for r in rows if 'spurious_subject' not in r['qc_flags']]
LV={'K':'Knows','KH':'Knows how','S':'Shows','SH':'Shows how','P':'Performs'}
qs=[];i=0
for r in rows:
    t=r['competency_text'].strip().rstrip('.'); t=t[0].upper()+t[1:]
    if r['n_words']<3: t='Discuss '+t[0].lower()+t[1:]  # title-only competencies (e.g. 'Laparoscopy')
    kinds=[]
    if r['as_written']: kinds.append(('Written',t+'.'))
    if r['as_viva']: kinds.append(('Viva','Viva: '+t+'.'))
    if r['as_skill_assessment'] or r['tl_doap'] or r['level_max'] in('SH','P','S'): kinds.append(('Practical/Skill','Skill station: '+t+'.'))
    if not kinds: kinds.append(('Written',t+'.'))
    for k,q in kinds:
        i+=1
        qs.append({'id':f"Q{i:05d}",'code':r['code'],'subj':r['subject_code'],'subject':r['subject'].title(),'topic':r['topic'],'type':k,'q':q,'level':r['level_max'],'levelName':LV[r['level_max']],'domains':r['domains'],'core':r['core'],'tl':r['teaching_learning'],'int':r['horizontal_integration'] if len(r['horizontal_integration'])<80 else '','vol':r['source_volume'],'page':r['source_page']})
json.dump(qs,open('public/questions.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(rows),'competencies ->',len(qs),'questions')
