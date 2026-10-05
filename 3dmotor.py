import streamlit as st
import streamlit.components.v1 as components
import base64, os

st.set_page_config(page_title="Oyak Horse Görme Testi", layout="wide")

# padding'i sadece icerik icin sifirla, basliklari ezme
st.markdown("""
<style>
.block-container {padding-top: 0rem!important; padding-left: 0rem!important; padding-right: 0rem!important; max-width: 100%!important;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stApp {background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%)!important;}
</style>
""", unsafe_allow_html=True)

# BASLIK - hep gorunur
st.markdown("""
<div style="padding:18px; background: rgba(255,255,255,0.06); border-bottom:1px solid rgba(255,255,255,0.1); text-align:center;">
  <h1 style="margin:0; color:#f8fafc; font-size:26px; font-weight:800;">Oyak Horse Görme Testi Uygulaması</h1>
  <p style="margin:6px 0 0 0; color:#94a3b8; font-size:13px;">Üstteki 4 vidadan 2'si eksik</p>
</div>
""", unsafe_allow_html=True)

# GLB BUL - debug
POSSIBLE_NAMES = ["motor-v2.glb", "motor.glb", "engine.glb", "car engine 3d model.glb"]
glb_b64 = ""
found = None
for name in POSSIBLE_NAMES:
    if os.path.exists(name):
        size = os.path.getsize(name)
        if size > 1000:
            found = name
            with open(name, "rb") as f:
                glb_b64 = base64.b64encode(f.read()).decode()
            st.success(f"✅ {name} yüklendi - {size/1024/1024:.2f} MB")
            break

if not found:
    st.error("❌ GLB bulunamadı! Klasörde motor-v2.glb var mı kontrol et")
    st.write(os.listdir("."))
    st.stop()

html_code = """
<!DOCTYPE html>
<html>
<head>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<style>
  html, body {margin:0; padding:0; overflow:hidden; background:#1e293b; width:100%; height:100%}
  #c {width:100vw; height:750px; display:block}
  #loading {position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); color:white; font-family:sans-serif; background:rgba(0,0,0,0.6); padding:10px 20px; border-radius:10px;}
</style>
</head>
<body>
<div id="loading">Motor yükleniyor...</div>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1e293b);
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/750, 0.1, 100);
camera.position.set(1.6, 0.9, 1.6);
const renderer = new THREE.WebGLRenderer({canvas:document.getElementById('c'), antialias:true});
renderer.setSize(window.innerWidth, 750);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.outputColorSpace = THREE.SRGBColorSpace;

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.autoRotate = true;

scene.add(new THREE.AmbientLight(0xffffff, 1.5));
let d1 = new THREE.DirectionalLight(0xffffff, 2); d1.position.set(5,10,5); scene.add(d1);
let d2 = new THREE.DirectionalLight(0xffffff, 1); d2.position.set(-5,4,-3); scene.add(d2);

const engineGroup = new THREE.Group(); scene.add(engineGroup);

const b64 = "__B64__";
try{
  const bytes = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
  const loader = new GLTFLoader();
  const draco = new DRACOLoader();
  draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
  loader.setDRACOLoader(draco);
  loader.parse(bytes.buffer, '', (gltf)=>{
    document.getElementById('loading').style.display='none';
    let model = gltf.scene;
    let box = new THREE.Box3().setFromObject(model);
    let center = box.getCenter(new THREE.Vector3());
    model.position.sub(center);
    model.position.y += 0.15;
    let size = box.getSize(new THREE.Vector3()).length();
    model.scale.setScalar(1.9/size);

    let allMeshes = [];
    model.traverse(o=>{ if(o.isMesh) allMeshes.push(o); });
    allMeshes.sort((a,b)=>{
      let ya = new THREE.Box3().setFromObject(a).getCenter(new THREE.Vector3()).y;
      let yb = new THREE.Box3().setFromObject(b).getCenter(new THREE.Vector3()).y;
      return yb - ya;
    });
    let top4 = allMeshes.slice(0,4);
    [0,2].forEach(i=>{ if(top4[i]) top4[i].visible=false; });

    engineGroup.add(model);
  }, (e)=>{ console.error(e); document.getElementById('loading').innerText='Yükleme hatası'; });
}catch(e){ document.getElementById('loading').innerText='Base64 hatası: '+e; }

function animate(){ requestAnimationFrame(animate); controls.update(); renderer.render(scene,camera); }
animate();
</script>
</body>
</html>
"""

final_html = html_code.replace("__B64__", glb_b64)
components.html(final_html, height=760, scrolling=False)
