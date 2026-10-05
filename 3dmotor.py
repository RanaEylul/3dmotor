import streamlit as st
import os, base64

st.set_page_config(layout="wide", page_title="Oyak Horse")
st.markdown("<h2 style='text-align:center;'>Oyak Horse Görme Testi Uygulaması</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Üstteki 4 vidadan 2'si eksik versiyonu test için</p>", unsafe_allow_html=True)

# dosyalar
files = os.listdir(".")
if "motor-v2.glb" not in files:
    st.error(f"motor-v2.glb yok! Var olanlar: {files}")
    st.stop()

# GLB'yi static olarak kopyala - Streamlit bu klasörü sunar
os.makedirs("static", exist_ok=True)
with open("motor-v2.glb","rb") as src, open("static/motor-v2.glb","wb") as dst:
    dst.write(src.read())

st.markdown("""
<script type="module" src="https://unpkg.com/@google/model-viewer@3.4.0/dist/model-viewer.min.js"></script>
<style>
model-viewer{width:100%; height:700px; background:#1e293b; border-radius:12px;}
</style>
<model-viewer 
  src="app/static/motor-v2.glb" 
  camera-controls 
  auto-rotate 
  shadow-intensity="1" 
  exposure="1.2"
  ar-status="not-presenting">
</model-viewer>
<p style='text-align:center; color:#64748b; font-size:12px;'>Sürükle = Döndür | Scroll = Zoom</p>
""", unsafe_allow_html=True)

st.warning("Not: Vida eksik versiyonu için Blender'da 2 vidayı silip motor-eksik.glb olarak kaydetmen gerek. Kodla gizleme bu model-viewer'da stabil değil. İstersen ben sana Blender adımlarını yazayım.")
