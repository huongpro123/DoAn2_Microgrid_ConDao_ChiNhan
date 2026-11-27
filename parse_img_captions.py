with open('doc_structure.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('images_with_captions.txt', 'w', encoding='utf-8') as out:
    for i, line in enumerate(lines):
        if "imgs=['" in line:
            # check previous line and next line
            prev_line = lines[i-1].strip() if i > 0 else ""
            next_line = lines[i+1].strip() if i+1 < len(lines) else ""
            out.write(f"{line.strip()}\n  PREV: {prev_line}\n  NEXT: {next_line}\n\n")

print("Done writing images_with_captions.txt")

