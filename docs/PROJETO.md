# EntrePáginas — documentação técnica e planejamento

**Tema:** organização do acervo e da circulação de livros em uma biblioteca comunitária. O cenário é proposto para fins acadêmicos; a validação com usuários está prevista no plano de avaliação.

O desenvolvimento foi organizado em planejamento, implementação e avaliação. O planejamento definiu o problema, o escopo e as tecnologias que orientaram a construção do sistema.

## 1. Problema, objetivo e escopo

Registros dispersos de empréstimos dificultam consultar disponibilidade, localizar livros emprestados e identificar atrasos. O objetivo é centralizar o acervo e a circulação em uma aplicação web acessível ao responsável. O resultado esperado é registrar um empréstimo válido sem perder a integridade do estoque e manter o histórico da devolução.

A versão contempla um responsável, livros agregados por título, leitores com código interno e empréstimos de uma unidade por registro. Vários exemplares do mesmo título têm características equivalentes; não se rastreiam tombos individuais. Não há reservas, multas, renovação, notificações ou integração com catálogos externos. A ausência de edição e exclusão é limite explícito deste MVP.

## 2. Requisitos e critérios de aceitação

| ID | Requisito | Aceitação verificável |
|---|---|---|
| RF01 | Acesso restrito | Sem sessão, painel redireciona para login; senha incorreta não concede acesso |
| RF02 | Cadastro de livro | Título 1–120 caracteres; autor 1–100; quantidade inteira 1–999 |
| RF03 | Cadastro de leitor | Nome 1–100; código 1–30, único, normalizado em maiúsculas |
| RF04 | Busca | Parte de título ou autor filtra acervo e ausência de resultados é informada |
| RF05 | Empréstimo | Livro e leitor existem, há exemplar e prazo está entre hoje e 60 dias |
| RF06 | Devolução | Atualiza data uma vez, libera exemplar e conserva histórico |
| RF07 | Atrasos | Empréstimo ativo com prazo anterior ao dia atual recebe situação Em atraso |
| RF08 | Indicadores | Exibe títulos, exemplares disponíveis, empréstimos ativos e atrasados |
| RNF01 | Persistência | SQLite mantém registros após reconstrução da aplicação |
| RNF02 | Integridade | Chaves estrangeiras e transação impedem órfãos e excesso de empréstimos concorrentes |
| RNF03 | Interface | Rótulos explícitos, mensagens de resultado, foco visível, layouts para telas estreitas |
| RNF04 | Proteções básicas | SQL parametrizado, escape HTML, CSRF, sessão HttpOnly/SameSite e credenciais no ambiente |

## 3. Regras de negócio

Disponível = quantidade de exemplares − empréstimos sem devolução. Não se armazena saldo duplicado. Datas de empréstimo e devolução são geradas pelo servidor; o fuso do servidor deve corresponder ao calendário da biblioteca (configurar TZ=America/Sao_Paulo na hospedagem). Datas são ISO AAAA-MM-DD. Prazo no dia atual ainda não está atrasado. Código identifica leitor sem coletar CPF, telefone ou e-mail. Um leitor pode emprestar vários títulos e várias unidades, limitado pelo estoque; não há limite individual nesta versão.

## 4. Arquitetura e metodologia

Aplicação monolítica Flask com organização MVC, templates Jinja e SQLite. Controller recebe formulário e verifica sessão, model valida e executa SQL, view apresenta o estado atualizado. Após POST, redirecionamento GET reduz reenvio acidental ao recarregar. O banco ainda garante devolução única e limite de estoque; cadastro repetido de livro pode gerar novo título, limitação conhecida.

O desenvolvimento foi incremental: definição de requisitos, modelo relacional, implementação do fluxo e testes de aceitação automatizados. Não se afirma adoção de Scrum, sprints históricos ou reuniões que não ocorreram. Backlog futuro: edição segura de cadastros, contas individuais, limitação de login, acessibilidade avaliada, paginação e migrações de esquema.

## 5. Modelo conceitual e normalização

Livro 1:N Empréstimo; Leitor 1:N Empréstimo. Cada empréstimo refere um livro e um leitor. O modelo está em terceira forma normal sob estas dependências: id do livro determina título/autor/quantidade; id do leitor determina nome/código (código também é chave candidata); id do empréstimo determina livro/leitor/datas. Título e autor permanecem no cadastro do livro e nome no leitor, sem duplicá-los no empréstimo. Autor é texto descritivo, sem cadastro próprio; trata-se de decisão de escopo, não de normalização bibliográfica completa.

### Dicionário de dados

| Tabela.campo | Tipo SQLite | Regra / significado |
|---|---|---|
| books.id | INTEGER | PK, gerado pelo banco |
| books.title | TEXT | NOT NULL, 1–120 caracteres |
| books.author | TEXT | NOT NULL, 1–100 caracteres |
| books.copies | INTEGER | NOT NULL, 1–999 exemplares totais |
| readers.id | INTEGER | PK |
| readers.name | TEXT | NOT NULL, 1–100 caracteres |
| readers.code | TEXT | NOT NULL, UNIQUE, 1–30 caracteres |
| loans.id | INTEGER | PK |
| loans.book_id | INTEGER | FK books.id, obrigatória |
| loans.reader_id | INTEGER | FK readers.id, obrigatória |
| loans.borrowed_on | TEXT | Data ISO obrigatória, gerada pelo servidor |
| loans.due_on | TEXT | Data ISO obrigatória, maior ou igual ao empréstimo |
| loans.returned_on | TEXT | Data ISO, nula enquanto ativo, não anterior ao empréstimo |

Projeto físico em `app/schema.sql`. Índice composto por livro/devolução auxilia disponibilidade. Índice parcial por prazo apoia consultas futuras de atrasos, embora a tela atual carregue o histórico completo. Exclusões de registros referenciados são restringidas pelo SQLite, sem cascata. A sintaxe completa de datas é validada no modelo; SQL verifica ordem textual de valores ISO. Não execute gravações diretas fora do modelo.

## 6. IHC

Fluxo: login → painel → cadastro de livro/leitor → empréstimo → devolução/histórico. Painel apresenta números e estados textuais; cor não é o único sinal. Formulários usam label, required, limites e tipos apropriados. Confirmação JavaScript precede devolução; cancelar mantém estado. Há navegação por âncoras, link de salto e foco visível. Tabelas em tela estreita têm rolagem horizontal.

Erros de validação voltam ao painel com explicação; os campos não são preservados, uma melhoria de usabilidade pendente. Busca é parcial e o comportamento de maiúsculas/acentos depende do LIKE padrão do SQLite. As views são o protótipo funcional entregue. Não houve teste visual nem auditoria WCAG nesta execução.

## 7. Riscos e evolução

Senha compartilhada não identifica individualmente responsáveis; SQLite em arquivo exige volume persistente e backup; servidor sem fuso configurado pode classificar atrasos pela data UTC; histórico sem paginação limita escala. O MVP é acadêmico e deve ser avaliado com dados fictícios. Uso em instituição real requer requisitos adicionais, proteção de dados, autenticação individual e revisão de segurança.

## 8. Fontes

- Cruzeiro do Sul Virtual. Projeto Integrador Transdisciplinar em Engenharia de Software II. Prof. Me. Artur Marques. Material Teórico, Situações-Problema 1, 2 e 3, modelo de atividade e rubrica. Consultados no AVA da turma, outubro de 2026.
- Flask. Define and Access the Database. https://flask.palletsprojects.com/en/stable/tutorial/database/
- Flask. Gunicorn. https://flask.palletsprojects.com/en/stable/deploying/gunicorn/
- Flask. Deploying to Production. https://flask.palletsprojects.com/en/stable/deploying/

As fontes técnicas fundamentam a configuração e a estrutura da aplicação. Os resultados da avaliação são documentados separadamente, com suas respectivas evidências.
