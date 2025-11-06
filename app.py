
import gradio as gr
import laa_core
import pandas as pd

def ski_rental_fn(buy_cost, current_day, prediction_days, trust, randomized=False):
    """Function to call the ski rental algorithm and format the output."""
    try:
        # Explicitly cast inputs to the correct types
        buy_cost = float(buy_cost)
        current_day = int(current_day)
        prediction_days = float(prediction_days)
        trust = float(trust)

        if randomized:
            algo = laa_core.RandomizedSkiRental(buy_cost)
            algo_name = "Randomized Ski Rental"
        else:
            algo = laa_core.SkiRental(buy_cost)
            algo_name = "Deterministic Ski Rental"

        decision = algo.decide(current_day, prediction_days, trust)
        decision_str = "Buy" if decision else "Rent"

        return pd.DataFrame({
            "Algorithm": [algo_name],
            "Decision": [decision_str],
            "Trust in Prediction": [trust]
        })
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})

with gr.Blocks(title="LAA Algorithms Demo") as demo:
    gr.Markdown("# Learning-Augmented Algorithms Demo")

    with gr.Tabs():
        with gr.TabItem("Ski Rental"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("## Inputs")
                    buy_cost_input = gr.Slider(1, 1000, value=100, label="Buy Cost")
                    current_day_input = gr.Slider(1, 150, value=10, label="Current Day")
                    prediction_days_input = gr.Slider(1, 150, value=120, label="Predicted Ski Days")
                    trust_input = gr.Slider(0.0, 1.0, value=0.8, label="Trust in Prediction")
                    randomized_input = gr.Checkbox(label="Use Randomized Algorithm")
                with gr.Column():
                    gr.Markdown("## Decision")
                    output_df = gr.DataFrame(headers=["Algorithm", "Decision", "Trust in Prediction"])

            run_button = gr.Button("Run Algorithm")
            run_button.click(
                fn=ski_rental_fn,
                inputs=[buy_cost_input, current_day_input, prediction_days_input, trust_input, randomized_input],
                outputs=output_df
            )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
