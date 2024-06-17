from llm_guard.model import Model
from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF
from llm_guard.output_scanners import Deanonymize
from llm_guard.vault import Vault


class AIwallHelper:
    def __init__(self):
        self.vault = Vault()
        self.anonymize = self.Anonymize(self.vault)
        self.deanonymize = self.Deanonymize(self.vault)

    class Anonymize:
        def __init__(self, vault):
            self.vault = vault

            NER_CONF = {
                "PRESIDIO_SUPPORTED_ENTITIES": [
                                         "LOCATION",
                                         "DATE_TIME",
                                         "CREDIT_CARD",
                                         "CRYPTO",
                                         "EMAIL_ADDRESS",
                                         "IBAN_CODE",
                                         "IP_ADDRESS",
                                         "PERSON",
                                         "PHONE_NUMBER",
                                         "US_SSN",
                                         "US_BANK_NUMBER",
                                         "CREDIT_CARD_RE",
                                         "UUID",
                                         "EMAIL_ADDRESS_RE",
                                         "US_SSN_RE",
                                     ],
                "DEFAULT_MODEL": Model(
                    path="dslim/bert-large-NER",
                    revision="13e784dccceca07aee7a7aab4ad487c605975423",
                    onnx_path="dslim/bert-large-NER",
                    onnx_revision="13e784dccceca07aee7a7aab4ad487c605975423",
                    onnx_subfolder="onnx",
                    pipeline_kwargs={
                        "aggregation_strategy": "simple",
                    },
                    tokenizer_kwargs={"model_input_names": ["input_ids", "attention_mask"]},
                ),
                "LABELS_TO_IGNORE": ["O", "CARDINAL"],
                "DEFAULT_EXPLANATION": "Identified as {} by the dslim/bert-large-NER NER model",
                "DATASET_TO_PRESIDIO_MAPPING": {
                    "MISC": "O",
                    "LOC": "LOCATION",
                    "ORG": "ORGANIZATION",
                    "PER": "PERSON",
                },
                "MODEL_TO_PRESIDIO_MAPPING": {
                    "MISC": "O",
                    "LOC": "LOCATION",
                    "ORG": "ORGANIZATION",
                    "PER": "PERSON",
                },
                "CHUNK_OVERLAP_SIZE": 40,
                "CHUNK_SIZE": 600,
                "ID_SCORE_MULTIPLIER": 0.3,
                "ID_ENTITY_NAME": "ID",
            }

            self.scanner = Anonymize(self.vault, preamble="",
                                     entity_types=[
                                         "LOCATION",
                                         "DATE_TIME",
                                         "CREDIT_CARD",
                                         "CRYPTO",
                                         "EMAIL_ADDRESS",
                                         "IBAN_CODE",
                                         "IP_ADDRESS",
                                         "PERSON",
                                         "PHONE_NUMBER",
                                         "US_SSN",
                                         "US_BANK_NUMBER",
                                         "CREDIT_CARD_RE",
                                         "UUID",
                                         "EMAIL_ADDRESS_RE",
                                         "US_SSN_RE",
                                     ],
                                     allowed_names=["John Doe"],
                                     recognizer_conf=NER_CONF, language="en")

        def __call__(self, input: str):
            sanitized_prompt, is_valid, risk_score = self.scanner.scan(input)
            return sanitized_prompt

    class Deanonymize:
        def __init__(self, vault):
            self.vault = vault
            self.scanner = Deanonymize(self.vault)

        def __call__(self, sanitized_prompt: str, answer: str):
            sanitized_model_output, is_valid, risk_score = self.scanner.scan(sanitized_prompt, answer)
            return sanitized_model_output

    def anonymize_sundai(self, prompt: str):
        return self.anonymize(prompt)


if __name__ == '__main__':
    # Usage
    helper = AIwallHelper()

    # fails to locate street and town
    anonymized_prompt = helper.anonymize("Your input string here: my location is 32 vernon street, brookline MA")
    print(anonymized_prompt)

    # succeeds to locate street and town 
    anonymized_prompt = helper.anonymize("Your input string here: my location is 32 Vernon Street, Brookline MA")
    print(anonymized_prompt)
    deanonymized_output = helper.deanonymize(anonymized_prompt, "Your answer string here")
    anonymized_sundai = helper.anonymize_sundai("Your sundai prompt here")
