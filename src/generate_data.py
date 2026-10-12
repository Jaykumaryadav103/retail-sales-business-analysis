"""Create the deterministic, fictional 1,200-row order dataset for this project."""
from pathlib import Path
import csv, random
from datetime import date, timedelta

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'orders.csv'; OUT.parent.mkdir(exist_ok=True)
r=random.Random(27)
products={
 'Home & Kitchen':[('Steel Bottle',499,220),('Storage Set',899,410),('Desk Lamp',1299,670)],
 'Electronics':[('Wireless Mouse',799,340),('USB Hub',1199,510),('Earbuds',1799,850)],
 'Fashion':[('Cotton T-shirt',599,260),('Backpack',1499,720),('Sneakers',2499,1320)],
 'Beauty':[('Face Wash',349,125),('Skin Care Kit',999,430),('Hair Dryer',1899,940)]}
regions=['North','South','East','West']; channels=['Organic','Paid Search','Social','Email']
fields=['order_id','order_date','region','category','product','sales_channel','units','unit_price_inr','discount_pct','unit_cost_inr','order_status','customer_type']
with OUT.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
 for i in range(1,1201):
  category=r.choices(list(products),weights=[30,26,24,20])[0]; product,price,cost=r.choice(products[category])
  w.writerow({'order_id':f'ORD-{i:05d}','order_date':(date(2025,1,1)+timedelta(days=r.randrange(365))).isoformat(),
   'region':r.choice(regions),'category':category,'product':product,'sales_channel':r.choice(channels),
   'units':r.choices([1,2,3,4],weights=[62,25,10,3])[0],'unit_price_inr':price,
   'discount_pct':r.choices([0,.05,.10,.15,.20],weights=[35,20,25,15,5])[0], 'unit_cost_inr':cost,
   'order_status':r.choices(['Delivered','Cancelled','Returned'],weights=[91,5,4])[0],
   'customer_type':r.choices(['New','Returning'],weights=[64,36])[0]})
print(f'Generated {OUT} with 1,200 synthetic records.')

