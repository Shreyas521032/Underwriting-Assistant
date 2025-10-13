import streamlit as st
import json
from datetime import datetime
import pandas as pd

# Page config
st.set_page_config(
    page_title="Underwriting Assistant AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .risk-low {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    }
    .risk-medium {
        background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%);
    }
    .risk-high {
        background: linear-gradient(135deg, #ef5350 0%, #e53935 100%);
    }
    .info-box {
        background-color: #f3f4f6;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

def analyze_risk(applicant_data, claims_history, external_reports):
    """Simulate AI-powered risk analysis using prompt chaining"""
    
    # Step 1: Data Summarization
    applicant_summary = f"""
    Applicant Profile:
    - Age: {applicant_data['age']} years
    - Occupation: {applicant_data['occupation']}
    - Location: {applicant_data['location']}
    - Coverage Amount: ${applicant_data['coverage_amount']:,}
    - Health Status: {applicant_data['health_status']}
    - Lifestyle: {applicant_data['lifestyle_factors']}
    """
    
    # Step 2: Claims Analysis
    total_claims = len(claims_history)
    total_claim_amount = sum([c['amount'] for c in claims_history])
    
    claims_summary = f"""
    Claims History:
    - Total Claims: {total_claims}
    - Total Amount: ${total_claim_amount:,}
    - Claim Types: {', '.join(set([c['type'] for c in claims_history]))}
    """
    
    # Step 3: Risk Scoring (Simulated LLM chain)
    risk_factors = []
    risk_score = 50  # Base score
    
    # Age factor
    if applicant_data['age'] < 25:
        risk_score += 10
        risk_factors.append("Young driver/applicant - higher risk profile")
    elif applicant_data['age'] > 65:
        risk_score += 15
        risk_factors.append("Senior age - increased health considerations")
    else:
        risk_score -= 5
    
    # Claims history factor
    if total_claims > 3:
        risk_score += 20
        risk_factors.append("Multiple prior claims indicating pattern")
    elif total_claims > 0:
        risk_score += 10
        risk_factors.append("Previous claims history present")
    else:
        risk_score -= 10
        risk_factors.append("Clean claims history - positive indicator")
    
    # Health status factor
    if applicant_data['health_status'] == 'Excellent':
        risk_score -= 15
        risk_factors.append("Excellent health status - low risk")
    elif applicant_data['health_status'] == 'Poor':
        risk_score += 25
        risk_factors.append("Poor health status - significant risk factor")
    
    # Lifestyle factor
    if 'Smoker' in applicant_data['lifestyle_factors']:
        risk_score += 15
        risk_factors.append("Smoking habit increases risk profile")
    if 'High-risk sports' in applicant_data['lifestyle_factors']:
        risk_score += 10
        risk_factors.append("High-risk activities noted")
    
    # External reports factor
    if external_reports['credit_score'] < 600:
        risk_score += 10
        risk_factors.append("Low credit score indicates financial instability")
    elif external_reports['credit_score'] > 750:
        risk_score -= 5
        risk_factors.append("Strong credit score - financially stable")
    
    if external_reports['criminal_record']:
        risk_score += 20
        risk_factors.append("Criminal record present - elevated risk")
    
    # Normalize score to 0-100
    risk_score = max(0, min(100, risk_score))
    
    # Determine risk category
    if risk_score < 40:
        risk_category = "Low Risk"
        recommendation = "APPROVE - Standard premium rates recommended"
        color_class = "risk-low"
    elif risk_score < 70:
        risk_category = "Medium Risk"
        recommendation = "APPROVE WITH CONDITIONS - Consider adjusted premium or additional clauses"
        color_class = "risk-medium"
    else:
        risk_category = "High Risk"
        recommendation = "REVIEW REQUIRED - Manual underwriter review recommended before approval"
        color_class = "risk-high"
    
    return {
        'risk_score': risk_score,
        'risk_category': risk_category,
        'recommendation': recommendation,
        'color_class': color_class,
        'risk_factors': risk_factors,
        'applicant_summary': applicant_summary,
        'claims_summary': claims_summary,
        'total_claims': total_claims,
        'total_claim_amount': total_claim_amount
    }

def main():
    # Header
    st.markdown('<div class="main-header">🛡️ Underwriting Assistant AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">GenAI-Powered Risk Assessment & Decision Support System</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=Insurance+Co", use_container_width=True)
        st.markdown("### 📊 System Features")
        st.markdown("""
        - ✅ Automated risk scoring
        - 📝 Applicant data summarization
        - 📈 Claims history analysis
        - 🔍 External report integration
        - 🤖 LLM prompt chaining
        - 📋 Structured output generation
        """)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info("This AI co-pilot assists underwriters in making data-driven decisions by analyzing multiple data sources and generating comprehensive risk assessments.")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📝 New Application", "📊 Analysis Results", "📚 Sample Data"])
    
    with tab1:
        st.markdown("### Applicant Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Applicant Name", "John Smith")
            age = st.number_input("Age", 18, 100, 35)
            occupation = st.selectbox("Occupation", 
                ["Software Engineer", "Teacher", "Construction Worker", "Doctor", "Sales Manager", "Pilot"])
            location = st.text_input("Location", "New York, NY")
            coverage_amount = st.number_input("Coverage Amount ($)", 50000, 5000000, 500000, step=50000)
        
        with col2:
            health_status = st.selectbox("Health Status", 
                ["Excellent", "Good", "Fair", "Poor"])
            lifestyle_factors = st.multiselect("Lifestyle Factors",
                ["Non-smoker", "Smoker", "Regular exercise", "High-risk sports", "Alcohol consumption"],
                ["Non-smoker", "Regular exercise"])
            
        st.markdown("### Claims History")
        num_claims = st.number_input("Number of Previous Claims", 0, 10, 2)
        
        claims_history = []
        if num_claims > 0:
            for i in range(num_claims):
                with st.expander(f"Claim {i+1}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        claim_type = st.selectbox(f"Type", 
                            ["Auto", "Property", "Health", "Liability"], key=f"type_{i}")
                    with col2:
                        claim_amount = st.number_input(f"Amount ($)", 100, 100000, 5000, key=f"amt_{i}")
                    with col3:
                        claim_date = st.date_input(f"Date", key=f"date_{i}")
                    
                    claims_history.append({
                        'type': claim_type,
                        'amount': claim_amount,
                        'date': str(claim_date)
                    })
        
        st.markdown("### External Reports")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            credit_score = st.slider("Credit Score", 300, 850, 720)
        with col2:
            criminal_record = st.checkbox("Criminal Record")
        with col3:
            driving_record = st.selectbox("Driving Record", ["Clean", "Minor violations", "Major violations"])
        
        st.markdown("---")
        
        if st.button("🔍 Analyze Risk Profile", use_container_width=True):
            with st.spinner("Analyzing application data..."):
                applicant_data = {
                    'name': name,
                    'age': age,
                    'occupation': occupation,
                    'location': location,
                    'coverage_amount': coverage_amount,
                    'health_status': health_status,
                    'lifestyle_factors': ', '.join(lifestyle_factors)
                }
                
                external_reports = {
                    'credit_score': credit_score,
                    'criminal_record': criminal_record,
                    'driving_record': driving_record
                }
                
                results = analyze_risk(applicant_data, claims_history, external_reports)
                st.session_state.analysis_results = results
                st.success("✅ Analysis complete! View results in the 'Analysis Results' tab.")
                st.rerun()
    
    with tab2:
        if st.session_state.analysis_results is None:
            st.info("👈 Please complete the application form and click 'Analyze Risk Profile' to see results.")
        else:
            results = st.session_state.analysis_results
            
            st.markdown("### 🎯 Risk Assessment Summary")
            
            # Risk score display
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card {results['color_class']}">
                    <h3 style="margin:0;">Risk Score</h3>
                    <h1 style="margin:0.5rem 0;">{results['risk_score']}/100</h1>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card {results['color_class']}">
                    <h3 style="margin:0;">Risk Category</h3>
                    <h1 style="margin:0.5rem 0;">{results['risk_category']}</h1>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin:0;">Total Claims</h3>
                    <h1 style="margin:0.5rem 0;">{results['total_claims']}</h1>
                    <p style="margin:0;">${results['total_claim_amount']:,}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Recommendation
            st.markdown("### 💡 Underwriting Recommendation")
            st.success(results['recommendation'])
            
            # Risk factors
            st.markdown("### ⚠️ Key Risk Factors")
            for factor in results['risk_factors']:
                st.markdown(f"- {factor}")
            
            st.markdown("---")
            
            # Detailed summaries
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 👤 Applicant Summary")
                st.markdown(f"```\n{results['applicant_summary']}\n```")
            
            with col2:
                st.markdown("### 📋 Claims Summary")
                st.markdown(f"```\n{results['claims_summary']}\n```")
            
            # Export options
            st.markdown("---")
            st.markdown("### 📥 Export Report")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📄 Download JSON Report"):
                    report_json = json.dumps(results, indent=2, default=str)
                    st.download_button(
                        label="Save JSON",
                        data=report_json,
                        file_name=f"risk_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            with col2:
                if st.button("🔄 New Analysis"):
                    st.session_state.analysis_results = None
                    st.rerun()
    
    with tab3:
        st.markdown("### 📚 Sample Data & Use Cases")
        
        st.markdown("#### Low Risk Profile Example")
        st.code("""
Applicant: Sarah Johnson
Age: 32
Occupation: Teacher
Health: Excellent
Claims History: 0 claims
Credit Score: 780
Risk Score: 25/100 → APPROVED
        """)
        
        st.markdown("#### Medium Risk Profile Example")
        st.code("""
Applicant: Mike Davis
Age: 45
Occupation: Construction Worker
Health: Fair
Claims History: 2 claims ($12,000 total)
Credit Score: 650
Risk Score: 58/100 → APPROVED WITH CONDITIONS
        """)
        
        st.markdown("#### High Risk Profile Example")
        st.code("""
Applicant: Robert Wilson
Age: 68
Occupation: Pilot
Health: Poor
Claims History: 5 claims ($45,000 total)
Credit Score: 550
Criminal Record: Yes
Risk Score: 85/100 → MANUAL REVIEW REQUIRED
        """)
        
        st.markdown("---")
        st.markdown("### 🔧 AI Prompt Chaining Flow")
        st.markdown("""
        1. **Data Summarization**: Extract and structure applicant information
        2. **Claims Analysis**: Aggregate and analyze historical claims data
        3. **External Report Integration**: Incorporate credit, criminal, and driving records
        4. **Risk Factor Identification**: Identify key risk indicators using LLM reasoning
        5. **Score Calculation**: Weighted scoring based on multiple factors
        6. **Recommendation Generation**: Generate actionable underwriting decisions
        7. **Structured Output**: Format results in standardized JSON schema
        """)

if __name__ == "__main__":
    main()
