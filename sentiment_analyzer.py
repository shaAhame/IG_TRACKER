# sentiment_analyzer.py
import re


class SentimentAnalyzer:
    """
    Analyzes message sentiment and emotional signals
    to better understand customer satisfaction and urgency.

    Uses hybrid approach:
    - Rule-based keyword matching (fast, reliable)
    - Optional Free AI model (distilbert) for enhanced accuracy
    """

    def __init__(self):
        self.use_ai = False
        self.ai_model = None
        self.positive_words = {
            # English
            "love": 2,
            "amazing": 2,
            "great": 1.5,
            "awesome": 2,
            "perfect": 2,
            "excellent": 2,
            "good": 1,
            "beautiful": 2,
            "best": 1.5,
            "fantastic": 2,
            "happy": 1.5,
            "satisfied": 1,
            "impressed": 1.5,
            "recommend": 1,
            "worth": 1,
            "nice": 1,
            "cool": 1,
            "interesting": 1,
            # Sinhala
            "සුපිරි": 2,
            "ශ්‍රේෂ්ඨ": 2,
            "හොඳ": 1,
            "ඉතා": 1,
            "පිලිසිතුම්": 2,
            "ගිණුම්": 1,
        }

        self.negative_words = {
            # English
            "bad": 2,
            "awful": 2,
            "terrible": 2,
            "worse": 1.5,
            "worst": 2,
            "broken": 2,
            "damaged": 2,
            "expensive": 1,
            "fake": 2,
            "disappointed": 1.5,
            "poor": 1.5,
            "hate": 2,
            "useless": 2,
            "waste": 1.5,
            "problem": 1,
            "issue": 1,
            "complaint": 1.5,
            "scam": 2,
            "cheat": 2,
            # Sinhala
            "නරක": 2,
            "බිඳුණු": 2,
            "මිල අධිකයි": 1,
            "වංචනය": 2,
            "ගැටලුව": 1,
            "පිළිතුරු": 1,
        }

        self.urgent_modifiers = {
            # Extreme urgency
            "extreme": [
                "asap",
                "urgent",
                "emergency",
                "immediately",
                "right now",
                "hurry",
                "quick",
                "fastest",
                "fastest delivery",
                "වහා",
            ],
            # High urgency
            "high": ["today", "now", "soon", "today itself", "අද"],
            # Medium urgency
            "medium": ["tomorrow", "this week", "this weekend", "හෙට"],
            # Low urgency
            "low": ["eventually", "whenever", "no rush", "time"],
        }

        self.eagerness_signals = [
            "will buy",
            "coming",
            "i will come",
            "coming today",
            "coming tomorrow",
            "coming now",
            "keep one",
            "hold one",
            "sure",
            "definitely",
            "confirm",
            "එනවා",
            "ගන්නම්",
            "හරි",
        ]

        self.doubt_signals = [
            "maybe",
            "might",
            "perhaps",
            "probably",
            "thinking",
            "considering",
            "not sure",
            "unsure",
            "i will think",
            "let me think",
            "need time",
            "ඉතින්",
            "බලා ගමි",
        ]

        # Try to load free AI model (optional)
        self._load_ai_model()

    def _load_ai_model(self):
        """Load free distilbert sentiment model (optional enhancement)"""
        try:
            from transformers import pipeline

            print("⚙️  Loading free AI sentiment model (distilbert)...")
            self.ai_model = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1,  # Use CPU
            )
            self.use_ai = True
            print("✅ AI model loaded! Sentiment analysis enhanced.\n")
        except Exception as e:
            print(f"⚠️  AI model unavailable (using rule-based only): {e}\n")
            self.use_ai = False
            self.ai_model = None

    def analyze(self, text):
        """
        Comprehensive sentiment analysis
        Returns dict with sentiment, emotion score, urgency, and signals
        """
        text_lower = text.lower()

        # Sentiment analysis
        sentiment, sentiment_score = self._calculate_sentiment(text_lower)

        # Urgency detection
        urgency, urgency_score = self._calculate_urgency(text_lower)

        # Customer signals
        eagerness = self._detect_eagerness(text_lower)
        doubt = self._detect_doubt(text_lower)

        return {
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,  # -10 to 10
            "urgency": urgency,
            "urgency_score": urgency_score,  # 0 to 10
            "is_eager": eagerness,
            "has_doubts": doubt,
            "overall_signal": self._determine_overall_signal(
                sentiment_score, urgency_score, eagerness, doubt
            ),
        }

    def _calculate_sentiment(self, text_lower):
        """
        Calculate sentiment using hybrid approach:
        1. Try AI model first (if available) for nuanced understanding
        2. Fall back to rule-based keyword matching
        """

        # Try AI model first (free distilbert)
        if self.use_ai and self.ai_model:
            try:
                # Truncate to 512 tokens for model
                text_short = text_lower[:500]
                result = self.ai_model(text_short)[0]
                ai_label = result["label"]  # POSITIVE or NEGATIVE
                ai_score = result["score"]  # 0-1 confidence

                # Convert AI output to our scale (-10 to 10)
                if ai_label == "POSITIVE":
                    ai_sentiment_score = ai_score * 10
                    ai_sentiment = "Positive" if ai_score > 0.7 else "Neutral"
                else:
                    ai_sentiment_score = -ai_score * 10
                    ai_sentiment = "Negative" if ai_score > 0.7 else "Neutral"

                # Combine with keyword-based score for better accuracy
                keyword_score = self._calculate_keyword_sentiment(text_lower)

                # Weighted average: 70% AI, 30% Keywords (keywords good for domain-specific terms)
                combined_score = (ai_sentiment_score * 0.7) + (keyword_score * 0.3)

                if combined_score > 3:
                    sentiment = "Very Positive"
                elif combined_score > 0:
                    sentiment = "Positive"
                elif combined_score < -3:
                    sentiment = "Very Negative"
                elif combined_score < 0:
                    sentiment = "Negative"
                else:
                    sentiment = "Neutral"

                return sentiment, max(-10, min(10, combined_score))

            except Exception as e:
                # Fallback to keyword-based if AI fails
                print(f"  ⚠️  AI sentiment failed: {e}, using keywords")
                pass

        # Keyword-based sentiment (reliable fallback)
        keyword_score = self._calculate_keyword_sentiment(text_lower)

        if keyword_score > 3:
            sentiment = "Very Positive"
        elif keyword_score > 0:
            sentiment = "Positive"
        elif keyword_score < -3:
            sentiment = "Very Negative"
        elif keyword_score < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return sentiment, max(-10, min(10, keyword_score))

    def _calculate_keyword_sentiment(self, text_lower):
        """Calculate sentiment score from keyword matching"""
        pos_score = sum(
            weight for word, weight in self.positive_words.items() if word in text_lower
        )
        neg_score = sum(
            weight for word, weight in self.negative_words.items() if word in text_lower
        )
        return pos_score - neg_score

    def _calculate_urgency(self, text_lower):
        """Calculate urgency level"""

        urgency_score = 0
        urgency = "Not Specified"

        for level, words in self.urgent_modifiers.items():
            for word in words:
                if word in text_lower:
                    if level == "extreme":
                        urgency_score = 10
                        urgency = "Extreme Urgency"
                        return urgency, urgency_score
                    elif level == "high":
                        urgency_score = max(urgency_score, 8)
                        urgency = "High Urgency"
                    elif level == "medium":
                        urgency_score = max(urgency_score, 5)
                        urgency = "Medium Urgency"
                    elif level == "low" and urgency_score == 0:
                        urgency_score = 2
                        urgency = "Low Urgency"

        return urgency, urgency_score

    def _detect_eagerness(self, text_lower):
        """Detect if customer is eager to buy"""
        return any(signal in text_lower for signal in self.eagerness_signals)

    def _detect_doubt(self, text_lower):
        """Detect if customer has doubts"""
        return any(signal in text_lower for signal in self.doubt_signals)

    def _determine_overall_signal(
        self, sentiment_score, urgency_score, eagerness, doubt
    ):
        """
        Determine overall customer signal for decision making
        """
        score = urgency_score + (sentiment_score + 10) / 4  # Normalize sentiment to 0-5

        if eagerness:
            score += 3

        if doubt:
            score -= 2

        score = max(0, min(10, score))  # Clamp to 0-10

        if score >= 8:
            return "🚀 Strong Buy Signal"
        elif score >= 6:
            return "✅ Good Signal"
        elif score >= 4:
            return "⚠️ Neutral Signal"
        elif score >= 2:
            return "❓ Weak Signal"
        else:
            return "❌ Poor Signal"

    def get_response_recommendation(self, analysis):
        """
        Based on sentiment analysis, recommend response strategy
        """
        sentiment = analysis["sentiment"]
        urgency = analysis["urgency"]
        is_eager = analysis["is_eager"]
        has_doubts = analysis["has_doubts"]

        if is_eager and urgency == "Extreme Urgency":
            return {
                "priority": "CRITICAL",
                "response_time": "< 5 minutes",
                "tone": "Friendly & Fast",
                "action": "Call customer immediately",
            }

        elif urgency == "High Urgency" or is_eager:
            return {
                "priority": "HIGH",
                "response_time": "< 30 minutes",
                "tone": "Professional & Warm",
                "action": "Quick response with all details",
            }

        elif has_doubts:
            return {
                "priority": "MEDIUM",
                "response_time": "< 2 hours",
                "tone": "Informative & Reassuring",
                "action": "Address concerns, provide comparisons",
            }

        elif sentiment == "Very Negative":
            return {
                "priority": "MEDIUM",
                "response_time": "< 1 hour",
                "tone": "Empathetic & Solution-focused",
                "action": "Address issues, offer solutions",
            }

        else:
            return {
                "priority": "NORMAL",
                "response_time": "Same day",
                "tone": "Friendly & Informative",
                "action": "Standard response",
            }
