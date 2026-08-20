import os
from dotenv import load_dotenv
from openai import OpenAI
from knowledge_base import load_knowledge_base, search_resource

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_section(section_name, client_details, resource_content):
    
    prompt = f"""You are an experienced Behaviour Support Practitioner 
    writing a professional Behaviour Support Plan (BSP).

    CRITICAL RULES:
    1. Use ONLY information from the resource document below
    2. Do NOT add any information from outside this document
    3. Write in professional paragraphs NOT bullet points
    4. Use warm person-centred language
    5. Refer to the client by first name only

    CLIENT DETAILS:
    Name: {client_details['name']}
    Diagnosis: {client_details['diagnosis']}
    Behaviours of Concern: {client_details['behaviours']}
    Frequency: {client_details['frequency']}
    Triggers: {client_details.get('triggers', 'Not specified')}

    INTERNAL RESOURCE DOCUMENT CONTENT:
    {resource_content}

    Write the {section_name} section in 2-3 professional paragraphs.
    Use ONLY the resource content above. Nothing else."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": "You are a professional Behaviour Support Practitioner. Only use information from the provided resource document."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        max_tokens=500,
        temperature=0.3
    )
    
    return response.choices[0].message.content

def generate_bsp(client_details, plan_type):
    
    print(f"Starting BSP generation for {client_details['name']}...")
    
    # Load knowledge base
    kb = load_knowledge_base()
    
    # Search for diagnosis
    resource_content, diagnosis_found = search_resource(
        kb, 
        client_details['diagnosis']
    )
    
    # Flag if diagnosis not found
    if not diagnosis_found:
        print(f"⚠️ Diagnosis not found: {client_details['diagnosis']}")
        return {
            "success": False,
            "flag": True,
            "message": f"⚠️ FLAGGED: '{client_details['diagnosis']}' was not found in the internal resource document. Please review manually or update the resource document.",
            "content": None
        }
    
    print(f"✓ Found {client_details['diagnosis']} in resource document")
    
    # Define sections based on plan type
    if plan_type == "interim":
        sections = [
            "Background and Context",
            "Description of Behaviour",
            "Reactive Strategies",
            "Immediate Support Strategies"
        ]
    else:
        sections = [
            "Background and Context",
            "Diagnosis Overview",
            "Description of Behaviour",
            "Functional Assessment",
            "Proactive Strategies",
            "Reactive Strategies",
            "Crisis Management",
            "Staff Guidelines",
            "Review Process"
        ]
    
    # Generate each section
    generated_content = {}
    
    for section in sections:
        print(f"Generating: {section}...")
        generated_content[section] = generate_section(
            section,
            client_details,
            resource_content
        )
        print(f"✓ {section} complete")
    
    print("✓ All sections generated successfully!")
    
    return {
        "success": True,
        "flag": False,
        "message": "BSP generated successfully!",
        "content": generated_content,
        "client_details": client_details,
        "plan_type": plan_type
    }