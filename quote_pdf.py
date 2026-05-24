#!/usr/bin/env python3
"""
立高门业报价单PDF生成器 v2
用法: python3 quote_pdf.py quote-data.json
流程: 填充HTML模板 → WeasyPrint渲染PDF → 输出
"""

import json, sys, os
from datetime import datetime
from weasyprint import HTML

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# HTML 模板
# ============================================================
TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  @page {{ size: A4; margin: 12mm 14mm; }}
  body {{ font-family: "Microsoft YaHei","PingFang SC",sans-serif; color:#333; font-size:12px; line-height:1.6; }}

  /* 顶部蓝色标题栏 */
  .top-bar {{ background:#1a3a5c; color:#fff; padding:10px 16px; display:flex; justify-content:space-between; align-items:center; border-radius:4px 4px 0 0; }}
  .top-bar .title {{ font-size:22px; font-weight:800; letter-spacing:3px; }}
  .top-bar .info {{ font-size:10px; text-align:right; line-height:1.8; }}

  /* 客户信息 */
  .customer {{ padding:8px 16px; background:#f5f5f5; border-bottom:2px solid #1a3a5c; }}
  .customer table {{ width:100%; margin:0; border:none; }}
  .customer td {{ padding:3px 12px; font-size:12px; border:none; text-align:left; }}
  .customer b {{ color:#1a3a5c; }}

  /* 报价表 */
  table.main {{ width:100%; border-collapse:collapse; margin-top:6px; }}
  table.main th {{ background:#1a3a5c; color:#fff; padding:8px 4px; font-size:10px; font-weight:500; border:1px solid #1a3a5c; }}
  table.main td {{ padding:6px 4px; border:1px solid #ccc; text-align:center; font-size:11px; }}
  table.main td.l {{ text-align:left; padding-left:6px; }}
  table.main td.r {{ text-align:right; padding-right:8px; }}
  table.main tr.data:nth-child(even) td {{ background:#fafafa; }}
  table.main tr.total td {{ font-size:13px; font-weight:700; background:#e8f0fa; border-top:2px solid #1a3a5c; }}

  /* 底部 */
  .foot {{ margin-top:16px; display:flex; justify-content:space-between; align-items:flex-end; }}
  .summary {{ font-size:14px; }}
  .summary .big {{ font-size:20px; font-weight:800; color:#d4380d; }}
  .seal-area {{ text-align:center; }}
  .seal-area img {{ width:80px; }}
  .notes {{ font-size:10px; color:#999; margin-top:12px; padding:8px 12px; background:#fafafa; border-radius:4px; line-height:1.8; }}
  .page-foot {{ margin-top:20px; text-align:center; font-size:9px; color:#bbb; border-top:1px solid #eee; padding-top:10px; }}
</style>
</head>
<body>

<div class="top-bar">
  <div class="title">立高门业报价单</div>
  <div class="info">
    重庆立高门业有限公司<br>
    地址：重庆市巴南区公平场大道845号附17号<br>
    电话：023-67399080 | 手机：18983919000 | 联系人：郭纪敏
  </div>
</div>

<div class="customer">
  <table><tr>
    <td><b>客户：</b>{customer}</td>
    <td><b>联系人：</b>{contact}</td>
    <td><b>电话：</b>{phone}</td>
    <td><b>日期：</b>{date}</td>
  </tr></table>
</div>

<table class="main">
  <thead>
    <tr>
      <th style="width:5%">序号</th>
      <th style="width:22%">产品名称</th>
      <th style="width:9%">门洞宽<br>(mm)</th>
      <th style="width:9%">门洞高<br>(mm)</th>
      <th style="width:7%">数量<br>(樘)</th>
      <th style="width:9%">面积<br>(㎡)</th>
      <th style="width:11%">单价<br>(元/樘)</th>
      <th style="width:11%">金额<br>(元)</th>
      <th style="width:17%">备注</th>
    </tr>
  </thead>
  <tbody>
    {items_html}
  </tbody>
  <tr class="total">
    <td colspan="7" style="text-align:right;padding-right:16px;">合  计（含13%增值税）</td>
    <td class="r">{total}</td>
    <td></td>
  </tr>
</table>

<div class="foot">
  <div class="summary">
    合计（大写）：<span class="big">{total_chinese}</span><br>
    <span class="big">¥ {total}</span>
  </div>
  <div class="seal-area">
    <img src="file://{seal_path}" alt="电子章"><br>
    <span style="font-size:9px;color:#999;">报价专用章</span>
  </div>
</div>

<div class="notes">
  <b>备注：</b><br>
  1、以上报价含整套门制作、运输、安装等全部费用；<br>
  2、报价不含拆旧门、拆墙、加装门框、门控制箱以上强电布线；<br>
  3、以上报价含13%增值税专用发票，本报价有效期30天。
</div>

<div class="page-foot">
  重庆立高门业有限公司 · 15年工业门自研品牌 · 023-67399080
</div>

</body>
</html>"""

# ============================================================
# 工具函数
# ============================================================
def num_to_chinese(n):
    digits = "零壹贰叁肆伍陆柒捌玖"
    units = ["", "拾", "佰", "仟"]
    if n == 0:
        return "零元整"
    if n >= 100000000:
        return f"{n:,}元整"
    wan = n // 10000
    rest = n % 10000
    def conv4(num):
        if num == 0: return "零"
        s = f"{num:04d}"
        r, pz = "", False
        for i, ch in enumerate(s):
            d = int(ch); pos = 3 - i
            if d == 0: pz = True
            else:
                if pz and r: r += "零"
                r += digits[d] + units[pos]; pz = False
        return r.rstrip("零")
    result = ""
    if wan > 0: result += conv4(wan) + "万"
    if rest > 0:
        if wan > 0 and rest < 1000: result += "零"
        result += conv4(rest)
    return result + "元整"


# ============================================================
# Main
# ============================================================
def main():
    if len(sys.argv) < 2:
        print("用法: python3 quote_pdf.py <quote-data.json>")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)

    # 生成表格行
    items_html = ""
    total = 0
    for item in data.get("items", []):
        no = item.get("no", "")
        name = item.get("name", "")
        w = item.get("width", "-")
        h = item.get("height", "-")
        qty = item.get("qty", "")
        area = item.get("area", "-")
        up = item.get("unit_price", "")
        amt = item.get("amount", 0)
        if amt == 0 and qty and up:
            amt = int(qty) * int(up)
        notes = item.get("notes", "")
        total += amt

        up_str = f"{up:,}" if isinstance(up, int) and up > 0 else str(up)
        amt_str = f"{amt:,}"
        area_str = str(area)
        qty_str = str(qty)

        items_html += (
            f'<tr class="data"><td>{no}</td><td class="l">{name}</td>'
            f'<td>{w}</td><td>{h}</td><td>{qty_str}</td><td>{area_str}</td>'
            f'<td class="r">{up_str}</td><td class="r">{amt_str}</td>'
            f'<td class="l">{notes}</td></tr>\n'
        )

    # 填充模板
    seal_path = os.path.join(SCRIPT_DIR, "images/seal.png").replace("\\", "/")
    html = TEMPLATE.format(
        customer=data.get("customer", ""),
        contact=data.get("contact", ""),
        phone=data.get("phone", ""),
        date=data.get("date", datetime.now().strftime("%Y-%m-%d")),
        items_html=items_html,
        total=f"{total:,}",
        total_chinese=num_to_chinese(total),
        seal_path=seal_path,
    )

    # 渲染PDF
    customer_short = data.get("customer", "客户")[:6].replace(" ", "")
    date_str = data.get("date", datetime.now().strftime("%Y%m%d")).replace("-", "")
    out_name = f"报价单-{customer_short}-{date_str}.pdf"
    out_path = os.path.join(SCRIPT_DIR, out_name)

    HTML(string=html).write_pdf(out_path)

    print(f"✅ 报价单已生成: {out_path}")
    print(f"   客户: {data.get('customer')}")
    print(f"   总金额: ¥{total:,}")
    return out_path


if __name__ == "__main__":
    main()
