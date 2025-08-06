import json
from texttemplater import replace

"""Usage examples."""

# define template using placeholders
# name, profession, adjective, nevermatch
template = """Hello {{name}},
[[you are a {{profession}}||you have no profession]][[,
and you are {{adjective}}!||.]]{{nevermatch}}"""

# some incomplete datasets
data = [
    {"name": "Nick", "profession": "programmer", "adjective": "handsome"},
    {"name": "Klaus", "profession": "manager"},
    {"name": "Peter", "adjective": "useless"}
]

if __name__ == "__main__":
    print(f"Raw Template:\n{template}\n")
    print(f"Raw Data:\n{json.dumps(data, indent=2)}\n")
    print("Replaced texts:")
    [print(replace(template, d), end="\n\n") for d in data]

    # beware empty scopes and else blocks
    print()
    templates = [
            "[[Beware empty scopes]]",
            "[[Beware empty scopes {{x}}]]",
            "[[Beware empty scopes [[{{x}}||xxx]]]]"
    ]
    for template in templates:
        print(template, "=>", replace(template, {}))
    template = "[[But if {{y}} then [[{{x}}||xxx]]]]"
    print(template, "=>", replace(template, {"y": "y"}))
