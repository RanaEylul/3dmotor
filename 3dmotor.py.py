import streamlit as st
import streamlit.components.v1 as components
import os, base64

st.set_page_config(page_title="3D Motor", layout="wide")
st.markdown("<h2 style='text-align:center'>🚗 İnteraktif 3D Araba Motoru</h2>", unsafe_allow_html=True)

FILE = "car engine 3d model.glb"
if not os.path.exists(FILE):
    # alternatif isimleri de dene
    for alt in ["motor.glb", "model.glb", "car-engine.glb"]:
        if os.path.exists(alt):
            FILE = alt
            break

if not os.path.exists(FILE):
    st.error(f"{FILE} bulunamadi! Klasordekiler: {os.listdir('.')}")
    st.stop()

size_mb = os.path.getsize(FILE) / 1024 / 1024
st.sidebar.success(f"Bulundu: {FILE} ({size_mb:.1f} MB)")

with open(FILE, "rb") as f:
    b64_data = base64.b64encode(f.read()).decode()

# F-STRING KULLANMIYORUZ - BU YUZDEN } HATASI ASLA OLMAZ
# __B64__ yerine sonradan koyuyoruz
html_code = """
<html><head>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<style>body{margin:0;background:#121212} #c{width:100%;height:700px;display:block}</style>
</head><body>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

const scene=new THREE.Scene(); 
scene.background=new THREE.Color(0x121212);
const camera=new THREE.PerspectiveCamera(50, window.innerWidth/700, 0.1, 100); 
camera.position.set(1.5,0.8,1.5);
const renderer=new THREE.WebGLRenderer({canvas:document.getElementById('c'),antialias:true}); 
renderer.setSize(window.innerWidth,700);
renderer.outputColorSpace=THREE.SRGBColorSpace;
const controls=new OrbitControls(camera,renderer.domElement); 
controls.enableDamping=true; 
controls.autoRotate=true;
controls.autoRotateSpeed=0.6;

scene.add(new THREE.AmbientLight(0xffffff,1.2));
const d=new THREE.DirectionalLight(0xffffff,1.5); 
d.position.set(5,10,5); 
scene.add(d);
const d2=new THREE.DirectionalLight(0xffffff,0.6);
d2.position.set(-5,3,-3);
scene.add(d2);

const loader=new THREE.GLTFLoader();
const b64="__B64__";
const bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));
loader.parse(bytes.buffer,'',(gltf)=>{
  let m=gltf.scene;
  let box=new THREE.Box3().setFromObject(m);
  let center=box.getCenter(new THREE.Vector3());
  m.position.sub(center);
  let size=box.getSize(new THREE.Vector3()).length();
  m.scale.setScalar(1.8/size);
  m.traverse(o=>{
    if(o.isMesh){
      o.material=new THREE.MeshStandardMaterial({color:0xd1d5db,roughness:0.5,metalness:0.2});
    }
  });
  scene.add(m);
});

function animate(){
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene,camera);
}
animate();
</script></body></html>
"""

# sadece burda replace ediyoruz, f-string yok
final_html = html_code.replace("__B64__", b64_data)

components.html(final_html, height=720)
