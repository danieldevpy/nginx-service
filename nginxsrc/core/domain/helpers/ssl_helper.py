from dataclasses import dataclass
from typing import Optional, Tuple, List

@dataclass
class SSLHelper:
    default_pattern_start_ssl: str = 'listen 443 ssl'
    default_pattern_end_ssl: str = 'ssl_dhparam'
    default_pattern_end_config: str = '# end'

    def check_has_ssl(self, block: str) -> bool:
        return self.default_pattern_start_ssl in block
    
    def edit_server_block(
        self, 
        block: str, 
        replace: Optional[dict] = None, 
        remove: bool = False
    ) -> Tuple[str, List[str]]:
        """
        Edit an Nginx server block provided as a string.

        Args:
            block (str): full server block string.
            replace (dict, optional): mapping of original line -> new line for replacement.
            remove (bool, optional): if True, remove the SSL sub-block.

        Returns:
            str: modified server block.
            list[str]: lines of the copied sub-block (if any).
        """
        lines = block.splitlines(keepends=True)
        lines_lenght = len(lines)
        new_lines = []
        copied_block = []
        copying = False

        for i, line in enumerate(lines):
            stripped_line = line.strip()

            # Detect start of SSL block
            if not copying and self.default_pattern_start_ssl in stripped_line:
                copying = True

            # Copy line if inside SSL block
            if copying:
                copied_block.append(line)

            # Replace line if mapping provided
            if replace and stripped_line in replace:
                line = replace[stripped_line] + "\n"

            # Detect end of SSL block
            if copying and self.default_pattern_end_ssl in stripped_line:
                copying = False
                if remove:
                    continue  # skip the last line of SSL block

                # Do not add the end line twice if removing
                if remove:
                    continue

            # Add line if not removing the block
            if not (remove and line in copied_block):
                new_lines.append(line)
            

        return "".join(new_lines), copied_block

    def insert_rules_ssl(
        self,
        block: str,
        rules: List[str]
    ):
        lines = block.splitlines(keepends=True)
        new_lines = []

        for line in lines:
            
            if self.default_pattern_end_config in line:
                line_replace = "    # end\n\n" + "".join(rules)
                new_lines.append(line_replace)
            else:
                new_lines.append(line)

        return "".join(new_lines)