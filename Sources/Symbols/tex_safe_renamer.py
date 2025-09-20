import os
import re
import unicodedata

def scan_files(base_path):
    """
    Recursively scan all files inside base_path,
    skipping the root directory itself (no changes to root files).
    """
    file_list = []
    script_path = os.path.abspath(__file__)  # current script path

    for root, _, files in os.walk(base_path):
        # Skip root directory
        if os.path.abspath(root) == os.path.abspath(base_path):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            # Avoid renaming the running script itself
            if os.path.abspath(file_path) != script_path:
                file_list.append(file_path)
    return file_list


def lowercase_filename(filename):
    """Convert filename to lowercase."""
    return filename.lower()


def normalize_filename(filename):
    """
    Replace spaces and dashes with underscores,
    keep only letters, digits, and underscores,
    remove extra underscores, and trim from both ends.
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
    """
    If filename starts with a number, move it to the end.
    Example: '123file.png' -> 'file_123.png'
    """
    name, ext = os.path.splitext(filename)
    match = re.match(r"^(\d+)(.+)", name)
    if match:
        num = match.group(1)
        rest = match.group(2).strip("_")
        return f"{rest}_{num}{ext}"
    return filename


def resolve_conflicts(existing_names, filename):
    """
    Ensure a unique filename in the same folder, even if extensions differ.
    Example:
        file.png  -> file.png
        file.pdf  -> file2.pdf
        file.svg  -> file3.svg
    """
    name, ext = os.path.splitext(filename)
    counter = 2
    new_name = filename

    existing_basenames = {os.path.splitext(f)[0].lower() for f in existing_names}

    while name.lower() in existing_basenames:
        new_name = f"{name}{counter}{ext}"
        existing_basenames.add(name.lower())  # update the set to avoid infinite loop
        name, ext = os.path.splitext(new_name)
        counter += 1

    return new_name


def rename_file(old_path, new_path):
    """Rename a file if the new name is different from the old one."""
    if os.path.abspath(old_path) != os.path.abspath(new_path):
        os.rename(old_path, new_path)


def log_changes(log_file_path, base_path, old_name, new_name):
    """
    Append rename operation to log file in 'old_path --> new_path' format.
    Only logs if names actually changed.
    """
    if os.path.abspath(old_name) != os.path.abspath(new_name):
        old_rel = os.path.relpath(old_name, base_path)
        new_rel = os.path.relpath(new_name, base_path)
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"{old_rel} --> {new_rel}\n")


def append_U_to_subfolders(uncolored_svg_path, log_file_path, base_path):
    """
    Add 'U_' prefix to all subfolders inside the 'uncolored_svg' directory (recursive),
    avoiding overwriting by adding a numeric counter (e.g., U_folder2).
    Skips folders that already start with 'U_' to prevent duplication.
    """
    for root, dirs, _ in os.walk(uncolored_svg_path, topdown=False):
        for dirname in dirs:
            old_dir_path = os.path.join(root, dirname)

            # Skip the uncolored_svg root directory itself
            if os.path.abspath(old_dir_path) == os.path.abspath(uncolored_svg_path):
                continue

            # Skip if this folder already starts with 'U_'
            if dirname.lower().startswith("u_"):
                continue

            new_dirname = f"U_{dirname}"
            new_dir_path = os.path.join(root, new_dirname)
            counter = 2

            # Avoid overwriting existing folder names
            while os.path.exists(new_dir_path):
                new_dirname = f"U_{dirname}{counter}"
                new_dir_path = os.path.join(root, new_dirname)
                counter += 1

            os.rename(old_dir_path, new_dir_path)
            if log_file_path:
                log_changes(log_file_path, base_path, old_dir_path, new_dir_path)


def main():
    base_path = os.getcwd()

    # Ask user if they want to create a log file
    make_log = input("Do you want to create a log file? (y/n): ").strip().lower() in ("y", "yes")
    log_file_path = os.path.join(base_path, "rename_log.txt") if make_log else None

    # Clear previous log if exists
    if log_file_path:
        open(log_file_path, "w", encoding="utf-8").close()

    # Process special folder: uncolored_svg
    uncolored_svg_path = os.path.join(base_path, "uncolored_svg")
    if os.path.isdir(uncolored_svg_path):
        append_U_to_subfolders(uncolored_svg_path, log_file_path, base_path)

    # Scan all files except root, and rename them
    file_paths = scan_files(base_path)

    # Group files by folder to handle conflicts locally
    files_by_folder = {}
    for path in file_paths:
        folder = os.path.dirname(path)
        files_by_folder.setdefault(folder, []).append(path)

    for folder, paths in files_by_folder.items():
        existing_names = {os.path.basename(p) for p in paths}
        for old_path in paths:
            old_filename = os.path.basename(old_path)

            # Apply transformations
            filename_lower = lowercase_filename(old_filename)
            normalized_name = normalize_filename(filename_lower)
            final_name = move_number_to_end(normalized_name)

            # Resolve conflicts within the same folder
            unique_name = resolve_conflicts(existing_names - {old_filename}, final_name)
            new_path = os.path.join(folder, unique_name)

            # Rename if changed
            rename_file(old_path, new_path)
            existing_names.add(unique_name)

            # Log changes if enabled
            if make_log:
                log_changes(log_file_path, base_path, old_path, new_path)

    print("✅ All files renamed successfully.")
    if make_log:
        print(f"📄 Log saved at: {log_file_path}")


if __name__ == "__main__":
    main()

