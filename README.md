# Doug-Server

Doug Serve faz parte do conjunto de projetos que compõem o chatbot da universidade federal de São João del Rei que está sendo Desenvolvido no meu projeto de Iniciação Científica. Está parte representa todo os módulos que funcionam como webhook para o Dialogflow, ou seja, quando uma pergunta é enviada na Interface de chat, este é o módulo capaz de recuperar uma resposta.

# Como instalar
Para instalação de depêndencias utilize :

    pip install -r requirements.txt
Para execução do projeto em localhost utilize:
    
    python manage.py runserver

É necessário também a realização da migração do banco de dados (Neste projeto o postgres).
    
    python manage.py migrate

É possível simplificar todo esse processo utilizando Docker, para isso é necessário apenas utilizar o comando:
    
    docker-compose up --build

Futuramente pretendo adicionar a migração do banco de dados aos arquivos do docker para facilitar ainda mais a utilização deste projeto.

Abraços!!
