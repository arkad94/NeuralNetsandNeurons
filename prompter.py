def create_prompt(CMD, tag, SPINS):
    cmd_templates = {
        "Word of The Day": "Template for command 1",
        "A Story": "Template for command 2",
        # Add more CMDs and their templates here
    }
    prompt_template = cmd_templates.get(CMD, "Default template if CMD not found")
    # Now incorporate tag and SPINS into the prompt
    final_prompt = f"{prompt_template} with Tag: {tag} and Additional Instructions: {SPINS}"
    return final_prompt


if __name__ == "__main__":
    example_prompt = create_prompt("A Story", "Technology", "Include examples")
    print(example_prompt)
