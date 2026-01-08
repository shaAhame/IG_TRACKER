# question_analyzer.py

class QuestionAnalyzer:
    def __init__(self):
        self.patterns = {
            'Price': {
                'keywords': ['price', 'how much', 'cost', 'kiyada', 'කීයද', 'ගණන', 'මිල'],
                'priority': 1,
                'urgency': 'high'
            },
            'Availability': {
                'keywords': ['available', 'have', 'stock', 'තියෙනවද', 'තියනවද', 'do you have', 'do u have'],
                'priority': 1,
                'urgency': 'high'
            },
            'Payment': {
                'keywords': ['installment', 'payment', 'card', 'වාරික', 'monthly', 'emi'],
                'priority': 2,
                'urgency': 'medium'
            },
            'Exchange': {
                'keywords': ['exchange', 'trade', 'old phone', 'give', 'trade in'],
                'priority': 2,
                'urgency': 'medium'
            },
            'Colors': {
                'keywords': ['color', 'colour', 'black', 'white', 'blue', 'red', 'pink'],
                'priority': 3,
                'urgency': 'medium'
            },
            'Warranty': {
                'keywords': ['warranty', 'guarantee', 'original', 'වගකීම', 'brand new'],
                'priority': 4,
                'urgency': 'low'
            },
            'Delivery': {
                'keywords': ['delivery', 'courier', 'send', 'යවන්න', 'ship'],
                'priority': 5,
                'urgency': 'low'
            },
            'Reservation': {
                'keywords': ['reserve', 'preorder', 'book', 'keep', 'hold'],
                'priority': 2,
                'urgency': 'high'
            }
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
            'Today': ['today', 'අද', 'right now', 'now'],
            'Tomorrow': ['tomorrow', 'හෙට', 'tmrw'],
            'This Weekend': ['weekend', 'saturday', 'sunday'],
            'Next Week': ['next week', 'ලබන සතියේ'],
            'This Month': ['this month', 'මේ මාසේ'],
        }
        
        for tf, keywords in timeframes.items():
            if any(kw in text_lower for kw in keywords):
                return tf
        
        return "Not specified"