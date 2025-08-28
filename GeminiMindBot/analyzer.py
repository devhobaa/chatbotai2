import os
from google import genai
from google.genai import types
import json
import logging
from typing import Dict, Any, List

class QuestionAnalyzer:
    """Analyzes user questions to extract intent, sentiment, and other metadata"""
    
    def __init__(self):
        """Initialize the question analyzer with Gemini API client"""
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-pro"  # Using pro model for better analysis
        
        # System instruction for question analysis
        self.system_instruction = (
            "You are an expert at analyzing user questions and messages. "
            "Analyze the given text and provide structured information about "
            "the user's intent, sentiment, topic, and complexity level. "
            "Be precise and concise in your analysis."
        )
    
    def analyze_question(self, question: str) -> Dict[str, Any]:
        """
        Analyze a user's question to extract metadata
        
        Args:
            question: The user's question or message
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Create analysis prompt
            analysis_prompt = f"""
            Analyze the following user message and provide a JSON response with these fields:
            - intent: The user's primary intent (e.g., "question", "request", "greeting", "complaint", "compliment")
            - sentiment: The emotional tone (e.g., "positive", "negative", "neutral", "curious", "frustrated")
            - topic: The main topic or subject area (e.g., "technology", "health", "general", "personal")
            - complexity: The complexity level (e.g., "simple", "moderate", "complex")
            - keywords: Array of 3-5 key terms from the message
            
            User message: "{question}"
            
            Respond only with valid JSON.
            """
            
            # Generate analysis using Gemini
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Content(
                        role="user", 
                        parts=[types.Part(text=analysis_prompt)]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    response_mime_type="application/json",
                    temperature=0.3  # Lower temperature for more consistent analysis
                )
            )
            
            if response.text:
                try:
                    analysis_data = json.loads(response.text)
                    return self._validate_analysis(analysis_data)
                except json.JSONDecodeError as e:
                    logging.error(f"Failed to parse analysis JSON: {str(e)}")
                    return self._create_smart_fallback_analysis(question)
            else:
                return self._create_smart_fallback_analysis(question)
                
        except Exception as e:
            logging.error(f"Error analyzing question: {e}")
            # Create basic analysis based on the question content
            return self._create_smart_fallback_analysis(question)
    
    def _validate_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean the analysis data
        
        Args:
            analysis: Raw analysis data from Gemini
            
        Returns:
            Validated analysis data
        """
        validated = {}
        
        # Validate intent
        valid_intents = ["question", "request", "greeting", "complaint", "compliment", "information", "help"]
        validated["intent"] = analysis.get("intent", "question").lower()
        if validated["intent"] not in valid_intents:
            validated["intent"] = "question"
        
        # Validate sentiment
        valid_sentiments = ["positive", "negative", "neutral", "curious", "frustrated", "excited"]
        validated["sentiment"] = analysis.get("sentiment", "neutral").lower()
        if validated["sentiment"] not in valid_sentiments:
            validated["sentiment"] = "neutral"
        
        # Validate complexity
        valid_complexities = ["simple", "moderate", "complex"]
        validated["complexity"] = analysis.get("complexity", "moderate").lower()
        if validated["complexity"] not in valid_complexities:
            validated["complexity"] = "moderate"
        
        # Validate topic
        validated["topic"] = analysis.get("topic", "general").lower()
        
        # Validate keywords
        keywords = analysis.get("keywords", [])
        if isinstance(keywords, list):
            validated["keywords"] = keywords[:5]  # Limit to 5 keywords
        else:
            validated["keywords"] = []
        
        return validated
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """
        Get default analysis when analysis fails
        
        Returns:
            Default analysis structure
        """
        return {
            "intent": "question",
            "sentiment": "neutral",
            "topic": "general",
            "complexity": "moderate",
            "keywords": []
        }
    
    def _create_smart_fallback_analysis(self, question: str) -> Dict[str, Any]:
        """
        Create intelligent fallback analysis based on keywords
        
        Args:
            question: The user's question
            
        Returns:
            Smart analysis based on content
        """
        question_lower = question.lower()
        
        # Detect intent based on keywords
        intent = "question"
        if any(word in question_lower for word in ["ساعة", "منتج", "سعر", "شراء", "اشتري"]):
            intent = "information"
        elif any(word in question_lower for word in ["أهلاً", "السلام", "مرحباً", "صباح"]):
            intent = "greeting"
        elif any(word in question_lower for word in ["طلب", "تتبع", "وصل", "شحن"]):
            intent = "request"
        elif any(word in question_lower for word in ["مشكلة", "شكوى", "خطأ", "غلط"]):
            intent = "complaint"
        elif any(word in question_lower for word in ["شكراً", "ممتاز", "رائع"]):
            intent = "compliment"
        elif any(word in question_lower for word in ["مساعدة", "ساعدني", "كيف"]):
            intent = "help"
        
        # Detect sentiment
        sentiment = "neutral"
        if any(word in question_lower for word in ["شكراً", "ممتاز", "رائع", "جيد", "أحب"]):
            sentiment = "positive"
        elif any(word in question_lower for word in ["سيء", "مشكلة", "غاضب", "محبط", "زعلان"]):
            sentiment = "negative"
        elif any(word in question_lower for word in ["؟", "كيف", "ماذا", "متى", "أين"]):
            sentiment = "curious"
        
        # Detect topic
        topic = "general"
        if any(word in question_lower for word in ["ساعة", "منتج"]):
            topic = "product"
        elif any(word in question_lower for word in ["شحن", "توصيل", "طلب"]):
            topic = "shipping"
        elif any(word in question_lower for word in ["دفع", "فلوس", "سعر"]):
            topic = "payment"
        elif any(word in question_lower for word in ["إرجاع", "استبدال", "ضمان"]):
            topic = "returns"
        
        # Determine complexity
        complexity = "simple"
        if len(question) > 50 or question.count("؟") > 1:
            complexity = "moderate"
        if len(question) > 100 or any(word in question_lower for word in ["معقد", "صعب", "مشكلة كبيرة"]):
            complexity = "complex"
        
        # Extract basic keywords
        keywords = [word for word in question_lower.split() if len(word) > 2][:5]
        
        return {
            "intent": intent,
            "sentiment": sentiment,
            "topic": topic,
            "complexity": complexity,
            "keywords": keywords
        }
    
    def analyze_conversation_patterns(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze patterns across multiple interactions
        
        Args:
            interactions: List of conversation interactions with analysis data
            
        Returns:
            Pattern analysis results
        """
        if not interactions:
            return {}
        
        patterns = {
            "most_common_intent": {},
            "sentiment_distribution": {},
            "topic_frequency": {},
            "complexity_trend": [],
            "total_interactions": len(interactions)
        }
        
        for interaction in interactions:
            analysis = interaction.get("analysis", {})
            
            # Count intents
            intent = analysis.get("intent", "unknown")
            patterns["most_common_intent"][intent] = patterns["most_common_intent"].get(intent, 0) + 1
            
            # Count sentiments
            sentiment = analysis.get("sentiment", "unknown")
            patterns["sentiment_distribution"][sentiment] = patterns["sentiment_distribution"].get(sentiment, 0) + 1
            
            # Count topics
            topic = analysis.get("topic", "unknown")
            patterns["topic_frequency"][topic] = patterns["topic_frequency"].get(topic, 0) + 1
            
            # Track complexity trend
            complexity = analysis.get("complexity", "unknown")
            patterns["complexity_trend"].append(complexity)
        
        return patterns
