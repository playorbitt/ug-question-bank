import json,re
W='/tmp/claude-0/-home-claude/e92aff11-3822-5985-abba-4ce5ce7b495f/scratchpad/'
d=json.load(open(W+'n24/rows24.json'));rows=d['rows']
O={ # code: (domain, level, core, competency, n_cert)
'BC8.3':('K','KH','Y','Describe the types and causes of protein energy malnutrition and its effects.',''),
'PH8.1':('K','KH','Y','Discuss general principles of chemotherapy with emphasis on antimicrobial resistance.',''),
'PH8.2':('K','KH','Y','Discuss rational use of antimicrobials and describe antibiotic stewardship program of your institute',''),
'PH8.3':('K','KH','Y','Explain the kinetics, dynamics, adverse effects, indications of the following antibacterial drugs: Sulphonamides Quinolones, Beta-lactams, Macrolides, Tetracyclines, Aminoglycosides, and newer antibacterial drugs',''),
'PH8.4':('K/A/C','KH/SH','Y','Devise a pharmacotherapeutic plan for UTI and STDs and explain to patient the instructions and adherence to treatment.',''),
'PH8.5':('K','KH/SH','Y','Explain the types, kinetics, dynamics, therapeutic uses and adverse effects of drugs used in tuberculosis. Devise management plan for tuberculosis treatment in various categories.',''),
'PH8.6':('K','KH','Y','Discuss the types, Kinetics, dynamics, adverse effects for drugs used for Leprosy and outline management of Lepra reactions',''),
'PH8.7':('K','KH','Y','Discuss the types, Kinetics, dynamics, adverse effects of drugs used for following Protozoal / Vector borne diseases: Amoebiasis, Kala-azar, Malaria, Filariasis',''),
'PH8.8':('K','KH','Y','Explain the types, kinetics, dynamics, adverse effects of drugs used for fungal infections',''),
'PH8.9':('K','KH','Y','Discuss the types, kinetics, dynamics, adverse effects of drugs used for Intestinal Helminthiasis',''),
'PH10.4':('K','KH/SH','Y','Describe parts of a correct, rational and legible prescription and write rational prescriptions for the provided condition. (examples of conditions to be used are given with other relevant competencies)','5'),
'PH10.5':('K','KH','Y','Identify and apply the legal and ethical regulation of prescribing drugs especially when prescribing for controlled drugs, off-label medicines, and prescribing for self, close family and friends',''),
'PH10.6':('K/S','KH','Y','Perform a critical appraisal of a given prescription and suggest ways to improve it',''),
'PH10.7':('K','KH/SH','N','Describe Pharmacogenomics and Pharmacoeconomics and manage genomic & economic issues in drug use and find out the price of given medication(s).',''),
'PH10.8':('K','KH/SH','Y','Describe Essential medicines, Fixed dose combination, Over the counter drugs and explain steps to choose essential medicines.',''),
'PH10.9':('K/S','SH','Y','Calculate the dosage of drugs for an individual patient, including children, elderly, pregnant and lactating women and patients with renal or hepatic dysfunction.','1'),
'PH10.10':('K','KH','N','Identify when therapeutic drug monitoring is considered for a particular patient, determine timing of sampling and calculate revised dose.',''),
'PH10.11':('K','KH/SH','Y','Identify and apply drug Regulations principles, acts and legal aspects related of drug discovery and clinical use',''),
'PH10.12':('K/A','KH','Y','Describe overview of drug development including phases of clinical trials and Good Clinical Practice & reflect on the role of research in developing new drugs',''),
'MI10.1':('K','K','Y','Enumerate different causative agents and the types of Healthcare-Associated Infections (HAI). Define HAI and describe the chain of transmission and its role in preventing HAI.',''),
'MI10.5':('K','KH','Y','Describe the commonly detected drug-resistant microbes in HAI. Explain the mechanism of evolution, spread, and control of antimicrobial drug resistance in hospitalized patients.',''),
'GM1.22':('K','KH','','Describe and discuss the pharmacology of drugs including indications, contraindications in the management of heart failure including diuretics, ACE inhibitors, Beta blockers, aldosterone antagonists and cardiac glycosides',''),
'GM1.26':('S','SH','','Elicit document and present an appropriate history, demonstrate correctly general examination, relevant clinical findings and formulate document and present a management plan for an adult patient presenting with a common form of congenital heart disease',''),
'GM2.11':('S','SH','','Order and interpret a Chest X-ray and markers of acute myocardial Infarction','3'),
'GM2.12':('S','SH','','Choose and interpret a lipid profile and identify the desirable lipid profile in the clinical context',''),
'GM11.5':('UNK','UNK','','Describe and discuss the pathogenesis and temporal evolution of microvascular and macrovascular complications of diabetes',''),
'GM13.11':('S','K','','Order and interpret diagnostic testing based on the clinical diagnosis in a cancer patient. Including CBC and stool occult blood and prostate specific antigen',''),
'MI1.12':('K','KH','Y','Classify and describe the different methods of sterilization and disinfection. Discuss the mechanism of action, application and quality control of different methods in the laboratory and in clinical and surgical practices.',''),
'GM3.14':('K','KH','Y','Describe and enumerate the indications for further testing including HRCT, Viral cultures, PCR and specialized testing',''),
'GM4.19':('S','SH','Y','Develop an appropriate empiric treatment plan based on the patient’s clinical and Immune status pending definitive diagnosis',''),
'GM27.10':('S','SH','Y','Interpret a sputum gram stain and AFB with antibiotic sensitivity test from a given report',''),
'OR1.5':('K/S/A/C','SH','Y','Participate as a member in the team for closed reduction of shoulder dislocation / hip dislocation / knee dislocation and dislocation of finger joints,',''),
}
PAGE={'MI1.12':681,'GM3.14':761,'GM4.19':763,'GM27.10':796,'BC8.3':640,'PH10.6':658,'PH10.10':658,'MI10.1':687,'MI10.5':687,'GM1.22':757,'GM1.26':757,'GM2.11':758,'GM2.12':759,'GM11.5':774,'GM13.11':777,'OR1.5':918}
POL=re.compile(r'\b(?:LGT|SGT|SDL|CBL|PBL)s?\b[,/ ]*|\bFlipped(?: class)?\b[,/ ]*|\bcase studies\b[,/ ]*|\bBedside\s*(?:clinic)?[,/ ]*|\bWritten\b[,/ ]*|\bViva(?: voce)?\b[,/ ]*|\bSkill assessment\b[,/ ]*|\bDOAP\b(?! of)[,/ ]*|(?<=[,/ ])Case\b[,/ ]*',re.I)
out=[];seen=set()
for r in rows:
    c=r['code']
    r['qc']=[]
    if c in O:
        dom,lev,core,txt,n=O[c]
        r.pop('parse_failed',None);r.pop('raw',None);r.pop('pending',None)
        r.update({'domain':dom,'level':lev,'core':core,'competency':txt,'n_procedures_to_certify':n or r.get('n_procedures_to_certify','')})
        r.setdefault('teaching_learning','');r.setdefault('assessment','')
        r['qc'].append('manual_transcription')
        if core=='': r['qc'].append('core_blank_in_source')
        if c=='GM13.11': r['qc'].append('core_typo_in_source(K)')
    elif r.get('parse_failed'):
        continue
    elif re.search(r'\b(LGT|SGT|DOAP|Written|Viva|SDL|Flipped)\b',r['competency']) and not (c in('FM8.5','GM9.4')):
        t=POL.sub(' ',r['competency']); t=re.sub(r'\s+',' ',t); t=re.sub(r'(\w)- (?=[a-z])',r'\1-',t).strip()
        r['competency']=t; r['qc'].append('text_cleaned_column_bleed')
    if r.get('domain')=='UNK' or r.get('level')=='UNK':
        if c not in O: r['qc'].append('domain_level_unreadable')
    if c in PAGE: r['page']=PAGE[c]
    out.append(r)
json.dump({'rows':out,'tot':d['tot']},open(W+'n24/rows24_fixed.json','w'))
print(len(out),len({x['code'] for x in out}))
for x in out:
    if 'text_cleaned_column_bleed' in x['qc'] : print(x['code'],'|',x['competency'][:200])
print([ (x['code'],x['domain'],x['level']) for x in out if 'domain_level_unreadable' in x['qc']])
