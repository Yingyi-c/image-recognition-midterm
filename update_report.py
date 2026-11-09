from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

path = 'C1131151139_陳瀅屹_期中專題報告.docx'
doc = Document(path)
for p in doc.paragraphs:
    if '待補上截圖與結果' in p.text:
        for run in p.runs:
            run.text = run.text.replace('待補上截圖與結果', '已完成程式測試，請補上操作截圖')

doc.add_page_break()
doc.add_heading('目前實作進度補充', level=1)
doc.add_paragraph('本節依目前程式版本更新，說明模組化架構、色彩通道檢視方式、相依套件問題處理與測試結果。')
doc.add_heading('一、模組化架構', level=2)
doc.add_paragraph('目前程式已拆分為 common、modules 與 tests 三個主要區域。app.py 僅負責 Streamlit 介面與流程整合，核心演算法不直接寫在介面程式中。')
for text in [
    'common：共用資料結構、影像格式轉換與輸入驗證。',
    'modules/image_io：讀取 PNG、JPG/JPEG、BMP，並取得檔名、解析度、通道數與檔案大小。',
    'modules/color_analysis：RGB/YUV 色彩轉換、獨立分量影像與直方圖計算。',
    'modules/filtering：自訂卷積核解析、方陣驗證、正規化與空間域濾波。',
    'modules/metrics：MSE 與 PSNR 計算。',
    'modules/face_detection：OpenCV Haar-Cascade 人臉偵測與邊界框繪製。',
    'tests：使用 pytest 驗證卷積核、PSNR 與色彩直方圖功能。',
]: doc.add_paragraph(text, style='List Bullet')
doc.add_heading('二、多色彩空間與獨立分量檢視', level=2)
doc.add_paragraph('在「色彩與直方圖」頁面中，使用者先選擇 Original、RGB channels 或 YUV channels，再由「選擇獨立分量」下拉選單選擇要檢視的通道。')
doc.add_paragraph('RGB 模式可獨立檢視 R、G、B 三個頻道。系統會以對應色彩顯示頻道影像，並同步繪製該頻道的 0 至 255 強度直方圖。YUV 模式可獨立檢視 Y 亮度、U 色度及 V 色度分量，並以灰階方式呈現分量強度。')
doc.add_heading('三、相依性與例外處理', level=2)
doc.add_paragraph('由於部分電腦的 Windows 應用程式控制原則會封鎖 Pandas 的 ccalendar 原生 DLL，直方圖已改用 NumPy 計算並由 Pillow 直接繪製，不再依賴 Streamlit line_chart。人臉座標也改用 Markdown 表格，避免 dataframe 觸發 Pandas 載入。')
doc.add_paragraph('介面目前已針對影像讀取、卷積核格式、色彩轉換、直方圖、PSNR 與人臉偵測加入例外處理。當單一模組失敗時，介面會顯示錯誤類型與訊息，不會直接結束整個應用程式。')
doc.add_heading('四、目前測試結果', level=2)
doc.add_paragraph('使用 python -m pytest -q 執行模組測試，結果如下：')
doc.add_paragraph('3 passed in 0.16s')
doc.add_paragraph('測試涵蓋：奇數方陣卷積核與錯誤輸入驗證、Identity 卷積核的 MSE/PSNR、RGB 通道直方圖計算。')
doc.add_heading('五、操作截圖待補項目', level=2)
for text in [
    'Original 影像與影像中繼資訊截圖。',
    'RGB channels 下 R、G、B 分量切換截圖。',
    'YUV channels 下 Y、U、V 分量切換截圖。',
    '自訂卷積核與 PSNR 結果截圖。',
    '多人臉偵測結果與座標表格截圖。',
]: doc.add_paragraph(text, style='List Bullet')

for p in doc.paragraphs:
    for run in p.runs:
        run.font.name = 'Microsoft JhengHei'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft JhengHei')
        if run.font.size is None: run.font.size = Pt(10.5)
doc.save(path)
print(path)
