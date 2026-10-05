import streamlit as st
import streamlit.components.v1 as components

# Sayfa ayarları
st.set_page_config(page_title="3D Model Görüntüleyici", layout="centered")

st.title("🚗 3D Araba Motoru Modeli")
st.write("Streamlit ve Python ile yüklenen GLB 3D model görüntüleyici.")

# Three.js kullanan HTML/JavaScript arayüzü
streamlit_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { margin: 0; overflow: hidden; background-color: #1a1a1a; }
        #canvas-container { width: 100%; height: 500px; }
        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-family: Arial, sans-serif;
            font-size: 16px;
            pointer-events: none;
        }
    </style>
</head>
<body>
    <div id="loading">Model Yükleniyor...</div>
    <div id="canvas-container"></div>

    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
            }
        }
    </script>

    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
        import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

        const container = document.getElementById('canvas-container');
        const loadingElement = document.getElementById('loading');

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1a1a1a);

        const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 2, 5);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
        scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 2.5);
        directionalLight.position.set(5, 10, 7);
        scene.add(directionalLight);

        const loader = new GLTFLoader();
        
        // Doğrudan rawusercontent linki:
        loader.load(
            'https://raw.githubusercontent.com/RanaEylul/3dmotor/main/car%20engine%203d%20model.glb',
            function (gltf) {
                scene.add(gltf.scene);
                loadingElement.style.display = 'none';
            },
            function (xhr) {
                const percent = (xhr.loaded / xhr.total * 100).toFixed(0);
                if (!isNaN(percent)) {
                    loadingElement.innerText = `Yükleniyor: %${percent}`;
                }
            },
            function (error) {
                console.error('Hata Detayı:', error);
                loadingElement.innerText = 'Model yüklenemedi! Tarayıcı konsolunu kontrol edin.';
            }
        );

        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });

        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

components.html(streamlit_html, height=520)

st.markdown("---")
st.info("İpucu: Mouse sol tuşu ile modeli döndürebilir, sağ tuş ile kaydırabilir ve tekerlekle yakınlaşabilirsiniz.")
