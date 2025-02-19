import math
from collections import Counter
import random
import wikipedia
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords

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

def load_data():
       with open('shannon_entropy_results.txt', 'r') as f:
        data = f.read()
        result = []
        entries = data.strip().split('Entropy:')
        title, insight, entropy = None, None, None
        for entry in entries:
            for line in entry.splitlines():
                if 'Title:' in line:
                    title = line.replace('Title:', '').strip()
                elif 'Insight:' in line:
                    insight = line.replace('Insight:', '').strip()
                elif line.strip().replace('.', '', 1).isdigit():
                    entropy = float(line.strip())
                    result.append({'title': title, 'insight': insight, 'entropy': entropy})
        return result

def random_noisy_data(n = 50):
    noisy_data = []
    i = 0
    while i < n:
        random_data = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!/.(*^%*)?\'~`><', k=100))
        noisy_data.append({'title' : f'noise {i}', 'insight' : random_data, 'entropy': ShannonEntropy.get(random_data)})
        i += 1
    return noisy_data

def remove_noise(text):
    """Remove noise from text by filtering non-informative content."""
    
    # Convert text to lowercase
    text = text.lower()

    # Remove special characters, numbers, and extra whitespace
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    cleaned_words = [word for word in words if word not in stop_words]

    # Reconstruct cleaned text
    cleaned_text = ' '.join(cleaned_words)
    
    return cleaned_text

def existing_demo():
    data = load_data()
    nltk.download('stopwords')
    choice = input('Create new random noisy data? [y/n] ')
    if choice == 'y':
        noisy_data = random_noisy_data()
        noisy_data.sort(key=lambda x: x['entropy'], reverse=False)
        save_data(noisy_data, 'noisy_data.txt')
        plot_data(noisy_data, 'noisy_data_plot', 'Shannon Entropy of Noisy Insights')

    entropies = [item['entropy'] for item in data]
    mean_entropy = sum(entropies) / len(entropies)
    variance = sum((x - mean_entropy) ** 2 for x in entropies) / len(entropies)
    std_deviation = math.sqrt(variance)
    print(f"Mean Entropy: {mean_entropy}")
    print(f"Standard Deviation: {std_deviation}")
    noise_constant = float(input('Set noise constant k = '))
    cut_off = mean_entropy + noise_constant * std_deviation

    unnoised_data = []
    for item in data:
        if item['entropy'] > cut_off:
            unnoised_insight = remove_noise(item['insight'])
            unnoised_entropy = ShannonEntropy.get(unnoised_insight)
            unnoised_data.append({'title': item['title'], 'raw_insight' : item['insight'], 'raw_entropy' : item['entropy'], 'unnoised_insight': unnoised_insight, 'unnoised_entropy': unnoised_entropy})
    
    save_data(unnoised_data, 'unnoised_data.txt')

    # Plot raw entropy vs unnoised entropy
    raw_entropies = [item['raw_entropy'] for item in unnoised_data]
    unnoised_entropies = [item['unnoised_entropy'] for item in unnoised_data]
    titles = [item['title'] for item in unnoised_data]

    plt.figure(figsize=(10, 5))
    plt.barh(titles, raw_entropies, color='red', alpha=0.5, label='Raw Entropy')
    plt.barh(titles, unnoised_entropies, color='green', alpha=0.5, label='Unnoised Entropy')
    plt.xlabel('Entropy')
    plt.ylabel('Title')
    plt.title('Comparison of Raw and Unnoised Entropy')
    plt.legend()
    plt.yticks(fontsize=6)
    plt.tight_layout()
    plt.savefig('unnoised_entropy_comparison.png')
    plt.show()
    plt.savefig('unnoised_entropy_comparison.png')

def save_data(data, destination):
        # Save data to a text file
    with open(destination, 'w') as f:
        for item in data:
            for key, value in item.items():
                f.write(f"{key.capitalize()}: {value}\n")
            f.write("\n")

def plot_data(data, destination, name):
     # Extract titles and entropy values for plotting
    titles = [item['title'] for item in data]
    entropies = [item['entropy'] for item in data]

    # Plot the graph
    plt.figure(figsize=(10, 5))
    plt.barh(titles, entropies, color='skyblue')
    plt.xlabel('Entropy')
    plt.ylabel('Title')
    plt.title(name)
    plt.yticks(fontsize=6)
    plt.tight_layout()
    plt.savefig(destination + '.png')  # Save plot to a PNG file
    plt.show()
    
def new_demo():
    data = ShannonEntropy.shanon_demo(50)
    # Sort data by entropy from higher to lower
    data.sort(key=lambda x: x['entropy'], reverse=False)
    
    save_data(data, 'shannon_entropy_results.txt')
    plot_data(data, 'shanon_entropy_plot', 'Shannon Entropy of Wikipedia Insights')


if __name__ == '__main__':
    choice = input('existing/new demo? [y/n]')
    if choice == 'y':
        existing_demo()
    else:
        new_demo()