import asyncio
import json
from llm_guard.model import Model
from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF
from llm_guard.output_scanners import Deanonymize
from llm_guard.vault import Vault
from llm_guard import scan_output, scan_prompt

from config import PersistentConfig

NER_CONF = {
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


class AIwallHelper:
    def __init__(self, config):
        self.vault = Vault()
        self.config = config
        self.set_entities()

        self.deanon_scanner = Deanonymize(self.vault)
        
        def __call__(self, input: str):
            sanitized_prompt, is_valid, risk_score = self.scanner.scan(input)
            return sanitized_prompt
        
    def set_entities(self):
        self.entities = {
            "LOCATION": self.config.MASK_LOCATION,
            "DATE_TIME": False, 
            "CREDIT_CARD": self.config.MASK_CREDIT_CARD,
            "CRYPTO": self.config.MASK_CRYPTO,
            "EMAIL_ADDRESS": self.config.MASK_EMAIL_ADDRESS,
            "IBAN_CODE": self.config.MASK_IBAN_CODE,
            "IP_ADDRESS": self.config.MASK_IP_ADDRESS,
            "PERSON": self.config.MASK_PERSON,
            "PHONE_NUMBER": self.config.MASK_PHONE_NUMBER,
            "US_SSN": self.config.MASK_US_SSN,
            "US_BANK_NUMBER": self.config.MASK_US_BANK_NUMBER,
            "CREDIT_CARD_RE": self.config.MASK_CREDIT_CARD_RE,
            "UUID": self.config.MASK_UUID,
            "EMAIL_ADDRESS_RE": self.config.MASK_EMAIL_ADDRESS_RE,
            "US_SSN_RE": self.config.MASK_US_SSN_RE,
            "URL": self.config.MASK_URL,
            "ORGANIZATION": self.config.MASK_COMPANY
        }
        NER_CONF["PRESIDIO_SUPPORTED_ENTITIES"] = [
            key for key, value in self.entities.items() if value
        ]

        self.anon_scanner = Anonymize(self.vault, preamble="",
            entity_types=NER_CONF["PRESIDIO_SUPPORTED_ENTITIES"],
            allowed_names=["John Doe"],
            recognizer_conf=NER_CONF,
            language="en"
        )


    def anonymize(self, prompt: str):
        self.set_entities()

        print("/nAnonymize!")
        print(self.config)
        print(NER_CONF["PRESIDIO_SUPPORTED_ENTITIES"])

        sanitized_prompt, is_valid, risk_score = self.anon_scanner.scan(prompt)
        return sanitized_prompt
    
    def deanonymize(self, sanitized_prompt: str, answer: str):
        sanitized_model_output, is_valid, risk_score = self.deanon_scanner.scan(sanitized_prompt, answer)
        return sanitized_model_output
        
    async def ascan_output(self, output_scanners, prompt, output):
        return await asyncio.to_thread(scan_output, output_scanners, prompt, output, fail_fast=True)

    async def stream_wrapper(self, original_generator, prompt, is_openai_call=False):
        output = ""
        prev_out = ""
        stop_package = None
        async for data in original_generator:
            body_str = data.decode("utf-8")
            if is_openai_call:
                body_str = body_str[5:]
                if "[DONE]" in body_str:
                    stop_package = data
                    break
                if not body_str:
                    yield data
                    continue
            
            new_data_dec = json.loads(body_str) if body_str else {}
            
            if new_data_dec.get("done_reason", "") == "stop":
                stop_package = data
                break
            data_dec = new_data_dec
            
            # print("\nBodyStr, ", body_str,"Data: ", data_dec)
            if is_openai_call:
                orig_content = data_dec.get("choices", [{}])[0].get("delta", {}).get("content", "")
            else:
                orig_content = data_dec.get("message", {}).get("content", "")
                
            output += orig_content
            # sanitized_output, is_valid, risk_score = await self.ascan_output(
            #     [self.deanon_scanner], prompt, output
            # )
            # if not all(is_valid.values()):
            #     print(f"Invalid output detected: {sanitized_output} ({risk_score})")
            #     break
            # Modify the response
            # data_dec["message"]["content"] = sanitized_output[len(prev_out):]
            # prev_out = sanitized_output
            # print("Mod chunk: ", data_dec["message"]["content"], sanitized_output)
            
            # # Re-encode and yield the modified chunk
            # ret_str = (json.dumps(data_dec) + "\n\n").encode("utf-8")
            yield data
            
        # Transform the output
        # print("\n\nOrig chunk: ", output)
        sanitized_output, is_valid, risk_score = await self.ascan_output(
            [self.deanon_scanner], prompt, output
        )
        # print("\n\nSanitized chunk: ", sanitized_output)
        
        prefix = "\n\n\n ⬇️🥷⬇️ Deanonymized Output Below ⬇️🥷⬇️ \n\n\n"
        if sanitized_output != output and all(is_valid.values()):
            if is_openai_call:
                # print(data_dec)
                data_dec["choices"][0]["delta"] = {"content": prefix + sanitized_output}
                # print(data_dec)
                yield f"data: {json.dumps(data_dec)}\n\n"
            else:
                print("Mistral dec: ", data_dec)
                data_dec["message"]["content"] = prefix + sanitized_output
                yield f"{json.dumps(data_dec)}\n"
        else:
            print(f"Invalid output detected: {sanitized_output} ({risk_score})")
        
        yield stop_package
        
        # async for data in original_generator:
        #     yield data

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
