## Dependancy 
> pip install Scrapy

> pip install python-resize-image

## Get Data Examvida
> python grab_examvida.py "Clock"

## Get Data Study Press
> python grab_studypress.py "ModelTest01"

> python grab_studypress.py "PhraseIdioms"

> python grab_studypress.py "Books Author(Bank-Eng)"


## Get Image 
> python grab_image.py

## New Target
> http://studypress.org//member/dashboard

## Todo
  
        f= open("out.html","w+")
        f.write(edited_body)
        f.close() 

## Mac setting Environment
sudo -H pip install virtualenv
python3 -m virtualenv env
source env/bin/activate

https://github.com/jazzband/pip-tools

## pip3 to pip
which pip
/usr/local/bin/pip
sudo rm /usr/local/bin/pip
which pip3
/usr/local/bin/pip3
sudo ln -s /usr/local/bin/pip3 /usr/local/bin/pip
