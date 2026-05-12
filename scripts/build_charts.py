import xlsxwriter
import pandas as pd
import numpy as np

INPUT  = '/sessions/vibrant-intelligent-babbage/mnt/my-website/session-4-data/college-analysis.xlsx'
OUTPUT = INPUT

# ── Read source data ──────────────────────────────────────────────────────────
df1 = pd.read_excel(INPUT, sheet_name='Chart Data 1', header=0)
df2 = pd.read_excel(INPUT, sheet_name='Chart Data 2', header=0)
df3 = pd.read_excel(INPUT, sheet_name='Chart Data 3', header=0)
df4 = pd.read_excel(INPUT, sheet_name='Chart Data 4', header=0)
df5 = pd.read_excel(INPUT, sheet_name='Chart Data 5', header=0)

other_roi    = df2.iloc[:, 1].dropna().values
median_roi   = float(np.median(other_roi))

# My-Schools ROI rows (Duke row 34, UT Austin row 154, UNC row 174 – sorted nicely)
roi_comp = [
    ('Duke',            1.422380, median_roi),
    ('UNC Chapel Hill', 8.027574, median_roi),
    ('UT Austin',       6.427190, median_roi),
]

# ── Palette ───────────────────────────────────────────────────────────────────
GOLD      = '#E8983F'
DARK_GOLD = '#C0703F'
BLUE      = '#4472C4'
TEAL      = '#2E75B6'
GRAY      = '#8496B0'
LIGHT_GRAY= '#CBD5E0'
NAVY      = '#1F3864'
BG_ACCENT = '#FFF3E0'

# ── Workbook ──────────────────────────────────────────────────────────────────
wb = xlsxwriter.Workbook(OUTPUT)

# Formats
def hdr(wb):
    return wb.add_format({'bold': True, 'bg_color': NAVY, 'font_color': 'white',
                          'font_name': 'Arial', 'font_size': 10, 'border': 1, 'align': 'center'})
def cell(wb):
    return wb.add_format({'font_name': 'Arial', 'font_size': 10, 'border': 1})
def curr(wb):
    return wb.add_format({'font_name': 'Arial', 'font_size': 10, 'num_format': '$#,##0', 'border': 1})
def pct(wb):
    return wb.add_format({'font_name': 'Arial', 'font_size': 10, 'num_format': '0.0%', 'border': 1})
def num2(wb):
    return wb.add_format({'font_name': 'Arial', 'font_size': 10, 'num_format': '0.00', 'border': 1})
def my_cell(wb):
    return wb.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 10,
                          'border': 1, 'bg_color': BG_ACCENT})
def my_curr(wb):
    return wb.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 10,
                          'num_format': '$#,##0', 'border': 1, 'bg_color': BG_ACCENT})
def my_pct(wb):
    return wb.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 10,
                          'num_format': '0.0%', 'border': 1, 'bg_color': BG_ACCENT})
def my_num2(wb):
    return wb.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 10,
                          'num_format': '0.00', 'border': 1, 'bg_color': BG_ACCENT})

H = hdr(wb); C = cell(wb); CU = curr(wb); PC = pct(wb); N2 = num2(wb)
MH = my_cell(wb); MC = my_curr(wb); MP = my_pct(wb); MN = my_num2(wb)

# ── Sheet 1: Chart Data 1 ─────────────────────────────────────────────────────
ws1 = wb.add_worksheet('Chart Data 1')
ws1.write_row(0, 0, list(df1.columns), H)
for i, row in df1.iterrows():
    ws1.write(i+1, 0, row.iloc[0], MH)
    ws1.write(i+1, 1, row.iloc[1], MC)
    ws1.write(i+1, 2, row.iloc[2], MC)
    ws1.write(i+1, 3, row.iloc[3], MC)
ws1.set_column('A:A', 18); ws1.set_column('B:D', 24)

# ── Sheet 2: Chart Data 2 (hidden) ───────────────────────────────────────────
ws2 = wb.add_worksheet('Chart Data 2')
ws2.hide()
ws2.write_row(0, 0, list(df2.columns), H)
for i, row in df2.iterrows():
    is_my = not pd.isna(row.iloc[2])
    f = MH if is_my else C; fn = MN if is_my else N2
    ws2.write(i+1, 0, str(row.iloc[0]) if not pd.isna(row.iloc[0]) else '', f)
    ws2.write(i+1, 1, row.iloc[1] if not pd.isna(row.iloc[1]) else None, fn)
    ws2.write(i+1, 2, row.iloc[2] if not pd.isna(row.iloc[2]) else None, fn)
    ws2.write(i+1, 3, str(row.iloc[3]) if not pd.isna(row.iloc[3]) else '', f)
ws2.set_column('A:A', 50); ws2.set_column('B:D', 18)

# ── Sheet 3: Chart Data 3 (hidden) ───────────────────────────────────────────
ws3 = wb.add_worksheet('Chart Data 3')
ws3.hide()
ws3.write_row(0, 0, list(df3.columns), H)
for i, row in df3.iterrows():
    ws3.write(i+1, 0, row.iloc[0] if not pd.isna(row.iloc[0]) else None, C)
    ws3.write(i+1, 1, row.iloc[1] if not pd.isna(row.iloc[1]) else None, CU)
    ws3.write(i+1, 2, row.iloc[2] if not pd.isna(row.iloc[2]) else None, MH)
    ws3.write(i+1, 3, row.iloc[3] if not pd.isna(row.iloc[3]) else None, MC)
ws3.set_column('A:D', 20)

# ── Sheet 4: Chart Data 4 (hidden) ───────────────────────────────────────────
ws4 = wb.add_worksheet('Chart Data 4')
ws4.hide()
ws4.write_row(0, 0, list(df4.columns), H)
for i, row in df4.iterrows():
    ws4.write(i+1, 0, row.iloc[0], MH)
    ws4.write(i+1, 1, row.iloc[1] / 100, MP)   # completion rate → decimal
    ws4.write(i+1, 2, row.iloc[2], MC)           # median debt
    ws4.write(i+1, 3, row.iloc[3], MP)           # debt-to-earnings (already decimal)
ws4.set_column('A:A', 18); ws4.set_column('B:D', 20)

# ── Sheet 5: Chart Data 5 (hidden) ───────────────────────────────────────────
ws5 = wb.add_worksheet('Chart Data 5')
ws5.hide()
ws5.write_row(0, 0, list(df5.columns), H)
for i, row in df5.iterrows():
    ws5.write(i+1, 0, row.iloc[0], MH)
    ws5.write(i+1, 1, row.iloc[1], MC)
    ws5.write(i+1, 2, row.iloc[2], MC)
    ws5.write(i+1, 3, row.iloc[3], MC)
    ws5.write(i+1, 4, row.iloc[4], MC)
ws5.set_column('A:A', 18); ws5.set_column('B:F', 22)

# ── Sheet 6: ROI Summary (hidden, feeds Chart 2) ─────────────────────────────
ws_roi = wb.add_worksheet('ROI Summary')
ws_roi.hide()
ws_roi.write_row(0, 0, ['School', 'My School ROI', f'Median ROI ({len(other_roi)} Other Schools)'], H)
for i, (school, my_r, med) in enumerate(roi_comp):
    ws_roi.write(i+1, 0, school, MH)
    ws_roi.write(i+1, 1, my_r,  MN)
    ws_roi.write(i+1, 2, med,   N2)
ws_roi.set_column('A:C', 28)

# ── Helper: chart style ───────────────────────────────────────────────────────
def style_chart(ch):
    ch.set_chartarea({'border': {'none': True}, 'fill': {'color': 'white'}})
    ch.set_plotarea({'border': {'color': '#E0E0E0'}})

GRIDLINE = {'visible': True, 'line': {'color': '#EBEBEB', 'dash_type': 'solid'}}
TITLE_FONT = {'size': 13, 'bold': True, 'color': NAVY}
AXIS_FONT  = {'name': 'Arial', 'size': 10, 'color': '#444444'}

# ── Dashboard Sheet ───────────────────────────────────────────────────────────
dash = wb.add_worksheet('📊 My Schools Charts')
dash.hide_gridlines(2)
dash.set_zoom(85)

title_fmt = wb.add_format({
    'bold': True, 'font_size': 15, 'font_name': 'Arial',
    'align': 'center', 'valign': 'vcenter',
    'font_color': 'white', 'bg_color': NAVY
})
dash.merge_range('A1:X1',
    '📊  College Analysis  —  My Schools Dashboard  |  Duke  •  UNC Chapel Hill  •  UT Austin',
    title_fmt)
dash.set_row(0, 38)

# ════════════════════════════════════════════════════════════════════
# CHART 1 — What You Pay vs. What You Earn (cost vs earnings bar)
# ════════════════════════════════════════════════════════════════════
c1 = wb.add_chart({'type': 'column'})

c1.add_series({
    'name': 'In-State Tuition',
    'categories': ['Chart Data 1', 1, 0, 3, 0],
    'values':     ['Chart Data 1', 1, 1, 3, 1],
    'fill': {'color': BLUE}, 'border': {'color': NAVY},
})
c1.add_series({
    'name': 'Out-of-State Tuition',
    'categories': ['Chart Data 1', 1, 0, 3, 0],
    'values':     ['Chart Data 1', 1, 2, 3, 2],
    'fill': {'color': GRAY}, 'border': {'color': '#5A6A7A'},
})
c1.add_series({
    'name': '10-Year Median Earnings',
    'categories': ['Chart Data 1', 1, 0, 3, 0],
    'values':     ['Chart Data 1', 1, 3, 3, 3],
    'fill': {'color': GOLD}, 'border': {'color': DARK_GOLD},
})
c1.set_title({'name': 'Chart 1: What You Pay vs. What You Earn', 'name_font': TITLE_FONT})
c1.set_x_axis({'name': '', 'name_font': AXIS_FONT, 'num_font': AXIS_FONT})
c1.set_y_axis({'name': 'Amount ($)', 'name_font': AXIS_FONT, 'num_font': AXIS_FONT,
               'num_format': '$#,##0', 'major_gridlines': GRIDLINE})
c1.set_legend({'position': 'bottom', 'font': {'name': 'Arial', 'size': 9}})
c1.set_size({'width': 490, 'height': 330})
style_chart(c1)
dash.insert_chart('A3', c1)

# ════════════════════════════════════════════════════════════════════
# CHART 2 — ROI: My Schools vs. Median of All Others
# ════════════════════════════════════════════════════════════════════
c2 = wb.add_chart({'type': 'column'})

c2.add_series({
    'name': 'My School ROI',
    'categories': ['ROI Summary', 1, 0, 3, 0],
    'values':     ['ROI Summary', 1, 1, 3, 1],
    'fill': {'color': GOLD}, 'border': {'color': DARK_GOLD},
    'data_labels': {'value': True, 'num_format': '0.0"x"',
                    'font': {'bold': True, 'name': 'Arial', 'size': 9, 'color': NAVY}},
})
c2.add_series({
    'name': f'Median ROI – {len(other_roi)} Other Schools ({median_roi:.1f}x)',
    'categories': ['ROI Summary', 1, 0, 3, 0],
    'values':     ['ROI Summary', 1, 2, 3, 2],
    'fill': {'color': LIGHT_GRAY}, 'border': {'color': '#9AAABB'},
})
c2.set_title({'name': 'Chart 2: Value for Money — ROI vs. All Schools Median', 'name_font': TITLE_FONT})
c2.set_x_axis({'name': '', 'name_font': AXIS_FONT, 'num_font': AXIS_FONT})
c2.set_y_axis({'name': 'ROI (10-yr Earnings ÷ In-State Tuition)',
               'name_font': AXIS_FONT, 'num_font': AXIS_FONT,
               'num_format': '0.0"x"', 'major_gridlines': GRIDLINE})
c2.set_legend({'position': 'bottom', 'font': {'name': 'Arial', 'size': 9}})
c2.set_size({'width': 490, 'height': 330})
style_chart(c2)
dash.insert_chart('L3', c2)

# ════════════════════════════════════════════════════════════════════
# CHART 3 — Selectivity vs. Earnings Scatter (197 schools + My Schools)
# ════════════════════════════════════════════════════════════════════
c3 = wb.add_chart({'type': 'scatter'})
n3 = len(df3)  # 197

c3.add_series({
    'name': 'Other Universities',
    'categories': ['Chart Data 3', 1, 0, n3, 0],
    'values':     ['Chart Data 3', 1, 1, n3, 1],
    'marker': {'type': 'circle', 'size': 4,
               'fill': {'color': LIGHT_GRAY},
               'border': {'color': '#A0AEC0'}},
    'line': {'none': True},
})
c3.add_series({
    'name': 'My Schools ★',
    'categories': ['Chart Data 3', 1, 2, 3, 2],
    'values':     ['Chart Data 3', 1, 3, 3, 3],
    'marker': {'type': 'diamond', 'size': 12,
               'fill': {'color': GOLD},
               'border': {'color': DARK_GOLD}},
    'line': {'none': True},
    'data_labels': {
        'custom': [
            {'value': 'Duke (5.7%)'},
            {'value': 'UNC (15.3%)'},
            {'value': 'UT Austin (26.6%)'},
        ],
        'position': 'above',
        'font': {'bold': True, 'name': 'Arial', 'size': 8, 'color': NAVY},
    },
})
c3.set_title({'name': 'Chart 3: Selectivity vs. 10-Year Earnings', 'name_font': TITLE_FONT})
c3.set_x_axis({'name': 'Admission Rate (%) — lower = more selective',
               'name_font': AXIS_FONT, 'num_font': AXIS_FONT,
               'num_format': '0"%"', 'major_gridlines': GRIDLINE})
c3.set_y_axis({'name': '10-Year Median Earnings ($)',
               'name_font': AXIS_FONT, 'num_font': AXIS_FONT,
               'num_format': '$#,##0', 'major_gridlines': GRIDLINE})
c3.set_legend({'position': 'bottom', 'font': {'name': 'Arial', 'size': 9}})
c3.set_size({'width': 490, 'height': 330})
style_chart(c3)
dash.insert_chart('A21', c3)

# ════════════════════════════════════════════════════════════════════
# CHART 4 — Graduation Rate vs. Debt Burden
# ════════════════════════════════════════════════════════════════════
c4 = wb.add_chart({'type': 'column'})

c4.add_series({
    'name': 'Graduation Rate',
    'categories': ['Chart Data 4', 1, 0, 3, 0],
    'values':     ['Chart Data 4', 1, 1, 3, 1],
    'fill': {'color': TEAL}, 'border': {'color': NAVY},
    'data_labels': {'value': True, 'num_format': '0.0%',
                    'font': {'bold': True, 'name': 'Arial', 'size': 9, 'color': 'white'},
                    'position': 'inside_end'},
})
c4.add_series({
    'name': 'Debt-to-Earnings Ratio',
    'categories': ['Chart Data 4', 1, 0, 3, 0],
    'values':     ['Chart Data 4', 1, 3, 3, 3],
    'fill': {'color': GOLD}, 'border': {'color': DARK_GOLD},
    'data_labels': {'value': True, 'num_format': '0.0%',
                    'font': {'bold': True, 'name': 'Arial', 'size': 9, 'color': NAVY}},
})
c4.set_title({'name': 'Chart 4: Graduation Rate vs. Debt-to-Earnings Burden',
              'name_font': TITLE_FONT})
c4.set_x_axis({'name': '', 'name_font': AXIS_FONT, 'num_font': AXIS_FONT})
c4.set_y_axis({'name': 'Rate (%)', 'name_font': AXIS_FONT, 'num_font': AXIS_FONT,
               'num_format': '0%', 'min': 0, 'max': 1.05,
               'major_gridlines': GRIDLINE})
c4.set_legend({'position': 'bottom', 'font': {'name': 'Arial', 'size': 9}})
c4.set_size({'width': 490, 'height': 330})
style_chart(c4)
dash.insert_chart('L21', c4)

# ════════════════════════════════════════════════════════════════════
# CHART 5 — Earnings vs. State Benchmarks
# ════════════════════════════════════════════════════════════════════
c5 = wb.add_chart({'type': 'column'})

c5.add_series({
    'name': 'State HS Earnings',
    'categories': ['Chart Data 5', 1, 0, 3, 0],
    'values':     ['Chart Data 5', 1, 1, 3, 1],
    'fill': {'color': LIGHT_GRAY}, 'border': {'color': '#9AAABB'},
})
c5.add_series({
    'name': "State Bachelor's Earnings",
    'categories': ['Chart Data 5', 1, 0, 3, 0],
    'values':     ['Chart Data 5', 1, 2, 3, 2],
    'fill': {'color': GRAY}, 'border': {'color': '#5A6A7A'},
})
c5.add_series({
    'name': 'School 10-Year Earnings',
    'categories': ['Chart Data 5', 1, 0, 3, 0],
    'values':     ['Chart Data 5', 1, 3, 3, 3],
    'fill': {'color': GOLD}, 'border': {'color': DARK_GOLD},
})
c5.add_series({
    'name': 'COL-Adjusted Earnings',
    'categories': ['Chart Data 5', 1, 0, 3, 0],
    'values':     ['Chart Data 5', 1, 4, 3, 4],
    'fill': {'color': '#8B4513'}, 'border': {'color': '#5D2E0C'},
})
c5.set_title({'name': 'Chart 5: Earnings Uplift vs. State Benchmarks',
              'name_font': TITLE_FONT})
c5.set_x_axis({'name': '', 'name_font': AXIS_FONT, 'num_font': AXIS_FONT})
c5.set_y_axis({'name': '10-Year Median Earnings ($)',
               'name_font': AXIS_FONT, 'num_font': AXIS_FONT,
               'num_format': '$#,##0', 'major_gridlines': GRIDLINE})
c5.set_legend({'position': 'bottom', 'font': {'name': 'Arial', 'size': 9}})
c5.set_size({'width': 700, 'height': 330})
style_chart(c5)
dash.insert_chart('A39', c5)

# ── Finalize ──────────────────────────────────────────────────────────────────
wb.close()
print("Done — college-analysis.xlsx written successfully.")
