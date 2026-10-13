"""Explicit legacy-layout provenance -> scope -> graph -> historical comparison.

No network, alignment controllers, source imports, or publication. The supplied
workspace is a read-only resource tree except for a fresh private output folder.
"""
import argparse
import json
from pathlib import Path
from scripts.verify_portable_patient_snapshot import main as provenance
from scripts.scope_phase_contract import run as scope
from scripts.portable_phase_multichunk import run as replay
from scripts.portable_phase_snapshot import sha


def compare(old, new, markers):
    if old['markers'] != [r['key'] for r in markers]:
        raise ValueError('marker order mismatch')
    fields=('markers','relevant_names','accepted_observed_pairs','edges',
            'optimistic_connected','strict_connected','phase_established','chunks')
    checks={k:old['summary'][k]==new['summary'][k] for k in fields}
    checks['exact_edges']=old['edges']==new['edges']
    return dict(checks=checks,all_match=all(checks.values()),phase_established=False)


def run(workspace_root, alignment_data, output):
    root=Path(workspace_root).resolve();output=Path(output).absolute()
    if not output.resolve().is_relative_to((root/'data/intermediate').resolve()) or output.exists():
        raise ValueError('fresh private output required')
    output.mkdir(mode=0o700);(output/'INCOMPLETE').touch()
    source=provenance(root,Path(alignment_data).resolve(),output/'provenance')
    contract=source/'journal/contract.json'
    receipt=json.loads((source/'provenance.json').read_text())
    if sha(contract)!=receipt['contract_sha256']:raise ValueError('provenance contract drift')
    scope(contract,receipt['contract_sha256'],output/'scoped')
    replay(output/'scoped/contract.json',output/'replay')
    oldpath=root/'data/intermediate/paired-marker-graph-1791913158725419000/result.json'
    oldhash=receipt['input_hashes'][str(oldpath)]
    if sha(oldpath)!=oldhash:raise ValueError('historical result drift')
    old=json.loads(oldpath.read_text());new=json.loads((output/'replay/result.json').read_text())
    markers=json.loads(contract.read_text())['markers']
    comparison=compare(old,new,markers)
    comparison.update(historical_result_sha256=oldhash,replay_result_sha256=sha(output/'replay/result.json'),
                      provenance_sha256=sha(source/'provenance.json'),scope_receipt_sha256=sha(output/'scoped/receipt.json'),
                      source_contract_sha256=sha(contract),script_sha256=sha(Path(__file__)))
    (output/'comparison.json').write_text(json.dumps(comparison,indent=2))
    if not comparison['all_match']:raise ValueError('historical parity mismatch')
    (output/'INCOMPLETE').unlink()
    print(json.dumps(dict(all_match=True,compared_checks=len(comparison['checks']),phase_established=False)))
    return comparison


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace-root',type=Path,required=True)
    p.add_argument('--alignment-data',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    try:run(a.workspace_root,a.alignment_data,a.output)
    except Exception as e:
        print('WORKFLOW_GATE_FAILED: '+type(e).__name__)
        raise SystemExit(1)
