import streamlit as st
import re  # For regex operations

# Assuming 'chat' is your function that returns [{'page_number': ..., 'text': ...}]
from main import chat


def highlight_search_terms(text, term):
    """Highlight the search term in the text with a yellow background."""
    highlighted_text = re.sub(f"({re.escape(term)})", r"<span style='background-color: #FFFF00'>\1</span>", text,
                              flags=re.IGNORECASE)
    return highlighted_text


st.title('Document Search with Streamlit')

user_input = st.text_input("Enter your query:", "")

if st.button('Search'):
    if user_input:
        results = chat(user_input)
        if results:
            st.text_area("Bot:", value=results, height=300)
        else:
            st.write("No results found.")
    else:
        st.write("Please enter a query to search.")
