#######################################################################################
## DO NOT EDIT THIS FILE! This file was automatically generated from the dockerfile. ##
## Run babelwhale::convert_dockerfile_to_singularityrecipe() to update this file.    ##
#######################################################################################

Bootstrap: shub

From: dynverse/dynwrap:py3.6

%labels
    version 0.1.2

%files
    . /code

%post
    chmod -R 755 '/code'
    pip install GPy
    pip install git+https://github.com/SheffieldML/GPclust.git
    pip install git+https://github.com/Teichlab/GPfates.git@bccd5496b4121b3e634ce7cd5b0bff823b2850fa

%runscript
    exec python /code/run.py

