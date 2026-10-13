# Scan nearby wifi (NetworkManager) into networks.json. Run: python scan.py
import json, subprocess
out = subprocess.run(['nmcli', '-t', '-f', 'SIGNAL,SECURITY,SSID', 'dev', 'wifi', 'list', '--rescan', 'yes'],
                     capture_output=True, text=True, check=True).stdout
best = {}
for line in out.splitlines():
    sig, sec, ssid = line.split(':', 2)
    ssid = ssid.replace('\\:', ':').strip()
    if ssid and 'BinusWifi-Staff' not in ssid and int(sig) > best.get(ssid, (0,))[0]:
        best[ssid] = (int(sig), bool(sec))
nets = [{'name': n, 'bars': max(1, min(4, -(-s // 25))), 'lock': int(l)} for n, (s, l) in sorted(best.items(), key=lambda x: -x[1][0])]
json.dump(nets, open('networks.json', 'w'), ensure_ascii=False, indent=1)
print(len(nets), 'networks')
