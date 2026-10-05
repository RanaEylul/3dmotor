import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="Oyak Horse Görme Testi", layout="wide")

st.markdown("""
<style>
.block-container {padding: 0!important; max-width: 100%!important;}
header, footer {visibility: hidden; height:0;}
.stApp {background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%)!important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin:0; padding:18px 24px 14px 24px; background: rgba(255,255,255,0.06); border-bottom:1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px); text-align:center;">
  <h1 style="margin:0; color:#f8fafc; font-weight:800; font-size:26px;">Oyak Horse Görme Testi Uygulaması</h1>
  <p style="margin:6px 0 0 0; color:#94a3b8; font-size:13px;">Eksik vidaları bulmak için modele tıkla</p>
  <div style="margin-top:10px; display:flex; justify-content:center; gap:8px;">
    <span style="background:#0ea5e9; color:white; padding:5px 14px; border-radius:20px; font-size:11px; font-weight:700;">LIVE 3D</span>
    <span style="background:rgba(255,255,255,0.1); color:#cbd5e1; padding:5px 14px; border-radius:20px; font-size:11px;">Tıklanabilir</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🔧 Test Ayarları")
test_mode = st.sidebar.radio("Mod", ["Sağlam Motor", "Vida Eksik (Test)"], key="mode")
eksik_sayi = st.sidebar.slider("Kaç vida eksik", 1, 6, 2, disabled=(test_mode=="Sağlam Motor"), key="count")
st.sidebar.info("Mode değiştirince 3D otomatik yenilenir. Eksik modda motora tıkla!")

POSSIBLE_NAMES = ["motor-v2.glb", "motor.glb", "engine.glb"]
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
<style>
  html, body {margin:0; padding:0; overflow:hidden; background:#1e293b; width:100%; height:100%; cursor: crosshair;}
  #c {width:100vw; height:calc(100vh - 105px); display:block}
  #score {position:fixed; top:10px; left:50%; transform:translateX(-50%); background:rgba(0,0,0,0.7); color:white; padding:8px 16px; border-radius:20px; font-family:sans-serif; font-size:13px; z-index:10}
</style>
</head>
<body>
<div id="score">Yükleniyor...</div>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

const TEST_MODE = "__TESTMODE__";
const EKSIK_SAYI = __EKSIK__;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1e293b);
const camera = new THREE.PerspectiveCamera(42, window.innerWidth/(window.innerHeight-105), 0.1, 100);
camera.position.set(1.6, 0.9, 1.6);

const renderer = new THREE.WebGLRenderer({canvas:document.getElementById('c'), antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight-105);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.outputColorSpace = THREE.SRGBColorSpace;

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = false; // tiklanabilir olsun diye kapattim

scene.add(new THREE.AmbientLight(0xffffff, 1.2));
let d1 = new THREE.DirectionalLight(0xffffff, 2.0); d1.position.set(5,10,5); scene.add(d1);
let d2 = new THREE.DirectionalLight(0xffffff, 0.9); d2.position.set(-5,4,-3); scene.add(d2);

const engineGroup = new THREE.Group(); scene.add(engineGroup);
let missingPositions = [];
let found = 0;

const b64 = "__B64__";
const bytes = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
const loader = new GLTFLoader();
const draco = new DRACOLoader();
draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
loader.setDRACOLoader(draco);

loader.parse(bytes.buffer, '', (gltf)=>{
  let model = gltf.scene;
  let box = new THREE.Box3().setFromObject(model);
  let center = box.getCenter(new THREE.Vector3());
  model.position.sub(center);
  model.position.y += 0.15;
  let size = box.getSize(new THREE.Vector3()).length();
  model.scale.setScalar(1.9/size);

  let allMeshes = [];
  model.traverse(o=>{ if(o.isMesh){ allMeshes.push(o); }});
  allMeshes.sort((a,b)=>{
    let sa = new THREE.Box3().setFromObject(a).getSize(new THREE.Vector3()).length();
    let sb = new THREE.Box3().setFromObject(b).getSize(new THREE.Vector3()).length();
    return sa - sb;
  });

  if(TEST_MODE.includes("Vida Eksik")){
    for(let i=0; i<EKSIK_SAYI && i<allMeshes.length; i++){
      let pos = new THREE.Box3().setFromObject(allMeshes[i]).getCenter(new THREE.Vector3());
      missingPositions.push(pos.clone());
      allMeshes[i].visible = false;
      // delik gozukmesi icin kucuk siyah nokta koy - vida yokmus gibi
      let hole = new THREE.Mesh(new THREE.CircleGeometry(0.015, 16), new THREE.MeshBasicMaterial({color:0x000000}));
      hole.position.copy(pos);
      hole.position.y += 0.001;
      engineGroup.add(hole);
    }
  }

  engineGroup.add(model);
  document.getElementById('score').innerText = TEST_MODE.includes("Eksik")? `Bul: 0 / ${EKSIK_SAYI} - Eksik vidaların olduğu yere tıkla!` : "Sağlam Motor - Referans";
});

// TIKLAMA - raycaster
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
renderer.domElement.addEventListener('click', (e)=>{
  if(!TEST_MODE.includes("Eksik") || missingPositions.length===0) return;
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / (window.innerHeight-105)) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  let intersects = raycaster.intersectObjects(engineGroup.children, true);
  if(intersects.length>0){
    let p = intersects[0].point;
    for(let mp of missingPositions){
      if(p.distanceTo(mp) < 0.15){
        found++;
        missingPositions = missingPositions.filter(m=> m!==mp);
        document.getElementById('score').innerText = `Bulundu: ${found} / ${EKSIK_SAYI} 🎉`;
        if(found>=EKSIK_SAYI) document.getElementById('score').innerText = `TEBRIKLER! Tum eksikleri buldun! ${found}/${EKSIK_SAYI}`;
        break;
      }
    }
  }
});

function animate(){ requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }
animate();
</script>
</body>
</html>
"""

final_html = html_code.replace("__B64__", glb_b64).replace("__TESTMODE__", test_mode).replace("__EKSIK__", str(eksik_sayi))
# KEY cok onemli - tiklayinca yenilenmesi icin
components.html(final_html, height=820, scrolling=False, key=f"{test_mode}-{eksik_sayi}")
