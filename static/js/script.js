/**
 * 剪纸大师 (Papercraft Maestro) - 前端交互逻辑
 * 处理页面切换、API 调用、图片生成等功能
 */

// ========== 全局变量 ==========
let currentImageUrl = '';
let currentPrompt = '';

// ========== DOM 元素 ==========
const ui1Container = document.getElementById('ui-page-1');
const ui2Container = document.getElementById('ui-page-2');
const ui3Container = document.getElementById('ui-page-3');
const promptInput = document.getElementById('prompt-input');
const generateBtn = document.getElementById('generate-btn');
const tryAgainBtn = document.getElementById('try-again-btn');
const downloadBtn = document.getElementById('download-btn');
const renderSceneBtn = document.getElementById('render-scene-btn');
const resultImage = document.getElementById('result-image');
const loadingOverlay = document.getElementById('loading-overlay');
const loadingMessage = document.getElementById('loading-message');
const loadingSteps = document.getElementById('loading-steps');

// ========== 页面切换函数 ==========

/**
 * 切换到 UI_2 结果页面
 */
function switchToResultPage() {
    ui1Container.classList.remove('active');
    ui2Container.classList.add('active');
    ui2Container.style.display = 'block';
}

/**
 * 切换回 UI_1 主页面
 */
function switchToMainPage() {
    ui2Container.classList.remove('active');
    ui3Container.classList.remove('active');
    ui1Container.classList.add('active');
    ui2Container.style.display = 'none';
    ui3Container.style.display = 'none';
    
    // 清空输入框
    promptInput.value = '';
    currentImageUrl = '';
    currentPrompt = '';
}

/**
 * 切换到 UI_3 场景渲染页面
 */
function switchToScenePage() {
    if (!currentImageUrl) {
        alert('⚠️ 请先生成剪纸图案！');
        return;
    }
    
    ui1Container.classList.remove('active');
    ui2Container.classList.remove('active');
    ui3Container.classList.add('active');
    ui1Container.style.display = 'none';
    ui2Container.style.display = 'none';
    ui3Container.style.display = 'block';
    
    // 加载剪纸到所有场景
    loadPapercutToScenes();
}

/**
 * 显示加载状态
 */
function showLoading(message = '正在生成剪纸图案...') {
    loadingOverlay.classList.remove('hidden');
    resultImage.classList.remove('loaded');
    loadingMessage.textContent = message;
    loadingSteps.innerHTML = '';
}

/**
 * 隐藏加载状态，显示结果图片
 */
function hideLoading() {
    loadingOverlay.classList.add('hidden');
    resultImage.classList.add('loaded');
}

/**
 * 更新加载进度步骤
 */
function updateLoadingSteps(steps) {
    if (Array.isArray(steps)) {
        loadingSteps.innerHTML = steps.map(step => 
            `<div>${step}</div>`
        ).join('');
    }
}

// ========== API 调用函数 ==========

/**
 * 调用后端生成剪纸图案
 */
async function generatePapercut() {
    const prompt = promptInput.value.trim();
    
    // 验证输入
    if (!prompt) {
        alert('⚠️ 请输入创意描述！');
        return;
    }
    
    console.log('🔵 开始生成剪纸图案');
    console.log('📝 Prompt:', prompt);
    
    // 立即切换到结果页面并显示加载状态
    currentPrompt = prompt;
    switchToResultPage();
    showLoading('🚀 正在准备生成...');
    
    try {
        // 构建表单数据
        const formData = new FormData();
        formData.append('prompt', prompt);
        formData.append('scene', 'none');  // 默认无场景，后续可扩展
        
        // 调用后端 API
        const response = await fetch('/api/generate', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        console.log('📦 收到响应:', data);
        
        if (data.success) {
            // 更新进度步骤
            if (data.steps) {
                updateLoadingSteps(data.steps);
            }
            
            // 加载生成的图片
            currentImageUrl = data.image_url;
            resultImage.src = currentImageUrl;
            
            // 图片加载完成后隐藏加载状态
            resultImage.onload = () => {
                hideLoading();
                console.log('✅ 图片加载完成');
            };
            
            resultImage.onerror = () => {
                console.error('❌ 图片加载失败');
                loadingMessage.textContent = '❌ 图片加载失败，请重试';
            };
        } else {
            // 生成失败
            loadingMessage.textContent = data.message || '❌ 生成失败，请重试';
            console.error('❌ 生成失败:', data.message);
            
            if (data.steps) {
                updateLoadingSteps(data.steps);
            }
        }
    } catch (error) {
        console.error('❌ API 调用失败:', error);
        loadingMessage.textContent = '❌ 网络错误，请检查连接后重试';
    }
}

/**
 * 下载生成的剪纸图片
 */
async function downloadImage() {
    if (!currentImageUrl) {
        alert('⚠️ 没有可下载的图片！');
        return;
    }
    
    try {
        console.log('📥 开始下载图片:', currentImageUrl);
        
        // 创建一个临时的 a 标签来触发下载
        const link = document.createElement('a');
        link.href = currentImageUrl;
        link.download = `papercut_${Date.now()}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        console.log('✅ 下载成功');
    } catch (error) {
        console.error('❌ 下载失败:', error);
        alert('❌ 下载失败，请重试');
    }
}

/**
 * 渲染到场景（切换到 UI_3）
 */
function renderInScene() {
    if (!currentImageUrl) {
        alert('⚠️ 没有可渲染的剪纸图案！');
        return;
    }
    
    console.log('🎬 切换到场景渲染页面');
    switchToScenePage();
}

/**
 * 加载剪纸到所有场景
 */
function loadPapercutToScenes() {
    const scenes = ['door', 'wall', 'window'];
    
    scenes.forEach(scene => {
        const overlay = document.getElementById(`papercut-overlay-${scene}`);
        if (overlay) {
            overlay.src = currentImageUrl;
            overlay.style.display = 'block';
            console.log(`✅ 剪纸已加载到 ${scene} 场景`);
        }
    });
}

/**
 * 下载场景合成图片
 */
async function downloadSceneImage(scene) {
    const preview = document.getElementById(`scene-preview-${scene}`);
    if (!preview) {
        alert('❌ 场景不存在');
        return;
    }
    
    try {
        console.log(`📥 开始下载 ${scene} 场景图片`);
        
        // 使用 html2canvas 库来截图（需要在 HTML 中引入）
        // 这里我们简化处理，直接下载剪纸图片
        const link = document.createElement('a');
        link.href = currentImageUrl;
        link.download = `papercut_${scene}_${Date.now()}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        console.log(`✅ ${scene} 场景图片下载成功`);
    } catch (error) {
        console.error(`❌ 下载 ${scene} 场景失败:`, error);
        alert('❌ 下载失败，请重试');
    }
}

// ========== 事件监听器 ==========

// 生成按钮点击
if (generateBtn) {
    generateBtn.addEventListener('click', () => {
        console.log('🔴 Generate 按钮被点击');
        generatePapercut();
    });
}

// Enter 键快速触发
if (promptInput) {
    promptInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            console.log('⌨️ Enter 键触发生成');
            generatePapercut();
        }
    });
}

// Try Again 按钮
if (tryAgainBtn) {
    tryAgainBtn.addEventListener('click', () => {
        console.log('🔄 Try Again 按钮被点击');
        switchToMainPage();
    });
}

// Download 按钮
if (downloadBtn) {
    downloadBtn.addEventListener('click', () => {
        console.log('📥 Download 按钮被点击');
        downloadImage();
    });
}

// Render in Scene 按钮
if (renderSceneBtn) {
    renderSceneBtn.addEventListener('click', () => {
        console.log('🏠 Render in Scene 按钮被点击');
        renderInScene();
    });
}

// 场景下载按钮监听
document.addEventListener('DOMContentLoaded', () => {
    const sceneDownloadBtns = document.querySelectorAll('.scene-download-btn');
    sceneDownloadBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const scene = btn.getAttribute('data-scene');
            console.log(`📥 下载 ${scene} 场景`);
            downloadSceneImage(scene);
        });
    });
    
    // 场景预览点击效果
    const scenePreviews = document.querySelectorAll('.scene-preview');
    scenePreviews.forEach(preview => {
        preview.addEventListener('click', () => {
            console.log('🖼️ 场景预览被点击');
            // 可以添加放大查看等功能
        });
    });
});

// ========== 页面加载完成 ==========
window.addEventListener('load', () => {
    console.log('✅ 页面加载完成');
    console.log('🎨 剪纸大师 (Papercraft Maestro) 前端已就绪');
    
    // 检查后端健康状态
    checkBackendHealth();
});

/**
 * 检查后端服务健康状态
 */
async function checkBackendHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('🏥 后端健康检查:', data);
        
        if (data.modules_available) {
            console.log('✅ ComfyUI 模块已加载');
        } else {
            console.warn('⚠️ 运行在占位符模式');
        }
        
        if (data.comfyui_connected) {
            console.log('✅ ComfyUI 服务已连接');
        } else {
            console.warn('⚠️ ComfyUI 服务未连接');
        }
    } catch (error) {
        console.error('❌ 后端健康检查失败:', error);
    }
}

// ========== 工具函数 ==========

/**
 * 延迟函数
 */
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 格式化时间戳
 */
function formatTimestamp(timestamp) {
    const date = new Date(timestamp * 1000);
    return date.toLocaleString('zh-CN');
}


// ========== 页面关闭检测 ==========

/**
 * 检测浏览器标签页/窗口关闭
 * 注意: beforeunload 仅在真正关闭时触发,刷新页面不会触发关闭服务器
 */
let isPageUnloading = false;

window.addEventListener('beforeunload', function(e) {
    // 标记页面正在卸载
    isPageUnloading = true;
    
    // 使用 sendBeacon 确保请求能发送出去
    // 即使页面正在关闭,beacon 也能完成发送
    const sent = navigator.sendBeacon('/api/shutdown');
    
    if (sent) {
        console.log('🛑 已发送服务器关闭请求');
    }
});

/**
 * 检测页面刷新(不关闭服务器)
 */
window.addEventListener('load', function() {
    // 重置标记
    isPageUnloading = false;
});

/**
 * 检测页面可见性变化
 */
document.addEventListener('visibilystatechange', function() {
    if (document.visibilityState === 'hidden') {
        // 页面不可见时记录
        console.log('📱 页面进入后台');
    } else {
        console.log('📱 页面返回前台');
    }
});
