# product_detector.py
import re

class ProductDetector:
    def __init__(self):
        self.use_ai = False
        self.ai_model = None
        self.product_categories = ['iPhone', 'iPad', 'MacBook', 'Samsung Galaxy', 'Redmi', 'Apple Watch', 'Google Pixel', 'OnePlus', 'Sony']
        
        self.products = {
            # === APPLE PRODUCTS ===
            'iPhone': {
                # iPhone 17 Series
                'iphone 17 pro max': ['17 pro max', 'iphone 17 pro max', '17pm', 'ip17pm'],
                'iphone 17 pro': ['17 pro', 'iphone 17 pro', '17p'],
                'iphone 17': ['iphone 17', '17'],
                
                # iPhone 16 Series
                'iphone 16 pro max': ['16 pro max', 'iphone 16 pro max', '16pm', 'ip16pm'],
                'iphone 16 pro': ['16 pro', 'iphone 16 pro', '16p'],
                'iphone 16 plus': ['16 plus', 'iphone 16 plus'],
                'iphone 16': ['iphone 16', '16'],
                
                # iPhone 15 Series
                'iphone 15 pro max': ['15 pro max', 'iphone 15 pro max'],
                'iphone 15 pro': ['15 pro', 'iphone 15 pro'],
                'iphone 15 plus': ['15 plus', 'iphone 15 plus'],
                'iphone 15': ['iphone 15', '15'],
                
                # iPhone 14 Series
                'iphone 14 pro max': ['14 pro max', 'iphone 14 pro max'],
                'iphone 14 pro': ['14 pro', 'iphone 14 pro'],
                'iphone 14 plus': ['14 plus', 'iphone 14 plus'],
                'iphone 14': ['iphone 14', '14'],
                
                # iPhone 13 Series
                'iphone 13 pro max': ['13 pro max', 'iphone 13 pro max'],
                'iphone 13 pro': ['13 pro', 'iphone 13 pro'],
                'iphone 13 mini': ['13 mini', 'iphone 13 mini'],
                'iphone 13': ['iphone 13', '13'],
                
                # iPhone 12 Series
                'iphone 12 pro max': ['12 pro max', 'iphone 12 pro max'],
                'iphone 12 pro': ['12 pro', 'iphone 12 pro'],
                'iphone 12 mini': ['12 mini', 'iphone 12 mini'],
                'iphone 12': ['iphone 12', '12'],
            },
            
            'iPad': {
                # iPad Pro
                'ipad pro 12.9 m4': ['ipad pro 12.9 m4', 'pro 12.9 m4'],
                'ipad pro 11 m4': ['ipad pro 11 m4', 'pro 11 m4'],
                'ipad pro 12.9 m2': ['ipad pro 12.9 m2', 'pro 12.9 m2'],
                'ipad pro 11 m2': ['ipad pro 11 m2', 'pro 11 m2'],
                'ipad pro 12.9': ['ipad pro 12.9', 'pro 12.9'],
                'ipad pro 11': ['ipad pro 11', 'pro 11'],
                
                # iPad Air
                'ipad air m2': ['ipad air m2', 'air m2'],
                'ipad air m1': ['ipad air m1', 'air m1'],
                'ipad air': ['ipad air'],
                
                # iPad (Regular)
                'ipad 10th gen': ['ipad 10th', 'ipad 10'],
                'ipad 9th gen': ['ipad 9th', 'ipad 9'],
                'ipad': ['ipad'],
                
                # iPad Mini
                'ipad mini 7': ['ipad mini 7', 'mini 7'],
                'ipad mini 6': ['ipad mini 6', 'mini 6'],
                'ipad mini': ['ipad mini'],
            },
            
            'MacBook': {
                # MacBook Pro M4
                'macbook pro 16 m4': ['macbook pro 16 m4', 'pro 16 m4'],
                'macbook pro 14 m4': ['macbook pro 14 m4', 'pro 14 m4'],
                
                # MacBook Pro M3
                'macbook pro 16 m3': ['macbook pro 16 m3', 'pro 16 m3'],
                'macbook pro 14 m3': ['macbook pro 14 m3', 'pro 14 m3'],
                'macbook pro m3': ['macbook pro m3'],
                
                # MacBook Pro M2
                'macbook pro 16 m2': ['macbook pro 16 m2', 'pro 16 m2'],
                'macbook pro 14 m2': ['macbook pro 14 m2', 'pro 14 m2'],
                'macbook pro m2': ['macbook pro m2'],
                
                # MacBook Air M4
                'macbook air 15 m4': ['macbook air 15 m4', 'air 15 m4'],
                'macbook air 13 m4': ['macbook air 13 m4', 'air 13 m4'],
                
                # MacBook Air M3
                'macbook air 15 m3': ['macbook air 15 m3', 'air 15 m3', 'macbook air m3'],
                'macbook air 13 m3': ['macbook air 13 m3', 'air 13 m3'],
                
                # MacBook Air M2
                'macbook air 15 m2': ['macbook air 15 m2', 'air 15 m2'],
                'macbook air 13 m2': ['macbook air 13 m2', 'air 13 m2', 'macbook air m2', 'macbook air 2023'],
                
                # MacBook Air M1
                'macbook air m1': ['macbook air m1', 'air m1'],
                
                # Generic
                'macbook air': ['macbook air'],
                'macbook pro': ['macbook pro'],
                'macbook': ['macbook'],
            },
            
            'Samsung Galaxy': {
                # S Series Flagship
                's24 ultra': ['s24 ultra', 'samsung s24 ultra', 'galaxy s24 ultra'],
                's24+': ['s24+', 'samsung s24+'],
                's24': ['s24', 'samsung s24', 'galaxy s24'],
                
                's23 ultra': ['s23 ultra', 'samsung s23 ultra'],
                's23+': ['s23+', 'samsung s23+'],
                's23': ['s23', 'samsung s23'],
                
                's22 ultra': ['s22 ultra', 'samsung s22 ultra'],
                's22+': ['s22+', 'samsung s22+'],
                's22': ['s22', 'samsung s22'],
                
                's21 ultra': ['s21 ultra', 'samsung s21 ultra'],
                's21+': ['s21+', 'samsung s21+'],
                's21': ['s21', 'samsung s21'],
                
                's20 ultra': ['s20 ultra', 'samsung s20 ultra'],
                's20+': ['s20+', 'samsung s20+'],
                's20': ['s20', 'samsung s20'],
                
                # A Series Mid-range
                'galaxy a55': ['a55', 'samsung a55', 'galaxy a55'],
                'galaxy a54': ['a54', 'samsung a54', 'galaxy a54'],
                'galaxy a53': ['a53', 'samsung a53'],
                'galaxy a52': ['a52', 'samsung a52'],
                'galaxy a51': ['a51', 'samsung a51'],
                
                # M Series Budget
                'galaxy m55': ['m55', 'samsung m55'],
                'galaxy m35': ['m35', 'samsung m35'],
                'galaxy m34': ['m34', 'samsung m34'],
                'galaxy m33': ['m33', 'samsung m33'],
                
                # Z Fold & Z Flip (Foldables)
                'galaxy z fold 6': ['z fold 6', 'fold 6', 'galaxy fold 6'],
                'galaxy z fold 5': ['z fold 5', 'fold 5', 'galaxy fold 5'],
                'galaxy z flip 6': ['z flip 6', 'flip 6', 'galaxy flip 6'],
                'galaxy z flip 5': ['z flip 5', 'flip 5', 'galaxy flip 5'],
                
                # Tab Series
                'galaxy tab s10': ['tab s10', 'samsung tab s10'],
                'galaxy tab s9': ['tab s9', 'samsung tab s9'],
                'galaxy tab s8': ['tab s8', 'samsung tab s8'],
            },
            
            # === SONY PRODUCTS ===
            'Sony PlayStation': {
                # PS5
                'ps5': ['ps5', 'playstation 5', 'sony ps5'],
                'ps5 pro': ['ps5 pro', 'playstation 5 pro'],
                'ps5 console': ['ps5 console', 'playstation 5 console'],
                'ps5 digital': ['ps5 digital', 'ps5 de', 'playstation 5 digital'],
                'ps5 disc': ['ps5 disc', 'playstation 5 disc'],
                
                # PS4 (Legacy)
                'ps4': ['ps4', 'playstation 4', 'sony ps4'],
                'ps4 pro': ['ps4 pro', 'playstation 4 pro'],
                'ps4 slim': ['ps4 slim', 'playstation 4 slim'],
            },
            
            'Sony Camera': {
                'sony a9 iii': ['a9 iii', 'sony a9 iii', 'alpha 9 iii'],
                'sony a9 ii': ['a9 ii', 'sony a9 ii'],
                'sony a9': ['a9', 'sony a9'],
                'sony a7r v': ['a7r v', 'sony a7r v'],
                'sony a7r iv': ['a7r iv', 'sony a7r iv'],
                'sony a7 iv': ['a7 iv', 'sony a7 iv'],
                'sony a6700': ['a6700', 'sony a6700'],
                'sony a6400': ['a6400', 'sony a6400'],
            },
            
            # === XIAOMI PRODUCTS ===
            'Xiaomi': {
                # Xiaomi 14 Series
                'xiaomi 14 ultra': ['xiaomi 14 ultra', '14 ultra', 'mi 14 ultra'],
                'xiaomi 14': ['xiaomi 14', '14', 'mi 14'],
                
                # Xiaomi 13 Series
                'xiaomi 13 ultra': ['xiaomi 13 ultra', '13 ultra', 'mi 13 ultra'],
                'xiaomi 13': ['xiaomi 13', '13', 'mi 13'],
                
                # Xiaomi 12 Series
                'xiaomi 12s ultra': ['12s ultra', 'xiaomi 12s ultra', 'mi 12s ultra'],
                'xiaomi 12': ['xiaomi 12', '12', 'mi 12'],
            },
            
            # === REDMI PHONES ===
            'Redmi': {
                # Redmi Note Series (Flagship Budget)
                'redmi note 14 pro': ['redmi note 14 pro', 'note 14 pro', 'redmi note 14p'],
                'redmi note 14 pro+': ['redmi note 14 pro+', 'note 14 pro+', 'redmi note 14 pro plus'],
                'redmi note 14': ['redmi note 14', 'note 14'],
                
                'redmi note 13 pro': ['redmi note 13 pro', 'note 13 pro', 'redmi note 13p'],
                'redmi note 13 pro+': ['redmi note 13 pro+', 'note 13 pro+', 'redmi note 13 pro plus'],
                'redmi note 13': ['redmi note 13', 'note 13'],
                
                'redmi note 12 pro': ['redmi note 12 pro', 'note 12 pro'],
                'redmi note 12 pro+': ['redmi note 12 pro+', 'note 12 pro plus'],
                'redmi note 12': ['redmi note 12', 'note 12'],
                
                'redmi note 11 pro': ['redmi note 11 pro', 'note 11 pro'],
                'redmi note 11': ['redmi note 11', 'note 11'],
                
                # Redmi Series (Mid-range)
                'redmi 14': ['redmi 14'],
                'redmi 13': ['redmi 13'],
                'redmi 12': ['redmi 12'],
                'redmi 11': ['redmi 11'],
                'redmi 10': ['redmi 10'],
                
                # Redmi K Series (Performance)
                'redmi k70': ['redmi k70', 'k70'],
                'redmi k70 pro': ['redmi k70 pro', 'k70 pro'],
                'redmi k60': ['redmi k60', 'k60'],
                'redmi k60 pro': ['redmi k60 pro', 'k60 pro'],
                'redmi k50': ['redmi k50', 'k50'],
                'redmi k50 pro': ['redmi k50 pro', 'k50 pro'],
                
                # Redmi 9 Series (Budget)
                'redmi 9': ['redmi 9'],
                'redmi 9 pro': ['redmi 9 pro'],
                
                # Redmi A Series (Entry-level)
                'redmi a3': ['redmi a3'],
                'redmi a2': ['redmi a2'],
                'redmi a1': ['redmi a1'],
                'redmi a4': ['redmi a4'],
                'redmi a5': ['redmi a5','A5', 'a 5', 'A-5','A5'],
            },
            
            # === GOOGLE PIXEL ===
            'Google Pixel': {
                'pixel 9 pro': ['pixel 9 pro', 'google pixel 9 pro'],
                'pixel 9': ['pixel 9', 'google pixel 9'],
                'pixel 8 pro': ['pixel 8 pro', 'google pixel 8 pro'],
                'pixel 8': ['pixel 8', 'google pixel 8'],
                'pixel 7 pro': ['pixel 7 pro', 'google pixel 7 pro'],
                'pixel 7': ['pixel 7', 'google pixel 7'],
                'pixel 6 pro': ['pixel 6 pro', 'google pixel 6 pro'],
                'pixel 6': ['pixel 6', 'google pixel 6'],
            },
            
            # === ONEPLUS ===
            'OnePlus': {
                'oneplus 12': ['oneplus 12', 'one plus 12'],
                'oneplus 11': ['oneplus 11'],
                'oneplus 10': ['oneplus 10'],
                'oneplus 9': ['oneplus 9'],
            },
            
            # === HONOR ===
            'Honor': {
                'honor 200': ['honor 200'],
                'honor 200 pro': ['honor 200 pro'],
                'honor x9c': ['honor x9c'],
                'honor 50': ['honor 50'],
            },
            
            # === APPLE WATCH ===
            'Apple Watch': {
                'apple watch ultra 2': ['apple watch ultra 2', 'watch ultra 2', 'ultra 2'],
                'apple watch ultra': ['apple watch ultra', 'watch ultra'],
                'apple watch series 9': ['apple watch series 9', 'series 9', 'watch 9'],
                'apple watch series 8': ['apple watch series 8', 'series 8', 'watch 8'],
                'apple watch series 7': ['apple watch series 7', 'series 7', 'watch 7'],
                'apple watch se 3': ['apple watch se 3', 'watch se 3', 'se 3'],
                'apple watch se 2': ['apple watch se 2', 'watch se 2', 'se 2'],
                'apple watch se': ['apple watch se', 'watch se'],
            },
            
            # === OTHER BRANDS ===
            'Other Devices': {
                'airpods pro': ['airpods pro', 'airpods max'],
                'airpods': ['airpods'],
                'samsung watch': ['samsung watch'],
                'realme': ['realme'],
                'vivo': ['vivo'],
                'oppo': ['oppo'],
            }
        }
        
        # Try to load free AI model (optional enhancement)
        self._load_ai_model()
    
    def _load_ai_model(self):
        """Load free zero-shot classification model for product detection"""
        try:
            from transformers import pipeline
            print("⚙️  Loading free AI product detection model (zero-shot)...")
            self.ai_model = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1  # Use CPU
            )
            self.use_ai = True
            print("✅ AI product detection model loaded!\n")
        except Exception as e:
            print(f"⚠️  AI product model unavailable (using rule-based only): {e}\n")
            self.use_ai = False
            self.ai_model = None
    
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
        
        # Try AI model first (if available)
        if self.use_ai and self.ai_model:
            try:
                ai_products = self._detect_products_ai(text)
                detected.extend(ai_products)
            except Exception as e:
                print(f"  ⚠️  AI product detection failed: {e}, using keywords")
                pass
        
        # Rule-based detection (always run as fallback)
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
    
    def _detect_products_ai(self, text):
        """Detect products using zero-shot classification (AI-powered)"""
        try:
            results = []
            text_short = text[:300]  # Limit text length
            
            # Use zero-shot classification to find product mentions
            # The pipeline returns a dict with 'labels' and 'scores'
            predictions = self.ai_model(text_short, self.product_categories, multi_class=False)
            labels = predictions.get('labels', []) if isinstance(predictions, dict) else []
            scores = predictions.get('scores', []) if isinstance(predictions, dict) else []

            if labels and scores:
                top_label = labels[0]
                top_score = scores[0]
                if top_score > 0.5:  # Only if confident
                    results.append({
                        'product': top_label,
                        'category': top_label,
                        'confidence': 'medium' if top_score > 0.7 else 'low',
                        'source': 'ai'
                    })
            
            return results
        except Exception:
            return []
    
    def _match(self, pattern, text):
        return bool(re.search(r'\b' + re.escape(pattern) + r'\b', text, re.IGNORECASE))
    
    def _extract_storage(self, text):
        """Extract storage capacity with enhanced pattern matching"""
        patterns = [
            r'\b(\d+)\s?(gb|tb)\b',  # Standard: 256GB, 256 GB
            r'\b(\d+)(gb|tb)\b',      # Compact: 256gb, 256tb
            r'\b(\d+)\s?[\-/]\s?(\d+)',  # Dual: 256/512, 256-512
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower(), re.IGNORECASE)
            if match:
                if pattern == r'\b(\d+)\s?[\-/]\s?(\d+)':
                    return f"{match.group(1)}/{match.group(2)}GB"
                return f"{match.group(1)}{match.group(2).upper()}"
        
        return None
    
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