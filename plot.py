import pandas as pd
import plotly.graph_objects as go
import numpy as np
import calendar

# 1. Load the 10-millennia dataset
filename = 'makar_sankranti_dates_1400BC_12026AD.csv'
df = pd.read_csv(filename)

# 2. Pre-process dates for Y-axis visualization (Seasonal Drift)
# We need to calculate a "Relative Day" where Jan 1 = 0.
# Dates in December will be negative (e.g., Dec 31 = -1), and June will be ~150.
def get_relative_day(row):
    date_str = row['Sankranti_Date']
    year = int(row['Year'])
    
    # Split the date string. Note: handle negative years correctly.
    # Format is YYYY-MM-DD. For negative years, it's -YYYY-MM-DD.
    parts = date_str.split('-')
    if date_str.startswith('-'):
        # e.g. -1400-12-10 -> ['', '1400', '12', '10']
        month = int(parts[2])
        day = int(parts[3])
    else:
        # e.g. 2026-01-14 -> ['2026', '01', '14']
        month = int(parts[1])
        day = int(parts[2])
    
    # Simple cumulative day count (non-leap year basis for consistent Y-axis)
    month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day_of_year = sum(month_days[:month]) + day
    
    if month == 12:
        return day_of_year - 365 # Dec 31 -> 365 - 365 = 0? No, let's align Jan 1 as Day 1.
    return day_of_year

# Refining the relative day: Jan 1 = 1.
def get_refined_relative_day(row):
    date_str = row['Sankranti_Date']
    parts = date_str.split('-')
    if date_str.startswith('-'):
        month = int(parts[2])
        day = int(parts[3])
    else:
        month = int(parts[1])
        day = int(parts[2])
    
    # Days in month for a standard year
    m_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if month == 12:
        # December dates (e.g. Dec 21) should be "before" January.
        # Dec 31 = 0, Dec 30 = -1, ..., Dec 21 = -10, Dec 11 = -20
        return day - 31
    else:
        # Jan 1 = 1, Jan 14 = 14, Feb 1 = 32, ..., June 2 = 31+28+31+30+31+2 = 153
        return sum(m_days[:month]) + day

def get_formatted_day(row):
    date_str = row['Sankranti_Date']
    year = int(row['Year'])
    
    # Split the date string. Note: handle negative years correctly.
    # Format is YYYY-MM-DD. For negative years, it's -YYYY-MM-DD.
    parts = date_str.split('-')
    if date_str.startswith('-'):
        # e.g. -1400-12-10 -> ['', '1400', '12', '10']
        month = int(parts[2])
        day = int(parts[3])
    else:
        # e.g. 2026-01-14 -> ['2026', '01', '14']
        month = int(parts[1])
        day = int(parts[2])

    date_str = f'{calendar.month_abbr[month]} {day}'
    return date_str

df['Relative_Day'] = df.apply(get_refined_relative_day, axis=1)
df['Formatted Day'] = df.apply(get_formatted_day, axis=1)

# 3. Create Interactive Plotly Figure
fig = go.Figure()

# Add the main drift line
fig.add_trace(go.Scatter(
    x=df['Year'],
    y=df['Relative_Day'],
    mode='lines',
    name='Sankranti Drift',
    line=dict(color='#008080', width=1),
    hovertemplate='<b>Year:</b> %{x}<br><b>Calendar Date:</b> %{customdata}',
    customdata=df['Formatted Day']
))

# 4. Add Historical Markers (The "Ages")
markers = [
    {'year': -1399, 'label': 'Vedanga Jyotisha (Uttarayan in Dhanishta)', 'color': '#E67E22'},
    {'year': -45, 'label': 'Julian Calendar', 'color': '#C0392B'},
    {'year': 325, 'label': 'Siddhantic Era (Uttarayan in Makar)', 'color': '#E67E22'},
    {'year': 1582, 'label': 'Gregorian Calendar', 'color': '#C0392B'},
    {'year': 2026, 'label': 'Present Day (Uttarayan in Moola/Dhanu)', 'color': '#27AE60'},
    {'year': 12026, 'label': '10 Millenia Future (June Drift)', 'color': '#2980B9'}
]

for m in markers:
    fig.add_vline(x=m['year'], line_width=1.5, line_dash="dash", line_color=m['color'])
    fig.add_hline(y=-10, line_width=1.5, line_dash="dash", line_color='#C0392B')
    # Finding the y-value for the label position
    y_val = df.loc[df['Year'] == m['year'], 'Relative_Day'].values[0] if m['year'] in df['Year'].values else 0
    fig.add_annotation(
        x=m['year'], 
        y=y_val, 
        text=m['label'], 
        showarrow=True, 
        arrowhead=2, 
        ax=40, ay=-40,
        bgcolor="rgba(255,255,255,0.8)"
    )

# 5. Visual Styling
fig.update_layout(
    title='<b>The 10-Millennia Great Slide: Makar Sankranti Drift (1400 BC - 12026 AD)</b>',
    xaxis_title='Historical Year',
    yaxis_title='Calendar Date (Relative to Jan 1st)',
    template='plotly_white',
    hovermode='x unified',
    xaxis=dict(
        rangeslider=dict(visible=True),
        type='linear'
    ),
    yaxis=dict(
        tickmode='array',
        tickvals=[-20, -10, 1, 14, 32, 60, 91, 121, 152],
        ticktext=['Dec 11', 'Dec 21 (Winter Solstice)', 'Jan 01', 'Jan 14', 'Feb 01', 'Mar 01', 'Apr 01', 'May 01', 'Jun 01']
    )
)

# 6. Save as Interactive HTML
interactive_file = 'index.html'
fig.write_html(interactive_file)

print(f"Interactive dashboard generated: {interactive_file}")
