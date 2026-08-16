from anthropic import Anthropic
from dotenv import load_dotenv  

load_dotenv()

client = Anthropic()


architecture_decision="In our architecture we chose MongoDB over PostgreSQL primarily because of the highly variable and rapidly evolving nature of our domain data. Product catalogs, user activity streams, and configuration documents frequently contain nested structures and optional fields that differ significantly between tenants and change from one release to the next. MongoDB’s document model lets us store these structures naturally without forcing expensive schema migrations or sparse tables, while its flexible indexing and aggregation pipeline give us the query power we need for analytics and real-time features. Horizontal scaling through sharding also maps cleanly to our expected growth pattern, allowing us to add capacity without the operational complexity of managing read replicas and partitioning logic that a relational system would require at the same scale. Although PostgreSQL remains excellent for strongly relational workloads, the combination of schema flexibility, developer velocity, and straightforward horizontal scaling made MongoDB the better fit for our core services."

response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    betas=["skills-2025-10-02", "code-execution-2025-08-25"],
    container={
        "skills": [
            {
                "type": "custom",
                "skill_id": "skill_01YW4EAc2sTC3ZVc6t9MQbEX",
                "version": "latest",
            }
        ]
    },
    tools=[
        {
            "type": "code_execution_20250825",
            "name": "code_execution",
        }
    ],
    messages=[
        {
            "role": "user",
            "content": f"Generate a Architecture Decision Records from this text \n\n{architecture_decision}",
        }
    ],
)


print("stop_reason:", response.stop_reason)
print("block types:", [b.type for b in response.content])
print("-" * 40)


# First: print everything Claude said in text (intro + summary, maybe the ADR itself)
for block in response.content:
    if block.type == "text":
        print(block.text)
        print("-" * 40)

# Then: recursively search the WHOLE response for any file the run produced,
# regardless of which tool block created it (text editor OR bash).
def find_file_ids(obj, found=None):
    if found is None:
        found = []
    if isinstance(obj, dict):
        if obj.get("file_id"):
            found.append(obj["file_id"])
        for v in obj.values():
            find_file_ids(v, found)
    elif isinstance(obj, list):
        for v in obj:
            find_file_ids(v, found)
    return found

file_ids = list(dict.fromkeys(find_file_ids(response.model_dump())))  # dedup, keep order
print("file_ids found:", file_ids)

for fid in file_ids:
    meta = client.beta.files.retrieve_metadata(file_id=fid)
    content = client.beta.files.download(file_id=fid)
    with open(meta.filename, "wb") as f:
        f.write(content.read())
    print(f"Downloaded: {meta.filename} ({meta.size_bytes} bytes)")