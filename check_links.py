import subprocess
import sys


def main():
    output = build()
    problems = find_problems(output=output)

    if problems:
        print("MkDocs produced warnings:", file=sys.stderr)
        for problem in problems:
            print(problem, file=sys.stderr)
        sys.exit(1)

    print("MkDocs build completed with zero warnings.")
    sys.exit(0)


def build() -> str:
    """Builds the wiki and returns MkDoc's output"""

    # Run mkdocs build
    result = subprocess.run(
        ["mkdocs", "build"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    output = result.stdout
    print(f"MkDocs output:\n{output}\n")

    return output


def find_problems(output: str) -> list[str]:
    """Searches for warnings and other issues reported during the build

    :returns: List of problems found
    """

    patterns = ["WARNING", "unrecognized relative link"]
    issues_found = list()
    for pattern in patterns:
        issues_found += [line for line in output.splitlines() if pattern in line]

    return issues_found


if __name__ == "__main__":
    main()
