data = "1113222113"
for step in range(40):
    new_data = ""
    start = 0
    for i in range(len(data) + 1):
        if i >= len(data) or data[i] != data[start]:
            next_start = i
            new_data += f"{next_start-start}{data[start]}"
            start = next_start
    data = new_data
print(len(data))
