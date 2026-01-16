import streamlit as st

if "BLOCK_LIST" not in st.session_state:
    st.session_state.BLOCK_LIST = []

for i, block in enumerate(st.session_state.BLOCK_LIST):
    with st.expander(label=f"Block {i+1}", expanded=True):
        left_border, col1, col2, right_border = st.columns([1,2,2,1])
        with col1:
            st.button("ADD ABOVE", key=f"test1_{i}")
        with col2:
            st.button("ADD UNDER", key=f"test2_{i}")

if st.button("Create Block +", key="create_block"):
    st.session_state.BLOCK_LIST.append("NEW")
    st.rerun()
