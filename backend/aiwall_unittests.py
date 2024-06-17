
from aiwall import AIwallHelper

# import logging

# # Configure logging
# logging.getLogger("llm_guard").setLevel(logging.ERROR)

# # Or you can completely disable logging for llm_guard
# logging.getLogger("llm_guard").disabled = True

if __name__=='__main__':
    import unittest

    class TestAIwallHelper(unittest.TestCase):
        def setUp(self):
            self.helper = AIwallHelper()
        
        def print_test_result(self, prompt):
            print(f"Original Prompt: {prompt}")
            anonymized_prompt = self.helper.anonymize(prompt)
            print(f"Anonymized Prompt: {anonymized_prompt}")
            deanonymized_output = self.helper.deanonymize(anonymized_prompt, "Sample answer")
            print(f"Deanonymized Output: {deanonymized_output}")
            print("\n")

        def test_locations(self):
            prompts = [
                "The office is located at 123 Main St, Springfield, IL, 62701.", # fails at zipcode 
                "We will meet at 221B Baker Street, London, UK.",
                "Deliver to Apt 5, 742 Evergreen Terrace, Springfield.",
                "Our new branch is at 1600 Amphitheatre Parkway, Mountain View, CA 94043.", # fails at zipcode 
                "Visit us at 10 Downing Street, London.",
                "He lives at 350 Fifth Avenue, New York, NY 10118.", # fails at zipcode 
                "Her address is 4 Privet Drive, Little Whinging, Surrey.",
                "Headquarters: 1 Microsoft Way, Redmond, WA.",
                "My home is at 1001 E. Southlake Blvd, Southlake, TX 76092.", # fails at zipcode 
                "Our facility is at 555 California Street, San Francisco, CA."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

        def test_organizations(self):
            prompts = [
                "She works at OpenAI.",  # all succeed
                "The contract is with Google LLC.",
                "He is employed by the United Nations.",
                "Our partner is IBM Corporation.",
                "We collaborated with NASA.",
                "The supplier is Siemens AG.",
                "The service is provided by Amazon Web Services.",
                "The agreement is with Goldman Sachs.",
                "He joined Microsoft.",
                "She left her job at Facebook, Inc."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

        def test_names(self):
            prompts = [
                "The CEO is John Smith.", # all succeed
                "Our client is María García.",
                "He was referred by Li Wei.",
                "The contract was signed by Amit Patel.",
                "The president is François Hollande.",
                "The representative is Ahmed Mohamed.",
                "She was assisted by Yuki Tanaka.",
                "The letter was addressed to Olga Ivanova.",
                "The team includes José Silva.",
                "The report was written by Kofi Annan."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

        def test_dates(self):
            prompts = [
                "The deadline is 12/31/2024.",
                "The meeting is on January 1, 2024.", # fails 
                "The event is scheduled for 2024-06-16.",
                "His birthdate is 04-15-1990.",
                "The anniversary is 15th June 2024.", # fails 
                "The project started on 2024.06.01.", # fails 
                "The invoice date is 20240616.", # fails 
                "The due date is 06/16/24.",
                "The end date is June 2024.", # fails 
                "The contract is valid from 01/01/2023 to 12/31/2023."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

        def test_ssn(self):
            prompts = [
                "His SSN is 123-45-6789.",  # all succeed
                "The social security number is 987-65-4321.",
                "Her SSN: 111-22-3333.",
                "Please provide your SSN: 222-33-4444.",
                "SSN 333-44-5555 is required.",
                "His number is 444-55-6666.",
                "The SSN 555-66-7777 was used.",
                "Use the SSN 666-77-8888.",
                "Enter the SSN: 777-88-9999.",
                "The SSN needed is 888-99-0000."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)


        def test_emails(self):
            prompts = [
                "Contact us at info@example.com.", # all succeed
                "My email is john.doe@domain.com.",
                "Send the details to support@company.org.",
                "Her address is jane_smith123@gmail.com.",
                "Email me at firstname.lastname@yahoo.co.uk.",
                "The email address is example@subdomain.domain.net.",
                "Reach out to admin@website.com.",
                "Their contact is contact_us@service.io.",
                "His work email is employee@enterprise.biz.",
                "Our email is feedback@platform.co."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

        def test_phone_numbers(self):
            prompts = [
                "Call me at (123) 456-7890.", # fails 
                "Her number is +1-800-555-1234.",
                "His phone is 123.456.7890.",
                "Reach us at 123-456-7890.", # fails 
                "The contact number is 800.555.6789.",
                "Dial 1-800-123-4567.", # fails 
                "Phone: 1234567890.",
                "The office number is +44 20 7946 0958.",
                "Her mobile: 098-765-4321.",
                "Contact: (800) 555-9876." # fails 
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

        def test_api_keys(self):
            prompts = [
                "API key: sk_test_4eC39HqLyjWDarjtT1zdp7dc.", # all of these fail 
                "The key is: 12345-abcde-67890-fghij.",
                "Use this API key: abc123-xyz789.",
                "API_KEY=abcdefghijklmnop1234567890.",
                "Secret key: 1a2b3c4d5e6f7g8h9i0j.",
                "Token: ABCD-1234-EFGH-5678.",
                "Your API key: 1234-5678-9101-1121.",
                "Key: a1b2c3d4e5f6g7h8i9j0.",
                "Access token: 0987ZYX6543WVU210.",
                "The API key is ABCD-EFGH-IJKL-MNOP."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

        def test_credit_cards(self):
            prompts = [
                "Card number: 4111 1111 1111 1111.",
                "Credit card: 5500 0000 0000 0004.",
                "Use card 3400 0000 0000 009.",
                "Mastercard: 2221 0000 0000 0009.", # fails 
                "Card details: 6011 0000 0000 0004.",
                "Visa: 4000 0000 0000 0002.",
                "Discover: 6011 0009 9013 9424.",
                "Amex: 3782 822463 10005.",
                "JCB: 3530 1113 3330 0000.",
                "Card number: 5555 5555 5555 4444."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

        def test_urls(self):
            prompts = [
                "Visit our site at https://www.example.com.",
                "The URL is http://domain.org.",
                "Find more at https://sub.domain.co.uk.",
                "Our homepage is http://example.net.",
                "Check https://www.website.io for details.",
                "The link is http://www.site.biz.", # partially fails [REDACTED_URL_6]z.
                "Visit https://platform.com.",
                "Go to http://www.page.info.", # partially fails [REDACTED_URL_8]fo.
                "Resource found at https://subdomain.domain.com/path.",
                "Our page: http://example.co."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)


        def test_crypto(self):
            prompts = [ 
                "My Bitcoin address is 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa.", # didnt test 
                "Use Ethereum address 0x32Be343B94f860124dC4fEe278FDCBD38C102D88.",
                "Send funds to Litecoin address LcHK4XXsFwMu7WhZXjFX8q4HbNJipg6wni.",
                "Monero address is 44AFFq5kSiGBoZ...PVNnBn.",
                "Deposit to Ripple address rDsbeomae4FXwgQTJp9Rs64Qg9vDiTCdBv.",
                "My Dogecoin address: DShTmSEaR5oGH7hK2ZAG9SbMw6h91J1KM3.",
                "Use this Dash address: XxGJezP19Q2L8CpkkARzTe3k8S2KMdZv2g.",
                "The Zcash address is t1eQG9FZnZ...7RHJdQU.",
                "Here is my Stellar address: GCL7YWI6GDO...X2S3B5.",
                "Cardano address: DdzFFzCqrhs...q8n." 
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

        def test_iban_code(self):
            prompts = [
                "My IBAN is GB29NWBK60161331926819.", # all succeed
                "The account number is DE89370400440532013000.",
                "Use IBAN: FR1420041010050500013M02606.",
                "Transfer to this IBAN: ES9121000418450200051332.",
                "Her IBAN code: IT60X0542811101000000123456.",
                "Our IBAN is NL91ABNA0417164300.",
                "IBAN: BE68539007547034.",
                "Send money to IBAN: CH9300762011623852957.",
                "Deposit to IBAN: DK5000400440116243.",
                "Their IBAN is AT611904300234573201."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

        def test_ip_address(self):
            prompts = [
                "The server IP is 192.168.1.1.", # all succeed
                "My IP address: 10.0.0.1.",
                "Connect to 172.16.254.1.",
                "His IP is 192.0.2.146.",
                "Public IP address is 203.0.113.0.",
                "Her IP: 198.51.100.23.",
                "Use IP 224.0.0.1 for multicast.",
                "Local IP address: 127.0.0.1.",
                "Gateway IP is 192.168.0.1.",
                "Router IP: 10.0.0.254."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

        def test_us_bank_number(self):
            prompts = [
                "The account number is 123456789.",
                "Use bank number 987654321.",
                "Her bank account: 1111222233334444.", # this is the only one that suceeds. all others fail 
                "Deposit to account 567890123.",
                "Bank number: 432109876.",
                "Account: 000111222333.",
                "His bank account number is 555666777.",
                "Use this account: 333444555666.",
                "Our bank number is 111222333.",
                "Their account number: 222333444555."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

        def test_uuid(self):
            prompts = [
                "The UUID is 123e4567-e89b-12d3-a456-426614174000.",
                "Here is the UUID: 550e8400-e29b-41d4-a716-446655440000.",
                "Use UUID 6ba7b810-9dad-11d1-80b4-00c04fd430c8.",
                "My UUID: 1a2b3c4d-5f6g-7h8i-9j0k-1l2m3n4o5p6q.", # fails 
                "Her UUID is 9b8c7d6e-5f4g-3h2i-1j0k-9l8m7n6o5p4q.", # fails 
                "UUID: f47ac10b-58cc-4372-a567-0e02b2c3d479.",
                "Their UUID is 3f8e8a2c-d3bf-4a7e-a2b4-ea7461f7df7a.",
                "Use this UUID: 2b1e7e9a-9a4d-4e7c-a5f5-29e45d57b2bb.",
                "Generated UUID: 7c9e6679-7425-40de-944b-e07fc1f90ae7.",
                "UUID: e4eaaaf2-d142-11e1-b3e4-080027620cdd."
            ]
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.print_test_result(prompt)

    unittest.main()