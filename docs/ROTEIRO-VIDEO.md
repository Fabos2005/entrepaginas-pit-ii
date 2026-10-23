# Roteiro de demonstração — alvo de 5 minutos

O template pede no mínimo cinco minutos; a Situação-Problema 3 pede até cinco. Buscar exatamente 5:00 e, se possível, confirmar a divergência com a tutoria. Este é roteiro com ações e tópicos, não vídeo gravado. Ensaiar e ajustar ritmo ao cronômetro. Mostrar apenas dados fictícios e não exibir senhas ou variáveis secretas.

## 0:00–0:35 — problema e proposta

Apresentar nome, disciplina e projeto EntrePáginas. Explicar que o sistema atende ao cenário proposto de uma biblioteca comunitária, organizando acervo e empréstimos. Mostrar a tela de entrada e entrar sem revelar a senha.

## 0:35–1:15 — painel e cadastros

Apresentar indicadores. Cadastrar um livro com título, autor e um exemplar. Cadastrar leitor fictício com código DEMO-001. Mostrar as duas listas. Explicar que o leitor é identificado por código interno, sem CPF, e que o cadastro de um código duplicado é rejeitado.

## 1:15–2:05 — empréstimo e busca

Buscar parte do título. Selecionar livro e leitor, confirmar prazo e registrar empréstimo. Mostrar a disponibilidade zero e o novo registro. Explicar a regra: estoque disponível é calculado como exemplares menos empréstimos ativos. Mostrar a opção sem disponibilidade desabilitada no formulário; explicar que o servidor também verifica, inclusive em transação concorrente.

## 2:05–2:40 — devolução e histórico

Escolher Devolver, cancelar a primeira confirmação e mostrar que nada mudou. Repetir e confirmar. Mostrar o exemplar disponível e o registro histórico com data. Explicar identificação de atrasos pela comparação da data prevista com a data atual do servidor. Não modificar a data do computador para simular evidência.

## 2:40–3:25 — arquitetura e banco

Abrir a árvore do repositório e mostrar models.py, controllers.py e templates. Explicar MVC: modelo valida e persiste, controlador coordena requisições, view apresenta. Mostrar schema.sql e as três entidades. Explicar chaves estrangeiras e a relação de cada empréstimo com um livro e um leitor.

## 3:25–4:10 — testes e qualidade

Executar a suíte e mostrar o resultado real. Destacar indisponibilidade, devolução repetida, prazo inválido, acesso sem sessão e concorrência. Explicar que testes automatizados cobrem cenários definidos, não provam ausência de defeitos. Após testes humanos reais, mostrar síntese dos cinco formulários e um exemplo de correção. Se ainda não houver esses resultados, a entrega permanece pendente: não narrar como realizados.

## 4:10–4:45 — documentação e limitações

Mostrar documentação, modelagem, dicionário e laudo atualizado. Explicar limites: um responsável, sem edição de cadastros, reservas ou multas. Apresentar melhorias futuras pertinentes às avaliações efetivamente recebidas.

## 4:45–5:00 — conclusão

Mostrar aplicação publicada e repositório acessíveis. Retomar resultado: organizar livros, empréstimos, devoluções e histórico. Encerrar em 5:00. Verificar som, legibilidade, duração e permissão de visualização do link antes do envio.

# Segundo vídeo obrigatório — solução atualizada (até 5 minutos)

A última página do template exige outro link: vídeo após coletar feedbacks e executar correções pertinentes. O roteiro acima corresponde ao primeiro vídeo; não substitui este segundo registro. Gravar somente após a validação externa e a atualização.

- 0:00–0:40: identificar versão anterior, versão atual e contexto dos testes com cinco participantes.
- 0:40–1:40: mostrar principais relatos reais e evidências, omitindo informações pessoais desnecessárias.
- 1:40–3:30: demonstrar modificações realizadas, relacionando cada uma ao problema observado. Mostrar antes/depois quando houver evidência.
- 3:30–4:20: repetir cenários corrigidos e mostrar resultado real dos testes automatizados atualizados.
- 4:20–4:50: explicar sugestões não implementadas e justificativas de escopo; apresentar laudo e links atualizados.
- Encerrar antes de 5:00. Não inventar bugs, pareceres, correções ou retestes para preencher o vídeo.
