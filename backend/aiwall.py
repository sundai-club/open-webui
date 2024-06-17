from llm_guard.model import Model
from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF
from llm_guard.output_scanners import Deanonymize
from llm_guard.vault import Vault

from config import PersistentConfig


class AIwallHelper:
    def __init__(self, config):
        self.vault = Vault()
        self.config = config
        print("/n/n CONFIG!")
        print(config)
        attributes = dir(config)
        # Filter out special methods and callables, and print each field
        for attr in attributes:
            if not attr.startswith("__") and not callable(getattr(config, attr)):
                value = getattr(config, attr)
                print(f"{attr}: {value}")
        print("MORE STUFF!!!!")
        # self.entities = {
        #     "LOCATION": self.config.MASK_LOCATION,
        #     "DATE_TIME": False,
        #     "CREDIT_CARD": self.config.MASK_CREDIT_CARD,
        #     "CRYPTO": self.config.MASK_CRYPTO,
        #     "EMAIL_ADDRESS": self.config.MASK_EMAIL_ADDRESS,
        #     "IBAN_CODE": self.config.MASK_IBAN_CODE,
        #     "IP_ADDRESS": self.config.MASK_IP_ADDRESS,
        #     "PERSON": self.config.MASK_PERSON,
        #     "PHONE_NUMBER": self.config.MASK_PHONE_NUMBER,
        #     "US_SSN": self.config.MASK_US_SSN,
        #     "US_BANK_NUMBER": self.config.MASK_US_BANK_NUMBER,
        #     "CREDIT_CARD_RE": self.config.MASK_CREDIT_CARD_RE,
        #     "UUID": self.config.MASK_UUID,
        #     "EMAIL_ADDRESS_RE": self.config.MASK_EMAIL_ADDRESS_RE,
        #     "US_SSN_RE": self.config.MASK_US_SSN_RE,
        #     "URL": self.config.MASK_URL,
        #     "ORGANIZATION": self.config.MASK_COMPANY
        # }
        self.anonymize = self.Anonymize(vault=self.vault, config=self.config)
        self.deanonymize = self.Deanonymize(self.vault)

    class Anonymize:
        def __init__(self, vault, config):
            self.vault = vault
            self.config = config

        #     entities = {
        #     "LOCATION": self.config.MASK_LOCATION if self.config.MASK_LOCATION is not None else True,
        #     "DATE_TIME": False,
        #     "CREDIT_CARD": self.config.MASK_CREDIT_CARD,
        #     "CRYPTO": self.config.MASK_CRYPTO,
        #     "EMAIL_ADDRESS": self.config.MASK_EMAIL_ADDRESS,
        #     "IBAN_CODE": self.config.MASK_IBAN_CODE,
        #     "IP_ADDRESS": self.config.MASK_IP_ADDRESS,
        #     "PERSON": self.config.MASK_PERSON,
        #     "PHONE_NUMBER": self.config.MASK_PHONE_NUMBER,
        #     "US_SSN": self.config.MASK_US_SSN,
        #     "US_BANK_NUMBER": self.config.MASK_US_BANK_NUMBER,
        #     "CREDIT_CARD_RE": self.config.MASK_CREDIT_CARD_RE,
        #     "UUID": self.config.MASK_UUID,
        #     "EMAIL_ADDRESS_RE": self.config.MASK_EMAIL_ADDRESS_RE,
        #     "US_SSN_RE": self.config.MASK_US_SSN_RE,
        #     "URL": self.config.MASK_URL,
        #     "ORGANIZATION": self.config.MASK_COMPANY
        # }
            print("/n IN anon/n")

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
                                         "URL",
                                         "ORGANIZATION",
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
                                         "URL",
                                         "ORGANIZATION",
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
    from IPython import embed; embed()    


    ### ANONIMIZE KEY FAIL & SUCCESS CASES to fix 
    # fails to locate street and town
    anonymized_prompt = helper.anonymize("Your input string here: my location is 32 vernon street, brookline MA")
    print(anonymized_prompt)
    # succeeds to locate street and town 
    anonymized_prompt = helper.anonymize("Your input string here: my location is 32 Vernon Street, Brookline MA")
    print(anonymized_prompt)

    ### DEANONIMIZE KEY FAIL & SUCCESS CASES to fix 
    # works 
    deanonymized_output = helper.deanonymize(anonymized_prompt, "Your answer string here: [REDACTED_LOCATION_1] and then [REDACTED_LOCATION_2]")
    # doesn't work 
    deanonymized_output = helper.deanonymize(anonymized_prompt, "Your answer string here: REDACTED_LOCATION_1 and then REDACTED_LOCATION_2")
    anonymized_sundai = helper.anonymize_sundai("Your sundai prompt here")
