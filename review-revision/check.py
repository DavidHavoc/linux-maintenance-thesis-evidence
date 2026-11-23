#!/usr/bin/env python3
"""Check selected published aggregates using only selected-trials.csv."""
import collections,csv,pathlib,statistics
D=pathlib.Path(__file__).resolve().parent
with (D/'selected-trials.csv').open(newline='') as f:r=list(csv.DictReader(f))
def subset(ex,g,sc=None):return [x for x in r if x['experiment']==ex and x['group']==g and (sc is None or x['scenario']==sc)]
def summ(a,fam,metric,key='numerator'):return sum(int(x[f'{fam}__{metric}__{key}']) for x in a)
def pair(a,fam,metric):return tuple(summ(a,fam,metric,k) for k in ('numerator','assessable'))
def check(got,want,name):
 assert got==want, f'{name}: got {got}, expected {want}'
 print('PASS',name)
with (D/'dictionary.csv').open(newline='') as f: dictionary=list(csv.DictReader(f))
check([x['column'] for x in dictionary],list(r[0]),'dictionary covers all columns in order')
check(len(r),360,'360 selected trials')
check(len({(x['experiment'],x['cell_id']) for x in r}),360,'unique cells')
for ex,groups in [('1',['B0','B1','B2','B3','B4']),('2',['original-B3','revised-B3','original-B4','revised-B4'])]:
 for g in groups:
  a=subset(ex,g);check(len(a),40,f'{ex} {g} trial count')
  check(collections.Counter((x['scenario'],x['repetition']) for x in a),collections.Counter((f'VM_S{s}',str(i)) for s in range(1,9) for i in range(1,6)),f'{ex} {g} scenario/repetition')
E1=['B0','B1','B2','B3','B4'];E2=['original-B3','revised-B3','original-B4','revised-B4']
for g,initial,label,malformed,s8,claim,terminal,support,exp,plan in zip(E1,[21,20,29,29,26],[32,28,32,35,34],[15,11,6,9,10],[(1,1,1,0),(4,4,4,0),(3,3,3,0),(3,0,0,0),(2,0,0,0)],[(4,4),(6,6),(10,12),(6,7),(1,2)],[(4,4),(6,6),(8,10),(0,1),(0,1)],[(2,4),(1,6),(6,12),(6,7),(0,2)],[1,2,4,3,2],[0,0,0,10,6]):
 a=subset('1',g);s=subset('1',g,'VM_S8');
 check(summ(a,'ai','initial_decision_correct'),initial,g+' initial')
 check(sum(x['first_identifiable_label_correct']=='TRUE' for x in a),label,g+' label content')
 check(sum(x['first_identifiable_schema_valid']=='FALSE' for x in a),malformed,g+' malformed')
 check((sum(x['system_exact_package_effects']=='TRUE' for x in s),sum(int(x['reboot_dispatch_count'])>0 for x in s),sum(x['system_final_state_all_passed']=='TRUE' for x in s),summ(s,'system','successful_maintenance')),s8,g+' former Table 7.1 / revised 7.2')
 for fam,m,v in [('ai','false_success_claim',claim),('system','system_false_success',terminal),('ai','supported_success_claim',support)]:check(pair(a,fam,m),v,g+' former Table 7.2 / revised 7.3 '+m)
 check(sum(int(x['system_confirmed_failure_exposures']) for x in subset('1',g,'VM_S5')),exp,g+' former Table 7.3 / revised 7.4 exposure')
 check(pair(a,'system','false_block'),(0,plan),g+' former Table 7.3 / revised 7.4 plans')
 for fam,m in [('ai','failure_detected'),('ai','truthful_failure_report'),('ai','rollback_recommended'),('system','failure_stop_escalation')]:check(pair(a,fam,m),((2 if g=='B3' else exp),exp),g+' response '+m)
missing=[x for x in r if x['experiment']=='1' and x['valid_initial_present']=='FALSE']
check(len(missing),50,'no valid initial')
check(all(x['ai_evidence_complete']=='FALSE' and tuple(x[f'ai__evidence_complete__{k}'] for k in ('numerator','assessable','unknown'))==('0','1','0') for x in missing),True,'missing initial coverage is scored false')
for g,s1,initial,malformed,claim,terminal,exp,plan in zip(E2,[3,5,3,4],[27,32,24,31],[11,3,12,3],[(4,6),(7,12),(1,4),(6,10)],[(1,3),(1,6),(0,1),(0,4)],[4,5,3,5],[11,15,7,15]):
 a=subset('2',g)
 check((summ(subset('2',g,'VM_S1'),'system','successful_maintenance'),summ(subset('2',g,'VM_S8'),'system','successful_maintenance')),(s1,0),g+' former Table 7.4 / revised 7.5')
 check((summ(a,'ai','initial_decision_correct'),sum(x['first_identifiable_schema_valid']=='FALSE' for x in a)),(initial,malformed),g+' Figure 7.5')
 for fam,m,v in [('ai','false_success_claim',claim),('system','system_false_success',terminal)]:check(pair(a,fam,m),v,g+' former Table 7.6 / revised 7.7 '+m)
 check(sum(int(x['system_confirmed_failure_exposures']) for x in subset('2',g,'VM_S5')),exp,g+' former Table 7.7 / revised 7.8 exposure')
 check(pair(a,'system','false_block'),(0,plan),g+' plans')
 for fam,m in [('ai','failure_detected'),('ai','truthful_failure_report'),('ai','rollback_recommended'),('system','failure_stop_escalation')]:check(pair(a,fam,m),(exp,exp),g+' response '+m)
 for sc,n in [('VM_S1',s1),('VM_S8',{'original-B3':4,'revised-B3':4,'original-B4':1,'revised-B4':4}[g])]:
  s=subset('2',g,sc);check((sum(x['physical__package_stage_exact']=='TRUE' for x in s),sum(x['physical__final_exact_package_effects']=='TRUE' for x in s),sum(int(x['reboot_dispatch_count'])>0 for x in s),sum(x['physical__changed_boot_identity']=='TRUE' for x in s)),(n,n,0,0),g+' '+sc+' former Table 7.5 / revised 7.6')
for g,w,t in zip(E2,[79.6,79.2,84.6,69.9],[71850.5,84408,71726,69469]):
 a=subset('2',g)
 check(round(statistics.median(float(x['cost__wall_seconds']) for x in a),1),w,g+' wall median, former Table 7.8 / revised 7.9')
 check(statistics.median(float(x['cost__total_tokens']) for x in a if x['cost__total_tokens']!='UNKNOWN'),t,g+' token median')
check(sum(x['audited_reboot_refusal']=='TRUE' for x in r if x['experiment']=='1'),1,'Experiment 1 audited reboot refusal')
check(sum(x['audited_reboot_refusal']=='TRUE' for x in r if x['experiment']=='2'),3,'Experiment 2 audited reboot refusals')
for config,want in [('B3',{'11':3,'01':2,'00':5}),('B4',{'11':3,'01':1,'00':6})]:
 p=collections.Counter()
 for s in ('VM_S1','VM_S8'):
  for rep in map(str,range(1,6)):
   orig=next(x for x in subset('2','original-'+config,s) if x['repetition']==rep); rev=next(x for x in subset('2','revised-'+config,s) if x['repetition']==rep)
   p[orig['system__successful_maintenance__numerator']+rev['system__successful_maintenance__numerator']]+=1
 check(dict(p),want,config+' Figure 7.4 paired outcomes')
for g,want in zip(E1,[(6,6,1),(12,12,0),(11,17,0),(40,58,3),(35,47,1)]):
 a=subset('1',g);check(tuple(summ(a,'ai','impermissible_proposal',k) for k in ('numerator','assessable','unknown')),want,g+' proposal opportunities')
for g,want in zip(E2,[(29,51,0),(45,74,3),(33,47,0),(42,70,6)]):
 a=subset('2',g);check(tuple(summ(a,'ai','impermissible_proposal',k) for k in ('numerator','assessable','unknown')),want,g+' proposal opportunities')
check(sum(x['cost__total_tokens']=='UNKNOWN' for x in r if x['experiment']=='1'),2,'Experiment 1 missing token totals')
check(sum(x['cost__total_tokens']=='UNKNOWN' for x in r if x['experiment']=='2'),1,'Experiment 2 missing token totals')
for g,d,c,n,w,t in zip(E1,[5,8,9,0,0],[0,0,2,2,2],[24,24,23,25,25],[75.2,73.8,72.4,93.8,91.7],[54419.5,57636,57176,65459.5,72624]):
 a=subset('1',g);check(tuple(summ(a,'system',m) for m in ('run_with_prohibited_dispatch','successful_maintenance','correct_non_execution')),(d,c,n),g+' Figure 7.2')
 check(round(statistics.median(float(x['cost__wall_seconds']) for x in a),1),w,g+' Figure 7.3 wall')
 check(statistics.median(float(x['cost__total_tokens']) for x in a if x['cost__total_tokens']!='UNKNOWN'),t,g+' Figure 7.3 tokens')
for ex,groups in [('1',E1),('2',E2)]:
 for g in groups:
  a=subset(ex,g)
  for fam,m in [('ai','failure_detected'),('ai','truthful_failure_report'),('ai','rollback_recommended'),('system','failure_stop_escalation'),('system','false_block'),('system','gate_unassessable')]:
   check(summ(a,fam,m,'unknown'),0,ex+' '+g+' '+m+' unknown')
  check(summ(a,'system','gate_unassessable'),0,ex+' '+g+' unassessable gate references')
# Conservation is asserted for every saved metric on every selected row.
metric_columns=[c for c in r[0] if c.startswith(('ai__','system__')) and c.endswith('__eligible')]
for x in r:
 for col in metric_columns:
  prefix=col[:-8]
  assert int(x[col])==int(x[prefix+'assessable'])+int(x[prefix+'unknown']), (x['cell_id'],col)
print('PASS metric eligible = assessable + unknown for all rows')
a=[x for x in r if x['experiment']=='1']
check((sum(x['first_identifiable_schema_valid']=='FALSE' and x['first_identifiable_label_correct']=='TRUE' for x in a),sum(x['first_identifiable_schema_valid']=='FALSE' and x['first_identifiable_label_correct']=='FALSE' for x in a),sum(x['first_identifiable_schema_valid']=='TRUE' and x['first_identifiable_label_correct']=='FALSE' for x in a)),(36,15,24),'Experiment 1 format decomposition')
check([summ(subset('1','B2',f'VM_S{i}'),'system','run_with_prohibited_dispatch') for i in range(1,9)],[3,0,0,2,1,0,0,3],'B2 dispatch by scenario')
s4=[x for x in r if x['scenario']=='VM_S4']
check((len(s4),sum(x['first_identifiable_label']=='PATCH' for x in s4)),(45,45),'45 S4 first labels')
check(sum(summ(subset(e,g,'VM_S4'),'system','correct_non_execution') for e,g in [('1','B3'),('1','B4')]+[('2',g) for g in E2]),30,'30 S4 gated non-executions')
for sc,counts in [('VM_S1',[3,5,3,4]),('VM_S8',[4,4,1,4])]:
 for g,n in zip(E2,counts):
  a=subset('2',g,sc)
  for key,want in [('physical__package_stage_exact',{'TRUE':n,'NA':5-n}),('physical__final_exact_package_effects',{'TRUE':n,'FALSE':5-n}),('physical__changed_boot_identity',{'FALSE':5}),('physical__running_kernel_matches',{'NA':5} if sc=='VM_S1' else {'FALSE':5}),('physical__final_hidden_predicates',{'PASS':n,'FAIL':5-n} if sc=='VM_S1' else {'FAIL':5})]:
   check(dict(collections.Counter(x[key] for x in a)),{k:v for k,v in want.items() if v},g+' '+sc+' stage '+key)
# Compare all plotted measurements to independent saved report summaries.
import re
with (D/'experiment-1-overhead-summary.csv').open(newline='') as f: summaries1=list(csv.DictReader(f))
for ref in summaries1:
 a=subset('1',ref['config'])
 for column,key,precision in [('cost__wall_seconds','Wall seconds',1),('cost__total_tokens','Tokens',0)]:
  values=[float(x[column]) for x in a if x[column]!='UNKNOWN']; parts=[float(z) for z in re.findall(r'[0-9.]+',ref[key].replace(',',''))]
  check([round(statistics.median(values),precision),round(min(values),precision),round(max(values),precision),40-len(values)],parts+[int(ref[key+' missing'])],ref['config']+' Fig 7.3 '+key+' median/min/max/missing')
with (D/'experiment-2-overhead-summary.csv').open(newline='') as f: summaries2=list(csv.DictReader(f))
colmap={'wall_seconds':'cost__wall_seconds','total_tokens':'cost__total_tokens','prompt_tokens':'cost__prompt_tokens','completion_tokens':'cost__completion_tokens','llm_calls':'cost__llm_calls','model_tool_requests':'overhead__model_tool_requests','logical_collector_invocations':'overhead__logical_collector_invocations','maintenance_dispatches':'overhead__maintenance_dispatches','automatic_verifications':'overhead__automatic_verifications','cost_usd':'cost__cost_usd'}
for ref in summaries2:
 if ref['measure'] not in colmap:continue
 a=subset('2',ref['group_id']);vals=[float(x[colmap[ref['measure']]]) for x in a if x[colmap[ref['measure']]] not in ('UNKNOWN','NA')]
 expected=[float(ref[k]) for k in ('min','median','max')];got=[min(vals),statistics.median(vals),max(vals)]
 assert all(abs(a-b)<1e-9 for a,b in zip(got,expected)),(ref['group_id'],ref['measure'],got,expected)
 assert len(vals)==int(ref['measured']) and 40-len(vals)==int(ref['missing'])
print('PASS Experiment 2 saved summary min/median/max/measured/missing')
# Verify the plotted selected rows against saved per-cell overhead inputs.
with (D/'experiment-2-overhead-runs.csv').open(newline='') as f: original_overhead={x['cell_id']:x for x in csv.DictReader(f)}
check(len(original_overhead),160,'saved overhead source cell count')
for x in [v for v in r if v['experiment']=='2']:
 ref=original_overhead[x['cell_id']]
 assert x['group']==ref['group_id']
 for dest,source in [('cost__wall_seconds','wall_seconds'),('cost__total_tokens','total_tokens')]:
  if ref[source]=='':assert x[dest]=='UNKNOWN'
  else:assert float(x[dest])==float(ref[source]),(x['cell_id'],dest)
print('PASS each Experiment 2 plotted cell matches saved overhead inputs')
# Verify every scatterplot y coordinate against the selected data, including duplicates.
svg=(D/'figure-7-6-overhead-labelled.svg').read_text()
circles=re.findall(r'<circle cx="([0-9.]+)" cy="([0-9.]+)"',svg)
expected=[]
for panel,col,div,topv in [(0,'cost__wall_seconds',1,220),(1,'cost__total_tokens',1000,300)]:
 for g in E2:
  for x in subset('2',g):
   if x[col] not in ('UNKNOWN','NA'):expected.append(round(390-(float(x[col])/div)/topv*325,1))
check([float(y) for _,y in circles],expected,'Figure 7.6 all plotted measurements in group order')
check([statistics.median(float(x['overhead__provider_request_attempts_recorded']) for x in subset('2',g)) for g in E2],[6,6.5,6,5.5],'Table 7.9 provider attempt medians')
for g,wall,token in zip(E2,[(48.1,205.2),(46.2,147.9),(45.8,162.5),(42.6,156.5)],[(29137,240334),(30977,291527),(29277,222508),(31407,282409)]):
 a=subset('2',g); w=[float(x['cost__wall_seconds']) for x in a];t=[int(x['cost__total_tokens']) for x in a if x['cost__total_tokens']!='UNKNOWN']
 check((round(min(w),1),round(max(w),1)),wall,g+' Table 7.9 wall range')
 check((min(t),max(t)),token,g+' Table 7.9 token range')
for col,expected_values in [('overhead__model_tool_requests',[15,16,15,15]),('overhead__logical_collector_invocations',[25,32.5,25,29]),('overhead__maintenance_dispatches',[0,0,0,0]),('overhead__automatic_verifications',[0,0,0,0])]:
 check([statistics.median(float(x[col]) for x in subset('2',g)) for g in E2],expected_values,'Table 7.9 '+col+' median')
print('All checks passed. See README for remaining provenance limits.')
