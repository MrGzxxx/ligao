#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 5 个产品详情页（快速门/硬质快速门/堆积门/工业滑升门/道闸）。

设计约束（与 docs/SPEC-官网精修.md 一致）：
- 单文件 HTML + 内联 CSS，无 JS、无框架、无构建链
- 同一套设计令牌，与 index.html 视觉一致
- 参数只给「常规配置区间」，逐页声明非承诺值；不编造客户、项目、数字
- 每页含 Product / BreadcrumbList / FAQPage 结构化数据
用法：python3 docs/build-products.py
"""
import json
import os

SITE = "https://ligaomenye.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026-10-17"

CSS = """
:root { --navy:#1a3a5c; --accent:#c43713; --ink:#293744; --muted:#5e6b77; --line:#d6dde3; --soft:#f8f9fa; }
*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }
html { -webkit-text-size-adjust:100%; }
body { font-family:"Microsoft YaHei","PingFang SC","Hiragino Sans GB","Source Han Sans SC",sans-serif; color:var(--ink); background:#fff; line-height:1.75; font-size:15px; }
img { max-width:100%; display:block; }
a { color:var(--navy); text-decoration:none; }
a:hover { text-decoration:underline; }
.inner { max-width:1120px; margin:0 auto; padding:0 20px; }

/* nav */
nav { position:sticky; top:0; z-index:50; background:#fff; border-bottom:1px solid var(--line); }
nav .inner { display:flex; align-items:center; justify-content:space-between; height:64px; gap:16px; }
.logo { font-size:21px; font-weight:700; color:var(--navy); letter-spacing:.5px; white-space:nowrap; }
.logo span { color:var(--accent); }
.nav-check { display:none; }
.nav-burger { display:none; cursor:pointer; margin-left:auto; color:var(--navy); }
nav .links { display:flex; gap:26px; list-style:none; align-items:center; }
nav .links a { font-size:15px; color:var(--ink); padding:4px 0; border-bottom:2px solid transparent; }
nav .links a:hover { color:var(--navy); border-bottom-color:var(--accent); text-decoration:none; }
nav .tel { font-weight:700; color:var(--navy); white-space:nowrap; }
@media (max-width:820px) {
  .nav-burger { display:block; }
  nav .inner { gap:10px; }
  nav .links { display:none; position:absolute; top:100%; left:0; right:0; background:#fff; flex-direction:column; align-items:stretch; gap:0; padding:6px 20px 14px; border-bottom:1px solid var(--line); box-shadow:0 6px 12px rgba(26,58,92,.06); }
  nav .links li { border-top:1px solid #eef1f4; }
  nav .links a { display:block; padding:11px 0; border-bottom:0; }
  .nav-check:checked ~ .links { display:flex; }
}

/* breadcrumb */
.crumb { font-size:13px; color:var(--muted); padding:14px 0 0; }
.crumb a { color:var(--muted); }
.crumb span { margin:0 6px; color:#b6c1cb; }

/* hero */
.phero { padding:26px 0 40px; border-bottom:1px solid var(--line); }
.phero-in { display:grid; grid-template-columns:1.04fr .96fr; gap:44px; align-items:center; }
.kicker { display:inline-block; font-size:13px; color:var(--accent); border:1px solid #eccfc6; background:#fdf5f2; padding:3px 10px; border-radius:2px; margin-bottom:14px; }
.phero h1 { font-size:40px; line-height:1.25; color:var(--navy); letter-spacing:.5px; margin-bottom:14px; }
.phero h1 small { display:block; font-size:15px; font-weight:400; color:var(--muted); letter-spacing:0; margin-top:10px; }
.lead { font-size:16px; color:#3d4d5c; margin-bottom:20px; }
.badges { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:22px; }
.badges span { font-size:13px; color:#435d73; background:#eef2f5; padding:4px 10px; border-radius:2px; }
.btns { display:flex; flex-wrap:wrap; gap:12px; align-items:center; }
.btn { display:inline-block; padding:12px 22px; border-radius:3px; font-size:15px; font-weight:600; border:1px solid transparent; transition:background .15s,color .15s,border-color .15s; }
.btn:hover { text-decoration:none; }
.btn.primary { background:var(--accent); color:#fff; }
.btn.primary:hover { background:#a92d0f; }
.btn.ghost { border-color:#b9c5cf; color:var(--navy); background:#fff; }
.btn.ghost:hover { border-color:var(--navy); }
.btn:focus-visible { outline:2px solid var(--navy); outline-offset:2px; }
.phero-visual img { width:100%; height:auto; border:1px solid var(--line); border-radius:3px; background:#f4f4f4; }
.phero-visual .cap { font-size:13px; color:var(--muted); margin-top:9px; }

/* layout */
.pbody { display:grid; grid-template-columns:minmax(0,1fr) 316px; gap:48px; padding:44px 0 60px; align-items:start; }
article, aside { min-width:0; }
article section + section { margin-top:42px; }
article h2 { font-size:25px; color:var(--navy); line-height:1.4; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid var(--line); }
article h3 { font-size:17px; color:var(--navy); margin:22px 0 8px; }
article p { margin-bottom:12px; }
article ul,article ol { margin:0 0 14px 20px; }
article li { margin-bottom:7px; }
strong { color:#1f2f3d; }

/* table */
.tw { overflow-x:auto; -webkit-overflow-scrolling:touch; max-width:100%; margin:6px 0 16px; }
table { border-collapse:collapse; width:100%; font-size:14px; min-width:520px; table-layout:auto; }
td, th { word-break:break-word; }
th,td { border:1px solid var(--line); padding:9px 12px; text-align:left; vertical-align:top; }
th { background:#f2f5f8; color:var(--navy); font-weight:600; white-space:nowrap; }
td:first-child { white-space:nowrap; color:#3d4d5c; }
.yes { color:#1f7a4d; font-weight:600; }
.no { color:#a33; font-weight:600; }
.mid { color:#9a6a12; font-weight:600; }

/* note */
.note { background:var(--soft); border-left:3px solid #9fb1c1; padding:12px 16px; font-size:14px; color:#4a5a68; margin:14px 0; }
.note b { color:var(--navy); }

/* gallery */
.gal { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:16px; }
.gal figure { margin:0; }
.gal img { width:100%; height:170px; object-fit:cover; border:1px solid var(--line); border-radius:3px; background:#f4f4f4; }
.gal figcaption { font-size:12.5px; color:var(--muted); margin-top:7px; }

/* faq */
details { border:1px solid var(--line); border-radius:3px; padding:14px 16px; margin-bottom:10px; background:#fff; }
details[open] { background:#fcfdfe; }
summary { font-weight:600; color:var(--navy); cursor:pointer; font-size:15.5px; list-style:none; position:relative; padding-right:22px; }
summary::-webkit-details-marker { display:none; }
summary::after { content:"+"; position:absolute; right:0; top:-2px; color:var(--accent); font-weight:400; font-size:20px; }
details[open] summary::after { content:"\\2013"; }
details p { margin:10px 0 0; font-size:14.5px; color:#455564; }

/* aside */
aside { position:sticky; top:84px; }
.card { border:1px solid var(--line); border-radius:4px; padding:20px; background:#fff; box-shadow:0 1px 2px rgba(26,58,92,.03); }
.card h3 { font-size:16px; color:var(--navy); margin:0 0 12px; padding-bottom:10px; border-bottom:1px solid var(--line); }
.card .row { display:flex; gap:8px; font-size:14px; color:#455564; margin-bottom:9px; line-height:1.65; }
.card .row b { flex:0 0 40px; color:var(--navy); font-weight:600; }
.card .row span { flex:1 1 auto; min-width:0; }
.card .phone { display:block; font-size:22px; font-weight:700; color:var(--accent); letter-spacing:.5px; margin:2px 0 16px; }
.qrbox { text-align:center; border-top:1px dashed var(--line); margin-top:14px; padding-top:16px; }
.qrbox img { width:168px; height:168px; margin:0 auto 8px; border:1px solid var(--line); border-radius:3px; }
.qrbox p { font-size:13px; color:var(--muted); line-height:1.6; }
.card + .card { margin-top:16px; }
.card ul { margin:0; padding:0; list-style:none; }
.card ul li { font-size:14px; padding:7px 0; border-bottom:1px solid #eef1f4; }
.card ul li:last-child { border-bottom:0; }

/* related */
.related { background:var(--soft); padding:40px 0; border-top:1px solid var(--line); }
.related h2 { font-size:20px; color:var(--navy); margin-bottom:18px; }
.rel-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }
.rel-grid a { display:block; border:1px solid var(--line); background:#fff; border-radius:3px; padding:16px; color:var(--ink); }
.rel-grid a:hover { border-color:#879bae; text-decoration:none; }
.rel-grid b { display:block; color:var(--navy); font-size:15.5px; margin-bottom:5px; }
.rel-grid span { font-size:13px; color:var(--muted); }

/* cta strip */
.strip { background:var(--navy); color:#fff; padding:34px 0; }
.strip .inner { display:flex; align-items:center; justify-content:space-between; gap:20px; flex-wrap:wrap; }
.strip p { font-size:17px; }
.strip small { display:block; font-size:13px; color:#b9cade; margin-top:4px; }
.strip .btn.primary { background:var(--accent); }

footer { background:#12293f; color:#93a7ba; padding:26px 0; font-size:13px; text-align:center; line-height:2; }
footer a { color:#c3d3e0; }

@media (max-width:980px) {
  .pbody { grid-template-columns:1fr; gap:34px; }
  aside { position:static; }
  .phero-in { grid-template-columns:1fr; gap:26px; }
  .phero h1 { font-size:31px; }
  .rel-grid { grid-template-columns:repeat(2,1fr); }
  .gal { grid-template-columns:repeat(2,1fr); }
}
@media (max-width:560px) {
  table { min-width:0; font-size:12.5px; }
  th, td { padding:7px 8px; }
  td:first-child { white-space:normal; }
  article h2 { font-size:22px; }
  .pbody { padding:32px 0 44px; }
  .gal { grid-template-columns:1fr; }
  .gal img { height:200px; }
  .rel-grid { grid-template-columns:1fr; }
  .strip p { font-size:15px; }
}
"""

PHONE_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" '
             'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
             'style="vertical-align:-3px;margin-right:7px"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 '
             '19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 '
             '2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>')

NAV = """<nav>
  <div class="inner">
    <a class="logo" href="index.html">立高<span>门业</span></a>
    <input type="checkbox" id="navtoggle" class="nav-check" aria-hidden="true">
    <label for="navtoggle" class="nav-burger" aria-label="打开菜单"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg></label>
    <ul class="links">
      <li><a href="index.html#about">关于我们</a></li>
      <li><a href="index.html#products">产品中心</a></li>
      <li><a href="index.html#industries">应用行业</a></li>
      <li><a href="index.html#projects">工程案例</a></li>
      <li><a href="index.html#reports">检测报告</a></li>
      <li><a href="index.html#contact">联系我们</a></li>
    </ul>
    <a class="tel" href="tel:18983919000">189-8391-9000</a>
  </div>
</nav>"""

ASIDE = """<aside>
  <div class="card">
    <h3>按现场条件报价</h3>
    <a href="tel:18983919000" class="phone">189-8391-9000</a>
    <div class="row"><b>公司</b><span>重庆立高门业有限公司</span></div>
    <div class="row"><b>地址</b><span>重庆市巴南区公平场大道845号附17号</span></div>
    <div class="row"><b>服务</b><span>勘测 · 设计 · 生产 · 安装 · 维保</span></div>
    <div class="qrbox">
      <img src="images/wechat-qr.png" alt="微信咨询二维码 — 立高门业 郭纪敏" width="168" height="168" loading="lazy">
      <p>微信扫码，加我好友<br>郭纪敏 · 189-8391-9000</p>
    </div>
  </div>
  <div class="card">
    <h3>常被问到</h3>
    <ul>
      <li>能不能先上门量尺寸？</li>
      <li>旧门能不能只换门体？</li>
      <li>外地项目做不做？</li>
      <li>交期一般多久？</li>
    </ul>
  </div>
</aside>"""

FOOTER = """<footer>
  <p>© 2011-2026 重庆立高门业有限公司 &nbsp;|&nbsp; 15年工业门自研品牌</p>
  <p><a href="index.html">返回首页</a> · <a href="index.html#products">全部产品</a> · <a href="index.html#contact">联系方式</a></p>
</footer>"""


def render(p):
    url = f"{SITE}/{p['slug']}.html"
    ld = [{
        "@context": "https://schema.org", "@type": "Product",
        "name": p["name"], "description": p["meta_desc"], "category": p["category"],
        "image": [f"{SITE}/images/products/{p['images'][0]}"],
        "url": url,
        "brand": {"@type": "Brand", "name": "立高门业"},
        "manufacturer": {"@type": "Organization", "name": "重庆立高门业有限公司",
                         "url": SITE, "telephone": "18983919000"},
        "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in p["props"]],
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "产品中心", "item": f"{SITE}/#products"},
            {"@type": "ListItem", "position": 3, "name": p["name"], "item": url},
        ],
    }, {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]],
    }]

    gal = "\n".join(
        f'        <figure><img src="{src}" alt="{alt}" width="{g[3] if len(g) > 3 else 1200}" '
        f'height="{g[4] if len(g) > 4 else 900}" loading="lazy">'
        f'<figcaption>{cap}</figcaption></figure>'
        for g in p["gallery"] for src, alt, cap in [g[:3]])

    faq_html = "\n".join(
        f'      <details><summary>{q}</summary><p>{a}</p></details>' for q, a in p["faq"])

    rel = "\n".join(
        f'      <a href="{s}.html"><b>{n}</b><span>{d}</span></a>' for s, n, d in p["related"])

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['title']}</title>
<meta name="description" content="{p['meta_desc']}">
<meta name="keywords" content="{p['keywords']}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{p['title']}">
<meta property="og:description" content="{p['meta_desc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/products/{p['images'][0]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="images/favicon.png">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<style>{CSS}</style>
</head>
<body>
{NAV}
<div class="inner"><div class="crumb"><a href="index.html">首页</a><span>/</span><a href="index.html#products">产品中心</a><span>/</span>{p['name']}</div></div>

<header class="phero">
  <div class="inner phero-in">
    <div>
      <span class="kicker">{p['kicker']}</span>
      <h1>{p['h1']}<small>{p['sub']}</small></h1>
      <p class="lead">{p['lead']}</p>
      <div class="badges">{''.join(f'<span>{b}</span>' for b in p['badges'])}</div>
      <div class="btns">
        <a class="btn primary" href="tel:18983919000">{PHONE_SVG}189-8391-9000</a>
        <a class="btn ghost" href="index.html#contact">上门勘测 / 微信咨询</a>
      </div>
    </div>
    <div class="phero-visual">
      <img src="images/products/{p['images'][0]}" alt="{p['hero_alt']}" width="1200" height="900" fetchpriority="high">
      <p class="cap">{p['hero_cap']}</p>
    </div>
  </div>
</header>

<div class="inner pbody">
  <article>
{p['body']}
    <section>
      <h2>{p.get('galtitle', '项目实拍')}</h2>
      <div class="gal">
{gal}
      </div>
    </section>

    <section>
      <h2>常见问题</h2>
{faq_html}
    </section>

    <div class="note">
      <b>关于参数</b>：本页数据为常规配置区间，用于初选与预算参考，不构成对具体项目的性能承诺；
      实际参数以现场勘测记录与合同技术附件为准。产品检测情况见<a href="index.html#reports">检测报告</a>。
    </div>

    <section>
      <h2>参考标准</h2>
      <ul>
{''.join(f'        <li>{s}</li>' + chr(10) for s in p['stds'])}
      </ul>
      <p style="font-size:13px;color:#7b8894">本页更新于 {TODAY}。以上标准为产品选型与验收的通用依据，具体执行版本以项目所在地区现行有效版本为准。</p>
    </section>
  </article>
{ASIDE}
</div>

<section class="strip">
  <div class="inner">
    <p>不确定该用哪一种门？<small>把洞口尺寸、通行频率、现场照片发过来，我们给方案和报价。</small></p>
    <a class="btn primary" href="tel:18983919000">{PHONE_SVG}189-8391-9000</a>
  </div>
</section>

<section class="related">
  <div class="inner">
    <h2>相关产品</h2>
    <div class="rel-grid">
{rel}
    </div>
  </div>
</section>

{FOOTER}
</body>
</html>
"""


# ---------------------------------------------------------------- 1. 快速门
rapid = {
    "slug": "rapid-door", "name": "快速门", "images": ["rapid-door.jpg", "hard-rapid-door.jpg"],
    "category": "工业门 / 快速卷帘门",
    "title": "快速门（PVC快速卷帘门）选型与参数｜重庆立高门业",
    "meta_desc": "快速门怎么选：适用场景判断、门帘与导轨结构、开启速度与安全配置、安装条件与维护周期，附立高门业康明斯、赛力斯、ABB等项目实拍。重庆本地勘测报价 189-8391-9000。",
    "keywords": "快速门,快速卷帘门,PVC快速门,重庆快速门厂家,车间快速门,冷库快速门,立高门业",
    "kicker": "PVC 快速卷帘门",
    "h1": "快速门",
    "sub": "车间通道 · 洁净区 · 冷库缓冲 · 物流隔断",
    "hero_alt": "快速门（康明斯项目实拍）— 重庆立高门业",
    "hero_cap": "康明斯项目 · 内置电机快速门",
    "lead": "快速门最容易被误解的一点是：它的价值不在“快”，而在“开得短”。门每开一秒，车间与外界就交换一秒的空气——洁净区的压差、冷库的冷量、除尘车间的粉尘，都是按秒算成本的。",
    "badges": ["15年自研制造", "已通过重庆市计量质量检测研究院检验", "自有安装与维保团队"],
    "props": [("适用洞口宽", "2–6 m"), ("开启速度", "0.6–2.0 m/s（立高KJM系列产品卡标注1.2–1.5 m/s）"),
              ("驱动", "伺服或变频电机"), ("安全配置", "光电对射、安全底边（选配）")],
    "body": """    <section>
      <h2>先判断：这个位置该不该装快速门</h2>
      <p>快速门不是“比卷帘门高级”的替代品，它解决的是<strong>高频通行下的空气交换</strong>问题。用错位置，钱花了效果也不明显；用对位置，一年省下的冷量与洁净维护费就能抵掉差价。</p>
      <div class="tw"><table>
        <tr><th>现场情况</th><th>适合度</th><th>说明</th></tr>
        <tr><td>车间之间通道，每小时通行十几次以上</td><td class="yes">适合</td><td>高频启闭是快速门的主场，普通卷帘门跟不上节拍，也更容易坏</td></tr>
        <tr><td>洁净车间、制药、食品内包</td><td class="yes">适合</td><td>开门时间短，空气交换少，有利于维持压差与洁净度</td></tr>
        <tr><td>冷库穿堂、缓冲间</td><td class="yes">适合</td><td>减少冷量流失和门口结霜，配合风幕效果更好</td></tr>
        <tr><td>室外大洞口、山口或沿海强风区</td><td class="mid">谨慎</td><td>软帘靠抗风杆约束，抗风能力有限，建议改硬质快速门或堆积门</td></tr>
        <tr><td>每天只开三五次的仓库大门</td><td class="no">不建议</td><td>用工业滑升门更划算，保温与密封也更好</td></tr>
      </table></div>
    </section>

    <section>
      <h2>一樘快速门由哪些部分组成</h2>
      <p>把这六件事搞清楚，报价单上的差异就能看懂了——同样的尺寸，价格差往往不在电机，而在门帘、导轨和安全感应的配置上。</p>
      <h3>① 门帘</h3>
      <p>PVC 涂层织物，中间可加透明视窗方便观察。门帘的克重、抗撕裂强度和颜色都影响寿命与采光，属于“看不见但决定耐用度”的部分。频繁通行、叉车贴边作业的现场，门帘是最先损耗的件。</p>
      <h3>② 抗风杆</h3>
      <p>横向穿在门帘里的加强杆，把风压分散到两侧导轨。它是软帘门抗风能力的来源，也是判断一樘门适不适合室外的重要依据。</p>
      <h3>③ 导轨与密封</h3>
      <p>导轨不只是“让门上下走”的槽，它同时承担密封与抗风。带毛刷或密封条的导轨能明显减少缝隙渗风；导轨安装的垂直度直接决定门体运行是否偏摆。</p>
      <h3>④ 驱动系统</h3>
      <p>伺服或变频电机。高频工况（每天数百次）优先伺服：启停更柔和、定位更准、寿命更长；低频工况用变频即可，成本更低。</p>
      <h3>⑤ 控制与感应</h3>
      <p>雷达、地磁、拉绳、遥控、门禁刷卡、AGV/输送线联动，按通行方式组合。感应方式选错是“门不好用”的最常见原因——人车混行却只装雷达，就会频繁误开。</p>
      <h3>⑥ 安全装置</h3>
      <p>光电对射（门洞两侧）与安全底边（门帘下沿受压回弹）。有人员步行通过、或有叉车与人员混行的通道，这两项不是选配，是必需。</p>
    </section>

    <section>
      <h2>选型要问清楚的五件事</h2>
      <ol>
        <li><strong>每小时通行次数</strong>——决定电机类型与门帘等级，也决定保修条款是否覆盖。</li>
        <li><strong>洞口尺寸与门楣空间</strong>——宽度决定卷轴长度与抗风杆数量；门楣上方要留出卷轴和防护罩的位置，这一条最常被土建忽略。</li>
        <li><strong>两侧有没有人行通道</strong>——有，就必须配光电与安全底边；没有，也要留出检修空间。</li>
        <li><strong>内外压差与温差</strong>——洁净区与冷库的压差会让门帘“鼓”或“吸”，需要靠抗风杆和导轨密封来约束。</li>
        <li><strong>要不要联动</strong>——门禁、风淋室、输送线、消防信号、AGV，联动方式在报价阶段就要定，后期加装成本高。</li>
      </ol>
    </section>

    <section>
      <h2>参数参考</h2>
      <div class="tw"><table>
        <tr><th>项目</th><th>常规配置区间</th><th>说明</th></tr>
        <tr><td>适用洞口宽</td><td>2–6 m</td><td>超过 6 m 建议评估堆积门或硬质快速门</td></tr>
        <tr><td>适用洞口高</td><td>2–6 m</td><td>门楣上方需预留卷轴与防护罩空间</td></tr>
        <tr><td>开启速度</td><td>0.6–2.0 m/s</td><td>立高 KJM 系列产品卡标注 1.2–1.5 m/s，其余按项目配置</td></tr>
        <tr><td>门帘</td><td>PVC 涂层织物，可选透明视窗</td><td>颜色、克重按项目配置</td></tr>
        <tr><td>驱动</td><td>伺服 / 变频电机</td><td>高频工况优先伺服</td></tr>
        <tr><td>控制方式</td><td>雷达、地磁、拉绳、遥控、门禁联动</td><td>按通行方式选配</td></tr>
        <tr><td>安全装置</td><td>光电对射 + 安全底边</td><td>人车混行时建议全配</td></tr>
      </table></div>
    </section>

    <section>
      <h2>安装前，现场要具备什么</h2>
      <ul>
        <li><strong>门楣空间</strong>：卷轴、防护罩、电机都要装在上方，空间不足只能改门型或改土建，越早确认越省事。</li>
        <li><strong>两侧立柱或墙体</strong>：导轨要固定在结构上，轻钢隔断需要加背衬加固。</li>
        <li><strong>电源</strong>：控制箱位置、电源容量与接地要提前定；室外还要考虑防雨。</li>
        <li><strong>地面</strong>：门帘下沿与地面的贴合度决定密封效果，门槛有坡度或破损的要先处理。</li>
        <li><strong>排水与防水</strong>：室外或半室外安装时，电机与电控的防护等级要按环境选。</li>
      </ul>
    </section>

    <section>
      <h2>维护：四件事按周期做</h2>
      <div class="tw"><table>
        <tr><th>周期</th><th>做什么</th><th>为什么</th></tr>
        <tr><td>每月</td><td>擦拭光电探头、测试安全底边回弹</td><td>灰尘遮挡是误动作和不停门的主要原因</td></tr>
        <tr><td>每季度</td><td>检查门帘有无裂口、导轨有无异物、毛刷是否脱落</td><td>小裂口不处理，几周就会撕成大口</td></tr>
        <tr><td>每半年</td><td>紧固件复紧、限位复核、刹车测试</td><td>高频振动会松动固定点</td></tr>
        <tr><td>每年</td><td>卷轴、轴承、电机碳刷（如有）检查</td><td>把突发故障变成计划检修</td></tr>
      </table></div>
      <p>每天通行 500 次以上的现场，建议把“每月”缩到“每两周”，并把易损件（门帘、底边胶条）备一份在库房——这类件停一次门就是停一条线。</p>
    </section>""",
    "gallery": [
        ("images/products/rapid-door.jpg", "康明斯项目内置电机快速门 — 重庆立高门业", "康明斯 · 快速门（内置电机）"),
        ("images/projects/abb.jpg", "ABB（中国）PVC快速门项目 — 重庆立高门业", "ABB（中国）· PVC 快速门"),
        ("images/projects/dingjin.jpg", "成都顶津食品快速门项目 — 重庆立高门业", "成都顶津食品 · 快速门 · 2020"),
    ],
    "faq": [
        ("快速门和卷帘门到底有什么区别？",
         "卷帘门是帘片卷绕、以“关得严、用得久”为目标；快速门是软帘高速启闭、以“少开门、少交换空气”为目标。每天开合三五次的仓库用卷帘门更划算，每小时十几次以上的通道才需要快速门。两者不是替代关系，选错方向钱就白花了。"),
        ("快速门能抗多大风？",
         "软帘的抗风能力靠抗风杆与导轨约束，本身有限。室外、山口、沿海强风位置，建议改用硬质快速门或堆积门。抗风压性能的检测方法见 GB/T 7106-2019，性能等级按 GB/T 31433 判定，具体到项目要按当地基本风压和安装高度核算。"),
        ("停电了门会不会卡住？",
         "配手动释放装置（手摇或离合），停电后可手动提升，不影响人员和车辆通行。有消防联动要求的场所，按项目配置联动与迫降逻辑。"),
        ("旧门能不能只换门体，不换洞口？",
         "多数情况可以。导轨、卷轴、电机的可复用程度要看原门的状态和尺寸是否匹配；这类改造我们会先看现场照片再判断，避免报了价到现场才发现洞口需要修补。"),
    ],
    "stds": ["JG/T 302-2022《卷帘门窗》（代替 JG/T 302-2011）",
             "GB/T 7106-2019《建筑外门窗气密、水密、抗风压性能检测方法》",
             "GB/T 31433《建筑幕墙、门窗通用技术条件》（性能等级判定）"],
    "related": [("hard-rapid-door", "硬质快速门", "门板结构，抗风与保温更强"),
                ("stacking-door", "堆积门", "超大洞口与高风压通道"),
                ("lifting-door", "工业滑升门", "保温夹芯板，仓库与消防站"),
                ("barrier-gate", "道闸", "出入口车辆管理")],
}

# ---------------------------------------------------------------- 2. 硬质快速门
hard = {
    "slug": "hard-rapid-door", "name": "硬质快速门", "images": ["hard-rapid-door.jpg"],
    "category": "工业门 / 硬质快速卷帘门",
    "title": "硬质快速门（螺旋式/滚筒式）选型与参数｜重庆立高门业",
    "meta_desc": "硬质快速门与软帘快速门的区别、螺旋式与滚筒式怎么选、门板结构与抗风密封、安装土建配合与维护要点，附成都益海、昆船、洛碛垃圾处理厂项目实拍。",
    "keywords": "硬质快速门,螺旋硬质快速门,铝合金快速门,硬质快速卷帘门,重庆硬质快速门,立高门业",
    "kicker": "铝合金 / 钢质夹芯门板",
    "h1": "硬质快速门",
    "sub": "螺旋式 · 滚筒式 · 外立面与高频重载通道",
    "hero_alt": "硬质快速门（成都益海项目实拍）— 重庆立高门业",
    "hero_cap": "成都益海嘉里 · 螺旋硬质快速门",
    "lead": "软帘快速门的天花板很清楚：风一大门帘就鼓，压差一大缝隙就漏，洞口一宽卷轴就吃力。硬质快速门换的不是电机，是门体——用铝合金或钢质夹芯门板替代软帘，把抗风、保温和密封一并接过去。",
    "badges": ["门板结构，抗风更强", "夹芯板可选，兼顾保温", "螺旋轨迹，适合高频重载"],
    "props": [("门板", "铝合金或钢质夹芯板"), ("开启速度", "1.0–2.5 m/s（按配置）"),
              ("抗风", "按 GB/T 7106-2019 检测，等级按 GB/T 31433"), ("轨迹", "螺旋式 / 滚筒式")],
    "body": """    <section>
      <h2>硬质快速门和软帘快速门，差在哪</h2>
      <p>两者常被放在一张报价单上比较，但适用的位置其实不一样。先看这张表，再决定要不要多花这笔钱。</p>
      <div class="tw"><table>
        <tr><th>维度</th><th>软帘快速门</th><th>硬质快速门</th></tr>
        <tr><td>门体</td><td>PVC 涂层软帘</td><td>铝合金或钢质夹芯门板</td></tr>
        <tr><td>抗风</td><td>靠抗风杆约束，能力有限</td><td>门板刚度 + 螺旋导轨，明显更强</td></tr>
        <tr><td>保温</td><td>一般</td><td>夹芯板结构，保温更好</td></tr>
        <tr><td>密封</td><td>毛刷 + 软帘贴合</td><td>门板搭接 + 密封条，缝隙更少</td></tr>
        <tr><td>速度</td><td>常见 1.2–1.5 m/s</td><td>1.0–2.5 m/s，按配置</td></tr>
        <tr><td>造价</td><td>低</td><td>高（门板与导轨成本占比大）</td></tr>
        <tr><td>典型位置</td><td>车间内部通道、洁净区隔断</td><td>外立面、大洞口、高频重载、强风区</td></tr>
      </table></div>
      <p>一句话：<strong>门朝外、洞口大、风压高、要保温，就上硬质；门朝内、只做隔断，软帘够用。</strong></p>
    </section>

    <section>
      <h2>螺旋式与滚筒式，怎么选</h2>
      <h3>螺旋式</h3>
      <p>门板沿螺旋导轨收进门楣上方的“螺旋塔”，不占用洞口两侧空间，运行轨迹平滑，启闭速度快、噪音低，适合高频与重载工况。代价是门楣上方需要更高的安装空间。</p>
      <h3>滚筒式</h3>
      <p>门板卷绕在卷轴上，结构简单、门楣占用小、造价低，适合洞口不高、频率中等的场合。卷径会随门高变大，门洞越高越吃亏。</p>
      <div class="note"><b>选型判断</b>：门楣空间够、每天启闭上百次 → 螺旋式；门楣紧张、预算优先、频率中等 → 滚筒式。这一条比品牌比较更能决定后期好不好用。</div>
    </section>

    <section>
      <h2>门体结构与关键部件</h2>
      <ul>
        <li><strong>门板</strong>：铝合金挤压型材或钢质夹芯板，中间可填聚氨酯保温材料。板间用铰链连接，靠密封条搭接。</li>
        <li><strong>螺旋导轨</strong>：决定运行轨迹与抗风能力，安装精度要求高，土建偏差会直接变成异响和偏磨。</li>
        <li><strong>平衡与驱动</strong>：配重或扭簧平衡门体重量，伺服电机驱动；平衡没调好，电机再大也费劲。</li>
        <li><strong>安全装置</strong>：光电对射、安全底边、防坠落（钢丝绳或链条断裂保护）、急停。</li>
        <li><strong>视窗</strong>：可加透明或采光窗，用于观察与采光；位置和尺寸按使用习惯定，不是越多越好。</li>
      </ul>
    </section>

    <section>
      <h2>典型应用场景</h2>
      <div class="tw"><table>
        <tr><th>行业</th><th>位置</th><th>为什么用硬质</th></tr>
        <tr><td>汽车制造</td><td>焊装、涂装、总装车间通道</td><td>节拍快、通行频繁，门体要抗撞抗风</td></tr>
        <tr><td>环保能源</td><td>垃圾处理厂卸料大厅</td><td>负压与异味控制要求密封，洞口大、风压高</td></tr>
        <tr><td>食品医药</td><td>洁净区外门、原料缓冲</td><td>夹芯板易清洁，密封好，利于维持压差</td></tr>
        <tr><td>冷链物流</td><td>冷库月台、穿堂</td><td>保温与密封直接决定能耗</td></tr>
        <tr><td>工业厂房</td><td>外立面主通道</td><td>抗风、防盗、外观整齐</td></tr>
      </table></div>
    </section>

    <section>
      <h2>参数参考</h2>
      <div class="tw"><table>
        <tr><th>项目</th><th>常规配置区间</th><th>说明</th></tr>
        <tr><td>门板</td><td>铝合金型材 / 钢质夹芯板</td><td>厚度、填充材料按保温要求配置</td></tr>
        <tr><td>适用洞口宽</td><td>2–6 m</td><td>更宽建议评估堆积门或分节提升门</td></tr>
        <tr><td>适用洞口高</td><td>2–6 m</td><td>螺旋式需更高的门楣空间</td></tr>
        <tr><td>开启速度</td><td>1.0–2.5 m/s</td><td>按门体重量与电机配置</td></tr>
        <tr><td>抗风性能</td><td>按项目核算</td><td>检测方法 GB/T 7106-2019，等级判定 GB/T 31433</td></tr>
        <tr><td>安全装置</td><td>光电、安全底边、防坠落</td><td>人员通行位置建议全配</td></tr>
      </table></div>
    </section>

    <section>
      <h2>安装要与土建配合的三件事</h2>
      <ol>
        <li><strong>门楣高度</strong>：螺旋式要留出螺旋塔空间，这一项在土建阶段定，后期改代价最大。</li>
        <li><strong>侧柱与预埋</strong>：导轨受力集中在立柱上，砌体墙需加钢构背衬，不能直接打在空心砖上。</li>
        <li><strong>地坪与排水</strong>：门槛平整度影响密封；卸料大厅、垃圾站这类冲洗频繁的位置，地坪坡度和排水要先做好。</li>
      </ol>
    </section>

    <section>
      <h2>维护重点</h2>
      <p>硬质门的维护重点和软帘门不同：软帘怕撕裂，硬质门怕<strong>导轨偏磨与平衡失调</strong>。每月听一次运行声音、每季度检查铰链与密封条、每半年复核平衡与限位，基本可以把大故障挡在发生之前。门板被叉车撞凹的，单片可换，不必整樘更换。</p>
    </section>""",
    "gallery": [
        ("images/products/hard-rapid-door.jpg", "成都益海嘉里螺旋硬质快速门 — 重庆立高门业", "成都益海嘉里 · 螺旋硬质快速门"),
        ("images/products/hard-rapid-door-2.jpg", "硬质快速门项目实拍 — 重庆立高门业", "益海项目 · 硬质快速门"),
        ("images/products/hard-rapid-door-3.jpg", "昆船集团硬质快速门项目 — 重庆立高门业", "昆船集团 · 硬质快速门"),
    ],
    "faq": [
        ("硬质快速门为什么比软帘贵这么多？",
         "贵在门体和导轨：铝合金型材或夹芯门板、螺旋导轨、平衡系统，材料和加工成本都高于软帘与卷轴。它换来的是抗风、保温、密封和使用寿命，适合门朝外、洞口大、频率高的位置；只做车间内部隔断就没必要上。"),
        ("螺旋式和滚筒式哪个更耐用？",
         "同等使用频率下，螺旋式的运行轨迹更平滑、门板不卷绕，疲劳损伤更小，通常更耐用，但要求门楣空间和安装精度。滚筒式结构简单、维护便宜，适合频率中等的场合。没有绝对的好坏，只有匹配不匹配。"),
        ("加了透明视窗会不会影响强度？",
         "视窗是嵌在门板框架里的，按规范配置不会削弱整体刚度，但开窗面积和位置要合理。观察需求集中在某一高度时，做窄条窗比做大面积更划算。"),
        ("门板被撞了怎么办？",
         "单片门板可以单独更换，不需要整樘报废；导轨变形的要看变形程度，轻微校正、严重更换。这类事故多半发生在叉车贴边通行的位置，加装防撞柱比事后维修更省钱。"),
    ],
    "stds": ["GB/T 7106-2019《建筑外门窗气密、水密、抗风压性能检测方法》",
             "GB/T 31433《建筑幕墙、门窗通用技术条件》（性能等级判定）",
             "JG/T 302-2022《卷帘门窗》"],
    "related": [("rapid-door", "快速门", "PVC软帘，内部通道隔断"),
                ("stacking-door", "堆积门", "超大洞口与高风压"),
                ("lifting-door", "工业滑升门", "保温夹芯板分节门"),
                ("barrier-gate", "道闸", "出入口车辆管理")],
}

# ---------------------------------------------------------------- 3. 堆积门
stack = {
    "slug": "stacking-door", "name": "堆积门", "images": ["stacking-door.jpg"],
    "category": "工业门 / 堆积式快速门",
    "title": "堆积门（抗风堆积式快速门）选型与参数｜重庆立高门业",
    "meta_desc": "堆积门适合超大洞口：折叠堆积原理、横向抗风杆如何分散风压、适用场景与不适用情况、参数区间、安装条件与维护，附东方希望、永川野生动物园等项目实拍。",
    "keywords": "堆积门,抗风堆积门,快速堆积门,大洞口工业门,垃圾站堆积门,重庆堆积门,立高门业",
    "kicker": "折叠堆积 · 横向抗风杆",
    "h1": "堆积门",
    "sub": "超大洞口 · 高风压 · 物流与环保通道",
    "hero_alt": "堆积门 — 重庆立高门业",
    "hero_cap": "堆积门 · 多层帘布结构",
    "lead": "洞口一到十米宽，卷绕方案就开始吃力：卷轴太长会颤，卷径太大顶到门楣，软帘在风里像帆。堆积门的解法是换一种收门方式——门帘向上折叠堆积，而不是卷起来。",
    "badges": ["适合 6 米以上大洞口", "横向抗风杆分散风压", "折叠提升，门楣占用低"],
    "props": [("适用洞口宽", "6–15 m"), ("收门方式", "折叠堆积（非卷绕）"),
              ("抗风", "内置或外置横向抗风杆"), ("速度", "0.5–1.0 m/s（按配置）")],
    "body": """    <section>
      <h2>为什么大洞口要用堆积门</h2>
      <p>卷绕式门在大洞口上有三个绕不过去的物理限制：</p>
      <ul>
        <li><strong>卷轴太长会颤</strong>——门宽超过六米，卷轴跨度变大，转速一高就抖，抖动会传导到轴承和导轨。</li>
        <li><strong>卷径顶门楣</strong>——门越高，卷起来的那一坨越大，门楣空间不够就只能压低门高。</li>
        <li><strong>软帘受风像帆</strong>——大面积软帘在风压下整体鼓出，导轨约束不住中间部分。</li>
      </ul>
      <p>折叠堆积把门帘一段段叠进门楣上方的堆积区，卷轴不再是受力主角；配合横向抗风杆，风压被分散到整幅门帘再传到导轨，这就是它能做大洞口的原因。</p>
    </section>

    <section>
      <h2>抗风是怎么做到的</h2>
      <p>关键在于<strong>横向抗风杆</strong>：每隔一段距离在门帘上穿一根加强杆，杆的两端卡在导轨里。风压作用在门帘上时，力先传到杆，再由杆传到两侧导轨和立柱，而不是全部由帘布自己扛。</p>
      <p>抗风杆有内置和外置两种做法：内置外观整齐、密封好；外置便于更换、抗风更强。风压特别大的位置（山口、沿海、厂房穿堂风），杆的间距要加密、杆径要加大，这些都要按当地基本风压核算，不是套一个“能抗几级风”的口号。</p>
      <div class="note"><b>提醒</b>：任何“可抗 10 级风”的说法都缺少前提——洞口多大、杆距多少、安装在什么位置，结果完全不同。靠谱的做法是按项目核算，并把核算依据写进技术附件。</div>
    </section>

    <section>
      <h2>结构组成</h2>
      <ul>
        <li><strong>门帘</strong>：PVC 涂层织物，多段式，折叠处有加强带。</li>
        <li><strong>抗风杆</strong>：横向贯穿，两端入导轨，是承风主体。</li>
        <li><strong>导轨</strong>：比普通快速门更重，承担风压传递与门帘导向。</li>
        <li><strong>提升机构</strong>：卷扬或链条提升，配重与刹车。</li>
        <li><strong>安全装置</strong>：光电、安全底边、防坠、限位与急停。</li>
      </ul>
    </section>

    <section>
      <h2>适合与不适合</h2>
      <div class="tw"><table>
        <tr><th>场景</th><th>适合度</th><th>说明</th></tr>
        <tr><td>物流园区通道、月台</td><td class="yes">适合</td><td>洞口宽、车辆频繁，折叠提升不占侧向空间</td></tr>
        <tr><td>垃圾中转站、处理厂卸料口</td><td class="yes">适合</td><td>洞口大、需要异味与粉尘隔断，配合负压使用</td></tr>
        <tr><td>大型厂房、钢构车间大门</td><td class="yes">适合</td><td>十米级洞口，卷帘与提升门都吃力</td></tr>
        <tr><td>动物园、养殖场隔离通道</td><td class="yes">适合</td><td>开启快、洞口大，便于车辆与动物转运</td></tr>
        <tr><td>要求严格气密的洁净区</td><td class="mid">谨慎</td><td>折叠结构的密封弱于硬质门板，压差要求高时另选门型</td></tr>
        <tr><td>每天上千次的超高频通道</td><td class="no">不建议</td><td>折叠带是易损点，超高频应选硬质快速门</td></tr>
      </table></div>
    </section>

    <section>
      <h2>参数参考</h2>
      <div class="tw"><table>
        <tr><th>项目</th><th>常规配置区间</th><th>说明</th></tr>
        <tr><td>适用洞口宽</td><td>6–15 m</td><td>超过 15 m 需按结构单独核算</td></tr>
        <tr><td>适用洞口高</td><td>5–10 m</td><td>门楣需留堆积区高度</td></tr>
        <tr><td>开启速度</td><td>0.5–1.0 m/s</td><td>比软帘快速门慢，换取大洞口稳定性</td></tr>
        <tr><td>门帘</td><td>PVC 涂层织物，分段折叠</td><td>可按需加视窗</td></tr>
        <tr><td>抗风</td><td>横向抗风杆，内置/外置</td><td>杆距与杆径按当地风压核算</td></tr>
        <tr><td>控制</td><td>雷达、地磁、遥控、联动</td><td>车辆通行多用雷达+地磁组合</td></tr>
      </table></div>
    </section>

    <section>
      <h2>安装条件</h2>
      <ul>
        <li><strong>门楣堆积区</strong>：折叠后的门帘要堆在门楣上方，高度按门高与折叠段数计算，这一项决定能不能装。</li>
        <li><strong>立柱承载</strong>：大洞口的风压最终落在立柱上，轻钢厂房要核算立柱与檩条的承载。</li>
        <li><strong>导轨基础</strong>：地面导轨槽要顺直，车辆碾压位置建议做保护。</li>
        <li><strong>电源与检修</strong>：提升机构在门楣上方，检修平台或爬梯要提前规划。</li>
      </ul>
    </section>

    <section>
      <h2>维护重点</h2>
      <p>折叠门帘的<strong>折痕处</strong>是最先出问题的地方：反复折叠会出现裂纹，裂纹扩大就是撕裂。建议每季度展开检查折痕与加强带，每半年检查抗风杆是否变形、卡扣是否脱落。风大的地区，每次大风过后巡一次，比按周期保养更有效。</p>
    </section>""",
    "gallery": [
        ("images/products/stacking-door.jpg", "堆积门多层帘布结构 — 重庆立高门业", "堆积门 · 帘布与抗风杆"),
        ("images/projects/dongfang-xiwang.jpg", "东方希望堆积门项目 — 重庆立高门业", "东方希望 · 堆积门 · 2021"),
        ("images/projects/yongchuan-zoo.jpg", "永川野生动物园堆积门项目 — 重庆立高门业", "永川野生动物园 · 堆积门 · 2018"),
    ],
    "faq": [
        ("堆积门和快速门有什么区别？",
         "核心区别在收门方式：快速门把软帘卷在卷轴上，堆积门把门帘折叠堆在门楣上方。前者适合六米以内的通道，后者适合六米以上的大洞口和高风压位置。速度上快速门更快，堆积门胜在洞口适应性和抗风。"),
        ("堆积门真的能抗十级风吗？",
         "不能笼统地说能或不能。抗风能力取决于洞口尺寸、抗风杆间距与杆径、导轨与立柱的承载，同一款门装在不同位置结果不同。正确做法是按项目所在地的基本风压核算，并把核算结果写进技术附件，而不是只看一句宣传语。"),
        ("大洞口为什么不能用卷帘门？",
         "卷轴跨度大就会颤，卷径大门楣装不下，软帘面积大风压下整体鼓出。这三个问题在大洞口会同时出现，所以工业上大洞口普遍改用堆积门、分节提升门或推拉门。"),
        ("日常维护麻烦吗？",
         "不复杂，但要按位置检查。重点是折叠处的折痕、抗风杆的卡扣、导轨里的异物。风大的地区建议大风后巡一次；有条件的每季度做一次完整展开检查。"),
    ],
    "stds": ["JG/T 302-2022《卷帘门窗》",
             "GB/T 7106-2019《建筑外门窗气密、水密、抗风压性能检测方法》",
             "GB/T 31433《建筑幕墙、门窗通用技术条件》"],
    "related": [("rapid-door", "快速门", "PVC软帘，内部通道隔断"),
                ("hard-rapid-door", "硬质快速门", "门板结构，抗风保温"),
                ("lifting-door", "工业滑升门", "保温夹芯板分节门"),
                ("barrier-gate", "道闸", "出入口车辆管理")],
}

# ---------------------------------------------------------------- 4. 工业滑升门
lift = {
    "slug": "lifting-door", "name": "工业滑升门", "images": ["lifting-door.jpg"],
    "category": "工业门 / 分节提升门",
    "title": "工业滑升门（提升门）标准、提升方式与参数｜重庆立高门业",
    "meta_desc": "工业滑升门执行 JG/T 353-2012：标准/高位/垂直三种提升方式怎么选、扭簧平衡与防坠落安全、夹芯板保温密封、维护周期，附仙女山消防队、长安汽研院项目实拍。",
    "keywords": "工业滑升门,工业提升门,分节提升门,保温提升门,消防站提升门,重庆提升门,立高门业",
    "kicker": "分节门板 · 扭簧平衡",
    "h1": "工业滑升门",
    "sub": "厂房仓库 · 消防站 · 汽车 4S 店 · 车库",
    "hero_alt": "工业滑升门 — 重庆立高门业",
    "hero_cap": "分节提升门 · 夹芯板门体",
    "lead": "工业滑升门是有明确行业产品标准的常用工业门类型（JG/T 353-2012），标准管的是门板、平衡、安全这些硬指标；而在实际项目里，决定好不好用的往往是另一件事——提升方式选得对不对。",
    "badges": ["执行 JG/T 353-2012", "夹芯板保温，密封性好", "三种提升方式可选"],
    "props": [("执行标准", "JG/T 353-2012《工业滑升门》"), ("门板", "聚氨酯夹芯板，常规 40 mm"),
              ("提升方式", "标准提升 / 高位提升 / 垂直提升"), ("平衡", "扭簧平衡，配防坠落")],
    "body": """    <section>
      <h2>先看标准：JG/T 353-2012 管什么</h2>
      <p>《工业滑升门》JG/T 353-2012 是建筑工业行业产品标准，2012 年 8 月 1 日实施，适用于工业建筑出入口使用的滑升门，规定了术语与分类、代号标记、一般要求、性能要求、试验方法与检验规则。配套的开门机标准是 JG/T 325《工业滑升门开门机》；卷帘类产品对应的标准则是 JG/T 302-2022《卷帘门窗》，两类不要混用。</p>
      <p>对采购方来说，这份标准最实际的用处是：<strong>验收时有据可依</strong>。门板厚度、平衡性能、安全装置、运行噪声这些都可以对照标准条款核，而不是只听厂家说“我们的门很结实”。</p>
    </section>

    <section>
      <h2>提升方式：这一步决定土建</h2>
      <div class="tw"><table>
        <tr><th>方式</th><th>门体去向</th><th>需要什么条件</th><th>常见位置</th></tr>
        <tr><td>标准提升</td><td>沿导轨上提，门体收在门楣下方</td><td>门楣到顶棚的净高约等于门高</td><td>普通厂房、仓库</td></tr>
        <tr><td>高位提升</td><td>提升高度超过门洞，门体贴近顶棚</td><td>层高较高，需加长导轨与特殊铰链</td><td>层高充裕的车间、需要净空的门洞</td></tr>
        <tr><td>垂直提升</td><td>门体整体垂直上升，不占侧向与前方空间</td><td>门楣上方有完整垂直空间</td><td>消防站、车库、通道进深受限处</td></tr>
      </table></div>
      <p>这一项要在土建阶段定。很多项目是门装完了才发现提升高度不够、门体顶到消防管，只能改门型或改管线，代价远高于提前算一次。</p>
    </section>

    <section>
      <h2>平衡与安全：两个不能省的部分</h2>
      <h3>扭簧平衡</h3>
      <p>分节门体很重，靠扭簧平衡重量，电机只负责克服剩余阻力。扭簧是<strong>有寿命的受力件</strong>，不是装上去就一劳永逸：疲劳断裂会让门体瞬间失去支撑，所以必须按周期检查，并在设计上配防坠落。</p>
      <h3>安全装置</h3>
      <ul>
        <li><strong>防坠落</strong>：钢丝绳或链条断裂时的机械止挡，是滑升门的底线配置。</li>
        <li><strong>底边保护</strong>：门体下行遇阻回弹，保护人员与车辆。</li>
        <li><strong>光电对射</strong>：门洞两侧检测，人员通过时阻止关门。</li>
        <li><strong>手动释放</strong>：停电时用链条或手摇把门打开。</li>
      </ul>
      <div class="note"><b>提醒</b>：扭簧断裂是滑升门最典型的事故来源。验收时要求提供扭簧的设计寿命与更换周期说明，比多要一年保修更实际。</div>
    </section>

    <section>
      <h2>保温与密封：冷库、车间、消防站为什么都用它</h2>
      <p>门板是聚氨酯夹芯板（常规 40 mm），板间靠铰链连接、边缘配密封条，四周再加顶部、侧边、底部三道密封。这决定了它在<strong>保温、隔音、防尘</strong>上明显优于卷帘门和软帘门，也是冷库、洁净车间、消防站车库的常见选择。</p>
      <p>密封效果不只看门板：门槛做法、导轨与墙体的收口、门洞四周的平整度，都会在缝隙上体现出来。同一款门，收口做得好与差，冬天门口的温度能差出一截。</p>
    </section>

    <section>
      <h2>三个常见变体</h2>
      <ul>
        <li><strong>柔性提升门</strong>：门体轻、成本低，适合对保温要求不高的位置。</li>
        <li><strong>透明提升门</strong>：门板带采光窗或整体透光，用于需要自然光的车间与展厅。</li>
        <li><strong>车库提升门</strong>：尺寸与装饰面更接近民用，用于 4S 店、车库、别墅车库。</li>
      </ul>
    </section>

    <section>
      <h2>参数参考</h2>
      <div class="tw"><table>
        <tr><th>项目</th><th>常规配置区间</th><th>说明</th></tr>
        <tr><td>适用洞口宽</td><td>3–8 m</td><td>更宽需按门体重量与导轨核算</td></tr>
        <tr><td>适用洞口高</td><td>3–8 m</td><td>提升方式影响所需净高</td></tr>
        <tr><td>门板</td><td>聚氨酯夹芯板，常规 40 mm</td><td>厚度与钢板厚度按保温要求配置</td></tr>
        <tr><td>平衡</td><td>扭簧平衡</td><td>按周期检查与更换</td></tr>
        <tr><td>驱动</td><td>工业开门机（JG/T 325）</td><td>可配遥控、地磁、门禁联动</td></tr>
        <tr><td>安全</td><td>防坠落、底边保护、光电</td><td>人员通行位置建议全配</td></tr>
      </table></div>
    </section>

    <section>
      <h2>维护：把扭簧当耗材看</h2>
      <div class="tw"><table>
        <tr><th>周期</th><th>项目</th><th>说明</th></tr>
        <tr><td>每月</td><td>运行听音、底边保护测试</td><td>异响多为导轨异物或滚轮磨损</td></tr>
        <tr><td>每季度</td><td>铰链、滚轮、密封条检查</td><td>密封条老化会直接反映在能耗上</td></tr>
        <tr><td>每半年</td><td>钢丝绳、防坠装置、紧固件</td><td>钢丝绳断丝要整根更换，不做局部接续</td></tr>
        <tr><td>按周期</td><td>扭簧检查与更换</td><td>按厂家给的寿命周期执行，不等到断</td></tr>
      </table></div>
    </section>""",
    "gallery": [
        ("images/products/lifting-door.jpg", "工业滑升门分节门体 — 重庆立高门业", "分节提升门 · 夹芯板"),
        ("images/products/lifting-door-2.jpg", "工业滑升门项目实拍 — 重庆立高门业", "工业滑升门 · 车间外门"),
        ("images/projects/xianshan.jpg", "仙女山消防队工业提升门项目 — 重庆立高门业", "仙女山消防队 · 工业提升门 · 2018"),
    ],
    "faq": [
        ("工业滑升门和快速门怎么选？",
         "看频率和保温。每天开合几十次、对保温密封有要求（冷库、洁净区、消防站），选滑升门；每小时十几次以上的高频通道，选快速门。两者的定位不同，很多厂房是外墙用滑升门、内部通道用快速门。"),
        ("扭簧多久要换？",
         "按设计寿命和使用频率算，不能一概而论。高频使用的位置周期短，低频位置周期长。关键是把它列入计划检修：扭簧断裂是突然失效，门体会瞬间失去支撑，靠防坠装置兜底，但不能替代定期更换。"),
        ("提升方式能不能后期改？",
         "很难。提升方式决定了导轨长度、铰链形式、门楣空间和顶棚净高，属于土建阶段就要定的内容。后期改通常要连导轨和门体一起换，成本接近新装。"),
        ("能不能只换门板，保留原有导轨和开门机？",
         "要看原导轨的规格、磨损程度和开门机是否匹配新门体的重量。多数老门改造是门板+平衡系统一起换，开门机视状态决定。这类项目我们会先看现场再报价。"),
    ],
    "stds": ["JG/T 353-2012《工业滑升门》",
             "JG/T 325《工业滑升门开门机》",
             "GB/T 7106-2019《建筑外门窗气密、水密、抗风压性能检测方法》"],
    "related": [("rapid-door", "快速门", "PVC软帘，内部通道隔断"),
                ("hard-rapid-door", "硬质快速门", "门板结构，抗风保温"),
                ("stacking-door", "堆积门", "超大洞口与高风压"),
                ("barrier-gate", "道闸", "出入口车辆管理")],
}

# ---------------------------------------------------------------- 5. 道闸
gate = {
    "slug": "barrier-gate", "name": "道闸", "images": ["barrier-gate.jpg"],
    "category": "出入口设备 / 道闸",
    "title": "道闸（空降闸/广告闸）选型、起落时间与防砸配置｜重庆立高门业",
    "meta_desc": "道闸不只是栏杆：直杆、栅栏、空降闸、广告闸怎么选，起落时间与车流量的关系，地感雷达红外三重防砸，基础施工与联动配置，附万盛煤化项目实拍。",
    "keywords": "道闸,空降闸,广告道闸,车牌识别道闸,工厂大门道闸,重庆道闸,立高门业",
    "kicker": "直杆 · 栅栏 · 空降闸 · 广告闸",
    "h1": "道闸",
    "sub": "工厂大门 · 园区 · 停车场出入口",
    "hero_alt": "道闸（空降闸）— 重庆立高门业",
    "hero_cap": "空降闸 · 红白反光杆体",
    "lead": "道闸常被当成“一根会抬起来的杆”，实际上它是一套出入口系统的执行末端：识别、判断、放行、落杆，四步里任何一步配错，现场就会堵车。选道闸，先选系统，再选杆型。",
    "badges": ["直杆/栅栏/空降/广告四类", "可接车牌识别与访客系统", "地感+雷达+红外防砸"],
    "props": [("类型", "直杆、曲杆、栅栏、空降闸、广告闸"), ("起落时间", "快速 1–2 s，常规 2–6 s"),
              ("防砸", "地感线圈、雷达、红外对射"), ("联动", "车牌识别、访客、考勤、消防")],
    "body": """    <section>
      <h2>道闸在系统里处在什么位置</h2>
      <p>一套完整的出入口系统是这样的：</p>
      <ol>
        <li><strong>识别</strong>——车牌识别一体机、刷卡、人脸或访客二维码。</li>
        <li><strong>判断</strong>——管理软件比对白名单、放行规则、收费规则。</li>
        <li><strong>执行</strong>——道闸抬杆，车辆通过。</li>
        <li><strong>复位</strong>——地感确认车尾离开后落杆，避免砸车。</li>
      </ol>
      <p>道闸属于第三步。很多现场觉得“道闸不好用”，问题其实出在识别率或放行逻辑上；反过来，识别再准，道闸起落太慢也会在早晚高峰堵成一排。</p>
    </section>

    <section>
      <h2>四类杆型，各自适合什么位置</h2>
      <div class="tw"><table>
        <tr><th>类型</th><th>特点</th><th>适合位置</th></tr>
        <tr><td>直杆</td><td>最常见，结构简单，成本低</td><td>车道平整、净宽适中的厂区与停车场</td></tr>
        <tr><td>曲杆（折臂）</td><td>杆体可折，避开低矮顶棚</td><td>地下车库入口、层高受限处</td></tr>
        <tr><td>栅栏</td><td>杆下带栅格，防止行人、动物钻越</td><td>人车混行、需要防钻的园区与厂区</td></tr>
        <tr><td>空降闸</td><td>整体升降的围栏式道闸，抗风与防冲撞更好</td><td>重载车辆出入口、环保能源与化工园区</td></tr>
        <tr><td>广告闸</td><td>杆体带广告位，可对外招商</td><td>商业体、园区主入口（有广告运营需求时）</td></tr>
      </table></div>
      <p>工厂大门和渣土、煤化工这类重载出入口，空降闸更合适：门体整体升降、抗风好，也不像直杆那样容易被大车刮弯。</p>
    </section>

    <section>
      <h2>起落时间怎么定</h2>
      <p>行业里通常把道闸按起落速度分为快速道闸（约 1–2 秒）和普通道闸（约 2–6 秒），这一分级在停车出入口设备的相关技术文件中也是常见口径（参见 GA/T 992《停车库（场）出入口控制设备技术要求》）。</p>
      <p>判断方法很直接：<strong>算高峰期的车流量</strong>。一条车道每小时过 200 辆车，平均 18 秒一辆，2 秒的杆和一个 6 秒的杆差别不大；但如果是一车一杆、还要等识别和抬杆，杆速就会变成排队长度的一部分。反过来，车流很少的内部通道，把钱花在快速杆上不如花在识别率上。</p>
    </section>

    <section>
      <h2>防砸：三重保护缺一不可</h2>
      <ul>
        <li><strong>地感线圈</strong>——埋在杆下方的感应线圈，检测车辆是否还在杆下，是落杆的最后一道判断。</li>
        <li><strong>雷达</strong>——检测移动目标，反应快，适合车流连续通过的场景。</li>
        <li><strong>红外对射</strong>——杆两侧对射，检测行人或异形物体，补地感与雷达的盲区。</li>
      </ul>
      <div class="note"><b>提醒</b>：只装地感是最常见的省成本做法，但地感对行人、非机动车、动物没有保护作用。人车混行的厂区大门，红外或雷达要一起上。</div>
    </section>

    <section>
      <h2>选型要问的五个问题</h2>
      <ol>
        <li><strong>车道多宽、要多长的杆</strong>——杆越长，晃动越大，超过常规长度要考虑栅栏或空降闸。</li>
        <li><strong>要不要广告位</strong>——广告闸的杆体更重，对机芯和基础要求更高。</li>
        <li><strong>识别方式</strong>——车牌、刷卡、人脸、访客码，决定要不要配一体机与软件。</li>
        <li><strong>是否联动</strong>——访客系统、考勤、消防（火警时应自动抬杆）、地磅。</li>
        <li><strong>停电怎么办</strong>——手动离合释放是标配，但要确认现场有人会用、知道在哪。</li>
      </ol>
    </section>

    <section>
      <h2>参数参考</h2>
      <div class="tw"><table>
        <tr><th>项目</th><th>常规配置区间</th><th>说明</th></tr>
        <tr><td>杆长</td><td>直杆 3–6 m</td><td>更长建议栅栏或空降闸</td></tr>
        <tr><td>起落时间</td><td>1–6 s</td><td>快速 1–2 s，常规 2–6 s</td></tr>
        <tr><td>电源</td><td>AC 220 V</td><td>需接地，室外配电箱防雨</td></tr>
        <tr><td>防砸</td><td>地感 + 雷达 / 红外</td><td>人车混行位置建议全配</td></tr>
        <tr><td>联动</td><td>车牌识别、访客、考勤、消防</td><td>按系统方案配置</td></tr>
        <tr><td>机箱</td><td>户外型，按环境选防护</td><td>粉尘、腐蚀环境需加强防护</td></tr>
      </table></div>
    </section>

    <section>
      <h2>施工：基础比设备更容易出问题</h2>
      <ul>
        <li><strong>混凝土基础</strong>：道闸要固定在独立基础上，不能直接打在沥青或回填土上，否则半年就开始歪。</li>
        <li><strong>预埋管</strong>：电源线、网线、地感线要在浇筑前埋好，后期开槽既难看又容易伤线。</li>
        <li><strong>安全岛</strong>：有安全岛的位置，机箱与识别一体机的高度、角度要按驾驶员视线调，不是统一一个高度就行。</li>
        <li><strong>排水</strong>：低洼处机箱进水是雨季最常见的故障。</li>
      </ul>
    </section>

    <section>
      <h2>维护</h2>
      <p>道闸的故障八成集中在三处：<strong>机芯、地感、杆体</strong>。每月检查地感是否误触发、杆体平衡弹簧是否松、螺丝是否松动；每季度清理机箱内灰尘、检查离合与限位；雨季前检查机箱密封与排水。重载出入口的空降闸，导轨与滚轮要单独列保养项。</p>
    </section>""",
    "gallery": [
        ("images/products/barrier-gate.jpg", "空降闸（红白反光杆体）— 重庆立高门业", "空降闸 · 红白反光杆体"),
        ("images/products/barrier-gate-2.jpg", "广告道闸（带广告位）— 重庆立高门业", "广告闸 · 杆体广告位"),
    ],
    "faq": [
        ("道闸起落时间越快越好吗？",
         "不是。杆速要和车流量、识别方式匹配：车流大的主入口，快速杆（1–2 秒）能缩短排队；车流小的内部通道，普通杆（2–6 秒）够用，钱花在识别率上更值。杆速越快，机芯负荷和噪音也越大。"),
        ("只装地感防砸够不够？",
         "不够。地感只能检测金属车辆，对行人、非机动车、小动物基本无效。人车混行的厂区大门、园区入口，应加红外对射或雷达，形成多重保护。"),
        ("空降闸和直杆道闸怎么选？",
         "看重载与抗风。空降闸是整体升降的围栏式门体，抗风好、不易被大车刮弯，适合煤化工、垃圾处理、物流园区这类重载出入口；直杆结构简单、成本低，适合普通厂区与停车场。"),
        ("停电了杆抬不起来怎么办？",
         "配手动离合释放装置，断电后手动抬杆。要点是两个：一是安装时把释放位置和操作方法交代给现场值班人员，二是定期试一次，避免真停电时发现钥匙找不到、机构卡死。"),
    ],
    "stds": ["GA/T 992《停车库（场）出入口控制设备技术要求》",
             "GA/T 1302《停车库（场）安全管理系统技术要求》",
             "GB 50067《汽车库、修车库、停车场设计防火规范》（出入口布置相关）"],
    "related": [("rapid-door", "快速门", "PVC软帘，内部通道隔断"),
                ("hard-rapid-door", "硬质快速门", "门板结构，抗风保温"),
                ("stacking-door", "堆积门", "超大洞口与高风压"),
                ("lifting-door", "工业滑升门", "保温夹芯板分节门")],
}

# ---------------------------------------------------------------- 6. 悬浮门
suspended = {
    "slug": "suspended-door", "name": "悬浮门", "images": ["suspended-door.jpg"],
    "category": "电动大门 / 无轨悬浮门",
    "title": "悬浮门（无轨悬浮大门）选型与参数｜重庆立高门业",
    "meta_desc": "悬浮门怎么选：无地轨的运行原理、适用洞口宽度与门体高度、立柱基础与安装条件、维护周期，附北大医药项目实拍与产品图。重庆本地勘测报价 189-8391-9000。",
    "keywords": "悬浮门,无轨悬浮门,电动悬浮门,悬浮平移门,厂区大门,重庆悬浮门厂家,立高门业",
    "kicker": "无轨悬浮大门",
    "h1": "悬浮门",
    "sub": "厂区主入口 · 园区大门 · 超宽洞口 · 地面无轨",
    "hero_alt": "悬浮门（北大医药项目实拍）— 重庆立高门业",
    "hero_cap": "北大医药 · 无轨悬浮门",
    "lead": "悬浮门最实在的好处是地面不用开槽：门体离地运行，没有预埋导轨，车辆进出不会被轨道硌一下，雨雪天也不容易卡轮。代价是门体、立柱和基础都要按更大的荷载设计——十几米以上的主入口，选它通常比伸缩门更稳。",
    "badges": ["15年自研制造", "无地轨，门体离地运行", "自有安装与维保团队"],
    "props": [("适用洞口宽", "6–30 m（按段数配置）"), ("门体高度", "1.6–1.8 m"),
              ("运行速度", "0.3–0.5 m/s"), ("驱动", "电机 + 齿条/链条"),
              ("控制", "遥控、按钮、车牌识别、门禁联动")],
    "body": """    <section>
      <h2>先判断：这个入口适不适合装悬浮门</h2>
      <p>悬浮门不是“更高级的伸缩门”，两者的结构完全不同：伸缩门靠交叉杆收放、门体落地走轮；悬浮门是整扇门体离地、靠托轮和立柱导向平移。判断标准也就一件事——<strong>洞口宽不宽、地面能不能开槽</strong>。</p>
      <div class="tw"><table>
        <tr><th>现场情况</th><th>适合度</th><th>说明</th></tr>
        <tr><td>厂区主入口，洞口 10 m 以上</td><td class="yes">适合</td><td>门体分段悬挂，超宽洞口比伸缩门更稳，收放不占门口车道</td></tr>
        <tr><td>地面已硬化，不能开槽</td><td class="yes">适合</td><td>无地轨是它最主要的施工优势，安装不动原有地面</td></tr>
        <tr><td>重载车辆、挂车频繁进出</td><td class="yes">适合</td><td>没有轨道可以被压坏，也不会有槽里积泥卡轮的问题</td></tr>
        <tr><td>门口有大坡度或常年积水</td><td class="mid">谨慎</td><td>要核算门体离地间隙与排水，必要时改门型或先做场地处理</td></tr>
        <tr><td>人行小门、3 m 以内的通道</td><td class="no">不建议</td><td>平开门或小尺寸伸缩门更经济</td></tr>
        <tr><td>强风口、山口、沿海位置</td><td class="mid">需核算</td><td>分段方案与立柱基础要按当地风荷载算，不能照搬标准图</td></tr>
      </table></div>
    </section>

    <section>
      <h2>悬浮门靠什么“悬”起来</h2>
      <p>把这五部分搞清楚，报价单上的差别就看得懂了。悬浮门的成本大头不在电机，而在门体分段、立柱和基础——这三项决定它能做多宽、抗多大风。</p>
      <h3>① 门体框架</h3>
      <p>铝合金或钢质型材，按洞口宽度分成若干段拼接。段数越多，单段的悬挑长度越短，运行越稳，但连接件和安装工作量也越多。</p>
      <h3>② 下梁与导向托轮</h3>
      <p>这是“悬浮”的来源：门排下梁由导向托轮支撑，靠杠杆平衡保持门体离地运行。托轮的磨损和调整，直接决定门体运行时会不会下沉、跑偏。</p>
      <h3>③ 立柱与驱动</h3>
      <p>主动立柱里装电机、齿条或链条，以及离合装置。立柱基础是整樘门的受力点，必须按图纸浇筑，不能直接坐在回填土或地砖上。</p>
      <h3>④ 控制与感应</h3>
      <p>遥控、按钮、车牌识别、门禁刷卡、道闸联动，按出入口管理方式组合。有值班室的门口，通常还会加快捷开关和状态指示。</p>
      <h3>⑤ 安全装置</h3>
      <p>红外对射、遇阻停止、防爬。人车混行或夜间无人值守的入口，这几项不是选配，是必需。</p>
    </section>

    <section>
      <h2>选型要问清楚的五件事</h2>
      <ol>
        <li><strong>洞口净宽与分段数</strong>——宽度决定门体分几段、立柱装几根，也决定价格的大头。</li>
        <li><strong>门体高度与净空</strong>——常用 1.6–1.8 m；上方有雨棚、管线或限高的，要先量净空。</li>
        <li><strong>地面条件</strong>——平整度、坡度、排水。无地轨不等于对地面没要求，门体离地运行需要一条平整的通道。</li>
        <li><strong>通行方式</strong>——遥控、车牌识别、门禁、值班室按钮，联动方式在报价阶段就要定。</li>
        <li><strong>抗风要求</strong>——当地基本风压、是否迎风口、门体高度，三项一起决定分段方案和基础尺寸。</li>
      </ol>
    </section>

    <section>
      <h2>参数参考</h2>
      <div class="tw"><table>
        <tr><th>项目</th><th>常规配置区间</th><th>说明</th></tr>
        <tr><td>适用洞口宽</td><td>6–30 m</td><td>更宽按分段与结构核算，不是简单加长</td></tr>
        <tr><td>门体高度</td><td>1.6–1.8 m</td><td>图册悬浮门 01 标注最佳高度 1700 mm</td></tr>
        <tr><td>运行速度</td><td>0.3–0.5 m/s</td><td>按门体长度与配重调整，宽门不宜一味求快</td></tr>
        <tr><td>驱动</td><td>电机 + 齿条/链条</td><td>220 V 单相或 380 V 三相，按现场电源定</td></tr>
        <tr><td>控制方式</td><td>遥控、按钮、车牌识别、门禁</td><td>按出入口管理方式选配</td></tr>
        <tr><td>安全装置</td><td>红外对射、遇阻停止、防爬</td><td>人车混行、夜间无人值守建议全配</td></tr>
        <tr><td>基础</td><td>独立立柱基础</td><td>无地轨，但基础与预埋件要按图纸施工</td></tr>
      </table></div>
    </section>

    <section>
      <h2>安装前，现场要具备什么</h2>
      <ul>
        <li><strong>立柱基础</strong>：混凝土基础与预埋件，强度达到后才能安装；基础位置偏差会直接导致门体跑偏。</li>
        <li><strong>运行通道</strong>：门体悬空经过的地面要平整、无凸起，宽度足够门体运行。</li>
        <li><strong>电源与控制</strong>：电源引到立柱或值班室，控制箱位置要防雨、便于操作。</li>
        <li><strong>排水</strong>：门口低洼处先处理，避免积水影响托轮与电机。</li>
        <li><strong>净空</strong>：门体上方不能有雨棚、管线、树枝，否则运行时干涉。</li>
      </ul>
    </section>

    <section>
      <h2>维护：四件事按周期做</h2>
      <div class="tw"><table>
        <tr><th>周期</th><th>做什么</th><th>为什么</th></tr>
        <tr><td>每月</td><td>听运行声音、看门体有无下沉跑偏、清理运行通道</td><td>托轮异常最先表现为异响和轻微下沉</td></tr>
        <tr><td>每季度</td><td>紧固件复紧、齿条/链条润滑、限位复核</td><td>长门体振动大，固定点松动会累积成故障</td></tr>
        <tr><td>每半年</td><td>电机与控制系统检查、红外与遇阻测试</td><td>安全装置失效往往平时看不出来</td></tr>
        <tr><td>每年</td><td>门体防腐检查、焊缝与连接件检查、基础沉降观察</td><td>户外门体的寿命取决于防腐和基础</td></tr>
      </table></div>
    </section>""",
    "gallery": [
        ("images/products/suspended-door.jpg", "北大医药悬浮门（闭合状态）— 重庆立高门业", "北大医药 · 悬浮门（闭合）"),
        ("images/products/suspended-door-2.jpg", "北大医药悬浮门（运行状态，门体离地无地轨）— 重庆立高门业", "北大医药 · 门体运行状态"),
        ("images/products/suspended-door-3.jpg", "悬浮门 01 产品图（无地轨，门体离地运行）— 重庆立高门业", "产品图 · 悬浮门 01", 1200, 477),
    ],
    "faq": [
        ("悬浮门和伸缩门到底差在哪？",
         "结构不同：伸缩门靠平行四边形交叉杆收放、门体落地走轮；悬浮门是整扇门体离地，靠托轮与立柱导向平移，地面没有轨道。结果就是——超宽洞口、地面不能开槽、重载车辆频繁进出的入口，悬浮门更稳；洞口十来米、预算优先的场合，伸缩门更经济。"),
        ("地面一定要开挖吗？",
         "不需要预埋地轨，这是悬浮门最主要的施工优势。但立柱基础要开挖浇筑，门体运行范围内的地面要平整、能承重；门口是软土或回填土的，基础要按图纸加深处理。"),
        ("大风吹会不会晃？",
         "门体越高、洞口越宽，风的影响越明显。做法是分段控制单段长度、加密立柱与连接件、按当地基本风压核算，而不是照标准图施工。抗风压性能的检测方法见 GB/T 7106-2019，风荷载取值见 GB 50009-2012。"),
        ("停电了门怎么开？",
         "配手动释放装置，断电后可用离合或手摇把门体推到指定位置，不影响车辆通行。有消防或应急通行要求的入口，按项目加装备用电源或联动逻辑。"),
    ],
    "stds": ["GB/T 7106-2019《建筑外门窗气密、水密、抗风压性能检测方法》",
             "GB 50009-2012《建筑结构荷载规范》（风荷载取值）",
             "GB/T 5226.1-2019《机械电气安全 机械电气设备 第1部分：通用技术条件》"],
    "related": [("telescopic-door", "伸缩门", "平行四边形收放，经济型企业大门"),
                ("barrier-gate", "道闸", "出入口车辆管理与车牌识别"),
                ("rapid-door", "快速门", "车间通道隔断与洁净缓冲"),
                ("lifting-door", "工业滑升门", "保温夹芯板，仓库与消防站")],
}

# ---------------------------------------------------------------- 7. 伸缩门
telescopic = {
    "slug": "telescopic-door", "name": "伸缩门", "images": ["telescopic-door.jpg"],
    "category": "电动大门 / 电动伸缩围墙大门",
    "title": "伸缩门（电动伸缩围墙大门）选型与参数｜重庆立高门业",
    "meta_desc": "伸缩门怎么选：有轨与无轨的区别、门体高度与单节宽度、收缩后占地、电机功率与安全配置、安装条件与维护周期，附平安门、富贵门系列产品图。重庆本地勘测报价 189-8391-9000。",
    "keywords": "伸缩门,电动伸缩门,电动围墙大门,铝合金伸缩门,不锈钢伸缩门,厂区大门,重庆伸缩门厂家,立高门业",
    "kicker": "电动伸缩围墙大门",
    "h1": "伸缩门",
    "sub": "企业大门 · 学校 · 园区 · 停车场入口",
    "hero_alt": "伸缩门（蓝白折叠门体）— 重庆立高门业",
    "hero_cap": "产品图 · 蓝白折叠门体",
    "lead": "选伸缩门，先算的不是门洞多宽，而是“收起来占多大地方”。门体一节节叠进机头，收缩后的长度决定门口还能不能停车、值班室摆不摆得下；这件事定了，再谈高度、材质和电机。",
    "badges": ["15年自研制造", "铝合金 / 不锈钢门体", "自有安装与维保团队"],
    "props": [("适用洞口宽", "4–20 m（按节数配置）"), ("门体高度", "1.2–1.8 m"),
              ("单节宽度（轮中）", "450–820 mm"), ("驱动", "220 V 单相电机"),
              ("控制", "遥控、按钮、刷卡、车牌识别联动")],
    "body": """    <section>
      <h2>先判断：伸缩门适合什么入口</h2>
      <p>伸缩门是性价比最高的一类电动大门，但它有两个绕不过去的前提：<strong>门口要有机头位，地面要么能预埋导轨、要么足够平整</strong>。这两条不满足，再便宜的报价也装不顺。</p>
      <div class="tw"><table>
        <tr><th>现场情况</th><th>适合度</th><th>说明</th></tr>
        <tr><td>企业大门、学校、园区主入口</td><td class="yes">适合</td><td>常规 4–15 m 洞口，样式多、造价可控、收放快</td></tr>
        <tr><td>门口一侧有位置放机头</td><td class="yes">适合</td><td>机头约占 1 m 见方，还要留检修空间</td></tr>
        <tr><td>洞口 20 m 以上</td><td class="mid">需对比</td><td>节数多、机头负荷大，建议同时比较悬浮门或段滑门</td></tr>
        <tr><td>重载车辆频繁、地面易沉降</td><td class="mid">谨慎</td><td>地轨容易被压变形，优先考虑无轨或改悬浮门</td></tr>
        <tr><td>强风口、沿海、迎风面开阔</td><td class="mid">需加固</td><td>门体高、节数多时抗风是短板，要加导杆、加密节距</td></tr>
        <tr><td>只走人的小门</td><td class="no">不建议</td><td>用平开门更合适，成本和维护都低</td></tr>
      </table></div>
    </section>

    <section>
      <h2>一樘伸缩门由哪些部分组成</h2>
      <p>伸缩门的钱差在门体节距、型材厚度、机头和导轨上，不在“外观像不像”。把这五部分问清楚，报价单就不会看糊涂。</p>
      <h3>① 门体</h3>
      <p>铝合金型材或不锈钢，靠平行四边形交叉铰接实现收放。型材壁厚、节距和交叉杆的销轴强度，决定门体收放是否顺畅、能用多久。</p>
      <h3>② 走轮与导轨</h3>
      <p>有轨：地面预埋导轨，走轮卡在轨内，直线度和抗风更好，但轨道槽会积灰积水。无轨：靠导向轮与磁导航，地面干净，但对平整度要求高。</p>
      <h3>③ 机头</h3>
      <p>电机、减速机、离合器、控制板都在机头里。机头是整樘门最贵的部件，也是后期维护的主要对象。</p>
      <h3>④ 控制</h3>
      <p>遥控、按钮、刷卡、车牌识别、道闸联动。园区入口常见的做法是伸缩门与道闸、识别相机联动，一套系统管车和门。</p>
      <h3>⑤ 安全装置</h3>
      <p>红外对射、遇阻停止、警示灯，防爬刺按需要选配。人车混行、儿童出入多的学校门口，这几项要配齐。</p>
    </section>

    <section>
      <h2>选型要问清楚的五件事</h2>
      <ol>
        <li><strong>洞口净宽与收缩后长度</strong>——门体收进机头后还有多长，直接决定门口能不能停车。</li>
        <li><strong>门体高度与节距</strong>——常用 1.2–1.8 m；节距越小，收起来越紧凑，但节数更多。</li>
        <li><strong>有轨还是无轨</strong>——看地面能不能开槽、有没有重载车辆压过。</li>
        <li><strong>机头位置与电源</strong>——机头位、检修空间、220 V 电源与控制线管要提前留。</li>
        <li><strong>联动需求</strong>——车牌识别、道闸、值班室开关、消防信号，报价阶段定，后期加装成本高。</li>
      </ol>
    </section>

    <section>
      <h2>参数参考</h2>
      <div class="tw"><table>
        <tr><th>项目</th><th>常规配置区间</th><th>说明</th></tr>
        <tr><td>适用洞口宽</td><td>4–20 m</td><td>超过 20 m 建议对比悬浮门或段滑门</td></tr>
        <tr><td>门体高度</td><td>1.2–1.8 m</td><td>图册各系列标注最佳高度 1200–1600 mm，厂区常用 1.6 m 左右</td></tr>
        <tr><td>单节宽度（轮中）</td><td>450–820 mm</td><td>图册路障 1 号 450 mm，平安门 4 号 760 mm，富贵门 7 号 820 mm</td></tr>
        <tr><td>运行速度</td><td>0.2–0.35 m/s</td><td>按门体长度与机头功率调整</td></tr>
        <tr><td>驱动</td><td>220 V 单相电机，370–750 W</td><td>长门体、重门体选大功率机头</td></tr>
        <tr><td>材质</td><td>铝合金型材 / 不锈钢</td><td>铝合金轻、耐腐蚀；不锈钢更重，适合对外观要求高的门口</td></tr>
        <tr><td>安全装置</td><td>红外对射、遇阻停止、警示灯</td><td>学校、人车混行入口建议配齐</td></tr>
      </table></div>
    </section>

    <section>
      <h2>安装前，现场要具备什么</h2>
      <ul>
        <li><strong>机头位</strong>：门口一侧留出约 1 m 见方的机头位与检修空间，地面要能承重。</li>
        <li><strong>地面与导轨</strong>：有轨方案要预埋导轨并做混凝土基础；无轨方案要求地面平整、无大坡、无大面积破损。</li>
        <li><strong>电源</strong>：机头附近预留 220 V 电源和控制线管，室外要防雨。</li>
        <li><strong>排水</strong>：导轨槽最容易积灰积水，门口要有排水坡。</li>
        <li><strong>门柱与净空</strong>：门柱、围墙、雨棚不能与门体运行轨迹冲突。</li>
      </ul>
    </section>

    <section>
      <h2>维护：四件事按周期做</h2>
      <div class="tw"><table>
        <tr><th>周期</th><th>做什么</th><th>为什么</th></tr>
        <tr><td>每月</td><td>清理导轨槽与走轮杂物、试一遍收放</td><td>砂石卡在轨槽里是门体跑偏和异响的主因</td></tr>
        <tr><td>每季度</td><td>走轮磨损检查、链条润滑、紧固件复紧</td><td>走轮磨偏以后，门体会越跑越歪</td></tr>
        <tr><td>每半年</td><td>电机与离合器检查、红外与遇阻测试</td><td>离合是停电时唯一的手动手段，必须能动作</td></tr>
        <tr><td>每年</td><td>门体防腐与型材检查、机头内部除尘</td><td>户外粉尘和雨水是机头故障的主要来源</td></tr>
      </table></div>
    </section>""",
    "galtitle": "产品图与现场",
    "gallery": [
        ("images/products/telescopic-door.jpg", "伸缩门（蓝白折叠门体）— 重庆立高门业", "产品图 · 蓝白折叠门体"),
        ("images/products/telescopic-door-2.jpg", "平安门 4 号伸缩门产品图（最佳高度 1600 mm）— 重庆立高门业", "产品图 · 平安门 4 号", 1200, 477),
        ("images/products/telescopic-door-3.jpg", "富贵门 7 号伸缩门产品图（最佳高度 1600 mm）— 重庆立高门业", "产品图 · 富贵门 7 号", 1200, 477),
    ],
    "faq": [
        ("有轨和无轨怎么选？",
         "有轨是地面预埋导轨、走轮卡在轨内，直线度和抗风更好；无轨靠导向轮与磁导航，地面干净，适合已硬化、不能开槽的门口。重载车辆频繁、门口有坡的现场，地轨容易变形，建议先看无轨方案，或者直接比较悬浮门。"),
        ("伸缩门能抗几级风？",
         "门体越高、节数越多，迎风面越大。抗风靠型材截面、节距、导杆和机头扭矩一起支撑，不是单看型材厚度。沿海、山口、迎风口的项目要按当地基本风压核算，抗风压检测方法见 GB/T 7106-2019。"),
        ("门体高度一般做多高？",
         "常用 1.2–1.8 m。厂区主入口多为 1.6 m 左右，学校、园区可以做到 1.8 m；图册各系列标注的最佳高度在 1200–1600 mm 之间，具体按洞口宽度、门柱高度和是否需要防爬来定。"),
        ("旧门能不能只换机头或门体？",
         "多数情况可以，但要先核对节距、走轮间距和导轨规格是否匹配。我们会先看现场照片和原门尺寸，再判断是换机头、换门体还是整体更换，避免报了价到现场装不上。"),
    ],
    "stds": ["JG/T 154-2013《电动伸缩围墙大门》（电动伸缩门产品标准）",
             "GB/T 7106-2019《建筑外门窗气密、水密、抗风压性能检测方法》",
             "GB/T 5226.1-2019《机械电气安全 机械电气设备 第1部分：通用技术条件》"],
    "related": [("suspended-door", "悬浮门", "无地轨，超宽洞口更稳"),
                ("barrier-gate", "道闸", "出入口车辆管理与车牌识别"),
                ("stacking-door", "堆积门", "超大洞口与高风压通道"),
                ("rapid-door", "快速门", "车间通道隔断与洁净缓冲")],
}

PAGES = [rapid, hard, stack, lift, gate, suspended, telescopic]

if __name__ == "__main__":
    for p in PAGES:
        path = os.path.join(ROOT, p["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(render(p))
        print("写入", path, os.path.getsize(path) // 1024, "KB")