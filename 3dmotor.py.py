import streamlit as st
import streamlit.components.v1 as components

# Sayfa ayarlarını geniş ekran yapıyoruz
st.set_page_config(
    page_title="3D Araba Motoru Görüntüleyici",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Özel CSS tasarımı
st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        .main-title {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
            color: #00adb5;
            text-align: center;
            margin-bottom: 0px;
            font-size: 2.3rem;
        }
        .sub-title {
            text-align: center;
            color: #a3a3a3;
            margin-bottom: 20px;
            font-size: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🚗 İnteraktif 3D Araba Motoru Simülasyonu</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Model boyutu büyütüldü ve ekrana yakınlaştırıldı.</p>", unsafe_allow_html=True)

# Three.js kullanan HTML/JavaScript arayüzü
streamlit_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            margin: 0; 
            overflow: hidden; 
            background-color: #121212; 
            font-family: Arial, sans-serif;
        }
        #canvas-container { 
            width: 100%; 
            height: 720px; 
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        }
        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #00adb5;
            font-size: 18px;
            font-weight: bold;
            background: rgba(18, 18, 18, 0.9);
            padding: 20px 30px;
            border-radius: 10px;
            border: 1px solid #00adb5;
            pointer-events: none;
            box-shadow: 0 4px 20px rgba(0,173,181,0.2);
            letter-spacing: 1px;
            z-index: 10;
        }
        .control-panel {
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(18, 18, 18, 0.85);
            color: #ffffff;
            padding: 14px 20px;
            border-radius: 8px;
            border-left: 4px solid #00adb5;
            font-size: 13px;
            backdrop-filter: blur(6px);
            line-height: 1.5;
            z-index: 5;
        }
        /* Yakınlaşma / Uzaklaşma Butonları */
        .zoom-buttons {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            z-index: 5;
        }
        .zoom-btn {
            background: rgba(0, 173, 181, 0.8);
            color: white;
            border: none;
            width: 45px;
            height: 45px;
            font-size: 22px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.2s;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .zoom-btn:hover {
            background: rgba(0, 173, 181, 1);
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div id="loading">Model Yükleniyor, Lütfen Bekleyin...</div>
    <div id="canvas-container">
        <!-- Bilgilendirme Paneli -->
        <div class="control-panel">
            🖱️ <b>Sol Tık + Sürükle:</b> Modeli Döndür<br>
            🔍 <b>Fare Tekerleği veya Sağdaki Butonlar:</b> Yakınlaş / Uzaklaş<br>
            ✋ <b>Sağ Tık + Sürükle:</b> Konumu Kaydır
        </div>

        <!-- Ekrana Eklenen Yakınlaştır / Uzaklaştır Butonları -->
        <div class="zoom-buttons">
            <button class="zoom-btn" id="btn-in" title="Yakınlaştır">+</button>
            <button class="zoom-btn" id="btn-out" title="Uzaklaştır">-</button>
        </div>
    </div>

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
        scene.background = new THREE.Color(0x121212);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        
        // Kamera modele çok daha yakın konumlandırıldı
        camera.position.set(0, 1.2, 2.5);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        // Butonlar ile yakınlaştırma / uzaklaştırma mantığı
        document.getElementById('btn-in').addEventListener('click', () => {
            controls.dollyIn(1.2);
            controls.update();
        });

        document.getElementById('btn-out').addEventListener('click', () => {
            controls.dollyOut(1.2);
            controls.update();
        });

        // Işıklandırma
        const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 2.5);
        dirLight.position.set(5, 10, 7);
        scene.add(dirLight);

        const blueLight = new THREE.DirectionalLight(0x00adb5, 1.2);
        blueLight.position.set(-5, -5, -5);
        scene.add(blueLight);

        const loader = new GLTFLoader();
        
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
                console.error('Hata:', error);
                loadingElement.innerText = 'Model yüklenemedi!';
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

components.html(streamlit_html, height=740)
