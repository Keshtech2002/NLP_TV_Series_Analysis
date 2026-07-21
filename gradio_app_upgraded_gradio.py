import gradio as gr
import pandas as pd
from theme_classifier import ThemeClassifier


def get_themes(theme_list_str, subtitles_path, save_path):
    theme_list = theme_list_str.split(",")
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)

    # Remove dialogue from the theme list
    theme_list = [theme for theme in theme_list if theme != "dialogue"]
    output_df = output_df[theme_list]

    output_df = output_df[theme_list].sum().reset_index()
    output_df.columns = ["Theme", "Score"]

    # In modern Gradio (6.0+), returning gr.BarPlot(value=...) updates the component
    # 'vertical' is removed and width/height controls are passed via container attributes
    output_chart = gr.BarPlot(
        value=output_df,
        x="Theme",
        y="Score",
        title="Series Themes",
        tooltip=["Theme", "Score"],
        container=True,
    )

    return output_chart


def main():
    # Title is passed in gr.Blocks; theme is moved to launch() for Gradio 6.0
    with gr.Blocks(title="TV Series Theme Analysis") as iface:
        gr.Markdown(
            """
            # 🎬 TV Series Theme Classification
            Analyze episode transcripts or subtitles using Zero-Shot NLP Classifiers.
            """
        )

        with gr.Row():
            # Left Column: Inputs & Controls
            with gr.Column(scale=1):
                theme_list_input = gr.Textbox(
                    label="Themes (comma-separated)",
                    placeholder="battle, friendship, sacrifice, betrayal",
                    value="battle, friendship, sacrifice, betrayal",
                )
                subtitles_path_input = gr.Textbox(
                    label="Subtitles / Script Directory Path",
                    placeholder="data/subtitles",
                )
                save_path_input = gr.Textbox(
                    label="Save Path (CSV output)",
                    placeholder="stubs/theme_classifier_output.csv",
                )

                get_themes_button = gr.Button("Analyze Themes", variant="primary")

            # Right Column: Visual Output
            with gr.Column(scale=2):
                plot_output = gr.BarPlot(
                    value=None,
                    x="Theme",
                    y="Score",
                    title="Series Themes Distribution",
                    tooltip=["Theme", "Score"],
                    height=350,
                )

        # Wire click event
        get_themes_button.click(
            fn=get_themes,
            inputs=[theme_list_input, subtitles_path_input, save_path_input],
            outputs=[plot_output],
        )

    # Pass theme and share parameters into launch() as required by Gradio 6.0+
    iface.launch(share=True, theme=gr.themes.Soft())


if __name__ == "__main__":
    main()