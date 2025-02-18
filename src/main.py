import math
from collections import Counter
import random
import wikipedia

 # Entropy means disorder or uncertainty. In information theory, it refers to the average amount of information produced by a stochastic source of data.
 # In our case, higher entropy means more randomness or disorder in the data, while lower entropy means less randomness or more predictability.
class ShannonEntropy:
     @staticmethod
     def get(data):
        """Calculate Shannon entropy of a given string or dataset."""
        if not data:
            return 0  # Entropy is 0 for empty data
        # Count occurrences of each unique symbol
        counts = Counter(data)
        # Calculate probabilities
        total = len(data)
        probabilities = [count / total for count in counts.values()]
        # Compute entropy using Shannon's formula
        entropy = -sum(p * math.log2(p) for p in probabilities)

        return entropy
     
     @staticmethod
     def wiki_data(language = 'en'):
        # load single data from wikipedia
        wikipedia.set_lang(language)
        page = wikipedia.random()
        try:
            title = wikipedia.page(page).title
            text = wikipedia.page(page).content
        except wikipedia.exceptions.DisambiguationError as e:
            # If the page name is ambiguous, try again
            return ShannonEntropy.wiki_data(language)
        # get only articles that are long enough
        if len(text) < 500:
            return ShannonEntropy.wiki_data(language)
        return title, text
     
     @staticmethod 
     def sample_insight(text):
        # get all phrases
        phrases = text.split('.')
        # get section from text - insight content
        max_insight_size = 5 if 5 < len(phrases) else len(phrases)
        insight_size = random.randint(1, max_insight_size)
        start_phrase = random.randint(0, max_insight_size - insight_size)
        # return random selected insight content
        insight = '.'.join(phrases[start_phrase:start_phrase + insight_size])
        return insight
     
     @staticmethod
     def shanon_demo(data_amount = 100):
         pass


text = ShannonEntropy.wiki_data()
print(text)

#entropy_value = shannon_entropy(text)

#print(f"Shannon Entropy of '{text}': {entropy_value:.4f}")
