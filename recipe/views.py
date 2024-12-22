from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm, EditNutritionForm
from .models import EditNutrition, ListItem, LikedRecipe
from django.http import JsonResponse
import pandas 
import joblib
import random
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

# Create your views here.
def home(request): 
	return render(request, 'main/main.html', {})

def test(request): 
	return render(request, 'main/test.html', {})

def login_user (request):
	if request.method == 'POST': #if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:# if user exist
			login(request, user)
			messages.success(request,('Youre logged in'))
			return redirect('main') #routes to 'home' on successful login  
		else:
			messages.success(request,('Error logging in'))
			return redirect('login') #re routes to login page upon unsucessful login
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request,('Youre now logged out'))
	return redirect('main')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and get the instance
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            # Automatically assign random nutrition values
            EditNutrition.objects.create(
                user=user,
                calories=random.randint(1500, 2500),
                fat=random.uniform(50, 100),
                saturated_fat=random.uniform(10, 30),
                cholesterol=random.uniform(100, 300),
                sodium=random.uniform(1500, 2300),
                carbohydrate=random.uniform(200, 300),
                fiber=random.uniform(20, 50),
                sugar=random.uniform(50, 100),
                protein=random.uniform(50, 100)
            )
            
            # Authenticate and log in the user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You are now registered and logged in.')
            return redirect('home')
        else:
             messages.success(request,('Error to register'))
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'authenticate/register.html', context)

def edit_profile(request):
    user = request.user
    nutrition_data = get_object_or_404(EditNutrition, user=user)

    if request.method == 'POST':
        # Profile form handling
        profile_form = EditProfileForm(request.POST, instance=user)

        # Nutrition form handling
        nutrition_form = EditNutritionForm(request.POST, instance=nutrition_data)

        # Check which form was submitted and process accordingly
        if 'profile_submit' in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
        else:
            messages.success(request, 'Error to update.')

        if 'nutrition_submit' in request.POST and nutrition_form.is_valid():
            nutrition_form.save()
            messages.success(request, 'Your nutrition preferences have been updated.')

        return redirect('edit_profile')

    else:
        # If GET request, instantiate the forms
        profile_form = EditProfileForm(instance=user)
        nutrition_form = EditNutritionForm(instance=nutrition_data)

    context = {
        'form': profile_form,
        'nutrition_form': nutrition_form,
        'nutrition_data': nutrition_data,
    }

    return render(request, 'authenticate/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'You have edited your password')
            return redirect('home')
        else:
            messages.error(request, 'You failed to edit your password')
    else:
        # Passes in user information
        form = PasswordChangeForm(user=request.user)

    return render(request, 'authenticate/change_password.html', {'form': form})

def item(request):
    # Handle form submission
    if request.method == "POST":
        item_name = request.POST.get("item_name")  # Get the item name from the form
        if item_name:
            ListItem.objects.create(user=request.user, item_name=item_name)  # Create the item

    # Get all items for the logged-in user
    user_items = ListItem.objects.filter(user=request.user)

    return render(request, 'authenticate/item.html', {'user_items': user_items})

def remove_item(request, item_id):
    item = get_object_or_404(ListItem, id=item_id, user=request.user)
    item.delete()
    return redirect('item')  # Redirect back to the item list page

# Load pre-trained artifacts
scaler = joblib.load(open('recipe/static/artifacts/scaler.pkl', 'rb')) 
neigh = joblib.load(open('recipe/static/artifacts/neigh.pkl', 'rb'))
df = joblib.load(open('recipe/static/artifacts/recipes.pkl', 'rb'))

def scaling(dataframe):
    if dataframe.empty:
        raise ValueError("No data available for scaling.")
    scaler = StandardScaler()
    prep_data = scaler.fit_transform(dataframe.iloc[:, 12:21].to_numpy())
    return prep_data, scaler


def build_pipeline(neigh,scaler,params):
    transformer = FunctionTransformer(neigh.kneighbors,kw_args=params)
    pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])
    return pipeline

def extract_data(dataframe, ingredient_filter, max_nutritional_values):
    extracted_data = dataframe.copy()
    for column, maximum in zip(extracted_data.columns[12:21], max_nutritional_values):
        extracted_data = extracted_data[extracted_data[column] < maximum]

    if ingredient_filter is not None:
        if isinstance(ingredient_filter, str):
            ingredient_filter = [ingredient_filter]
        for ingredient in ingredient_filter:
            extracted_data = extracted_data[extracted_data['RecipeIngredientParts'].str.contains(ingredient, case=False, regex=False)]
        #15/12/2024 print(extracted_data.head())  # Check the filtered data

    return extracted_data

def apply_pipeline(pipeline,_input,extracted_data):
    return extracted_data.iloc[pipeline.transform(_input)[0]]

def recommand(dataframe,_input,max_nutritional_values,ingredient_filter=None,params={'return_distance':False}):
    extracted_data=extract_data(dataframe,ingredient_filter,max_nutritional_values)
    prep_data,scaler=scaling(extracted_data)
    neigh = neigh.fit(prep_data)
    pipeline=build_pipeline(neigh,scaler,params)
    return apply_pipeline(pipeline,_input,extracted_data)

def recommend_by_calories(neigh, dataframe, max_daily_calories, max_nutritional_values, ingredient_filter=None, params={'return_distance': False}):
    # Extract data based on maximum nutritional values and ingredient filter
    extracted_data = extract_data(dataframe, ingredient_filter, max_nutritional_values)

    # Handle the case when no data is extracted
    if extracted_data.empty:
        return pandas.DataFrame()  # Return an empty DataFrame

    # Scale the data
    prep_data, scaler = scaling(extracted_data)

    # Fit the Nearest Neighbors model
    neigh = neigh.fit(prep_data)

    # Build the pipeline
    pipeline = build_pipeline(neigh, scaler, params)

    # Create a test input with specified calories
    test_input = np.array([[0] * 9])  # Assuming the input shape is (1, 9) for 9 nutritional features
    test_input[0, 1] = max_daily_calories  # Set the calories

    # Get recipe recommendation based on test input
    recommended_recipe = apply_pipeline(pipeline, test_input, extracted_data)

    return recommended_recipe


# Main view for recipe recommendations
def recommend_recipe(request):
    # Default max nutritional values
    max_values = [500, 15, 5, 50, 600, 50, 5, 20, 25]

    # Retrieve user's custom nutrition preferences, if available
    if request.user.is_authenticated:
        user = request.user
        nutrition_data = get_object_or_404(EditNutrition, user=user)
        max_values = [
            getattr(nutrition_data, "calories", 500),
            getattr(nutrition_data, "fat", 15),
            getattr(nutrition_data, "saturated_fat", 5),
            getattr(nutrition_data, "cholesterol", 50),
            getattr(nutrition_data, "sodium", 600),
            getattr(nutrition_data, "carbohydrate", 50),
            getattr(nutrition_data, "fiber", 5),
            getattr(nutrition_data, "sugar", 20),
            getattr(nutrition_data, "protein", 25),
        ]

    if request.method == 'POST':
        if 'like' in request.POST:
            # Handle recipe "like" functionality
            recipe_id = int(request.POST.get('recipe_id'))
            recommendations_list = request.session.get('recommendations_list', [])

            # Find the recipe in the recommendations list
            recipe = next((r for r in recommendations_list if r['RecipeId'] == recipe_id), None)

            if not recipe:
                return JsonResponse({'message': 'Recipe not found!'}, status=404)

            # Check if the recipe is already liked
            if LikedRecipe.objects.filter(user=request.user, recipe_id=recipe_id).exists():
                return JsonResponse({'message': 'Recipe already liked!'}, status=400)

            # Save the liked recipe to the database
            liked_recipe = LikedRecipe.objects.create(
                user=request.user,
                recipe_id=recipe['RecipeId'],
                name=recipe['Name'],
                author_id=recipe.get('AuthorId', 0),
                author_name=recipe.get('AuthorName', ''),
                total_time=recipe.get('TotalTime', ''),
                description=recipe.get('Description', ''),
                images=recipe.get('Images', ''),
                calories=recipe.get('Calories', 0.0),
                fat_content=recipe.get('FatContent', 0.0),
                saturated_fat_content=recipe.get('SaturatedFatContent', 0.0),
                cholesterol_content=recipe.get('CholesterolContent', 0.0),
                sodium_content=recipe.get('SodiumContent', 0.0),
                carbohydrate_content=recipe.get('CarbohydrateContent', 0.0),
                fiber_content=recipe.get('FiberContent', 0.0),
                sugar_content=recipe.get('SugarContent', 0.0),
                protein_content=recipe.get('ProteinContent', 0.0),
                recipe_instructions=recipe.get('RecipeInstructions', ''),
                recipe_ingredients=recipe.get('RecipeIngredientParts', ''),
            )
            liked_recipe.save()

            return JsonResponse({'message': 'Recipe liked successfully!'}, status=200)

        # Handle search by ingredient if present in POST data
        ingredient = request.POST.get('ingredient')
        recommendations = recommend_by_calories(neigh, df, 500, max_values, ingredient)
    else:
        # Handle GET request and return recommendations
        recommendations = recommend_by_calories(neigh, df, 500, max_values)

    # Check if no recommendations are found
    if recommendations.empty:
        return render(request, 'main/main.html', {'message': 'No recipes found. Please try a different ingredient or adjust your preferences.', 'recommendations': []})

    # Convert recommendations to list of dictionaries
    recommendations_list = recommendations.to_dict(orient='records')

    # Store recommendations in session for further use (e.g., like functionality)
    request.session['recommendations_list'] = recommendations_list

    return render(request, 'main/main.html', {'recommendations': recommendations_list})




def liked_recipes(request):
    if request.method == 'POST' and 'remove_like' in request.POST:
        recipe_id = int(request.POST.get('recipe_id'))
        try:
            liked_recipe = LikedRecipe.objects.get(user=request.user, recipe_id=recipe_id)
            liked_recipe.delete()
            return JsonResponse({'message': 'Recipe removed from likes!'}, status=200)
        except LikedRecipe.DoesNotExist:
            return JsonResponse({'message': 'Recipe not found!'}, status=404)

    # For GET requests, display the liked recipes
    liked_recipes = LikedRecipe.objects.filter(user=request.user)
    return render(request, 'main/menu.html', {'liked_recipes': liked_recipes})










