import os
import json
import openai

def extract_and_update_memory(user_id, conversation, existing_memory):
    """Use AI to extract important details from conversation and update memory"""
    
    extraction_prompt = f"""You are a memory extraction assistant. 
    
Current memory about this person: {json.dumps(existing_memory)}

New conversation:
{conversation}

Extract any important personal details mentioned. Return ONLY a JSON object with these fields if mentioned:
- name
- age
- job
- location
- relationship_status
- pets
- hobbies
- favourite_things
- things_they_dislike
- emotional_details
- birthday
- anything_important

Only include fields that were actually mentioned. Merge with existing memory, don't overwrite good existing data unless corrected.
Return only valid JSON, nothing else."""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": extraction_prompt}
        ],
        max_tokens=500
    )
    
    try:
        new_memory = json.loads(response.choices[0].message["content"])
        merged = {**existing_memory, **new_memory}
        return merged
    except:
        return existing_memory
