import gradio as gr
import pandas as pd
from character_network import CharacterNetworkGenerator, NamedEntityRecognizer
from theme_classifier import ThemeClassifier
from text_classification import JutsuClassifier

import os

# ==========================================
# 1. Event Handler Functions
# ==========================================


def get_themes(theme_list_str, subtitles_path, save_path):
    # Parse theme inputs and strip whitespace and extra quotation marks
    theme_list = [
        t.strip().strip('"').strip("'")
        for t in theme_list_str.split(",")
        if t.strip()
    ]

    # Run theme classification pipeline
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)

    # Remove 'dialogue' column if present
    theme_list = [theme for theme in theme_list if theme != "dialogue"]
    output_df = output_df[theme_list]

    # Aggregate scores for visualization
    aggregated_df = output_df[theme_list].sum().reset_index()
    aggregated_df.columns = ["Theme", "Score"]

    # Return updated gr.BarPlot component with values
    return gr.BarPlot(
        value=aggregated_df,
        x="Theme",
        y="Score",
        title="Series Themes",
        tooltip=["Theme", "Score"],
        container=True,
    )


def get_character_network(subtitles_path, ner_path):
    # Extract NERs from subtitles
    ner = NamedEntityRecognizer()
    ner_df = ner.get_ners(subtitles_path, ner_path)

    # Generate network graph HTML
    character_network_generator = CharacterNetworkGenerator()
    relationship_df = character_network_generator.generate_character_network(
        ner_df
    )
    html = character_network_generator.draw_network_graph(relationship_df)

    # Return HTML string directly to update gr.HTML component
    return html


def classify_text(text_classifcation_model, text_classifcation_data_path, text_to_classify):
    jutsu_classifier = JutsuClassifier(
        model_path=text_classifcation_model,
        data_path=text_classifcation_data_path,
        huggingface_token=os.getenv("huggingface_token"),
    )

    output = jutsu_classifier.classify_jutsu(text_to_classify)

    # Extract the key with the highest score (e.g., 'Ninjutsu')
    if isinstance(output, dict) and output:
        return max(output, key=output.get)
    
    return output  # <-- Return output directly (no [0])


# ==========================================
# 2. Gradio App Layout
# ==========================================


def main():
    with gr.Blocks(title="TV Series Analysis System") as iface:
        gr.Markdown(
            """
            # 🎬 TV Series Analysis System
            Analyze narrative themes and extract interactive character relationship networks.
            """
        )

        # ------------------------------------------
        # Section 1: Theme Classification
        # ------------------------------------------
        gr.Markdown("## 📊 Theme Classification (Zero Shot Classifiers)")
        with gr.Row():
            # Left Column: Inputs & Controls
            with gr.Column(scale=1):
                theme_list_input = gr.Textbox(
                    label="Themes (comma-separated)",
                    placeholder="friendship,hope,sacrifice,battle,self development,betrayal,love,dialogue",
                    value="friendship,hope,sacrifice,battle,self development,betrayal,love,dialogue",
                )
                subtitles_path_input1 = gr.Textbox(
                    label="Subtitles or Script Directory Path",
                    placeholder="/content/data/Subtitles",
                )
                save_path_input1 = gr.Textbox(
                    label="Save Path (CSV output)",
                    placeholder="/content/analyze_series_with_NLP/stubs/theme_classifier_output.csv",
                )
                get_themes_button = gr.Button(
                    "Get Themes", variant="primary"
                )

            # Right Column: Visual Output Plot
            with gr.Column(scale=2):
                plot_output = gr.BarPlot(
                    value=None,
                    x="Theme",
                    y="Score",
                    title="Series Themes Distribution",
                    tooltip=["Theme", "Score"],
                    height=350,
                )

        # Wire Theme Button Click Event
        get_themes_button.click(
            fn=get_themes,
            inputs=[
                theme_list_input,
                subtitles_path_input1,
                save_path_input1,
            ],
            outputs=[plot_output],
        )

        gr.HTML("<hr>")

        # ------------------------------------------
        # Section 2: Character Network (NERs and Graphs)
        # ------------------------------------------
        gr.Markdown("## 🕸️ Character Network (NERs and Graphs)")
        with gr.Row():
            # Left Column: Inputs & Controls
            with gr.Column(scale=1):
                subtitles_path_input2 = gr.Textbox(
                    label="Subtitles or Script Directory Path",
                    placeholder="/content/data/Subtitles",
                )
                ner_path_input = gr.Textbox(
                    label="NERs Save Path (CSV output)",
                    placeholder="/content/analyze_series_with_NLP/stubs/ner_output.csv",
                )
                get_network_graph_button = gr.Button(
                    "Get Character Network", variant="primary"
                )

            # Right Column: HTML Network Graph Output
            with gr.Column(scale=2):
                network_html_output = gr.HTML(
                    label="Interactive Character Network"
                )

        # Wire Character Network Button Click Event
        get_network_graph_button.click(
            fn=get_character_network,
            inputs=[subtitles_path_input2, ner_path_input],
            outputs=[network_html_output],
        )

        gr.HTML("<hr>")

        # ------------------------------------------
        # Section 3: Text Classification with LLMs
        # ------------------------------------------
        gr.Markdown("## 🤖 Text Classification with LLMs")
        with gr.Row():
            # Left Column: Inputs & Controls
            with gr.Column(scale=1):
                text_classifcation_model = gr.Textbox(
                    label="Model Path",
                    placeholder="KeshtechABU/jutsu_classifier",
                )
                text_classifcation_data_path = gr.Textbox(
                    label="Data Path",
                    placeholder="/content/data/jutsus.jsonl",
                )
                text_to_classify = gr.Textbox(
                    label="Text input",
                    lines=4,
                    placeholder="The Rasengan is an A-rank, close-range ninjutsu.",
                )
                classify_text_button = gr.Button(
                    "Classify Text (Jutsu)", variant="primary"
                )

            # Right Column: Text Output
            with gr.Column(scale=2):
                text_classification_output = gr.Textbox(
                    label="Text Classification Output",
                    lines=4,
                )

        # Wire Text Classification Button Click Event
        classify_text_button.click(
            fn=classify_text,
            inputs=[
                text_classifcation_model,
                text_classifcation_data_path,
                text_to_classify,
            ],
            outputs=[text_classification_output],
        )

    # Launch interface (passing theme in launch() for Gradio 6.0+)
    iface.launch(share=True, theme=gr.themes.Soft())


if __name__ == "__main__":
    main()