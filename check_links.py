import subprocess
import sys


def main():
    output = build()

    problems = find_problems(output)

    if problems:
        print("MkDocs produced warnings:")
        for problem in problems:
            print(problem)

    print("MkDocs build completed.")
    sys.exit(0)


def build() -> str:
    """Builds the wiki and returns MkDocs output."""

    result = subprocess.run(
        ["mkdocs", "build"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    output = result.stdout
    print(f"MkDocs output:\n{output}\n")

    # Only fail if mkdocs itself fails
    if result.returncode != 0:
        print(
            f"MkDocs build failed with exit code {result.returncode}.",
            file=sys.stderr,
        )
        sys.exit(result.returncode)

    return output


def find_problems(output: str) -> list:
    """Searches for warnings and other issues reported during the build.
    Returns:
        List of warning lines found in the output.
    """
    patterns = ["WARNING", "unrecognized relative link"]

    issues_found = []
    for pattern in patterns:
        issues_found.extend(
            [line for line in output.splitlines() if pattern in line]
        )

    return issues_found


if __name__ == "__main__":
    main()
