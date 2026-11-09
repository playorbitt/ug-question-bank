"""Generate public/questions.json (CBME 2024) and public/questions_2018.json (CBME 2018). Run from repo root."""
import json,csv,re
CMP=list(csv.DictReader(open('data/comparison_2018_vs_2024.csv',encoding='utf-8')))
LV={'K':'Knows','KH':'Knows how','S':'Shows','SH':'Shows how','P':'Performs'}
WR=re.compile(r'written|tutorial|short note|mcq|essay|application|assignment|question',re.I)
VV=re.compile(r'viva',re.I)
SK=re.compile(r'skill|osce|ospe|log ?book|observation|practical|simulation|checklist|document|scenario|exercise|case|rubric',re.I)
def stem(t):
    t=t.strip().rstrip('.'); t=t[0].upper()+t[1:]
    return 'Discuss '+t[0].lower()+t[1:] if len(t.split())<3 else t
def kinds(t,assess,lvl,written,viva,skill):
    k=[]
    if written: k.append(('Written',t+'.'))
    if viva: k.append(('Viva','Viva: '+t+'.'))
    if skill or lvl in('SH','P','S'): k.append(('Practical/Skill','Skill station: '+t+'.'))
    return k or [('Written',t+'.')]
def build(rows,prefix,chgmap,srcfn,edition):
    qs=[];i=0
    for r in rows:
        lvl=r['level_max'];t=stem(r['competency_text'])
        if edition==2024:
            a=r['assessment'];ks=kinds(t,a,lvl,bool(WR.search(a)),bool(VV.search(a)),bool(SK.search(a)))
        else:
            ks=kinds(t,'',lvl,r['as_written'],r['as_viva'],r['as_skill_assessment'] or r['tl_doap'])
        for k,q in ks:
            i+=1
            qs.append({'id':f'{prefix}{i:05d}','code':r['code'],'subj':r['subject_code'],'subject':r['subject'],'topic':r['topic'],'type':k,'q':q,'level':lvl,'levelName':LV.get(lvl,'Not stated'),'domains':r['domains'],'core':r['core'] if r['core']!='' else -1,'tl':r['teaching_learning'],'chg':chgmap.get(r['code'],'No match'),'src':srcfn(r)})
    return qs
L24={'identical':'Unchanged','minor_edit':'Minor edit','reworded':'Reworded','added_in_2024':'New in 2024'}
L18={'identical':'Unchanged in 2024','minor_edit':'Minor edit in 2024','reworded':'Reworded in 2024','removed_in_2024':'Removed in 2024'}
c24={r['code_2024']:L24[r['status']] for r in CMP if r['code_2024']}
c18={r['code_2018']:L18[r['status']] for r in CMP if r['code_2018']}
r24=[json.loads(l) for l in open('data/competencies_2024.jsonl')]
r18=[json.loads(l) for l in open('data/competencies_2018.jsonl')]
r18=[r for r in r18 if 'spurious_subject' not in r['qc_flags']]
q24=build(r24,'Q',c24,lambda r:f"2024 PDF p.{r['source_page_pdf']}",2024)
q18=build(r18,'E',c18,lambda r:f"2018 Vol {r['source_volume']}, p.{r['source_page']}",2018)
for n,q in (('questions.json',q24),('questions_2018.json',q18)):
    json.dump(q,open('public/'+n,'w'),ensure_ascii=False,separators=(',',':'))
    print(n,len({x['code'] for x in q}),'competencies ->',len(q),'questions')
