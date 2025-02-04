from django.core.paginator import Paginator
from django.shortcuts import render
from .models import ProblemSolution
import re

# Function to fix MathJax formatting
def fix_mathjax(text):
    text = text.replace(", ", ",").replace(",", ", ")

    pattern_dollar = r'\$\$(.*?)\$\$'

    pattern_dollar_inline = r'\$(.*?)\$'

    pattern_square = r'\[\s*(.*?)\s*\]'

    underscore = r'_(\d+)'

    if re.search(pattern_dollar, text):  # Check if text matches $$...$$ pattern
        return re.sub(pattern_dollar, r'\\( \1 \\)', text)
    elif re.search(pattern_dollar_inline, text):  # Check if text matches $...$ pattern
        return re.sub(pattern_dollar_inline, r'\\( \1 \\)', text)
    elif re.search(pattern_square, text):  # Check if text matches [ ... ] pattern
        return re.sub(pattern_square, r'\\( \1 \\)', text)   
    elif re.search(underscore, text):
        return re.sub(underscore, r'_{\text{\1}}', text)
    return text

# View function to render dataset with pagination
def show_dataset(request):
    problems_solutions = ProblemSolution.objects.all()
    paginator = Paginator(problems_solutions, 15)  # Show 20 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Apply formatting fix for each problem and solution
    for problem in page_obj:
        problem.problem = fix_mathjax(problem.problem)
        problem.solution = fix_mathjax(problem.solution)

    return render(request, 'index.html', {'page_obj': page_obj})


