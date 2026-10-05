import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="3D Araba Motoru Simulasyonu", layout="wide")

st.markdown("<h2 style='text-align:center'>🚗 İnteraktif 3D Araba Motoru Simülasyonu</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;opacity:.6'>Laptop trackpad (iki parmak) ve fare tekerleği desteği aktif.</p>", unsafe_allow_html=True)

# Senin dosya adın - bosluklu isimleri de dener
POSSIBLE_NAMES = [
    "car engine 3d model.glb",
    "car engine 3d model.glb",
    
]

glb_b64 = ""
found_file = None
for name in POSSIBLE_NAMES:
    if os.path.exists(name):
        found_file = name
        with open(name, "rb") as f:
            glb_b64 = base64.b64encode(f.read()).decode()
        break

if found_file:
    st.sidebar.success(f"Yüklü: {found_file}")
else:
    up = st.sidebar.file_uploader("GLB yükle", type=["glb"])
    if up:
        glb_b64 = base64.b64encode(up.read()).decode()

# SADECE GORUNTULEME - tabla yok, hata modu yok, acik gri gercekci renk
html_template = f'''
<!DOCTYPE html>
<html>
<head>
<script type="importmap">
{{"imports":{{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}}}
</script>
<style>
  body{{margin:0;overflow:hidden;background:#0a0a0a}}
  #c{{width:100%;height:750px;display:block}}
</style>
</head>
<body>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {{OrbitControls}} from 'three/addons/controls/OrbitControls.js';
import {{GLTFLoader}} from 'three/addons/loaders/GLTFLoader.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0e0e12);
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/750, 0.1, 100);
camera.position.set(1.8, 1.0, 1.8);

const renderer = new THREE.WebGLRenderer({{canvas:document.getElementById('c'), antialias:true, alpha:true}});
renderer.setSize(window.innerWidth, 750);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true;
renderer.outputColorSpace = THREE.SRGBColorSpace;

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.5;
controls.minDistance = 0.8;
controls.maxDistance = 6;

// ISIKLAR - gercekci gri icin guclu aydinlatma
scene.add(new THREE.AmbientLight(0xffffff, 1.1));
const d1 = new THREE.DirectionalLight(0xffffff, 1.5); d1.position.set(4,6,4); d1.castShadow = true; scene.add(d1);
const d2 = new THREE.DirectionalLight(0xffffff, 0.8); d2.position.set(-4,3,-3); scene.add(d2);
const d3 = new THREE.DirectionalLight(0xffffff, 0.5); d3.position.set(0,-2,2); scene.add(d3);

const engineGroup = new THREE.Group();
scene.add(engineGroup);
// TABLA KALDIRILDI - artik alt taraf tamamen gorunuyor

function loadFromBase64(b64){{
  if(!b64) return;
  try{{
    const bytes = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
    const loader = new GLTFLoader();
    loader.parse(bytes.buffer, '', (gltf)=>{{
      const model = gltf.scene;
      const box = new THREE.Box3().setFromObject(model);
      const center = box.getCenter(new THREE.Vector3());
      model.position.sub(center);
      const size = box.getSize(new THREE.Vector3()).length();
      model.scale.setScalar(1.8/size);
      
      model.traverse(o=>{{
        if(o.isMesh){{
          // GERCEKCI ACIK GRI MOTOR RENGI - sabit
          o.material = new THREE.MeshStandardMaterial({{
            color: new THREE.Color(0xd1d5db),
            roughness: 0.45,
            metalness: 0.25,
            flatShading: false
          }});
          o.castShadow = true;
          o.receiveShadow = true;
        }}
      }});
      engineGroup.add(model);
    }});
  }}catch(e){{ console.error(e); }}
}}

function animate(){{
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}}
animate();

loadFromBase64("{glb_b64}");

window.addEventListener('resize', ()=>{{
  camera.aspect = window.innerWidth/750;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, 750);
}});
</script>
</body>
</html>
'''

components.html(html_template, height=760)

if not glb_b64:
    st.error("GLB bulunamadi! Repo kokune 'car engine 3d model.glb' yukle.")
    st.write("Mevcut dosyalar:", os.listdir("."))
