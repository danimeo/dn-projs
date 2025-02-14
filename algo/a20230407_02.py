
date = input()
yr = int(date[:4])

def filter_(year: int, md: str):
    month, day = int(md[:2]) - 1, int(md[2:4]) - 1
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month < 12:
        if month == 1:
            if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                return (month, day) if day < 29 else (-1, -1)
            else:
                return (month, day) if day < 28 else (-1, -1)
        else:
            return (month, day) if day < days_in_month[month] else (-1, -1)
    else:
        return (-1, -1)

rdates = []
rdate = ()
for y in range(yr, 9000):
    m_d = filter_(y, ''.join(reversed(str(y))))
    # print(m_d)
    # if '{:04d}'.format(y) == '{:02d}{:02d}'.format(m_d[0]+1, m_d[1]+1):
    if m_d != (-1, -1):
        rdates.append((y, m_d))
        if rdate == ():
            rdate = rdates[-1]
    
rdates.sort()
# print(rdates)

for i in range(rdates.index(rdate) + 1, len(rdates)):
    y, m_d = rdates[i]
    print('{:04d}{:02d}{:02d}'.format(y, m_d[0]+1, m_d[1]+1))
    for j in range(i, len(rdates)):
        y, m_d = rdates[j]
        if str(y)[:2] == str(y)[2:]:
            print('{:04d}{:02d}{:02d}'.format(y, m_d[0]+1, m_d[1]+1))
            break
    break

