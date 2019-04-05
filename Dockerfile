FROM dynverse/dynwrappy:v0.1.0

ARG GITHUB_PAT

RUN pip install git+https://github.com/SheffieldML/GPy.git

RUN pip install git+https://github.com/SheffieldML/GPclust.git

RUN pip install git+https://github.com/Teichlab/GPfates.git@bccd5496b4121b3e634ce7cd5b0bff823b2850fa

COPY definition.yml run.py example.sh /code/

ENTRYPOINT ["/code/run.py"]
