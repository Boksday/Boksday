"""잔디(기여 달력)를 읽어 픽셀 스타일 통계 카드 SVG를 그린다. 바깥 서비스 없이 Actions에서 돈다."""
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request

USER = os.environ['GH_USER']
TOKEN = os.environ['GH_TOKEN']
OUT = sys.argv[1]

QUERY = '''query($login: String!) { user(login: $login) {
  contributionsCollection { contributionCalendar { totalContributions
    weeks { contributionDays { date contributionCount } } } } } }'''


def fetch():
    body = json.dumps({'query': QUERY, 'variables': {'login': USER}}).encode()
    req = urllib.request.Request('https://api.github.com/graphql', body, {
        'Authorization': f'bearer {TOKEN}', 'User-Agent': 'profile-stats'})
    # GitHub이 가끔 504를 돌려줘서 잠깐 쉬고 다시 묻는다.
    for attempt in range(5):
        try:
            return json.load(urllib.request.urlopen(req, timeout=30))['data']['user']
        except urllib.error.HTTPError as error:
            if error.code < 500 or attempt == 4:
                raise
            time.sleep(10)


def streaks(days):
    """days: 날짜순 (date, count). 오늘 아직 안 했으면 어제까지로 연속 일수를 센다."""
    longest = run = 0
    for _, n in days:
        run = run + 1 if n else 0
        longest = max(longest, run)
    current = 0
    tail = days[:-1] if days and days[-1][1] == 0 else days
    for _, n in reversed(tail):
        if not n:
            break
        current += 1
    return current, longest


THEMES = {
    'light': dict(bg='#FBF6EE', frame='#156B67', shadow='#E6DCCB', text='#3D2B28', sub='#7A6661',
                  accent='#156B67', fire='#E0605A', grass=['#EBE3D6', '#BFE3DF', '#7FC4BD', '#3E9A93', '#156B67']),
    'dark': dict(bg='#151817', frame='#7FD1C9', shadow='#2C3230', text='#F2ECE6', sub='#B3A8A1',
                 accent='#7FD1C9', fire='#F07A72', grass=['#232826', '#1F4A46', '#2E7A73', '#4FB0A7', '#7FD1C9']),
}


def card(stats, recent, t):
    W, H = 900, 250
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         'shape-rendering="crispEdges" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>',
         f'<rect x="14" y="14" width="{W - 22}" height="{H - 22}" fill="{t["shadow"]}"/>',
         f'<rect x="8" y="8" width="{W - 22}" height="{H - 22}" fill="{t["bg"]}" stroke="{t["frame"]}" stroke-width="4"/>']
    for i, (value, label, color) in enumerate(stats):
        cx = 8 + i * (W - 22) // 3 + (W - 22) // 6
        s.append(f'<text x="{cx}" y="78" text-anchor="middle" font-size="44" font-weight="800" fill="{color}">{value}</text>')
        s.append(f'<text x="{cx}" y="108" text-anchor="middle" font-size="16" font-weight="600" fill="{t["sub"]}">{label}</text>')
        if i:
            x = 8 + i * (W - 22) // 3
            s.append(f'<rect x="{x}" y="36" width="4" height="80" fill="{t["shadow"]}"/>')
    # 최근 12주 잔디를 한 줄 픽셀로
    cell, gap = 9, 3
    weeks = [recent[i:i + 7] for i in range(0, len(recent), 7)]
    gx = (W - len(weeks) * (cell + gap)) // 2
    peak = max([n for _, n in recent] + [1])
    for w, week in enumerate(weeks):
        for d, (_, n) in enumerate(week):
            level = 0 if not n else min(4, 1 + int(3 * n / peak))
            s.append(f'<rect x="{gx + w * (cell + gap)}" y="{140 + d * (cell + gap)}" width="{cell}" height="{cell}" fill="{t["grass"][level]}"/>')
    s.append('</svg>')
    return '\n'.join(s)


user = fetch()
cal = user['contributionsCollection']['contributionCalendar']
days = [(d['date'], d['contributionCount']) for w in cal['weeks'] for d in w['contributionDays']]
today = dt.date.today().isoformat()
days = [d for d in days if d[0] <= today]
current, longest = streaks(days)
recent = days[-7 * 26:]
recent = recent[len(recent) % 7:]
for name, t in THEMES.items():
    stats = [(f'{cal["totalContributions"]:,}', '최근 1년 기여', t['accent']),
             (f'{current}일', '🔥 지금 연속', t['fire']),
             (f'{longest}일', '최장 연속', t['accent'])]
    path = os.path.join(OUT, 'stats.svg' if name == 'light' else 'stats-dark.svg')
    open(path, 'w').write(card(stats, recent, t))
print('total', cal['totalContributions'], 'current', current, 'longest', longest)
