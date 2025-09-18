import os
import re
import unicodedata

def scan_files(base_path):
    """Recursively scan and return all file paths inside the given base_path."""
    file_list = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file != os.path.basename(__file__):  # Avoid renaming the running script
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list

def lowercase_filename(filename):
    """Convert the filename to lowercase for case-insensitive handling."""
    return filename.lower()

def normalize_filename(filename):
    """
    Normalize filename:
    - Keep Unicode letters/digits
    - Replace spaces and dashes with underscores
    - Remove emojis and forbidden symbols
    """
    name, ext = os.path.splitext(filename)
    name = name.replace(" ", "_").replace("-", "_")
    allowed_chars = []
    for ch in name:
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat.startswith("N") or ch == "_":
            allowed_chars.append(ch)
    cleaned_name = "".join(allowed_chars)
    cleaned_name = re.sub(r"_+", "_", cleaned_name)
    cleaned_name = cleaned_name.strip("_")
    return cleaned_name + ext

def move_number_to_end(filename):
    """If filename starts with numbers, move them to the end before extension."""
    name, ext = os.path.splitext(filename)
    match = re.match(r"^(\d+)(.+)", name)
    if match:
        num = match.group(1)
        rest = match.group(2).strip("_")
        return f"{rest}_{num}{ext}"
    return filename

def resolve_conflicts(existing_names, filename):
    """Ensure filename is unique by appending a number if it already exists."""
    name, ext = os.path.splitext(filename)
    counter = 2
    new_name = filename
    while new_name.lower() in existing_names:
        new_name = f"{name}{counter}{ext}"
        counter += 1
    return new_name

def rename_file(old_path, new_path):
    """Rename the file on the filesystem if the name has changed."""
    if old_path != new_path:
        os.rename(old_path, new_path)

def log_changes(log_file_path, base_path, old_name, new_name):
    """Append old and new file names to the log file (relative paths)."""
    old_rel = os.path.relpath(old_name, base_path)
    new_rel = os.path.relpath(new_name, base_path)
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{old_rel} --> {new_rel}\n")

def main():
    base_path = os.getcwd()
    make_log = input("Do you want to create a log file? (y/n): ").strip().lower() in ("y", "yes")
    log_file_path = os.path.join(base_path, "rename_log.txt") if make_log else None

    file_paths = scan_files(base_path)
    existing_names = set()

    for old_path in file_paths:
        dirname, old_filename = os.path.split(old_path)

        filename_lower = lowercase_filename(old_filename)
        normalized_name = normalize_filename(filename_lower)
        final_name = move_number_to_end(normalized_name)
        unique_name = resolve_conflicts(existing_names, final_name)

        new_path = os.path.join(dirname, unique_name)
        rename_file(old_path, new_path)

        existing_names.add(unique_name.lower())

        if make_log:
            log_changes(log_file_path, base_path, old_path, new_path)

    print("✅ All files renamed successfully.")
    if make_log:
        print(f"📄 Log saved at: {log_file_path}")

if __name__ == "__main__":
    main()

