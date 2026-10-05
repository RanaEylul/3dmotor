import streamlit as st
import base64, os
import streamlit.components.v1 as components

st.set_page_config(page_title="Oyak Horse", layout="wide")

st.markdown("""
<style>
header,footer{display:none}
.block-container{padding:0!important}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; color:white; padding:15px; margin:0; background:#0f172a;'>Oyak Horse Görme Testi Uygulaması</h2>", unsafe_allow_html=True)

# GLB yükle
b64 = ""
for name in ["motor-v2.glb","motor.glb"]:
    if os.path.exists(name):
        with open(name,"rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        break

if not b64:
    st.error("GLB yok")
    st.stop()

# BU KISIM HATA VERDIRMIYOR - sabit html, key yok
html_code = """
<!DOCTYPE html>
<html><body style="margin:0; background:#1e293b; overflow:hidden;">
<canvas id="c" style="width:100%; height:700px; display:block;"></canvas>
<script type="importmap">{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';
const scene=new THREE.Scene(); scene.background=new THREE.Color(0x1e293b);
const camera=new THREE.PerspectiveCamera(45, 800/700, 0.1, 100); camera.position.set(1.5,0.8,1.5);
const renderer=new THREE.WebGLRenderer({canvas:document.getElementById('c'), antialias:true}); renderer.setSize(window.innerWidth,700);
const controls=new OrbitControls(camera, renderer.domElement); controls.enableDamping=true; controls.autoRotate=true; controls.autoRotateSpeed=0.6;
scene.add(new THREE.AmbientLight(0xffffff,1.8));
const d=new THREE.DirectionalLight(0xffffff,2); d.position.set(5,10,5); scene.add(d);
const group=new THREE.Group(); scene.add(group);
const b64="__B64__";
const bytes=Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
const loader=new GLTFLoader(); const draco=new DRACOLoader(); draco.setDecoderPath('https://www.gstatic.com/draco/v1.5.6/'); loader.setDRACOLoader(draco);
loader.parse(bytes.buffer,'',(gltf)=>{
  let m=gltf.scene; let box=new THREE.Box3().setFromObject(m); let c=box.getCenter(new THREE.Vector3()); m.position.sub(c); m.position.y+=0.2; let s=box.getSize(new THREE.Vector3()).length(); m.scale.setScalar(2/s);
  // ÜSTTEKI 4 VIDADAN 2'SINI GIZLE
  let meshes=[]; m.traverse(o=>{if(o.isMesh) meshes.push(o);});
  meshes.sort((a,b)=> new THREE.Box3().setFromObject(b).getCenter(new THREE.Vector3()).y - new THREE.Box3().setFromObject(a).getCenter(new THREE.Vector3()).y );
  let top4=meshes.slice(0,4); if(top4[0]) top4[0].visible=false; if(top4[2]) top4[2].visible=false;
  group.add(m);
});
(function loop(){ requestAnimationFrame(loop); controls.update(); renderer.render(scene,camera); })();
</script></body></html>
""".replace("__B64__", b64)

components.html(html_code, height=710, scrolling=False)

# BUNLARI HTML'DEN SONRA YAZMA - hata sebebi
# st.success falan koyma buraya
