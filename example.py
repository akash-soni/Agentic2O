# Import required libraries
from langchain_openai import ChatOpenAI  # For using OpenAI's chat models
from dotenv import load_dotenv  # For loading environment variables
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the ChatOpenAI model with specific parameters
# model: 'gpt-4' - Using GPT-4 model
# temperature: 1.5 - Higher temperature for more creative/random outputs
# max_completion_tokens: 10 - Limit the response length to 10 tokens
model = ChatOpenAI(model= 'gpt-4', temperature=1.5, max_completion_tokens=10)

# Invoke the model with a prompt to write a poem
result = model.invoke("Write a 5 line poem on cricket")

# Print the generated content from the model
print(result.content)