import streamlit as st
import requests

def find_pattern(seq):
    # 수열의 패턴을 찾고 다음 항을 예측하는 함수
    diff1 = seq[1] - seq[0]
    diff2 = seq[2] - seq[1]
    diff3 = seq[3] - seq[2]
    diff4 = seq[4] - seq[3]

    # 등차수열 검사
    if diff1 == diff2 == diff3 == diff4:
        return seq[4] + diff1, f"등차수열입니다. 공차는 {diff1}입니다."
    
    # 등비수열 검사
    if seq[0] != 0 and seq[1] != 0:  # 0으로 나누지 않기 위해 조건 추가
        ratio1 = seq[1] / seq[0]
        ratio2 = seq[2] / seq[1]
        ratio3 = seq[3] / seq[2]
        ratio4 = seq[4] / seq[3]
        if abs(ratio1 - ratio2) < 0.0001 and abs(ratio2 - ratio3) < 0.0001 and abs(ratio3 - ratio4) < 0.0001:
            return seq[4] * ratio1, f"등비수열입니다. 공비는 {ratio1:.2f}입니다."
    
    # 2차 수열 검사
    second_diff1 = diff2 - diff1
    second_diff2 = diff3 - diff2
    second_diff3 = diff4 - diff3
    if abs(second_diff1 - second_diff2) < 0.0001 and abs(second_diff2 - second_diff3) < 0.0001:
        return seq[4] + diff4 + second_diff1, f"2차 수열입니다. 차이의 차이는 {second_diff1}입니다."
    
    # 패턴을 찾지 못한 경우
    return None, "기본 패턴을 찾을 수 없습니다. OEIS 검색 결과를 확인해보세요."

def search_oeis(sequence):
    # OEIS API URL 설정
    url = f"https://oeis.org/search?q={','.join(map(str, sequence))}&fmt=json"
    response = requests.get(url)

    # 상태 코드 확인 및 디버깅 출력
    if response.status_code != 200:
        st.write("API 요청 실패:", response.status_code)
        return None

    # 응답 데이터 확인
    data = response.json()
    st.write("OEIS 응답 데이터:", data)  # 디버깅용 출력

    # OEIS 검색 결과 확인
    if "results" in data and data["results"]:
        return data["results"][:3]  # 최대 3개의 결과만 반환
    return None
    
# Streamlit UI 설정
st.title("수열 예측기 및 OEIS 검색")
st.write("수열의 첫 5개 항을 입력하고 다음 항을 예측하세요.")

# 사용자 입력 받기
input_numbers = [st.number_input(f"{i+1}번째 항 입력", value=0, step=1) for i in range(5)]
sequence = [int(num) for num in input_numbers]

if st.button("패턴 분석하기"):
    # 패턴 분석 및 다음 항 예측
    next_value, explanation = find_pattern(sequence)
    st.write(f"**분석 결과:** {explanation}")
    if next_value is not None:
        st.write(f"**예측된 다음 항:** {next_value}")

    # OEIS 검색 실행
    st.write("**OEIS 검색 결과:**")
    oeis_results = search_oeis(sequence)
    if oeis_results:
        for result in oeis_results:
            st.write(f"**A{result['number']}: {result['name']}**")
            st.write(f"설명: {result['description']}")
            st.write(f"처음 10개 항: {', '.join(result['data'][:10])}")
            st.write(f"[OEIS에서 더 알아보기](https://oeis.org/A{result['number']})")
    else:
        st.write("OEIS에서 일치하는 수열을 찾을 수 없습니다.")
