from openai import OpenAI
import os
from dotenv import load_dotenv
import tools
import json

load_dotenv('.env')
openai_api_key = os.getenv("OPENAI_API_KEY")