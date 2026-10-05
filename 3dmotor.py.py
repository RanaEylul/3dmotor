import streamlit as st
import streamlit.components.v1 as components
import os, base64

st.set_page_config(layout="wide")

FILE = "car engine 3d model.glb"
if not os.path.exists(FILE):
    for alt in ["motor.glb", "model.glb", "car-engine.glb", "engine.glb"]:
        if os.path.exists(alt):
            FILE = alt
            break

if not os.path.exists(FILE):
    st.error(f"GLB yok! Dosyalar: {os.listdir('.')}")
    st.stop()

size = os.path.getsize(FILE)/1024/1024
st.sidebar.write(f"{FILE}: {size:.2f} MB")

with open(FILE, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

html = """
<!DOCTYPE html>
<html><head>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<style>
body{margin:0;background:#151515;color:white;font-family:monospace}
#c{width:100%;height:700px;display:block}
#log{position:absolute;top:10px;left:10px;background:rgba(0,0,0,0.8);padding:10px;border-radius:6px;max-width:500px;white-space:pre-wrap}
</style>
</head><body>
<div id="log">Basliyor...</div>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

const logEl = document.getElementById('log');
function log(t){ logEl.textContent += "\\n" + t; console.log(t); }

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x151515);
const camera=new THREE.PerspectiveCamera(50, window.innerWidth/700, 0.1, 1000);
camera.position.set(1.5,1,1.5);
const renderer=new THREE.WebGLRenderer({canvas:document.getElementById('c'),antialias:true});
renderer.setSize(window.innerWidth,700);
renderer.outputColorSpace=THREE.SRGBColorSpace;

const controls=new OrbitControls(camera,renderer.domElement);
controls.enableDamping=true;
controls.autoRotate=true;

scene.add(new THREE.AmbientLight(0xffffff,1.5));
const dl=new THREE.DirectionalLight(0xffffff,2); dl.position.set(5,10,5); scene.add(dl);

const loader=new GLTFLoader();
const draco=new DRACOLoader();
draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
loader.setDRACOLoader(draco);

log('Loader hazir, GLB parse ediliyor...');

try{
const b64Str="__B64__";
log('B64 uzunluk: '+b64Str.length);
const binStr=atob(b64Str);
const bytes=new Uint8Array(binStr.length);
for(let i=0;i<binStr.length;i++) bytes[i]=binStr.charCodeAt(i);

loader.parse(bytes.buffer,'', (gltf)=>{
  log('PARSE OK! Scene icinde: '+gltf.scene.children.length+' obje');
  let m=gltf.scene;
  const box=new THREE.Box3().setFromObject(m);
  log('Box size: '+box.getSize(new THREE.Vector3()).length().toFixed(2));
  if(box.getSize(new THREE.Vector3()).length() < 0.001){
    log('HATA: Model cok kucuk veya bos!');
  }
  m.position.sub(box.getCenter(new THREE.Vector3()));
  m.scale.setScalar(1.8 / (box.getSize(new THREE.Vector3()).length() || 1));
  let meshCount=0;
  m.traverse(o=>{
    if(o.isMesh){
      meshCount++;
      try{
        o.material=new THREE.MeshStandardMaterial({color:0xd1d5db, roughness:0.5, metalness:0.2});
      }catch(e){}
    }
  });
  log('Mesh sayisi: '+meshCount);
  scene.add(m);
  log('Eklendi! Gorunmesi lazim.');
}, (e)=>{
  log('PARSE HATASI: '+e.message);
  console.error(e);
});
}catch(err){
  log('JS HATASI: '+err.message);
}

function animate(){ requestAnimationFrame(animate); controls.update(); renderer.render(scene,camera); }
animate();
</script>
</body></html>
"""

final = html.replace("__B64__", b64)
components.html(final, height=730)

st.caption("Ekranda sol üstte log çıkacak. Orada ne yazdığını bana at.")
