import os
import subprocess

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
        command.extend(args)
        completed_process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=30)

        results = ""
        if completed_process.returncode != 0:
            results += f"Process exited with code {completed_process.returncode}"
        if (not completed_process.stdout or not completed_process.stderr):
            results += "No output produced"
        else:
            results += f"STDOUT: {completed_process.stdout}"
            results += f"STDERR: {completed_process.stderr}"
        return results
        
    except Exception as e:
        return f"Error: executing python file: {e}"