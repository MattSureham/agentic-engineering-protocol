import json,re,subprocess,sys
from pathlib import Path
root=Path.cwd();target='6e39cea8ac46d909709ddaeeda1aa8d2df59ce08'
sys.path.insert(0,str(root/'scripts'));import run_pipeline as p
issue='ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md'
evidence='EVIDENCE/EVIDENCE-20260930T015159Z-scope-attribution-review-round-1.md'
git=lambda *a:subprocess.check_output(['git',*a],text=True).strip()
text=(root/issue).read_text();review=p._parse_latest_review(text,issue)
assert (review.target,review.material_findings,review.disposition,review.reviewer)==(target,5,'CHANGES_REQUIRED','agent:Codex-scope-review-20260930')
assert p._metadata(text,issue)['Status']=='IMPLEMENTING'
handoff=(root/'HANDOFF.md').read_text();heads=re.findall(r'^## (.+)$',handoff,re.M)
assert heads==['Current State','Active Issues','Next Action','Recent Activity','Archived Summary'],heads
next_action=handoff.split('## Next Action\n',1)[1].split('\n## ',1)[0].strip()
assert len(next_action.split('\n\n'))==1 and 'R1–R5' in next_action
old=git('show',target+':HANDOFF.md');history=old.split('## Recent Activity\n',1)[1].lstrip()
assert handoff.rstrip().endswith(history)
context=p._load_context(root);milestone=next(m for m in context.milestones if m.milestone_id=='MILESTONE-20260918T064510Z-prompt-independent-discovery-v1')
state=context.states[milestone.milestone_id]
assert state==p._parse_state(git('show',target+':'+milestone.issue),milestone)
assert (state['state'],state['attempt'],state['target_revision'])==('IN_PROGRESS',3,None)
assert len(p._parse_intervening_registry(context.issue_texts[milestone.milestone_id],milestone.issue))==2
changed=set(git('diff','--name-only',target).splitlines());allowed={'HANDOFF.md','HUMAN_CHECKPOINT.md',issue,evidence}
new=set(git('ls-files','--others','--exclude-standard').splitlines())
assert all(n in allowed or n.startswith('EVIDENCE/scope-attribution-review-round-1/') for n in changed|new),changed|new
links=0
for name in sorted(changed|new):
 path=root/name;assert path.is_file() and not path.is_symlink(),name
 data=path.read_bytes();assert data.endswith(b'\n'),name
 assert not any(line.rstrip(b' \t')!=line for line in data.splitlines()),name
 if path.suffix!='.md':continue
 body=data.decode();fence=None
 for line in body.splitlines():
  match=re.match(r'^ {0,3}('+chr(96)+r'{3,}|~{3,})(.*)$',line)
  if match:
   mark,tail=match.groups()
   if fence is None:fence=mark
   elif mark[0]==fence[0] and len(mark)>=len(fence) and not tail.strip():fence=None
 assert fence is None,name
 for destination in re.findall(r'\]\(([^)]+)\)',body):
  if '://' in destination or destination.startswith(('mailto:','#')):continue
  resolved=(path.parent/destination.split('#',1)[0]).resolve();assert resolved.exists(),(name,destination)
  links+=1
payloads=[json.loads((root/'EVIDENCE/scope-attribution-review-round-1'/n).read_text()) for n in ['primary-results.json','supplemental-results.json']]
rows=[r for payload in payloads for r in payload['probes']]
assert len(rows)==22 and sum(not r['requirement_met'] for r in rows)==11
assert sum(r['actual']=='REFUSED' for r in rows)==9
assert all(r['refusal_no_mutation'] for r in rows if r['actual']=='REFUSED')
for rev in ['47a0cb40684ad8edc1d574eba28ded610ea2ba93','9e8f6b285b8e9f47022c7c3fb4ba67d5341601b3','79063cb2201517567c3a8fe9702fd59ca41e9e5d']:
 subprocess.run(['git','merge-base','--is-ancestor',rev,target],check=True)
print('PASS governance: review=CHANGES_REQUIRED material=5 issue=IMPLEMENTING')
print('PASS HANDOFF: five ordered sections; one bounded Next Action; authored history preserved')
print('PASS pipeline: IN_PROGRESS attempt=3 target=null original state unchanged registry_entries=2')
print('PASS review-only diff; regular files; local file links='+str(links)+'; fences/newlines/trailing whitespace')
print('PASS retained reproductions: 22 scenarios; 11 false advances; 9 no-mutation refusals; 2 positives')
print('PASS accepted intervening commits remain ancestors of immutable target')
