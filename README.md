Recipe and Grocery List App

A web application that allows users to search for recipes within a specified budget, view ingredients, and add them to a grocery list. The app integrates with Spoonacular API to fetch recipes and ingredients. Users can plan meals that fit their budget and manage their grocery shopping list.
Features

    Recipe Search: Search for recipes based on a specific budget and view the ingredients.

    Grocery List: Add ingredients from recipes to your grocery list.

    Total Grocery Cost Calculation: Calculate the total cost of the grocery items based on real-time prices (optional integration with APIs like Kroger).

    Meal Planning: Organize meals within your specified budget.

Tech Stack

    Frontend: React, Axios, CSS (Custom styles)

    Backend: FastAPI, Python

    APIs:

        Spoonacular API for recipe search and ingredient data

        Kroger API for fetching grocery product prices
Installation

Follow these steps to set up the project locally.
1. Clone the Repository

Clone the repository to your local machine using:

git clone https://github.com/username/repository-name.git

2. Set Up the Backend
2.1 Install Dependencies

Navigate to the backend directory and create a virtual environment:

cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

Install the required dependencies:

pip install -r requirements.txt

2.2 Create .env File

Create a .env file in the backend directory with the following environment variables:

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SPOONACULAR_API_KEY=your_spoonacular_api_key
KROGER_CLIENT_ID=your_kroger_client_id
KROGER_CLIENT_SECRET=your_kroger_client_secret

Make sure to replace the placeholders with actual values.
2.3 Run the Backend

Run the FastAPI server:

uvicorn main:app --reload

The backend will be accessible at http://127.0.0.1:8000.
3. Set Up the Frontend
3.1 Install Dependencies

Navigate to the frontend directory:

cd frontend

Install the required dependencies:

npm install

3.2 Run the Frontend

Start the React development server:

npm start

The frontend will be accessible at http://localhost:3000.
4. Connect the Frontend to the Backend

Ensure the frontend is connected to the backend API by checking the API calls for:

    Recipe search

    Grocery list management

    (Optional) Price calculation for grocery items

Make sure the endpoints in the frontend match the ones exposed by the backend.
Usage

Once everything is set up:

    Search Recipes: Use the search bar to find recipes based on your budget. You can filter recipes based on ingredients.

    Add Ingredients to Grocery List: After finding a recipe, you can add the ingredients to your grocery list.

    View Grocery List: See all the ingredients you need to buy for your recipes.

    Calculate Grocery Cost: (Optional) Calculate the total cost of the grocery items using real-time prices.

Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

    Fork the repository

    Create a new branch (git checkout -b feature-name)

    Commit your changes (git commit -am 'Add feature')

    Push to the branch (git push origin feature-name)

    Create a new Pull Request

License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    Spoonacular API for providing recipe and ingredient data.

    Kroger API for real-time grocery prices (optional integration).
