with open('images_with_captions.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
entries = text.split('\n\n')
with open('homer_img_list.txt', 'w', encoding='utf-8') as out:
    for e in entries:
        m = re.search(r"imgs=\['media/(image\d+\.[a-z]+)'\]", e)
        if m:
            img = m.group(1)
            # find NEXT: or PREV:
            lines = e.split('\n')
            captions = [l for l in lines if 'NEXT:' in l or 'PREV:' in l]
            out.write(f"{img}:\n")
            for c in captions:
                out.write(f"  {c}\n")
print("Done writing homer_img_list.txt")

