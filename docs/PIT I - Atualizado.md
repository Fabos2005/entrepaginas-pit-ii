# PIT I Atualizado

Planejamento do sistema EntrePáginas

Fabricio Feliciano Cardoso
Projeto Integrador Transdisciplinar em Engenharia de Software

## 1 Problema e objetivo

O projeto propõe um sistema web para organizar o acervo e a circulação de livros em uma biblioteca comunitária. Registros dispersos dificultam consultar a disponibilidade, acompanhar prazos e conservar o histórico de empréstimos. O objetivo é reunir essas operações em uma interface acessível ao responsável pela biblioteca.

O cenário é acadêmico. A avaliação da solução será realizada com cinco colegas ou profissionais, utilizando dados fictícios. O planejamento define o escopo, os requisitos, a estrutura dos dados e os critérios que orientarão a implementação e os testes.

## 2 Escopo e público

O usuário direto é o responsável pela biblioteca. Os leitores são cadastrados como participantes dos empréstimos, sem acesso próprio ao sistema. Cada título possui uma quantidade total de exemplares; cada empréstimo corresponde a uma unidade. Não há rastreamento individual de tombo nesta versão.

| Incluído | Fora desta versão |
| --- | --- |
| Acesso por senha; cadastro de livros e leitores | Contas individuais, recuperação de senha |
| Busca; empréstimos; devoluções; histórico | Reservas, renovações, multas e notificações |
| Indicadores de disponibilidade e atraso | Edição e exclusão de cadastros; catálogo externo |

## 3 Organização do trabalho

A execução é organizada em planejamento, construção da versão inicial, verificação técnica, publicação, avaliação por cinco participantes e melhoria da solução. A documentação deve acompanhar as mudanças, e a versão inicial precisa ser preservada para comparação com as correções posteriores.

## 4 Requisitos e critérios de aceitação

| Requisito | Critério de aceitação |
| --- | --- |
| RF01 Acesso | Sem sessão, solicitar senha; credencial inválida não libera o painel. |
| RF02 Livros | Título obrigatório até 120 caracteres, autor até 100 e quantidade inteira de 1 a 999. |
| RF03 Leitores | Nome até 100 caracteres e código interno único até 30, convertido em maiúsculas. |
| RF04 Busca | Filtrar por parte do título ou autor e informar quando não houver resultados. |
| RF05 Empréstimo | Exigir livro, leitor, estoque e prazo entre hoje e os próximos 60 dias. |
| RF06 Devolução | Registrar a data uma única vez, liberar exemplar e manter o histórico. |
| RF07 Atrasos | Identificar empréstimos ativos com prazo anterior ao dia atual. |
| RF08 Indicadores | Exibir títulos, exemplares disponíveis, empréstimos ativos e atrasados. |

## 5 Arquitetura e requisitos de qualidade

A solução utiliza Python com Flask, SQLite e páginas HTML com Jinja, CSS e JavaScript. A organização MVC separa as funções de persistência e validação em models.py, o fluxo HTTP em controllers.py e a apresentação em templates e static. As operações de alteração utilizam POST, seguido de redirecionamento.

O banco deve conservar registros após reinício, rejeitar referências inexistentes e impedir empréstimos acima do estoque. As proteções previstas são consultas parametrizadas, escape de HTML, token CSRF, sessão com HttpOnly e SameSite e segredos fora do repositório. HTTPS e cookie Secure são necessários na hospedagem.

O painel deve ter rótulos claros, estados expressos em texto, foco visível e adaptação a telas estreitas. A navegação por teclado e a apresentação em diferentes telas devem ser verificadas antes do aceite. Não se presume conformidade de acessibilidade sem avaliação.

## 6 Projeto de dados

Modelo conceitual: Livro possui zero ou muitos Empréstimos; Leitor possui zero ou muitos Empréstimos. Cada Empréstimo está vinculado obrigatoriamente a um Livro e a um Leitor. O disponível é calculado como exemplares totais menos empréstimos sem devolução, evitando armazenar saldos redundantes.

Modelo lógico: books(id, title, author, copies); readers(id, name, code); loans(id, book_id, reader_id, borrowed_on, due_on, returned_on). Os atributos descritivos dependem da chave de sua entidade; nome do leitor e dados do livro não são repetidos em loans. O código do leitor é chave candidata. A modelagem adota terceira forma normal dentro do escopo proposto.

| Campo | Tipo e regra |
| --- | --- |
| books.id / readers.id / loans.id | INTEGER, chave primária gerada pelo banco |
| books.title / books.author | TEXT obrigatório; limites de 120 / 100 caracteres |
| books.copies | INTEGER obrigatório, 1 a 999 |
| readers.name / readers.code | TEXT obrigatório; 100 / 30 caracteres; code UNIQUE |
| loans.book_id / loans.reader_id | INTEGER obrigatório, chaves estrangeiras |
| loans.borrowed_on | TEXT com data ISO, gerada pelo servidor |
| loans.due_on | TEXT com data ISO, não anterior à retirada |
| loans.returned_on | TEXT com data ISO ou NULL enquanto ativo |

O projeto físico está em app/schema.sql, com restrições CHECK, NOT NULL, UNIQUE e FOREIGN KEY. A conexão habilita integridade referencial. A verificação de estoque e a inclusão do empréstimo ocorrem na mesma transação, com bloqueio de escrita antes da consulta. Índices auxiliam consultas por livro e situação de devolução.

## 7 Modelagem comportamental

Casos de uso do responsável autenticado: cadastrar livro, cadastrar leitor, consultar acervo, registrar empréstimo, registrar devolução e consultar histórico. No empréstimo, o controlador recebe os dados, o modelo valida entidades e prazo, consulta disponibilidade na transação e grava ou retorna erro. Na devolução, apenas registros ativos podem receber a data de retorno.

Os diagramas de classes, sequência e atividades, além das especificações dos casos de uso, estão em docs/MODELAGEM.md. Eles complementam este planejamento e devem ser atualizados junto das regras de negócio.

## 8 Planejamento da interface

O fluxo principal é acesso → painel → cadastro de livros e leitores → empréstimo → devolução e histórico. O painel reúne indicadores, busca, tabela do acervo, formulário de empréstimo, histórico e cadastros. A disponibilidade deve aparecer junto do livro, e o histórico deve mostrar leitor, retirada, prazo e situação.

Erros devem ser descritos em linguagem direta, como código já cadastrado, prazo inválido ou falta de exemplar. A devolução terá confirmação com possibilidade de cancelamento. Tabelas em telas pequenas poderão rolar horizontalmente. O manual de uso acompanhará a versão publicada.

## 9 Verificação e validação

A verificação técnica deve cobrir entradas válidas e inválidas, persistência, duplicidade, indisponibilidade, prazos, devolução repetida, concorrência pelo último exemplar, acesso sem sessão e proteções contra entradas maliciosas. Os resultados executados serão registrados em docs/test-results.txt; esta seção define o plano, não substitui a evidência.

Após a publicação da versão inicial, cinco participantes receberão o endereço e um formulário. Cada avaliação deverá registrar nome, data, funcionalidades que funcionaram, falhas, correções sugeridas e funcionalidades não testadas com justificativa. Capturas de tela deverão acompanhar falhas quando possível. As cinco respostas serão reunidas em PDF.

As propostas recebidas serão avaliadas por impacto e pertinência ao escopo. Correções incorporadas deverão ser retestadas e documentadas no laudo, com evidências antes e depois.

## 10 Entregáveis e riscos

Entregáveis: código e planejamento no GitHub; aplicação por endereço web; manual; vídeo inicial narrado; PDF das cinco avaliações; laudo de qualidade; vídeo das modificações; Word oficial preenchido com os links. O envio final depende da conclusão dessas etapas.

Riscos: senha compartilhada, falta de limitação de tentativas de login, perda de dados em hospedagem sem disco persistente, calendário incorreto do servidor e ausência de testes reais de usabilidade. Medidas: dados fictícios na avaliação, HTTPS, configuração de fuso, backup do SQLite, validação externa e evolução das proteções antes de uso real.

Referências: material da disciplina e situações-problema no AVA; documentação oficial do Flask sobre banco de dados, fábrica da aplicação e implantação. Especificações detalhadas e referências estão em docs/PROJETO.md.
