#!/usr/bin/env python3
"""
立高门业报价单PDF生成器
用法: python3 quote_pdf.py quote-data.json
输出: quote-{客户简称}-{日期}.pdf
"""

import json, sys, os
from datetime import datetime
from fpdf import FPDF

# ============================================================
# 配置
# ============================================================
FONT_PATH = "/mnt/c/Windows/Fonts/msyh.ttc"      # 微软雅黑 (支持中文)
FONT_BOLD = "/mnt/c/Windows/Fonts/msyhbd.ttc"     # 微软雅黑粗体
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

COMPANY = "重庆立高门业有限公司"
ADDRESS = "重庆市巴南区公平场大道845号附17号"
PHONE   = "023-67399080"
MOBILE  = "18983919000"
CONTACT = "郭纪敏"
WEBSITE = "www.ligaomenye.com"

# ============================================================
# PDF 类
# ============================================================
class QuotePDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.add_font("yahei", "", FONT_PATH)
        self.add_font("yahei", "B", FONT_BOLD)
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        pass  # 自定义 header 在 body 里画

    def footer(self):
        self.set_y(-18)
        self.set_font("yahei", "", 7)
        self.set_text_color(150,150,150)
        self.cell(0, 10, f"{COMPANY} · 15年工业门自研品牌 · {PHONE}", align="C")

    def draw_seal(self, x, y):
        """绘制电子公章 (红色圆形)"""
        r = 15  # 半径 mm
        self.set_fill_color(255, 240, 240)
        self.set_draw_color(200, 30, 30)
        self.set_line_width(0.8)
        # 外圆
        self.ellipse(x-r, y-r, 2*r, 2*r, style="DF")
        # 内圆
        self.set_line_width(0.3)
        self.ellipse(x-r+2, y-r+2, 2*(r-2), 2*(r-2), style="D")
        # 五角星
        self.set_fill_color(200, 30, 30)
        star_size = 5
        self.draw_five_star(x, y, star_size)
        # 公司名沿弧 (简化：直接用直排文字)
        self.set_text_color(200, 30, 30)
        self.set_font("yahei", "B", 7)
        self.set_xy(x-13, y+r-8)
        self.cell(26, 5, COMPANY[:8], align="C")
        self.set_xy(x-13, y+r-3)
        self.cell(26, 5, COMPANY[8:], align="C")

    def ellipse(self, x, y, w, h, style=""):
        """画椭圆 (fpdf2 内置方法)"""
        super().ellipse(x, y, w, h, style)

    def draw_five_star(self, cx, cy, size):
        """画简易五角星"""
        import math
        points = []
        for i in range(10):
            angle = math.pi/2 + i * math.pi/5
            r = size if i % 2 == 0 else size * 0.4
            points.append((cx + r * math.cos(angle), cy - r * math.sin(angle)))
        self.set_fill_color(200, 30, 30)
        self.set_draw_color(200, 30, 30)
        self.polygon(points, style="DF")


# ============================================================
# 页面绘制
# ============================================================
def draw_page(pdf, data, page_num=1, total_pages=1):
    """绘制一页报价单"""
    # ── 标题区 ──
    pdf.set_fill_color(26, 58, 92)
    pdf.rect(12, 10, 186, 28, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("yahei", "B", 22)
    pdf.set_xy(16, 14)
    pdf.cell(100, 10, "立高门业报价单")
    pdf.set_font("yahei", "", 9)
    pdf.set_xy(16, 24)
    pdf.cell(100, 8, "专业生产 · 安装工业门 快速门 伸缩门 道闸")

    # ── 公司信息 (右侧) ──
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("yahei", "", 7)
    pdf.set_xy(120, 12)
    pdf.cell(75, 5, f"电话: {PHONE}  |  手机: {MOBILE}", align="R")
    pdf.set_xy(120, 18)
    pdf.cell(75, 5, f"联系人: {CONTACT}  |  {WEBSITE}", align="R")
    pdf.set_xy(120, 24)
    pdf.cell(75, 5, ADDRESS, align="R")

    # ── 客户信息区 ──
    pdf.set_text_color(50, 50, 50)
    pdf.set_font("yahei", "", 9)
    y = 44
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(12, y, 186, 14, "F")
    pdf.set_xy(16, y+2)
    pdf.cell(24, 5, "客户名称:")
    pdf.set_font("yahei", "B", 10)
    pdf.cell(60, 5, data.get("customer", ""))
    pdf.set_font("yahei", "", 9)
    pdf.cell(24, 5, "联系人:")
    pdf.cell(35, 5, data.get("contact", ""))
    pdf.cell(24, 5, "电话:")
    pdf.cell(35, 5, data.get("phone", ""))
    pdf.cell(24, 5, "报价日期:")
    pdf.cell(0, 5, data.get("date", datetime.now().strftime("%Y-%m-%d")), align="R")

    # ── 报价表 ──
    y_start = 62
    col_w = [10, 44, 19, 19, 14, 18, 22, 22, 28]  # 列宽 mm
    headers = ["序号","产品名称","门洞宽\n(mm)","门洞高\n(mm)","数量\n(樘)","面积\n(㎡)","单价\n(元/樘)","金额\n(元)","备注"]
    aligns  = ["C","L","C","C","C","C","R","R","L"]

    # 表头
    pdf.set_fill_color(26, 58, 92)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("yahei", "B", 8)
    x = 12
    for i, (w, hdr) in enumerate(zip(col_w, headers)):
        pdf.set_xy(x, y_start)
        # 多行表头
        lines = hdr.split("\n")
        if len(lines) > 1:
            pdf.multi_cell(w, 5, hdr, border=0, align="C")
        else:
            pdf.cell(w, 10, hdr, border=0, align="C")
        x += w
    pdf.rect(12, y_start, sum(col_w), 10)  # 表头边框

    # 表体
    items = data.get("items", [])
    row_h = 8  # 行高
    max_rows_per_page = 22  # A4 一页大约容纳的行数

    y = y_start + 10
    pdf.set_draw_color(220, 220, 220)
    pdf.set_line_width(0.2)

    total = 0
    for idx, item in enumerate(items):
        if y > 270:  # 超出页面
            break

        row_color = (250, 250, 250) if idx % 2 == 0 else (255, 255, 255)
        pdf.set_fill_color(*row_color)
        pdf.rect(12, y, sum(col_w), row_h, "F")

        pdf.set_text_color(50, 50, 50)
        pdf.set_font("yahei", "", 8)

        values = [
            str(item.get("no", idx+1)),
            item.get("name", ""),
            str(item.get("width", "-")),
            str(item.get("height", "-")),
            str(item.get("qty", "")),
            str(item.get("area", "-")),
            f"{item.get('unit_price',0):,}",
            f"{item.get('amount', item.get('qty',0)*item.get('unit_price',0)):,}",
            item.get("notes", ""),
        ]

        x = 12
        for i, (w, val, al) in enumerate(zip(col_w, values, aligns)):
            pdf.set_xy(x, y+1)
            if al == "R":
                pdf.cell(w-1, 5, val, align="R")
            elif al == "C":
                pdf.cell(w-1, 5, val, align="C")
            else:
                pdf.cell(w-1, 5, val, align="L")
            x += w

        total += item.get("amount", item.get("qty",0)*item.get("unit_price",0))
        y += row_h

    # 合计行
    pdf.set_fill_color(235, 240, 250)
    pdf.set_draw_color(26, 58, 92)
    pdf.set_line_width(0.6)
    pdf.rect(12, y, sum(col_w), 10, "DF")
    pdf.set_text_color(26, 58, 92)
    pdf.set_font("yahei", "B", 10)
    pdf.set_xy(12, y+2)
    pdf.cell(sum(col_w)-col_w[-2]-col_w[-1], 6, "合  计（含13%增值税）", align="R")
    pdf.set_font("yahei", "B", 11)
    pdf.set_text_color(200, 30, 30)
    pdf.cell(col_w[-2]-2, 6, f"{total:,}", align="R")
    pdf.cell(col_w[-1], 6, "")

    y += 14

    # ── 大写金额 + 电子章 ──
    chinese_num = num_to_chinese(total)
    pdf.set_text_color(50, 50, 50)
    pdf.set_font("yahei", "B", 10)
    pdf.set_xy(16, y)
    pdf.cell(100, 6, f"合计（大写）：{chinese_num}")

    # 电子章
    pdf.draw_seal(175, y+22)

    # ── 备注 ──
    y += 12
    pdf.set_font("yahei", "", 7.5)
    pdf.set_text_color(130, 130, 130)
    notes = [
        "备注：",
        "1、以上报价含整套门制作、运输、安装等全部费用；",
        "2、报价不含拆旧门、拆墙、加装门框、门控制箱以上强电布线；",
        "3、以上报价含13%增值税专用发票，本报价有效期30天。",
    ]
    pdf.set_xy(16, y)
    for note in notes:
        pdf.set_x(16)
        pdf.cell(180, 4.5, note)
        pdf.ln()


# ============================================================
# 工具函数
# ============================================================
def num_to_chinese(n):
    """数字转中文大写 (简化版, 万元以内)"""
    digits = "零壹贰叁肆伍陆柒捌玖"
    units = ["", "拾", "佰", "仟"]
    big_units = ["", "万", "亿"]

    if n == 0:
        return "零元整"
    if n >= 100000000:
        return f"{n:,}元整"  # 超范围直接输出数字

    wan = n // 10000
    rest = n % 10000

    def convert_4digit(num):
        if num == 0:
            return "零"
        result = ""
        num_str = f"{num:04d}"
        prev_zero = False
        for i, ch in enumerate(num_str):
            d = int(ch)
            pos = 3 - i
            if d == 0:
                prev_zero = True
            else:
                if prev_zero and result:
                    result += "零"
                result += digits[d] + units[pos]
                prev_zero = False
        return result.rstrip("零")

    result = ""
    if wan > 0:
        result += convert_4digit(wan) + "万"
    if rest > 0:
        w_part = convert_4digit(wan) if wan > 0 else ""
        if w_part and w_part != "零":
            if rest < 1000:
                result += "零"
        result += convert_4digit(rest)

    return result + "元整"


# ============================================================
# Main
# ============================================================
def main():
    if len(sys.argv) < 2:
        print("用法: python3 quote_pdf.py <quote-data.json>")
        print("JSON格式见示例文件")
        sys.exit(1)

    json_path = sys.argv[1]
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pdf = QuotePDF()
    pdf.add_page()
    draw_page(pdf, data)

    # 输出文件名
    customer_short = data.get("customer", "客户")[:6].replace(" ", "")
    date_str = data.get("date", datetime.now().strftime("%Y%m%d")).replace("-", "")
    out_name = f"报价单-{customer_short}-{date_str}.pdf"
    out_path = os.path.join(OUTPUT_DIR, out_name)

    pdf.output(out_path)
    print(f"✅ 报价单已生成: {out_path}")
    print(f"   客户: {data.get('customer')}")
    print(f"   总金额: ¥{sum(i.get('amount', i.get('qty',0)*i.get('unit_price',0)) for i in data.get('items',[])):,}")
    return out_path

if __name__ == "__main__":
    main()
