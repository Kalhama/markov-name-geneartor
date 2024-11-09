import random
from collections import defaultdict
import pandas as pd


class BrandNameGenerator:
    def __init__(self, order=2):
        self.order = order
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.starts = defaultdict(int)
        self.total_counts = defaultdict(int)

        # Default letter penalties (1.0 = no penalty, 0.0 = completely discouraged)
        self.letter_penalties = {
            "ä": 0.2,
            "š": 0.2,
            "ö": 0.2,
            "-": 0.2,
            "x": 0.3,
            "g": 0.3,
            "b": 0.4,
            "q": 0.4,
            "z": 0.5,
            "v": 0.7,
            "w": 0.8,
            "r": 2,
        }

    def train(self, words, weight=1.0):
        """
        Train the model with weighted examples
        :param words: List of words to learn from
        :param weight: Weight of these examples
        """
        padded_words = ["^" * self.order + word.lower() + "$" for word in words]

        for word in padded_words:
            start_seq = word[: self.order]
            self.starts[start_seq] += weight

            for i in range(len(word) - self.order):
                state = word[i : i + self.order]
                next_char = word[i + self.order]
                self.transitions[state][next_char] += weight
                self.total_counts[state] += weight

    def apply_penalties(self, current_word, next_char, base_weight):
        """
        Apply various penalties to the weight of a character
        """
        penalty = 1.0

        # Apply individual letter penalties
        if next_char in self.letter_penalties:
            penalty *= self.letter_penalties[next_char]

        return base_weight * penalty

    def generate_word(self, min_length=3, max_length=12, temperature=0.5):
        """
        Generate a brand name with temperature control and letter penalties
        """
        if not self.starts:
            return ""

        # Select start based on weighted probabilities
        start_items = list(self.starts.items())
        start_weights = [count for _, count in start_items]
        current = random.choices(
            [seq for seq, _ in start_items], weights=start_weights
        )[0]
        result = current[self.order :]

        while len(result) < max_length:
            state = current[-self.order :]
            if state not in self.transitions:
                break

            # Get next character probabilities with penalties
            choices = list(self.transitions[state].items())
            weights = [
                self.apply_penalties(result, char, count) for char, count in choices
            ]

            # Apply temperature
            weights = [w ** (1 / temperature) for w in weights]

            if not any(weights):  # If all weights are zero
                break

            next_char = random.choices([char for char, _ in choices], weights=weights)[
                0
            ]

            if next_char == "$":
                if len(result) >= min_length:
                    break
                continue

            result += next_char
            current = current[1:] + next_char

        return result.capitalize()


def general_corpus():
    df = pd.read_csv("corpus/nykysuomensanalista2024.csv", sep="\t", index_col=False)
    words = df["Hakusana"]

    return words


# Example usage
if __name__ == "__main__":
    # Initialize generator
    generator = BrandNameGenerator(order=2)

    # Train with sample data
    general_words = general_corpus()
    generator.train(general_words, weight=1.0)

    brand_names = [
        "Google",
        "Apple",
        "Nike",
        "Adidas",
        "Spotify",
        "Netflix",
        "Amazon",
        "Tesla",
        "Microsoft",
        "Intel",
    ]
    generator.train(brand_names, weight=10000)

    # Generate examples
    print("\nGenerated Brand Names:")
    for _ in range(20):
        print(generator.generate_word(temperature=1))
