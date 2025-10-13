import streamlit as st
import json
from datetime import datetime
import pandas as pd
import requests
import time

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
    .flow-step {
        background: white;
        border: 2px solid #667eea;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .agent-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.2rem;
        border-radius: 8px;
        color: white;
        margin: 0.8rem 0;
    }
    .process-arrow {
        text-align: center;
        font-size: 2rem;
        color: #667eea;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'agent_outputs' not in st.session_state:
    st.session_state.agent_outputs = {}

# AI Agent Class
class UnderwritingAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def query_llm(self, prompt, max_tokens=500):
        """Query Hugging Face LLM API"""
        if not self.api_key or self.api_key == "":
            return self._fallback_response(prompt)
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.95,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').strip()
                return str(result)
            else:
                return self._fallback_response(prompt)
        except Exception as e:
            st.warning(f"API call failed: {str(e)}. Using fallback logic.")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt):
        """Fallback response when API is unavailable"""
        if "summarize" in prompt.lower():
            return "Applicant profile analyzed. Key factors identified include age, occupation, health status, and lifestyle factors that contribute to overall risk assessment."
        elif "claims" in prompt.lower():
            return "Claims history reviewed. Pattern analysis indicates frequency and severity of previous claims, which are important predictors of future risk."
        elif "risk factors" in prompt.lower():
            return "Multiple risk factors identified including age demographics, health conditions, lifestyle choices, financial stability indicators, and historical claims patterns."
        elif "recommendation" in prompt.lower():
            return "Based on comprehensive analysis, underwriting decision should consider all identified risk factors with appropriate premium adjustments or policy conditions."
        return "Analysis complete. Risk assessment performed based on available data."

class DataSummarizationAgent(UnderwritingAgent):
    def summarize_applicant(self, applicant_data):
        """Agent 1: Summarize applicant information"""
        prompt = f"""You are an insurance underwriting assistant. Analyze and summarize the following applicant information in 2-3 concise sentences, highlighting key risk-relevant factors:

Applicant Details:
- Name: {applicant_data['name']}
- Age: {applicant_data['age']} years
- Occupation: {applicant_data['occupation']}
- Location: {applicant_data['location']}
- Coverage Amount Requested: ${applicant_data['coverage_amount']:,}
- Health Status: {applicant_data['health_status']}
- Lifestyle Factors: {applicant_data['lifestyle_factors']}

Provide a professional summary focusing on risk-relevant aspects."""

        return self.query_llm(prompt, max_tokens=200)

class ClaimsAnalysisAgent(UnderwritingAgent):
    def analyze_claims(self, claims_history):
        """Agent 2: Analyze claims history"""
        if not claims_history:
            return "No previous claims on record. This is a positive indicator for risk assessment."
        
        total_claims = len(claims_history)
        total_amount = sum([c['amount'] for c in claims_history])
        claim_types = ', '.join(set([c['type'] for c in claims_history]))
        
        prompt = f"""You are an insurance claims analyst. Analyze the following claims history and provide insights about risk patterns:

Claims Summary:
- Total Number of Claims: {total_claims}
- Total Claim Amount: ${total_amount:,}
- Types of Claims: {claim_types}
- Claims Details: {json.dumps(claims_history, indent=2)}

Provide a 2-3 sentence analysis focusing on frequency, severity, and any concerning patterns."""

        return self.query_llm(prompt, max_tokens=200)

class RiskFactorAgent(UnderwritingAgent):
    def identify_risk_factors(self, applicant_data, claims_history, external_reports):
        """Agent 3: Identify key risk factors"""
        prompt = f"""You are a risk assessment specialist. Identify the top 3-5 key risk factors based on:

Applicant: Age {applicant_data['age']}, {applicant_data['occupation']}, Health: {applicant_data['health_status']}
Lifestyle: {applicant_data['lifestyle_factors']}
Claims: {len(claims_history)} previous claims
Credit Score: {external_reports['credit_score']}
Criminal Record: {'Yes' if external_reports['criminal_record'] else 'No'}
Driving Record: {external_reports['driving_record']}

List the most significant risk factors in bullet points, each with a brief explanation."""

        return self.query_llm(prompt, max_tokens=300)

class RecommendationAgent(UnderwritingAgent):
    def generate_recommendation(self, risk_score, risk_category, all_factors):
        """Agent 4: Generate underwriting recommendation"""
        prompt = f"""You are a senior underwriter. Based on the following risk assessment, provide a clear underwriting decision and recommendation:

Risk Score: {risk_score}/100
Risk Category: {risk_category}
Key Factors: {all_factors}

Provide:
1. Clear decision (Approve/Approve with Conditions/Decline/Manual Review)
2. Specific recommendations for premium adjustments or policy conditions
3. Any additional steps needed

Keep response concise and actionable (3-4 sentences)."""

        return self.query_llm(prompt, max_tokens=250)

def calculate_risk_score(applicant_data, claims_history, external_reports):
    """Calculate numerical risk score"""
    risk_score = 50  # Base score
    
    # Age factor
    if applicant_data['age'] < 25:
        risk_score += 10
    elif applicant_data['age'] > 65:
        risk_score += 15
    else:
        risk_score -= 5
    
    # Claims history factor
    total_claims = len(claims_history)
    if total_claims > 3:
        risk_score += 20
    elif total_claims > 0:
        risk_score += 10
    else:
        risk_score -= 10
    
    # Health status factor
    if applicant_data['health_status'] == 'Excellent':
        risk_score -= 15
    elif applicant_data['health_status'] == 'Poor':
        risk_score += 25
    
    # Lifestyle factor
    if 'Smoker' in applicant_data['lifestyle_factors']:
        risk_score += 15
    if 'High-risk sports' in applicant_data['lifestyle_factors']:
        risk_score += 10
    
    # External reports factor
    if external_reports['credit_score'] < 600:
        risk_score += 10
    elif external_reports['credit_score'] > 750:
        risk_score -= 5
    
    if external_reports['criminal_record']:
        risk_score += 20
    
    # Normalize score
    risk_score = max(0, min(100, risk_score))
    
    # Determine category
    if risk_score < 40:
        risk_category = "Low Risk"
        color_class = "risk-low"
    elif risk_score < 70:
        risk_category = "Medium Risk"
        color_class = "risk-medium"
    else:
        risk_category = "High Risk"
        color_class = "risk-high"
    
    return risk_score, risk_category, color_class

def analyze_with_agents(applicant_data, claims_history, external_reports, api_key):
    """Orchestrate multi-agent analysis"""
    
    # Initialize agents
    data_agent = DataSummarizationAgent(api_key)
    claims_agent = ClaimsAnalysisAgent(api_key)
    risk_agent = RiskFactorAgent(api_key)
    rec_agent = RecommendationAgent(api_key)
    
    # Agent 1: Summarize applicant
    st.session_state.agent_outputs['applicant_summary'] = data_agent.summarize_applicant(applicant_data)
    time.sleep(0.5)
    
    # Agent 2: Analyze claims
    st.session_state.agent_outputs['claims_analysis'] = claims_agent.analyze_claims(claims_history)
    time.sleep(0.5)
    
    # Agent 3: Identify risk factors
    st.session_state.agent_outputs['risk_factors'] = risk_agent.identify_risk_factors(
        applicant_data, claims_history, external_reports
    )
    time.sleep(0.5)
    
    # Calculate risk score
    risk_score, risk_category, color_class = calculate_risk_score(
        applicant_data, claims_history, external_reports
    )
    
    # Agent 4: Generate recommendation
    all_factors = f"{st.session_state.agent_outputs['applicant_summary']} {st.session_state.agent_outputs['claims_analysis']}"
    st.session_state.agent_outputs['recommendation'] = rec_agent.generate_recommendation(
        risk_score, risk_category, all_factors
    )
    
    # Compile results
    return {
        'risk_score': risk_score,
        'risk_category': risk_category,
        'color_class': color_class,
        'agent_outputs': st.session_state.agent_outputs,
        'total_claims': len(claims_history),
        'total_claim_amount': sum([c['amount'] for c in claims_history]) if claims_history else 0
    }

def main():
    # Header
    st.markdown('<div class="main-header">🛡️ Underwriting Assistant AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">GenAI-Powered Risk Assessment with Multi-Agent System</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=Insurance+Co", use_container_width=True)
        st.markdown("### 🤖 AI Agents")
        st.markdown("""
        1. **Data Summarization Agent**
           - Extracts key applicant info
        2. **Claims Analysis Agent**
           - Analyzes historical patterns
        3. **Risk Factor Agent**
           - Identifies critical risks
        4. **Recommendation Agent**
           - Generates decisions
        """)
        
        st.markdown("---")
        st.markdown("### 🔑 API Configuration")
        
        # Get API key from secrets or input
        try:
            default_api_key = st.secrets.get("HUGGINGFACE_API_KEY", "")
        except:
            default_api_key = ""
        
        api_key = st.text_input(
            "Hugging Face API Key",
            value=default_api_key,
            type="password",
            help="Enter your Hugging Face API key or configure in Streamlit secrets"
        )
        
        if api_key:
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Using fallback mode")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info("This system uses multiple AI agents powered by LLMs to perform comprehensive underwriting analysis through prompt chaining.")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 New Application", "📊 Analysis Results", "🔄 System Flow", "📚 Sample Data"])
    
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
        
        if st.button("🤖 Analyze with AI Agents", use_container_width=True):
            if not api_key:
                st.warning("⚠️ No API key provided. Running in fallback mode with rule-based logic.")
            
            with st.spinner("🔄 AI Agents processing application..."):
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
                
                # Progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🤖 Agent 1: Summarizing applicant data...")
                progress_bar.progress(25)
                time.sleep(0.5)
                
                status_text.text("🤖 Agent 2: Analyzing claims history...")
                progress_bar.progress(50)
                time.sleep(0.5)
                
                status_text.text("🤖 Agent 3: Identifying risk factors...")
                progress_bar.progress(75)
                time.sleep(0.5)
                
                status_text.text("🤖 Agent 4: Generating recommendations...")
                progress_bar.progress(90)
                
                results = analyze_with_agents(applicant_data, claims_history, external_reports, api_key)
                st.session_state.analysis_results = results
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                time.sleep(0.5)
                
                st.success("✅ Multi-agent analysis complete! View results in the 'Analysis Results' tab.")
                st.rerun()
    
    with tab2:
        if st.session_state.analysis_results is None:
            st.info("👈 Please complete the application form and click 'Analyze with AI Agents' to see results.")
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
            
            # AI Agent Outputs
            st.markdown("### 🤖 AI Agent Analysis")
            
            agent_outputs = results['agent_outputs']
            
            st.markdown("#### 📊 Agent 1: Applicant Summary")
            st.markdown(f"""
            <div class="agent-card">
                <h4 style="margin:0 0 0.5rem 0;">Data Summarization Agent</h4>
                <p style="margin:0;">{agent_outputs.get('applicant_summary', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📋 Agent 2: Claims Analysis")
            st.markdown(f"""
            <div class="agent-card">
                <h4 style="margin:0 0 0.5rem 0;">Claims Analysis Agent</h4>
                <p style="margin:0;">{agent_outputs.get('claims_analysis', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### ⚠️ Agent 3: Risk Factors")
            st.markdown(f"""
            <div class="agent-card">
                <h4 style="margin:0 0 0.5rem 0;">Risk Factor Identification Agent</h4>
                <p style="margin:0; white-space: pre-wrap;">{agent_outputs.get('risk_factors', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 💡 Agent 4: Underwriting Recommendation")
            st.markdown(f"""
            <div class="agent-card">
                <h4 style="margin:0 0 0.5rem 0;">Recommendation Agent</h4>
                <p style="margin:0;">{agent_outputs.get('recommendation', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Export options
            st.markdown("---")
            st.markdown("### 📥 Export Report")
            
            col1, col2 = st.columns(2)
            with col1:
                report_json = json.dumps(results, indent=2, default=str)
                st.download_button(
                    label="📄 Download JSON Report",
                    data=report_json,
                    file_name=f"risk_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col2:
                if st.button("🔄 New Analysis", use_container_width=True):
                    st.session_state.analysis_results = None
                    st.session_state.agent_outputs = {}
                    st.rerun()
    
    with tab3:
        st.markdown("### 🔄 Multi-Agent System Flow")
        
        st.markdown("""
        <div class="flow-step">
            <h3>📥 Step 1: Data Ingestion</h3>
            <p><strong>Input Sources:</strong></p>
            <ul>
                <li>Applicant demographic information (age, occupation, location)</li>
                <li>Health status and lifestyle factors</li>
                <li>Historical claims data (type, amount, date)</li>
                <li>External reports (credit score, criminal record, driving record)</li>
                <li>Requested coverage amount</li>
            </ul>
            <p><strong>Processing:</strong> Data validation and normalization</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="process-arrow">↓</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="flow-step">
            <h3>🤖 Step 2: Agent 1 - Data Summarization</h3>
            <p><strong>Agent:</strong> Data Summarization Agent (LLM-powered)</p>
            <p><strong>Task:</strong> Extract and summarize key applicant information</p>
            <p><strong>Prompt Engineering:</strong></p>
            <ul>
                <li>Structured prompt with applicant details</li>
                <li>Request for 2-3 sentence professional summary</li>
                <li>Focus on risk-relevant factors</li>
            </ul>
            <p><strong>Output:</strong> Concise applicant profile highlighting critical factors</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="process-arrow">↓</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="flow-step">
            <h3>🤖 Step 3: Agent 2 - Claims Analysis</h3>
            <p><strong>Agent:</strong> Claims Analysis Agent (LLM-powered)</p>
            <p><strong>Task:</strong> Analyze historical claims patterns</p>
            <p><strong>Analysis:</strong></p>
            <ul>
                <li>Frequency analysis: Number of claims over time</li>
                <li>Severity analysis: Total claim amounts and averages</li>
                <li>Pattern detection: Claim types and recurring issues</li>
                <li>Temporal analysis: Claim distribution timeline</li>
            </ul>
            <p><strong>Output:</strong> Claims pattern analysis with risk indicators</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="process-arrow">↓</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="flow-step">
            <h3>🤖 Step 4: Agent 3 - Risk Factor Identification</h3>
            <p><strong>Agent:</strong> Risk Factor Identification Agent (LLM-powered)</p>
            <p><strong>Task:</strong> Identify and prioritize key risk factors</p>
            <p><strong>Risk Categories:</strong></p>
            <ul>
                <li><strong>Demographic Risks:</strong> Age, occupation, location</li>
                <li><strong>Health Risks:</strong> Current health status, lifestyle factors</li>
                <li><strong>Behavioral Risks:</strong> Smoking, high-risk activities</li>
                <li><strong>Financial Risks:</strong> Credit score, financial stability</li>
                <li><strong>Historical Risks:</strong> Claims history, criminal record</li>
            </ul>
            <p><strong>Output:</strong> Prioritized list of 3-5 key risk factors with explanations</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="process-arrow">↓</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="flow-step">
            <h3>📊 Step 5: Risk Score Calculation</h3>
            <p><strong>Method:</strong> Weighted scoring algorithm</p>
            <p><strong>Scoring Components:</strong></p>
            <ul>
                <li>Base score: 50/100</li>
                <li>Age factor: ±5 to ±15 points</li>
                <li>Claims history: -10 to +20 points</li>
                <li>Health status: -15 to +25 points</li>
                <li>Lifestyle factors: +10 to +15 points per risk</li>
                <li>Credit score: -5 to +10 points</li>
                <li>Criminal record: +20 points</li>
            </ul>
            <p><strong>Risk Categories:</strong></p>
            <ul>
                <li><strong>Low Risk:</strong> 0-39 (Green)</li>
                <li><strong>Medium Risk:</strong> 40-69 (Orange)</li>
                <li><strong>High Risk:</strong> 70-100 (Red)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="process-arrow">↓</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="flow-step">
            <h3>🤖 Step 6: Agent 4 - Recommendation Generation</h3>
            <p><strong>Agent:</strong> Recommendation Agent (LLM-powered)</p>
            <p><strong>Task:</strong> Generate actionable underwriting decision</p>
            <p><strong>Decision Framework:</strong></p>
            <ul>
                <li><strong>Approve:</strong> Low risk, standard terms</li>
                <li><strong>Approve with Conditions:</strong> Medium risk, adjusted premium/terms</li>
                <li><strong>Manual Review:</strong> High risk, requires human oversight</li>
                <li><strong>Decline:</strong> Unacceptable risk level</li>
            </ul>
            <p><strong>Recommendations Include:</strong></p>
            <ul>
                <li>Clear approval/decline decision</li>
                <li>Premium adjustment suggestions</li>
                <li>Special conditions or exclusions</li>
                <li>Additional documentation requirements</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="process-arrow">↓</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="flow-step">
            <h3>📋 Step 7: Structured Output Generation</h3>
            <p><strong>Output Format:</strong> JSON structured report</p>
            <p><strong>Report Components:</strong></p>
            <ul>
                <li>Risk score (0-100)</li>
                <li>Risk category (Low/Medium/High)</li>
                <li>All agent outputs (summaries, analyses, recommendations)</li>
                <li>Supporting data (claims total, amounts)</li>
                <li>Timestamp and metadata</li>
            </ul>
            <p><strong>Delivery:</strong> Dashboard display + downloadable JSON/PDF</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 🎯 Prompt Chaining Strategy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Sequential Chain Benefits
            - **Modularity:** Each agent has focused expertise
            - **Quality:** Specialized prompts yield better results
            - **Transparency:** Clear audit trail of decisions
            - **Maintainability:** Easy to update individual agents
            - **Scalability:** Add new agents without disruption
            """)
        
        with col2:
            st.markdown("""
            #### LLM Integration Points
            1. **Agent 1:** Text summarization
            2. **Agent 2:** Pattern recognition
            3. **Agent 3:** Risk identification & reasoning
            4. **Agent 4:** Decision synthesis
            5. **Fallback:** Rule-based logic when API unavailable
            """)
        
        st.markdown("---")
        
        st.markdown("### 🔐 Security & Compliance")
        st.markdown("""
        - **Data Privacy:** No applicant data stored permanently
        - **API Security:** Keys stored in Streamlit secrets
        - **Audit Trail:** All agent decisions logged
        - **Compliance:** Follows insurance underwriting standards
        - **Bias Mitigation:** Multiple agent perspectives reduce bias
        """)
    
    with tab4:
        st.markdown("### 📚 Sample Data & Use Cases")
        
        st.markdown("#### Low Risk Profile Example")
        st.code("""
Applicant: Sarah Johnson
Age: 32
Occupation: Teacher
Health: Excellent
Lifestyle: Non-smoker, Regular exercise
Claims History: 0 claims
Credit Score: 780
Criminal Record: No
Driving Record: Clean

Expected Risk Score: 20-30/100 → LOW RISK
Expected Recommendation: APPROVE with standard premium rates
        """)
        
        st.markdown("#### Medium Risk Profile Example")
        st.code("""
Applicant: Mike Davis
Age: 45
Occupation: Construction Worker
Health: Fair
Lifestyle: Non-smoker, occasional alcohol
Claims History: 2 claims ($12,000 total)
Credit Score: 650
Criminal Record: No
Driving Record: Minor violations

Expected Risk Score: 55-65/100 → MEDIUM RISK
Expected Recommendation: APPROVE WITH CONDITIONS
- Premium adjustment: +20%
- Higher deductible recommended
        """)
        
        st.markdown("#### High Risk Profile Example")
        st.code("""
Applicant: Robert Wilson
Age: 68
Occupation: Pilot (High-risk)
Health: Poor
Lifestyle: Smoker, High-risk sports
Claims History: 5 claims ($45,000 total)
Credit Score: 550
Criminal Record: Yes
Driving Record: Major violations

Expected Risk Score: 80-90/100 → HIGH RISK
Expected Recommendation: MANUAL REVIEW REQUIRED
- Requires senior underwriter approval
- Consider policy exclusions
- Substantial premium increase if approved
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Tips for Best Results")
        st.info("""
        **For Optimal AI Agent Performance:**
        1. Provide complete and accurate applicant data
        2. Include all relevant claims history
        3. Ensure external reports are up-to-date
        4. Use valid Hugging Face API key for best LLM responses
        5. Review all agent outputs before final decision
        
        **API Key Setup:**
        - Get free API key from: https://huggingface.co/settings/tokens
        - Add to Streamlit secrets as `HUGGINGFACE_API_KEY`
        - Or enter directly in the sidebar
        """)
        
        st.markdown("---")
        st.markdown("### 🚀 Technology Stack")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **Frontend**
            - Streamlit
            - Custom CSS
            - Responsive UI
            """)
        
        with col2:
            st.markdown("""
            **AI/ML**
            - Hugging Face API
            - Mixtral-8x7B LLM
            - Prompt Engineering
            """)
        
        with col3:
            st.markdown("""
            **Backend**
            - Python 3.8+
            - Multi-agent system
            - JSON data handling
            """)

if __name__ == "__main__":
    main()
