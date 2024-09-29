from transformers import pipeline

def test_bert():
    fill_mask = pipeline("fill-mask", model="bert-base-uncased")
    sentence = "A inteligência artificial é muito [MASK]."
    result = fill_mask(sentence)

    for prediction in result:
        print(f"Opção: {prediction['sequence']} (Score: {prediction['score']})")

if __name__ == "__main__":
    test_bert()
