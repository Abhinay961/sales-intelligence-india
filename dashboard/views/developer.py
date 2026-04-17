import streamlit as st

def app():

    st.markdown("<h1 style='text-align: center; color: #4facfe;'>Developer Profiles</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #a0a0a0;'>Meet the creators of the Sales Intelligence Platform.</p>", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='text-align: center; color: #00f2fe;'>Abhinay Mishra</h3>", unsafe_allow_html=True)
        st.info("""
        **B.Tech CSBS Student**  
        **Aspiring Data Analyst**  
        **ML & Data Science Enthusiast**  
        """, icon="🎓")

    with col2:
        st.markdown("<h3 style='text-align: center; color: #00f2fe;'>Sharad Singh Ghosh</h3>", unsafe_allow_html=True)
        st.info("""
        **B.Tech CSBS (4th sem, 2nd year)**  
        **MITS Gwalior**  
        **Developer**
        """, icon="🎓")

    st.markdown("---")

    st.markdown("<h3 style='color: #4facfe;'>Project Highlights</h3>", unsafe_allow_html=True)
    st.markdown("""
    <ul style='font-size: 16px; line-height: 1.8;'>
        <li>Built an end-to-end <b>Sales Intelligence Platform</b></li>
        <li>Implemented Machine Learning-based revenue prediction</li>
        <li>Designed an interactive, dynamic dashboard using Streamlit and Plotly</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='color: #4facfe;'>Core Skills</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px;'>Python | Pandas | Machine Learning | Data Visualization | SQL</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='text-align: center; font-style: italic; color: #888;'>Built with Streamlit & Plotly</p>", unsafe_allow_html=True)