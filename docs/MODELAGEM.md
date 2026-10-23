# Modelagem UML e dados

Os diagramas Mermaid abaixo podem ser visualizados no GitHub. O diagrama de classes representa entidades de persistência; funções de serviço em models.py implementam as operações.

## Classes
```mermaid
classDiagram
class Livro {
  +int id
  +str titulo
  +str autor
  +int exemplares
}
class Leitor {
  +int id
  +str nome
  +str codigo
}
class Emprestimo {
  +int id
  +int livro_id
  +int leitor_id
  +date retirada
  +date prazo
  +date devolucao
}
Livro "1" --> "0..*" Emprestimo
Leitor "1" --> "0..*" Emprestimo
```

## Casos de uso (especificação textual)

Ator: responsável autenticado. UC01 Cadastrar livro; UC02 Cadastrar leitor; UC03 Consultar acervo; UC04 Emprestar livro; UC05 Registrar devolução; UC06 Consultar situação e histórico. Autenticar é precondição de todos. Leitor é entidade participante do negócio, não usuário direto da interface.

UC04: precondições livro/leitor cadastrados e estoque positivo. Fluxo: escolher livro, leitor e prazo; enviar; validar; iniciar transação; conferir estoque; gravar; confirmar. Alternativas: entrada inválida retorna mensagem; estoque esgotado não grava. Pós-condição: empréstimo ativo persistido e disponibilidade reduzida em uma unidade.

UC05: precondição empréstimo ativo. Fluxo: escolher Devolver, confirmar, gravar data do servidor, mostrar confirmação. Alternativas: cancelar mantém estado; ID inexistente ou já devolvido não atualiza. Pós-condição: histórico preservado, disponibilidade acrescida em uma unidade.

## Sequência do empréstimo
```mermaid
sequenceDiagram
actor R as Responsável
participant C as Controller
participant M as Model
participant B as SQLite
R->>C: POST livro, leitor, prazo, CSRF
C->>C: Validar sessão e CSRF
C->>M: borrow(form)
M->>M: Validar campos e prazo
M->>B: BEGIN IMMEDIATE e consultar estoque
alt Disponível e entidades válidas
M->>B: INSERT e COMMIT
M-->>C: Sucesso
else Indisponível
M->>B: ROLLBACK
M-->>C: Erro de validação
end
C-->>R: Redirecionar e apresentar resultado
```

## Atividades
```mermaid
flowchart TD
 A[Selecionar livro e leitor] --> B[Informar prazo]
 B --> C{Dados válidos?}
 C -->|Não| E[Exibir erro]
 C -->|Sim| D{Exemplar disponível?}
 D -->|Não| E
 D -->|Sim| F[Gravar empréstimo]
 F --> G[Atualizar painel]
 E --> A
```
