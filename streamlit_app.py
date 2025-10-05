import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pilotage Portefeuille", layout="wide")
st.title("Pilotage live — Portefeuille résilient")

col1, col2, col3, col4 = st.columns(4)
vix = col1.number_input("VIX", value=18.0, step=0.1)
atr = col2.number_input("ATR S&P / prix (%)", value=1.3, step=0.1)
dd  = col3.number_input("Drawdown depuis pic (%)", value=-3.0, step=0.1)
mom = col4.toggle("Momentum actions (MA200) haussier", value=True)

data = [
    ["Equities — VWCE", "IE00BK5BQT80", 16.0, 16.0],
    ["Global Agg EUR-H — AGGH", "IE00BDBRDM35", 10.0, 10.0],
    ["UST 20y EUR-H", "IE00BD8PGZ49", 6.0, 6.0],
    ["ILB Global — IGIL", "IE00B3B8PX14", 20.0, 20.0],
    ["Gold ETC — SGLN", "IE00B4ND3602", 15.0, 15.0],
    ["Commodities — CMOD", "IE00BD6FTQ80", 12.0, 12.0],
    ["CTA — Man AHL", "LU0424370004", 11.0, 11.0],
    ["CTA — Winton", "IE00BG382R37", 8.0, 8.0],
    ["Cat Bonds — GAM Star", "IE00B6TLWG59", 2.0, 2.0],
]
df = pd.DataFrame(data, columns=["Ligne","ISIN","Cible_%","Actuel_%"])

st.subheader("Lignes & pondérations")
edit = st.data_editor(df, num_rows="dynamic", key="table")

st.subheader("Alertes")
alerts = []
tot = edit["Actuel_%"].sum()
if abs(tot-100) > 0.5: alerts.append(f"⚠️ Somme Actuel = {tot:.1f}% → rééquilibrer.")
if dd <= -8:          alerts.append("ℹ️ DD ≤ -8% : réinvestir ⅓ du cash (contrarien).")
if dd <= -12:         alerts.append("🛡️ DD ≤ -12% : réduire actions/commodities ; +ILB +CTA.")
if not mom:           alerts.append("📉 Momentum négatif : -4 à -6 pts actions ; +2 pts CTA ; +2 pts ILB.")
if vix>25 or atr>2.5: alerts.append("⏱️ Haute volatilité : passer en 1h/3j ; stops ATR plus serrés.")
for a in alerts: st.write("- ", a)
