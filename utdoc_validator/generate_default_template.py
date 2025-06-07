class GenerateDefaultTemplate:
    def __init__(self, template_name):
        self.template_name = template_name

    def GenerateDefaultTemplate(self, path: str):
        default_template = {
            "templateName": self.template_name,
            # "templateDescription": self.template_description,
            # "templateBody": self.template_body,
            "content": f"""
            ## Test Cases
            Describe individual test cases here.

            ## Coverage
            Include your code coverage summary here.

            ## Edge Cases
            Mention edge or uncommon scenarios tested.

            """,
        }

        with open(path, "w") as f:
            f.write(default_template)
            f.write("\n")
