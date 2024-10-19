from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = 'Run Flake8 and then run tests if Flake8 passes'

    def handle(self, *args, **kwargs):
        # Run Flake8
        result = subprocess.run(['flake8', '.'], capture_output=True, text=True)

        if result.returncode == 0:
            self.stdout.write(self.style.SUCCESS('Flake8 passed. Running tests...'))
            test_result = subprocess.run(['python', 'manage.py', 'test'], capture_output=True, text=True)
            self.stdout.write(test_result.stdout)
        else:
            self.stdout.write(self.style.ERROR('Flake8 errors detected:'))
            self.stdout.write(result.stderr)
            self.stderr.write("Fix them before running tests.")
            exit(1)
