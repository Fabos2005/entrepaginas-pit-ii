# Laudo técnico preliminar de qualidade

**Objeto:** EntrePáginas, implementação acadêmica inicial. **Responsável pelo projeto:** Fabricio Feliciano Cardoso. **Situação:** verificação automatizada e verificação inicial no navegador e na hospedagem concluídas; avaliação por cinco participantes pendente. Este documento não constitui laudo de um avaliador externo.

## Método e evidência

Executada a suíte `python -m unittest discover -s tests -v`, em Python 3.12, Flask 3.1.3 e SQLite. Resultado: **26 testes passaram**, conforme saída integral em `test-results.txt`. Cada teste cria banco temporário e independente; não utiliza dados pessoais reais. Abrangência: regras do modelo, integrações HTTP e SQL, sessão, mensagens e HTML renderizado. Não foi medida cobertura de linhas; 26 testes não significam cobertura total.

## Resultados observados

| Dimensão | Evidência | Conclusão limitada |
|---|---|---|
| Adequação funcional | Cadastro, busca, empréstimo e devolução aprovados na suíte | Fluxos cobertos funcionaram no ambiente de teste |
| Integridade | Estoque esgotado recusado; concorrência aceita um de dois pedidos; FK rejeita órfão | Regras verificadas preservadas |
| Confiabilidade | Reabertura conserva cadastro; devolução repetida recusada | Persistência e idempotência da devolução verificadas |
| Segurança básica | Sessão exigida; CSRF recusado; HTML escapado; SQL parametrizado | Proteções pontuais presentes, sem auditoria ou pentest |
| Usabilidade | Rótulos, feedback e adaptação CSS implementados | Interface inspecionada em desktop e largura de 390 pixels; avaliação pelos cinco participantes pendente |
| Manutenibilidade | MVC, esquema e testes separados | Estrutura documentada, sem métrica quantitativa |
| Eficiência | Suíte executada com base pequena | Não houve ensaio de carga nem meta de latência verificada |
| Portabilidade | Aplicação Python/WSGI e instruções locais | Hospedagem PythonAnywhere executada; instalação local no Windows não verificada |

## Pendências e critérios para aceite

- Ampliar avaliação de teclado, foco e contraste; testar em celulares físicos.
- Coletar cinco avaliações independentes, com falhas, sugestões e imagens quando aplicável.
- Corrigir defeitos encontrados, repetir cenários afetados e registrar evidências antes/depois.
- Acompanhar avaliações na versão publicada com HTTPS e banco persistente.
- Gravar vídeo e completar os links do formulário de entrega.

Conclusão: os cenários automatizados executados passaram. **O aceite final permanece pendente**, sobretudo da validação pelos cinco colegas ou profissionais. Não se afirma conformidade integral, ausência de defeitos ou prontidão para uso real.

## Registro de melhorias

| Item | Origem | Situação |
|---|---|---|
| Evitar empréstimos simultâneos acima do estoque | Análise técnica durante implementação | Transação BEGIN IMMEDIATE implementada e testada |
| Impedir dupla devolução | Análise técnica durante implementação | UPDATE condicional implementado e testado |
| Evitar códigos duplicados de leitores | Análise técnica durante implementação | Normalização e UNIQUE implementados e testados |
| Preservar entradas após erro | Revisão técnica | Pendente |
| Controle de tentativas de login | Revisão técnica | Pendente antes de uso real |
| Sugestões dos cinco participantes | Validação externa | Ainda não coletadas |

O template oficial solicita evidências dos erros e das correções inseridas no laudo e um segundo vídeo da solução atualizada (até cinco minutos). Esses itens permanecem pendentes da avaliação real, não sendo atendidos apenas pela suíte automatizada.

## Verificação da versão publicada

Endereço: https://fabrifeliciano.pythonanywhere.com/. Foram verificados login e logout, cadastro de livro e leitor, busca por autor, recusa de código de leitor duplicado, empréstimo com estoque zero e devolução. Cancelar a confirmação preservou o empréstimo ativo; confirmar registrou a devolução, elevou o estoque disponível de zero para um e manteve o histórico. O reinício do servidor preservou os cadastros e o empréstimo.

A confirmação de devolução foi substituída por controles dentro da página, com as opções Confirmar devolução e Cancelar. A interface foi inspecionada em desktop e em largura de 390 pixels; tabelas extensas mantêm rolagem horizontal. Essa inspeção não substitui a avaliação de acessibilidade nem os cinco pareceres externos.
