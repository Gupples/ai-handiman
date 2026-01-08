import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)
        completed_process = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True, 
            text=True, 
            timeout=30)

        results = []
        if completed_process.returncode != 0:
            results.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stdout and not completed_process.stderr:
            results.append("No output produced")
        
        if completed_process.stdout:
            results.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            results.append(f"STDERR:\n{completed_process.stderr}")
        return "\n".join(results)
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the contents of a given python file from within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to execute, which may include subdirectories of the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Any arguments the python file may potentially require",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)