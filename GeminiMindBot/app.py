import streamlit as st
from datetime import datetime
from chatbot import ChatBot
from memory import ConversationMemory
from analyzer import QuestionAnalyzer

# Initialize session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatBot()
    st.session_state.memory = ConversationMemory()
    st.session_state.analyzer = QuestionAnalyzer()
    st.session_state.messages = []
    st.session_state.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# Page configuration
st.set_page_config(page_title="مساعد عملاء 3QRab",
                   page_icon="⌚",
                   layout="centered")

# Custom CSS + Navbar
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    * {
        font-family: 'Cairo', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    .stApp {
        font-family: 'Cairo', sans-serif !important;
        padding-top: 80px !important;
    }
    .fixed-navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 15px 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e0e0e0;
    }
    .navbar-title {
        color: #000000;
        font-weight: 600;
        font-size: 1.5rem;
        font-family: 'Cairo', sans-serif;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .navbar-button, .navbar-home {
        background: linear-gradient(45deg, #000000, #333333);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: none;
        font-size: 14px;
        font-family: 'Cairo', sans-serif;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .navbar-button:hover, .navbar-home:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        text-decoration: none;
        color: white;
    }
</style>
<navbar>
<a href="https://3qrab.netlify.app/" target="_blank" style="
    display: inline-block;
    background: linear-gradient(45deg, #000000, #333333);
    color: white;
    padding: 12px 30px;
    border-radius: 25px;
    text-decoration: none;
    font-weight: 600;
    margin: 0 10px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    font-size: 16px;
">
    ↗ زيارة المتجر الرئيسي
</a>
</navbar>

""",
            unsafe_allow_html=True)

# Welcome section
st.markdown("""
<div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
    <h1 style="color: #000000; font-weight: 600; margin: 0 0 1rem 0; font-size: 2.5rem;">أهلاً بك في متجر 3QRab</h1>
    <p style="color: #666666; font-size: 1.1rem; margin: 1rem 0; font-weight: 400;">
        أنا موسي، مساعدك الذكي • يسعدني مساعدتك في كل احتياجاتك ⌚
    </p>
    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 1.5rem;">
        <span style="background: #f0f0f0; padding: 8px 16px; border-radius: 20px; color: #333; font-size: 14px;">💬 دردشة ذكية</span>
        <span style="background: #f0f0f0; padding: 8px 16px; border-radius: 20px; color: #333; font-size: 14px;">🤖 تقنية AI</span>
        <span style="background: #f0f0f0; padding: 8px 16px; border-radius: 20px; color: #333; font-size: 14px;">⚡ ردود سريعة</span>
    </div>
</div>
""",
            unsafe_allow_html=True)

# Call to action button
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <a href="https://3qrab.netlify.app/" target="_blank" style="
        display: inline-block;
        background: linear-gradient(45deg, #000000, #333333);
        color: white;
        padding: 15px 40px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        font-size: 18px;
        font-family: 'Cairo', sans-serif;
        margin: 20px 0;
    ">
        ↗ زيارة المتجر الرئيسي
    </a>
</div>
""",
            unsafe_allow_html=True)

# Clear conversation button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🗑️ مسح المحادثة", use_container_width=True,
                 type="secondary"):
        st.session_state.messages = []
        st.session_state.memory.clear_memory()
        st.session_state.conversation_id = datetime.now().strftime(
            "%Y%m%d_%H%M%S")
        st.rerun()

# Chat interface
st.markdown("""
<div style="background: white; border-radius: 15px; padding: 1.5rem; margin: 2rem 0; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;">
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h3 style="color: #000000; font-weight: 500; margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">
            <span style="background: linear-gradient(45deg, #000000, #333333); color: white; padding: 8px 12px; border-radius: 50%; font-size: 16px;">⌚</span>
            محادثة مع موسي
        </h3>
        <p style="color: #666; margin: 0.5rem 0 0 0; font-size: 14px;">مساعد ذكي لمتجر 3QRab • خبير في خدمة العملاء</p>
    </div>
</div>
""",
            unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 1.2rem; border-radius: 15px; margin: 1rem 0; border-left: 4px solid #000000; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span style="background: #000000; color: white; padding: 6px 10px; border-radius: 50%; font-size: 14px;">👤</span>
                <strong style="color: #000000; font-weight: 600;">أنت</strong>
            </div>
            <div style="color: #333333; padding-left: 40px; line-height: 1.6;">{message["content"]}</div>
        </div>
        """,
                    unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); padding: 1.2rem; border-radius: 15px; margin: 1rem 0; border: 1px solid #e0e0e0; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span style="background: linear-gradient(45deg, #000000, #333333); color: white; padding: 6px 10px; border-radius: 50%; font-size: 14px;">⌚</span>
                <strong style="color: #000000; font-weight: 600;">موسي</strong>
                <span style="background: #f0f0f0; color: #666; padding: 2px 8px; border-radius: 10px; font-size: 12px;">مساعد ذكي</span>
            </div>
            <div style="color: #333333; padding-left: 40px; line-height: 1.6;">{message["content"]}</div>
        </div>
        """,
                    unsafe_allow_html=True)

# Chat input
prompt = st.chat_input("💬 مرحباً! اكتب سؤالك أو استفسارك هنا...")

if prompt:
    timestamp = datetime.now().isoformat()
    analysis = {
        "intent": "question",
        "sentiment": "neutral",
        "topic": "general",
        "complexity": "moderate",
        "keywords": []
    }

    user_message = {
        "role": "user",
        "content": prompt,
        "timestamp": timestamp,
        "analysis": analysis
    }
    st.session_state.messages.append(user_message)

    # Display user message
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 1.2rem; border-radius: 15px; margin: 1rem 0; border-left: 4px solid #000000; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <span style="background: #000000; color: white; padding: 6px 10px; border-radius: 50%; font-size: 14px;">👤</span>
            <strong style="color: #000000; font-weight: 600;">أنت</strong>
        </div>
        <div style="color: #333333; padding-left: 40px; line-height: 1.6;">{prompt}</div>
    </div>
    """,
                unsafe_allow_html=True)

    # Generate response
    with st.spinner("🤔 جاري التفكير..."):
        try:
            context = st.session_state.memory.get_context()
            response = st.session_state.chatbot.generate_response(
                prompt, context=context, analysis=analysis)

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); padding: 1.2rem; border-radius: 15px; margin: 1rem 0; border: 1px solid #e0e0e0; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                    <span style="background: linear-gradient(45deg, #000000, #333333); color: white; padding: 6px 10px; border-radius: 50%; font-size: 14px;">⌚</span>
                    <strong style="color: #000000; font-weight: 600;">موسي</strong>
                    <span style="background: #f0f0f0; color: #666; padding: 2px 8px; border-radius: 10px; font-size: 12px;">مساعد ذكي</span>
                </div>
                <div style="color: #333333; padding-left: 40px; line-height: 1.6;">{response}</div>
            </div>
            """,
                        unsafe_allow_html=True)

            assistant_message = {
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.messages.append(assistant_message)
            st.session_state.memory.add_interaction(
                user_input=prompt,
                assistant_response=response,
                timestamp=timestamp,
                analysis=analysis)
        except Exception as e:
            error_msg = f"عذراً، حدث خطأ: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({
                "role":
                "assistant",
                "content":
                error_msg,
                "timestamp":
                datetime.now().isoformat()
            })

# Footer
st.markdown("""

  
    <p style="color: #999999; margin-top: 1.5rem; font-size: 0.85rem; font-weight: 500;">
        مدعوم بتقنية الذكاء الاصطناعي • موسي المساعد الذكي • 3QRab © 2025
    </p>
</div>
""",
            unsafe_allow_html=True)
