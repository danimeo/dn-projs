
date = input()
dates = [date]
months = list(range(12))
days = list(range(31))
abn = False

month, day = int(date[4:6]) - 1, int(date[6:8]) - 1
for m in range(month, month + 12):
    m %= 12
    for d in range(day + 1, day + 31):
        d %= 31
        year = ''.join(reversed('{:02d}{:02d}'.format(m+1, d+1)))
        print('{}{:02d}{:02d}'.format(year, m+1, d+1))
        if 1000 <= int(year) < 9000:
            # dates.append('{}{:02d}{:02d}'.format(year, m+1, d+1))
            # print('{}{:02d}{:02d}'.format(year, m+1, d+1))
            abn = True
            break
    if abn:
        break


# dates.sort()
# print(dates)
# print(dates[dates.index(date) + 1])
