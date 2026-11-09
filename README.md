# 基於 AI 輔助之互動式影像處理與人臉分析工具

## 功能

- 上傳 JPG、PNG、BMP、WEBP 圖片
- 影像資訊：解析度、色彩維度、檔案大小
- Original、RGB 與 YUV 色彩空間/通道檢視
- 同步顯示 0-255 強度直方圖
- 任意奇數邊長方形卷積核、正規化與邊界反射處理
- 濾波前後並排比較與 PSNR（dB）量化
- OpenCV Haar Cascade 人臉位置偵測與座標表格

## 執行方式

在本資料夾開啟終端機後執行：

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

接著使用瀏覽器開啟 Streamlit 顯示的網址，通常是 `http://localhost:8501`。

## PSNR 公式

令原圖為 `I`、濾波結果為 `K`，影像共有 `N` 個像素（含所有色彩通道）：

`MSE = (1/N) * Σ(I - K)^2`

`PSNR = 10 * log10(255^2 / MSE) dB`

當 `MSE = 0` 時，PSNR 定義為無限大。

## AI 協作說明

本專題使用生成式 AI 作為程式設計協作夥伴，協助規劃 GUI 功能、OpenCV 影像處理流程、錯誤排除與使用說明撰寫；實際程式由開發者測試、理解並整合。

## 限制與倫理

本系統只偵測人臉所在位置，不進行身分辨識、年齡、性別或情緒推論。人臉偵測效果會受到光線、角度、遮擋與圖片解析度影響。
