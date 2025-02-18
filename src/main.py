import math
from collections import Counter

# Entropy means disorder or uncertainty. In information theory, it refers to the average amount of information produced by a stochastic source of data.
# In our case, higher entropy means more randomness or disorder in the data, while lower entropy means less randomness or more predictability.
def shannon_entropy(data):
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

# Example usage
text = f"The 78th British Academy Film Awards, more commonly known as the BAFTAs, was a ceremony held on 16 February 2025, honouring films of any nationality that were screened in British cinemas in 2024.\
The BAFTA longlists were unveiled on 3 January 2025.[1] The Rising Star nominees, which is the only category voted for by the British public, were unveiled on 7 January 2025, with the final nominations for all other categories announced on 15 January 2025 by previous BAFTA award winners Mia McKenna-Bruce and Will Sharpe.[2][3]\
Spanish-language French musical crime film Emilia Pérez had fifteen nods in the longlists, followed by Conclave with fourteen;[4] Conclave received the most nominations with twelve, followed by Emilia Pérez with eleven and The Brutalist with nine.[5] The Brutalist and Conclave ultimately won the most awards, with four each."

entropy_value = shannon_entropy(text)

print(f"Shannon Entropy of '{text}': {entropy_value:.4f}")
