from anthropic import Anthropic
from dotenv import load_dotenv  

load_dotenv()

client = Anthropic()


skill = client.beta.skills.create(
    display_title="Status Report Generator",
    files=files_from_dir("status-report-skill"),  # folder containing SKILL.md
)

print(skill.id)  # reference this ID in future requests