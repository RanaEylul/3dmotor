import streamlit as st
import streamlit.components.v1 as components
import os, base64

st.set_page_config(page_title="3D Motor", layout="wide")
st.markdown("<h2 style='text-align:center'>🚗 İnteraktif 3D Araba Motoru</h2>", unsafe_allow_html=True)

FILE = "motor-v2.glb"

if not os.path.exists(FILE):
    st.error(f"{FILE} bulunamadi! Klasor: {os.listdir('.')}")
    st.stop()

size = os.path.getsize(FILE)
if size < 1000:
    st.error(f"{FILE} BOS ({size} byte)!")
    st.stop()

st.sidebar.success(f"{FILE} - {size/1024/1024:.2f} MB")

with open(FILE, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

html_template = """
<!DOCTYPE html>
<html><head>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<style>body{margin:0;background:#121212} #c{width:100%;height:720px;display:block}</style>
</head><body>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';
const scene=new THREE.Scene(); scene.background=new THREE.Color(0x121212);
const camera=new THREE.PerspectiveCamera(50, innerWidth/720, 0.1, 1000); camera.position.set(1.6,0.9,1.6);
const renderer=new THREE.WebGLRenderer({canvas:document.getElementById('c'),antialias:true}); renderer.setSize(innerWidth,720);
renderer.outputColorSpace=THREE.SRGBColorSpace;
const controls=new OrbitControls(camera,renderer.domElement); controls.enableDamping=true; controls.autoRotate=true;
scene.add(new THREE.AmbientLight(0xffffff,1.4));
let d1=new THREE.DirectionalLight(0xffffff,1.8); d1.position.set(5,10,5); scene.add(d1);
let d2=new THREE.DirectionalLight(0xffffff,0.7); d2.position.set(-5,3,-3); scene.add(d2);
const loader=new THREE.GLTFLoader(); const draco=new DRACOLoader(); draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/'); loader.setDRACOLoader(draco);
const bytes=Uint8Array.from(atob("__B64__"),c=>c.charCodeAt(0));
loader.parse(bytes.buffer,'',(gltf)=>{
  let m=gltf.scene; let box=new THREE.Box3().setFromObject(m); m.position.sub(box.getCenter(new THREE.Vector3())); m.scale.setScalar(2.0/(box.getSize(new THREE.Vector3()).length()||1));
  m.traverse(o=>{ if(o.isMesh) o.material=new THREE.MeshStandardMaterial({color:0xd1d5db,roughness:0.5,metalness:0.2}); });
  scene.add(m);
});
(function anim(){requestAnimationFrame(anim); controls.update(); renderer.render(scene,camera);})();
</script></body></html>
"""

final_html = html_template.replace("__B64__", b64)
components.html(final_html, height=730)
