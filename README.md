Deploy Time
===========

Como utilizar:
--------------------
Postar um Json (é obrigatório o uso do header de application/json) o endpoint http://`<IP>:<PORTA>/deploy/<nome_da_app>` no seguinte formato:

    {
	  "version": "2.3.4",
	  "user": "lalala",
	  "status": "OK"
	}

No campo status, é aceito somente **OK** ou **NOK**
Se todos os campos forem respeitados, a aplicação responde com um "200 OK", caso contrário "422 UNPROCESSABLE ENTITY" com uma explicação do erro. Exemplo:

    {
	  "status": "Fail",
	  "message": "Invalid Status"
	}
Nesse exemplo foi uma tentativa de inserir o campo status com valores inválidos.

Recuperando os dados armazenados
----------------------------------------------------
O sistema provê uma interface simples (muito simples mesmo!) para download dos arquivos. Acesse: `http://<ip>:<porta>/browse/`

Formato dos dados
----------------------------
Os arquivos são armazenados e exportados em CSV.

Armazenamento
-----------------------
É criado uma estrutura de diretórios no seguinte formato:

    <BASE_DIR>/<nome_da_aplicação>/<ano>/<mês>/<dia>/deploy.csv

Variáveis de Ambiente
--------------------------------
BASE_DIR - Diretório base onde os dados serão armazenados. Default:  "/data"

BIND_ADDR - Endereço IP que o servidor irá fazer bind. Default: 0.0.0.0

PORT - Porta. Default: 5000

Executando
==========
Se desejar ativar a persistência de dados:

    docker run -v <local_storage>:/data <endereço_imagem>:<tag>

Sem persistência

    docker run <endereço_imagem>:<tag>
 
 Alterando a porta

     docker run -e PORT=5555 <endereço_imagem>:<tag>
   
Logs
------
Todas as entradas são logadas para stdout.

    docker log <container_name>

Build
=====
Um script chamado build.sh ajuda a efetuar a geração de novas versões.

    REPO=repository... VERSION=latest ./build.sh <OPTIONS>
    REPO = Registry to push the image [OPTIONAL]
    VERSION = Docker Image Tag [OPTIONAL]
    VENV_PATH = Path to install virtualenv
    Options: 
      tests - Execute unit tests
      build - Build the docker image
      push - Push the docker image to registry
      create-venv - Create python virtualenv and install required deps
      all - Run a test, if pass, make a build, and push


Start on boot
=============
No diretório systemd, há um unit file simples, porém funcional.
Ele deve ser alterado de acordo com as necessidades, por exemplo o path com a persistencia de dados, a rede do docker, path da imagem no registry...
