# product_detector.py
import re

class ProductDetector:
    def __init__(self):
        self.products = {
            'iPhone': {
                'iphone 17 pro max': ['17 pro max', 'iphone 17 pro max', '17pro max'],
                'iphone 17 pro': ['17 pro', 'iphone 17 pro'],
                'iphone 17': ['iphone 17', '17'],
                'iphone 16 pro max': ['16 pro max', 'iphone 16 pro max'],
                'iphone 16 pro': ['16 pro', 'iphone 16 pro'],
                'iphone 16': ['iphone 16', '16'],
                'iphone 15 pro max': ['15 pro max', 'iphone 15 pro max'],
                'iphone 15 pro': ['15 pro', 'iphone 15 pro'],
                'iphone 15': ['iphone 15', '15'],
                'iphone 14 pro max': ['14 pro max', 'iphone 14 pro max'],
                'iphone 14 pro': ['14 pro', 'iphone 14 pro'],
                'iphone 14': ['iphone 14', '14'],
                'iphone 13': ['iphone 13', '13'],
            },
            'MacBook': {
                'macbook air m3': ['macbook air m3', 'air m3'],
                'macbook air m2': ['macbook air m2', 'air m2', 'macbook air 2023'],
                'macbook air': ['macbook air'],
                'macbook pro m3': ['macbook pro m3'],
                'macbook pro': ['macbook pro'],
            },
            'Samsung': {
                's24 ultra': ['s24 ultra', 'samsung s24 ultra'],
                's24': ['s24', 'samsung s24'],
                's23 ultra': ['s23 ultra'],
                's23': ['s23'],
            },
            'Other': {
                'honor 200': ['honor 200'],
                'ipad': ['ipad'],
            }
        }
    
    def detect_products(self, text, post_product=""):
        detected = []
        
        if post_product and post_product.strip():
            detected.append({
                'product': post_product.strip(),
                'category': self._get_category(post_product),
                'confidence': 'high',
                'source': 'post'
            })
        
        text_lower = text.lower()
        for category, models in self.products.items():
            for model_name, patterns in models.items():
                for pattern in patterns:
                    if self._match(pattern, text_lower):
                        storage = self._extract_storage(text)
                        prod_name = model_name.title()
                        if storage:
                            prod_name += f" {storage}"
                        
                        if not self._is_duplicate(prod_name, detected):
                            detected.append({
                                'product': prod_name,
                                'category': category,
                                'confidence': 'high',
                                'source': 'text'
                            })
                        break
        
        return detected if detected else [{'product': 'Not specified', 'category': 'Unknown', 'confidence': 'none', 'source': 'none'}]
    
    def _match(self, pattern, text):
        return bool(re.search(r'\b' + re.escape(pattern) + r'\b', text, re.IGNORECASE))
    
    def _extract_storage(self, text):
        match = re.search(r'\b(\d+)\s?(gb|tb)\b', text, re.IGNORECASE)
        return f"{match.group(1)}{match.group(2).upper()}" if match else None
    
    def _get_category(self, product):
        pl = product.lower()
        if 'iphone' in pl: return 'iPhone'
        if 'macbook' in pl: return 'MacBook'
        if 'samsung' in pl or 's24' in pl or 's23' in pl: return 'Samsung'
        return 'Phone'
    
    def _is_duplicate(self, product, detected):
        pl = product.lower()
        return any(pl in d['product'].lower() or d['product'].lower() in pl for d in detected)
    
    def get_primary_product(self, products):
        if not products or products[0]['product'] == 'Not specified':
            return "Not specified"
        for p in products:
            if p['source'] == 'post':
                return p['product']
        return products[0]['product']
    
    def format_products_list(self, products):
        if not products or products[0]['product'] == 'Not specified':
            return "Not specified"
        unique = []
        for p in products:
            if p['product'] not in unique:
                unique.append(p['product'])
        return ", ".join(unique)