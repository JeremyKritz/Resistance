import openai
import json, re, datetime, time
from constants import *
openai.api_key = '' #HIDE lol

class GPTService:
    
    def __init__(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"prompt_{timestamp}.txt"
        self.model = "gpt-3.5-turbo"
        # Create the file with just a header for now
        with open(self.log_filename, 'w') as f:
            f.write("Prompts and Responses\n")
            f.write("=====================\n\n")

    def call_gpt(self, system, prompt):
        print("\n Calling GPT")
        response = openai.ChatCompletion.create(
            model= self.model,
            messages=[
            {
            "role": "system",
            "content": system
            },
            {
            "role": "user",
            "content": prompt
            }
  ],
            max_tokens = 700
            #freq penalty? - idk might kill the json...
        )
        with open(self.log_filename, 'a') as f:
            f.write(f"System Prompt:\n{system}\n\n")
            f.write("\n    ------------\n\n")
            f.write(f"User Prompt:\n{prompt}\n\n")
            f.write("\n    ------------\n\n")
            f.write(f"Response:\n{response}\n")
            f.write("\n==========================\n\n")
            
        
        token_info = {"Prompt Tokens": response.usage["prompt_tokens"], "Completion Tokens": response.usage["completion_tokens"], "Total Tokens": response.usage["total_tokens"]}
        print(token_info)

        return response.choices[0].message.content.strip()



    def call_gpt_player(self, system, prompt, max_retries=1): #This one is for json responses
        retries = 0
        while retries <= max_retries: #GPT 3 sometimes (rarely) doesnt return proper format
            if retries > 0:
                time.sleep(.6)
                prompt = prompt + " Again, ensure the response matches the requested JSON format."
            response = self.call_gpt(system, prompt)
            clean_json_response = self.clean_json(response)
            try:
                pretty_response = json.loads(clean_json_response)
                print("\nResponse Text:\n", pretty_response)
                return clean_json_response
            except Exception as e:
                print(f"Attempt {retries+1} failed:")
                print(e)
                print(response)
                retries += 1
        
        print(f"Failed to get a valid JSON response after {max_retries} attempts.")
        return None

    
    

    def clean_json(self, text):

        start_idx = text.find('{')
        end_idx = text.rfind('}')
        if start_idx != -1 and end_idx != -1:
            text = text[start_idx:end_idx+1]
        else:
            text = "{" + text + "}"

        # Convert keys with single quotes to double quotes
        text = re.sub(r"(\s*?{\s*?|\s*?,\s*?)(\'|\")(\w+)(\'|\")\s*?:", r'\1"\3":', text)

        # Convert keys without quotes to double quotes
        text = re.sub(r"(\s*?{\s*?|\s*?,\s*?)(\w+)\s*?:", r'\1"\2":', text)

        # Convert values that are not wrapped in quotes but should be (like player names)
        text = re.sub(r":\s*\[([\w\s,]+)\]", lambda match: ': ["' + '", "'.join(match.group(1).split(", ")) + '"]', text)
        
        return text