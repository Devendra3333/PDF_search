import streamlit as st
from main import chat_prompt



st.title('Document Search with Streamlit')

user_input = st.text_input("Enter your query:", "")

if st.button('Search'):
    if user_input:
        results, docs = chat_prompt(user_input)
        if results:
            st.text_area("Bot:", value=results, height=300)

            # Assuming 'docs' is a list of 'Document' objects
            for doc in docs:
                page_content = doc.page_content  # Directly access the 'page_content' attribute
                page_number = doc.metadata['page']  # Access the 'page' key within the 'metadata' dictionary

                st.write(f"Page Number: {page_number}")
                st.write(f"Page Content: {page_content}\n")

        else:
            st.write("No results found.")
    else:
        st.write("Please enter a query to search.")
