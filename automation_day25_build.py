import os, subprocess, textwrap, tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT

OUT = "Day_25_Editorials.pdf"

cpp_2021 = r'''#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    long long x;
    cin >> n >> x;
    vector<long long> a(n);
    for (auto& v : a) cin >> v;
    sort(a.begin(), a.end());

    vector<int> cnt(n + 1);
    int p = 0;

    for (int mex = 0; mex <= n; ++mex) {
        while (p < n && a[p] <= mex) {
            ++cnt[a[p] % x];
            ++p;
        }

        int r = mex % x;
        if (cnt[r] == 0) {
            cout << mex << '\n';
            return;
        }
        --cnt[r];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) solve();
}'''

py_2021 = r'''def solve():
    n, x = map(int, input().split())
    a = sorted(map(int, input().split()))

    cnt = [0] * (n + 1)
    p = 0

    for mex in range(n + 1):
        while p < n and a[p] <= mex:
            cnt[a[p] % x] += 1
            p += 1

        r = mex % x
        if cnt[r] == 0:
            print(mex)
            return
        cnt[r] -= 1

for _ in range(int(input())):
    solve()'''

cpp_2023 = r'''#include <bits/stdc++.h>
using namespace std;
using ll = long long;

void solve() {
    int n;
    cin >> n;

    vector<ll> a(n + 1), pref(n + 1);
    vector<int> b(n + 1);

    for (int i = 1; i <= n; ++i) {
        cin >> a[i];
        pref[i] = pref[i - 1] + a[i];
    }
    for (int i = 1; i <= n; ++i) cin >> b[i];

    const ll INF = (1LL << 62);
    vector<ll> dist(n + 1, INF);
    priority_queue<pair<ll, int>,
                   vector<pair<ll, int>>,
                   greater<pair<ll, int>>> pq;

    dist[1] = 0;
    pq.push({0, 1});

    while (!pq.empty()) {
        auto [d, v] = pq.top();
        pq.pop();

        if (d != dist[v]) continue;

        if (v > 1 && d < dist[v - 1]) {
            dist[v - 1] = d;
            pq.push({d, v - 1});
        }

        ll nd = d + a[v];
        if (nd < dist[b[v]]) {
            dist[b[v]] = nd;
            pq.push({nd, b[v]});
        }
    }

    ll ans = 0;
    for (int i = 1; i <= n; ++i) {
        ans = max(ans, pref[i] - dist[i]);
    }
    cout << ans << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) solve();
}'''

py_2023 = r'''import heapq

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))
    b = [0] + list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + a[i]

    inf = 10**30
    dist = [inf] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]

    while pq:
        d, v = heapq.heappop(pq)
        if d != dist[v]:
            continue

        if v > 1 and d < dist[v - 1]:
            dist[v - 1] = d
            heapq.heappush(pq, (d, v - 1))

        nd = d + a[v]
        if nd < dist[b[v]]:
            dist[b[v]] = nd
            heapq.heappush(pq, (nd, b[v]))

    ans = 0
    for i in range(1, n + 1):
        ans = max(ans, pref[i] - dist[i])

    print(ans)

for _ in range(int(input())):
    solve()'''

cpp_1941 = r'''#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, m;
    cin >> n >> m;

    vector<vector<int>> g(n + 1);
    map<int, int> id;

    for (int i = 0; i < m; ++i) {
        int u, v, c;
        cin >> u >> v >> c;

        auto [it, inserted] = id.emplace(c, -1);
        if (inserted) {
            it->second = (int)g.size();
            g.push_back({});
        }

        int node = it->second;
        g[u].push_back(node);
        g[node].push_back(u);
        g[v].push_back(node);
        g[node].push_back(v);
    }

    int s, t;
    cin >> s >> t;

    vector<int> dist(g.size(), -1);
    queue<int> q;
    dist[s] = 0;
    q.push(s);

    while (!q.empty()) {
        int v = q.front();
        q.pop();

        for (int to : g[v]) {
            if (dist[to] != -1) continue;
            dist[to] = dist[v] + 1;
            q.push(to);
        }
    }

    cout << dist[t] / 2 << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) solve();
}'''

py_1941 = r'''from collections import deque

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n + 1)]
    ids = {}

    for _ in range(m):
        u, v, c = map(int, input().split())

        if c not in ids:
            ids[c] = len(g)
            g.append([])

        node = ids[c]
        g[u].append(node)
        g[node].append(u)
        g[v].append(node)
        g[node].append(v)

    s, t = map(int, input().split())

    dist = [-1] * len(g)
    dist[s] = 0
    q = deque([s])

    while q:
        v = q.popleft()

        for to in g[v]:
            if dist[to] != -1:
                continue
            dist[to] = dist[v] + 1
            q.append(to)

    print(dist[t] // 2)

for _ in range(int(input())):
    solve()'''

sample_2021 = """3
6 3
0 3 2 1 5 2
6 2
1 3 4 1 0 2
4 5
2 5 10 3
"""
out_2021 = "4\n6\n0"

sample_2023 = """4
2
15 16
2 1
5
10 10 100 100 1000
3 4 1 1 1
3
100 49 50
3 2 2
4
100 200 300 1000
2 3 4 1
"""
out_2023 = "16\n200\n100\n1000"

sample_1941 = """5
6 6
1 2 1
2 3 1
5 2 2
2 4 2
4 6 2
3 6 3
1 3
6 6
1 2 1
2 3 1
5 2 2
2 4 2
4 6 2
3 6 3
1 6
6 6
1 2 1
2 3 1
5 2 2
2 4 2
4 6 2
3 6 3
6 6
4 3
1 2 1
1 3 1
4 1 1
2 3
6 7
1 2 43
1 3 34
4 6 43
6 3 43
2 3 43
5 3 43
4 5 43
1 6
"""
out_1941 = "1\n2\n0\n1\n1"

sample_1941_b = """3
7 9
2 4 1
3 6 1
2 3 5
1 7 1
4 7 1
2 5 4
5 4 4
3 4 1
3 7 1
5 3
6 5
6 5 83691
4 1 83691
5 4 83691
3 2 83691
4 3 83691
5 1
6 7
6 1 83691
6 2 83691
2 5 83691
5 6 83691
2 3 83691
5 4 83574
3 5 83691
1 4
"""
out_1941_b = "2\n1\n2"

def norm(s):
    return "\n".join(line.rstrip() for line in s.strip().splitlines())

def run_tests():
    pairs = [
        ("2021B", cpp_2021, py_2021, [(sample_2021, out_2021)]),
        ("2023B", cpp_2023, py_2023, [(sample_2023, out_2023)]),
        ("1941G", cpp_1941, py_1941, [(sample_1941, out_1941), (sample_1941_b, out_1941_b)])
    ]

    with tempfile.TemporaryDirectory() as td:
        for name, cpp, py, tests in pairs:
            cpp_path = os.path.join(td, name + ".cpp")
            py_path = os.path.join(td, name + ".py")
            exe_path = os.path.join(td, name)
            open(cpp_path, "w", encoding="utf-8").write(cpp)
            open(py_path, "w", encoding="utf-8").write(py)

            subprocess.run(
                ["g++", "-std=c++17", "-O2", "-pipe", cpp_path, "-o", exe_path],
                check=True
            )

            for inp, expected in tests:
                got_cpp = subprocess.run(
                    [exe_path], input=inp, text=True,
                    capture_output=True, check=True
                ).stdout
                got_py = subprocess.run(
                    ["python3", py_path], input=inp, text=True,
                    capture_output=True, check=True
                ).stdout

                assert norm(got_cpp) == norm(expected), (name, "C++", got_cpp, expected)
                assert norm(got_py) == norm(expected), (name, "Python", got_py, expected)

run_tests()

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

pdfmetrics.registerFont(TTFont("AA", FONT))
pdfmetrics.registerFont(TTFont("AA-Bold", BOLD))
pdfmetrics.registerFont(TTFont("AA-Mono", MONO))
pdfmetrics.registerFont(TTFont("AA-Mono-Bold", MONOB))

W, H = A4
NAVY = HexColor("#0B1638")
NAVY2 = HexColor("#142347")
TEXT = HexColor("#0F172A")
MUTED = HexColor("#64748B")
LIGHT = HexColor("#F7F9FC")
LINE = HexColor("#E4EAF2")
EASY = HexColor("#4375F5")
MED = HexColor("#14A89A")
HARD = HexColor("#F59E0B")
WHITE = HexColor("#FFFFFF")

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Algoritm Akademiyasi — Kunlik Editoriallar 25")
c.setAuthor("Algoritm Akademiyasi")

body_style = ParagraphStyle(
    "body", fontName="AA", fontSize=9.25, leading=13.1,
    textColor=TEXT, spaceAfter=0
)
small_style = ParagraphStyle(
    "small", fontName="AA", fontSize=8.4, leading=11.8,
    textColor=MUTED
)

def para(text, x, y_top, width, style=body_style):
    p = Paragraph(text, style)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - h)
    return y_top - h

def footer(problem, page):
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(42, 35, W - 42, 35)
    c.setFillColor(MUTED)
    c.setFont("AA", 7.4)
    c.drawString(42, 20, f"Kunlik to‘plam 25 • Codeforces {problem} • O‘zbekcha editorial")
    c.drawRightString(W - 42, 20, f"{page:02d}")

def content_header(letter, level, rating, problem, title, tags, accent):
    c.setFillColor(LIGHT)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.roundRect(36, H - 106, W - 72, 70, 14, fill=1, stroke=0)
    c.setFillColor(accent)
    c.setFont("AA-Bold", 26)
    c.drawString(54, H - 80, letter)
    c.setFillColor(WHITE)
    c.setFont("AA-Bold", 8.1)
    c.drawString(94, H - 61, f"{level} • {rating} • CODEFORCES {problem}")
    c.setFont("AA-Bold", 17)
    c.drawString(94, H - 84, title)
    c.setFillColor(HexColor("#C5D0E6"))
    c.setFont("AA", 7.8)
    c.drawString(94, H - 99, tags)

def section(y, num, title, html, accent, body=body_style):
    c.setFillColor(accent)
    c.roundRect(42, y - 14, 28, 18, 5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("AA-Bold", 8)
    c.drawCentredString(56, y - 8.7, num)
    c.setFillColor(TEXT)
    c.setFont("AA-Bold", 11.6)
    c.drawString(79, y - 9.3, title)
    y -= 24
    y = para(html, 43, y, W - 86, body)
    return y - 14

def code_block(title, code, accent, x, y_top, width, max_height, font_size=6.65, leading=8.15):
    c.setFillColor(accent)
    c.roundRect(x, y_top - 18, 26, 18, 5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("AA-Bold", 7.4)
    c.drawCentredString(x + 13, y_top - 12.5, title.split()[0])
    c.setFillColor(TEXT)
    c.setFont("AA-Bold", 10.4)
    c.drawString(x + 34, y_top - 13, " ".join(title.split()[1:]))
    y = y_top - 31
    c.setFillColor(HexColor("#EEF2F7"))
    box_h = min(max_height, len(code.splitlines()) * leading + 16)
    c.roundRect(x, y - box_h + 6, width, box_h, 8, fill=1, stroke=0)
    c.setFillColor(TEXT)
    c.setFont("AA-Mono", font_size)
    yy = y - 6
    for line in code.splitlines():
        c.drawString(x + 10, yy, line)
        yy -= leading
    return y - box_h - 8

def cover_card(y, letter, title, meta, accent):
    x = 55
    width = W - 110
    c.setFillColor(NAVY2)
    c.roundRect(x, y - 92, width, 82, 13, fill=1, stroke=0)
    c.setFillColor(accent)
    c.roundRect(x + 12, y - 79, 54, 54, 10, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("AA-Bold", 24)
    c.drawCentredString(x + 39, y - 62, letter)
    c.setFont("AA-Bold", 14.2)
    c.drawString(x + 82, y - 48, title)
    c.setFillColor(HexColor("#B8C5DF"))
    c.setFont("AA-Bold", 8.3)
    c.drawString(x + 82, y - 69, meta)

c.setFillColor(NAVY)
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(HexColor("#91A2C6"))
c.setFont("AA-Bold", 8)
c.drawString(55, H - 57, "CODEFORCES • KUNLIK TO‘PLAM 25")
c.setFillColor(WHITE)
c.setFont("AA-Bold", 34)
c.drawString(55, H - 112, "KUNLIK")
c.drawString(55, H - 151, "EDITORIALLAR")
c.setFillColor(HexColor("#B8C5DF"))
c.setFont("AA", 8.7)
tagline = "Darajaga mos tushuntirish • muhim kuzatuvlar • qisqa misollar • kuchli “Keyingi safar” • C++ va Python"
p = Paragraph(tagline, ParagraphStyle("cover", fontName="AA", fontSize=8.7, leading=12, textColor=HexColor("#B8C5DF")))
p.wrapOn(c, W - 110, 80)
p.drawOn(c, 55, H - 193)

cover_card(H - 220, "B", "Maximize Mex", "2021B • EASY • 1200", EASY)
cover_card(H - 322, "B", "Skipping", "2023B • MEDIUM • 1700", MED)
cover_card(H - 424, "G", "Rudolf and Subway", "1941G • HARD • 2000", HARD)

c.setFillColor(HexColor("#91A2C6"))
c.setFont("AA", 8.1)
c.drawString(55, 35, "Algoritm Akademiyasi • 3 ta masala • A4 format")
c.showPage()

content_header("B", "EASY", "1200", "2021B", "Maximize Mex", "greedy · qoldiq sinflari", EASY)
y = H - 132
y = section(y, "01", "Qisqacha shart",
    "n ta sonli a massiv va x soni berilgan. Istalgan elementga x ni xohlagancha marta qo‘shish mumkin. "
    "Operatsiyalarni optimal bajarib, massivning MEX qiymatini imkon qadar kattalashtiring.", EASY)
y = section(y, "02", "Kuzatuvlar",
    "<b>1.</b> a[i] ga faqat x qo‘shamiz. Demak uning <b>x ga bo‘lgandagi qoldig‘i hech qachon o‘zgarmaydi.</b><br/>"
    "<b>2.</b> Faqat qoldiq yetarli emas: qiymatni kamaytira olmaymiz. y sonini hosil qilish uchun tanlangan a[i] uchun "
    "a[i] ≤ y va a[i] mod x = y mod x bo‘lishi kerak. Masalan x=3 bo‘lsa, 4 qoldiq bo‘yicha 1 ga mos, lekin 4 dan 1 yasab bo‘lmaydi.<br/>"
    "<b>3.</b> MEX kamida M bo‘lishi uchun 0,1,...,M−1 ning har biri mavjud bo‘lishi kerak. Shuning uchun targetlarni 0 dan boshlab ketma-ket yopamiz.<br/>"
    "<b>4.</b> Hozirgi y ni yopadigan element bo‘lsa, uni hozir ishlatish xavfsiz. y ochiq qolsa MEX shu yerning o‘zida tugaydi; elementni “keyinga saqlash” foyda bermaydi.<br/>"
    "<b>5.</b> Massivni saralaymiz. y oshgani sari a[i]≤y bo‘lib qolgan elementlarni ularning qoldiq hisoblagichiga qo‘shamiz va y mod x guruhidan bittasini sarflaymiz.<br/>"
    "<b>Misol.</b> x=3, a=[0,3,2,1,5,2]. 0,1,2,3 ni yopish mumkin. 4 uchun qoldiq 1 kerak, lekin mos foydalanilmagan element qolmaydi. Javob 4.", EASY)
y = section(y, "03", "Keyingi safar",
    "<b>Faqat +x qilish mumkin bo‘lsa, ikki narsani darrov tekshiring: modulo invariant va faqat yuqoriga harakat.</b> "
    "Keyin targetni kichikdan kattaga yurib, “shu targetgacha yetib kelgan resurslar”ni qoldiq bo‘yicha saqlash ko‘p masalani greedy ga aylantiradi.", EASY)
y = section(y, "04", "Yechim",
    "a ni saralaymiz. mex=0..n bo‘yicha yuramiz. a[p]≤mex bo‘lgan barcha yangi elementlarni cnt[a[p] mod x] ga qo‘shamiz. "
    "Agar cnt[mex mod x]=0 bo‘lsa, mex ni hosil qilib bo‘lmaydi va shu maksimal MEX. Aks holda shu guruhdan bittasini ishlatamiz.", EASY)
y = section(y, "05", "To‘g‘rilik va murakkablik",
    "Induksiya bo‘yicha 0..mex−1 targetlari turli elementlar bilan yopilgan deb olaylik. mex uchun faqat a[i]≤mex va bir xil qoldiqli element yaroqli; algoritm aynan shularning foydalanilmagan sonini cnt da saqlaydi. "
    "cnt=0 bo‘lsa hech qanday operatsiya mex ni hosil qila olmaydi. cnt>0 bo‘lsa bittasini ishlatish avvalgi targetlarga tegmaydi va mex ham yopiladi. Shunday qilib birinchi muvaffaqiyatsiz mex optimal javob. "
    "<b>O(n log n)</b> vaqt, <b>O(n)</b> xotira.", EASY)
footer("2021B", 2)
c.showPage()

content_header("B", "EASY", "1200", "2021B", "Maximize Mex", "greedy · qoldiq sinflari", EASY)
y = H - 132
y = code_block("06 C++ kodi", cpp_2021, EASY, 42, y, W - 84, 360, 6.55, 8.0)
y = code_block("07 Python kodi", py_2021, EASY, 42, y, W - 84, 250, 6.55, 8.0)
footer("2021B", 3)
c.showPage()

content_header("B", "MEDIUM", "1700", "2023B", "Skipping", "Dijkstra · graf modeli · prefiks yig‘indi", MED)
y = H - 132
y = section(y, "01", "Qisqacha shart",
    "n ta masala bor. i-masala kelganda uni submit qilib a[i] ball olish yoki skip qilish mumkin. Submit qilsak tizim hali ko‘rilmagan j&lt;i lar ichidan eng kattasini, skip qilsak j≤b[i] lar ichidan eng kattasini beradi. "
    "Har bir masala ko‘pi bilan bir marta beriladi. Maksimal ballni toping.", MED)
y = section(y, "02", "Kuzatuvlar",
    "<b>1.</b> “Qancha ball oldim?” o‘rniga <b>“qancha ballni yo‘qotdim?”</b> deb qarash qulay. Submit narxi 0, skip qilish narxi a[i].<br/>"
    "<b>2.</b> Holatni hozir berilgan masala indeksi deb olsak, ikkita o‘tish paydo bo‘ladi: submit i → i−1, narx 0; skip i → b[i], narx a[i]. Bu — manfiy bo‘lmagan og‘irlikli yo‘naltirilgan graf.<br/>"
    "<b>3.</b> Asl shartda masalaga qayta kirib bo‘lmaydi. Grafda bunga ruxsat bergandek ko‘rinamiz. Lekin shortest path bir vertexni qayta aylanishdan foyda ko‘rmaydi: sikl narxi manfiy emas. Demak minimal yo‘lni takrorlanishsiz tanlash mumkin va u asl jarayonda ham bajariladi.<br/>"
    "<b>4.</b> i holatiga minimal penalty dist[i] bilan yetib kelsak, hali olinmagan indekslari ≤i bo‘lgan masalalarni submit qilib tugatish mumkin. Ularning umumiy potensial bali pref[i], yo‘qotilgan qismi esa dist[i]. Kandidat: <b>pref[i]−dist[i]</b>.<br/>"
    "<b>Misol.</b> Ikkinchi sampleda skip 1 → 3 (10 penalty), submit 3 → 2, skip 2 → 4 (yana 10). 4 ga penalty=20 bilan yetamiz. pref[4]=220, shuning uchun 220−20=200.", MED)
y = section(y, "03", "Keyingi safar",
    "<b>Maksimal reward va majburiy transitionlar aralashsa, rewardni yo‘qotilgan penalty ga aylantirib ko‘ring.</b> "
    "Agar har qaror sizni boshqa holatga olib borsa, “eng kam yo‘qotish bilan shu holatga yetish” shortest path bo‘lishi mumkin. So‘ng total reward − min penalty formulasini qidiring.", MED)
y = section(y, "04", "Yechim",
    "pref[i]=a[1]+...+a[i] ni hisoblaymiz. 1 dan Dijkstra boshlaymiz. Har v dan v−1 ga 0 og‘irlikli qirra va b[v] ga a[v] og‘irlikli qirra qo‘yamiz. "
    "Dijkstra dist[i] — i ga yetishdagi minimal yo‘qotish. Javob max(pref[i]−dist[i]).", MED)
y = section(y, "05", "To‘g‘rilik va murakkablik",
    "Har haqiqiy qarorlar ketma-ketligi grafdagi aynan shu transitionlar yo‘liga mos keladi va skip qilingan masalalar ballari yo‘l og‘irligiga teng. Aksincha, minimal yo‘lni siklsiz tanlash mumkin, shuning uchun u masalalarni takror ko‘rmaydi va haqiqiy strategiyaga mos. "
    "i ga eng kam penalty bilan kelgach, qolgan ≤i masalalarni submit qilish pref[i]−dist[i] beradi. Barcha i lar bo‘yicha maksimum optimal javob. <b>O(n log n)</b> vaqt, <b>O(n)</b> xotira.", MED)
footer("2023B", 4)
c.showPage()

content_header("B", "MEDIUM", "1700", "2023B", "Skipping", "Dijkstra · graf modeli · prefiks yig‘indi", MED)
y = H - 132
y = code_block("06 C++ kodi", cpp_2023, MED, 42, y, W - 84, 410, 6.0, 7.25)
y = code_block("07 Python kodi", py_2023, MED, 42, y, W - 84, 275, 6.0, 7.25)
footer("2023B", 5)
c.showPage()

content_header("G", "HARD", "2000", "1941G", "Rudolf and Subway", "BFS · bipartit graf · rangni siqish", HARD)
y = H - 132
y = section(y, "01", "Qisqacha shart",
    "Bog‘langan yo‘naltirilmagan graf berilgan; har qirraning rangi bor. Bir xil rangdagi barcha qirralar bitta subway line bo‘lib, ular bog‘langan subgraf hosil qiladi. "
    "b stansiyadan e stansiyaga borishda ishlatiladigan <b>turli line lar sonini</b> minimal qiling.", HARD)
y = section(y, "02", "Kuzatuvlar",
    "<b>1.</b> Oddiy shortest path qirralar sonini minimallashtiradi, lekin bizga bu kerak emas. Bir line ichida 1 ta qirra yursak ham, 100 ta qirra yursak ham narx 1.<br/>"
    "<b>2.</b> Har bir rang c uchun alohida yordamchi vertex C<sub>c</sub> yaratamiz. Rang c ga tegishli qirraning har ikki uchini C<sub>c</sub> bilan bog‘laymiz.<br/>"
    "<b>3.</b> Endi “stansiya → rang tuguni → stansiya” yurishi aynan <b>bitta line dan foydalanish</b>ni bildiradi. Shuning uchun yangi grafdagi har 2 ta BFS qirrasi asl masalada 1 line ga teng.<br/>"
    "<b>4.</b> Masaladagi muhim kafolat: bir rangdagi qirralar bog‘langan subgraf. Shu sabab bir rang tuguni orqali o‘sha line ga tegishli istalgan stansiyadan boshqasiga o‘tish qonuniy. Bu kafolat bo‘lmaganda bitta rang tuguni noto‘g‘ri ravishda ajralgan qismlarni ulab qo‘yardi.<br/>"
    "<b>Misol.</b> 1−2−3 yashil line bo‘lsa, yangi grafda 1 → Green → 3 yo‘li bor. BFS masofasi 2, demak ishlatilgan line lar soni 2/2=1.", HARD)
y = section(y, "03", "Keyingi safar",
    "<b>Narx qirraga emas, qirraning turi/rangi/rejimiga bog‘liq bo‘lsa, “type node” qo‘shishni o‘ylang.</b> "
    "Bitta tanlov bilan butun guruh ichida harakat qilish mumkin bo‘lgan masalalarda original grafni vertex↔type bipartit grafiga aylantirish ko‘pincha oddiy BFS ni yetarli qiladi.", HARD)
y = section(y, "04", "Yechim",
    "Har xil rangga yangi vertex id beramiz. Har original (u,v,c) qirra uchun u−C[c] va v−C[c] bog‘lanishlarini qo‘shamiz. "
    "b stansiyadan oddiy BFS qilamiz. e stansiyagacha topilgan masofa doim juft bo‘ladi; javob dist[e]/2.", HARD)
y = section(y, "05", "To‘g‘rilik va murakkablik",
    "Asl grafdagi k ta line ishlatadigan istalgan marshrut yangi grafda har line uchun station→color→station ko‘rinishidagi 2 qadamga almashtiriladi, ya’ni uzunligi 2k bo‘lgan yo‘l beradi. "
    "Aksincha, yangi grafdagi station va color tugunlari almashinadigan har yo‘lning har 2 qadami bitta haqiqiy line dan foydalanishga mos. Demak minimal BFS masofasi aynan 2·optimal_line_soni. "
    "C++ koddagi map sabab <b>O(m log m+n+m)</b> vaqt, <b>O(n+m)</b> xotira.", HARD)
footer("1941G", 6)
c.showPage()

content_header("G", "HARD", "2000", "1941G", "Rudolf and Subway", "BFS · bipartit graf · rangni siqish", HARD)
y = H - 132
code_block("06 C++ kodi", cpp_1941, HARD, 42, y, W - 84, 650, 6.35, 7.8)
footer("1941G", 7)
c.showPage()

content_header("G", "HARD", "2000", "1941G", "Rudolf and Subway", "BFS · bipartit graf · rangni siqish", HARD)
y = H - 132
code_block("07 Python kodi", py_1941, HARD, 42, y, W - 84, 650, 6.5, 8.0)
footer("1941G", 8)
c.save()

print("All C++ and Python solutions passed official samples.")
print(OUT)
