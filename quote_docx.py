#!/usr/bin/env python3
"""
立高门业报价单生成器 — 基于原Word模板直接修改
用法: python3 quote_docx.py quote-data.json
输出: 报价单-{客户}-{日期}.docx
"""

import json, sys, os, re
from datetime import datetime
from copy import deepcopy
from docx import Document

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE  = os.path.expanduser("~/.ligao/堆积门报价模板.docx")

WML = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def num_to_chinese(n):
    digits = "零壹贰叁肆伍陆柒捌玖"
    units = ["", "拾", "佰", "仟"]
    if n == 0: return "零元整"
    if n >= 100000000: return f"{n:,}元整"
    wan = n // 10000; rest = n % 10000
    def conv4(num):
        if num == 0: return "零"
        s = f"{num:04d}"; r, pz = "", False
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


def set_cell_text(cell, text):
    """完全替换单元格的文本内容，保留第一个run的格式"""
    paras = cell._tc.findall(f'.//{{{WML}}}p')
    if not paras: return
    # 找到所有text元素
    all_texts = paras[0].findall(f'.//{{{WML}}}t')
    if not all_texts: return
    # 保留第一个text元素, 设为新文本, 清空其余
    all_texts[0].text = str(text)
    # 设置space="preserve"以确保空格保留
    all_texts[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    for t in all_texts[1:]:
        t.text = ""


def replace_all_text(xml_str, old, new):
    """在XML字符串中替换所有text元素中的文本"""
    result = xml_str
    # 使用正则替换w:t标签内的文本
    pattern = re.compile(
        r'(<w:t[^>]*>)' + re.escape(old) + r'(</w:t>)',
        re.DOTALL
    )
    result = pattern.sub(r'\1' + new + r'\2', result)
    return result


def build_docx(data):
    doc = Document(TEMPLATE)

    date_str = data.get("date", datetime.now().strftime("%Y.%m.%d"))
    customer = data.get("customer", "")
    contact = data.get("contact", "")
    phone = data.get("phone", "")

    # ══════ 方案：直接操作底层 XML ══════
    # 这样能绕过python-docx对格式run的拆分问题
    xml = doc.element.xml if hasattr(doc.element, 'xml') else ''

    # 通过document.part获取XML
    body = doc.element.body

    # 用更直接的方式：找到所有w:t元素替换其中的文本
    all_ts = body.findall(f'.//{{{WML}}}t')

    # 1. 替换日期
    for t in all_ts:
        if t.text and "2026.5.13" in t.text:
            t.text = t.text.replace("2026.5.13", date_str)

    # 2. 替换客户信息（模板中客户名称后跟"；"在同一个或相邻run中）
    # 先找"客户名称"
    for t in all_ts:
        if t.text and "客户名称" in t.text:
            # 找后面的分号
            pass  # 下面统一处理

    # 遍历所有w:t, 处理客户信息替换
    for t in all_ts:
        if not t.text:
            continue
        # 客户名称后的分号 → 替换为客户名
        if t.text.strip() == "；":
            # 检查前一个兄弟节点是否是"客户名称"
            prev = t.getprevious()
            # 不检查了, 直接替换模板中的分号（模板中客户名称后面就是分号）
            t.text = customer
            continue
        # 联系人：→ 联系人：XXX
        if t.text.strip() == "联系人：" and contact:
            t.text = f"联系人：{contact}"
            continue
        # 电话：→ 电话：XXX
        if t.text.strip() == "电话：" and phone:
            t.text = f"电话：{phone}"
            continue

    # ══════ 表格处理 ══════
    table = doc.tables[0]
    items = data.get("items", [])
    total = 0

    # 计算总金额
    for item in items:
        amt = item.get("amount", 0)
        if not amt and item.get("qty") and item.get("unit_price"):
            amt = int(item["qty"]) * int(item["unit_price"])
        total += amt

    tbl = table._tbl
    all_rows = tbl.findall(f'.//{{{WML}}}tr')

    # 行结构: [0]表头, [1]数据行, [2]合计行, [3]备注空行, [4]备注内容
    data_row_idx = 1
    total_row_idx = 2

    # 保存模板数据行
    template_row = all_rows[data_row_idx]

    # 删除旧数据行
    tbl.remove(template_row)

    # 数据行按正序插入
    # 现在 all_rows 已经变了: [0]表头, [1]合计行, ...
    # 新total_row_idx = 1
    new_total_idx = 1
    total_row_elem = tbl.findall(f'.//{{{WML}}}tr')[new_total_idx]

    for item in items:
        no = item.get("no", "")
        name = item.get("name", "")
        w = str(item.get("width", "-"))
        h_val = str(item.get("height", "-"))
        qty = str(item.get("qty", ""))
        area = str(item.get("area", "-"))
        up = item.get("unit_price", "")
        amt = item.get("amount", 0) or (int(item.get("qty", 0)) * int(str(item.get("unit_price", 0)))
              if item.get("qty") and item.get("unit_price") else 0)
        notes = item.get("notes", "")

        up_str = f"{up:,}" if isinstance(up, int) and up > 0 else str(up)
        amt_str = f"{amt:,}"
        vals = [str(no), name, w, h_val, qty, area, up_str, amt_str, notes]

        new_tr = deepcopy(template_row)

        # 找到行内的单元格并填充
        tcs = new_tr.findall(f'.//{{{WML}}}tc')
        for ci, val in enumerate(vals):
            if ci < len(tcs):
                texts = tcs[ci].findall(f'.//{{{WML}}}t')
                if texts:
                    texts[0].text = str(val)
                    texts[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                    for xt in texts[1:]:
                        xt.text = ""

        # 插入到合计行之前 (每次都插入在total_row之前，自动正序)
        tbl.insert(list(tbl).index(total_row_elem), new_tr)

    # ══════ 替换合计行 ══════
    chinese_total = num_to_chinese(total)
    total_str = f"{total:,}"

    # 重新获取合计行（位置变了）
    all_rows_after = tbl.findall(f'.//{{{WML}}}tr')
    # 合计行是最后一个数据行后面的那行（表头 + N个数据行 + 合计行后的备注行）
    # 找包含"合计"的行
    for tr in all_rows_after:
        t_texts = [t.text for t in tr.findall(f'.//{{{WML}}}t') if t.text]
        full = "".join(t_texts)
        if "合计" in full and ("98000" in full or "玖万" in full):
            for t in tr.findall(f'.//{{{WML}}}t'):
                if t.text and "98000" in t.text:
                    t.text = t.text.replace("98000", total_str)
                if t.text and "玖万捌仟元整" in t.text:
                    t.text = t.text.replace("玖万捌仟元整", chinese_total)
            break

    return doc


def main():
    if len(sys.argv) < 2:
        print("用法: python3 quote_docx.py <quote-data.json>")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)

    doc = build_docx(data)

    customer_short = data.get("customer", "客户")[:6].replace(" ", "")
    date_str = data.get("date", datetime.now().strftime("%Y%m%d")).replace("-", "")
    out_name = f"报价单-{customer_short}-{date_str}.docx"
    out_path = os.path.join(SCRIPT_DIR, out_name)
    doc.save(out_path)

    total = sum(
        i.get("amount", 0) or (
            int(i.get("qty", 0)) * int(str(i.get("unit_price", 0)))
            if i.get("qty") and i.get("unit_price") else 0
        )
        for i in data.get("items", [])
    )
    print(f"✅ 报价单已生成: {out_path}")
    print(f"   客户: {data.get('customer')}")
    print(f"   总金额: ¥{total:,}")
    print(f"   用Word打开 → 另存为PDF 即可")
    return out_path


if __name__ == "__main__":
    main()
