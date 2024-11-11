import os
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("NVIDIA_API_KEY"))
print(os.getenv("OPENAI_API_KEY"))