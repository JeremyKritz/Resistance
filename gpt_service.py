import openai
import json, re, datetime
openai.api_key = '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' #HIDE lol

class GPTService:
    
    def __init__(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"prompt_{timestamp}.txt"
        # Create the file with just a header for now
        with open(self.log_filename, 'w') as f:
            f.write("Prompts and Responses\n")
            f.write("=====================\n\n")


    def call_gpt(self, prompt):
        print("\n Calling GPT")
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens = 700
        )

        with open(self.log_filename, 'a') as f:
            f.write(f"Prompt:\n{prompt}\n\n")
            f.write(f"Response:\n{response}\n")
            f.write("\n-------------------------\n\n")
        
        response_text = self.clean_json(response.choices[0].text.strip())



        try:
            pretty_response = json.loads(response_text)
        except Exception as e:
            print(e)
            print(response)

        token_info = {
            "Prompt Tokens": response.usage["prompt_tokens"],
            "Completion Tokens": response.usage["completion_tokens"],
            "Total Tokens": response.usage["total_tokens"]
        }
            
        print("\nResponse Text:\n", pretty_response)
        print("\nToken Usage:\n", token_info)
        
        #input("\n Press Enter to continue... \n ")
        return response_text
    

    def clean_json(self, text):
        # Convert keys with single quotes to double quotes
        text = re.sub(r"(\s*?{\s*?|\s*?,\s*?)(\'|\")(\w+)(\'|\")\s*?:", r'\1"\3":', text)

        # Convert keys without quotes to double quotes
        text = re.sub(r"(\s*?{\s*?|\s*?,\s*?)(\w+)\s*?:", r'\1"\2":', text)

        # Convert values that are not wrapped in quotes but should be (like player names)
        text = re.sub(r":\s*\[([\w\s,]+)\]", lambda match: ': ["' + '", "'.join(match.group(1).split(", ")) + '"]', text)
        
        return text