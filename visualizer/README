
# Visualizer

It is a web application for projecting and visualizing the extracted tiles on a map.
The application also supports date range filtering.

The app contains two sub-apps, a React application for visualization, and
a Django application to process the users requests and prepare the data to be
projected on the map.
## Installation


Django application requirements:
```batsh
$ cd backend
$ pip install -r requirements.txt
```

React requirements:
```bash
$ cd frontend
$ npm install
```
## Locally Usage

#### Using the pre-built frontend
```batch
$ cd backend
$ python manage.py runserver
```
Then in a browser open http://127.0.0.1:8000/

#### using live React frontend
- open a terminal then run the Django project server
    ```batch
    $ cd backend
    $ python manage.py runserver
    ```
- open another terminal and run the React project server
    ```bash
    $ cd frontend
    $ npm start
    ```
- open the file `frontend/src/components/TreeCoverLossMap.js line 16`, the url should point to your local Django project server url
    ```javascript
    const url = "http://127.0.0.1:8000/tiles/{z}/{x}/{y}.png";
    ```
    Then in a browser open http://127.0.0.1:3000/


## Deployment

To deploy this project you have first to build the frontend project and copy the
built files to `backend/static/main` folder. If backend and frontend folders are
in the same place, then the copy is done automatically after the built is done.
otherwise you have to copy it manually.

### steps:

1. Replace `frontend/src/components/TreeCoverLossMap.js line 16` by your hosting address.

2. Build fontend project.
  ```bash
    $ cd frontend
    $ npm run build
  ```

3. copy the built files if not done automatically.
  ```bash
  $ cp -r ./output/* [path to folder backend/static/main]
  ```

4. Copy the extracted tiles folders to `backend/images/`. *images* folder should contains
  two sub-folders `alert/` and `alertDate/`.
  > **Note**: *We can use a storage server to store the tiles.
  > The app is not support the external storage server yet.*

5. Add your hosting address to `ALLOWED_HOSTS` list in the file
  `backend/api/settings.py line 31`

6. Upload backend project to your hosting server.

**Note**: *You have to repeate the steps 2, 3, 6 every time you make changes in the frontend*.

> **Note**: You can deploy the project without building the frontend, but you will need to host two servers, one for React porject and the other for Django project.