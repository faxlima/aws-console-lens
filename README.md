# aws-console-lens
O aws-console-lens é uma coleção de scripts Python projetados para extrair informações específicas e metadados de uma conta AWS de forma rápida e programática. Em vez de navegar por várias telas do Console de Gerenciamento, esta "lente" foca nos dados que você precisa via terminal.

# Objetivo
Este repositório centraliza ferramentas de consulta (somente leitura) para facilitar a consulta de dados sobre recursos, políticas de segurança e uso de computação em nuvem em ambientes AWS.

# Pré-requisitos
Antes de executar os scripts, certifique-se de ter:
- Python 3.x instalado;
- Credenciais AWS configuradas localmente via aws configure ou variáveis de ambiente;  
- Aplicações diversas:  
```Bash
pip install -r requirements.txt
```

# Estrutura do Repositório
Cada script no diretório raiz é independente e focado em um serviço ou tipo de informação:

|Arquivo|Descrição|
|---|---|
|aws_emr_clusters.py|Baixa os arquivos JSON de clusters EC2 do EMR.|
|aws_glue_datacalog.py|Baixa os arquivos JSON das tabelas e campos do catálogo do GLUE.|
|aws_iam_policies.py|Baixa os arquivos JSON dos usuários, grupos e suas políticas de segurança do IAM.|
|params.py|Parâmetros da aplicação.|

# Como Usar
1. Clone o repositório:
```Bash
git clone https://github.com/faxlima/aws-console-lens.git
```
2. Entre na pasta:
```Bash
cd aws-console-lens
```
3. Execute o script desejado:
```Bash
# Para baixar os arquivos do IAM
python main.py --iam

# Para baixar os arquivos do GLUE
python main.py --glue

# Para baixar os arquivos do EMR
python main.py --emr
```

# Segurança
- Estes scripts realizam apenas chamadas de leitura (Describe*, List*, Get*).
- Nunca versionar arquivos .csv ou logs que contenham IDs de contas ou informações sensíveis geradas pelos scripts.
- Recomenda-se o uso de um perfil IAM com permissões de ReadOnlyAccess.
# Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.