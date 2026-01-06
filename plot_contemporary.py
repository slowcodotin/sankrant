import pandas as pd
import plotly.graph_objects as go
import numpy as np
import calendar

# 1. Load the 10-millennia dataset
filename = 'makar_sankranti_dates_1400BC_12026AD.csv'
df = pd.read_csv(filename)

# 2. Filter for the requested range: 1400 BCE (-1399) to 2500 CE
df = df[(df['Year'] >= -1399) & (df['Year'] <= 2500)].copy()

# Pre-process dates for Y-axis visualization (Seasonal Drift)
def get_refined_relative_day(row):
    date_str = row['Sankranti_Date']
    parts = date_str.split('-')
    if date_str.startswith('-'):
        # Negative year handling: -1400-12-10 -> ['', '1400', '12', '10']
        month = int(parts[2])
        day = int(parts[3])
    else:
        # Positive year handling: 2026-01-14 -> ['2026', '01', '14']
        month = int(parts[1])
        day = int(parts[2])
    
    m_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if month == 12:
        # December dates (e.g. Dec 21) are "before" Jan 1
        return day - 31
    else:
        # Jan 1 = 1, Jan 14 = 14, etc.
        return sum(m_days[:month]) + day

def get_formatted_day(row):
    date_str = row['Sankranti_Date']
    parts = date_str.split('-')
    if date_str.startswith('-'):
        month = int(parts[2])
        day = int(parts[3])
    else:
        month = int(parts[1])
        day = int(parts[2])

    return f'{calendar.month_abbr[month]} {day}'

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
    line=dict(color='#008080', width=1.5),
    hovertemplate='<b>Year:</b> %{x}<br><b>Calendar Date:</b> %{customdata}',
    customdata=df['Formatted Day']
))

# 4. Add Historical Markers (The "Ages")
markers = [
    {'year': -1399, 'label': 'Vedanga Jyotisha (Uttarayan in Dhanishta)', 'color': '#E67E22'},
    {'year': -45, 'label': 'Julian Calendar', 'color': '#C0392B'},
    {'year': 325, 'label': 'Siddhantic Era (Uttarayan in Makar)', 'color': '#E67E22'},
    {'year': 1582, 'label': 'Gregorian Calendar', 'color': '#C0392B'},
    {'year': 2026, 'label': 'Present Day (Uttarayan in Moola/Dhanu)', 'color': '#27AE60'}
]

# Add a reference line for the Winter Solstice (Dec 21)
fig.add_hline(y=-10, line_width=1.5, line_dash="dash", line_color='#C0392B', 
              annotation_text="Winter Solstice (Dec 21)", annotation_position="bottom right")

for m in markers:
    fig.add_vline(x=m['year'], line_width=1.5, line_dash="dash", line_color=m['color'])
    y_val = df.loc[df['Year'] == m['year'], 'Relative_Day'].values[0] if m['year'] in df['Year'].values else 0
    fig.add_annotation(
        x=m['year'], 
        y=y_val, 
        text=m['label'], 
        showarrow=True, 
        arrowhead=2, 
        ax=50, ay=-40,
        bgcolor="rgba(255,255,255,0.8)"
    )

# 5. Visual Styling
fig.update_layout(
    title='<b>The Great Slide: Makar Sankranti Drift (1400 BCE - 2500 CE)</b>',
    xaxis_title='Historical Year',
    yaxis_title='Calendar Date',
    template='plotly_white',
    hovermode='x unified',
    xaxis=dict(
        rangeslider=dict(visible=True),
        type='linear'
    ),
    yaxis=dict(
        tickmode='array',
        tickvals=[-20, -10, 1, 14, 21],
        ticktext=['Dec 11', 'Dec 21', 'Jan 01', 'Jan 14', 'Jan 21'],
        autorange=True
    )
)

# 6. Save as Interactive HTML
interactive_file = 'index.html'
fig.write_html(interactive_file)

print(f"Interactive dashboard generated: {interactive_file}")
