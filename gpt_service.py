import openai
import json, re, datetime
openai.api_key = '' #HIDE lol

class GPTService:
    
    def __init__(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"prompt_{timestamp}.txt"
        self.model = "gpt-3.5-turbo-instruct"
        # Create the file with just a header for now
        with open(self.log_filename, 'w') as f:
            f.write("Prompts and Responses\n")
            f.write("=====================\n\n")

    def call_gpt(self, prompt):
        print("\n Calling GPT")
        response = openai.Completion.create(
            model= self.model,
            prompt=prompt,
            max_tokens = 700
        )
        with open(self.log_filename, 'a') as f:
            f.write(f"Prompt:\n{prompt}\n\n")
            f.write(f"Response:\n{response}\n")
            f.write("\n-------------------------\n\n")
            
        
        token_info = {"Prompt Tokens": response.usage["prompt_tokens"], "Completion Tokens": response.usage["completion_tokens"], "Total Tokens": response.usage["total_tokens"]}
        print(token_info)

        return response.choices[0].text.strip()



    def call_gpt_player(self, prompt): #This one is for json responses
        response = self.call_gpt(prompt)
        clean_json_response = self.clean_json(response)
        try:
            pretty_response = json.loads(clean_json_response)
            print("\nResponse Text:\n", pretty_response)
        except Exception as e:
            print(e)
            print(response)
        return clean_json_response
    #Consider adding re-dos ...
    
    

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