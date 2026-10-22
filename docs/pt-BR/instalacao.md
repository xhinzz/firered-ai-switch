# Instalação

[English](../setup.md)

## O que é preciso

| | Usado neste projeto | Observações |
|---|---|---|
| Console | Nintendo Switch 2 | FireRed (inglês), a versão avulsa da eShop de fevereiro de 2026. |
| Captura | Placa de captura HDMI USB (`345f:2131`) | Qualquer uma que o OBS mostre. |
| Bluetooth | Adaptador USB CSR `0a12:0001` | Precisa ser um dispositivo USB que o WSL consiga assumir pelo usbipd. A pilha Bluetooth do Windows não emula controle. |
| PC | Windows 11, WSL 2 | A captura usa Win32; o servidor do controle roda no WSL. |
| Programas | Python 3.13, OBS Studio, usbipd-win, Git, Node.js (só para o gerador do ACE) | |
| Modelo | Login do Claude Code ou chave da Anthropic; chave da OpenAI ou do Gemini como alternativa | |

## 1. Python e o decomp

```powershell
git clone https://github.com/xhinzz/firered-ai-switch
cd firered-ai-switch
py -3.13 -m venv .venv
.venv\Scripts\pip install -e ".[dev,painel]"      # acrescente ,openai ou ,gemini para esses provedores
.venv\Scripts\python scripts\baixar_decomp.py     # clone esparso do pret/pokefirered, commit fixado, ~40 MB
.venv\Scripts\pytest                              # 36 testes offline; todos devem passar
```

## 2. OBS

1. Adicione a placa de captura como fonte de vídeo, ocupando o canvas 16:9.
2. Clique com o botão direito na prévia e escolha **Projetor em janela (Prévia)**. Deixe a janela num monitor
   paisagem com pelo menos 1800 px de largura; ela pode ficar atrás de outras janelas.
3. Alternativa: inicie a **Câmera Virtual**. Ela é usada quando o projetor não existe ou não está em 16:9
   (`CAMERA_OBS` = índice DirectShow, padrão 2).
4. Com o OBS em outro idioma, defina no `.env` o começo do título da janela (`OBS_PROJETOR=Windowed Projector` em
   inglês).
5. Não deixe o monitor dormir. Quando o monitor principal desliga, o Windows leva o projetor para outra tela e o quadro
   chega em pé.

A área do GBA é recortada por frações fixas do projetor (`RECORTE` em `fireredia/percepcao/olhos.py`), calibradas para
a versão do Switch. Ajuste se o seu quadro tiver outra borda.

## 3. Controle (WSL + NXBT)

No WSL, use o **Ubuntu 22.04**: o NXBT fixa `dbus-python==1.2.16`, que não compila no Python 3.12 do 24.04.

```bash
sudo apt update && sudo apt install -y python3-pip bluez
sudo pip3 install nxbt
```

Num PowerShell como administrador, compartilhe o adaptador com o WSL uma vez:

```powershell
usbipd list                                  # ache o VID:PID do adaptador
usbipd bind --hardware-id 0a12:0001
```

O `python -m fireredia` anexa o adaptador (`usbipd attach --wsl`), sobe `fireredia/controle/servidor_wsl.py` como root
e espera a conexão. Enquanto o adaptador está anexado, o Windows fica sem Bluetooth. Para devolver:

```powershell
usbipd detach --hardware-id 0a12:0001
```

**Primeiro pareamento:** no Switch, abra *Controles → Alterar empunhadura/ordem* e inicie a IA. O controle pareia
como Pro Controller e o endereço fica salvo em `memoria/switch_endereco.txt`. Depois disso ele reconecta sem essa tela.

**Problemas comuns**

| Sintoma | Causa e solução |
|---|---|
| `maos.estado()` dá `offline`, mas dentro do WSL o `curl 127.0.0.1:8765` responde `connected` | O encaminhamento do localhost do WSL quebrou. Use o IP do WSL: `MAOS_URL=http://<wsl hostname -I>:8765/`. |
| Estado `crashed` com `Connection reset by peer` | O Switch recusou o pareamento salvo. Abra *Alterar empunhadura/ordem* e inicie de novo. |
| Nada conecta e a tela do Switch está apagada | O console dormiu, e um controle emulado não o acorda. Aperte um botão no console. |
| Dois processos `servidor_wsl.py` | Eles disputam o adaptador: `wsl -u root pkill -f servidor_wsl.py`. |

## 4. Provedor do modelo

Copie `.env.exemplo` para `.env`. Ele fica só na máquina e é ignorado pelo git. Escolha o provedor:

| `IA_PROVEDOR` | Chave | Modelos |
|---|---|---|
| `anthropic` (padrão) | `ANTHROPIC_API_KEY` opcional; sem ela, usa o login do Claude Code | Opus no estrategista, Sonnet no executor |
| `openai` | `OPENAI_API_KEY` | `IA_MODELO_ESTRATEGISTA` e `IA_MODELO_EXECUTOR` obrigatórios |
| `gemini` | `GEMINI_API_KEY` | idem |

`IA_ESFORCO_ESTRATEGISTA` e `IA_ESFORCO_EXECUTOR` definem o esforço de raciocínio (`low`, `medium`, `high`,
`nenhum`). Os ajustes da máquina (`MAOS_URL`, `CAMERA_OBS`, `OBS_PROJETOR`, `WSL_DISTRO`, `BLUETOOTH_DONGLE`,
`FIRERED_DECOMP`) também vão no `.env`.

## 5. Rodar

Com o FireRed aberto no mapa:

```powershell
.venv\Scripts\python -m fireredia                          # controle + painel + episódios do agente
.venv\Scripts\python -m fireredia --restricao "só Pokémon tipo fogo"
.venv\Scripts\python -m fireredia.painel.app               # janela do painel com Jogar / Parar
```

Pare com Ctrl+C ou com o botão Parar. O progresso fica em `memoria/`, e a próxima execução continua de onde parou.
Apague `memoria/` para começar outra campanha. Os logs vão para `logs/` (`jogo.log`, `controle.log`) e as fotos dos
scripts para `logs/fotos/`.
