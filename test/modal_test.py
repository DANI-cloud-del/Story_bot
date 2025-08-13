from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class TextGenerator:
    def __init__(self, model_name='gpt2'):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)

    def generate_text(self, prompt, max_length=150, temperature=0.7, top_k=50, top_p=0.9):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)
        gen_kwargs = {
            "max_length": max_length,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "pad_token_id": self.tokenizer.eos_token_id,
            "no_repeat_ngram_size": 2,
            "do_sample": True,
        }
        with torch.no_grad():
            output_sequences = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                **gen_kwargs
            )
        generated_text = self.tokenizer.decode(output_sequences[0], skip_special_tokens=True)
        return generated_text

# Example usage with a better prompt and parameters:
prompt = (
    "Write a short, engaging, and positive story scene set in a tranquil forest where a brave "
    "hero meets a cunning villain. Include vivid descriptions, dialogue, and action fitting a peaceful atmosphere."
)

generator = TextGenerator()
story = generator.generate_text(prompt, max_length=200, temperature=0.75, top_k=40, top_p=0.9)
print("Generated Story:\n", story)
