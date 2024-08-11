# ReciPY

#### Video Demo: https://youtu.be/uIdtA-aYVho

#### Description:

ReciPY is an innovative application that allows users to discover a wide array of recipes, from local favorites to international cuisines. Utilizing the Kivy library, which supports graphical user interface (GUI) development, the app provides an intuitive and interactive experience for searching and exploring recipes. The core functionality of ReciPY revolves around an API provided by Edamam.com, a popular resource for culinary data. This API grants access to a vast repository of recipe information, including names, links to the original sources, images, and ingredient lists. ReciPY focuses on these key elements to deliver a streamlined and user-friendly experience. The app is organized into three main screens or modules, each serving a specific purpose in the user's journey.

#### Modules:

**TitleScreen:** This is where the application starts, featuring the title and an image of various foods. There are two buttons on this screen: Start and Exit. The Exit button leads to the Exit Screen, where users are asked to confirm if they wish to quit the app. The Start button navigates to the Main Screen.

**Main Screen:** Here, users can search for recipes. The screen initially displays three widgets: the Exit Button, the Search Bar, and the Search Button. Users can enter their desired dish in the search bar, and the Main Screen will display 19 results. Two additional buttons, Back and Next, appear to navigate through the results. The results are displayed in batches of five, with the last batch showing four, as the API returns 19 recipes in total.

**Recipe Screen:** This screen displays detailed information about a selected recipe from the Main Screen. It includes the recipe's name, an image of the dish, a link to the original source, and the list of ingredients.

ReciPY is not a linear app. Users can search for and select a dish, then return to the Main Screen to search for more dishes as desired. The API provides access to a vast and diverse collection of recipes, encompassing foods from every culture, whether Asian or Western.

#### Libraries I used:

**Kivy:** This is the library I used to make ReciPY a graphical user interface application. It allows for building windows, buttons, search bars, images, and text elements.
**KivyMD:** This library extends Kivy by providing additional widgets, such as MDFLatButton and MDTextField, which are necessary for the app's functionality.
**Requests:** This library enables me to send requests to the server to obtain data from the API, such as recipe names, images, links, and ingredients.
**Configparser:** This library allows me to conceal my app ID and app key when making API requests. Regardless of the programming language, I aim to practice secure coding while developing the application.

#### About the Developer

I am Jhon Jhio Dalagan from the Philippines. I am a recent graduate with a BSIT degree. I want to pursue a Software Development career that is why i want to learn more different programming languages like python. My motivation on creating ReciPY is from my previous plan to create an application something like ReciPY but more advance that it won't just get recipe results but with AI integration and more features. Though now that i created ReciPY, i feel like i need to learn more to make the application i envisioned.
