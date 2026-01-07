import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)

    except Exception as e:
        return f"Error writing files: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a specified file within the working directory, creating specified subdirectories as needed, as well as the file to be written to if it does not yet exist",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, which may include subdirectories to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents of the file post-execution",
            )
        },
    ),
)