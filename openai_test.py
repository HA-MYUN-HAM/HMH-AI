import os
import openai
import pandas as pd


client = openai.api_key = os.getenv("OPENAI_API_KEY")

positive = [
    "A님, 정말 프로젝트마다 항상 새로운 아이디어를 가져와서 팀에 활력을 불어넣어 주시는 것 같아요. 창의적인 접근 방식이 정말 대단하다고 생각해요. 이런 에너지가 팀 전체에 긍정적인 영향을 주고 있어요.",
    "업무를 진행하면서 A님의 세심한 주의력과 뛰어난 분석력이 정말 돋보입니다. 복잡한 문제를 쉽게 해결해주시는 능력 덕분에 많은 도움을 받고 있어요. 그리고 항상 친절하게 동료들을 도와주셔서 감사해요.",
    "A님은 항상 긍정적인 태도로 팀 분위기를 밝게 만들어 주시는 것 같아요. 어려운 상황에서도 늘 웃음을 잃지 않으시는 모습이 인상적이에요. 그런 긍정적인 에너지가 팀 전체에 좋은 영향을 주고 있어요.",
    "A님의 열정과 노력이 프로젝트마다 빛을 발하고 있어요. 어떤 일이든 최선을 다하는 모습이 정말 존경스럽습니다. 팀에 계시는 것만으로도 큰 힘이 되고 있어요.",
    "A님은 항상 새로운 것을 배우려는 열정이 가득하신 것 같아요. 기술적인 면이나 업무 처리 방식에서도 늘 앞서가려는 모습이 보기 좋아요. 그런 자세가 팀 전체에도 좋은 영향을 미치고 있어요."
]

negative = [
    "A님, 프로젝트 할 때 세부적인 부분에 너무 많은 시간을 쓰시는 것 같아요. 그래서인지 전체적인 일정 관리가 좀 힘들어 보이더라고요. 전체 팀의 워크플로우에 맞춰서 일정 관리를 좀 더 신경 써 주셨으면 해요.",
    "의사소통할 때 너무 직선적인 표현을 사용하시는 경우가 많은 것 같습니다. 가끔은 동료들이 상처받을 수도 있다는 걸 염두에 두시면 좋겠어요. 좀 더 부드러운 표현을 사용해보는 건 어떨까요?",
    "A님, 팀 내에서 다른 문제들에 조금 더 관심을 가져주셨으면 합니다. 혼자서만 일하려고 하지 말고 팀원들과의 협력을 높여보세요. 모두가 함께 일하는 것이니까요.",
    "마감 기한을 지키는 것에 좀 더 주의를 기울여야 할 것 같아요. 마감이 늦어지면 프로젝트 전체에 영향을 미치니까요. 앞으로는 시간 관리에 좀 더 신경 써 주세요.",
    "기술적인 능력은 정말 좋지만, 새로운 기술이나 방법에 좀 더 개방적이 되셨으면 합니다. 변화에 유연하게 대응하는 것도 중요하다고 생각해요. 새로운 것을 배우려는 태도를 가져보면 어떨까요?"
]

sentences = [
    "일을 너무 못해서 짜증나요. 제발 능력을 좀 키워오세요.",
    "당신이 맡은 일에 대해 마감 기한을 지켜주세요. 진짜 짜증나서 같이 일 못하겠어요. ",
    "당신은 항상 긍정적이고 최선을 다하지만, 기술적으로 성장하는 모습을 보여주시길 바랍니다."
]

prompt = f"""
입력된 테스트는 어떤 한 사람에 대한 동료평가 내용입니다.
피드백 대상은 문장 내에서 표현되며, 만약 대상을 명확히 할 수 없을 경우, ///대상없음/// 으로 출력하세요
입력 텍스트의 내용에서 긍정적인 부분과 부정적인 부분을 각각 넘버링 없이 문장 형식으로 정리하세요.
단, 입력 텍스트에서 혐오표현, 비속어, 욕설, 은어, 감정적인 표현 등은 다른 착한 표현으로 대체해서 정리해야 합니다.

<피드백 대상> 님의 피드백 결과
긍정적인 피드백: ...
부정적인 피드백: ...

[대체된 표현의 개수: ]
대체된 표현: 원래표현 -> 대체된 표현
...
대체된 표현: 원래표현 -> 대체된 표현 

"""

# 문장들을 하나의 문자열로 결합
positive_input = "\n".join(positive)
negative_input = "\n".join(negative)
input_text = "\n".join(sentences)

analyze = openai.chat.completions.create (
    model="gpt-4",
    messages=[
        {"role": "system", "content": input_text},
        {"role": "user", "content": prompt},
    ],
)

output_text = analyze.choices[0].message.content

# 결과 출력
print(output_text)

#결과 엑셀로 저장

# 대체된 표현 추출
replacements = []
start_index = output_text.find("대체된 표현:")
while start_index != -1:
    end_index = output_text.find("\n", start_index)
    replacement = output_text[start_index:end_index]
    replacements.append(replacement)
    start_index = output_text.find("대체된 표현:", end_index)

# 원래 표현과 대체된 표현 추출
originals = []
replaced = []
for replacement in replacements:
    original_start = replacement.find("대체된 표현:") + 1
    original_end = replacement.find("->")
    replaced_start = replacement.find("->") + 2
    originals.append(replacement[original_start:original_end])
    replaced.append(replacement[replaced_start:].strip())

# 결과를 엑셀 파일로 저장
data = {
    "인물": ["A님"] * len(replacements),
    "긍정적인 피드백": [output_text.split("긍정적인 피드백: ")[1].split("부정적인 피드백:")[0].strip()] * len(replacements),
    "부정적인 피드백": [output_text.split("부정적인 피드백: ")[1].split("대체된 표현의 개수:")[0].strip()] * len(replacements),
    "원래 표현": originals,
    "대체된 표현": replaced
}

df = pd.DataFrame(data)

# 결과를 엑셀 파일로 저장
df.to_excel("피드백 결과.xlsx", index=False)