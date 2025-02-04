import csv
from ...models import ProblemSolution
from django.core.management import BaseCommand
import re


def fix_mathjax(text):
    # pattern = r'\$\$(.*?)\$\$'
    pattern_dollar = r'\$\$(.*?)\$\$'

    # Pattern for $...$ (Inline Math) → \[ ... \]
    pattern_dollar_inline = r'\$(.*?)\$'

    # pattern2 = r'\[\s*(.*?)\s*\]'
    pattern_square = r'\[\s*(.*?)\s*\]'

    if re.search(pattern_dollar, text):  # Check if text matches $$...$$ pattern
        return re.sub(pattern_dollar, r'\\[ \1 \\]', text)
    elif re.search(pattern_dollar_inline, text):  
        return re.sub(pattern_dollar_inline, r'\\[ \1 \\]', text)
    elif re.search(pattern_square, text):  # Check if text matches [ ... ] pattern
        return re.sub(pattern_square, r'\\[ \1 \\]', text)         
    return text

class Command(BaseCommand):
    help = 'Load CSV data into the ProblemSolution model'

    def handle(self, *args, **kwargs):
        with open('dataset/numina-math-cot-bn.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                problem, solution = row
                ProblemSolution.objects.create(problem=problem, solution=solution)
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
