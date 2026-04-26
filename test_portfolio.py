from investment.portfolio import Portfolio

p = Portfolio(3000000)

p.buy("7203.T", 3000, 300000)
p.summary()

p.sell("7203.T", 3200)
p.summary()
