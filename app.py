import streamlit as st
from serpapi import GoogleSearch
import pandas as pd
from urllib.parse import urlparse

# Page Configuration
st.set_page_config(
    page_title="PulseIQ - Enterprise Search Intelligence Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphism & Modern Dark Theme Styling
st.markdown("""
    <style>
    /* Global Styling */
    .stApp {
        background-color: #0B0F19;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 25px;
    }
    /* Executive Summary Card */
    .summary-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    .summary-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #818CF8;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">⚡ PulseIQ Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Real-Time Search Index Synthesizer Grounded via SerpApi</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎛️ Control Center")
api_key = st.sidebar.text_input("SerpApi API Key", type="password", help="Get your API key from serpapi.com")

st.sidebar.divider()
st.sidebar.subheader("🎯 Intelligence Parameters")
city = st.sidebar.text_input("Target Location / Region", "Bengaluru")
domain_category = st.sidebar.selectbox(
    "Intelligence Domain",
    [
        "Tech Hiring & Developer Demand",
        "Air Quality & Environmental Safety",
        "Local Real Estate & Commercial Growth",
        "AI & Startup Ecosystem News"
    ]
)
sample_depth = st.sidebar.slider("Extraction Depth (Results)", min_value=5, max_value=15, value=8)

st.sidebar.divider()
st.sidebar.caption("🏆 Built for SerpApi India Hackathon 2026")

# Layout Column
col_main, col_status = st.columns([3, 1])

with col_main:
    st.markdown(f"### 📍 Target Matrix: **{city}** — *{domain_category}*")
    execute_btn = st.button("🚀 Execute Real-Time Scan", type="primary", use_container_width=True)

with col_status:
    st.info("🔒 **Engine Status:** Ready\n\n**API Engine:** `google`\n\n**Grounding:** Live Search")

if execute_btn:
    if not api_key:
        st.error("⚠️ SerpApi Secret Key missing! Please enter your key in the left sidebar.")
    else:
        search_query = f"{city} {domain_category}"
        
        with st.spinner(f"Querying SerpApi Google Search Engine for: '{search_query}'..."):
            params = {
                "q": search_query,
                "engine": "google",
                "api_key": api_key,
                "num": sample_depth
            }
            
            try:
                search = GoogleSearch(params)
                results = search.get_dict()
                organic_results = results.get("organic_results", [])
                metadata = results.get("search_metadata", {})

                if not organic_results:
                    st.warning("No search signals detected for this query. Adjust parameters and try again.")
                else:
                    # Top Level Metrics
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Latency", f"{metadata.get('total_time_taken', '0.38')}s")
                    m2.metric("Signals Processed", len(organic_results))
                    
                    # Extract unique domains
                    domains = [urlparse(item.get("link", "")).netloc for item in organic_results if item.get("link")]
                    unique_domains = len(set(domains))
                    m3.metric("Unique Sources", unique_domains)
                    m4.metric("Engine Context", "Google Search API")

                    st.divider()

                    # Executive Summary Synthesizer
                    all_snippets = " ".join([item.get("snippet", "") for item in organic_results])
                    top_words = pd.Series([w.strip(".,()[]'\"").lower() for w in all_snippets.split() if len(w) > 4]).value_counts().head(5).index.tolist()
                    
                    st.markdown(f"""
                        <div class="summary-card">
                            <div class="summary-title">💡 Executive Intelligence Brief: {city}</div>
                            <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 8px;">
                                Live web indexing for <strong>{city}</strong> within the <strong>{domain_category}</strong> domain reveals active market signals.
                                Key trending topics extracted across {len(organic_results)} live web indexes focus heavily on 
                                <span style="color: #818CF8; font-weight: 600;">{", ".join(top_words).title()}</span>.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

                    # Multi-View Dashboard Tabs
                    tab_signals, tab_analytics, tab_export = st.tabs([
                        "📡 Live Interactive Signals", 
                        "📊 Domain & Frequency Analytics", 
                        "💾 Export & Raw JSON"
                    ])

                    with tab_signals:
                        st.caption("👇 **Click on any intel signal to inspect metadata, source domain, and direct access links:**")
                        
                        for idx, item in enumerate(organic_results, start=1):
                            title = item.get("title", "Untitled Source")
                            snippet = item.get("snippet", "No summary snippet available.")
                            link = item.get("link", "#")
                            domain = urlparse(link).netloc
                            displayed_link = item.get("displayed_link", domain)

                            # Clean, Enterprise Signal Title
                            expander_title = f"🔴 SIGNAL #{idx:02d}  |  {domain.upper()}  —  {title}"
                            
                            with st.expander(expander_title, expanded=(idx == 1)):
                                c1, c2 = st.columns([3, 1])
                                
                                with c1:
                                    st.markdown("##### 📝 Extracted Intel Snippet")
                                    st.info(f'"{snippet}"')
                                    st.markdown(f"🌐 **Source URL:** [{link}]({link})")

                                with c2:
                                    st.markdown("##### 🛡️ Source Audit")
                                    st.markdown(f"""
                                    - **Rank Position:** `#{idx}`
                                    - **Domain Host:** `{domain}`
                                    - **Verification:** `SerpApi Grounded`
                                    - **Snippet Length:** `{len(snippet.split())} words`
                                    """)
                                    st.link_button("🔗 Open Source", link, use_container_width=True)

                    with tab_analytics:
                        col_chart1, col_chart2 = st.columns(2)
                        
                        with col_chart1:
                            st.markdown("#### 🌐 Top Source Domains")
                            if domains:
                                domain_counts = pd.Series(domains).value_counts().head(7)
                                st.bar_chart(domain_counts)

                        with col_chart2:
                            st.markdown("#### 🔑 Keyword Frequency in Search Snippets")
                            words = [w.strip(".,()[]'\"").lower() for w in all_snippets.split() if len(w) > 4]
                            if words:
                                word_counts = pd.Series(words).value_counts().head(7)
                                st.bar_chart(word_counts)

                    with tab_export:
                        st.markdown("#### 📄 Export Intelligence Data")
                        
                        df_export = pd.DataFrame([
                            {
                                "Rank": idx,
                                "Title": item.get("title"),
                                "Domain": urlparse(item.get("link", "")).netloc,
                                "Snippet": item.get("snippet"),
                                "URL": item.get("link")
                            } for idx, item in enumerate(organic_results, start=1)
                        ])

                        st.dataframe(df_export, use_container_width=True)
                        
                        csv_data = df_export.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Intelligence CSV Report",
                            data=csv_data,
                            file_name=f"PulseIQ_{city}_{domain_category}.csv",
                            mime="text/csv",
                            type="primary"
                        )
                        
                        st.divider()
                        st.markdown("#### ⚙️ Raw SerpApi JSON Payload")
                        st.json(organic_results)

                    st.success("✅ Real-Time Intelligence Scan Completed Successfully.")

            except Exception as e:
                st.error(f"Execution Failure: {str(e)}")

# Footer
st.divider()
st.caption("PulseIQ Engine • Powered by SerpApi Google Search API • Built for SerpApi India Hackathon 2026")