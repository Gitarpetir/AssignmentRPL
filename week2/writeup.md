# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: Muhammad Alfi Gunawan \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
Implement a new function called extract_action_items_llm(text: str) -> List[str].

Requirements:
- Use Ollama chat() with the local model llama3.1:8b.
- Extract actionable tasks from the input text.
- Return a Python list of strings.
- The model must output a JSON array of strings only.
- Parse the JSON safely using json.loads().
- Handle invalid JSON gracefully (return empty list on failure).
- Keep temperature low (0.0).
- Do not modify the existing extract_action_items() function.

Generated Code Snippets:
```
def extract_action_items_llm(text: str) -> List[str]:
    """
    Uses Ollama (llama3.1:8b) to extract actionable items.
    Returns a list of strings or empty list if parsing fails.
    """
    try:
        response = chat(
            model="llama3.1:8b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract actionable tasks from the given text. "
                        "Return ONLY a valid JSON array of strings. "
                        "Do not include explanations, markdown, or extra text."
                    ),
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
            options={"temperature": 0.0},
        )

        output = response.message.content.strip()
        data = json.loads(output)

        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return data

        return []

    except Exception:
        return []

### Exercise 2: Add Unit Tests
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
from ..app.services.extract import extract_action_items_llm


def test_llm_simple_sentences():
    text = "Finish homework. Email professor."
    items = extract_action_items_llm(text)

    assert isinstance(items, list)
    assert any("Finish homework" in item for item in items)
    assert any("Email professor" in item for item in items)


def test_llm_bullet_list():
    text = """
    - Set up database
    - Implement endpoint
    """
    items = extract_action_items_llm(text)

    assert isinstance(items, list)
    assert any("Set up database" in item for item in items)
    assert any("Implement endpoint" in item for item in items)


def test_llm_empty_input():
    items = extract_action_items_llm("")
    assert isinstance(items, list)

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
TODO
``` 

Generated/Modified Code Snippets:
```
TODO: List all modified code files with the relevant line numbers. (We anticipate there may be multiple scattered changes here – just produce as comprehensive of a list as you can.)
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 