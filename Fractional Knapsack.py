def fractionalKnapsack(val, wt, capacity):
    item = []
    for i in range(len(val)):
        item.append([val[i],wt[i],val[i]/wt[i]])
    item.sort(key=lambda x:x[2], reverse=True)
    total = 0
    capacityleft = capacity
    for j in item:
        if j[1]<capacityleft:
            total+=j[0]
            capacityleft-=j[1]
        else:
            total+=(capacityleft/j[1]) * j[0]
            break
    return total
