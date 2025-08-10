"""
### Assisgment:
Create a simple assistant that uses any LLM and should be pydantic, 
when we ask about any product it should give you two information product Name, product details 
tentative price in USD (integer). use chat Prompt Template.
"""

from langchain_openai import ChatOpenAI
#from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv  # For loading environment variables
import os
# Load environment variables from .env file
load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

## Langsmith Tracking And Tracing
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"]="true"


# Step 1: Define the output schema
class ProductInfo(BaseModel):
    product_name: str = Field(..., description="Name of the product")
    product_details: str = Field(..., description="Short description of the product")
    tentative_price_usd: int = Field(..., description="Tentative price in USD")



# Step 2: Create the output parser
parser = PydanticOutputParser(pydantic_object=ProductInfo)



# Step 3: Define the prompt template
prompt = PromptTemplate(
    template ="""You are a helpful product assistant. When given a product name, respond with:
- product name
- short product details
- a tentative price in USD (as an integer).\n

{format_instructions}\n

Product: {product_query}
""",
    input_variables=["product_query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Step 4: Initialize the LLM (using GPT-3.5 or GPT-4 via OpenAI)
model = ChatOpenAI(temperature=0.5, model="gpt-4o-mini")
#model = ChatGroq(model="qwen-qwq-32b")

# Step 5: Query function
def get_product_info(product_query: str, model, parser) -> ProductInfo:
    chain = prompt | model | parser
    result = chain.invoke({"product_query": product_query})
    return result


product = "Apple iPhone 15 Pro"
result = get_product_info(product, model, parser)
print(result)
