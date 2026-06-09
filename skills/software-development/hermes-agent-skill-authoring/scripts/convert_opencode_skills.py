import os, re, json

OP = r'C:\Users\scott\.config\opencode\skills'
HM = r'C:\Users\scott\AppData\Local\hermes\skills'

def categorize(name):
    n = name.lower()
    rp = ['reaper','reascript','midi','fxchain']
    ad = ['juce','clap','vst','dsp','audio','daw','faust','neural','mixing','mastering',
          'sound','music','synth','codec','simd','fft','filter','plugin','voice','latent',
          'generative','transformer','source-separation','ambisonic','fpga','rtneural',
          'usb-audio','arm-cortex','lock-free','vocoding','restoration']
    biz = ['business','license','copyright','patent','royalty','tax','grant','billing',
           'subscription','plg','ddex','gumroad','cmrra','socan','cusma','usmca','soproq',
           'sr-ed','factor-canada']
    hw = ['hardware','emc','emi','jtag','power-management','rtos','eurorack','hsm']
    if any(k in n for k in rp): return 'reaper-reascripts'
    if any(k in n for k in ad): return 'audio-dsp'
    if any(k in n for k in biz): return 'business'
    if any(k in n for k in hw): return 'hardware'
    return 'software-development'

ok = 0
fail = 0

for root, dirs, files in os.walk(OP):
    if 'SKILL.md' not in files:
        continue
    path = os.path.join(root, 'SKILL.md')
    name = os.path.basename(root)
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    m = re.match(r'^---\n(.+?)\n---\n(.*)', content, re.DOTALL)
    if not m:
        fail += 1
        continue
    
    fm_raw = m.group(1)
    body = m.group(2)
    
    d = re.search(r'description:\s*(.+?)$', fm_raw, re.MULTILINE)
    if not d:
        d = re.search(r'description:\s*>\s*\n((?:\s+.+?\n)+)', fm_raw)
    desc = d.group(1).strip().replace('\n', ' ') if d else name.replace('-', ' ').title()
    desc = re.sub(r'\s+', ' ', desc).strip()
    
    cat = categorize(name)
    tags = [name.replace('-', ' ').title(), 'opencode-migrated']
    
    hermes_lines = []
    hermes_lines.append('---')
    hermes_lines.append('name: ' + name)
    hermes_lines.append('description: "' + desc + '"')
    hermes_lines.append('version: 1.0.0')
    hermes_lines.append('author: OpenCode (migrated to Hermes)')
    hermes_lines.append('license: MIT')
    hermes_lines.append('metadata:')
    hermes_lines.append('  hermes:')
    hermes_lines.append('    tags: ' + json.dumps(tags))
    hermes_lines.append('    related_skills: []')
    hermes_lines.append('---')
    hermes_lines.append('')
    hermes_lines.append(body)
    
    target_dir = os.path.join(HM, cat, name)
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, 'SKILL.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(hermes_lines))
    ok += 1

print('Converted %d skills, %d failed' % (ok, fail))
