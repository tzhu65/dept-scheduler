# dept-scheduler

## Setup
This project requires python3 (along with pip) and npm to be installed.

* Install python requirements 
  * `pip install -r requirements.txt`
  * That should be enough to run the server `python manage.py runserver`
* Install client dependencies 
  * Make sure yarn is installed globally `npm install -g yarn`
  * Go to the directory of the client `cd ./schedule/client`
  * Install dependencies there `yarn install`
  * Build the client code `yarn watch`
  * The packaged code should be found in `./schedule/static/js` and `./schedule/static/css`

By default, the django server is running on `localhost:8000` so go there in your browser. For development run `python manage.py runserver` in one terminal and `yarn watch` in another.

## Deployment Instructions

* Add SSH key to your GitLab profile
* Push code to GitLab
 * `git remote add gitlab https://sc.unc.edu/dept-schedulechecker/dept-scheduler.git`
 * `git push gitlab master`
* Go to OpenShift
 * Go to Project page -> Builds -> dept-scheduler -> Start Build
