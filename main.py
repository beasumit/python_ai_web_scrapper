import streamlit as st
from page.scrape import scrape_website, extract_body_content,clean_body_content,split_dom_content
from page.parse import parse_with_ollama
st.set_page_config(page_title="Python AI Web Scrapper 🪛",page_icon="🪛",layout="wide")
st.title(" Python AI Web Scrapper 🪛 ")


url = st.text_input(label="Enter The Website to Scrape")
if st.button(label="Scrape",type="primary"):
    st.success("Scrapping the website 🕸️")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)
    
    st.session_state.dom_content = cleaned_content
    
    with st.expander("View DOM Content"):
        st.text_area("Dom Content",cleaned_content,height=300)
    st.balloons()
    
if "dom_content" in st.session_state:
    parse_discription = st.text_area("Describe What You Want to Parse ?")
    
    if st.button(label="parse Content",type="primary"):
        if parse_discription:
            st.write("Parsing the Content 🔃")
            
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks,parse_discription)
            st.write(result)