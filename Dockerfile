FROM dynverse/dynwrappy:v0.1.0

RUN pip install git+https://github.com/SheffieldML/GPy.git
RUN pip install git+https://github.com/SheffieldML/GPclust.git
RUN pip install git+https://github.com/Teichlab/GPfates.git@bccd5496b4121b3e634ce7cd5b0bff823b2850fa

COPY definition.yml example.h5 run.py /code/

ENTRYPOINT ["/code/run.py"]
