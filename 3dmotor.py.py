import streamlit as st
import streamlit.components.v1 as components
import os, base64

st.set_page_config(page_title="3D Motor", layout="wide")
st.markdown("<h2 style='text-align:center'>🚗 İnteraktif 3D Araba Motoru</h2>", unsafe_allow_html=True)

# SENIN YENI KUCULTULMUS DOSYAN
FILE = "motor.glb"

if not os.path.exists(FILE):
    st.error(f"{FILE} bulunamadi!")
    st.write("Klasorde olanlar:", os.listdir("."))
    st.stop()

size_bytes = os.path.getsize(FILE)
size_mb = size_bytes / 1024 / 1024

if size_bytes < 1000:
    st.error(f"{FILE} BOS! {size_bytes} byte - GitHub'a tekrar yukle")
    st.stop()

st.sidebar.success(f"{FILE} OK - {size_mb:.2f} MB (kucultulmus)")

with open(FILE, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

# f-string yok, {} hatasi yok
html_template = """
<!DOCTYPE html>
<html><head>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<style>
body{margin:0;background:#121212;overflow:hidden}
#c{width:100%;height:720px;display:block}
</style>
</head><body>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x121212);
const camera=new THREE.PerspectiveCamera(50, window.innerWidth/720, 0.1, 1000);
camera.position.set(1.6, 0.9, 1.6);

const renderer=new THREE.WebGLRenderer({canvas:document.getElementById('c'),antialias:true});
renderer.setSize(window.innerWidth, 720);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.outputColorSpace=THREE.SRGBColorSpace;

const controls=new OrbitControls(camera, renderer.domElement);
controls.enableDamping=true;
controls.dampingFactor=0.08;
controls.autoRotate=true;
controls.autoRotateSpeed=0.5;

scene.add(new THREE.AmbientLight(0xffffff, 1.4));
const dir1=new THREE.DirectionalLight(0xffffff, 1.8);
dir1.position.set(5,10,5);
scene.add(dir1);
const dir2=new THREE.DirectionalLight(0xffffff, 0.7);
dir2.position.set(-5,3,-3);
scene.add(dir2);

const loader=new THREE.GLTFLoader();
const draco=new DRACOLoader();
draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
loader.setDRACOLoader(draco);

const b64data="__B64__";
const binStr=atob(b64data);
const bytes=new Uint8Array(binStr.length);
for(let i=0;i<binStr.length;i++){ bytes[i]=binStr.charCodeAt(i); }

loader.parse(bytes.buffer, '', (gltf)=>{
  let model=gltf.scene;
  const box=new THREE.Box3().setFromObject(model);
  const center=box.getCenter(new THREE.Vector3());
  model.position.sub(center);
  const size=box.getSize(new THREE.Vector3()).length();
  model.scale.setScalar(2.0 / (size || 1));
  
  // TABLA YOK - sadece acik gri gercekci motor
  model.traverse((o)=>{
    if(o.isMesh){
      o.material=new THREE.MeshStandardMaterial({
        color: 0xd1d5db,
        roughness: 0.5,
        metalness: 0.2
      });
    }
  });
  scene.add(model);
});

function animate(){
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene,camera);
}
animate();
</script>
</body></html>
"""

final_html = html_template.replace("__B64__", b64)
components.html(final_html, height=730)
