import pandas as pd

# Reference parameters from previous successful runs
jd_ref = 2460324.0 + 0.38541666666 + 0.5 
sidereal_year = 365.256363

def jd_to_date(jd):
    jd = jd + 0.5
    z = int(jd)
    f = jd - z
    if z < 2299161:
        a = z
    else:
        alpha = int((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - int(alpha / 4)
    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    day = b - d - int(30.6001 * e) + f
    if e < 14:
        month = e - 1
    else:
        month = e - 13
    if month > 2:
        year = c - 4716
    else:
        year = c - 4715
    return year, month, int(day)

# Range: 1400 BC (-1399) to 5026 AD
start_year = -1399
end_year = 12026
data = []
for y in range(start_year, end_year + 1):
    diff = y - 2024
    jd_moment = jd_ref + (diff * sidereal_year)
    yr, mo, dy = jd_to_date(jd_moment)
    date_str = f"{yr}-{mo:02d}-{dy:02d}"
    data.append({'Year': yr, 'Sankranti_Date': date_str})

df_millenia = pd.DataFrame(data)
output_file = 'makar_sankranti_dates_1400BC_12026AD.csv'
df_millenia.to_csv(output_file, index=False)

print(f"CSV generated: {output_file}")
print(f"First 5 entries:\n{df_millenia.head()}")
print(f"Last 5 entries:\n{df_millenia.tail()}")
