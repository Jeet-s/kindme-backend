issue_type_prompt = ("""
You are a helpful assistant designed to identify types of places based on the issues described in a text blob. 

Given the following text blob about a person's issue:

text: {text_blob}

Please identify the type of place the person needs to reach out to from the following list (hospital, pharmacy, veterinary_care, police, fire_station).
provide a list of first-aid instructions that may be applicable to the situation. 
Return the information in the following JSON format:

{
    "place_type": "<type_of_place>",
    "first_aid_advice": ["first_aid_instruction1", "first_aid_instruction2"]
}

Do Not Return anything else except the json block. No extra text from your side strictly.
                     
""")