from llm_guard.model import Model
from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF
from llm_guard.output_scanners import Deanonymize
from llm_guard.vault import Vault

from config import PersistentConfig


class AIwallHelper:
    def __init__(self,PersistentConfig):
        self.vault = Vault()
        
        if isinstance(PersistentConfig,Config):
            # for debug - i.e. if config is manually instantiated in this file inside __main__
            self.config = PersistentConfig
        else:
            self.config = dict[str, PersistentConfig]
        self.entities = {
                    "LOCATION":self.config.location,
                    "DATE_TIME":False,
                    "CREDIT_CARD":False,
                    "CRYPTO":False,
                    "EMAIL_ADDRESS":False,
                    "IBAN_CODE":False,
                    "IP_ADDRESS":False,
                    "PERSON":self.config.location,
                    "PHONE_NUMBER":False,
                    "US_SSN":False,
                    "US_BANK_NUMBER":False,
                    "CREDIT_CARD_RE":False,
                    "UUID":False,
                    "EMAIL_ADDRESS_RE":False,
                    "US_SSN_RE":False,
                    "URL":False,
                    "ORGANIZATION":self.config.location
                    }
        self.entities_list = [key for key, value in self.entities.items() if value]
        self.anonymize = self.Anonymize(self.vault, self.entities_list)
        self.deanonymize = self.Deanonymize(self.vault)

    class Anonymize:
        def __init__(self, vault, entities_list):
            self.vault = vault

            NER_CONF = {
                "PRESIDIO_SUPPORTED_ENTITIES": entities_list,
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
                                     entity_types=entities_list,
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

class Config:
    # used for  running debug 
    def __init__(self, location):
        self.location = location
        self.date_time = True
        self.credit_card = True
        self.crypto = True
        self.email_address = True
        self.iban_code = True
        self.ip_address = True
        self.person = True
        self.phone_number = True
        self.us_ssn = True
        self.us_bank_number = True
        self.credit_card_re = True
        self.uuid = True
        self.email_address_re = True
        self.us_ssn_re = True
        self.url = True
        self.organization = True
        
if __name__ == '__main__':
    # Usage
    config = Config(location=True)
    helper = AIwallHelper(config)
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
