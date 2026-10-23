# Manual de uso — EntrePáginas

Público: responsável por uma biblioteca comunitária. Para instalação, consulte README.md. Esta versão utiliza uma única senha de responsável. Durante a avaliação acadêmica, use dados fictícios.

## Entrar e sair

Abra o endereço da aplicação, informe a senha configurada pelo responsável e clique em Entrar. Senha incorreta mantém a tela de acesso. Para encerrar, use Sair no cabeçalho. Se a sessão ou o formulário expirar, recarregue a página e entre novamente.

## Cadastrar livros

Em Cadastros, preencha título, autor e quantidade de exemplares (inteiro entre 1 e 999). Clique em Adicionar ao acervo. Verifique a mensagem de sucesso e o livro na tabela. Todos os exemplares de um registro compartilham título e autor. Esta versão não oferece edição ou exclusão: confira antes de enviar.

## Cadastrar leitores

Informe um nome fictício durante o teste e um código interno exclusivo, como TESTE-001. Clique em Cadastrar leitor. O código é convertido em maiúsculas; repetir o código gera erro. Não use CPF. Verifique a lista de leitores.

## Buscar

Digite parte do título ou do autor na busca do Acervo e clique em Buscar. Limpar restaura a listagem completa. A comparação de acentos depende do comportamento padrão do SQLite. Se não houver resultado, revise o texto ou use parte menor do título.

## Emprestar

É necessário cadastrar pelo menos um livro e um leitor. Em Novo empréstimo, selecione ambos, escolha a data prevista de devolução e clique em Registrar empréstimo. A sugestão é 14 dias; o intervalo permitido vai de hoje até 60 dias. Livros sem exemplares disponíveis não podem ser selecionados. O servidor também recusa operações sem estoque. Confira o histórico e a disponibilidade após a confirmação.

## Devolver

Na tabela Circulação e histórico, localize o livro e o leitor, clique em Devolver e confirme. Cancelar mantém o registro ativo. Confirmar registra a data atual do servidor e libera o exemplar. O empréstimo continua no histórico e não pode ser devolvido novamente.

## Acompanhar prazos

Em andamento significa que o prazo ainda não passou. Em atraso significa prazo anterior ao dia atual, sem devolução registrada. Devolvido mostra a data de retorno. Os indicadores exibem títulos, exemplares disponíveis, empréstimos ativos e atrasados. Não há multas automáticas nem mensagens enviadas ao leitor.

## Resolver erros

- Campo vazio ou fora do limite: corrija e reenvie. Nesta versão, dados digitados podem precisar ser preenchidos novamente após erro.
- Código já cadastrado: use outro código ou selecione o leitor existente.
- Sem exemplar: aguarde uma devolução ou selecione outro livro.
- Formulário expirado: recarregue a página.
- Falha ao salvar: tente novamente e informe ao responsável caso persista; não assuma que a operação foi concluída sem verificar a listagem.

## Relatar problemas

Anote o que tentou fazer, passos, resultado esperado e observado, navegador e dispositivo. Se possível, anexe captura sem informações pessoais. Use FORMULARIO-TESTE.md. Não registre como realizado algo que não testou.
