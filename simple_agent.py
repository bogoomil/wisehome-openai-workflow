import os
from openai import OpenAI
import json

def analyze_command(text: str) -> dict:
    """
    Analyze smart home command using OpenAI GPT-4o-mini
    
    Returns:
    {
        "helyiség": "nappali",
        "eszköz": "lámpa",
        "parancs": "bekapcsol"
    }
    """
    client = OpenAI()
    
    system_prompt = """Te egy okosotthon eszköz vezérlő asszisztens vagy.
A felhasználó magyar nyelvű hangparancsokat ad.

A feladatod: Elemezd a parancsot és válaszolj JSON formátumban:
{"helyiség": "", "eszköz": "", "parancs": ""}

Példák:
- "Kapcsold be a nappaliban a lámpát" → {"helyiség": "nappali", "eszköz": "lámpa", "parancs": "bekapcsol"}
- "Kapcsold ki a hálószobában a fényt" → {"helyiség": "hálószoba", "eszköz": "fény", "parancs": "kikapcsol"}
- "Állítsd 22 fokra a fűtést a konyhában" → {"helyiség": "konyha", "eszköz": "fűtés", "parancs": "22 fok"}
- "Nyisd ki a nappali redőnyöket" → {"helyiség": "nappali", "eszköz": "redőny", "parancs": "kinyit"}

Ha nincs helyiség megadva, használd: "összes" vagy "általános"
Ha nem egyértelmű a parancs, használd: "ismeretlen"

FONTOS: CSAK JSON-t adj vissza, semmi mást!"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=100,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return {
            "helyiség": "hiba",
            "eszköz": "hiba",
            "parancs": str(e)
        }

