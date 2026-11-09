import numpy as np
import streamlit as st
from PIL import Image, ImageDraw
from modules.image_io.service import load_image, get_metadata
from modules.color_analysis.service import convert_channels, calculate_histograms
from modules.filtering.service import parse_kernel, apply_custom_kernel
from modules.metrics.service import calculate_psnr
from modules.face_detection.service import detect_faces

st.set_page_config(page_title="互動式影像處理與人臉分析", page_icon="🖼️", layout="wide")

def make_histogram_image(histograms, width=900, height=360):
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    colors = [(220, 60, 60), (60, 150, 70), (60, 90, 210), (120, 80, 160)]
    max_value = max(int(values.max()) for values in histograms.values()) or 1
    left, top, right, bottom = 55, 20, width - 20, height - 45
    draw.line((left, bottom, right, bottom), fill="black", width=2)
    draw.line((left, top, left, bottom), fill="black", width=2)
    for index, (name, values) in enumerate(histograms.items()):
        points = []
        for x in range(256):
            px = left + int(x * (right - left) / 255)
            py = bottom - int(float(values[x]) * (bottom - top) / max_value)
            points.append((px, py))
        draw.line(points, fill=colors[index % len(colors)], width=2)
        draw.text((left + index * 130, height - 32), name, fill=colors[index % len(colors)])
    draw.text((left - 8, bottom + 5), "0", fill="black")
    draw.text((right - 25, bottom + 5), "255", fill="black")
    draw.text((left + 5, top), "Pixel count", fill="black")
    return canvas

def channel_preview(channel, name):
    channel = np.asarray(channel, dtype=np.uint8)
    if name == "R":
        return np.stack([channel, np.zeros_like(channel), np.zeros_like(channel)], axis=2)
    if name == "G":
        return np.stack([np.zeros_like(channel), channel, np.zeros_like(channel)], axis=2)
    if name == "B":
        return np.stack([np.zeros_like(channel), np.zeros_like(channel), channel], axis=2)
    return channel
st.title("🖼️ 互動式影像處理與人臉分析工具")
st.caption("模組化版本：影像讀取、色彩分析、卷積濾波、品質評估與人臉偵測彼此獨立。")
uploaded = st.file_uploader("上傳影像", type=["png", "jpg", "jpeg", "bmp"])
if uploaded is None:
    st.info("請上傳影像後開始分析。")
    st.stop()

try:
    original = load_image(uploaded)
except Exception as exc:
    st.error(f"影像讀取失敗：{type(exc).__name__}: {exc}")
    st.stop()
with st.sidebar:
    view = st.radio("色彩空間 / 通道", ["Original", "RGB channels", "YUV channels"])
    kernel_text = st.text_area("自訂卷積核（每列以逗號分隔）", "0,-1,0\n-1,5,-1\n0,-1,0")
    normalize = st.checkbox("正規化卷積核", value=False)
    scale = st.slider("人臉 scaleFactor", 1.05, 1.50, 1.10, 0.05)
    neighbors = st.slider("人臉 minNeighbors", 1, 10, 5)

try:
    kernel = parse_kernel(kernel_text)
    filtered = apply_custom_kernel(original, kernel, normalize)
    kernel_error = None
except Exception as exc:
    kernel = np.eye(3, dtype=np.float32)
    filtered = original.copy()
    kernel_error = str(exc)

tab1, tab2, tab3, tab4 = st.tabs(["影像資訊", "色彩與直方圖", "卷積濾波與 PSNR", "人臉偵測"])
with tab1:
    meta = get_metadata(uploaded.name, uploaded.size, original)
    try:
        st.markdown(
            f"**檔名：** {meta.filename}  \n"
            f"**解析度：** {meta.width} × {meta.height}  \n"
            f"**色彩維度：** {meta.channels} channels  \n"
            f"**檔案大小：** {meta.file_size:,} bytes"
        )
    except Exception as exc:
        st.error(f"影像資訊顯示失敗：{type(exc).__name__}: {exc}")
    st.image(original, caption="Original", use_container_width=True)
with tab2:
    try:
        shown, channels = convert_channels(original, view)
        selected_channel = st.selectbox("選擇獨立分量", list(channels.keys()))
        selected_image = channel_preview(channels[selected_channel], selected_channel)
        left, right = st.columns(2)
        left.image(shown, caption=f"{view} 轉換結果", use_container_width=True)
        right.image(selected_image, caption=f"{selected_channel} 分量獨立檢視", use_container_width=True)
        hist = calculate_histograms(channels)
        selected_hist = {selected_channel: hist[selected_channel]}
        st.image(make_histogram_image(selected_hist), caption=f"{selected_channel} 分量直方圖：橫軸 0-255，縱軸為像素數量")
        st.caption("RGB 可切換 R/G/B；YUV 可切換 Y（亮度）、U（色度）、V（色度）。")
    except Exception as exc:
        st.warning(f"色彩或直方圖處理失敗：{type(exc).__name__}: {exc}")
        st.info("影像與通道分析仍可正常使用；請檢查 Python 與 OpenCV 安裝環境。")
with tab3:
    if kernel_error:
        st.error(f"卷積核輸入錯誤：{kernel_error}")
        st.caption("格式範例：0,-1,0  下一列輸入 -1,5,-1  再下一列輸入 0,-1,0")
    left, right = st.columns(2)
    left.image(original, caption="濾波前", use_container_width=True)
    right.image(filtered, caption="濾波後", use_container_width=True)
    value = calculate_psnr(original, filtered)
    st.markdown(f"**PSNR：** {'∞ dB' if np.isinf(value) else f'{value:.2f} dB'}")
    st.code(np.array2string(kernel, precision=3), language="text")
with tab4:
    try:
        result = detect_faces(original, scale, neighbors)
        st.image(result.image, caption=f"偵測到 {result.count} 張人臉", use_container_width=True)
        st.markdown(f"**人臉數量：** {result.count}")
        if result.boxes:
            st.markdown("| 編號 | X | Y | 寬 | 高 |\n|---:|---:|---:|---:|---:|\n" + "\n".join(f"| {i} | {x} | {y} | {w} | {h} |" for i, (x, y, w, h) in enumerate(result.boxes, 1)))
    except Exception as exc:
        st.error(f"人臉偵測失敗：{type(exc).__name__}: {exc}")
