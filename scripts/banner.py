"""프로필 맨 위 픽셀 배너(라이트/다크)를 그린다. 바꿀 일이 있을 때만 손으로 돌린다."""
F = {'B': ["1110", "1001", "1001", "1110", "1001", "1001", "1110"],
     'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
     'S': ["0111", "1000", "1000", "0110", "0001", "0001", "1110"],
     'I': ["111", "010", "010", "010", "010", "010", "111"],
     'D': ["1110", "1001", "1001", "1001", "1001", "1001", "1110"],
     'E': ["1111", "1000", "1000", "1110", "1000", "1000", "1111"]}
HEART = ["0110110", "1111111", "1111111", "0111110", "0011100", "0001000"]
P, HP = 14, 10  # 글자 픽셀, 하트 픽셀
W, H = 900, 240


def svg(bg, fg, acc, shadow, text, sub):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges">',
           f'<rect width="{W}" height="{H}" fill="{bg}"/>',
           f'<rect x="14" y="14" width="{W - 22}" height="{H - 22}" fill="{shadow}"/>',
           f'<rect x="8" y="8" width="{W - 22}" height="{H - 22}" fill="{bg}" stroke="{fg}" stroke-width="4"/>']
    word = "BYSIDE"
    letters = sum(len(F[c][0]) for c in word) * P + (len(word) - 1) * P
    heart = len(HEART[0]) * HP
    gap = 2 * P
    x = (W - 8 - (heart + gap + letters)) // 2 + 4
    y = 44
    for r, row in enumerate(HEART):
        for c, v in enumerate(row):
            if v == '1':
                out.append(f'<rect x="{x + c * HP}" y="{y + 18 + r * HP}" width="{HP}" height="{HP}" fill="{acc}"/>')
    x += heart + gap
    for ch in word:
        for r, row in enumerate(F[ch]):
            for c, v in enumerate(row):
                if v == '1':
                    out.append(f'<rect x="{x + c * P + 4}" y="{y + r * P + 4}" width="{P}" height="{P}" fill="{shadow}"/>')
                    out.append(f'<rect x="{x + c * P}" y="{y + r * P}" width="{P}" height="{P}" fill="{fg}"/>')
        x += (len(F[ch][0]) + 1) * P
    font = 'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" text-anchor="middle"'
    out.append(f'<text x="{(W - 8) // 2 + 4}" y="178" {font} font-size="22" font-weight="800" fill="{text}">기획부터 디자인·개발·출시까지, 혼자 만드는 앱 스튜디오</text>')
    out.append(f'<text x="{(W - 8) // 2 + 4}" y="206" {font} font-size="15" font-weight="600" fill="{sub}" letter-spacing="2">SOLO APP STUDIO · iOS &amp; ANDROID</text>')
    out.append('</svg>')
    return '\n'.join(out)


open('banner-light.svg', 'w').write(svg('#FBF6EE', '#156B67', '#E0605A', '#E6DCCB', '#3D2B28', '#7A6661'))
open('banner-dark.svg', 'w').write(svg('#151817', '#7FD1C9', '#F07A72', '#2C3230', '#F2ECE6', '#B3A8A1'))
