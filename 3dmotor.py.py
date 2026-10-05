import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align:center'>🚗 İnteraktif 3D Araba Motoru Simülasyonu</h2>", unsafe_allow_html=True)

GLB_NAME = "car engine 3d model.glb"

if not os.path.exists(GLB_NAME):
    st.error(f"{GLB_NAME} bulunamadı!")
    st.write("Klasördeki dosyalar:", os.listdir("."))
    st.stop()
else:
    st.sidebar.success(f"Bulundu: {GLB_NAME} - {os.path.getsize(GLB_NAME)/1e6:.1f} MB")

# BU KOD BASE64 KULLANMIYOR - DIREKT URL'DEN YUKLUYOR, SIYAH EKRAN FIX
html = f"""
<!DOCTYPE html>
<html>
<head>
<script type="importmap">
{{"imports":{{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}}}
</script>
<style>body{{margin:0;background:#111}} #c{{width:100%;height:750px;display:block}} #log{{position:absolute;top:10px;left:10px;color:#0f0;font-family:monospace;background:rgba(0,0,0,.7);padding:6px;border-radius:4px}}</style>
</head>
<body>
<div id="log">Yukleniyor... {GLB_NAME}</div>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {{OrbitControls}} from 'three/addons/controls/OrbitControls.js';
import {{GLTFLoader}} from 'three/addons/loaders/GLTFLoader.js';
import {{DRACOLoader}} from 'three/addons/loaders/DRACOLoader.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111111);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth/750, 0.1, 1000);
camera.position.set(0,0.5,2);

const renderer = new THREE.WebGLRenderer({{canvas:document.getElementById('c'), antialias:true}});
renderer.setSize(window.innerWidth, 750);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setPixelRatio(window.devicePixelRatio);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.6;

// ISIKLAR - SİYAH EKRANI COZER
scene.add(new THREE.AmbientLight(0xffffff, 1.5));
const d1 = new THREE.DirectionalLight(0xffffff, 2); d1.position.set(5,10,5); scene.add(d1);
const d2 = new THREE.DirectionalLight(0xffffff, 1); d2.position.set(-5,5,-5); scene.add(d2);

const loader = new GLTFLoader();
// Draco destekli GLB'ler icin decoder ekle
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
loader.setDRACOLoader(dracoLoader);

const log = document.getElementById('log');

loader.load('./app/static/{GLB_NAME}', (gltf) => {{
    log.textContent = 'Model yuklendi!';
    log.style.color = '#0f0';
    let model = gltf.scene;
    
    // MODELI ORTALA VE OLCEKLE - SIYAH EKRANIN ASIL COZUMU
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    model.position.sub(center);
    const size = box.getSize(new THREE.Vector3()).length();
    const scale = 2.0 / size;
    model.scale.setScalar(scale);

    model.traverse(o=>{{
        if(o.isMesh){{
            // Acik gri gercekci renk, tabla yok
            o.material = new THREE.MeshStandardMaterial({{
                color: 0xd1d5db,
                roughness: 0.5,
                metalness: 0.2
            }});
        }}
    }});

    scene.add(model);
    // Kamerayi modele odakla
    const newBox = new THREE.Box3().setFromObject(model);
    const newCenter = newBox.getCenter(new THREE.Vector3());
    controls.target.copy(newCenter);
    camera.lookAt(newCenter);
}}, 
(progress) => {{
    log.textContent = 'Yukleniyor %' + Math.round(progress.loaded/progress.total*100);
}},
(err) => {{
    log.textContent = 'HATA: ' + err.message + ' - Dosya static klasorunde olmayabilir';
    log.style.color = 'red';
    console.error(err);
    // Fallback: root'dan dene
    loader.load('{GLB_NAME}', (gltf)=>{{ log.textContent='Fallback ile yuklendi!'; scene.add(gltf.scene); }}, null, (e)=>{{ log.textContent='Root da da bulunamadi: '+e.message; }});
});

function animate(){{ requestAnimationFrame(animate); controls.update(); renderer.render(scene,camera); }}
animate();
</script>
</body>
</html>
"""

components.html(html, height=760)

st.caption("Eğer hala siyah ise: 1) GitHub'da GLB'nin yanında static klasörü oluşturup içine de kopyala, 2) Dosya adında Türkçe karakter/boşluk varsa düzelt: car-engine.glb yap")
