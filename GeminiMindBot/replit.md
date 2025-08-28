# مساعد عملاء 3QRab الذكي - Voice-Enabled Customer Service Bot

## Overview

This is a voice-enabled Arabic customer service chatbot for "3QRab" built with Streamlit that integrates with Google's Gemini API. The application serves as an intelligent customer service representative that can handle customer inquiries about products, shipping, payments, and returns in Arabic. It features voice capabilities, conversation memory, question analysis, and real-time analytics. Customers can speak their questions in Arabic or type them, and receive spoken responses.

## User Preferences

- Preferred communication style: Simple, everyday language
- Business: 3QRab customer service
- Language: Arabic interface and responses
- Role: Customer service representative bot

## System Architecture

### Frontend Architecture
- **Streamlit Web Interface**: Single-page application with real-time chat interface
- **Voice Integration**: Text-to-speech and speech-to-text capabilities using Web Speech APIs
- **Custom Dark Theme**: Modern dark theme with coral/red accent colors for better user experience
- **Session State Management**: Persistent conversation state using Streamlit's session management
- **Sidebar Analytics**: Real-time conversation metrics and memory summaries
- **Responsive Layout**: Wide layout configuration for optimal user experience

### Backend Architecture
- **Modular Component Design**: Separated into specialized classes for different functionalities
  - `ChatBot`: Core conversation handling and Gemini API integration with Arabic customer service instructions
  - `ConversationMemory`: Persistent memory management with JSON file storage
  - `QuestionAnalyzer`: Intent and sentiment analysis using Gemini Pro model
- **Customer Service Knowledge Base**: Integrated business information including:
  - Product catalog (Carbon black watch - 400 EGP)
  - Payment methods (Cash on delivery)
  - Shipping policies (Free shipping over 500 EGP, 3-4 days delivery)
  - Return policies (7-day exchange period)
  - Contact information for complex inquiries
- **Context-Aware Responses**: Integration of conversation history and question analysis into response generation
- **Memory Optimization**: Configurable interaction limits (default 20) to manage memory usage

### Data Storage Solutions
- **File-Based Persistence**: Local JSON file storage for conversation memory
- **Session-Based Storage**: Temporary conversation state in Streamlit session
- **Memory Management**: Automatic pruning of old interactions to maintain performance

### AI Model Integration
- **Dual Model Strategy**: 
  - Gemini 2.5 Flash for main conversation responses (optimized for speed)
  - Gemini 2.5 Pro for detailed question analysis (optimized for accuracy)
- **System Instructions**: Customized prompts for different AI functions
- **Context Injection**: Dynamic integration of conversation history and analysis into prompts

### Voice Capabilities
- **Speech-to-Text**: Real-time voice input using browser's Web Speech Recognition API
- **Text-to-Speech**: Automatic spoken responses using Web Speech Synthesis API
- **Voice Controls**: Play/stop controls for managing audio output
- **Multi-Modal Input**: Support for both voice and text input simultaneously

### Analytics and Monitoring
- **Real-Time Metrics**: Live conversation statistics and user engagement tracking
- **Question Analysis**: Automatic extraction of intent, sentiment, topic, complexity, and keywords
- **Memory Summarization**: Intelligent conversation context summaries

## External Dependencies

### AI Services
- **Google Gemini API**: Primary AI service for conversation and analysis
  - Requires `GEMINI_API_KEY` environment variable
  - Uses both Flash and Pro model variants

### Python Libraries
- **Streamlit**: Web application framework for the user interface and voice integration
- **Google GenAI**: Official Google client library for Gemini API integration
- **Streamlit Components**: Custom HTML/JavaScript components for voice functionality
- **Standard Libraries**: JSON for data serialization, datetime for timestamps, os for environment variables, logging for error handling

### Environment Configuration
- **API Key Management**: Secure environment variable handling for Gemini API access
- **Error Handling**: Comprehensive validation for missing API credentials