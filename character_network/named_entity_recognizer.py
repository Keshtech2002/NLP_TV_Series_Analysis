from ast import literal_eval
import os
import pathlib
import sys
import pandas as pd
import spacy
from nltk.tokenize import sent_tokenize

# Correct dynamic path resolution using __file__
folder_path = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(folder_path.parent))

from utils import load_subtitles_dataset


class NamedEntityRecognizer:

    def __init__(self):
        self.nlp_model = self.load_model()

    def load_model(self):
        nlp = spacy.load("en_core_web_trf")
        return nlp

    def get_ners_inference(self, script):
        script_sentences = sent_tokenize(script)
        ner_output = []

        for sentence in script_sentences:
            doc = self.nlp_model(sentence)
            ners = set()
            for entity in doc.ents:
                if entity.label_ == "PERSON":
                    full_name = entity.text
                    first_name = full_name.split(" ")[0].strip()
                    ners.add(first_name)
            ner_output.append(ners)

        return ner_output

    def get_ners(self, dataset_path, save_path=None):
        # Read saved stub if it already exists
        if save_path is not None and os.path.exists(save_path):
            df = pd.read_csv(save_path)
            df["ners"] = df["ners"].apply(
                lambda x: literal_eval(x) if isinstance(x, str) else x
            )
            return df

        # Load dataset
        df = load_subtitles_dataset(dataset_path)

        # NOTE: Comment out or remove .head(10) when doing a full GPU run across all episodes
        # df = df.head(10)

        # Run Inference
        df["ners"] = df["script"].apply(self.get_ners_inference)

        # Save output
        if save_path is not None:
            df.to_csv(save_path, index=False)

        return df