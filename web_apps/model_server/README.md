



# dev init


to resolve any pyenv issues:
```
if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)" # This only sets up the path stuff.
eval "$(pyenv init -)" # This makes pyenv work in the shell.
eval "$(pyenv virtualenv-init -)" # Enabling virtualenv so it works natively.

```


```
pyenv virtualenv 3.11 model_server
pyenv local model_server

pip3 install -r requirements.txt 

```



# run the hellow world fastapi

```
uvicorn model_server.main:app --reload
```


```
docker build -t model_server .
docker run -d --name mycontainer -p 80:80 model_server
```

# urls

http://127.0.0.1
http://127.0.0.1/docs
http://127.0.0.1/docs#/default/root__get
http://127.0.0.1/openapi.json
