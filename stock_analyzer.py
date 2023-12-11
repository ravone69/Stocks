import yfinance as yf
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class StockAnalyzerApp(App):
    def build(self):
        Window.clearcolor = (0.8, 0.8, 1, 1)  # Light blue background color

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)  # Add padding and spacing for a clean look

        # Stock symbol entry
        self.entry = TextInput(hint_text='Stock Symbol', multiline=False, font_size=16, size_hint=(1, 0.1))
        layout.add_widget(self.entry)

        # Update button
        update_button = Button(text='Get Recommendation', font_size=18, size_hint=(1, 0.1))
        update_button.bind(on_press=self.update_recommendation)
        layout.add_widget(update_button)

        # Result label
        self.result_label = Label(text='', font_size=24, size_hint=(1, 0.8), color=(0.7, 0, 0, 1))  # Dark red color for probability text
        layout.add_widget(self.result_label)

        return layout

    def analyze_stock(self, data):
        symbol = data.index[0]
        if len(data) < 2:
            return symbol, 'Hold', 50

        price = data['Close'].iloc[-1]
        previous_close = data['Close'].iloc[-2]
        change_percent = (price - previous_close) / previous_close * 100

        if change_percent > 0:
            recommendation = 'Buy'
        elif change_percent < 0:
            recommendation = 'Sell'
        else:
            recommendation = 'Hold'

        # Calculate probability based on historical price movements
        price_changes = (data['Close'].diff() / data['Close'].shift(1)) * 100
        positive_changes = price_changes[price_changes > 0]
        negative_changes = price_changes[price_changes < 0]
        positive_probability = len(positive_changes) / len(price_changes) * 100
        negative_probability = len(negative_changes) / len(price_changes) * 100

        if recommendation == 'Buy':
            probability = positive_probability
        elif recommendation == 'Sell':
            probability = negative_probability
        else:
            probability = 100 - (positive_probability + negative_probability)

        return symbol, recommendation, probability, data

    def update_recommendation(self, instance):
        stock_symbol = self.entry.text
        stock_data = yf.download(stock_symbol, period='1mo')

        symbol, recommendation, probability, data = self.analyze_stock(stock_data)
        self.result_label.text = f"Stock: {symbol}\nRecommendation: {recommendation}\nProbability: {probability:.2f}%"

        # Plotting the real-time graph
        plt.figure(figsize=(8, 4))
        plt.plot(data['Close'], color='blue')
        plt.title(f"{stock_symbol} Stock Price")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    StockAnalyzerApp().run()
