def get_custom_css():
    return """
    <style>
        /* General font and layout tweaks (warm theme) */
        body, .stApp {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            color: #111111;
            background-color: #fffaf5;
        }
        .main-header {
            font-size: 2.4rem;
            font-weight: 700;
            text-align: left;
            color: #d9480f; /* warm orange */
            margin: 0.2rem 0 0.6rem 0;
        }
        .sub-header {
            color: #7c4a00;
            margin-top: -6px;
            margin-bottom: 12px;
        }
        .metric-card {
            background: linear-gradient(135deg, #ff7a00 0%, #ff4500 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
        }
        .priority-high {
            background-color: #c53030;
            color: white;
            padding: 0.5rem;
            border-radius: 5px;
            font-weight: bold;
            margin: 0.5rem 0;
        }
        .priority-medium {
            background-color: #f97316;
            color: white;
            padding: 0.5rem;
            border-radius: 5px;
            font-weight: bold;
            margin: 0.5rem 0;
        }
        /* Make core text and container elements high-contrast */
        .stApp, .stApp * {
            color: #111111 !important;
        }
        .block-container {
            background-color: #fffaf5 !important;
            padding: 1rem 1.5rem !important;
        }
        .streamlit-expanderHeader, .st-expander {
            background-color: #fff3e0 !important;
            color: #111111 !important;
            border-radius: 8px;
        }
        .stMetric, .stMetricLabel, .stMetricValue {
            color: #111111 !important;
        }
        .stButton>button, .st-download-button>button {
            background-color: #d9480f !important;
            color: white !important;
        }
        .stDataFrame, .stTable {
            background-color: #fffaf5 !important;
            color: #111111 !important;
        }
        /* Make cards and legends stand out */
        .priority-high, .priority-medium {
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }
        .legend-badge { outline: 1px solid rgba(0,0,0,0.06); }
        .segment-badge {
            display: inline-block;
            padding: 0.4rem 0.8rem;
            border-radius: 15px;
            font-weight: bold;
            margin: 0.2rem 0.2rem 0.2rem 0;
            font-size: 0.85rem;
        }
        .hot-lead {
            background-color: #c53030;
            color: white;
        }
        .warm-lead {
            background-color: #fb923c;
            color: white;
        }
        .vip-customer {
            background-color: #9c27b0;
            color: white;
        }
        .urgency-extreme {
            background-color: #d72626;
            color: white;
            padding: 0.3rem 0.6rem;
            border-radius: 3px;
            font-weight: bold;
        }
        .urgency-high {
            background-color: #ff7a00;
            color: white;
            padding: 0.3rem 0.6rem;
            border-radius: 3px;
            font-weight: bold;
        }
        .urgency-medium {
            background-color: #f97316;
            color: white;
            padding: 0.3rem 0.6rem;
            border-radius: 3px;
            font-weight: bold;
        }
        .stButton>button {
            width: 100%;
            background-color: #d9480f;
            color: white;
            border-radius: 8px;
            padding: 8px 12px;
        }
        /* Small colored badge used for legends */
        .legend-badge {
            display:inline-block;
            width:12px;
            height:12px;
            border-radius:3px;
            margin-right:6px;
            vertical-align:middle;
        }

        /* Sidebar specific styling for better contrast and pale warm theme */
        section[data-testid='stSidebar'] {
            background-color: #fff3e0 !important;
            color: #111111 !important;
            padding: 1rem !important;
            border-right: 1px solid rgba(0,0,0,0.04);
        }
        section[data-testid='stSidebar'] * {
            color: #111111 !important;
        }
        section[data-testid='stSidebar'] .stButton>button,
        section[data-testid='stSidebar'] .st-download-button>button {
            background-color: #fb923c !important;
            color: white !important;
            border-radius: 6px !important;
        }
        section[data-testid='stSidebar'] .stImage > img {
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        section[data-testid='stSidebar'] .stRadio > div, section[data-testid='stSidebar'] .stMetric {
            background: transparent !important;
        }

        /* File uploader (browse) clarity */
        section[data-testid='stSidebar'] .stFileUploader, section[data-testid='stSidebar'] input[type="file"] {
            background-color: #fffaf0 !important;
            border: 1px solid rgba(0,0,0,0.06) !important;
            padding: 10px !important;
            border-radius: 8px !important;
            color: #111111 !important;
        }
        section[data-testid='stSidebar'] .stFileUploader button, section[data-testid='stSidebar'] .stFileUploader .css-1hsw8m0 {
            background-color: #fb923c !important;
            color: white !important;
        }
        /* Force uploader inner text/icons to be dark on pale background */
        section[data-testid='stSidebar'] .stFileUploader * {
            color: #111111 !important;
        }
        section[data-testid='stSidebar'] input[type="file"] {
            color: #111111 !important;
            background: #fffaf5 !important;
        }
        /* Webkit button inside file input */
        section[data-testid='stSidebar'] input[type="file"]::-webkit-file-upload-button {
            background: #fb923c !important;
            color: #ffffff !important;
            border: none !important;
            padding: 6px 10px !important;
            border-radius: 6px !important;
            cursor: pointer !important;
        }
        /* Ensure file name / status text is readable */
        section[data-testid='stSidebar'] .stFileUploader div, section[data-testid='stSidebar'] .stFileUploader p, section[data-testid='stSidebar'] .stFileUploader span {
            color: #111111 !important;
        }

        /* Main block help page readability */
        .block-container .stMarkdown, .block-container p, .block-container li, .block-container h1, .block-container h2, .block-container h3 {
            color: #111111 !important;
            line-height: 1.5 !important;
        }
        .block-container .stMarkdown code, .block-container pre, .block-container .code-block {
            background: #fff3e0 !important;
            color: #111111 !important;
            padding: 6px !important;
            border-radius: 6px !important;
        }

        /* Ensure help page headers are legible on pale background */
        .block-container h1, .block-container h2, .block-container h3 {
            color: #c2410c !important;
        }
    </style>
    """
