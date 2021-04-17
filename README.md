# Books to Scrap Monitoring

## Description

Books to Scrap Monitoring is a program that extracts and tracks pricing information from the Books To Scrap online 
bookstore. In beta version, it retrieves information only at the time of its execution.

##  Installation
* The application has been developed with Python 3.9.2.
* The installation procedure applies to a Windows environment using Git Bash.

### clone repository

```bash
$ git clone https://github.com/dardevetdidier/bs_monitoring.git
```

### create and activate virtual environment

```bash
$ cd [project_directory]
$ python -m venv venv
$ cd venv/Script/
$ . activate
```

### Install Python packages 

```bash
$ pip install -r requirements.txt
```

### Execute the script

```bash
$ cd [project_directory]
$ python bs_monitoring.py
```

## Usage

* Create a folder tree ./scrap_dir/category_name/images  (one folder by category)

* The 'category_name' folder contents:
    * a csv file contening the information of all products in the category
    
* The 'images' folder contents:
    * images of each product accessed in the category  

* Once the scraping process is completed, displays the number of products accessed 

## Improvements to expect

* Creation of a graphic interface with a search field by category or product (name, number)
* Real time monitoring