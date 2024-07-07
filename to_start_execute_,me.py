import os
import subprocess
import sys
from pathlib import Path
from typing import Callable, Optional, Literal, List

NAME_PATTERN_VENV = "venv2"


def create_virtual_env() -> None:
    """
        Create virtual ambient in local
    """
    print("Criando o ambiente virtual...")
    subprocess.run([sys.executable, "-m", "venv", NAME_PATTERN_VENV])


def enter_virtual_env(name: str = NAME_PATTERN_VENV) -> None:

    """
        Active ambient virtual by system operacional
    """

    message = "Ativando o ambiente virtual, executando: '{}'"

    # check if System Operacional is Windows
    if os.name == "nt":
        activate_script = os.path.join(name, "Scripts", "activate")
        print(message.format(f"{activate_script}.bat"))
        subprocess.run(activate_script, shell=True)

    else:  # for System Operacional Linux or Mac
        activate_script = os.path.join(name, "bin", "activate")
        print(message.format(f"source {activate_script}"))
        subprocess.run(["source", activate_script], shell=True)


def condition_response_yes_no(response: str) -> Optional[Literal['s', 'n']]:

    """
    Checker of condition to response from type yes or no

    Args:
        response(str): response to be checked

    Returns:
        str: return s or n
    """

    if response in ['s', 'n']:
        return response
    else:
        print("Resposta inválida. Por favor, responda com 's' ou 'n'.")


def condition_ambiente_virtual(path: str) -> Optional[str]:

    """
    Checker of condition to response is a path valid

    Args:
        response(str): response to be checked

    Returns:
        str: return a path from valid.
    """

    if Path(path).exists():
        return path
    else:
        print("Resposta inválida. Por favor, insira um cainho valido")


def install_dependencies_by_type(
    type: Literal["prod", "dev", "doc"] = "prod"
) -> None:

    """
    Process for install dependencies in projects, targeted by
    use of the repository.

    Args:
        type (literal["prod", "dev", "doc"], as default: 'prod'):
            target to user expect using repository.

    Raises:
        ValueError: type parsed is not valid, not in "prod", "dev" or "doc"
    """

    file_requirements = "requirements{other}.txt"

    if type in ["dev", "doc"]:
        file_requirements = file_requirements.format(other=f"-{type}")
    elif type == "prod":
        file_requirements = file_requirements.format(other="")
    else:
        raise ValueError(
            "Value parse is invalid, insert a value in ['prod', 'dev', 'doc']"
        )

    install_requirements(file_requirements)


def execution_line_by_line(command: List[str]) -> None:

    """
    Execute command and print line by line from de process

    Args:
        command (List[str]): Command to execute in process

    Raises:
        subprocess.CalledProcessError: Error generation in runtime by
        process
    """

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # Stream the output in real-time
    for line in iter(process.stdout.readline, ''):
        print(line, end='')

    process.stdout.close()
    process.wait()

    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command)


def install_pip_update(ignore_errors: bool = False):

    """
    Execute update from pip from python in virtual ambient or global python

    args:
        ignore_errors (bool, as default: False): ignore errors if occurred

    Raises:
        subprocess.CalledProcessError: Error generation in runtime by process
    """

    try:
        if os.name == "nt":
            bin = "Scripts"
        else:
            bin = "bin"

        python = os.path.join(
            NAME_PATTERN_VENV, bin, "python.exe"
        )
        command = [
            python, "-m", "pip", "install", "--upgrade", "pip"
        ]
        execution_line_by_line(command=command)

        # print version with pip
        execution_line_by_line(["pip", "--version"])

    except subprocess.CalledProcessError as err:
        if not ignore_errors:
            raise err


def install_wheels_update(ignore_errors: bool = False):

    """
    Execute update from wheels and setuptools from python in virtual ambient
    or global python

    args:
        ignore_errors (bool, as default: False): ignore errors if occurred

    Raises:
        subprocess.CalledProcessError: Error generation in runtime by process
    """

    try:

        command = [
            "pip", "install", "--no-cache-dir", "--upgrade",
            "wheel", "setuptools", "thinc", "aiohttp==3.9.0b0"
        ]
        execution_line_by_line(command=command)

    except subprocess.CalledProcessError as err:
        if not ignore_errors:
            raise err


def purge_cache_pip(ignore_errors=False):

    """
    Execute purge of datas in cache from pip

    args:
        ignore_errors (bool, as default: False): ignore errors if occurred

    Raises:
        subprocess.CalledProcessError: Error generation in runtime by process
    """

    try:

        command = ["pip", "cache", "purge"]
        execution_line_by_line(command=command)

    except subprocess.CalledProcessError as err:
        if not ignore_errors:
            raise err


def install_requirements(file_requirements: str, pip_update: bool = True):

    """
    Installer dependencies by file with dependencies

    Args:
        file_requirements (str): file name using for install
            dependencies
        pip_update (bool, as defaults: True): if try command update to pip
    """

    # check if update pip or no
    if pip_update:
        install_pip_update(True)

    # prevent errors
    install_wheels_update(True)
    purge_cache_pip(True)

    command = ["pip", "install", "--no-cache-dir", "-r", file_requirements]
    execution_line_by_line(command=command)


def get_user_input(
    prompt: str,
    condition: Callable[[str], Optional[str]] = condition_response_yes_no
) -> str:

    """
    Execute an answer in loop until response valid

    Args:
        prompt (str): response of prompt for answer realized
        condition (Callable[[str], Optional[str]], is defaults:
            condition_response_yes_no): function to check condition of
            response from prompt

    Returns:
        str: return a response valid
    """
    while True:
        response = input(prompt).strip().lower()
        response = condition(response)
        if response is not None:
            return response


def main():

    # Pergunta ao usuário se ele já criou um repositório virtual
    create_venv = get_user_input("Você já criou um ambiente virtual? (s/n): ")

    # Checa se o ambiente foi criado:
    #  se Mão ele o criara com os parâmetros padrões:
    #  se Sim, ele foi criado e pedido o caminho até ele:
    if create_venv == "n":
        create_virtual_env()
        enter_virtual_env()
    else:
        name_env = get_user_input(
            "Passe o caminho até o Ambiente Virtual criado: \n",
            condition_ambiente_virtual
        )
        enter_virtual_env(name_env)

    # answer install dependencies
    install_deps = get_user_input("Deseja instalar as dependências? (s/n): ")
    if install_deps == "s":

        # Answer install dependencies to development, document or just
        # dependencies to execute application
        if get_user_input(
            "Você vai desenvolver algo no código? (s/n): "
        ).__eq__('s'):
            install_dependencies_by_type("dev")
        elif get_user_input(
            "Você somente modificar a documentação? (s/n): "
        ).__eq__('s'):
            install_dependencies_by_type("doc")
        else:
            install_dependencies_by_type()


if __name__ == "__main__":
    install_pip_update()

    main()
