"""
Advanced AI Service
Integrates OpenAI API for intelligent features across the platform
"""

import os
import sys
sys.path.append('/home/ubuntu/fineguard-marketing')

from typing import Dict, List, Optional
from datetime import datetime
import json

# Import vault for API key
from api.vault.secret_manager import SecretVault


class AIService:
    """Advanced AI service using OpenAI API"""
    
    def __init__(self):
        # Get OpenAI API key from vault
        vault = SecretVault(master_password="fineguard_secure_2024")
        self.api_key = vault.get_secret("openai_api_key")
        
        # Initialize OpenAI client (lazy loading)
        self._client = None
    
    @property
    def client(self):
        """Lazy load OpenAI client"""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                print("⚠️  OpenAI library not installed. Install with: pip3 install openai")
                return None
        return self._client
    
    def generate_email_content(
        self,
        email_type: str,
        context: Dict
    ) -> Dict[str, str]:
        """
        Generate personalized email content using AI
        
        Args:
            email_type: Type of email (welcome, reminder, follow_up, proposal, etc.)
            context: Context data for personalization
            
        Returns:
            Dict with subject and body
        """
        
        if not self.client:
            return self._fallback_email(email_type, context)
        
        try:
            prompt = self._build_email_prompt(email_type, context)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional business communication expert for Devonshire Green, a UK accounting firm with 90+ years of experience."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            
            # Parse response (expecting JSON format)
            result = json.loads(content)
            
            return {
                "subject": result.get("subject", ""),
                "body": result.get("body", ""),
                "tone": result.get("tone", "professional")
            }
            
        except Exception as e:
            print(f"⚠️  AI email generation failed: {e}")
            return self._fallback_email(email_type, context)
    
    def analyze_company_sentiment(
        self,
        company_data: Dict
    ) -> Dict:
        """
        Analyze company data and provide sentiment analysis
        
        Args:
            company_data: Company information
            
        Returns:
            Sentiment analysis results
        """
        
        if not self.client:
            return self._fallback_sentiment(company_data)
        
        try:
            prompt = f"""
            Analyze the following company data and provide sentiment analysis:
            
            Company: {company_data.get('name')}
            Industry: {company_data.get('industry')}
            Turnover: £{company_data.get('annualTurnover', 0):,}
            Employees: {company_data.get('employees', 0)}
            Compliance Score: {company_data.get('complianceScore', 0)}%
            Risk Level: {company_data.get('riskLevel', 'unknown')}
            
            Provide:
            1. Overall sentiment (positive/neutral/negative)
            2. Key strengths (3-5 points)
            3. Key concerns (3-5 points)
            4. Recommendations (3-5 points)
            
            Return as JSON with keys: sentiment, strengths, concerns, recommendations
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a business analyst expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            return result
            
        except Exception as e:
            print(f"⚠️  AI sentiment analysis failed: {e}")
            return self._fallback_sentiment(company_data)
    
    def generate_proposal(
        self,
        lead_data: Dict,
        package: str
    ) -> str:
        """
        Generate personalized proposal using AI
        
        Args:
            lead_data: Lead information
            package: Package type (Starter/Professional/Enterprise)
            
        Returns:
            Generated proposal text
        """
        
        if not self.client:
            return self._fallback_proposal(lead_data, package)
        
        try:
            prompt = f"""
            Generate a professional proposal for accounting services:
            
            Client: {lead_data.get('companyName')}
            Industry: {lead_data.get('industry')}
            Package: {package}
            Recommended Services: {', '.join(lead_data.get('recommendedServices', []))}
            Potential Value: £{lead_data.get('potentialValue', 0):,}/year
            
            Create a compelling 3-paragraph proposal that:
            1. Acknowledges their specific needs
            2. Explains how our services will help
            3. Includes a clear call to action
            
            Keep it professional, concise, and persuasive.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a sales expert for Devonshire Green accounting services."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️  AI proposal generation failed: {e}")
            return self._fallback_proposal(lead_data, package)
    
    def chatbot_response(
        self,
        user_message: str,
        conversation_history: List[Dict] = None
    ) -> str:
        """
        Generate chatbot response for customer support
        
        Args:
            user_message: User's message
            conversation_history: Previous messages
            
        Returns:
            AI-generated response
        """
        
        if not self.client:
            return "I'm currently unavailable. Please contact us at admin@devonshiregreen.uk or call 01959 565 772."
        
        try:
            messages = [
                {"role": "system", "content": """You are a helpful customer support assistant for FineGuard, 
                a compliance and accounting platform powered by Devonshire Green (90+ years experience). 
                Be professional, helpful, and concise. If you don't know something, direct them to contact 
                admin@devonshiregreen.uk or call 01959 565 772."""}
            ]
            
            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history[-5:])  # Last 5 messages
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️  AI chatbot failed: {e}")
            return "I'm having trouble right now. Please contact us at admin@devonshiregreen.uk or call 01959 565 772."
    
    def summarize_document(
        self,
        document_text: str,
        max_length: int = 200
    ) -> str:
        """
        Summarize long documents using AI
        
        Args:
            document_text: Full document text
            max_length: Maximum summary length in words
            
        Returns:
            Summarized text
        """
        
        if not self.client:
            return document_text[:500] + "..."
        
        try:
            prompt = f"""
            Summarize the following document in {max_length} words or less:
            
            {document_text}
            
            Focus on key points and actionable insights.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at summarizing business documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=max_length * 2
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️  AI summarization failed: {e}")
            return document_text[:500] + "..."
    
    def predict_churn_risk(
        self,
        customer_data: Dict
    ) -> Dict:
        """
        Predict customer churn risk using AI
        
        Args:
            customer_data: Customer information
            
        Returns:
            Churn prediction with risk level and recommendations
        """
        
        if not self.client:
            return self._fallback_churn(customer_data)
        
        try:
            prompt = f"""
            Analyze customer churn risk based on:
            
            Last Contact: {customer_data.get('lastContactDate', 'Never')}
            Engagement Score: {customer_data.get('engagementScore', 0)}/100
            Payment History: {customer_data.get('paymentHistory', 'Unknown')}
            Support Tickets: {customer_data.get('supportTickets', 0)}
            Satisfaction: {customer_data.get('satisfaction', 0)}/5
            
            Provide:
            1. Churn risk level (low/medium/high)
            2. Risk percentage (0-100)
            3. Key risk factors
            4. Retention recommendations
            
            Return as JSON with keys: risk_level, risk_percentage, risk_factors, recommendations
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a customer success expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            return result
            
        except Exception as e:
            print(f"⚠️  AI churn prediction failed: {e}")
            return self._fallback_churn(customer_data)
    
    # Fallback methods when AI is unavailable
    
    def _fallback_email(self, email_type: str, context: Dict) -> Dict[str, str]:
        """Fallback email templates"""
        templates = {
            "welcome": {
                "subject": "Welcome to FineGuard!",
                "body": f"Dear {context.get('name', 'Valued Customer')},\n\nWelcome to FineGuard! We're excited to help you with your compliance and accounting needs.\n\nBest regards,\nThe FineGuard Team"
            },
            "reminder": {
                "subject": "Upcoming Consultation Reminder",
                "body": f"Dear {context.get('name', 'Valued Customer')},\n\nThis is a reminder about your upcoming consultation.\n\nBest regards,\nThe FineGuard Team"
            }
        }
        return templates.get(email_type, templates["welcome"])
    
    def _fallback_sentiment(self, company_data: Dict) -> Dict:
        """Fallback sentiment analysis"""
        compliance_score = company_data.get('complianceScore', 0)
        
        if compliance_score >= 80:
            sentiment = "positive"
        elif compliance_score >= 60:
            sentiment = "neutral"
        else:
            sentiment = "negative"
        
        return {
            "sentiment": sentiment,
            "strengths": ["Established business", "Active operations"],
            "concerns": ["Compliance monitoring needed"],
            "recommendations": ["Regular compliance reviews", "Professional accounting support"]
        }
    
    def _fallback_proposal(self, lead_data: Dict, package: str) -> str:
        """Fallback proposal template"""
        return f"""Dear {lead_data.get('companyName', 'Valued Client')},

Thank you for your interest in our {package} package. Based on your business needs, we believe our comprehensive accounting services can help you achieve your goals.

Our team at Devonshire Green has 90+ years of combined experience and we're ready to support your success.

Please contact us to discuss next steps.

Best regards,
The Devonshire Green Team"""
    
    def _fallback_churn(self, customer_data: Dict) -> Dict:
        """Fallback churn prediction"""
        engagement = customer_data.get('engagementScore', 50)
        
        if engagement >= 70:
            risk_level = "low"
            risk_percentage = 15
        elif engagement >= 40:
            risk_level = "medium"
            risk_percentage = 45
        else:
            risk_level = "high"
            risk_percentage = 75
        
        return {
            "risk_level": risk_level,
            "risk_percentage": risk_percentage,
            "risk_factors": ["Low engagement", "Infrequent contact"],
            "recommendations": ["Increase touchpoints", "Provide value-add content"]
        }
    
    def _build_email_prompt(self, email_type: str, context: Dict) -> str:
        """Build prompt for email generation"""
        return f"""
        Generate a professional email for: {email_type}
        
        Context:
        {json.dumps(context, indent=2)}
        
        Return as JSON with keys: subject, body, tone
        Keep it professional, concise, and personalized.
        """


# Singleton instance
ai_service = AIService()

