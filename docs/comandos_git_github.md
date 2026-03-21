# 🚀 Git / Git Bash — Comandos Essenciais (Resumo Profissional)

## 🔹 1. Inicialização e configuração

| Comando | O que faz | Onde executa |
|--------|----------|--------------|
| git init | Inicializa um repositório Git na pasta | Local |
| git clone <url> | Clona um repositório remoto | Local → Remoto |
| git config --global user.name "Nome" | Define nome do usuário | Local |
| git config --global user.email "email" | Define email do usuário | Local |

---

## 🔹 2. Controle de arquivos

| Comando | O que faz | Onde executa |
|--------|----------|--------------|
| git status | Mostra estado dos arquivos | Local |
| git add . | Adiciona TODOS arquivos para staging | Local |
| git add <arquivo> | Adiciona arquivo específico | Local |
| git restore <arquivo> | Descarta alterações do arquivo | Local |

---

## 🔹 3. Versionamento (commit)

| Comando | O que faz | Onde executa |
|--------|----------|--------------|
| git commit -m "msg" | Salva alterações no histórico | Local |
| git commit -am "msg" | Add + commit (arquivos já rastreados) | Local |
| git log | Histórico de commits | Local |
| git diff | Mostra diferenças | Local |

---

## 🔹 4. Branches (linhas de desenvolvimento)

| Comando | O que faz | Onde executa |
|--------|----------|--------------|
| git branch | Lista branches | Local |
| git branch <nome> | Cria nova branch | Local |
| git checkout <branch> | Troca de branch | Local |
| git checkout -b <branch> | Cria e troca | Local |
| git merge <branch> | Junta branches | Local |

---

## 🔹 5. Integração com GitHub (remoto)

| Comando | O que faz | Onde executa |
|--------|----------|--------------|
| git remote -v | Lista repositórios remotos | Local |
| git remote add origin <url> | Conecta ao GitHub | Local → Remoto |
| git push origin <branch> | Envia commits | Local → Remoto |
| git pull | Atualiza do remoto | Remoto → Local |
| git fetch | Busca atualizações sem aplicar | Remoto → Local |

---

## 🔹 6. Correções e limpeza

| Comando | O que faz | Onde executa |
|--------|----------|--------------|
| git reset --hard | Volta estado do projeto (perigoso) | Local |
| git rm <arquivo> | Remove arquivo do Git | Local |
| git clean -fd | Remove arquivos não rastreados | Local |

---

## 🔹 7. Fluxo padrão (ESSENCIAL)

```bash
git add .
git commit -m "sua alteração"
git push origin sua-branch
```

---

## 🔥 Visão profissional

| Etapa | Comando | Objetivo |
|------|--------|---------|
| Preparar | git add | Selecionar mudanças |
| Registrar | git commit | Versionar |
| Publicar | git push | Subir para GitHub |
