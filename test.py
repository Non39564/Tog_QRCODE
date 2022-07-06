car = ['Car01','Car02','Car03','Car04','Truck01','Truck02','Truck03','Truck04','Moto01','Moto02']
Car01,Car02,Car03,Car04,Truck01,Truck02,Truck03,Truck04,Moto01,Moto02 = 0,0,0,0,0,0,0,0,0,0
year = []
carsum = [0,0,0,0,0,0,0,0,0,0j]
res = [{'Date': '22-04-2022', 'Container': 'Car01', 'COUNT(*)': 39},
{'Date': '22-04-2022', 'Container': 'Car02', 'COUNT(*)': 1},
{'Date': '22-04-2022', 'Container': 'Moto02', 'COUNT(*)': 2},
{'Date': '22-04-2022', 'Container': 'Truck03', 'COUNT(*)': 1},
{'Date': '22-04-2022', 'Container': 'Truck03', 'COUNT(*)': 4},
{'Date': '23-04-2022', 'Container': 'Truck03', 'COUNT(*)': 1},
{'Date': '23-04-2022', 'Container': 'Truck03', 'COUNT(*)': 4}]

for d in range(len(res)):
    result = dict(res[d])
    day = result.get('Date')
    if day not in year:
        year.append(day)
                
for y in range(len(year)):
    text=['',0,0,0,0,0,0,0,0,0,0]
    for i in range(len(res)):
        result = dict(res[i])
        day = result.get('Date')
        Container = result.get('Container')
        sum = result.get('COUNT(*)')
        if day == year[y]:
            text[0] = day
            if Container in car:
                index = car.index(Container)   
                text[index+1] = text[index+1] + sum
    print(text)
