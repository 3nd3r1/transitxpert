""" tasks.py """

import sys
import os
import anybadge
from invoke.tasks import task


@task
def start(ctx):
    if sys.platform.startswith("win"):
        ctx.run("py soteriareitti/main.py")
    else:
        ctx.run("python soteriareitti/main.py")


@task
def debug(ctx):
    if sys.platform.startswith("win"):
        ctx.run("py soteriareitti/main.py debug")
    else:
        ctx.run("python soteriareitti/main.py debug")


@task
def benchmark(ctx):
    if sys.platform.startswith("win"):
        ctx.run("py tests/benchmark_test.py")
    else:
        ctx.run("python tests/benchmark_test.py")


@task
def test(ctx):
    ctx.run("pytest .")


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest .")


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html -d ./docs/coverage")
    ctx.run("coverage-badge -o ./docs/images/coverage.svg -f")


@task
def lint(ctx):
    _result = ctx.run("pylint soteriareitti", warn=True)

    pylint_output = os.popen("pylint --output-format=text soteriareitti").read()
    pylint_score = float(pylint_output.split("/")[-3].split(" ")[-1].strip())

    badge = anybadge.Badge(
        'pylint',
        pylint_score,
        default_color='forestgreen',
        value_suffix='/10'
    )
    badge.write_badge('./docs/images/pylint-badge.svg', overwrite=True)


@task
def build(ctx):
    ctx.run("rm -rf dist/soteriareitti/")
    ctx.run("""pyinstaller soteriareitti/main.py -n SoteriaReitti -w
             --icon=resources/icon.ico""")
    ctx.run("cp -r resources dist/soteriareitti/_internal")
    ctx.run("cp .env dist/soteriareitti/")
