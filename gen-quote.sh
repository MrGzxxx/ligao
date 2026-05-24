#!/bin/bash
# 立高门业报价单快速生成
# 用法: ./gen-quote.sh <客户简称> <联系人> <电话>
# 示例: ./gen-quote.sh 赛力斯 张工 13888886666

VENV=/home/lenovo_he/.hermes/venv/bin/python
SCRIPT=$(dirname "$0")/quote_pdf.py
DATA_DIR=$(dirname "$0")

CLIENT="${1:-测试客户}"
CONTACT="${2:-联系人}"
PHONE="${3:-电话}"
DATE=$(date +%Y-%m-%d)

# 生成默认JSON
cat > "$DATA_DIR/_tmp_quote.json" << EOF
{
  "customer": "$CLIENT",
  "contact": "$CONTACT",
  "phone": "$PHONE",
  "date": "$DATE",
  "items": [
    {"no": 1, "name": "快速门（PVC软帘）", "width": "", "height": "", "qty": "", "area": "", "unit_price": "", "amount": "", "notes": ""},
    {"no": 2, "name": "", "width": "", "height": "", "qty": "", "area": "", "unit_price": "", "amount": "", "notes": ""}
  ]
}
EOF

echo "📝 请编辑 $DATA_DIR/_tmp_quote.json 填入产品明细后运行："
echo "   $VENV $SCRIPT $DATA_DIR/_tmp_quote.json"
