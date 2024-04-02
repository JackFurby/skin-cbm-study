# skin-cbm-study
Webapp for a user study looking at CBMs trained on SkinCon


The following instructions will set up a local instance of the study app. This page is for setup with Conda and is targeted at development. The is a docker file that can also be used

1. Clone repository to your local machine

    ```sh
    git clone https://github.com/JackFurby/skin-cbm-study.git
    ```

2. Install conda

    Install conda onto your machine. Conda should be accessible via the command line. Depending on your operating system you may have to use Conda or Anaconda or another alternative.

3. Create and setup environment

    ```sh
    conda create -n skin-cbm-study python=3.10
    conda activate skin-cbm-study
    pip install -r requirements.txt
    ```

4. Add devices and required files
    The demo requires a couple of files and devices to operate correctly.

    **Model**: Place a Pytorch model file in `skin-cbm-study/study_app/demo/model_saves/<model_file>`  


5. Setup environmental variables for `config.py`  
    For some aspects of the demo to function we will need to provide an environmental variable. To set these variables follow the corresponding steps for your operating system.

    **Windows**:

    i. Open `Control Panel`

    ii. Click on the Advanced system settings link and then click `Environment Variables`. Click create new variable under your users Environment Variables.

    iii. Set a variable for each of the following

    ```sh
    STUDY_MODEL="independent.pth"
    ```

    STUDY_MODEL sets the file name and extension for a Pytorch model

    **Unix based systems**:

    i.

    ```sh
    nano ~/.bash_profile

    ```

    ii. Enter the following variables

    ```sh
    export MAIL_SERVER=smtp.office365.com
    export MAIL_PORT=587
    export MAIL_USE_TLS=1
    export MAIL_USERNAME=<your-username>
    export MAIL_PASSWORD=<your-password>
    ```

    Note: If you need to use special characters enclose the var value in single quotation marks ('')

    STUDY_MODEL sets the file name and extension for a Pytorch model

    iii. Save the variables
    ```sh
    source ~/.bash_profile
    ```
6. Set flask app

```sh
export FLASK_APP=study.py
export FLASK_ENV=development
```

7. Start the application

    You're done! All that is left now is to start the application and start developing!

    ```sh
    flask --app app --debug run
    ```

Deploying the application

It is assumed you have a server setup. We used Ubuntu 22.04

connect to server: `ssh -i ./skin-study ubuntu@131.251.172.175`

1. Update server and install software

  ```sh
  suso apt-get update
  sudo apt-get upgrade
  sudo apt install gunicorn libsm6 libxext6 libgl1 ffmpeg libxrender-dev pymysql
  ```

2. Clone repository to your server

  ```sh
  git clone https://github.com/JackFurby/skin-cbm-study.git
  cd skin-cbm-study
  ```

3. Install pip packages

  ```sh
  pip3 install -r requirements.txt
  pip3 install pymysql
  ```
4. Set environmental variables

  ```sh
  export DATABASE_URL='mysql+pymysql://<USER_NAME>:<PASSWORD>@<DB_URL>:3306/<DB_NAME>'
  source ~/.bash_profile
  ```

5. Start app

  *Note: this should be started such that it will run when you exit the terminal e.g. with tmux*

  gunicorn -b 0.0.0.0:8080 study:app
