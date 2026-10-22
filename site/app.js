// Replay da campanha a partir de dados/campanha.json (gerado por scripts/gerar_site.py) e tradução EN/PT.
"use strict";

const PT = {
  "nav.replay": "Replay", "nav.como": "Como funciona", "nav.pos": "Pós-jogo", "nav.eng": "Engenharia",
  "hero.selo": "Nintendo Switch de verdade · sem emulador · sem ROM",
  "hero.titulo": "Uma IA que zerou <em>Pokémon FireRed</em> num Switch de verdade.",
  "hero.sub": "Ela vê o jogo por uma placa de captura e joga com um controle Bluetooth emulado. Um modelo de linguagem planeja; código determinístico anda, batalha e lê cada pixel. Abaixo, a campanha inteira reproduzida a partir do diário da própria IA.",
  "hero.cta": "Ver o replay", "hero.codigo": "Código-fonte", "hero.legenda": "Quadros capturados do console durante a campanha",
  "n.episodios": "episódios do agente", "n.acoes": "ações", "n.insignias": "insígnias + Campeão", "n.lendarios": "lendários shiny",
  "n.mapas": "mapas visitados", "n.testes": "testes offline",
  "replay.etiqueta": "Replay interativo", "replay.titulo": "Seis dias de jogo, evento por evento",
  "replay.sub": "Cada ponto é um evento real do diário da IA: onde ela estava, o que decidiu, o time que levava. Arraste a linha do tempo ou aperte play; os marcadores pulam para insígnias, marcos da história e capturas. As anotações aparecem como a IA escreveu.",
  "leg.insignia": "insígnia", "leg.marco": "marco da história", "leg.captura": "captura",
  "lado.time": "Time", "lado.insignias": "Insígnias", "lado.pensando": "Última decisão do modelo", "lado.objetivo": "Objetivo",
  "lado.feed": "Diário de eventos", "carregando": "Carregando a campanha…",
  "como.etiqueta": "Como funciona", "como.titulo": "Entra pixel, sai botão",
  "como.sub": "O único sensor é a imagem de 240×160 e a única saída é um controle. O resto é reconstruído do próprio código-fonte decompilado do jogo.",
  "c1.t": "Percepção", "c1.p": "O quadro é comparado com todos os mapas desenhados a partir do decomp pret/pokefirered para achar o tile exato; o texto é lido com a fonte do próprio jogo; as espécies são reconhecidas pelo sprite.",
  "c2.t": "Habilidades", "c2.p": "O caminho pelo mundo inteiro (portas, degraus, Surf, Strength, gelo) roda em malha fechada, conferido quadro a quadro. Batalhas contra selvagens e treinadores, menus e o PC rodam sem o modelo.",
  "c3.t": "Agente", "c3.p": "Um modelo estrategista escreve o plano; um executor joga com cerca de 60 ferramentas. A memória é um histórico só de acréscimo, então cada episódio começa pequeno e nada é esquecido.",
  "f.percepcao": "percepção", "f.habilidades": "habilidades ⇄ agente", "f.controle": "NXBT no WSL",
  "fig.loc": "Localização: o quadro do Switch (à esquerda) e a janela encontrada no mapa desenhado a partir do decomp; o quadrado vermelho é o tile do jogador.",
  "fig.painel": "O painel ao vivo: tela, objetivo e plano, alertas, progresso, time, mochila, Pokédex, mapa atual com o rastro da IA e o histórico completo.",
  "pos.etiqueta": "Pós-jogo", "pos.titulo": "Sete lendários, todos shiny",
  "pos.sub": "Depois do Campeão, missões roteirizadas e execução arbitrária de código (código digitado nos nomes das caixas do PC pelo Mail glitch) capturaram e recoloriram todos. Todo disparo salva antes e confere as caixas na tela.",
  "fig.deoxys": "O triângulo do Deoxys: 11 toques, cada um dentro do limite de passos do jogo (sDeoxysStepCaps). Planejado por busca e resolvido de primeira.",
  "fig.gelo": "Icefall Cave: quatro deslizes no chão de gelo até a escada da HM07, achados por uma busca em largura nos pontos de parada.",
  "g1": "Deoxys shiny, estrela conferida no resumo", "g2": "Cume da Navel Rock depois do Ho-Oh", "g3": "O código ACE escrito nos nomes das caixas 1–11",
  "eng.etiqueta": "Notas de engenharia", "eng.titulo": "O que o hardware real ensina",
  "e1.t": "Perder toque é normal", "e1.p": "O Bluetooth derruba botões, principalmente em animações. Toda ação de várias etapas confere a tela antes de confirmar: cursor da batalha, painel do PC, página e cursor do teclado.",
  "e2.t": "O mapa do decomp não é a verdade toda", "e2.p": "Scripts trocam metatiles e flags escondem NPCs. O navegador modela portas abertas por script e recebe a lista de NPCs que a história já tirou do lugar.",
  "e3.t": "Reproduza o motor, não a intuição", "e3.p": "Só se sai do Surf para elevação 3 (CanStopSurfing); o gelo desliza até bater; o triângulo do Deoxys tem limite de passos. Cada regra virou código e teste.",
  "e4.t": "Testado offline", "e4.p": "36 testes rodam sem console: planejamento em grades sintéticas, navegação nos mapas reais do decomp e percepção em quadros capturados do Switch. A CI roda tudo no Windows.",
  "rodape": "Feito com a decompilação pret/pokefirered, o NXBT e o CodeGenerator do E-Sh4rk. Pokémon e FireRed são marcas da Nintendo, Game Freak e Creatures; este projeto não distribui código do jogo, e as imagens vêm do console do autor e do decomp.",
};
const TEXTOS_EXTRA = {
  en: { evento: "event", episodio: "episode", dia: "Day", insignia: "badge", desconhecido: "position not recorded", vazio: "—" },
  pt: { evento: "evento", episodio: "episódio", dia: "Dia", insignia: "insígnia", desconhecido: "posição não gravada", vazio: "—" },
};
const LENDARIOS = [["MEWTWO", "Cerulean Cave"], ["SUICUNE", "ACE · Viridian"], ["ENTEI", "ACE · Viridian"], ["RAIKOU", "ACE · Viridian"],
  ["HO_OH", "Navel Rock"], ["LUGIA", "Navel Rock"], ["DEOXYS", "Birth Island"]];
const INSIGNIAS = ["Boulder", "Cascade", "Thunder", "Rainbow", "Soul", "Marsh", "Volcano", "Earth"];
const ROTULOS_EN = { decisao: "decision", captura: "capture", insignia: "badge", historia: "story", batalha: "battle", derrota: "defeat",
  objetivo: "objective", evolucao: "evolution", presente: "gift", compra: "purchase", cura: "heal", save: "save", item: "item" };
const ROTULOS_PT = { decisao: "decisão", insignia: "insígnia", historia: "história", evolucao: "evolução" };
const IMPORTANTES = new Set(["decisao", "captura", "insignia", "historia", "batalha", "derrota", "objetivo", "evolucao", "presente", "compra", "cura", "save", "item"]);

const $ = (id) => document.getElementById(id);
const el = (tag, cls, texto) => { const e = document.createElement(tag); if (cls) e.className = cls; if (texto != null) e.textContent = texto; return e; };
const titulo = (s) => s.toLowerCase().replace(/(^|[\s_-])\w/g, (m) => m.toUpperCase()).replace(/_/g, " ").replace("Ho Oh", "Ho-Oh");
function nomeMapa(id) {
  return id.replace(/^MAP_/, "").replace(/([A-Z]+)(\d+)/g, "$1 $2").split("_")
    .map((p) => (/^\d+F$|^B\d+F$/.test(p) ? p : p.charAt(0) + p.slice(1).toLowerCase())).join(" ");
}

// ---------------- idioma ----------------
let idioma = (localStorage.getItem("idioma") || navigator.language || "en").toLowerCase().startsWith("pt") ? "pt" : "en";
const ORIGINAL = {};
for (const e of document.querySelectorAll("[data-t]")) ORIGINAL[e.dataset.t] = e.innerHTML;
function aplicarIdioma() {
  document.documentElement.lang = idioma === "pt" ? "pt-BR" : "en";
  for (const e of document.querySelectorAll("[data-t]")) {
    const texto = idioma === "pt" ? PT[e.dataset.t] : ORIGINAL[e.dataset.t];
    if (texto == null) continue;
    if (e.hasAttribute("data-html")) e.innerHTML = texto; else e.textContent = texto.replace(/<[^>]+>/g, "");
  }
  document.querySelectorAll(".idioma button").forEach((b) => b.classList.toggle("on", b.dataset.lang === idioma));
  if (dados) desenhar();
}
document.querySelectorAll(".idioma button").forEach((b) => (b.onclick = () => { idioma = b.dataset.lang; try { localStorage.setItem("idioma", idioma); } catch {} aplicarIdioma(); }));

// ---------------- lendários ----------------
$("lendarios").replaceChildren(...LENDARIOS.map(([esp, onde]) => {
  const d = el("div", "lendario"), i = el("img", "px"); i.src = `sprites/shiny/${esp}.png`; i.alt = titulo(esp);
  d.append(i, el("b", "", titulo(esp)), el("small", "", onde)); return d;
}));

// ---------------- replay ----------------
let dados = null, indice = 0, tocando = false, acumulado = 0, ultimoQuadro = 0;
const imagens = {}, canvas = $("palco"), ctx = canvas.getContext("2d");
let entrada, ultimaDecisao, ultimoObjetivo, importantes, marcos, inicioMs;
const TILE = 16, ESCALA = 2;

function mapaImg(i) {
  const id = dados.mapas[i][0];
  if (!imagens[id]) { imagens[id] = new Image(); imagens[id].onload = () => desenhar(); imagens[id].src = `mapas/${id}.png`; }
  return imagens[id];
}

function preparar() {
  const ev = dados.eventos, n = ev.length, tipos = dados.tipos;
  entrada = new Int32Array(n); ultimaDecisao = new Int32Array(n); ultimoObjetivo = new Int32Array(n);
  importantes = [];
  let ent = 0, dec = -1, obj = -1;
  for (let i = 0; i < n; i++) {
    if (i && ev[i][3] !== ev[i - 1][3]) ent = i;
    const tipo = tipos[ev[i][2]];
    if (tipo === "decisao") dec = i;
    if (tipo === "objetivo") obj = i;
    entrada[i] = ent; ultimaDecisao[i] = dec; ultimoObjetivo[i] = obj;
    if (IMPORTANTES.has(tipo)) importantes.push(i);
  }
  marcos = [...dados.insignias.slice(1).map(([i]) => [i, "insignia"]), ...dados.marcos.map(([i]) => [i, "marco"]),
    ...dados.capturas.map(([i]) => [i, "captura"])].sort((a, b) => a[0] - b[0]);
  const [d, h] = dados.inicio.split(" "), [dia, mes] = d.split("/");
  inicioMs = new Date(`2026-${mes}-${dia}T${h}`).getTime();
  $("linha").max = n - 1;
  $("marcas").replaceChildren(...marcos.map(([i, tipo]) => {
    const b = el("button", tipo); b.style.left = `${(100 * i) / (n - 1)}%`; b.title = rotuloMarco(i, tipo);
    b.onclick = () => irPara(i); return b;
  }));
  $("nEpisodios").textContent = dados.resumo.episodios.toLocaleString();
  $("nAcoes").textContent = dados.resumo.acoes.toLocaleString();
}

function rotuloMarco(i, tipo) {
  if (tipo === "insignia") return `${dados.insignias.find((x) => x[0] === i)[1]} Badge`;
  if (tipo === "captura") { const c = dados.capturas.find((x) => x[0] === i); return `${titulo(c[1])} nv ${c[2]}`; }
  return dados.marcos.find((x) => x[0] === i)[1];
}

const ultimoAte = (lista, i) => { let lo = 0, hi = lista.length - 1, r = -1; while (lo <= hi) { const m = (lo + hi) >> 1; if (lista[m][0] <= i) { r = m; lo = m + 1; } else hi = m - 1; } return r; };

function desenharMapa(ev) {
  const [, , , m, x, y] = ev, [, w, h] = dados.mapas[m], img = mapaImg(m);
  ctx.fillStyle = "#000"; ctx.fillRect(0, 0, canvas.width, canvas.height);
  if (!img.complete || !img.naturalWidth) return;
  const vw = canvas.width / (TILE * ESCALA), vh = canvas.height / (TILE * ESCALA);
  const cx = x < 0 ? w / 2 : x + .5, cy = y < 0 ? h / 2 : y + .5;
  let ox = w <= vw ? (w - vw) / 2 : Math.min(Math.max(cx - vw / 2, 0), w - vw);
  let oy = h <= vh ? (h - vh) / 2 : Math.min(Math.max(cy - vh / 2, 0), h - vh);
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(img, -ox * TILE * ESCALA, -oy * TILE * ESCALA, w * TILE * ESCALA, h * TILE * ESCALA);
  const px = (tx) => (tx + .5 - ox) * TILE * ESCALA, py = (ty) => (ty + .5 - oy) * TILE * ESCALA;
  const pontos = [];
  for (let k = Math.max(entrada[indice], indice - 400); k <= indice; k++) {
    const e = dados.eventos[k]; if (e[4] < 0) continue;
    const ultimo = pontos[pontos.length - 1]; if (!ultimo || ultimo[0] !== e[4] || ultimo[1] !== e[5]) pontos.push([e[4], e[5]]);
  }
  if (pontos.length > 1) {
    // salto maior que 3 tiles (porta, posição herdada, leitura perdida) não vira linha atravessando paredes
    ctx.strokeStyle = "rgba(255, 196, 0, .9)"; ctx.lineWidth = 5; ctx.lineJoin = ctx.lineCap = "round"; ctx.beginPath();
    pontos.forEach(([a, b], k) => {
      const salto = k && Math.abs(a - pontos[k - 1][0]) + Math.abs(b - pontos[k - 1][1]) > 3;
      if (!k || salto) ctx.moveTo(px(a), py(b)); else ctx.lineTo(px(a), py(b));
    });
    ctx.stroke();
  }
  if (x >= 0) {
    ctx.fillStyle = "#e53935"; ctx.strokeStyle = "#fff"; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.arc(px(x), py(y), 11, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  }
}

function desenhar() {
  if (!dados) return;
  const T = TEXTOS_EXTRA[idioma], ev = dados.eventos[indice], tipos = dados.tipos;
  desenharMapa(ev);
  $("lugar").textContent = nomeMapa(dados.mapas[ev[3]][0]) + (ev[4] < 0 ? ` · ${T.desconhecido}` : ` (${ev[4]}, ${ev[5]})`);
  const quando = new Date(inicioMs + ev[0] * 1000), dia = Math.floor(ev[0] / 86400) + 1;
  $("relogio").textContent = `${T.dia} ${dia} · ${quando.toLocaleString(idioma === "pt" ? "pt-BR" : "en-GB", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" })}`;
  $("info").textContent = `${T.evento} ${(indice + 1).toLocaleString()} / ${dados.eventos.length.toLocaleString()} · ${T.episodio} ${ev[1]}`;
  $("linha").value = indice;

  const t = ultimoAte(dados.times, indice), time = t >= 0 ? dados.times[t][1] : [];
  $("time").replaceChildren(...time.slice(0, 6).map(([esp, nv]) => {
    const d = el("div"), i = el("img", "px"); i.src = `sprites/${esp}.png`; i.alt = esp; i.onerror = () => (i.style.visibility = "hidden");
    d.append(i, el("b", "", titulo(esp)), document.createTextNode(`Lv ${nv}`)); return d;
  }));
  $("nivelTime").textContent = time.length ? `Lv ${Math.max(...time.map((p) => p[1]))} max` : "";
  const nIns = ultimoAte(dados.insignias, indice) + 1;
  $("nInsignias").textContent = `${nIns}/8`;
  $("insignias").replaceChildren(...INSIGNIAS.map((nome, k) => {
    const s = el("span", k < nIns ? "tem" : ""); s.style.backgroundImage = "url(sprites/insignias.png)"; s.style.backgroundPosition = `${-28 * k}px 0`; s.title = nome; return s;
  }));
  $("pensamento").textContent = ultimaDecisao[indice] >= 0 ? dados.eventos[ultimaDecisao[indice]][6] : T.vazio;
  $("objetivo").textContent = ultimoObjetivo[indice] >= 0 ? dados.eventos[ultimoObjetivo[indice]][6] : T.vazio;
  let lo = 0, hi = importantes.length; while (lo < hi) { const m = (lo + hi) >> 1; if (importantes[m] <= indice) lo = m + 1; else hi = m; }
  const ultimos = importantes.slice(Math.max(0, lo - 7), lo).reverse();
  $("nEventos").textContent = `${lo}`;
  $("feed").replaceChildren(...ultimos.map((k) => {
    const e = dados.eventos[k], tipo = tipos[e[2]], li = el("li");
    li.append(el("span", "tag " + tipo, (idioma === "pt" ? ROTULOS_PT : ROTULOS_EN)[tipo] || tipo), el("span", "", e[6]));
    return li;
  }));
}

function irPara(i) { indice = Math.max(0, Math.min(dados.eventos.length - 1, i)); desenhar(); }
function marcoVizinho(direcao) {
  const lista = marcos.map((m) => m[0]);
  const alvo = direcao > 0 ? lista.find((i) => i > indice) : [...lista].reverse().find((i) => i < indice);
  if (alvo != null) irPara(alvo);
}
function quadro(agora) {
  if (!tocando) return;
  const dt = Math.min(250, agora - (ultimoQuadro || agora)); ultimoQuadro = agora;
  acumulado += (dt / 1000) * Number($("velocidade").value);
  if (acumulado >= 1) { const passos = Math.floor(acumulado); acumulado -= passos; irPara(indice + passos); }
  if (indice >= dados.eventos.length - 1) tocar(false); else requestAnimationFrame(quadro);
}
function tocar(sim) {
  tocando = sim; $("icTocar").firstElementChild.setAttribute("href", sim ? "#i-pausa" : "#i-play");
  if (sim) { ultimoQuadro = 0; requestAnimationFrame(quadro); }
}
$("tocar").onclick = () => tocar(!tocando);
$("voltar").onclick = () => marcoVizinho(-1);
$("avancar").onclick = () => marcoVizinho(1);
$("linha").oninput = (e) => irPara(+e.target.value);
document.addEventListener("keydown", (e) => {
  if (!dados || e.target.tagName === "SELECT") return;
  if (e.code === "Space" && document.activeElement !== document.body) return;
  if (e.code === "ArrowRight") irPara(indice + (e.shiftKey ? 50 : 1));
  else if (e.code === "ArrowLeft") irPara(indice - (e.shiftKey ? 50 : 1));
  else return;
  e.preventDefault();
});

aplicarIdioma();
fetch("dados/campanha.json").then((r) => r.json()).then((d) => {
  dados = d; preparar();
  irPara(dados.insignias[1] ? dados.insignias[1][0] - 40 : 0);  // abre logo antes da Cascade Badge
}).catch(() => { $("feed").replaceChildren(el("li", "carregando", "Could not load dados/campanha.json")); });
