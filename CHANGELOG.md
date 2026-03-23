# Changelog

## 2026-03-23 - Ajustes de autenticacao, validacao e rotas publicas

### O que mudou
- Corrigido o comportamento dos endpoints publicos `register`, `login` e `refresh` para ignorarem headers `Authorization` invalidos ou expirados enviados pelo Swagger.
- Corrigido o mesmo problema nas rotas publicas de documentacao `/api/schema/` e `/api/schema/swagger/`.
- Normalizado o email no cadastro, login e persistencia para evitar duplicidade por caixa alta/baixa e falhas de autenticacao.
- Adicionadas validacoes de telefone e data de nascimento no cadastro e na atualizacao de perfil.
- Padronizadas mensagens principais de erro em portugues na camada comum de excecoes.
- Otimizado o script `iniciar_if_bank.ps1` para evitar reinstalacao desnecessaria de dependencias em toda execucao.

### Arquivos de destaque
- `apps/users/views/auth_views.py`
- `apps/users/urls/__init__.py`
- `common/views/docs.py`
- `config/urls.py`
- `apps/users/serializers/register_serializers.py`
- `apps/users/serializers/auth_serializers.py`
- `apps/users/serializers/profile_serializers.py`
- `apps/users/services/user_service.py`
- `apps/users/validators/user_fields.py`
- `apps/users/models/user.py`
- `apps/users/models/managers.py`

### Testes adicionados ou ampliados
- Cobertura para login com email em caixa alta/baixa.
- Cobertura para telefone invalido no cadastro.
- Cobertura para data de nascimento futura no cadastro e no perfil.
- Cobertura para `register`, `login` e `refresh` com header `Authorization` invalido.
- Cobertura para `schema`, `swagger` e `healthcheck` com header `Authorization` invalido.

### Validacao executada
- `python manage.py check --settings=config.settings.test`
- `python manage.py test --settings=config.settings.test`
- `python manage.py spectacular --validate --settings=config.settings.test`

### Observacao importante
- Existe uma migration nova em `apps/users/migrations/0002_alter_user_birth_date_alter_user_cpf_and_more.py`.
- Antes de subir fora do ambiente de teste, rode `python manage.py migrate`.
