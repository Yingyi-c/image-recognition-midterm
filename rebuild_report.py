from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT = 'C1131151139_陳瀅屹_期中專題報告.docx'

def font_style(style, size, color=(0, 0, 0)):
    style.font.name = 'Microsoft JhengHei'
    style._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft JhengHei')
    style.font.size = Pt(size)
    style.font.color.rgb = RGBColor(*color)

def shade(cell, color):
    tcpr = cell._tc.get_or_add_tcPr(); shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), color); tcpr.append(shd)

def cell_text(cell, text, bold=False, color=None):
    cell.text = ''; run = cell.paragraphs[0].add_run(text); run.bold = bold
    run.font.name = 'Microsoft JhengHei'; run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft JhengHei')
    if color: run.font.color.rgb = RGBColor(*color)

doc = Document(); sec = doc.sections[0]
sec.top_margin = Inches(.7); sec.bottom_margin = Inches(.7); sec.left_margin = Inches(.8); sec.right_margin = Inches(.8)
font_style(doc.styles['Normal'], 10.5)
font_style(doc.styles['Title'], 24, (31, 78, 121)); font_style(doc.styles['Heading 1'], 17, (31, 78, 121)); font_style(doc.styles['Heading 2'], 13, (55, 55, 55))

p = doc.add_paragraph(style='Title'); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run('基於 AI 輔助之互動式影像處理與人臉分析工具')
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run('期中專題報告').bold = True
for line in ['學號：C1131151139', '姓名：陳瀅屹', '課程：影像辨識', '報告版本：依目前模組化實作狀態重建']:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run(line)
doc.add_page_break()

doc.add_heading('報告摘要', 1)
doc.add_paragraph('本專題以 Python、Streamlit、NumPy、Pillow 與 OpenCV 建立互動式影像處理與人臉分析工具。系統目前已完成影像載入與中繼資訊、RGB/YUV 色彩空間轉換、R/G/B 與 Y/U/V 分量獨立檢視、同步直方圖、自訂卷積核、PSNR 評估及 Haar-Cascade 人臉偵測。程式採模組化設計，並加入卷積核與影像處理的例外處理，方便後續維護與測試。')

doc.add_heading('Chapter 1 專案概述與環境建置', 1)
doc.add_heading('1.1 專案目標與範圍', 2)
doc.add_paragraph('本專案的目標是將影像辨識課程中的色彩空間、直方圖、空間域卷積、PSNR 與人臉偵測概念整合為單一瀏覽器介面。使用者不需撰寫程式，即可上傳影像、切換通道、輸入卷積核並觀察處理結果。')
doc.add_heading('1.2 開發語言與環境', 2)
doc.add_paragraph('開發語言：Python 3.9 以上。建議使用 Python 3.11 或 3.12 建立虛擬環境，以避免部分 Python 3.14 套件原生 DLL 與 Windows 應用程式控制原則的相容性問題。介面框架為 Streamlit。')
doc.add_heading('1.3 requirements.txt 套件說明', 2)
t = doc.add_table(rows=1, cols=3); t.style = 'Table Grid'
for c, x in zip(t.rows[0].cells, ['套件條目', '用途', '目前使用位置']): shade(c, '1F4E79'); cell_text(c, x, True, (255,255,255))
rows = [
    ('streamlit>=1.35', '建立互動式 Web 介面', 'app.py'),
    ('opencv-python-headless>=4.8,<5', '卷積、人臉偵測與影像處理', 'filtering、face_detection'),
    ('numpy>=1.24', '矩陣、色彩轉換、直方圖與 PSNR', 'common、color_analysis、metrics'),
    ('Pillow>=10.0', '影像讀取與直方圖繪圖', 'image_io、app.py'),
    ('pytest>=8.0', '模組單元測試', 'tests/')]
for row in rows:
    cells = t.add_row().cells
    for c, x in zip(cells, row): cell_text(c, x)
doc.add_heading('1.4 安裝與啟動', 2)
doc.add_paragraph('PowerShell 若封鎖 Activate.ps1，可不啟用環境，直接使用虛擬環境 Python：')
doc.add_paragraph(r'.\.venv\Scripts\python.exe -m pip install -r requirements.txt\n.\.venv\Scripts\python.exe -m pytest -q\n.\.venv\Scripts\python.exe -m streamlit run app.py', style='Intense Quote')

doc.add_heading('Chapter 2 可執行連結', 1)
doc.add_paragraph('本章連結必須在部署完成後，以瀏覽器無痕模式確認可公開開啟，再填入正式網址。目前未提供實際 Public 網址，因此以下欄位保留給作者補填。')
for label in ['Live Demo：［待補 Streamlit Cloud／Hugging Face Spaces 公開連結］', 'Source Code：［待補 GitHub／GitLab 完整儲存庫連結］']:
    doc.add_paragraph(label, style='List Bullet')
doc.add_paragraph('部署驗收清單：確認連結不需登入、Repository 可查看完整原始碼、requirements.txt 位於根目錄、啟動指令與 README 說明一致。')

doc.add_heading('Chapter 3 程式功能與操作說明書', 1)
doc.add_heading('3.1 模組架構', 2)
doc.add_paragraph('系統採「核心模組獨立、app.py 負責整合」的架構。')
for label in ['common：共用資料結構、影像轉換與驗證。', 'modules/image_io：影像讀取與 ImageMetadata。', 'modules/color_analysis：RGB/YUV 轉換、分量檢視與直方圖。', 'modules/filtering：卷積核解析、驗證、正規化與濾波。', 'modules/metrics：MSE 與 PSNR。', 'modules/face_detection：Haar-Cascade 與邊界框。', 'tests：卷積核、PSNR、RGB 直方圖測試。']:
    doc.add_paragraph(label, style='List Bullet')
doc.add_paragraph('資料流：上傳影像 → image_io 轉換為 RGB 陣列 → 分流至 color_analysis、filtering/metrics、face_detection → ui 元件顯示結果。')
doc.add_paragraph('［此處插入：模組架構圖與資料流圖］')

doc.add_heading('3.2 功能一：影像載入與基本解析', 2)
doc.add_paragraph('操作：上傳 PNG、JPG/JPEG 或 BMP。系統顯示檔名、寬度、高度、色彩通道數、檔案大小與原始影像。讀取錯誤會顯示錯誤類型，不會直接中止介面。')
doc.add_paragraph('［此處插入：功能一操作截圖］')

doc.add_heading('3.3 功能二：RGB/YUV 色彩空間與同步直方圖', 2)
doc.add_paragraph('操作：在「色彩與直方圖」頁面先選擇 Original、RGB channels 或 YUV channels，再以「選擇獨立分量」切換通道。RGB 可獨立檢視 R、G、B；YUV 可獨立檢視 Y 亮度、U 色度、V 色度。畫面會同時顯示轉換結果、選定分量影像與該分量的 0 至 255 直方圖。')
doc.add_paragraph('目前直方圖以 NumPy 計算，使用 Pillow 直接繪製，避免 Streamlit dataframe/chart 觸發 Pandas 原生 DLL。')
doc.add_paragraph('［此處插入：RGB R/G/B 截圖］\n［此處插入：YUV Y/U/V 截圖］')

doc.add_heading('3.4 功能三：自訂卷積核與 PSNR', 2)
doc.add_paragraph('操作：在側欄每列輸入逗號分隔的數值，例如 0,-1,0／-1,5,-1／0,-1,0，並選擇是否正規化。系統比較濾波前後影像並顯示 PSNR。')
doc.add_paragraph('輸入防呆涵蓋空白、非數字、空白欄位、列長不一致、非方陣、偶數邊長與非有限數值，錯誤時顯示具體列號與修正提示。')
doc.add_paragraph('PSNR 公式：MSE = (1/N) Σ(I - K)^2；PSNR = 10 log10(255^2 / MSE) dB。其中 I 為原圖、K 為濾波影像、N 為像素與通道總數。MSE=0 時，PSNR 定義為無限大。PSNR 越高表示濾波結果與原圖的數值差異越小，但實際銳化或平滑效果仍須搭配影像觀察。')
doc.add_paragraph('［此處插入：卷積核輸入、濾波前後與 PSNR 截圖］')

doc.add_heading('3.5 功能四：人臉偵測', 2)
doc.add_paragraph('操作：進入「人臉偵測」頁面，調整 scaleFactor 與 minNeighbors。系統使用 OpenCV Haar-Cascade 標記人臉邊界框，顯示人臉數量與座標。此模組只進行位置偵測，不辨識身分。若 OpenCV DLL 或 CascadeClassifier 不可用，頁面會顯示明確錯誤訊息。')
doc.add_paragraph('［此處插入：單人與多人臉測試截圖］')

doc.add_heading('3.6 測試案例與邊界條件', 2)
t = doc.add_table(rows=1, cols=4); t.style = 'Table Grid'
for c, x in zip(t.rows[0].cells, ['編號', '測試輸入', '預期結果', '目前結果']): shade(c, '1F4E79'); cell_text(c, x, True, (255,255,255))
tests = [('T1','PNG、JPG、BMP','成功讀取並顯示資訊','待以截圖補強'),('T2','RGB R/G/B 切換','分量圖與直方圖同步更新','已完成'),('T3','YUV Y/U/V 切換','亮度與色度分量正常顯示','已完成'),('T4','adf、空白、偶數核','顯示對應防呆訊息','已完成'),('T5','Identity 卷積核','MSE=0、PSNR=∞','已通過測試'),('T6','多人臉影像','框出多張人臉並列出數量','待實機截圖'),('T7','OpenCV 5 或 DLL 被封鎖','顯示模組錯誤而非整頁崩潰','已加入例外處理')]
for row in tests:
    cells=t.add_row().cells
    for c,x in zip(cells,row): cell_text(c,x)
doc.add_paragraph('目前自動化測試結果：python -m pytest -q → 3 passed。')

doc.add_heading('Chapter 4 AI 協作與完整 Prompt 歷程', 1)
doc.add_paragraph('模型版本：本報告應以實際使用介面顯示的模型名稱與版本為準。請將下方「待補」欄位替換為完整模型識別資訊與對話截圖。')
audit = [
('階段一：需求拆解', '原始 Prompt：請依題目規格規劃影像處理、人臉偵測、報告與部署功能。', 'AI 產出：列出四大核心功能、Streamlit 介面與報告章節。', 'Refinement：要求改為模組化，一個功能一個資料夾，先測試再整合。'),
('階段二：模組化實作', '原始 Prompt：請建立 image_io、color_analysis、filtering、metrics、face_detection 與 tests。', 'AI 產出：建立 service、parser、detector、metrics 與測試檔案。', 'Refinement：修正 filtering service 的公開函式名稱，讓 app 與測試一致。'),
('階段三：色彩與直方圖', '原始 Prompt：顯示 RGB 各分量與 YUV 的 Y/U/V 分量及直方圖。', 'AI 產出：新增分量選擇、RGB 彩色預覽、YUV 分量預覽與直方圖。', 'Refinement：因 Pandas DLL 錯誤，改用 NumPy 計算與 Pillow 繪圖。'),
('階段四：環境除錯', '原始 Prompt：處理 ccalendar DLL、CascadeClassifier 不存在與 PowerShell 執行政策錯誤。', 'AI 產出：加入例外處理、OpenCV 版本限制、直接使用 venv Python 的啟動方式。', 'Refinement：將錯誤訊息改為使用者可理解的修復提示。'),
('階段五：卷積核防呆', '原始 Prompt：輸入 adf 時不要顯示原始 Python 例外，請做輸入防呆。', 'AI 產出：加入空白、非數字、非方陣、偶數邊長與欄位錯誤檢查。', 'Refinement：顯示錯誤列號、錯誤原因與正確格式範例。')]
for title, prompt, result, refine in audit:
    doc.add_heading(title, 2); doc.add_paragraph(prompt); doc.add_paragraph(result); doc.add_paragraph(refine)
doc.add_paragraph('［此處插入：完整 AI 對話紀錄、模型版本、日期與程式修正前後截圖］')

doc.add_heading('結論與後續工作', 1)
doc.add_paragraph('目前已完成可執行的模組化原型與三項自動化測試。提交前仍需補齊實際 Public Demo、GitHub 連結、各功能操作截圖、多人臉測試影像與 AI 對話原始紀錄。完成上述項目後，即可依題目要求輸出正式 PDF。')
footer = sec.footer.paragraphs[0]; footer.alignment = WD_ALIGN_PARAGRAPH.CENTER; footer.add_run('C1131151139  陳瀅屹  |  影像辨識期中專題')
doc.save(OUT); print(OUT)
