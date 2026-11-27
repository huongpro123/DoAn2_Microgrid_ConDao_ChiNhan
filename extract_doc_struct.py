import docx
import zipfile
import xml.etree.ElementTree as ET

doc = docx.Document('noi dung_ngoc hien.docx')
with open('doc_structure.txt', 'w', encoding='utf-8') as out:
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        imgs = []
        for r in p.runs:
            if 'drawing' in r._r.xml:
                root = ET.fromstring(r._r.xml)
                for blip in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip'):
                    embed = blip.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                    if embed and embed in doc.part.rels:
                        imgs.append(doc.part.rels[embed].target_ref)
        if text or imgs:
            out.write(f'P{i}: text="{text}" imgs={imgs}\n')
print('Extracted doc structure')

