from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF
# from langfuse.decorators import observe, langfuse_context
from llm_guard.output_scanners import Deanonymize
from llm_guard.vault import Vault

vault = Vault()

# @observe()
def anonymize(input: str):
  scanner = Anonymize(vault, preamble="[Insert before prompt]\n",
                      entity_types = ["PHONE_NUMBER", "ORGANIZATION", "LOCATION"], allowed_names=["John Doe"], hidden_names=["Test LLC"],
                    recognizer_conf=BERT_LARGE_NER_CONF, language="en")
  sanitized_prompt, is_valid, risk_score = scanner.scan(input)
  return sanitized_prompt

# @observe()
def deanonymize(sanitized_prompt: str, answer: str):
  scanner = Deanonymize(vault)
  sanitized_model_output, is_valid, risk_score = scanner.scan(sanitized_prompt, answer)

  return sanitized_model_output





# @observe()
def anonymize_sundai(prompt: str):
  return anonymize(prompt)

