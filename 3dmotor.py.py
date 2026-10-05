import streamlit as st
import os

st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align:center'>🚗 İnteraktif 3D Araba Motoru</h2>", unsafe_allow_html=True)

# Dosya kontrol
paths = ["static/motor-v2.glb", "motor-v2.glb"]
found = None
for p in paths:
    if os.path.exists(p):
        found = p
        break

if not found:
    st.error(f"motor-v2.glb bulunamadi! Klasor: {os.listdir('.')} static: {os.listdir('static') if os.path.exists('static') else 'yok'}")
    st.stop()

size = os.path.getsize(found) / 1024 / 1024
st.sidebar.success(f"{found} - {size:.2f} MB")

# MODEL-VIEWER - EN GARANTILI, SIYAH EKRAN YOK
html = """
<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
<style>
model-viewer{
 width:100%;
 height:750px;
 background:#121212;
 border-radius:12px;
}
</style>
<model-viewer 
 src="/app/static/motor-v2.glb" 
 alt="Motor" 
 auto-rotate 
 camera-controls 
 shadow-intensity="1" 
 exposure="1.2"
 environment-image="neutral"
 style="background-color:#121212;"
>
</model-viewer>
<div style="text-align:center;color:#888;margin-top:8px">Fare ile döndür / tekerlek ile zoom</div>
<script>
// Fallback - eger static calismazsa root'tan dene
document.querySelector('model-viewer').addEventListener('error', (e)=>{
  console.log('static failed, trying root');
  e.target.src = 'motor-v2.glb';
});
</script>
"""

st.components.v1.html(html, height=800)
