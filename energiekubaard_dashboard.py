

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="EnergieKûbaard Accu Dashboard", layout="wide")


st.title("🔋 EnergieKûbaard - Terugverdientijd Thuisaccu")
st.markdown("Vergelijk scenario's met en zonder accu bij een dynamisch contract. Vul je gegevens in en zie direct het resultaat.")

# Inputkolommen
col1, col2 = st.columns(2)

with col1:
    jaarlijkse_pv_opbrengst = st.number_input("☀️ Jaarlijkse PV-opbrengst (kWh)", 0, 20000, 9000)
    jaarverbruik = st.number_input("⚡ Jaarverbruik (kWh)", 0, 20000, 9000)
    accu_grootte_kwh = st.number_input("🔋 Accugrootte (kWh)", 1, 100, 10)
    accu_rendement = st.slider("🔁 Accu-rendement (%)", 50, 100, 90)
    aanschafprijs_accu = st.number_input("💰 Aanschafprijs accu (€)", 100, 20000, 5000)

with col2:
    terugleververgoeding = st.number_input("📉 Terugleververgoeding (€/kWh)", 0.0, 1.0, 0.05)
    inkoopprijs_normaal = st.number_input("🛒 Inkoopprijs normaal tarief (€/kWh)", 0.0, 1.0, 0.35)
    goedkoop_dynamisch_tarief = st.number_input("📉 Goedkoop dynamisch tarief (€/kWh)", 0.0, 1.0, 0.08)
    zonnige_dagen = st.slider("☀️ Zonnige dagen per jaar (met overschot)", 100, 300, 250)
    winter_dagen_goedkoop = st.slider("❄️ Winterdagen voor goedkope inkoop", 0, 159, 105)

# Berekeningen
opslag_zonnig_kwh = zonnige_dagen * min(accu_grootte_kwh, jaarlijkse_pv_opbrengst / 365) * (accu_rendement / 100)
besparing_zonnig = opslag_zonnig_kwh * (inkoopprijs_normaal - terugleververgoeding)

opslag_winter_kwh = winter_dagen_goedkoop * accu_grootte_kwh * (accu_rendement / 100)
besparing_winter = opslag_winter_kwh * (inkoopprijs_normaal - goedkoop_dynamisch_tarief)

jaarlijkse_besparing = besparing_zonnig + besparing_winter
terugverdientijd = aanschafprijs_accu / jaarlijkse_besparing if jaarlijkse_besparing > 0 else float("inf")

# Resultaten
st.subheader("📊 Resultaten")
colr1, colr2 = st.columns(2)
colr1.metric("💶 Jaarlijkse besparing", f"€ {jaarlijkse_besparing:,.0f}")
colr2.metric("⏳ Terugverdientijd", f"{terugverdientijd:.1f} jaar")

# Dataframe voor grafieken
df = pd.DataFrame({
    "Categorie": ["Zomer (PV overschot)", "Winter (goedkoop laden)"],
    "Jaarlijkse kWh opslag": [opslag_zonnig_kwh, opslag_winter_kwh],
    "Besparing (€)": [besparing_zonnig, besparing_winter]
})

# Grafieken
st.subheader("📈 Grafieken")
colg1, colg2 = st.columns(2)

with colg1:
    fig1, ax1 = plt.subplots()
    ax1.bar(df["Categorie"], df["Jaarlijkse kWh opslag"], color="#FDB813")
    ax1.set_ylabel("kWh per jaar")
    ax1.set_title("Jaarlijkse Accu-opslag (kWh)")
    st.pyplot(fig1)

with colg2:
    fig2, ax2 = plt.subplots()
    ax2.bar(df["Categorie"], df["Besparing (€)"], color="#2CA02C")
    ax2.set_ylabel("€ per jaar")
    ax2.set_title("Besparing per categorie")
    st.pyplot(fig2)

st.caption("📌 Disclaimer: Werkelijke resultaten kunnen afwijken door weersomstandigheden, stroomprijzen en accuprestaties.")

