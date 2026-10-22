# Setup

[Português](pt-BR/instalacao.md)

## What you need

| | Used in this project | Notes |
|---|---|---|
| Console | Nintendo Switch 2 | FireRed (English), the standalone eShop release of February 2026. |
| Capture | USB HDMI capture card (`345f:2131`) | Anything OBS can show. |
| Bluetooth | USB dongle, CSR `0a12:0001` | It must be a USB device that WSL can own through usbipd. Windows' own Bluetooth stack can't emulate a controller. |
| PC | Windows 11, WSL 2 | Screen capture uses Win32; the controller server runs in WSL. |
| Software | Python 3.13, OBS Studio, usbipd-win, Git, Node.js (only for the ACE generator) | |
| Model | Claude Code login or an Anthropic API key; OpenAI or Gemini key as alternatives | |

## 1. Python and the decomp

```powershell
git clone https://github.com/xhinzz/firered-ai-switch
cd firered-ai-switch
py -3.13 -m venv .venv
.venv\Scripts\pip install -e ".[dev,painel]"      # add ,openai or ,gemini for those providers
.venv\Scripts\python scripts\baixar_decomp.py     # sparse clone of pret/pokefirered, pinned commit, ~40 MB
.venv\Scripts\pytest                              # 36 offline tests; all should pass
```

## 2. OBS

1. Add the capture card as a video source and make it fill the 16:9 canvas.
2. Right-click the preview and choose **Windowed Projector (Preview)**. Leave the window on a landscape monitor at
   least 1800 px wide; it can stay behind other windows.
3. Alternatively, start the **Virtual Camera**. It is used whenever the projector is missing or not 16:9
   (`CAMERA_OBS` = DirectShow index, default 2).
4. If your OBS is not in Portuguese, set `OBS_PROJETOR=Windowed Projector` in `.env`. The default matches the
   Portuguese title "Projetor".
5. Keep the monitor from sleeping. When the main monitor turns off, Windows moves the projector to another screen and
   the frame arrives in portrait.

The GBA area is cropped by fixed fractions of the projector (`RECORTE` in `fireredia/percepcao/olhos.py`),
calibrated for the Switch release. Adjust it if your frame has a different border.

## 3. Controller (WSL + NXBT)

In WSL, use **Ubuntu 22.04**: NXBT pins `dbus-python==1.2.16`, which does not build on the Python 3.12 of 24.04.

```bash
sudo apt update && sudo apt install -y python3-pip bluez
sudo pip3 install nxbt
```

In an elevated PowerShell, share the dongle with WSL once:

```powershell
usbipd list                                  # find the dongle's VID:PID
usbipd bind --hardware-id 0a12:0001
```

`python -m fireredia` attaches the dongle (`usbipd attach --wsl`), starts `fireredia/controle/servidor_wsl.py` as
root and waits for the connection. While the dongle is attached, Windows has no Bluetooth. To give it back:

```powershell
usbipd detach --hardware-id 0a12:0001
```

**First pairing:** on the Switch, open *Controllers → Change Grip/Order* and start the AI. The controller pairs as a
Pro Controller and its address is saved in `memoria/switch_endereco.txt`. After that it reconnects without that
screen.

**Troubleshooting**

| Symptom | Cause and fix |
|---|---|
| `maos.estado()` is `offline`, but `curl 127.0.0.1:8765` inside WSL answers `connected` | WSL's localhost forwarding broke. Use the WSL IP: `MAOS_URL=http://<wsl hostname -I>:8765/`. |
| State `crashed` with `Connection reset by peer` | The Switch refused the saved pairing. Open *Change Grip/Order* and start again. |
| Nothing connects and the Switch screen is off | The console is asleep, and an emulated controller can't wake it. Press a button on the console. |
| Two `servidor_wsl.py` processes | They fight over the dongle: `wsl -u root pkill -f servidor_wsl.py`. |

## 4. Model provider

Copy `.env.exemplo` to `.env`. It stays local and is git-ignored. Choose the provider:

| `IA_PROVEDOR` | Key | Models |
|---|---|---|
| `anthropic` (default) | optional `ANTHROPIC_API_KEY`; without it, the Claude Code login is used | Opus as strategist, Sonnet as executor |
| `openai` | `OPENAI_API_KEY` | `IA_MODELO_ESTRATEGISTA` and `IA_MODELO_EXECUTOR` required |
| `gemini` | `GEMINI_API_KEY` | same |

`IA_ESFORCO_ESTRATEGISTA` and `IA_ESFORCO_EXECUTOR` set the reasoning effort (`low`, `medium`, `high`, `nenhum`).
All machine settings (`MAOS_URL`, `CAMERA_OBS`, `OBS_PROJETOR`, `WSL_DISTRO`, `BLUETOOTH_DONGLE`, `FIRERED_DECOMP`)
can also go in `.env`.

## 5. Run

With FireRed open on the overworld:

```powershell
.venv\Scripts\python -m fireredia                        # controller + dashboard + agent episodes
.venv\Scripts\python -m fireredia --restricao "fire types only"
.venv\Scripts\python -m fireredia.painel.app             # dashboard window with Play / Stop
```

Stop with Ctrl+C or the Stop button. Progress lives in `memoria/`, and the next run continues from it. Delete
`memoria/` to start a new campaign. Logs go to `logs/` (`jogo.log`, `controle.log`), and screenshots from scripts
go to `logs/fotos/`.
