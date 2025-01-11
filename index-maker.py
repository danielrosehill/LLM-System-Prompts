#!/usr/bin/env python3
import os
import re
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_file_description(content, filename):
    print(f"\n🤖 Generating description for {filename}...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a technical documentation assistant. Generate a clear, concise two-line description of the provided markdown document. Focus on the main purpose and key points. Return only the description, no additional text."},
                {"role": "user", "content": content}
            ],
            max_tokens=100,
            temperature=0.7
        )
        description = response.choices[0].message.content.strip()
        print(f"✅ Description generated successfully")
        print(f"📝 Description: {description}\n")
        return description
    except Exception as e:
        print(f"❌ Error generating description: {e}\n")
        return "Description generation failed"

def clean_title(filename):
    title = os.path.splitext(filename)[0]
    title = re.sub(r'[-_]', ' ', title)
    return title.title()

def generate_docs_index(repo_path, readme_file="README.md"):
    print(f"🔍 Starting documentation index generation in {repo_path}")
    markdown_files = []
    exclude = {'non-docs'}
    
    print("\n📁 Scanning directories...")
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in exclude and not d.startswith('.')]
        print(f"  Scanning: {root}")
        
        for file in files:
            if file.lower().endswith('.md') and file != readme_file:
                rel_path = os.path.relpath(os.path.join(root, file), repo_path)
                full_path = os.path.join(root, file)
                print(f"  📄 Found markdown file: {rel_path}")
                
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(f"    📖 Read {len(content)} characters")
                    description = get_file_description(content, file)
                except Exception as e:
                    print(f"    ❌ Error reading file {full_path}: {e}")
                    description = "File content unavailable"
                
                title = clean_title(file)
                markdown_files.append((title, rel_path, description))

    print(f"\n📝 Generating index table for {len(markdown_files)} files...")
    markdown_files.sort(key=lambda x: x[0])

    table_content = ["<!-- START_DOCS_INDEX -->\n\n"]
    table_content.append("## Documentation Index\n\n")
    table_content.append("| Document | Description | Link |\n")
    table_content.append("|----------|-------------|------|\n")
    for title, path, desc in markdown_files:
        desc_formatted = desc.replace('\n', '<br>')
        table_content.append(f"| {title} | {desc_formatted} | [{title}]({path}) |\n")
    table_content.append("\n<!-- END_DOCS_INDEX -->\n")
    
    print("\n💾 Updating README.md...")
    try:
        with open(os.path.join(repo_path, readme_file), 'r') as f:
            content = f.read()
            print("  📖 Existing README.md loaded")
    except FileNotFoundError:
        print("  ⚠️ README.md not found, creating new file")
        content = "# Repository Documentation\n\n<!-- START_DOCS_INDEX -->\n<!-- END_DOCS_INDEX -->\n"

    pattern = r'<!-- START_DOCS_INDEX -->.*<!-- END_DOCS_INDEX -->'
    index_text = ''.join(table_content)
    
    if '<!-- START_DOCS_INDEX -->' in content:
        content = re.sub(pattern, index_text.strip(), content, flags=re.DOTALL)
        print("  ✏️ Updated existing index section")
    else:
        content += '\n' + index_text
        print("  ✏️ Added new index section")

    with open(os.path.join(repo_path, readme_file), 'w') as f:
        f.write(content.strip() + '\n')
    
    print("\n✅ Documentation index generated successfully!")

if __name__ == "__main__":
    generate_docs_index('.')