# usage: python3 upload.py targets.json file1 file2 ...  (targets in same order)
import json, subprocess, sys
t = json.load(open(sys.argv[1]))['data']['stagedUploadsCreate']['stagedTargets']
for tgt, f in zip(t, sys.argv[2:]):
    args = ['curl', '-sS', '-o', '/dev/null', '-w', '%{http_code}', '-X', 'POST', tgt['url']]
    for p in tgt['parameters']:
        args += ['-F', f"{p['name']}={p['value']}"]
    args += ['-F', f'file=@{f};type=text/plain']
    code = subprocess.run(args, capture_output=True, text=True).stdout
    print(code, f, '->', tgt['resourceUrl'])
