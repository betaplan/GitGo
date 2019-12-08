from src.EquityLib import Market
a = Market()
b = a.get_url_lists(0,a.get_pages_counts())
c = a.get_tickers_ex(b)
d = list(c)
for i in range(len(d)):
    try:
        df = a.loadData('cn_stock_163',d[i])
        df1 = df.drop_duplicates('名称', keep='last')
        df1.to_csv('my_csv.csv', mode='a', header=False)
    except:
        print("No data for ", d[i])
