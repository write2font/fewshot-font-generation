import os
import math
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from PIL import Image

# 1. 한글 폰트 설정 (윈도우 matplotlib 깨짐 방지용)
try:
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
except:
    pass

# 2. 레퍼런스 문자열 처리 (중복 제거 및 가나다순 정렬)
raw_string = "\uac12\uac19\uacec\uacf6\uae4e\ub10b\ub2aa\ub2eb\ub2ed\ub2fb\ub429\ub5cc\ub7b5\uba83\ubc1f\ubcd8\ube90\ubf48\uc1a9\uc410\uc549\uc54a\uc598\uc5be\uc5cc\uc633\uc74a\uc8e1\ucb9c\ucdb0\uce04\ud02d\ud2d4\ud540\ud565\ub2eb\ub2ed\ud565\ub158\uc88b\uc6b0"
chars = sorted(list(set(raw_string)))
print(f"총 분석 글자 수: {len(chars)}자")

# 3. 폴더 경로 설정 (본인 환경에 맞게 수정하세요)
orig_dir = "write2font/png/OwnglyphGeumhyang"             # 원본 손글씨 이미지가 있는 폴더
gen_dir = "result/OwnglyphGeumhyang"       # 모델이 생성한 이미지가 있는 폴더
output_path = "font_comparison_result.png"    # 최종 저장될 이미지 파일명

# 파일 이름 규칙 대응 ('가.png' 형태와 'ac00.png' 유니코드 헥스 형태 모두 확인)
def get_img_path(base_dir, char):
    char_path = os.path.join(base_dir, f"{char}.png")
    hex_path = os.path.join(base_dir, f"{hex(ord(char))[2:]}.png")
    
    if os.path.exists(char_path):
        return char_path
    elif os.path.exists(hex_path):
        return hex_path
    return None

# 4. 시각화 그리드 설정 (예: 1줄에 8글자씩 배치)
cols = 8
rows = math.ceil(len(chars) / cols)

# 원본(위)과 생성(아래)을 짝지어 보여주기 위해 행을 두 배로 늘림
fig, axes = plt.subplots(rows * 2, cols, figsize=(cols * 2.5, rows * 4))
plt.subplots_adjust(wspace=0.1, hspace=0.6)

# 5. 이미지 렌더링 루프
for idx, char in enumerate(chars):
    r = (idx // cols) * 2  # 원본 이미지가 들어갈 짝수 행 인덱스
    c = idx % cols
    
    orig_img_path = get_img_path(orig_dir, char)
    gen_img_path = get_img_path(gen_dir, char)
    
    # 상단: 원본 이미지 플롯
    ax_orig = axes[r, c]
    if orig_img_path:
        img_orig = Image.open(orig_img_path).convert('RGB')
        ax_orig.imshow(img_orig)
    else:
        ax_orig.text(0.5, 0.5, '이미지 없음', ha='center', va='center', color='red')
    ax_orig.set_title(f"원본: {char}", fontsize=12, fontweight='bold')
    ax_orig.axis('off')
    
    # 하단: 생성 이미지 플롯
    ax_gen = axes[r+1, c]
    if gen_img_path:
        img_gen = Image.open(gen_img_path).convert('RGB')
        ax_gen.imshow(img_gen)
    else:
        ax_gen.text(0.5, 0.5, '생성 실패', ha='center', va='center', color='gray')
    ax_gen.set_title("생성결과", fontsize=11, color='blue')
    ax_gen.axis('off')

# 글자가 들어가지 않은 남는 빈칸 축(Axis) 숨기기
for idx in range(len(chars), rows * cols):
    r = (idx // cols) * 2
    c = idx % cols
    axes[r, c].axis('off')
    axes[r+1, c].axis('off')

# 최종 이미지 저장 및 출력
plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ 비교 이미지가 성공적으로 저장되었습니다: {output_path}")

# 화면에 즉시 띄워서 확인하고 싶다면 아래 주석을 해제하세요
# plt.show()