import streamlit as st
import streamlit.components.v1 as components
import base64, os

st.set_page_config(page_title="Oyak Horse Görme Testi", layout="wide")

st.markdown("""
<style>
.block-container {padding: 0 !important; max-width: 100% !important;}
header, footer {visibility: hidden; height:0;}
.stApp {background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:14px; background: rgba(255,255,255,0.06); border-bottom:1px solid rgba(255,255,255,0.1);">
  <h1 style="margin:0; color:#f8fafc; font-size:26px; font-weight:800;">Oyak Horse Görme Testi Uygulaması</h1>
  <p style="margin:4px 0 0 0; color:#94a3b8; font-size:13px;">Defektli motor görselleri oluştur</p>
</div>
""", unsafe_allow_html=True)

# DEFECT PANEL
st.sidebar.title("🔧 Defekt Ayarları")
defect_type = st.sidebar.selectbox("Hata Tipi", ["Sağlam (Referans)", "Vida Eksik", "Vida Gevşek", "Çatlak Blok", "Yağ Kaçağı", "Conta Eksik", "Pas / Korozyon"])
defect_count = st.sidebar.slider("Kaç vida / nokta gizlensin", 1, 8, 2)
show_marker = st.sidebar.checkbox("Hata noktasını kırmızı işaretle", True)
auto_rotate = st.sidebar.checkbox("Otomatik dönme", True)

if st.sidebar.button("📸 Ekran Görüntüsü Al (tarayıcıdan sağ tık)"):
    st.sidebar.info("3D alanın üstüne sağ tık > Resmi farklı kaydet yapabilirsin")

POSSIBLE_NAMES = ["motor-v2.glb", "motor.glb"]
glb_b64 = ""
for name in POSSIBLE_NAMES:
    if os.path.exists(name) and os.path.getsize(name) > 1000:
        with open(name, "rb") as f:
            glb_b64 = base64.b64encode(f.read()).decode()
        break

html_code = """
<!DOCTYPE html>
<html>
<head>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<style>html,body{margin:0;background:#1e293b;overflow:hidden} #c{width:100vw;height:calc(100vh - 80px);display:block}</style>
</head>
<body>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

const DEFECT_TYPE = "__DEFECT__";
const DEFECT_COUNT = __COUNT__;
const SHOW_MARKER = __MARKER__;
const AUTO_ROT = __AUTOROT__;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1e293b);
const camera = new THREE.PerspectiveCamera(42, window.innerWidth/(window.innerHeight-80), 0.1, 100);
camera.position.set(1.6, 0.9, 1.6);
const renderer = new THREE.WebGLRenderer({canvas:document.getElementById('c'), antialias:true, preserveDrawingBuffer:true});
renderer.setSize(window.innerWidth, window.innerHeight-80);
renderer.outputColorSpace = THREE.SRGBColorSpace;

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.autoRotate = AUTO_ROT;

scene.add(new THREE.AmbientLight(0xffffff, 1.2));
let d1 = new THREE.DirectionalLight(0xffffff, 2.0); d1.position.set(5,10,5); scene.add(d1);
let d2 = new THREE.DirectionalLight(0xffffff, 0.8); d2.position.set(-5,4,-3); scene.add(d2);

const engineGroup = new THREE.Group(); scene.add(engineGroup);

const b64 = "__B64__";
const bytes = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
const loader = new GLTFLoader();
const draco = new DRACOLoader();
draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
loader.setDRACOLoader(draco);

loader.parse(bytes.buffer, '', (gltf)=>{
  let model = gltf.scene;
  let box = new THREE.Box3().setFromObject(model);
  model.position.sub(box.getCenter(new THREE.Vector3()));
  model.position.y += 0.15;
  let size = box.getSize(new THREE.Vector3()).length();
  model.scale.setScalar(1.9/size);
  
  let allMeshes = [];
  model.traverse(o=>{ if(o.isMesh) allMeshes.push(o); });
  // En kucuk mesleri vida olarak kabul et
  allMeshes.sort((a,b)=>{
    let ba = new THREE.Box3().setFromObject(a).getSize(new THREE.Vector3()).length();
    let bb = new THREE.Box3().setFromObject(b).getSize(new THREE.Vector3()).length();
    return ba - bb;
  });

  if(DEFECT_TYPE !== "Sağlam (Referans)"){
    let toHide = allMeshes.slice(0, DEFECT_COUNT);
    toHide.forEach(m=>{
      if(DEFECT_TYPE.includes("Vida Eksik") || DEFECT_TYPE.includes("Conta Eksik")){
        m.visible = false;
      }
      if(DEFECT_TYPE.includes("Gevşek")){
        m.position.x += 0.02;
        m.rotation.z += 0.3;
      }
      if(DEFECT_TYPE.includes("Çatlak")){
        m.material = m.material.clone();
        m.material.wireframe = true;
        m.material.color.set(0xff0000);
      }
      if(SHOW_MARKER){
        let pos = new THREE.Box3().setFromObject(m).getCenter(new THREE.Vector3());
        let marker = new THREE.Mesh(new THREE.SphereGeometry(0.03, 16, 16), new THREE.MeshBasicMaterial({color:0xff0000}));
        marker.position.copy(pos);
        engineGroup.add(marker);
        let ring = new THREE.Mesh(new THREE.RingGeometry(0.04,0.06,32), new THREE.MeshBasicMaterial({color:0xff0000, side:THREE.DoubleSide}));
        ring.position.copy(pos);
        ring.lookAt(camera.position);
        engineGroup.add(ring);
      }
    });
    
    if(DEFECT_TYPE.includes("Yağ Kaçağı")){
      let leak = new THREE.Mesh(new THREE.CircleGeometry(0.15,32), new THREE.MeshStandardMaterial({color:0x111111, roughness:0.1, metalness:0}));
      leak.rotation.x = -Math.PI/2;
      leak.position.set(0,-0.6,0);
      engineGroup.add(leak);
    }
  }

  engineGroup.add(model);
});

function animate(){ requestAnimationFrame(animate); controls.update(); renderer.render(scene,camera); }
animate();
</script>
</body>
</html>
"""

final_html = html_code.replace("__B64__", glb_b64)\
    .replace("__DEFECT__", defect_type)\
    .replace("__COUNT__", str(defect_count))\
    .replace("__MARKER__", "true" if show_marker else "false")\
    .replace("__AUTOROT__", "true" if auto_rotate else "false")

components.html(final_html, height=780, scrolling=False)
