## Features
1. Count lines of code
2. Count empty lines 
3. Count both physical and logical lines of code 
4. Count comment lines & comment level of code 


## Usage
In order to analyze any code base provide a github repo URL as the first argument. 
`python main.py https://github.com/USER/REPO.git`


## How it works
This tool downloads a git repo to temporary directory, after that runs 
analysis using specified set of directories and extensions and represents
visual data table in your browser
