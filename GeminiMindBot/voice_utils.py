import streamlit as st
import streamlit.components.v1 as components


def add_voice_functionality():
    """Add text-to-speech and speech-to-text functionality using Web APIs"""
    
    # Text-to-speech JavaScript function
    tts_js = """
    <script>
    function speak(text) {
        if ('speechSynthesis' in window) {
            // Cancel any ongoing speech
            window.speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.8;
            utterance.pitch = 1;
            utterance.volume = 1;
            
            // Try to use a more natural voice if available
            const voices = window.speechSynthesis.getVoices();
            const preferredVoice = voices.find(voice => 
                voice.name.includes('Google') || 
                voice.name.includes('Microsoft') ||
                voice.lang.startsWith('en-')
            );
            
            if (preferredVoice) {
                utterance.voice = preferredVoice;
            }
            
            window.speechSynthesis.speak(utterance);
        } else {
            alert('Text-to-speech not supported in this browser');
        }
    }
    
    function stopSpeaking() {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
    }
    </script>
    """
    
    # Speech-to-text JavaScript function
    stt_js = """
    <script>
    let recognition;
    let isListening = false;
    
    function startListening() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
            
            recognition.onstart = function() {
                isListening = true;
                document.getElementById('listening-status').innerHTML = '🎤 Listening...';
                document.getElementById('voice-btn').innerHTML = '⏹️ Stop';
            };
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById('voice-input').value = transcript;
                
                // Trigger Streamlit to update
                const inputEvent = new Event('input', { bubbles: true });
                document.getElementById('voice-input').dispatchEvent(inputEvent);
            };
            
            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
                document.getElementById('listening-status').innerHTML = '❌ Error: ' + event.error;
            };
            
            recognition.onend = function() {
                isListening = false;
                document.getElementById('listening-status').innerHTML = '';
                document.getElementById('voice-btn').innerHTML = '🎤 Voice Input';
            };
            
            recognition.start();
        } else {
            alert('Speech recognition not supported in this browser');
        }
    }
    
    function toggleListening() {
        if (isListening) {
            recognition.stop();
        } else {
            startListening();
        }
    }
    </script>
    """
    
    # Render the JavaScript
    components.html(tts_js + stt_js, height=0)


def create_voice_input():
    """Create a voice input interface"""
    
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col1:
        # Voice input button
        voice_button_html = """
        <button id="voice-btn" onclick="toggleListening()" 
                style="
                    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                    border: none;
                    color: white;
                    padding: 10px 15px;
                    border-radius: 20px;
                    cursor: pointer;
                    font-size: 14px;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
                    margin-bottom: 10px;
                " 
                onmouseover="this.style.transform='scale(1.05)'"
                onmouseout="this.style.transform='scale(1)'"
        >🎤 Voice Input</button>
        <div id="listening-status" style="font-size: 12px; color: #FF6B6B; margin-top: 5px;"></div>
        """
        components.html(voice_button_html, height=80)
    
    with col2:
        # Hidden input for voice text
        voice_text = st.text_input("Voice Input", key="voice_input", placeholder="اضغط زر الصوت للتحدث أو اكتب هنا...", label_visibility="collapsed")
    
    with col3:
        st.write("")  # Empty space for alignment
    
    return voice_text


def speak_text(text):
    """Function to trigger text-to-speech"""
    if text:
        # Clean the text for JavaScript
        clean_text = text.replace('`', '').replace('"', "'").replace('\n', ' ').replace('\r', ' ')
        # Create a button to trigger speech
        speak_js = f"""
        <script>
        speak(`{clean_text}`);
        </script>
        """
        components.html(speak_js, height=0)


def create_voice_controls():
    """Create voice control buttons"""
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        voice_controls_html = """
        <div style="text-align: center; margin: 10px 0;">
            <button onclick="stopSpeaking()" 
                    style="
                        background: linear-gradient(45deg, #FF4757, #FF3742);
                        border: none;
                        color: white;
                        padding: 8px 16px;
                        border-radius: 15px;
                        cursor: pointer;
                        font-size: 12px;
                        margin: 0 5px;
                        transition: all 0.3s ease;
                        box-shadow: 0 2px 10px rgba(255, 71, 87, 0.3);
                    "
                    onmouseover="this.style.transform='scale(1.05)'"
                    onmouseout="this.style.transform='scale(1)'"
            >🔇 Stop Speaking</button>
        </div>
        """
        components.html(voice_controls_html, height=50)