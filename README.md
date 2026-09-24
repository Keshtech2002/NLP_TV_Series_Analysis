# 🎬 NLP TV Series Analysis

> A full-stack NLP and graph analytics project for analyzing anime and TV series narratives using subtitle data, zero-shot classification, named entity recognition, social graph extraction, text classification, and a conversational character chatbot.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Gradio](https://img.shields.io/badge/Gradio-4%2B-orange?style=flat-square)
![PyTorch](https://img.shields.io/badge/PyTorch-Enabled-red?style=flat-square)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=flat-square)
![spaCy](https://img.shields.io/badge/spaCy-NER-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active%20Research%20Project-purple?style=flat-square)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Why This Project Exists](#why-this-project-exists)
- [Core Features](#core-features)
- [Project Architecture](#project-architecture)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [Data Pipeline](#data-pipeline)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [How to Run the Application](#how-to-run-the-application)
- [Detailed Component Breakdown](#detailed-component-breakdown)
- [Training and Model Workflow](#training-and-model-workflow)
- [What Was Done From Start to Finish](#what-was-done-from-start-to-finish)
- [Usage Examples](#usage-examples)
- [Known Limitations and Future Improvements](#known-limitations-and-future-improvements)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

This project is a multi-module NLP system designed to analyze long-form TV series content, especially anime subtitles, and transform raw dialogue into structured insights.

The goal was not just to process text, but to build an end-to-end story intelligence pipeline capable of:

- identifying the dominant narrative themes in a series,
- extracting characters and co-occurrence relationships,
- understanding the semantic meaning of text using classification models,
- assembling a character-based chatbot persona,
- and presenting everything through a user-friendly Gradio interface.

The project uses subtitle files from a series dataset and converts them into structured transcripts for analysis. It then applies natural language processing, graph analysis, and transformer-based models to derive insights that would otherwise be difficult to see from raw scripts alone.

This is a research-style project with real-world storytelling, graph analytics, and machine learning components tied together in one workflow.

---

## Why This Project Exists

A TV series is more than dialogue. It contains:

- recurring themes such as friendship, betrayal, love, sacrifice, and conflict,
- emotional arcs across multiple episodes,
- relationships between characters that evolve over time,
- important lore or specialized vocabulary such as jutsu, techniques, and powers,
- and character identity that can be modeled through chat interactions.

This project was built to explore how textual data from subtitles can be converted into:

1. objective analytics,
2. narrative summaries,
3. relationship graphs,
4. behavioral models,
5. and interactive AI experiences.

It sits at the intersection of NLP, graph mining, transformer-based classification, and conversational AI.

---

## Core Features

### 1. Theme Classification

The system uses zero-shot classification with a transformer model to evaluate subtitle content against a user-defined set of themes, such as:

- friendship
- hope
- sacrifice
- battle
- love
- betrayal
- self development
- dialogue

This allows the model to infer theme relevance without training a custom classifier for every concept.

Files involved:

- `theme_classifier/theme_classifier.py`
- `gradio_app.py`
- `gradio_app_colab.py`

### 2. Character Network Generation

The project extracts named entities from subtitles and builds a network of character relationships based on co-occurrence within text windows. These relationships are then visualized using a graph and rendered as an HTML network.

This supports analysis such as:

- who appears with whom,
- who is central in the narrative,
- which characters are repeatedly connected,
- how relationship strength evolves across episodes.

Files involved:

- `character_network/named_entity_recognizer.py`
- `character_network/character_netowork_generator.py`

### 3. Jutsu Text Classification

The project also includes a specialized text classification pipeline for identifying jutsu categories such as:

- Ninjutsu
- Genjutsu
- Taijutsu

This creates a semantic understanding layer for Naruto-inspired content and demonstrates how domain-specific classification can be used on textual descriptions.

Files involved:

- `text_classification/jutsu_classifier.py`
- `text_classification/cleaner.py`
- `text_classification/training_utils.py`
- `text_classification/custom_trainer.py`

### 4. Character Chatbot

A chatbot component was developed to simulate a character persona from the series. The model is trained or loaded from a Hugging Face model repository and fine-tuned on character dialogue data.

This is a conversational interface built to mirror a character voice rather than simply answer generic questions.

Files involved:

- `character_chatbot/character_chatbot.py`
- `character_chatbot/__init__.py`

### 5. Data Collection and Curation

The project also includes a crawler that scrapes structured information from fandom-style content pages to collect jutsu descriptions and metadata.

Files involved:

- `crawler/jutsu_crawler.py`

### 6. Gradio Interface

The repo contains multiple Gradio app entry points for interaction:

- `gradio_app.py` — local desktop-style Gradio app
- `gradio_app_colab.py` — Google Colab-friendly version

These provide a web UI for:

- theme analysis,
- character network exploration,
- jutsu classification,
- and character chat.

---

## Project Architecture

The project is organized into clear functional modules.

### High-Level Flow

```text
Subtitle Dataset
     ↓
Data Loader
     ↓
Theme Classifier
     ↓
NER + Character Graph Builder
     ↓
Jutsu Classifier
     ↓
Character Chatbot
     ↓
Gradio Frontend
```

### Architectural Principles

- modularity: each feature is separated into logical packages,
- end-to-end pipeline: raw subtitles become structured intelligence,
- extensibility: new themes or models can be added with minimal change,
- experiment-first design: notebooks and scripts support iterative development,
- cloud-ready model workflow: Hugging Face integration supports remote model loading and push to hub.

---

## Technology Stack

### Core Libraries

- Python 3.10+
- PyTorch
- Hugging Face Transformers
- spaCy
- NetworkX
- PyVis
- Gradio
- Pandas
- NumPy
- scikit-learn
- BeautifulSoup
- Scrapy
- python-dotenv

### NLP / ML Tools

- zero-shot classification via `facebook/bart-large-mnli`
- transformer-based text classification with `distilbert-base-uncased`
- LoRA-based fine-tuning for a GPT-style character model
- quantized inference via BitsAndBytes
- sentence tokenization with NLTK

### Visualization

- HTML graph output for character networks
- Bar plots for theme distributions
- UI dashboard via Gradio

---

## Repository Structure

```text
NLP_TV_Series_Analysis/
├── README.md
├── requirements.txt
├── gradio_app.py
├── gradio_app_colab.py
├── rough.txt
├── example_html.html
├── .env
├── .env_example
├── .gitignore
│
├── character_chatbot/
│   ├── __init__.py
│   ├── character_chatbot.py
│   └── character_chatbot_development.ipynb
│
├── character_network/
│   ├── __init__.py
│   ├── named_entity_recognizer.py
│   ├── character_netowork_generator.py
│   ├── character_network_generator.ipynb
│   └── naruto.html
│
├── crawler/
│   ├── jutsu_crawler.py
│   └── jutsu_crawler_tutorial.md
│
├── data/
│   ├── download_link.txt
│   ├── jutsus.jsonl
│   ├── musab.jsonl
│   ├── naruto.csv
│   └── Subtitles/
│
├── stubs/
│   ├── ner_output.csv
│   ├── stubs_folder.txt
│   └── theme_classifier_output.csv
│
├── text_classification/
│   ├── __init__.py
│   ├── cleaner.py
│   ├── custom_trainer.py
│   ├── jutsu_classfier_development.ipynb
│   ├── jutsu_classifier.py
│   └── training_utils.py
│
├── theme_classifier/
│   ├── __init__.py
│   ├── theme_classifier.py
│   ├── analyze_your_favorite_series_develoment.ipynb
│   └── theme_classification_development.ipynb
│
└── utils/
    ├── __init__.py
    └── data_loader.py
```

---

## Data Pipeline

### Subtitle Loading

The onboarding pipeline starts with subtitle files stored in `data/Subtitles/`.

The loader reads `.ass` or `.srt` subtitle files and processes them into a tabular structure containing:

- `episode`
- `script`

This is done in `utils/data_loader.py`.

### Theme Extraction

The subtitle text is chunked into sentences and passed to a zero-shot classification pipeline. Each sentence or batch of sentences is evaluated across a set of labels to compute scores for each theme.

The final output is transformed into a DataFrame and saved to CSV when `save_path` is specified.

### Character Recognition

The NER component uses spaCy's transformer-based English model (`en_core_web_trf`) to detect `PERSON` entities. It extracts first names from named entities and builds a set of entities per sentence. These are then used to create character relationship edges.

### Character Graph Construction

The graph builder iterates over a sliding window of sentences and builds pairwise relationships between characters appearing in close proximity. Each edge is counted and grouped, then visualized as a network graph.

### Jutsu Classification

The model loads and optionally trains a text classifier using jutsu metadata scraped from fandom-like data sources. It preprocesses the description text, encodes labels, trains a model, and then uses the trained checkpoint or a remote model for inference.

### Chatbot Training

A character persona model is trained from conversational transcript data, where context windows are formed from prior dialogue lines and responses. The system uses a causal LM and LoRA adaptation to create a style-specific character chatbot.

---

## Installation

### 1. Clone the Project

```bash
git clone https://github.com/your-username/NLP_TV_Series_Analysis.git
cd NLP_TV_Series_Analysis
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If needed, install the spaCy model separately:

```bash
python -m spacy download en_core_web_trf
```

---

## Environment Setup

The project relies on a `.env` file for secrets and model credentials.

A sample file is provided in:

- `.env_example`

Example:

```env
huggingface_token=your_huggingface_token_here
```

This token is required if the project needs to access private models or push models to Hugging Face Hub.

Important note:

- do not commit your real token to GitHub,
- keep `.env` in `.gitignore`,
- use `.env_example` as a template for local setup.

---

## How to Run the Application

### Local Gradio App

```bash
python gradio_app.py
```

### Colab-Friendly Version

```python
!python gradio_app_colab.py
```

The application exposes interactive sections for:

- theme analysis,
- character network generation,
- text classification,
- and character chat.

---

## Detailed Component Breakdown

### `theme_classifier/theme_classifier.py`

This module:

- initializes a zero-shot classifier,
- tokenizes subtitle content into sentence batches,
- generates scores across user-selected labels,
- returns a theme score DataFrame,
- optionally saves results to CSV for later use.

### `character_network/named_entity_recognizer.py`

This module:

- loads a spaCy transformer-based model,
- extracts person entities from subtitle text,
- reduces entities to first-name representations,
- converts results into structured output for graph construction.

### `character_network/character_netowork_generator.py`

This module:

- builds character-to-character relationships using windows of dialogue,
- counts the frequency of each co-occurrence,
- creates a graph using NetworkX,
- renders the graph as interactive HTML using PyVis.

### `text_classification/jutsu_classifier.py`

This module:

- loads or trains a DistilBERT classifier,
- preprocesses jutsu descriptions and labels,
- performs training if a hub model is missing,
- classifies input text into output categories such as `Ninjutsu`, `Taijutsu`, and `Genjutsu`.

### `character_chatbot/character_chatbot.py`

This module:

- loads a character-specific LLM or trains one if needed,
- formats a persona prompt and conversation history,
- uses LoRA + quantized inference for efficient generation,
- returns a character-style generated response.

### `crawler/jutsu_crawler.py`

This module:

- crawls fandom or wiki pages,
- extracts jutsu names,
- collects classification and textual descriptions,
- organizes data for model training and downstream analysis.

---

## Training and Model Workflow

### Theme Model

The theme classifier uses:

```text
facebook/bart-large-mnli
```

This is a robust zero-shot model that can classify text based on semantic similarity between the input and theme labels. It does not require dedicated training for each new theme list.

### NER Model

The character extraction pipeline uses:

```text
en_core_web_trf
```

This is a transformer-based English spaCy model intended for high-quality named entity recognition.

### Jutsu Classification Model

This project uses a transformer model stack that can train a classifier on jutsu metadata. The pipeline includes:

- label encoding,
- cleaned text processing,
- dataset creation,
- training arguments,
- metrics evaluation,
- and model upload to Hugging Face Hub when configured.

### Character Chatbot

The chatbot uses a base LLM such as Meta-Llama 3 and applies LoRA-style fine-tuning with quantized loading for efficiency. The training data is built from Naruto-style conversational segments, and the final model is saved and optionally pushed to Hugging Face.

---

## What Was Done From Start to Finish

### Phase 1: Project Initialization

The project was set up as a modular AI and NLP research repo with separate folders for:

- text classification,
- character analysis,
- theme extraction,
- chatbot logic,
- crawling tools,
- data collection,
- and UI interfaces.

This created a clean structure that supports experimentation and scaling.

### Phase 2: Data Acquisition and Preparation

The repository includes:

- subtitle data in `data/Subtitles/`,
- jutsu data in `data/jutsus.jsonl`,
- transcript-style data in `data/naruto.csv`,
- and metadata such as downloads, stubs, and saved outputs.

The data loader standardizes this content into structured DataFrames for downstream modeling.

### Phase 3: Theme Analysis Pipeline

A zero-shot theme detection pipeline was built to analyze subtitle scripts and calculate theme scores over long episodes or series. This was one of the core narrative intelligence pieces of the project.

### Phase 4: Character Relationship Modeling

Using named entity recognition, the project extracted people appearing together in the same narrative contexts and converted that into a connected network of entities.

This created a graph-based representation of character relationships and influence.

### Phase 5: Text Classification for Jutsu

A specialized classifier was created to categorize jutsu descriptions into semantic classes. This introduced a domain-specific example of NLP classification on narrative content.

### Phase 6: Character Chatbot Development

The project embedded a conversational persona layer using large language model fine-tuning and prompt engineering. The chatbot focuses on producing a character-like response grounded in anime dialogue style.

### Phase 7: Data Crawling

The crawler was built to fetch structured jutsu information programmatically from web sources so that the project could create or enrich its dataset without manual collection.

### Phase 8: Gradio Interface

The final stage connected all modules into a web interface where the user can interactively:

- inspect theme distributions,
- generate relationship graphs,
- classify text,
- and chat with a character persona.

This is the part that makes the project usable outside notebook-only experimentation.

---

## Usage Examples

### Example 1: Theme Analysis

```python
from theme_classifier import ThemeClassifier

themes = ["friendship", "hope", "sacrifice", "battle", "betrayal", "love"]
model = ThemeClassifier(themes)
output = model.get_themes("/path/to/Subtitles", "/path/to/save.csv")
print(output.head())
```

### Example 2: Character Network Extraction

```python
from character_network import NamedEntityRecognizer, CharacterNetworkGenerator

ner = NamedEntityRecognizer()
ner_df = ner.get_ners("/path/to/Subtitles", "/path/to/ner_output.csv")

network_gen = CharacterNetworkGenerator()
relationship_df = network_gen.generate_character_network(ner_df)
html = network_gen.draw_network_graph(relationship_df)
print(html[:200])
```

### Example 3: Jutsu Classification

```python
from text_classification import JutsuClassifier

model = JutsuClassifier(
    model_path="KeshtechABU/jutsu_classifier",
    data_path="/path/to/data.jsonl",
    huggingface_token="YOUR_TOKEN",
)

result = model.classify_jutsu("The Rasengan is a close-range ninjutsu used for rapid chakra compression.")
print(result)
```

### Example 4: Character Chat

```python
from character_chatbot import CharacterChatbot

chatbot = CharacterChatbot(model_path="your-model-name", huggingface_token="YOUR_TOKEN")
response = chatbot.chat("What is your dream?", [])
print(response)
```

---

## Known Limitations and Future Improvements

### Current Limitations

- heavy GPU usage may be required for model inference and training,
- some modules assume specific folder structures and file formats,
- NER can be noisy for long anime dialogue due to naming variations,
- the character chatbot quality depends strongly on the training data,
- some models may require Hugging Face authentication,
- the network graph can become visually cluttered for large datasets.

### Planned Improvements

- improve episode-level narrative summaries,
- add stronger relationship weighting and temporal graph analysis,
- add more robust cleaning for subtitles and OCR-like text noise,
- expand jutsu taxonomy and dataset quality,
- integrate a dedicated front-end dashboard,
- add evaluation metrics and benchmarking,
- containerize the app with Docker,
- support deployment as a Streamlit or FastAPI service.

---

## Contributing

Contributions are welcome.

You can contribute by:

- improving the data cleaning pipeline,
- adding new analysis modules,
- improving model accuracy,
- refining the UI,
- documenting training workflows,
- and helping with dataset preparation.

Recommended workflow:

```bash
git checkout -b feature/your-feature
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

---

## License

This project is currently intended for research and educational use. If you are planning to publish or reuse it commercially, confirm the licenses for third-party models, datasets, and scraped data before distribution.

---

## Final Note

This project demonstrates how a series of raw subtitle files can be transformed into actionable AI-driven storytelling insights. It merges language understanding, graph analysis, and conversational AI into a single practical workflow.

The goal was to build more than just a model: it was to build an end-to-end storytelling analysis system that can interpret narrative content semantically and present it in an interactive, user-friendly way.

---

## Project Status

This project is best described as an active, research-driven NLP and AI analytics system with working components in:

- textual theme analysis,
- graph-based relationship extraction,
- domain text classification,
- and interactive conversational AI.

The combination of these components makes it a strong foundation for future expansion into a larger multi-modal entertainment analytics platform.
