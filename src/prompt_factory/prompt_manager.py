import glob, os
from pathlib import Path
from importlib import import_module

def get_latest_prompt_version(module_type="agent", module_name="decomposer"):
    prompt_folder = os.path.join("src", "prompt_factory", module_type+"_prompts", module_name+"_prompts")
    prompt_files_path = os.path.join(prompt_folder, "*.py")
    prompt_files=glob.glob(prompt_files_path)
    version_numbers=[]
    for prompt_file in prompt_files:
        file_name=Path(prompt_file).name[:-3]
        file_version=file_name.split("_")[1:]
        version_number=int("1"+"".join(file_version))
        version_numbers.append(version_number)
    latest_prompt_version=str(sorted(version_numbers)[-1])[1:]
    latest_prompt_version_name="v_"+  latest_prompt_version[:3] + "_" + latest_prompt_version[3:6] + "_" + latest_prompt_version[-3:]
    return latest_prompt_version_name


def version_name_standardisation(prompt_version):
    sub_version_list=[]
    sub_versions=prompt_version.split(".")
    for sub_version in sub_versions:
        remaining_length=3-len(sub_version)
        if remaining_length:
            sub_version=sub_version+remaining_length*"0"
        sub_version_list.append(sub_version)
    full_version="v_"+"_".join(sub_version_list)
    return full_version


def get_prompt(prompt_version="", module_type="agent", module_name="decomposer"):
    try:
        if not prompt_version:
            standardised_prompt_version=get_latest_prompt_version(module_type=module_type, module_name=module_name)
        else:
            standardised_prompt_version=version_name_standardisation(prompt_version)
        module_path=f"src.prompt_factory.{module_type}_prompts.{module_name}_prompts.{standardised_prompt_version}"
        module=import_module(module_path)
        get_prompt_func = getattr(module, "prompt")
        prompt=get_prompt_func()
        if prompt:
            return {"status":1, "content": prompt}
        return {"status":1, "content": "Prompt not found"}
    except Exception as e:
        return {"status":1, "content": str(e)}
