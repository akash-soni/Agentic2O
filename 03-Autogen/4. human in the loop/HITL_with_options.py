import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

assistant = AssistantAgent(
    name='Assistant',
    description='you are a great assistant',
    model_client=model_client,
    system_message='You are a really helpful assistant who helps with the task given.'
)

# We'll store a flag in outer scope so we can terminate from inside input
terminate_flag = {"stop": False}

def custom_input(prompt=""):
    user_text = input(prompt).strip()
    if user_text.upper() == "APPROVE":
        terminate_flag["stop"] = True
        return user_text  # just return, Console will stop next turn
    elif user_text.upper() == "REJECT":
        return "Please redo the answer from scratch."
    elif user_text.upper() == "TWEAK":
        return "Please improve or adjust the previous answer."
    else:
        return user_text

user_proxy_agent = UserProxyAgent(
    name='UserProxy',
    description='you are a user proxy agent',
    input_func=custom_input
)

team = RoundRobinGroupChat(
    participants=[assistant, user_proxy_agent],
    max_turns=10
)

async def main():
    stream = team.run_stream(task='Write a great poem about India?')

    async for message in stream:
        if terminate_flag["stop"]:
            print("\n✅ Conversation ended by user approval.")
            break
        await Console(stream)

if __name__ == '__main__':
    asyncio.run(Console(team.run_stream(task="Write a great poem about India?")))
