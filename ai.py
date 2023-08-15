import openai
openai.api_key = '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'
import json

class AI:
    def __init__(self, system="", model = 'gpt-4', openai=openai):
        self.system = system
        self.model = model
        self.openai = openai
        self.messages = [{"role": "system", "content": system}]


    def generate_response(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        response = self.openai.ChatCompletion.create(
            model=self.model,
            stream=True,
            messages=self.messages,
        )

        chat = []
        for chunk in response:
            delta = chunk["choices"][0]["delta"]
            msg = delta.get("content", "")
            print(msg, end="")
            chat.append(msg)

        print()

        response_text = "".join(chat)

        self.messages.append({"role": "assistant", "content": response_text})
        return response_text, self.messages
    
    def generate_image(self, prompt, n=1, size="1024x1024", response_format="url"):
        """Generate an image using DALL·E given a prompt.

        Arguments:
            prompt (str): A text description of the desired image(s). 
            n (int, optional): The number of images to generate. Defaults to 1.
            size (str, optional): The size of the generated images. Defaults to "1024x1024".
            response_format (str, optional): The format in which the generated images are returned. Defaults to "url".

        Returns:
            dict: The response from the OpenAI API.
        """
        return openai.Image.create(prompt=prompt, n=n, size=size, response_format=response_format)
