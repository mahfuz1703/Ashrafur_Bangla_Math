from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProblemSolution, ProblemStatus, UserProfile, Category
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
    category_name = request.GET.get('category', None)

    # Check if a category is selected and filter accordingly
    if category_name:
        problems_solutions = ProblemSolution.objects.filter(categories__name=category_name)
    else:
        problems_solutions = ProblemSolution.objects.all()

    # Paginate the problems and solutions
    paginator = Paginator(problems_solutions, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all categories
    categories = Category.objects.all()

    # Apply formatting fix for each problem and solution
    for problem in page_obj:
        problem.problem = fix_mathjax(problem.problem)
        problem.solution = fix_mathjax(problem.solution)

        # Check if the problem is read by the user
        if request.user.is_authenticated:
            problem.is_read = problem.problemstatus_set.filter(user=request.user, is_read=True).exists()
        else:
            problem.is_read = False

    return render(request, 'index.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_name
    })

# Marks a problem as read/unread and updates user points efficiently
@login_required
def toggle_problem_status(request, problem_id):
    problem = get_object_or_404(ProblemSolution, pk=problem_id)
    
    # Get or create ProblemStatus for the user and problem
    status, created = ProblemStatus.objects.get_or_create(user=request.user, problem=problem)

    if request.POST.get('is_read') == 'true':
        # Mark problem as read
        if not status.is_read:
            status.is_read = True
            status.save()

            # Increase user points
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            user_profile.points += 1
            user_profile.save()
            messages.info(request, "You have earned a point!")
    else:
        # Mark problem as unread
        if status.is_read:
            status.is_read = False
            status.save()

            # Decrease user points
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            if user_profile.points > 0:
                user_profile.points -= 1
                user_profile.save()
                messages.error(request, "You have lost a point!")
    return redirect(request.META.get('HTTP_REFERER', 'show_dataset'))

# Assigns a category to a problem for a specific user without duplicating rows
@login_required
def submit_category(request, problem_id):
    if request.method == 'POST':
        category_name = request.POST.get('category')  # Get the submitted category

        if category_name:
            # Get the selected category
            category = get_object_or_404(Category, pk=category_name)

            # Get the problem
            problem = get_object_or_404(ProblemSolution, pk=problem_id)
            problem.categories.add(category)
            messages.success(request, "Category updated successfully.")

            # Retrieve the existing ProblemStatus instead of creating a new one
            # problem_status, _ = ProblemStatus.objects.get_or_create(
            #     user=request.user,
            #     problem=problem
            # )
            
            # # Update the category instead of creating a new row
            # problem_status.selected_category = category
            # problem_status.save()
        else:
            messages.error(request, "Please select a category.")

    return redirect(request.META.get('HTTP_REFERER', 'show_dataset'))

# Returns the leaderboard data
def get_leaderboard(request):
    leaderboard_data = (
        UserProfile.objects.filter(points__gt=0)  # Only users with at least 1 point
        .order_by('-points')  # Sort by points descending
        .values('user__username', 'points')  # Select only username and points
    )
    return JsonResponse({'leaderboard': list(leaderboard_data)})

# Registers a new user
def register_user(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registered successfully.")
            return redirect('show_dataset')
    return render(request, 'register.html')

# Logs in a user
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_superuser:
                login(request, user)
                messages.success(request, "Admin logged in.")
                return redirect('admin:index')

            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('show_dataset') # Redirect to the previous page / dataset
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'login.html')

# Logs out a user
def logout_user(request):
    """Logs out a user"""
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('show_dataset')