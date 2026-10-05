import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="3D Araba Motoru Simulasyonu", layout="wide")

st.markdown("<h2 style='text-align:center'>🚗 İnteraktif 3D Araba Motoru Simülasyonu</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;opacity:.6'>Laptop trackpad (iki parmak) ve fare tekerleği desteği aktifleştirildi.</p>", unsafe_allow_html=True)

# --- SIDEBAR: RENKLENDİRME ---
st.sidebar.header("🎨 Renklendirme")
engine_color = st.sidebar.color_picker("Motor Gövde", "#8a8d91")
cover_color = st.sidebar.color_picker("Kapak Rengi", "#4b5563")
accent_color = st.sidebar.color_picker("Vurgu / Kayış", "#1f2937")

st.sidebar.divider()
st.sidebar.header("🎯 Hata Bulma")
fault_mode = st.sidebar.toggle("Hata Modunu Aç", value=False)

# GLB dosyası - repo kökünde motor.glb ara
GLB_FILE = "motor.glb"
# Eğer yoksa upload iste
glb_b64 = ""
if os.path.exists(GLB_FILE):
    with open(GLB_FILE, "rb") as f:
        glb_b64 = base64.b64encode(f.read()).decode()
else:
    up = st.sidebar.file_uploader("motor.glb yükle", type=["glb"])
    if up:
        glb_b64 = base64.b64encode(up.read()).decode()

# --- FIX: f-string icinde uc tirnak catismasini onlemek icin disariyi f''' yaptik ---
# Icinde hic ''' yok, sadece " var. Bu yuzden patlamaz.
html_template = f'''
<!DOCTYPE html>
<html>
<head>
<script type="importmap">
{{"imports":{{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}}}
</script>
<style>
  body{{margin:0;overflow:hidden;background:#0a0a0a}}
  #canvas{{width:100%;height:680px;display:block}}
  #score{{position:absolute;top:10px;left:10px;color:white;background:rgba(0,0,0,.6);padding:8px 12px;border-radius:8px;font-family:sans-serif;font-size:13px}}
</style>
</head>
<body>
<div id="score">Mod: FAULT</div>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {{OrbitControls}} from 'three/addons/controls/OrbitControls.js';
import {{GLTFLoader}} from 'three/addons/loaders/GLTFLoader.js';

const isFaultMode = {str(fault_mode).lower()};

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0a);
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/700, 0.1, 100);
camera.position.set(2.2,1.2,2.2);
const renderer = new THREE.WebGLRenderer({{canvas:document.getElementById('c'), antialias:true}});
renderer.setSize(window.innerWidth, 680);
renderer.setPixelRatio(window.devicePixelRatio);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.6;

scene.add(new THREE.AmbientLight(0xffffff, 0.9));
const d1 = new THREE.DirectionalLight(0xffffff, 1.2); d1.position.set(3,5,4); scene.add(d1);
const d2 = new THREE.DirectionalLight(0xffffff, 0.5); d2.position.set(-3,2,-2); scene.add(d2);

const engineGroup = new THREE.Group();
scene.add(engineGroup);
const plat = new THREE.Mesh(new THREE.CylinderGeometry(1.8,1.8,0.08,64), new THREE.MeshStandardMaterial({{color:0x1c1f27}}));
plat.position.y = -0.8; scene.add(plat);

let modelMeshes = [];
let faultMeshes = [];
const FAULT_POS = [[-1.1,0.3,0.2],[0.2,-0.4,0.65],[0.1,0.2,-0.75],[0,0.6,0.3],[0.9,0.6,0.1]];

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
      model.scale.setScalar(1.6/size);
      model.traverse(o=>{{
        if(o.isMesh){{
          o.castShadow = true;
          // BEYAZ SORUNU FIX: orijinal material yerine yeni PBR material
          const isCover = o.position.y > 0.2;
          const col = isCover ? "{cover_color}" : "{engine_color}";
          o.material = new THREE.MeshStandardMaterial({{
            color: new THREE.Color(col),
            roughness: 0.45,
            metalness: 0.25
          }});
          if(o.name.toLowerCase().includes('belt') || o.name.toLowerCase().includes('pulley')){{
            o.material.color.set("{accent_color}");
          }}
          modelMeshes.push(o);
        }}
      }});
      engineGroup.add(model);
      createFaults();
    }});
  }}catch(e){{ console.error(e); }}
}}

function createFaults(){{
  faultMeshes = [];
  FAULT_POS.forEach((p,i)=>{{
    const mat = new THREE.MeshBasicMaterial({{color:0xff0000, transparent:true, opacity: isFaultMode ? 0.18 : 0.0}});
    const sph = new THREE.Mesh(new THREE.SphereGeometry(0.15,16,16), mat);
    sph.position.set(p[0], p[1], p[2]);
    sph.userData.fault = i;
    engineGroup.add(sph);
    faultMeshes.push(sph);
    const ringMat = new THREE.MeshBasicMaterial({{color:0x22c55e, side:THREE.DoubleSide, transparent:true, opacity:0}});
    const ring = new THREE.Mesh(new THREE.RingGeometry(0.15,0.22,24), ringMat);
    ring.position.set(p[0], p[1], p[2]);
    ring.userData.ring = i;
    engineGroup.add(ring);
  }});
}}

const ray = new THREE.Raycaster();
const mouse = new THREE.Vector2();

renderer.domElement.addEventListener('click', (e)=>{{
  const rect = renderer.domElement.getBoundingClientRect();
  mouse.x = ((e.clientX - rect.left)/rect.width)*2 -1;
  mouse.y = -((e.clientY - rect.top)/rect.height)*2 +1;
  ray.setFromCamera(mouse, camera);
  if(isFaultMode){{
    const hits = ray.intersectObjects(faultMeshes);
    if(hits.length>0){{
      const obj = hits[0].object;
      obj.material.color.set(0x22c55e);
      obj.material.opacity = 0.6;
      const idx = obj.userData.fault;
      engineGroup.children.forEach(c=>{{ if(c.userData.ring===idx) c.material.opacity=1; }});
      document.getElementById('score').textContent = 'Bulundu: ' + (idx+1) + ' / 5';
    }}
  }}
}});

function animate(){{
  requestAnimationFrame(animate);
  controls.update();
  engineGroup.children.forEach(c=>{{ if(c.userData.ring!==undefined && c.material.opacity>0) c.lookAt(camera.position); }});
  renderer.render(scene, camera);
}}
animate();

loadFromBase64("{glb_b64}");

window.addEventListener('resize', ()=>{{
  camera.aspect = window.innerWidth/700;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, 680);
}});

document.getElementById('score').textContent = isFaultMode ? 'HATA BULMA - Kirmizi alanlara tikla' : 'RENKLENDIRME - Yan menuden renk sec';
</script>
</body>
</html>
'''

components.html(html_template, height=720)

if not glb_b64:
    st.warning("motor.glb bulunamadi. Repo kokune motor.glb yukle veya sidebar'dan yukle.")
