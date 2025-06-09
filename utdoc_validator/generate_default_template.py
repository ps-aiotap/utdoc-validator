"""Module for generating default unit test documentation templates."""

class GenerateDefaultTemplate:
    """Generates a default unit test documentation template."""
    
    def __init__(self, path: str):
        """Initialize with the path where the template will be saved.
        
        Args:
            path: Path where the template will be saved
        """
        self.path = path
        self._generate()
    
    def _generate(self):
        """Generate the default template and write it to the specified path."""
        template_content = """## Test Cases
Describe individual test cases here.

## Coverage
Include your code coverage summary here.

## Edge Cases
Mention edge or uncommon scenarios tested.
"""
        with open(self.path, "w") as f:
            f.write(template_content)