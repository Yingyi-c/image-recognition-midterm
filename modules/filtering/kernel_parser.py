import numpy as np
from common.validators import validate_kernel

def parse_kernel(text: str) -> np.ndarray:
    if not text or not text.strip():
        raise ValueError("卷積核不可為空白，請輸入例如 0,-1,0\\n-1,5,-1\\n0,-1,0")
    raw_rows = [line.strip() for line in text.strip().splitlines() if line.strip()]
    rows = []
    for row_index, line in enumerate(raw_rows, start=1):
        values = [value.strip() for value in line.split(",")]
        if any(value == "" for value in values):
            raise ValueError(f"第 {row_index} 列包含空白欄位，請使用逗號分隔數字")
        try:
            rows.append([float(value) for value in values])
        except ValueError:
            raise ValueError(f"第 {row_index} 列含有非數字內容，請只輸入數字與小數點") from None
    if any(len(row) != len(rows) for row in rows):
        raise ValueError("卷積核必須是每列長度相同的方陣")
    return validate_kernel(np.array(rows, dtype=np.float32))
