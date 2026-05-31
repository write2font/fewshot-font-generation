import json

# DM-Font가 사용하는 설계도 파일 열기
with open("data/kor/decomposition_DM.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("\n[ 67번 부품이 포함된 글자들 ]")
count = 0
for char, components in data.items():
    if 32 in components:
        print(char, end=" ")
        count += 1
        if count >= 20: # 너무 많으면 20개까지만 출력
            break
print("\n")