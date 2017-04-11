# Politicos API

Aqui você vai encontrar os dados, ferramentas e recursos para realizar pesquisas, desenvolver aplicativos, visualizações de dados, e muito mais.


## Instalação

1.  Clone o repositório:

        git clone https://github.com/olhoneles/politicos.git

1.  Crie um [*virtualenv*](http://virtualenvwrapper.readthedocs.org/en/latest/install.html):

        cd politicos
        mkvirtualenv politicos

1.  Instale as dependências:

        make setup

1.  Crie o banco de dados:

        make data

1.  Inicialize o projeto:

        make run

1.  Se você quiser sobrescrever algumas configurações do settings.py, como SECRET_KEY, DATABASES, ALLOWED_HOSTS, por favor crie o arquivo `politicos/local.config`.


## Como Contribuir

Participe da [lista de email](http://listas.olhoneles.org/cgi-bin/mailman/listinfo/montanha-dev) e também via IRC no canal [#olhoneles](irc://irc.freenode.net:6667/olhoneles) na Freenode.

Faça uma cópia do repositório e envie seus pull-requests.


## Licença

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
