# daily_analyzer.py - MAIN SCRIPT
import pandas as pd
import os
from datetime import datetime, date
from product_detector import ProductDetector
from question_analyzer import QuestionAnalyzer
from sentiment_analyzer import SentimentAnalyzer
import config

class DailyAnalyzer:
    def __init__(self):
        print("🚀 Instagram Message Analyzer Starting...\n")
        config.setup_directories()
        self.product_detector = ProductDetector()
        self.question_analyzer = QuestionAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        print("✅ System ready!\n")
    
    def analyze_today(self, excel_file=None):
        if excel_file is None:
            excel_file = config.DATA_FILE
        
        today = date.today().strftime('%Y-%m-%d')
        
        print("="*70)
        print(f"📅 DAILY ANALYSIS - {today}")
        print("="*70 + "\n")
        
        # Load Excel
        if not os.path.exists(excel_file):
            print(f"❌ File not found: {excel_file}")
            self._create_template(excel_file)
            print(f"✅ Template created: {excel_file}\n")
            return
        
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            print(f"❌ Error reading Excel: {e}\n")
            return
        
        # Add processed column
        if 'processed' not in df.columns:
            df['processed'] = 'no'
        
        # Filter NEW messages only
        new_messages = df[df['processed'] == 'no'].copy()
        
        print(f"📊 Total: {len(df)} | Already processed: {len(df) - len(new_messages)} | NEW: {len(new_messages)}\n")
        
        if len(new_messages) == 0:
            print("✅ No new messages!\n")
            return
        
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Process
        results = []
        stats = {'total': 0, 'very_high': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        print("🔄 Analyzing...\n" + "-"*70)
        
        for idx, row in new_messages.iterrows():
            username = str(row['username']).strip()
            message = str(row['message']).strip()
            
            if not message or message == 'nan':
                continue
            
            history_count = len(df[(df['username'] == username) & (df['processed'] == 'yes')])
            
            print(f"\n[{stats['total']+1}/{len(new_messages)}] @{username}")
            print(f"Message: {message[:60]}...")
            
            # Analyze
            analysis = self._analyze_message(row, history_count)
            
            print(f"   📱 {analysis['product']}")
            print(f"   ❓ {analysis['questions']}")
            print(f"   🎯 Intent: {analysis['intent']} ({analysis['intent_score']})")
            
            if analysis['intent'] in ['Very High', 'High']:
                print(f"   🚨 PRIORITY!")
            
            # Store
            results.append({
                'date': row['date'],
                'username': username,
                'message': message,
                'product': analysis['product'],
                'questions': analysis['questions'],
                'intent': analysis['intent'],
                'intent_score': analysis['intent_score'],
                'timeframe': analysis['timeframe'],
                'ready': analysis['ready_to_buy']
            })
            
            stats['total'] += 1
            intent_key = analysis['intent'].lower().replace(' ', '_')
            if intent_key in stats:
                stats[intent_key] += 1
            
            # Mark processed
            df.at[idx, 'processed'] = 'yes'
            df.at[idx, 'intent'] = analysis['intent']
            df.at[idx, 'product'] = analysis['product']
        
        print("\n" + "-"*70)
        
        # Save
        df.to_excel(excel_file, index=False)
        print(f"\n💾 Updated: {excel_file}")
        
        # Reports
        if results:
            self._generate_reports(results, today, stats)
        
        self._print_summary(stats, results)
    
    def _analyze_message(self, row, history_count):
        text = str(row['message']).strip()
        post_product = str(row.get('post_product', '')).strip()
        
        products = self.product_detector.detect_products(text, post_product)
        primary_product = self.product_detector.get_primary_product(products)
        
        questions = self.question_analyzer.analyze_questions(text)
        all_questions = self.question_analyzer.format_questions_list(questions)
        
        ready_to_buy = self.question_analyzer.is_ready_to_buy(text)
        timeframe = self.question_analyzer.detect_timeframe(text)
        
        # Sentiment analysis
        sentiment_analysis = self.sentiment_analyzer.analyze(text)
        
        # Calculate intent with enhanced scoring
        score = 0.3
        urgent_q = sum(1 for q in questions if q['urgency'] == 'high')
        score += urgent_q * 0.15
        if ready_to_buy:
            score += 0.3
        if timeframe in ['Today', 'Tomorrow']:
            score += 0.25
        if history_count > 0:
            score += min(history_count * 0.05, 0.15)
        
        # Boost score based on sentiment
        if sentiment_analysis['sentiment'] in ['Very Positive', 'Positive']:
            score += 0.1
        elif sentiment_analysis['is_eager']:
            score += 0.15
        
        # Boost for urgency modifiers
        urgency_modifier = self.question_analyzer.detect_urgency_modifiers(text)
        score += min(urgency_modifier * 0.02, 0.2)
        
        score = min(score, 1.0)
        
        if score >= 0.8:
            intent = "Very High"
        elif score >= 0.6:
            intent = "High"
        elif score >= 0.4:
            intent = "Medium"
        else:
            intent = "Low"
        
        # Customer segmentation
        customer_segment = self.question_analyzer.segment_customer(text, history_count, score)
        
        return {
            'product': primary_product,
            'questions': all_questions,
            'intent': intent,
            'intent_score': f"{score:.0%}",
            'ready_to_buy': 'YES' if ready_to_buy else 'NO',
            'timeframe': timeframe,
            'sentiment': sentiment_analysis['sentiment'],
            'customer_segment': customer_segment,
            'is_eager': 'YES' if sentiment_analysis['is_eager'] else 'NO',
            'has_doubts': 'YES' if sentiment_analysis['has_doubts'] else 'NO'
        }
    
    def _generate_reports(self, results, today, stats):
        print("\n📄 Generating reports...")
        
        # Daily report
        daily_file = config.DAILY_REPORTS / f"report_{today}.xlsx"
        df = pd.DataFrame(results)
        
        with pd.ExcelWriter(daily_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Messages', index=False)
            summary = pd.DataFrame({
                'Metric': ['Date', 'Total', 'Very High', 'High', 'Medium', 'Low'],
                'Value': [today, stats['total'], stats['very_high'], stats['high'], stats['medium'], stats['low']]
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"   ✅ Daily: {daily_file}")
        
        # Priority
        priority = [r for r in results if r['intent'] in ['High', 'Very High']]
        if priority:
            priority_file = config.PRIORITY_REPORTS / f"priority_{today}.xlsx"
            pd.DataFrame(priority).to_excel(priority_file, index=False)
            print(f"   🚨 Priority: {priority_file} ({len(priority)} customers)")
    
    def _print_summary(self, stats, results):
        print("\n" + "="*70)
        print("📊 SUMMARY")
        print("="*70)
        print(f"✅ Total: {stats['total']}")
        print(f"🔥 Very High: {stats['very_high']}")
        print(f"🎯 High: {stats['high']}")
        print(f"⚠️  Medium: {stats['medium']}")
        print(f"ℹ️  Low: {stats['low']}")
        
        priority = [r for r in results if r['intent'] in ['High', 'Very High']]
        
        if priority:
            print(f"\n{'='*70}")
            print(f"🚨 PRIORITY CUSTOMERS")
            print(f"{'='*70}")
            
            for p in priority:
                print(f"\n👤 @{p['username']}")
                print(f"   Product: {p['product']}")
                print(f"   Questions: {p['questions']}")
                print(f"   Intent: {p['intent']} ({p['intent_score']})")
                print(f"   Timeframe: {p['timeframe']}")
                if p['ready'] == 'YES':
                    print(f"   🔥 READY TO BUY!")
                if p['intent'] == 'Very High':
                    print(f"   ⚡ Reply in 30 mins!")
                else:
                    print(f"   ⚠️  Reply in 2 hours!")
        
        # Products
        products = {}
        for r in results:
            if r['product'] != 'Not specified':
                products[r['product']] = products.get(r['product'], 0) + 1
        
        if products:
            print(f"\n{'='*70}")
            print("📦 PRODUCT DEMAND")
            print(f"{'='*70}")
            for prod, count in sorted(products.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"   {prod}: {count} requests")
        
        print("\n" + "="*70)
        print("✅ COMPLETE!")
        print("="*70 + "\n")
    
    def _create_template(self, file_path):
        template_data = {
            'username': ['example1', 'example2', 'example3'],
            'message': [
                'iPhone 16 තියෙනවද? Price?',
                'MacBook Air M2 available?',
                'Samsung S24 Ultra I will come tomorrow'
            ],
            'post_product': ['iPhone 16', 'MacBook Air M2', 'Samsung S24 Ultra'],
            'date': [datetime.now()] * 3,
            'processed': ['no'] * 3
        }
        pd.DataFrame(template_data).to_excel(file_path, index=False)

def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║  📱 INSTAGRAM MESSAGE ANALYZER                           ║
╚═══════════════════════════════════════════════════════════╝

Options:
1. 📊 Analyze new messages
2. ❌ Exit
    """)
    
    choice = input("Choose (1-2): ").strip()
    
    if choice == '1':
        analyzer = DailyAnalyzer()
        analyzer.analyze_today()
    else:
        print("\n👋 Goodbye!\n")

if __name__ == "__main__":
    main()