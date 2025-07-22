from setuptools import find_packages, setup
from typing import List

HYPEN_edot = "-e ."

def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirment pakages like seaborn, numpu, etc
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements=[req.replace("\n", "") for req in requirements]
 
        if HYPEN_edot in requirements:
            requirements.remove(HYPEN_edot)
 
    return requirements

print(get_requirements)

# consider this as a metadata for the entire project
setup(
    name = "ML_Project",
    version = "0.0.1",
    author = "Muneeb Mughal",
    author_email= "muneerahmed8556@gmail.com",
    packages=find_packages(),
    install_requires =get_requirements("requirements.txt")
)