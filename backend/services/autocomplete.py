from __future__ import annotations

from typing import Final, Tuple


class AutocompleteService:
    fallback: Final[str] = "# try adding more detail"
    print_rules: Final[Tuple[Tuple[str, str], ...]] = (
        ("pri", "print('value')"),
        ("print", "print('value')"),
        ("sys", "System.out.println(\"value\");"),
        ("system.out", "System.out.println(\"value\");"),
        ("console", "console.log('value');"),
        ("con", "console.log('value');"),
    )

    def suggest(self, code: str) -> str:
        snippet = code.splitlines()[-1].strip() if code.strip() else ""
        if not snippet:
            return "print('hello world')"
        lower_snippet = snippet.lower()
        for trigger, suggestion in self.print_rules:
            if lower_snippet.startswith(trigger):
                return suggestion

        return self.fallback
