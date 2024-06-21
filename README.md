## Instalação de Dependências

```bash
  git clone https://github.com/gu1lh3rm3s0rd1/blog-django
  
  cd blog-django
  
  pip install virtualenv
  
  py -m venv .env
  
  source .env/Scripts/activate
  
  pip install -r requirements.txt

  py manage.py makemigrations

  py manage.py migrate
```

## Iniciando o Servidor

```bash
  py manage.py runserver
```

## Em ambientes Linux

```bash
   sudo apt update

   sudo apt install python3-venv

   git clone https://github.com/gu1lh3rm3s0rd1/blog-django

   cd blog-django

   python3 -m venv .env

   source .env/bin/activate

   pip install -r requirements.txt

   python3 manage.py makemigrations

   python3 manage.py migrate

   python3 manage.py runserver
```