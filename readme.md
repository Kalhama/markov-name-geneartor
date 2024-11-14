# Brand Name Generator

A sophisticated Python-based brand name generator that uses Markov chains and customizable weights to create unique, memorable brand names.

## Features

- **Markov Chain Generation**: Creates natural-sounding names using configurable n-gram order
- **Weighted Training**: Support for multiple training corpora with adjustable weights
- **Temperature Control**: Adjustable randomness in name generation
- **Letter Penalties**: Customizable penalties for specific characters
- **Length Control**: Configurable minimum and maximum word lengths
- **Case Handling**: Automatic capitalization of generated names

## Installation

```bash
git clone https://github.com/yourusername/brand-name-generator
cd brand-name-generator
python venv venv # optional
source venv/bin/acrivate # optional
pip install -r requirements.txt
```

## Usage

Basic usage example:

```python
from brand_name_generator import BrandNameGenerator

# Initialize generator
generator = BrandNameGenerator(order=2)

# Train with data
generator.train(["Example", "Words"], weight=1.0)

# Generate names
print(generator.generate_word(temperature=0.5))
```

## Configuration

### General Settings

- `order`: Length of character sequences used in generation (default: 2)
- `min_length`: Minimum length of generated names (default: 3)
- `max_length`: Maximum length of generated names (default: 12)
- `temperature`: Controls randomness (0.0-1.0, lower = more conservative)

### Corpus Configuration

Train the model with different text corpora:

```python
# General vocabulary
generator.train(general_corpus(), weight=1.0)

# Brand names (weighted higher)
generator.train(brand_names, weight=10000)
```

### Letter Penalties

Customize character probabilities using the letter_penalties dictionary:

```python
generator.letter_penalties = {
    'ä': 0.2,  # Reduce frequency of 'ä'
    'x': 0.3,  # Reduce frequency of 'x'
    'r': 2.0   # Increase frequency of 'r'
}
```

Default penalties are configured for optimal brand name generation in English/Finnish.

## Advanced Usage

### Custom Corpus Integration

```python
# Load custom corpus
df = pd.read_csv('your_corpus.csv', sep='\t')
words = df["column_name"]
generator.train(words, weight=1.5)
```

### Multiple Training Sources

```python
# Layer different training sources with weights
generator.train(technical_terms, weight=0.5)
generator.train(existing_brands, weight=2.0)
generator.train(common_words, weight=1.0)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License

## Other useful tools
- https://www.domainnamesoup.com/six-letter-random-domain-names.php
