# app.py - Streamlit Web App
# app.py - Complete Streamlit Web App
# Full working code - just copy and paste!

import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
from product_detector import ProductDetector
from question_analyzer import QuestionAnalyzer

# Page configuration
st.set_page_config(
    page_title="Instagram Message Analyzer",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .priority-high {
        background-color: #ff4444;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .priority-medium {
        background-color: #ffbb33;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'results' not in st.session_state:
    st.session_state.results = None
if 'df' not in st.session_state:
    st.session_state.df = None

# Load analyzers (cached for performance)
@st.cache_resource
def load_analyzers():
    """Load analyzers once and cache them"""
    return ProductDetector(), QuestionAnalyzer()

product_detector, question_analyzer = load_analyzers()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/instagram-new.png", width=80)
    st.title("📊 Dashboard")
    st.markdown("---")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📂 Upload Excel File",
        type=['xlsx'],
        help="Upload your instagram_conversations.xlsx file"
    )
    
    st.markdown("---")
    
    # Quick stats if data loaded
    if st.session_state.df is not None:
        st.metric("Total Messages", len(st.session_state.df))
        if 'processed' in st.session_state.df.columns:
            new_count = len(st.session_state.df[st.session_state.df['processed'] == 'no'])
            st.metric("New Messages", new_count)
    
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "📍 Navigate",
        ["🏠 Home", "📊 Daily Analysis", "🚨 Priority Alerts", "📈 Statistics", "ℹ️ Help"]
    )
    
    st.markdown("---")
    st.caption("Made with IDealz Lanka (PVT) Ltd 🇱🇰")

# ============================================
# HOME PAGE
# ============================================
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">📱 Instagram Message Analyzer</h1>', unsafe_allow_html=True)
    
    if uploaded_file is None:
        st.info("👈 Upload your Excel file from the sidebar to get started!")
        
        # Features showcase
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🎯 Smart Analysis")
            st.write("✅ Product detection")
            st.write("✅ Question analysis")
            st.write("✅ Intent scoring")
            st.write("✅ Conversation tracking")
        
        with col2:
            st.markdown("### 📊 Daily Reports")
            st.write("✅ Only new messages")
            st.write("✅ Priority alerts")
            st.write("✅ Product demand")
            st.write("✅ Customer insights")
        
        with col3:
            st.markdown("### 📈 Features")
            st.write("✅ English + Sinhala")
            st.write("✅ Multi-product")
            st.write("✅ Real-time analysis")
            st.write("✅ Downloadable reports")
        
        st.markdown("---")
        
        # Excel format example
        st.markdown("### 📝 Required Excel Format:")
        
        sample_data = {
            'username': ['user1', 'user2', 'user3'],
            'message': ['iPhone 16 තියෙනවද?', 'Price කීයද?', 'Available tomorrow?'],
            'post_product': ['iPhone 16', '', 'Samsung S24'],
            'date': ['2026-01-06', '2026-01-07', '2026-01-07'],
            'processed': ['no', 'no', 'no']
        }
        st.dataframe(pd.DataFrame(sample_data), use_container_width=True)
        
    else:
        # File loaded - show overview
        st.success(f"✅ File loaded: {uploaded_file.name}")
        
        try:
            df = pd.read_excel(uploaded_file)
            st.session_state.df = df
            
            # Overview metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Total Messages", len(df))
            
            with col2:
                st.metric("👥 Unique Customers", df['username'].nunique())
            
            with col3:
                if 'processed' in df.columns:
                    new_count = len(df[df['processed'] == 'no'])
                    st.metric("🆕 New Messages", new_count)
                else:
                    st.metric("🆕 New Messages", len(df))
            
            with col4:
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'], errors='coerce')
                    days = (df['date'].max() - df['date'].min()).days
                    st.metric("📅 Days Span", days)
                else:
                    st.metric("📅 Days Span", "N/A")
            
            st.markdown("---")
            
            # Preview data
            with st.expander("👁️ Preview Data"):
                st.dataframe(df.head(10), use_container_width=True)
            
            st.info("👈 Navigate to 'Daily Analysis' to start analyzing messages!")
            
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")
            st.info("Make sure your Excel file has the correct format")

# ============================================
# DAILY ANALYSIS PAGE
# ============================================
elif page == "📊 Daily Analysis":
    st.title("📊 Daily Analysis")
    
    if uploaded_file is None:
        st.warning("⚠️ Please upload an Excel file first!")
    else:
        try:
            # Load data
            df = pd.read_excel(uploaded_file)
            st.session_state.df = df
            
            # Add processed column if missing
            if 'processed' not in df.columns:
                df['processed'] = 'no'
                st.info("ℹ️ Added 'processed' column to your data")
            
            # Convert dates
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Filter new messages
            new_messages = df[df['processed'] == 'no']
            
            # Display stats
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Total Messages", len(df))
            with col2:
                st.metric("✅ Already Processed", len(df) - len(new_messages))
            with col3:
                st.metric("🆕 New to Analyze", len(new_messages), delta=len(new_messages))
            
            st.markdown("---")
            
            if len(new_messages) == 0:
                st.success("✅ All messages are already processed!")
                st.info("💡 Add new messages with processed='no' and upload the file again")
            else:
                st.info(f"🆕 Found {len(new_messages)} new messages ready to analyze")
                
                # Show preview of new messages
                with st.expander("👁️ Preview New Messages"):
                    preview_cols = ['username', 'message', 'date']
                    available_cols = [col for col in preview_cols if col in new_messages.columns]
                    preview_df = new_messages[available_cols].head(10)
                    st.dataframe(preview_df, use_container_width=True)
                
                st.markdown("---")
                
                # Analyze button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    analyze_button = st.button("🚀 Analyze New Messages", type="primary", use_container_width=True)
                
                if analyze_button:
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    results = []
                    
                    # Process each new message
                    for idx, (i, row) in enumerate(new_messages.iterrows()):
                        # Update progress
                        progress = (idx + 1) / len(new_messages)
                        progress_bar.progress(progress)
                        status_text.text(f"Analyzing {idx + 1}/{len(new_messages)}: @{row['username']}")
                        
                        # Get message data
                        username = str(row['username']).strip()
                        message = str(row['message']).strip()
                        post_product = str(row.get('post_product', '')).strip() if pd.notna(row.get('post_product')) else ''
                        
                        if not message or message == 'nan':
                            continue
                        
                        # Get conversation history
                        history_count = len(df[(df['username'] == username) & (df['processed'] == 'yes')])
                        
                        # Detect products
                        products = product_detector.detect_products(message, post_product)
                        primary_product = product_detector.get_primary_product(products)
                        
                        # Analyze questions
                        questions = question_analyzer.analyze_questions(message)
                        all_questions = question_analyzer.format_questions_list(questions)
                        
                        # Intent signals
                        ready_to_buy = question_analyzer.is_ready_to_buy(message)
                        timeframe = question_analyzer.detect_timeframe(message)
                        
                        # Calculate intent score
                        score = 0.3
                        urgent_q = sum(1 for q in questions if q['urgency'] == 'high')
                        score += urgent_q * 0.15
                        if ready_to_buy:
                            score += 0.3
                        if timeframe in ['Today', 'Tomorrow']:
                            score += 0.25
                        elif timeframe != 'Not specified':
                            score += 0.10
                        if history_count > 0:
                            score += min(history_count * 0.05, 0.15)
                        score = min(score, 1.0)
                        
                        # Intent level
                        if score > 0.8:
                            intent = "Very High"
                        elif score > 0.6:
                            intent = "High"
                        elif score > 0.4:
                            intent = "Medium"
                        else:
                            intent = "Low"
                        
                        # Conversation stage
                        if history_count == 0:
                            stage = "Initial Contact"
                        elif history_count <= 2:
                            stage = "Follow-up"
                        else:
                            stage = "Active Discussion"
                        
                        # Store result
                        results.append({
                            'username': username,
                            'message': message[:100] + "..." if len(message) > 100 else message,
                            'product': primary_product,
                            'questions': all_questions,
                            'intent': intent,
                            'intent_score': f"{score:.0%}",
                            'timeframe': timeframe,
                            'ready_to_buy': 'YES' if ready_to_buy else 'NO',
                            'stage': stage,
                            'message_number': history_count + 1
                        })
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Store results in session
                    st.session_state.results = results
                    st.session_state.analyzed = True
                    
                    # Success message
                    st.success(f"✅ Successfully analyzed {len(results)} messages!")
                    
                    st.markdown("---")
                    
                    # Display results
                    st.markdown("### 📊 Analysis Results")
                    
                    results_df = pd.DataFrame(results)
                    
                    # Color coding function
                    def highlight_intent(row):
                        if row['intent'] == 'Very High':
                            return ['background-color: #ff4444; color: white'] * len(row)
                        elif row['intent'] == 'High':
                            return ['background-color: #ffbb33; color: white'] * len(row)
                        elif row['intent'] == 'Medium':
                            return ['background-color: #4CAF50; color: white'] * len(row)
                        else:
                            return [''] * len(row)
                    
                    styled_df = results_df.style.apply(highlight_intent, axis=1)
                    st.dataframe(styled_df, use_container_width=True)
                    
                    # Download button
                    csv = results_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"analysis_{date.today()}.csv",
                        mime="text/csv",
                        key='download-csv',
                        use_container_width=True
                    )
                    
                    st.markdown("---")
                    
                    # Summary statistics
                    st.markdown("### 📈 Summary Statistics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        very_high = len([r for r in results if r['intent'] == 'Very High'])
                        st.metric("🔥 Very High Intent", very_high)
                    with col2:
                        high = len([r for r in results if r['intent'] == 'High'])
                        st.metric("🎯 High Intent", high)
                    with col3:
                        medium = len([r for r in results if r['intent'] == 'Medium'])
                        st.metric("⚠️ Medium Intent", medium)
                    with col4:
                        low = len([r for r in results if r['intent'] == 'Low'])
                        st.metric("ℹ️ Low Intent", low)
                    
                    # Priority summary
                    priority_count = very_high + high
                    if priority_count > 0:
                        st.markdown("---")
                        st.error(f"🚨 {priority_count} customers need priority response!")
                        st.info("👉 Check the 'Priority Alerts' page for details")
                
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("Make sure your Excel file has the correct format with required columns: username, message, date")

# ============================================
# PRIORITY ALERTS PAGE
# ============================================
elif page == "🚨 Priority Alerts":
    st.title("🚨 Priority Customer Alerts")
    
    if st.session_state.results is None:
        st.warning("⚠️ Please run Daily Analysis first to see priority alerts")
        st.info("💡 Go to 'Daily Analysis' page and click 'Analyze New Messages'")
    else:
        results = st.session_state.results
        priority = [r for r in results if r['intent'] in ['Very High', 'High']]
        
        if len(priority) == 0:
            st.success("✅ No high-priority customers at the moment")
            st.balloons()
        else:
            st.error(f"🚨 {len(priority)} HIGH PRIORITY CUSTOMERS - ACTION REQUIRED!")
            
            # Sort by intent (Very High first)
            priority.sort(key=lambda x: (x['intent'] == 'Very High', x['intent_score']), reverse=True)
            
            st.markdown("---")
            
            # Display each priority customer
            for idx, p in enumerate(priority, 1):
                with st.container():
                    # Priority badge
                    if p['intent'] == 'Very High':
                        st.markdown(f'<div class="priority-high">🔥 PRIORITY #{idx} - VERY HIGH URGENCY</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="priority-medium">⚠️ PRIORITY #{idx} - HIGH URGENCY</div>', unsafe_allow_html=True)
                    
                    # Customer details in columns
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"### 👤 @{p['username']}")
                        st.write(f"**Message:** {p['message']}")
                        st.write(f"**Conversation Stage:** {p['stage']} (Message #{p['message_number']})")
                    
                    with col2:
                        st.metric("Intent Level", p['intent'], p['intent_score'])
                        st.write(f"**Product Interest:** {p['product']}")
                        st.write(f"**Questions:** {p['questions']}")
                        st.write(f"**Timeframe:** {p['timeframe']}")
                        st.write(f"**Ready to Buy:** {p['ready_to_buy']}")
                    
                    # Action recommendation
                    if p['intent'] == 'Very High':
                        st.error("⚡ **URGENT ACTION:** Reply within 30 minutes! Customer is ready to buy NOW!")
                    else:
                        st.warning("⏰ **ACTION REQUIRED:** Reply within 2 hours to maintain interest")
                    
                    st.markdown("---")

# ============================================
# STATISTICS PAGE
# ============================================
elif page == "📈 Statistics":
    st.title("📈 Statistics & Insights")
    
    if st.session_state.results is None:
        st.warning("⚠️ Please run Daily Analysis first to see statistics")
        st.info("💡 Go to 'Daily Analysis' page and analyze your messages")
    else:
        results = st.session_state.results
        df = st.session_state.df
        
        # Overall metrics
        st.markdown("### 📊 Overall Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📧 Total Messages", len(df) if df is not None else 0)
        with col2:
            st.metric("🆕 Analyzed Today", len(results))
        with col3:
            st.metric("👥 Unique Customers", df['username'].nunique() if df is not None else 0)
        with col4:
            priority_count = len([r for r in results if r['intent'] in ['High', 'Very High']])
            st.metric("🚨 Priority Customers", priority_count)
        
        st.markdown("---")
        
        # Intent distribution
        st.markdown("### 🎯 Purchase Intent Distribution")
        
        intent_counts = {}
        for r in results:
            intent_counts[r['intent']] = intent_counts.get(r['intent'], 0) + 1
        
        if intent_counts:
            col1, col2 = st.columns(2)
            
            with col1:
                # Bar chart
                st.bar_chart(pd.Series(intent_counts))
            
            with col2:
                # Metrics
                st.write("**Intent Breakdown:**")
                for intent, count in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(results)) * 100
                    st.metric(intent, f"{count} ({percentage:.1f}%)")
        
        st.markdown("---")
        
        # Product demand
        st.markdown("### 📦 Product Demand Analysis")
        
        products = {}
        for r in results:
            if r['product'] != 'Not specified':
                products[r['product']] = products.get(r['product'], 0) + 1
        
        if products:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Top Requested Products:**")
                # Bar chart
                products_series = pd.Series(products).sort_values(ascending=False)
                st.bar_chart(products_series)
            
            with col2:
                st.markdown("**Product Request Details:**")
                # Table
                products_df = pd.DataFrame(list(products.items()), columns=['Product', 'Requests'])
                products_df = products_df.sort_values('Requests', ascending=False)
                products_df['Percentage'] = (products_df['Requests'] / products_df['Requests'].sum() * 100).round(1)
                st.dataframe(products_df, use_container_width=True)
        else:
            st.info("No specific products mentioned in analyzed messages")
        
        st.markdown("---")
        
        # Question analysis
        st.markdown("### ❓ Common Customer Questions")
        
        questions_dict = {}
        for r in results:
            for q in r['questions'].split(', '):
                questions_dict[q] = questions_dict.get(q, 0) + 1
        
        if questions_dict:
            questions_df = pd.DataFrame(list(questions_dict.items()), columns=['Question Type', 'Count'])
            questions_df = questions_df.sort_values('Count', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.bar_chart(questions_df.set_index('Question Type'))
            
            with col2:
                st.dataframe(questions_df, use_container_width=True)
        
        st.markdown("---")
        
        # Timeframe analysis
        st.markdown("### ⏰ Customer Urgency Timeline")
        
        timeframes = {}
        for r in results:
            if r['timeframe'] != 'Not specified':
                timeframes[r['timeframe']] = timeframes.get(r['timeframe'], 0) + 1
        
        if timeframes:
            col1, col2, col3 = st.columns(3)
            
            urgent = timeframes.get('Today', 0) + timeframes.get('Tomorrow', 0)
            soon = timeframes.get('This Weekend', 0) + timeframes.get('Next Week', 0)
            later = timeframes.get('This Month', 0)
            
            with col1:
                st.metric("🔥 Urgent (Today/Tomorrow)", urgent)
            with col2:
                st.metric("⏰ Soon (This Week)", soon)
            with col3:
                st.metric("📅 Later (This Month)", later)

# ============================================
# HELP PAGE
# ============================================
elif page == "ℹ️ Help":
    st.title("ℹ️ Help & Documentation")
    
    st.markdown("""
    ## 📖 How to Use This Application
    
    ### 1️⃣ Upload Your Excel File
    - Click **"Upload Excel File"** in the sidebar
    - Select your `instagram_conversations.xlsx` file
    - File will be loaded automatically
    
    ### 2️⃣ Required Excel Format
    
    Your Excel file **must** have these columns:
    
    | Column | Required? | Description | Example |
    |--------|-----------|-------------|---------|
    | **username** | ✅ Required | Customer's Instagram handle | nimesh_94 |
    | **message** | ✅ Required | Their message text | "iPhone 16 තියෙනවද? Price?" |
    | **date** | ✅ Required | When they messaged | 2026-01-06 |
    | **processed** | Optional | Leave as "no" for new messages | no |
    | **post_product** | Optional | Product in your ad (if they replied to post) | iPhone 16 |
    | **post_description** | Optional | Your ad caption | "Best Price in SL!" |
    
    ### 3️⃣ Daily Analysis Workflow
    
    1. Go to **"Daily Analysis"** page
    2. System automatically detects NEW messages (where processed='no')
    3. Click **"Analyze New Messages"** button
    4. Wait for analysis to complete (shows progress)
    5. View results and download CSV report
    
    ### 4️⃣ Priority Alerts
    
    - Navigate to **"Priority Alerts"** page
    - View customers with High or Very High purchase intent
    - See recommended response times
    - Take immediate action on urgent customers
    
    ### 5️⃣ Statistics Dashboard
    
    - View **"Statistics"** page for insights
    - See product demand trends
    - Analyze question patterns
    - Track customer urgency levels
    
    ## 🎯 Understanding Intent Levels
    
    The system scores purchase intent from 0-100%:
    
    ### 🔥 Very High Intent (80%+)
    - **Signals:** "I will come today", "keep one for me", urgent timeframe
    - **Action:** Reply within **30 minutes**
    - **Status:** Customer is ready to buy NOW!
    
    ### ⚠️ High Intent (60-80%)
    - **Signals:** Asking price + availability, mentions specific timeframe
    - **Action:** Reply within **2 hours**
    - **Status:** Serious buyer, high conversion potential
    
    ### 📊 Medium Intent (40-60%)
    - **Signals:** General questions, comparing options
    - **Action:** Reply **same day**
    - **Status:** Interested but still considering
    
    ### ℹ️ Low Intent (<40%)
    - **Signals:** Just browsing, vague inquiries
    - **Action:** Standard response time
    - **Status:** Information gathering stage
    
    ## 🌟 Features
    
    ### Product Detection
    - Automatically detects iPhone models (17, 16, 15, 14, 13)
    - MacBook models (Air M3/M2, Pro M3/M2)
    - Samsung Galaxy (S24, S23)
    - Storage sizes (128GB, 256GB, 512GB)
    
    ### Question Analysis
    - **Price inquiries** (English + Sinhala: කීයද?, ගණන)
    - **Availability** (තියෙනවද?, stock)
    - **Payment options** (වාරික, installment)
    - **Warranty** (වගකීම, guarantee)
    - **Colors, Delivery, Exchange**, etc.
    
    ### Language Support
    - **English:** Full support
    - **Sinhala:** Common phrases and questions
    - **Mixed:** Handles English-Sinhala mix
    
    ## 💡 Pro Tips
    
    ### Daily Workflow
    1. **Morning:** Update Excel with overnight Instagram messages
    2. **Run Analysis:** Upload file and analyze
    3. **Check Priority:** Respond to high-intent customers first
    4. **Track:** Download daily reports for records
    
    ### Excel Management
    - Keep ONE master Excel file
    - Add new messages with `processed='no'`
    - System automatically marks analyzed messages as 'yes'
    - Never delete processed messages (maintains conversation history)
    
    ### Conversation Tracking
    - System tracks returning customers automatically
    - Shows message number (1st, 2nd, 3rd contact)
    - Higher intent for engaged conversations
    
    ## 🆘 Troubleshooting
    
    ### "File upload error"
    - ✅ Check file is `.xlsx` format (not `.xls` or `.csv`)
    - ✅ Verify required columns exist
    - ✅ Make sure column names are exact
    
    ### "No results showing"
    - ✅ Run Daily Analysis first
    - ✅ Check there are messages with processed='no'
    - ✅ Verify Excel format is correct
    
    ### "Wrong products detected"
    - ✅ Add product name to `post_product` column
    - ✅ Use specific model names in messages
    - ✅ Check spelling matches supported products
    
    ### "Analysis takes too long"
    - ⏰ Normal: 1-2 seconds per message
    - ⏰ First time may be slower (loading models)
    - ⏰ 100 messages ≈ 3-5 minutes
    
    ## 📞 Best Practices
    
    ### Response Time Guidelines
    - **Very High Intent:** 30 minutes (drop everything!)
    - **High Intent:** 2 hours (priority over others)
    - **Medium Intent:** Same day (normal priority)
    - **Low Intent:** Within 24 hours
    
    ### Data Management
    - Update Excel daily for best results
    - Keep backup copies of your data
    - Download CSV reports regularly
    - Review weekly statistics for trends
    
    ### Team Usage
    - Share app URL with team members
    - Everyone can upload their own Excel files
    - No data shared between users
    - Perfect for multi-person shops
    
    ## 🎓 Need More Help?
    
    If you encounter issues:
    1. Check this help page first
    2. Verify Excel format is correct
    3. Make sure all required columns exist
    4. Try with sample data to test
    
    ## 📈 Measuring Success
    
    Track these metrics weekly:
    - **Response Time:** How fast you reply to high-intent customers
    - **Conversion Rate:** Messages that result in sales
    - **Product Trends:** Which models are most requested
    - **Customer Satisfaction:** Based on follow-up conversations
    
    ---
    
    **Happy analyzing! Your customers are waiting!** 🚀
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <strong>📱 Instagram Message Analyzer v1.0</strong><br>
    Made with for Idealz Lanka PVT (Ltd) in Sri Lanka 🇱🇰<br>
    <small>Analyze smarter, sell faster!</small>
</div>
""", unsafe_allow_html=True)