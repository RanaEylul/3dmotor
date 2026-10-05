import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="3D Araba Motoru Simülasyonu", layout="wide")

st.markdown("""
<h2 style='text-align:center'>🚗 İnteraktif 3D Araba Motoru Simülasyonu</h2>
<p style='text-align:center;opacity:.6'>Laptop trackpad (iki parmak) ve fare tekerleği desteği aktifleştirildi.</p>
""", unsafe_allow_html=True)

# --- SIDEBAR: RENKLENDİRME ---
st.sidebar.header("🎨 Renklendirme")
engine_color = st.sidebar.color_picker("Motor Gövde Rengi", "#8a8d91")
cover_color = st.sidebar.color_picker("Kapak Rengi", "#6b7280")
metal_color = st.sidebar.color_picker("Metal / Kayış", "#1f2937")

st.sidebar.divider()
st.sidebar.header("🎯 Hata Bulma Modu")
fault_mode = st.sidebar.toggle("Hata Bulma Modunu Aç", value=False)

FAULTS = {
    "Ön kayış gevşekliği": "Ön tarafta, büyük kasnakların üstünde",
    "Üst kapakta eksik vida": "Sağ üst kapak üzerinde",
    "Altta yağ sızıntısı": "Motorun alt kısmı",
    "Emme manifoldunda çatlak": "Ortadaki 4 boru",
    "Yanda kopuk kablo": "Sağ yan taraf"
}

if fault_mode:
    st.sidebar.write("### Görevler (yeri gizli)")
    for i, (name, hint) in enumerate(FAULTS.items(), 1):
        st.sidebar.write(f"**{i}.** {name} - _{hint}_")
    st.sidebar.info("Modeli çevir, hatalı bölgeye tıkla!")

# GLB'yi oku - senin dosyan
# Eğer repo'da motor.glb varsa onu kullan
import os
glb_path = "motor.glb"
if not os.path.exists(glb_path):
    uploaded = st.sidebar.file_uploader("GLB yükle", type=["glb"])
    if uploaded:
        with open(glb_path, "wb") as f:
            f.write(uploaded.read())

# base64 encode for viewer
glb_b64 = ""
if os.path.exists(glb_path):
    with open(glb_path, "rb") as f:
        glb_b64 = base64.b64encode(f.read()).decode()

html_code = f""
<!DOCTYPE html>
<html>
<head>
<script type="importmap">
{{"imports":{{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}}}
</script>
<style>body{{margin:0;overflow:hidden;background:#0a0a0a}}#canvas{{width:100%;height:700px;display:block}} #score{{position:absolute;top:10px;left:10px;color:white;background:rgba(0,0,0,.6);padding:8px 12px;border-radius:8px;font-family:sans-serif}}</style>
</head>
<body>
<div id="score">Mod: {'HATA BULMA - Tıkla' if fault_mode else 'RENKLENDİRME'}</div>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {{OrbitControls}} from 'three/addons/controls/OrbitControls.js';
import {{GLTFLoader}} from 'three/addons/loaders/GLTFLoader.js';

const scene=new THREE.Scene(); scene.background=new THREE.Color(0x0a0a0a);
const camera=new THREE.PerspectiveCamera(45, window.innerWidth/700, 0.1, 100); camera.position.set(2,1,2);
const renderer=new THREE.WebGLRenderer({{canvas:document.getElementById('c'), antialias:true}}); renderer.setSize(window.innerWidth,700);
const controls=new OrbitControls(camera, renderer.domElement); controls.enableDamping=true; controls.autoRotate=true; controls.autoRotateSpeed=0.6;

scene.add(new THREE.AmbientLight(0xffffff, 0.8));
const dl=new THREE.DirectionalLight(0xffffff, 1.2); dl.position.set(3,5,3); scene.add(dl);
const dl2=new THREE.DirectionalLight(0xffffff, 0.6); dl2.position.set(-2,3,-2); scene.add(dl2);

// base
