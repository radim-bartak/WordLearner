# Word Learner

This Flask application is designed to help children improve their word writing skills in a fun way. The app presents a picture from a chosen theme (animals, colors, fruits & vegetables, ...) and challenges the player to draw the corresponding word on a digital canvas. A custom-trained CNN model then checks whether the letters are drawn correctly. If the overall drawn word matches the expected word, the user scores a point. Players can also create an account to track their progress over time.

## Installation

1. **Install all dependencies in the project directory:**

   ```
   pip install -r requirements.txt
   ```

2. **Ensure there is a trained model and a dataset file:**

   There should be `letter_cnn.h5` and `letter_dataset.npz` files in the model and dataset directories. That is the dataset file and the trained CNN model used in this application.

   Alternatively you can train a new model from the dataset with the `model.ipynb` file. 

3. **Check the configuration file:**

   Optionally, you can edit the `config.json` file located in the projects directory for Flask configuration.

## Running the App

Start the Flask application by running:

```
python run.py
```

Then, open your browser and visit `http://127.0.0.1:5000` to use the app.

## Usage

1. **Registration & Login:**  
   - Users can register a new account or log in using existing credentials.
   
2. **Theme Selection:**  
   - After logging in, users can choose a theme from the available options.
   
3. **Playing the Game:**  
   - A picture is displayed on the screen.
   - The user draws the corresponding word on a canvas using pen and eraser tools.
   - After drawing, the "Zkontrolovat" button checks whether the word is drawn correctly. The application divides the entire word into individual letters and sends them into the model to check.
   - If the prediction is correct, the user receives a point. The program also sends the correct letters to the dataset for future model learning.

## Technologies Used

- **Backend:** Python, Flask, SQLAlchemy
- **Frontend:** HTML5, CSS, JavaScript
- **Machine Learning:** TensorFlow, Keras, NumPy, PIL

## Project Structure

```
Omeg/
├── app/
│   ├── __init__.py        # Initializes Flask app and database
│   ├── auth_routes.py     # Routes for authentication (register, login, logout)
│   ├── main_routes.py     # Main application routes (theme selection, play, check word)
│   ├── ml.py              # Machine learning functions (image segmentation, prediction)
│   ├── models.py          # Database models (User)
│   ├── config.py          # Application configuration parameters
│   └── templates/         # HTML templates
│   └── static/            # Static files (style.css, images, etc.)
├── model/                 # Contains the trained CNN model files and the dataset
├── run.py                 # Entry point to run the Flask application
└── config.json            # Configuration file
```

## Resources
I used following resources for development of this application:
- https://www.youtube.com/watch?v=jztwpsIzEGc
- https://www.youtube.com/watch?v=aircAruvnKk
- https://www.tensorflow.org/tutorials/images/cnn
- https://www.kaggle.com/code/arbazkhan971/image-classification-using-cnn-94-accuracy
- https://medium.com/@esrasoylu/creating-a-cnn-model-for-image-classification-with-tensorflow-49b84be8c12a
