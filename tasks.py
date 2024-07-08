from invoke import task
import subprocess
import markdown
import os
from re import search
from pathlib import Path
from os import mkdir
from typing import Union


def create_response_html(
    output: str, file_name: str, dir: str = r".\report"
) -> None:

    """
    Transform output from prompts in file type .html

    Args:
        output (str): data to writing in html
        file_name (str): Fina name of output
        dirs (str): path from directory where writing file
    """

    html_output = markdown.markdown(output)

    if not Path(dir).exists():
        mkdir(dir)

    path = os.path.join(dir, file_name)

    with open(path, 'w') as f:
        f.write(html_output)


def check_coverage_test(
    prompt: str,
    expect: Union[float, int] = 70
) -> None:

    """
    Read output from prompt and check if test passed in coverage

    Args:
        prompt (str): text od output from prompt
        expect (Float or Int, as defaults: 70): percent expect to
            passed in coverage
    """

    # Verificar a cobertura de testes
    if "TOTAL" in prompt:

        lines = prompt.split('\n')
        line_total = [line for line in lines if "TOTAL" in line][0]
        print(f"\nCobertura de testes: {line_total.strip()}")

        # isolate value of percent from coverage test
        percent = search("[0-9]{2,3}%", line_total).group()
        percent = percent.replace("%", "")
        result = int(percent)

        # check if passed in coverage
        if result >= expect:
            print("\nPassou na cobertura de testes")
        else:
            print("\nNão Passou na cobertura de testes")
    else:
        print(
            "Erro não foi possível realizar a verificação de cobertura \
                de testes"
        )


@task
def test(ctx):
    """
    Run tests with pytest and stream output in real-time.
    Display a summary of test results and coverage.
    """

    # Comando para executar os testes com cobertura
    test_cmd = ["pytest", "--cov=.", "--cov-report", "term-missing"]
    process = subprocess.Popen(
        test_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # Stream the output in real-time
    response_prompt = ""
    for line in iter(process.stdout.readline, ''):
        response_prompt += line
        print(line, end='')

    process.stdout.close()
    process.wait()

    # Check if tests passed or failed
    if process.returncode == 0:
        print("\nTodos os testes passaram.")
    else:
        print("\nAlguns testes falharam.")

    check_coverage_test(response_prompt)


if __name__ == "__main__":

    text = """
        ============================= test session starts =================
        platform linux -- Python 3.8.10, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
        cachedir: .pytest_cache
        rootdir: /path/to/your/project
        plugins: cov-2.12.1
        collected 2 items

        test_example.py ..                                     [100%]

        ----------- coverage: platform linux, python 3.8.10-final-0 -----------
        Name             Stmts   Miss  Cover
        ------------------------------------
        example.py           6      0   100%
        ------------------------------------
        TOTAL                6      0   100%

        ============================== 2 passed in 0.03s ===============
    """

    create_response_html(text, "test.html")
