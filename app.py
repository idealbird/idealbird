# app.py

import streamlit as st
import requests

def main():
    st.title('OEIS 수열 검색기')

    st.write('수열의 첫 4개 항을 입력하세요.')

    # 사용자 입력
    term1 = st.number_input('첫 번째 항', min_value=0, step=1)
    term2 = st.number_input('두 번째 항', min_value=0, step=1)
    term3 = st.number_input('세 번째 항', min_value=0, step=1)
    term4 = st.number_input('네 번째 항', min_value=0, step=1)

    # 검색 버튼이 눌렸을 때
    if st.button('검색'):
        try:
            # 모든 입력 값이 정수인지 확인하고, 변환
            terms = [term1, term2, term3, term4]
            terms = [str(int(term)) for term in terms]
            sequence = ','.join(terms)

            response = requests.get(f'https://oeis.org/search?seq={sequence}&fmt=json')

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])[:3]  # 최대 3개의 결과만 사용

                if results:
                    for result in results:
                        seq_id = f"A{str(result['number']).zfill(6)}"
                        name = result.get('name', 'N/A')
                        seq_data = ', '.join(result.get('data', '').split(',')[:10])
                        description = result.get('comment', '설명이 없습니다.')

                        st.subheader(f"{seq_id}: {name}")
                        st.write(f"**처음 10개 항**: {seq_data}")
                        st.write(f"**설명**: {description}")
                        st.markdown('---')
                else:
                    st.warning('일치하는 수열을 찾을 수 없습니다.')
            else:
                st.error('OEIS 검색 중 오류가 발생했습니다.')
        except ValueError:
            st.error('유효한 숫자를 입력해주세요.')

if __name__ == '__main__':
    main()
