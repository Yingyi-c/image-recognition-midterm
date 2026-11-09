from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT = 'C1131151139_陳瀅屹_期中專題報告.docx'
def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), fill); tcPr.append(shd)
def set_text(cell, text, bold=False, color=None):
    cell.text=''; r=cell.paragraphs[0].add_run(text); r.bold=bold; r.font.name='Microsoft JhengHei'; r._element.rPr.rFonts.set(qn('w:eastAsia'),'Microsoft JhengHei')
    if color: r.font.color.rgb=RGBColor(*color)
doc=Document(); sec=doc.sections[0]
sec.top_margin=Inches(.75); sec.bottom_margin=Inches(.7); sec.left_margin=Inches(.85); sec.right_margin=Inches(.85)
for name,size,color in [('Normal',10.5,(0,0,0)),('Title',24,(31,78,121)),('Heading 1',17,(31,78,121)),('Heading 2',13,(55,55,55))]:
    s=doc.styles[name]; s.font.name='Microsoft JhengHei'; s._element.rPr.rFonts.set(qn('w:eastAsia'),'Microsoft JhengHei'); s.font.size=Pt(size); s.font.color.rgb=RGBColor(*color)
p=doc.add_paragraph(style='Title'); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run('基於 AI 輔助之互動式影像處理與人臉分析工具')
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run('期中專題報告').bold=True
for line in ['學號：C1131151139','姓名：陳瀅屹','課程：影像辨識','日期：2026 年 11 月']:
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run(line)
doc.add_page_break()
def heading(text, level=1): doc.add_heading(text, level=level)
def para(text): doc.add_paragraph(text)
heading('摘要'); para('本專題以 Python、Streamlit 與 OpenCV 開發互動式影像處理工具。系統支援常見影像格式載入、影像中繼資訊顯示、RGB/YUV 色彩空間切換、同步直方圖分析、自訂卷積核濾波、PSNR 品質評估，以及 Haar-Cascade 人臉偵測。')
heading('Chapter 1 專案概述與環境建置'); heading('1.1 專案目標',2); para('將影像處理核心演算法整合至直覺的 Web GUI，讓使用者能以可視化方式比較色彩通道、像素分布與濾波結果，並以 PSNR 進行客觀評估。')
heading('1.2 開發環境與相依套件',2)
t=doc.add_table(rows=1,cols=3); t.style='Table Grid'
for c,x in zip(t.rows[0].cells,['套件','版本要求','用途']): shade(c,'1F4E79'); set_text(c,x,True,(255,255,255))
for row in [('Python','3.9 以上','主要開發語言'),('streamlit','>=1.35','互動式 Web GUI'),('opencv-python-headless','>=4.8','色彩轉換、卷積、人臉偵測'),('numpy','>=1.24','矩陣與數值運算'),('Pillow','>=10.0','影像讀取與格式轉換')]:
    cells=t.add_row().cells
    for c,x in zip(cells,row): set_text(c,x)
para('安裝與執行：python -m pip install -r requirements.txt；streamlit run app.py。')
heading('Chapter 2 可執行連結'); para('以下連結請於完成 GitHub 與雲端部署後替換：'); para('Live Demo（Streamlit Cloud / Hugging Face Spaces）：【待補公開連結】'); para('Source Code（GitHub / GitLab）：【待補儲存庫連結】')
heading('Chapter 3 程式功能與操作說明'); heading('3.1 系統資料流',2); para('影像上傳 → Pillow 讀取並轉換為 RGB 陣列 → 色彩空間與直方圖分析／卷積濾波與 PSNR／人臉偵測 → Streamlit 即時呈現結果。')
for h,txt in [('3.2 功能一：影像載入與基本解析','支援 PNG、JPG/JPEG、BMP。上傳後顯示檔名、解析度、色彩維度、檔案大小與原始影像。'),('3.3 功能二：色彩空間與直方圖','Original、RGB channels 與 YUV channels 可切換。直方圖橫軸為 0 至 255 像素強度，縱軸為像素數量，切換模式時同步更新。'),('3.4 功能三：自訂卷積核與 PSNR','使用者可輸入奇數邊長方陣，選擇正規化，並排比較濾波前後影像。PSNR = 10 log10(255² / MSE) dB；MSE = (1/N) Σ(I − K)²。MSE 為 0 時 PSNR 為無限大。'),('3.5 功能四：人臉偵測','使用 OpenCV Haar-Cascade 偵測人臉，以邊界框標示並顯示總數與座標。scaleFactor 與 minNeighbors 可調整偵測敏感度。')]:
    heading(h,2); para(txt)
heading('3.6 測試案例',2)
t=doc.add_table(rows=1,cols=4); t.style='Table Grid'
for c,x in zip(t.rows[0].cells,['案例','輸入','預期結果','實測紀錄']): shade(c,'1F4E79'); set_text(c,x,True,(255,255,255))
for row in [('T1','PNG/JPG/BMP','成功讀取並顯示資訊','請補上截圖與結果'),('T2','RGB/YUV 切換','通道圖與直方圖同步更新','請補上截圖與結果'),('T3','偶數或非方陣核','顯示輸入錯誤','請補上截圖與結果'),('T4','多人臉照片','框出多張人臉並顯示數量','請補上截圖與結果'),('T5','全黑或低對比影像','程式不崩潰，PSNR 正常','請補上截圖與結果')]:
    cells=t.add_row().cells
    for c,x in zip(cells,row): set_text(c,x)
heading('Chapter 4 AI 協作與完整 Prompt 歷程'); para('本專題使用生成式 AI 作為程式規劃、除錯與文件整理的協作工具。以下紀錄可依實際對話補充模型版本、日期與截圖。')
for h,txt in [('Prompt 1','請規劃符合影像辨識期中題目要求的 Streamlit 應用程式。產出系統架構與功能清單。'),('Prompt 2','請加入 RGB/YUV 色彩轉換與同步直方圖。產出通道轉換與直方圖繪製程式。'),('Prompt 3','請加入自訂卷積核、正規化與 PSNR。產出濾波與品質評估模組。'),('Refinement','請檢查非方陣、偶數方陣與除以零情況。加入輸入驗證。')]: heading(h,2); para(txt+'（請補上實際模型名稱與對話截圖。）')
heading('結論'); para('本系統將影像讀取、色彩分析、空間域濾波、PSNR 與人臉偵測整合於單一互動介面。後續可加入更多測試影像與雲端部署，以提升驗收完整度。')
footer=sec.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.CENTER; footer.add_run('C1131151139  陳瀅屹  |  影像辨識期中專題')
doc.save(OUT); print(OUT)
