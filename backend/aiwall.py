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
            self.scanner = Anonymize(self.vault, preamble="",
                                entity_types=["PHONE_NUMBER", "ORGANIZATION", "LOCATION"],
                                allowed_names=["John Doe"], hidden_names=["Test LLC"],
                                recognizer_conf=BERT_LARGE_NER_CONF, language="en")
            

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

if __name__=='__main__':
    # Usage
    helper = AIwallHelper()
    from IPython import embed; embed()
    
    # fails to locate street and town
    anonymized_prompt = helper.anonymize("Your input string here: my location is 32 vernon street, brookline MA")
    
    # succeeds to locate street and town 
    anonymized_prompt = helper.anonymize("Your input string here: my location is 32 Vernon Street, Brookline MA")
    print(anonymized_prompt)
    deanonymized_output = helper.deanonymize(anonymized_prompt, "Your answer string here")
    anonymized_sundai = helper.anonymize_sundai("Your sundai prompt here")
