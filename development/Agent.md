# Agent

## Objetivo
Definir como agentes devem atuar no monorepo para manter consistencia tecnica, qualidade e seguranca.

## Escopo
Aplica-se a alteracoes de codigo, infraestrutura e documentacao em qualquer servico.

## Regras De Operacao

- Respeitar os limites de arquitetura (`api`, `application`, `domain`, `infra`).
- Priorizar mudancas pequenas, rastreaveis e com justificativa clara.
- Seguir TDD: escrever teste primeiro, depois implementar o minimo para passar.
- Tratar seguranca (senha, token, segredo) como fluxo explicito e revisavel.
- Atualizar documentacao sempre que contrato, regra de negocio ou arquitetura mudar.
- Em caso de ambiguidade tecnica, registrar perguntas objetivas antes de alterar codigo.

## Checklist Para Escrever Codigo

- [ ] Entendi o escopo funcional e os impactos tecnicos da mudanca.
- [ ] Escrevi/ajustei teste antes da implementacao (TDD).
- [ ] Mantive separacao de camadas e dependencias corretas.
- [ ] Preservado contrato publico ou documentada a alteracao.
- [ ] Cobri cenario principal, erro e regressao relevante em testes.
- [ ] Nao introduzi segredo, credencial ou dado sensivel no codigo.
- [ ] Comandos/testes locais essenciais foram executados com sucesso.

## Checklist Para Escrever Documentacao

- [ ] Documento reflete o estado atual do codigo.
- [ ] Conteudo e estavel (sem historico de chat ou processo temporario).
- [ ] Links e caminhos estao validos no repositorio.
- [ ] Contratos e regras de negocio estao consistentes com implementacao.
- [ ] Texto esta claro, direto e sem duplicidade com outros documentos.

## Limites

- Nao alterar contrato de API silenciosamente.
- Nao vazar detalhes internos de excecao para clientes externos.
- Nao acoplar `domain` a framework ou tecnologia de infraestrutura.
- Nao executar acoes destrutivas sem solicitacao explicita.

## Referencias

- [Index.md](./Index.md)
- [Contributing.md](./Contributing.md)
- [ValidationRoadmap.md](./ValidationRoadmap.md)
- [Arquitetura do sistema](../docs/Architecture.md)
