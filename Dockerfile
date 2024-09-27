FROM ubuntu:latest
RUN apt update && apt install -y git vim curl htop net-tools && curl vim.kelvinho.org | bash
RUN apt update && apt install -y python3 python3-pip python-is-python3 nodejs npm && pip3 install --break-system-packages flask psycopg2-binary requests unidecode pycryptodome && npm install -g nodemon
RUN curl https://scripts.mlexps.com/pip2 | bash
RUN pip3 install --break-system-packages aigu && echo a1
WORKDIR /code
CMD ["./startup"]



