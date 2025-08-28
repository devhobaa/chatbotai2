import os
from google import genai
from google.genai import types
import json
import logging
from typing import Optional

class ChatBot:
    """Main chatbot class that handles interactions with Gemini API"""
    
    def __init__(self):
        """Initialize the chatbot with Gemini API client"""
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        
        # System instruction for the chatbot
        self.system_instruction = (
            "أنت مساعد ذكي لمتجر '3QRab' واسمك موسي. "
            "تتحدث بشخصية ودودة ومتحمسة للتكنولوجيا. "
            
            "عن موسي (المساعد الذكي):\n"
            "• شخصيته: ودود، صبور، يحب مساعدة العملاء بوضوح وسهولة\n"
            "• شغفه: متخصص في خدمة العملاء ومساعدتهم في كل احتياجاتهم\n"
            "• مهارته: خبير في منتجات المتجر وسياسات الخدمة\n"
            "• رؤيته: تقديم تجربة تسوق سهلة وممتعة لكل عميل\n"
            "• أسلوبه: يستمع جيداً، يرد بسرعة، يقدم حلول عملية\n"
            
            "معلومات المتجر:\n"
            "• المنتجات: ساعة كربون أسود بـ 400 جنيه مصري\n"
            "• الدفع: نقداً عند الاستلام\n"
            "• الشحن: مجاني للطلبات +500 جنيه، التوصيل 3-4 أيام\n"
            "• الإرجاع: 7 أيام للاستبدال، 3 أيام لاسترداد المبلغ\n"
            "• التواصل: 010-26897739 أو ehab.hussein.dev@gmail.com\n"
            
            "كيف ترد (بشخصية موسي):\n"
            "1. اسأل عن اسم العميل بودية: 'أهلاً بك! أنا موسي مساعد المتجر، ممكن أعرف اسمك؟'\n"
            "2. استخدم اسم العميل واجعله يشعر بالترحيب الشخصي\n"
            "3. أضف لمسة شخصية: 'يسعدني أن أساعدك!' أو 'كوني جزء من عائلة 3QRab!'\n"
            "4. اربط بشغف التكنولوجيا عند المناسب: 'أحب تجربة تقنيات AI جديدة لخدمتك!'\n"
            "5. لتتبع الطلبات: 'أهلاً [الاسم]! يمكنك تتبع طلبك: https://3qrab.netlify.app/track-order?phone=01026897739'\n"
            "6. كن صبوراً ومتفهماً واستمع لاحتياجات العميل\n"
            "7. قدم تجربة شخصية فريدة لكل عميل\n"
            
            "تحدث بروح موسي المتحمسة والودودة دائماً! ⌚"
        )
    
    def generate_response(self, user_input: str, context: str = "", analysis: Optional[dict] = None) -> str:
        """
        Generate a response using Gemini API with conversation context
        
        Args:
            user_input: The user's current message
            context: Previous conversation context from memory
            analysis: Question analysis data
            
        Returns:
            Generated response from the AI
        """
        try:
            # Prepare the prompt with context and analysis
            prompt_parts = []
            
            if context:
                prompt_parts.append(f"Previous conversation context:\n{context}\n")
            
            if analysis:
                analysis_text = self._format_analysis(analysis)
                prompt_parts.append(f"Question analysis:\n{analysis_text}\n")
            
            prompt_parts.append(f"Current user message: {user_input}")
            
            full_prompt = "\n".join(prompt_parts)
            
            # Generate response using Gemini
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Content(
                        role="user", 
                        parts=[types.Part(text=full_prompt)]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.7,
                    max_output_tokens=1000
                )
            )
            
            if response.text:
                return response.text.strip()
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            return f"I encountered an error while processing your request: {str(e)}"
    
    def _format_analysis(self, analysis: dict) -> str:
        """Format the question analysis for inclusion in the prompt"""
        if not analysis:
            return "No analysis available."
        
        formatted = []
        for key, value in analysis.items():
            formatted.append(f"- {key.capitalize()}: {value}")
        
        return "\n".join(formatted)
    
    def test_connection(self) -> bool:
        """Test if the Gemini API connection is working"""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents="Hello, this is a test message."
            )
            return bool(response.text)
        except Exception as e:
            logging.error(f"API connection test failed: {str(e)}")
            return False
