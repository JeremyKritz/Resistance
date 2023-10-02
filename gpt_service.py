import openai
import json, re, datetime, time
from constants import *
openai.api_key = '' #HIDE lol

class GPTService:
    RATE_LIMIT = 10000 # tokens per minute
    RATE_RESET_TIME = 60 # seconds (1 minute)
    
    def __init__(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"prompt_{timestamp}.txt"
        self.model = "gpt-4"
        self.tokens_used = 0
        self.last_request_time = 0
        # Create the file with just a header for now
        with open(self.log_filename, 'w') as f:
            f.write("Prompts and Responses\n")
            f.write("=====================\n\n")

    def call_gpt(self, system, prompt):
        print("\n Calling GPT")
        self._rate_limit_check()
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
        self.tokens_used += response.usage["total_tokens"]
        self.last_request_time = time.time()
        

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
    
    def _rate_limit_check(self):
        if self.last_request_time:
            time_since_last_request = time.time() - self.last_request_time
            if time_since_last_request >= self.RATE_RESET_TIME:
                # Reset the tokens used count after 1 minute
                self.tokens_used = 0
            elif self.tokens_used >= (self.RATE_LIMIT - 3000):
                # If tokens used is close to rate limit, wait for the reset time
                sleep_time = self.RATE_RESET_TIME - time_since_last_request
                print(f"Approaching rate limit. Sleeping for {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
                self.tokens_used = 0 # Reset after sleep