# question_analyzer.py

class QuestionAnalyzer:
    def __init__(self):
        self.patterns = {
            'Price': {
                'keywords': [
                    # English
                    'price', 'how much', 'cost', 'expensive', 'cheaper', 'discount',
                    'offer', 'rate', 'rupees', 'rs.', 'lkr', 'lowest price',
                    'best price', 'bulk discount', 'wholesale',
                    # Sinhala
                    'කීයද', 'ගණන', 'මිල', 'නිසැ', 'වඩා', 'අඩු',
                    'මිල අධිකයි', 'සිතුම්', 'දි'
                ],
                'priority': 1,
                'urgency': 'high'
            },
            'Availability': {
                'keywords': [
                    # English
                    'available', 'have', 'stock', 'do you have', 'do u have',
                    'in stock', 'out of stock', 'left', 'remaining', 'quantity',
                    'how many', 'still have',
                    # Sinhala
                    'තියෙනවද', 'තියනවද', 'තිබේ', 'තිබේද', 'තිබුණ',
                    'එක තිබේ', 'බරක තිබේ'
                ],
                'priority': 1,
                'urgency': 'high'
            },
            'Payment Methods': {
                'keywords': [
                    # English
                    'installment', 'card', 'emi', 'monthly', 'bank transfer',
                    'cash', 'credit', 'debit', 'online payment', 'sslcommerz',
                    'dialog', 'warpin', 'payment plan',
                    # Sinhala
                    'වාරික', 'ගෙවුම්', 'කර්ඩ්', 'මාසිකව', 'බැංකුවට'
                ],
                'priority': 2,
                'urgency': 'medium'
            },
            'Exchange & Trade-In': {
                'keywords': [
                    # English
                    'exchange', 'trade', 'trade in', 'old phone', 'give', 'part exchange',
                    'upgrade', 'swap', 'return', 'refund', 'buyback',
                    # Sinhala
                    'එක්ස්චේන්ජ්', 'ගබඩා', 'පැරණි', 'පිටපත්'
                ],
                'priority': 2,
                'urgency': 'medium'
            },
            'Storage & Memory': {
                'keywords': [
                    # English
                    'storage', 'gb', 'tb', 'memory', 'ram', 'capacity',
                    '64gb', '128gb', '256gb', '512gb', '1tb',
                    '8gb', '12gb', '16gb', '32gb',
                    # Sinhala
                    'ගිබී', 'ටිබී', 'මතකය'
                ],
                'priority': 3,
                'urgency': 'medium'
            },
            'Colors & Variants': {
                'keywords': [
                    # English
                    'color', 'colour', 'black', 'white', 'blue', 'red', 'pink',
                    'silver', 'gold', 'gray', 'purple', 'green',
                    'titanium', 'midnight', 'starlight', 'midnight black',
                    'space gray', 'gold', 'rose gold',
                    # Sinhala
                    'වර්ණ', 'කළු', 'සුදු', 'නිල්'
                ],
                'priority': 3,
                'urgency': 'medium'
            },
            'Warranty & Authenticity': {
                'keywords': [
                    # English
                    'warranty', 'guarantee', 'original', 'authentic', 'genuine',
                    'fake', 'real', 'certified', 'official', 'apple care',
                    '1 year', '2 year', 'international', 'local', 'brand new',
                    # Sinhala
                    'වගකීම', 'අරඹුවෙ', 'ඔරිජිනල්', 'නිසැ'
                ],
                'priority': 4,
                'urgency': 'low'
            },
            'Delivery & Shipping': {
                'keywords': [
                    # English
                    'delivery', 'courier', 'send', 'ship', 'mail', 'deliver',
                    'fast delivery', 'overnight', 'express', 'home delivery',
                    'colombo', 'province', 'all over', 'everywhere',
                    # Sinhala
                    'යවන්න', 'දුරකතන', 'නගරයට', 'ප්‍රධානයට'
                ],
                'priority': 5,
                'urgency': 'low'
            },
            'Reservation & Preorder': {
                'keywords': [
                    # English
                    'reserve', 'preorder', 'pre-order', 'book', 'keep', 'hold',
                    'coming soon', 'when available', 'waiting list', 'pre order',
                    # Sinhala
                    'බුක්', 'අපෙතින්න', 'සදහා'
                ],
                'priority': 2,
                'urgency': 'high'
            },
            'Specifications & Features': {
                'keywords': [
                    # English
                    'specs', 'specifications', 'features', 'processor', 'camera',
                    'battery', 'display', 'screen', 'resolution', 'refresh rate',
                    'fps', 'ai', 'ai features', 'performance', 'speed', 'benchmark',
                    # Sinhala
                    'විශේෂතා', 'ගුණාංග'
                ],
                'priority': 3,
                'urgency': 'medium'
            },
            'Comparisons': {
                'keywords': [
                    # English
                    'compare', 'vs', 'versus', 'better', 'difference', 'which one',
                    'worth', 'best', 'should i get', 'recommend',
                    # Sinhala
                    'ඉතා', 'වඩා', 'වෙනස'
                ],
                'priority': 3,
                'urgency': 'medium'
            },
            'Accessories': {
                'keywords': [
                    # English
                    'case', 'screen protector', 'charger', 'cable', 'headphones',
                    'adapter', 'dock', 'tempered glass', 'cover', 'accessories',
                    'glass protector', 'usb-c'
                ],
                'priority': 5,
                'urgency': 'low'
            },
        }
    
    def analyze_questions(self, text):
        text_lower = text.lower()
        detected = []
        
        for q_type, data in self.patterns.items():
            if any(kw in text_lower for kw in data['keywords']):
                detected.append({
                    'type': q_type,
                    'priority': data['priority'],
                    'urgency': data['urgency']
                })
        
        detected.sort(key=lambda x: x['priority'])
        return detected if detected else [{'type': 'General Inquiry', 'priority': 99, 'urgency': 'low'}]
    
    def get_primary_question(self, questions):
        return questions[0]['type'] if questions else 'General Inquiry'
    
    def format_questions_list(self, questions):
        if not questions or questions[0]['type'] == 'General Inquiry':
            return "General Inquiry"
        return ", ".join([q['type'] for q in questions[:3]])
    
    def get_urgency_level(self, questions):
        for q in questions:
            if q['urgency'] == 'high':
                return "high"
        for q in questions:
            if q['urgency'] == 'medium':
                return "medium"
        return "low"
    
    def is_ready_to_buy(self, text):
        text_lower = text.lower()
        keywords = [
            'i will come', 'coming', 'will buy', 'want to buy',
            'today', 'tomorrow', 'keep one', 'reserve',
            'එනවා', 'ගන්නම්', 'අද', 'හෙට'
        ]
        return any(kw in text_lower for kw in keywords)
    
    def detect_timeframe(self, text):
        text_lower = text.lower()
        
        timeframes = {
            'Today': ['today', 'අද', 'right now', 'now', 'asap', 'today itself'],
            'Tomorrow': ['tomorrow', 'හෙට', 'tmrw', 'tmr'],
            'This Weekend': ['weekend', 'saturday', 'sunday'],
            'Next Week': ['next week', 'ලබන සතියේ'],
            'This Month': ['this month', 'මේ මාසේ'],
        }
        
        for tf, keywords in timeframes.items():
            if any(kw in text_lower for kw in keywords):
                return tf
        
        return "Not specified"
    
    def segment_customer(self, text, history_count, intent_score):
        """
        Segment customers for personalized handling
        Score should be between 0.0 and 1.0
        """
        if history_count == 0:
            if intent_score > 0.8:
                return "🔥 Hot Lead"  # New but very interested
            elif intent_score > 0.6:
                return "✨ Warm Lead"
            else:
                return "📋 New Prospect"
        
        elif history_count <= 2:
            if intent_score > 0.8:
                return "🎯 Engaged Buyer"
            elif intent_score > 0.6:
                return "💬 Interested"
            else:
                return "📊 Browsing"
        
        else:
            if intent_score > 0.8:
                return "👑 VIP Customer"
            elif intent_score > 0.6:
                return "🤝 Regular Customer"
            else:
                return "💼 Returning"
    
    def detect_urgency_modifiers(self, text):
        """
        Detect urgent language patterns
        Returns urgency score 0-10
        """
        text_lower = text.lower()
        
        urgent_words = {
            'extreme': ['asap', 'urgent', 'emergency', 'immediately', 'right now', 'hurry'],
            'high': ['today', 'now', 'soon', 'quick', 'fast'],
            'medium': ['tomorrow', 'this week', 'this weekend'],
            'low': ['eventually', 'whenever', 'no rush']
        }
        
        urgency = 0
        
        for level, words in urgent_words.items():
            if any(word in text_lower for word in words):
                if level == 'extreme':
                    urgency += 10
                elif level == 'high':
                    urgency += 7
                elif level == 'medium':
                    urgency += 4
                elif level == 'low':
                    urgency += 1
        
        return min(urgency, 10)
