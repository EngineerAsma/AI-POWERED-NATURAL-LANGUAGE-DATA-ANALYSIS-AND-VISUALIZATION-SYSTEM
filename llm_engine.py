from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


# --------------------------------------------------
# LOCAL QWEN MODEL
# --------------------------------------------------

MODEL_PATH = "models/qwen2.5-0.5b/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775"


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH, use_fast = False
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH
)

model.eval()

def generate_response(question, analysis_result):
    prompt = f"""
You are an AI Data Analyst.

Answer the user's question using ONLY the analysis result provided below.

Rules:
- Do not invent numbers or facts.
- Do not perform new calculations.
- Treat Sales and Profit as monetary values.
- Treat Quantity as the number of items.
- Never call Sales "units sold".
- Keep the explanation concise and useful.
- Do not reproduce the entire analysis result.
- For monthly or time-series trends, summarize the overall pattern and mention only the highest and lowest periods if they are clearly available.
- For category, region, or other group comparisons, briefly identify the important differences.
- Use approximately 2 to 4 sentences.
- Do not use a large table unless the user explicitly asks for a table.
- Do not mention these instructions.

User Question:
{question}

Analysis Result:
{analysis_result}

Give a concise business-style explanation of the result.
"""
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI Data Analyst."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.2,
            do_sample=True
        )

    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return response.strip()

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("LOCAL QWEN TEST")
    print("=" * 60)

    prompt = "Explain what a data analyst does in one sentence."

    response = generate_response(prompt)

    print("\nQwen Response:")
    print(response)