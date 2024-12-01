data = list(map(int, "1113222113"))
for step in range(50):
    new_data = []
    start = 0
    for i in range(len(data) + 1):
        if i >= len(data) or data[i] != data[start]:
            next_start = i
            new_data.append(next_start - start)
            new_data.append(data[start])
            start = next_start
    data = new_data
print(len(data))
