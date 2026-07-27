import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="StatScribe | APA Results Writer", layout="centered")

st.title("📊 StatScribe: APA Results Generator")
st.write("Turn raw statistical output (SPSS, Statistix) into publication-ready APA formatted paragraphs.")

# Sidebar for API Key (Keeps it secure and doesn't require hardcoding)
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
st.sidebar.markdown("[Get a free Gemini API key here](https://aistudio.google.com/app/apikey)")

# Main Form
with st.form("stat_form"):
    st.subheader("1. Research Context")
    research_q = st.text_input(
        "What was being tested?", 
        placeholder="e.g., The effect of dumpsite microbial isolates on plastic degradation rates."
    )
    
    st.subheader("2. Statistical Output")
    col1, col2 = st.columns(2)
    
    with col1:
        test_type = st.selectbox("Statistical Test Used", [
            "Independent Samples t-test", 
            "Paired Samples t-test", 
            "One-Way ANOVA", 
            "Two-Way ANOVA", 
            "Chi-Square Test",
            "Mann-Whitney U Test",
            "Kruskal-Wallis H Test"
        ])
        test_statistic = st.text_input("Test Statistic Value (e.g., t, F, χ²)", placeholder="e.g., 4.52")
    
    with col2:
        p_value = st.text_input("p-value", placeholder="e.g., 0.034 or <0.001")
        degrees_freedom = st.text_input("Degrees of Freedom (df)", placeholder="e.g., 2, 27")
        
    descriptive_stats = st.text_area(
        "Descriptive Statistics (Means, SDs)", 
        placeholder="e.g., Isolate A (M = 45.2, SD = 3.1), Control (M = 12.4, SD = 1.2)"
    )
    
    submit_button = st.form_submit_button("Generate APA Results Paragraph")

# AI Generation Logic
if submit_button:
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar to continue.")
    elif not all([research_q, test_statistic, p_value]):
        st.warning("Please fill in the Research Context, Test Statistic, and p-value fields.")
    else:
        with st.spinner("Drafting results paragraph..."):
            try:
                # Configure the API
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # The AI Instructions (System Prompt)
                system_prompt = f"""
                You are an expert academic data analyst. The user has conducted a {test_type} to investigate the following: {research_q}.
                
                Here are the raw statistical outputs:
                - Test Statistic: {test_statistic}
                - Degrees of Freedom: {degrees_freedom}
                - p-value: {p_value}
                - Descriptive Statistics: {descriptive_stats}
                
                Task: Write a single, highly professional paragraph reporting these results in strict 7th Edition APA format. 
                - Ensure statistical symbols (e.g., F, t, p) are italicized using Markdown.
                - State clearly whether the null hypothesis is rejected or accepted based on the p-value.
                - Do not add any filler text, introductory greetings, or conclusions outside of the paragraph.
                """
                
                # Generate Response
                response = model.generate_content(system_prompt)
                
                st.success("Generation Complete!")
                st.markdown("### Your APA Results Paragraph:")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")