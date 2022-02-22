from transformers import AutoModelForQuestionAnswering, AutoTokenizer


model_name = "deepset/roberta-base-squad2"
AutoModelForQuestionAnswering.from_pretrained(model_name).save_pretrained('./model')
AutoTokenizer.from_pretrained(model_name).save_pretrained('./model')