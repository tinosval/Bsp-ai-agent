import os
from dotenv import load_dotenv
from knowledge_base import build_knowledge_base

load_dotenv()

print("=" * 50)
print("BUILDING KNOWLEDGE BASE")
print("=" * 50)

# Check resource file exists
if not os.path.exists("documents/resource.txt"):
    print("ERROR: documents/resource.txt not found!")
    print("Please run create_test_resource.py first")
else:
    print("Found resource document!")
    print("Building knowledge base...")
    print()
    
    kb = build_knowledge_base("documents/resource.txt")
    
    print()
    print("=" * 50)
    print("SUCCESS! Knowledge base is ready!")
    print("=" * 50)
    print()
    print("You can now run the app with:")
    print("streamlit run app.py")