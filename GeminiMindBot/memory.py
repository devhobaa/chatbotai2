import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import os

class ConversationMemory:
    """Manages conversation memory and context for the chatbot"""
    
    def __init__(self, max_interactions: int = 20):
        """
        Initialize conversation memory
        
        Args:
            max_interactions: Maximum number of interactions to store
        """
        self.max_interactions = max_interactions
        self.interactions: List[Dict[str, Any]] = []
        self.memory_file = "conversation_memory.json"
        self.load_memory()
    
    def add_interaction(self, user_input: str, assistant_response: str, 
                       timestamp: str, analysis: Optional[Dict] = None):
        """
        Add a new interaction to memory
        
        Args:
            user_input: User's message
            assistant_response: Assistant's response
            timestamp: Interaction timestamp
            analysis: Question analysis data
        """
        interaction = {
            "user_input": user_input,
            "assistant_response": assistant_response,
            "timestamp": timestamp,
            "analysis": analysis or {}
        }
        
        self.interactions.append(interaction)
        
        # Keep only the most recent interactions
        if len(self.interactions) > self.max_interactions:
            self.interactions = self.interactions[-self.max_interactions:]
        
        self.save_memory()
    
    def get_context(self, num_interactions: int = 5) -> str:
        """
        Get conversation context for the chatbot
        
        Args:
            num_interactions: Number of recent interactions to include
            
        Returns:
            Formatted context string
        """
        if not self.interactions:
            return ""
        
        # Get the most recent interactions
        recent_interactions = self.interactions[-num_interactions:]
        
        context_parts = []
        for interaction in recent_interactions:
            context_parts.append(f"User: {interaction['user_input']}")
            context_parts.append(f"Assistant: {interaction['assistant_response']}")
            context_parts.append("---")
        
        return "\n".join(context_parts)
    
    def get_memory_summary(self) -> str:
        """
        Generate a summary of the conversation memory
        
        Returns:
            Summary of key topics and themes
        """
        if not self.interactions:
            return ""
        
        # Extract topics and intents from analysis data
        topics = set()
        intents = set()
        
        for interaction in self.interactions:
            analysis = interaction.get("analysis", {})
            if "topic" in analysis:
                topics.add(analysis["topic"])
            if "intent" in analysis:
                intents.add(analysis["intent"])
        
        summary_parts = []
        
        if topics:
            summary_parts.append(f"Topics discussed: {', '.join(topics)}")
        
        if intents:
            summary_parts.append(f"User intents: {', '.join(intents)}")
        
        summary_parts.append(f"Total interactions: {len(self.interactions)}")
        
        return "\n".join(summary_parts)
    
    def get_interaction_count(self) -> int:
        """Get the total number of stored interactions"""
        return len(self.interactions)
    
    def clear_memory(self):
        """Clear all stored interactions"""
        self.interactions = []
        self.save_memory()
    
    def save_memory(self):
        """Save memory to a JSON file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.interactions, f, indent=2)
        except Exception as e:
            print(f"Failed to save memory: {str(e)}")
    
    def load_memory(self):
        """Load memory from a JSON file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    self.interactions = json.load(f)
        except Exception as e:
            print(f"Failed to load memory: {str(e)}")
            self.interactions = []
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """
        Extract user preferences from conversation history
        
        Returns:
            Dictionary of inferred user preferences
        """
        preferences = {
            "frequent_topics": {},
            "communication_style": "unknown",
            "complexity_preference": "unknown"
        }
        
        # Count topic frequencies
        for interaction in self.interactions:
            analysis = interaction.get("analysis", {})
            topic = analysis.get("topic")
            if topic:
                preferences["frequent_topics"][topic] = preferences["frequent_topics"].get(topic, 0) + 1
        
        # Analyze complexity preferences
        complexities = [interaction.get("analysis", {}).get("complexity") 
                       for interaction in self.interactions]
        complexities = [c for c in complexities if c]
        
        if complexities:
            # Most common complexity level
            complexity_counts = {}
            for c in complexities:
                complexity_counts[c] = complexity_counts.get(c, 0) + 1
            preferences["complexity_preference"] = max(complexity_counts.keys(), key=lambda x: complexity_counts[x])
        
        return preferences
