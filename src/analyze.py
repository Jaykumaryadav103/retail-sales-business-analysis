"""Rebuild portfolio KPI exports, business findings, and SVG chart."""
from pathlib import Path
from html import escape
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
REPORTS = ROOT / 'reports'
REPORTS.mkdir(exist_ok=True)
df = pd.read_csv(DATA / 'orders.csv')
required = {'order_id','order_date','region','category','sales_channel','units','unit_price_inr','discount_pct','unit_cost_inr','order_status'}
missing = required - set(df.columns)
if missing:
    raise ValueError(f'Missing required columns: {sorted(missing)}')
if df.order_id.duplicated().any():
    raise ValueError('Duplicate order IDs found')
if df[['order_date','region','category','order_status']].isna().any().any():
    raise ValueError('Required fields contain missing values')
if (df.units <= 0).any() or (~df.discount_pct.between(0,1)).any():
    raise ValueError('Invalid units or discount values')

df['net_sales_inr'] = df.units * df.unit_price_inr * (1-df.discount_pct)
df['gross_profit_inr'] = df.net_sales_inr - df.units * df.unit_cost_inr
deliv = df[df.order_status.eq('Delivered')].copy()
deliv['month'] = pd.to_datetime(deliv.order_date).dt.to_period('M').astype(str)
monthly = deliv.groupby('month',as_index=False).agg(orders=('order_id','nunique'),net_sales_inr=('net_sales_inr','sum'),gross_profit_inr=('gross_profit_inr','sum'))
category = deliv.groupby('category',as_index=False).agg(orders=('order_id','nunique'),net_sales_inr=('net_sales_inr','sum'),gross_profit_inr=('gross_profit_inr','sum'))
channel = deliv.groupby('sales_channel',as_index=False).agg(orders=('order_id','nunique'),net_sales_inr=('net_sales_inr','sum'),gross_profit_inr=('gross_profit_inr','sum'))
for result,name in [(monthly,'monthly_kpis.csv'),(category,'category_performance.csv'),(channel,'channel_performance.csv')]:
    result['gross_margin_pct'] = result.gross_profit_inr / result.net_sales_inr * 100
    result.to_csv(REPORTS/name,index=False)

best=monthly.loc[monthly.net_sales_inr.idxmax()]; worst=monthly.loc[monthly.net_sales_inr.idxmin()]
topcat=category.loc[category.net_sales_inr.idxmax()]; topchannel=channel.loc[channel.net_sales_inr.idxmax()]
returned=100*df.order_status.eq('Returned').mean(); cancelled=100*df.order_status.eq('Cancelled').mean()
sales=deliv.net_sales_inr.sum()
report=f'''# Business findings (synthetic practice data)\n\n## Executive summary\n- Delivered orders: **{len(deliv):,}** of {len(df):,} records.\n- Delivered net sales: **INR {sales:,.0f}** after discounts.\n- Highest-sales month: **{best.month}** (INR {best.net_sales_inr:,.0f}); lowest: **{worst.month}** (INR {worst.net_sales_inr:,.0f}).\n- Largest sales category: **{topcat.category}** (INR {topcat.net_sales_inr:,.0f}).\n- Largest sales channel: **{topchannel.sales_channel}** (INR {topchannel.net_sales_inr:,.0f}).\n- QA: {returned:.1f}% returned and {cancelled:.1f}% cancelled records; excluded from delivered-sales KPIs.\n\n## Recommended next steps\n1. Compare sales dips with promotion calendar, stock availability, and traffic. These explanatory fields are absent, so this dataset cannot establish causes.\n2. Compare channel profit and margin, not just sales, before changing marketing spend.\n3. Track return and cancellation rates by category and region in live data.\n4. Confirm order-status definitions with operations before using these KPIs in a real business review.\n\n## Metric definitions\n- **Delivered net sales** = units × unit price × (1 − discount), delivered orders only.\n- **Estimated gross profit** = delivered net sales − units × unit cost. Excludes shipping, marketing, tax, and overhead; not accounting profit.\n- **Return/cancellation rate** = records in that status ÷ all records.\n\n## Limitations\nAll records are synthetic and do not describe an actual retailer. Costs, discounts, order mix, and seasonality are simulated. Findings are descriptive and do not prove causation.\n'''
(REPORTS/'business_findings.md').write_text(report,encoding='utf-8')

colors=['#176B87','#64CCC5','#3B82A0','#8ECAE6']; W,H=1000,430
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="#fff"/>','<style>text{font-family:Arial,sans-serif;fill:#183b4e}.title{font-size:19px;font-weight:bold}.label{font-size:12px}.axis{stroke:#b8c7ce}</style>','<text x="35" y="34" class="title">Monthly delivered net sales (INR lakh)</text>','<text x="535" y="34" class="title">Delivered net sales by category (INR lakh)</text>']
x0,y0,pw,ph=45,350,410,260; maxm=max(monthly.net_sales_inr/100000); pts=[]
for i,row in monthly.reset_index(drop=True).iterrows():
    x=x0+i*pw/max(1,len(monthly)-1); y=y0-(row.net_sales_inr/100000)/maxm*ph; pts.append(f'{x:.1f},{y:.1f}')
    svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#176B87"/><text x="{x-14:.1f}" y="{y0+22}" class="label">{row.month[5:]}</text>')
svg.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#176B87" stroke-width="3"/>')
bx,by,bw,bh=550,350,400,260; slot=bw/len(category); maxc=max(category.net_sales_inr/100000)
for i,row in category.reset_index(drop=True).iterrows():
    barh=row.net_sales_inr/100000/maxc*bh; x=bx+i*slot+12; y=by-barh
    svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{slot-24:.1f}" height="{barh:.1f}" rx="4" fill="{colors[i%len(colors)]}"/>')
    svg.append(f'<text x="{x-4:.1f}" y="{by+20}" class="label">{escape(row.category)}</text>')
svg.append('</svg>'); (REPORTS/'sales_overview.svg').write_text('\n'.join(svg),encoding='utf-8')
print(f'Processed {len(df)} rows; {len(deliv)} delivered orders; INR {sales:,.0f} net sales')

