import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="PhonePe Dashboard",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Brand palette (exact PhonePe colors from screenshot) ─────────────────────
PURPLE      = "#5f259f"
LIGHT_PUR   = "#8b5cf6"
LAVENDER    = "#ede9fe"
DARK_BG     = "#1e1b2e"
CARD_BG     = "#2d2748"
GREEN       = "#00c48c"
YELLOW      = "#f4c430"
WHITE       = "#ffffff"
TEXT_LIGHT  = "#e2d9f3"

st.markdown(f"""
<style>
  /* ── Page background ── */
  [data-testid="stAppViewContainer"],
  [data-testid="stMainBlockContainer"],
  section[data-testid="stMain"] > div {{
      background: {DARK_BG} !important;
  }}
  [data-testid="stSidebar"] {{ background: {DARK_BG}; }}

  /* ── Remove all streamlit default padding ── */
  .block-container {{ padding: 1rem 1.5rem !important; max-width: 100% !important; }}

  /* ── KPI cards ── */
  .kpi-card {{
      background: linear-gradient(135deg, {CARD_BG} 0%, #3d3060 100%);
      border-radius: 16px;
      padding: 1rem 1.2rem;
      border: 1px solid rgba(139,92,246,0.3);
      text-align: center;
  }}
  .kpi-icon {{ font-size: 1.5rem; margin-bottom: 4px; }}
  .kpi-value {{ font-size: 1.9rem; font-weight: 700; color: {WHITE}; margin: 0; line-height: 1.1; }}
  .kpi-label {{ font-size: 0.72rem; color: {TEXT_LIGHT}; font-weight: 500; text-transform: uppercase;
                letter-spacing: 0.05em; margin: 0 0 4px 0; }}
  .kpi-growth {{ font-size: 0.78rem; color: {GREEN}; font-weight: 600; margin-top: 4px; }}

  /* ── Section cards ── */
  .chart-card {{
      background: {CARD_BG};
      border-radius: 16px;
      padding: 1rem 1.2rem;
      border: 1px solid rgba(139,92,246,0.2);
      margin-bottom: 0.8rem;
  }}
  .chart-title {{
      color: {WHITE};
      font-size: 0.88rem;
      font-weight: 600;
      margin-bottom: 0.6rem;
      letter-spacing: 0.02em;
  }}

  /* ── Header ── */
  .pp-header {{
      background: linear-gradient(135deg, {CARD_BG} 0%, #3d3060 100%);
      border-radius: 16px;
      padding: 1rem 1.5rem;
      border: 1px solid rgba(139,92,246,0.3);
      margin-bottom: 0.8rem;
  }}
  .pp-tagline {{ color: {TEXT_LIGHT}; font-size: 0.78rem; margin: 0; }}

  /* ── Filter buttons ── */
  div[data-testid="stHorizontalBlock"] .stButton button {{
      border-radius: 20px !important;
      font-size: 0.78rem !important;
      padding: 4px 16px !important;
      font-weight: 600 !important;
  }}

  /* ── Insights card ── */
  .insight-card {{
      background: linear-gradient(135deg, #4a1f8a 0%, {PURPLE} 100%);
      border-radius: 16px;
      padding: 1rem 1.2rem;
      border: 1px solid rgba(255,255,255,0.15);
  }}
  .insight-title {{ color: {WHITE}; font-size: 0.9rem; font-weight: 700; margin-bottom: 8px; }}
  .insight-item {{ color: {TEXT_LIGHT}; font-size: 0.78rem; margin-bottom: 5px; padding-left: 12px;
                   border-left: 3px solid {YELLOW}; }}

  /* ── Metric table ── */
  .svc-row {{ display: flex; justify-content: space-between; align-items: center;
              padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.07); }}
  .svc-name {{ color: {TEXT_LIGHT}; font-size: 0.78rem; }}
  .svc-bar-wrap {{ flex: 1; margin: 0 10px; background: rgba(255,255,255,0.08);
                   border-radius: 4px; height: 6px; overflow: hidden; }}
  .svc-bar {{ height: 100%; background: {LIGHT_PUR}; border-radius: 4px; }}
  .svc-val {{ color: {WHITE}; font-size: 0.78rem; font-weight: 600; min-width: 40px; text-align: right; }}

  /* hide streamlit branding */
  #MainMenu, footer, header {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# ── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    xl    = pd.ExcelFile("Phonepe-Final-Dataset.xlsx")
    users = pd.read_excel(xl, "All_Users",        parse_dates=["Join_Date"])
    txn   = pd.read_excel(xl, "All_Transactions", parse_dates=["Date"])
    txn["Month"]     = txn["Date"].dt.to_period("M").dt.to_timestamp()
    txn["MonthName"] = txn["Date"].dt.strftime("%b")
    txn["DayOfWeek"] = txn["Date"].dt.dayofweek
    txn["IsWeekend"] = txn["DayOfWeek"].isin([5, 6])
    users["Age_Group"] = pd.cut(
        users["Age"], bins=[0, 24, 39, 55, 100],
        labels=["Gen Z", "Millennials", "Gen X", "Boomers"]
    )
    return users, txn

users, txn = load()


# ── FILTERS ───────────────────────────────────────────────────────────────────
import base64 as _b64, pathlib as _pl

# Find logo file flexibly — matches any png with "phone" in name, or falls back
_logo = ""
for _p in _pl.Path(__file__).parent.glob("*.png"):
    if "phone" in _p.name.lower() or "logo" in _p.name.lower() or "pngwing" in _p.name.lower():
        with open(_p, "rb") as _lf:
            _logo = _b64.b64encode(_lf.read()).decode()
        break

_logo_html = f'<img src="data:image/png;base64,{_logo}" style="height:52px; width:auto;" alt="PhonePe"/>' if _logo else '<span style="font-size:1.6rem; font-weight:800; color:#ffffff;">💜 PhonePe</span>'

st.markdown(f"""
<div class="pp-header">
  <div style="display:flex; align-items:center; gap:12px; margin-bottom:6px;">
    {_logo_html}
  </div>
  <div style="font-size:1.15rem; font-weight:700; color:#e2d9f3;">Payment insights, powering <span style="color:#f4c430;">Bharat</span></div>
  <div class="pp-tagline">Secure. Simple. Seamless.</div>
</div>
""", unsafe_allow_html=True)

# Filter row
fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns([2, 1, 1, 1, 1])
with fcol1:
    month_opts = ["All"] + [d.strftime("%b %Y") for d in sorted(txn["Month"].unique())]
    sel_month  = st.selectbox("Month", month_opts, label_visibility="collapsed")
with fcol2:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    show_failed  = st.button("❌ Failed",     use_container_width=True)
with fcol3:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    show_pending = st.button("⏳ Pending",    use_container_width=True)
with fcol4:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    show_success = st.button("✅ Successful", use_container_width=True)
with fcol5:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    show_all     = st.button("🔄 All",        use_container_width=True)

# Apply month filter
df = txn.copy()
if sel_month != "All":
    df = df[df["Date"].dt.strftime("%b %Y") == sel_month]

# Apply status filter
if show_failed:
    df = df[df["Payment_Status"] == "Failed"]
elif show_success:
    df = df[df["Payment_Status"] == "Successful"]
elif show_pending:
    df = df[df["Payment_Status"].isin(["Wrong PIN", "Server error", "Insufficient amount"])]

df_ok = df[df["Payment_Status"] == "Successful"]

if len(df) == 0:
    st.warning("No data for selected filters.")
    st.stop()


# ── HELPERS ───────────────────────────────────────────────────────────────────
def fmt(v):
    if v >= 1e9:  return f"{v/1e9:.2f}bn"
    if v >= 1e6:  return f"{v/1e6:.1f}M"
    if v >= 1e3:  return f"{v/1e3:.0f}K"
    return f"{v:.0f}"

# Chart base — dark theme, fully explicit so theme=None works perfectly
BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color=WHITE, size=11),
    margin=dict(l=10, r=10, t=15, b=10),
)

def show(fig, h=220):
    fig.update_layout(height=h)
    st.plotly_chart(fig, use_container_width=True, theme=None)


# ── KPIs ──────────────────────────────────────────────────────────────────────
total_txn   = len(df)
total_val   = df["Amount"].sum()
uniq_users  = df["User_ID"].nunique()
succ_rate   = len(df_ok) / len(df) * 100 if len(df) > 0 else 0

# MOM growth
monthly_all = txn.groupby("Month").agg(Count=("Amount","count"), Val=("Amount","sum")).reset_index().sort_values("Month")
if len(monthly_all) >= 2:
    txn_growth = (monthly_all.iloc[-1]["Count"] - monthly_all.iloc[-2]["Count"]) / monthly_all.iloc[-2]["Count"] * 100
    val_growth = (monthly_all.iloc[-1]["Val"]   - monthly_all.iloc[-2]["Val"])   / monthly_all.iloc[-2]["Val"]   * 100
else:
    txn_growth = val_growth = 0

k1, k2, k3, k4 = st.columns(4)
for col, icon, label, value, growth, show_growth in [
    (k1, "🔄", "Total Transactions", fmt(total_txn),       txn_growth, True),
    (k2, "₹",  "Total Value",        f"₹{fmt(total_val)}", val_growth, True),
    (k3, "👥", "Unique Users",       fmt(uniq_users),      None,       False),
    (k4, "✅", "Successful Rate",    f"{succ_rate:.2f}%",  None,       False),
]:
    growth_html = f'<div class="kpi-growth">{"▲" if growth>=0 else "▼"} {abs(growth):.2f}% MOM growth</div>' if show_growth else ""
    col.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      {growth_html}
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


# ── ROW 2: Transactions Over Time  |  Age Segment ────────────────────────────
left, right = st.columns([3, 2])

with left:
    st.markdown('<div class="chart-card"><div class="chart-title">Transactions Over Time</div>', unsafe_allow_html=True)
    monthly = df.groupby("Month").agg(Count=("Amount","count"), Value=("Amount","sum")).reset_index()
    f1 = make_subplots(specs=[[{"secondary_y": True}]])
    f1.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Count"],
        name="Total Transaction", mode="lines+markers",
        line=dict(color=PURPLE, width=2.5), marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(95,37,159,0.15)"
    ), secondary_y=False)
    f1.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Value"],
        name="Total Transaction Value", mode="lines+markers",
        line=dict(color=LIGHT_PUR, width=2, dash="dot"), marker=dict(size=5),
    ), secondary_y=True)
    f1.update_layout(
        **BASE, height=220,
        legend=dict(orientation="h", x=0, y=1.12, font=dict(color=WHITE, size=10),
                    bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(tickformat="%b", tickfont=dict(color=TEXT_LIGHT, size=10),
                   showgrid=False, zeroline=False),
        yaxis=dict( tickfont=dict(color=TEXT_LIGHT, size=10), showgrid=True,
                    gridcolor="rgba(255,255,255,0.07)", zeroline=False),
        yaxis2=dict(tickfont=dict(color=TEXT_LIGHT, size=10), showgrid=False, zeroline=False,
                    tickprefix="₹", tickformat=".2s"),
    )
    show(f1, 220)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="chart-card"><div class="chart-title">Age Segment Contribution</div>', unsafe_allow_html=True)
    merged_age = df.merge(users[["User_ID","Age_Group"]], on="User_ID", how="left")
    merged_age["Age_Group"] = merged_age["Age_Group"].astype(str).replace("nan","Unknown")
    age_seg = merged_age[merged_age["Age_Group"]!="Unknown"].groupby("Age_Group")["Amount"].sum().reset_index()
    DONUT_COLORS = [PURPLE, LIGHT_PUR, "#c4b5fd", YELLOW]
    f2 = px.pie(age_seg, names="Age_Group", values="Amount",
                color_discrete_sequence=DONUT_COLORS, hole=0.62)
    f2.update_traces(
        textposition="outside",
        textinfo="label+value",
        texttemplate="%{label}<br>%{value:.2s}",
        textfont=dict(color=WHITE, size=10),
        pull=[0.04, 0, 0, 0],
    )
    f2.update_layout(
        **BASE, height=220,
        showlegend=False,
        annotations=[dict(text="💜", x=0.5, y=0.5, font_size=28,
                          showarrow=False, font_color=WHITE)]
    )
    f2.update_layout(margin=dict(l=30, r=30, t=20, b=20))
    show(f2, 220)
    st.markdown('</div>', unsafe_allow_html=True)


# ── ROW 3: Service Value  |  Top 5 Users  |  Weekday/Weekend  |  Insights ──
c1, c2, c3, c4 = st.columns([2, 2, 2, 2.5])

# Service Transaction Value
with c1:
    st.markdown('<div class="chart-card"><div class="chart-title">Service Transaction Value Analysis</div>', unsafe_allow_html=True)
    svc = df_ok.groupby("Service")["Amount"].sum().sort_values(ascending=False).reset_index()
    svc["Label"] = svc["Service"].str.replace("_", " ")
    svc["Short"] = svc["Amount"].map(lambda v: f"{v/1e6:.1f}M")
    max_val = svc["Amount"].max()
    svc["Pct"] = (svc["Amount"] / max_val * 100).round(1)

    rows_html = ""
    for _, row in svc.iterrows():
        rows_html += f"""
        <div class="svc-row">
          <span class="svc-name">{row['Label']}</span>
          <div class="svc-bar-wrap"><div class="svc-bar" style="width:{row['Pct']}%"></div></div>
          <span class="svc-val">{row['Short']}</span>
        </div>"""
    st.markdown(rows_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Top 5 Users
with c2:
    st.markdown('<div class="chart-card"><div class="chart-title">Top 5 Users (By Transaction Value)</div>', unsafe_allow_html=True)
    top_u = df_ok.merge(users[["User_ID","Name"]], on="User_ID", how="left")
    top5  = top_u.groupby("Name")["Amount"].sum().nlargest(5).reset_index()
    top5["Short"] = top5["Amount"].map(lambda v: f"{v/1e6:.1f}M")
    f3 = go.Figure(go.Bar(
        x=top5["Name"], y=top5["Amount"],
        marker=dict(
            color=[PURPLE, LIGHT_PUR, "#9d7fe8", "#b49de0", "#c4b5fd"],
            line=dict(width=0)
        ),
        text=top5["Short"], textposition="outside",
        textfont=dict(color=WHITE, size=10),
    ))
    f3.update_layout(
        **BASE, height=220,
        xaxis=dict(tickfont=dict(color=TEXT_LIGHT, size=9), showgrid=False,
                   zeroline=False,
                   ticktext=[n[:7]+"…" if len(n)>8 else n for n in top5["Name"]],
                   tickvals=top5["Name"]),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        bargap=0.3,
    )
    show(f3, 220)
    st.markdown('</div>', unsafe_allow_html=True)

# Weekday vs Weekend
with c3:
    st.markdown('<div class="chart-card"><div class="chart-title">Weekday v/s Weekend Usage</div>', unsafe_allow_html=True)
    ww = df.groupby("IsWeekend").size().reset_index(name="Count")
    ww["Label"]  = ww["IsWeekend"].map({False: "Weekday", True: "Weekend"})
    ww["Pct"]    = (ww["Count"] / ww["Count"].sum() * 100).round(1)
    ww["PctStr"] = ww["Pct"].map(lambda v: f"{v}%")

    f4 = go.Figure(go.Pie(
        labels=ww["Label"], values=ww["Count"],
        hole=0.62,
        marker=dict(colors=[PURPLE, "#c4b5fd"],
                    line=dict(color=DARK_BG, width=2)),
        textinfo="none",
        hovertemplate="%{label}: %{percent}<extra></extra>",
    ))
    f4.update_layout(
        **BASE, height=220,
        showlegend=False,
        annotations=[dict(text="📅", x=0.5, y=0.5, font_size=26,
                          showarrow=False)]
    )
    f4.update_layout(margin=dict(l=10, r=10, t=20, b=10))
    # Weekday % label below
    wd_pct = ww[ww["Label"]=="Weekday"]["Pct"].values[0]
    we_pct = ww[ww["Label"]=="Weekend"]["Pct"].values[0]
    show(f4, 185)
    st.markdown(
        f'<div style="text-align:center; margin-top:-10px;">'
        f'<span style="color:{WHITE}; font-size:1rem; font-weight:700;">Weekday {wd_pct}%</span>'
        f'<span style="color:{TEXT_LIGHT}; font-size:0.78rem; margin-left:10px;">Weekend {we_pct}%</span>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Insights
with c4:
    # Top user name for insight
    top_name = top5.iloc[0]["Name"] if len(top5) > 0 else "N/A"
    # Top service
    top_svc  = svc.iloc[0]["Label"] if len(svc) > 0 else "N/A"
    wd_label = "Weekdays" if wd_pct > 50 else "Weekends"
    # top age group by count
    age_cnt  = merged_age[merged_age["Age_Group"]!="Unknown"].groupby("Age_Group").size().idxmax() if len(merged_age)>0 else "Gen X"

    st.markdown(f"""
    <div class="insight-card" style="height:100%; min-height:220px; display:flex; flex-direction:column; justify-content:center;">
      <div class="insight-title">💡 Insights</div>
      <div class="insight-item"><b>{age_cnt}</b> Users Are Most Active Than Other Users</div>
      <div class="insight-item" style="margin-top:6px;"><b>{top_svc}</b> Give Highest Transaction Value</div>
      <div class="insight-item" style="margin-top:6px;">The Highest Number Of Transactions Take Place On <b>{wd_label}</b></div>
      <div style="margin-top:12px; font-size:1.8rem; text-align:center;">📈</div>
    </div>
    """, unsafe_allow_html=True)