import math
from collections import Counter
import random
import wikipedia
import matplotlib.pyplot as plt

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
        except wikipedia.exceptions.PageError as e:
            # If the page does not exist, try again
            return ShannonEntropy.wiki_data(language)
        # get only articles that are long enough
        if len(text) < 500:
            return ShannonEntropy.wiki_data(language)
        return title, text
     
     @staticmethod 
     def sample_insight(text, insight_preffered_size = 5):
        # get all phrases
        phrases = text.split('.')
        # get section from text - insight content
        max_insight_size = insight_preffered_size if insight_preffered_size < len(phrases) else len(phrases)
        insight_size = random.randint(1, max_insight_size)
        start_phrase = random.randint(0, max_insight_size - insight_size)
        # return random selected insight content
        insight = '.'.join(phrases[start_phrase:start_phrase + insight_size])
        return insight
     
     # function to get random data, calculate entropy and return those data with calculated entropy
     @staticmethod
     def shanon_demo(data_amount = 100):
        result = []
        i = 0
        while (i < data_amount):
            # get title and content from wikipedia
            title, text = ShannonEntropy.wiki_data()
            # content -> insight
            insight = ShannonEntropy.sample_insight(text)
            entropy = ShannonEntropy.get(insight)
            data = {
                'title': title,
                'insight': insight,
                'entropy': entropy
            }
            result.append(data)
            i += 1
        return result


if __name__ == '__main__':
    data = ShannonEntropy.shanon_demo(50)
    # Sort data by entropy from higher to lower
    data.sort(key=lambda x: x['entropy'], reverse=False)
    
    # Save data to a text file
    with open('shannon_entropy_results.txt', 'w') as f:
        for item in data:
            f.write(f"Title: {item['title']}\n")
            f.write(f"Insight: {item['insight']}\n")
            f.write(f"Entropy: {item['entropy']}\n")
            f.write("\n")

    # Extract titles and entropy values for plotting
    titles = [item['title'] for item in data]
    entropies = [item['entropy'] for item in data]

    # Plot the graph
    plt.figure(figsize=(10, 5))
    plt.barh(titles, entropies, color='skyblue')
    plt.xlabel('Entropy')
    plt.ylabel('Title')
    plt.title('Shannon Entropy of Wikipedia Insights')
    plt.yticks(fontsize=6)
    plt.tight_layout()
    plt.savefig('shannon_entropy_plot.png')  # Save plot to a PNG file
    plt.show()
