import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="3D Araba Motoru Simulasyonu", layout="wide")

# PREMIUM ARAYUZ - kenar 0 ama guzel detaylar
st.markdown("""
<style>
.block-container {padding-top: 0.5rem !important; padding-bottom: 0 !important; padding-left: 0 !important; padding-right: 0 !important; max-width: 100% !important;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stApp {background: radial-gradient(circle at 50% 30%, #1e293b 0%, #0f172a 40%, #020617 100%) !important;}
.title-box {
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 14px 20px;
  margin: 12px 16px;
  display:flex;
  justify-content: space-between;
  align-items:center;
}
.title-box h2 {margin:0 !important; color:#f1f5f9; font-size:22px; letter-spacing:0.5px}
.badge {background: linear-gradient(135deg, #38bdf8, #818cf8); color:white; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:600}
.info-bar {text-align:center; color:#94a3b8; font-size:13px; margin: 0 0 12px 0; letter-spacing:0.3px}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-box">
  <h2>🚗 İnteraktif 3D Motor Simülasyonu</h2>
  <div class="badge">GLB • Real-time • Trackpad destekli</div>
</div>
<p class="info-bar">🖱️ Sürükle = Döndür &nbsp;|&nbsp; 🔍 Tekerlek = Zoom &nbsp;|&nbsp; 👆 İki parmak = Kaydır</p>
""", unsafe_allow
