def write_file(filename: str, content: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
