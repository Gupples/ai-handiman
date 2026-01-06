import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    dir_contents = os.listdir(target_dir)
    directory_info = []
    for item in dir_contents:
        try:
            name = item
            filepath = os.path.join(target_dir, item)
            file_size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)
            item_info =  f"- {name}: file_size={file_size}, is_dir={is_dir}"
            directory_info.append(item_info)
        except:
            return f"Error: Unexpected error with file {item}."
    return "\n".join(directory_info)
