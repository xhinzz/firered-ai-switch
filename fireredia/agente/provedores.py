"""Episódios com GPT (OpenAI, Responses API) e Gemini (Google GenAI): mesmo prompt, mesmas ferramentas e mesma memória
do cérebro com Claude, num laço de chamadas de ferramenta escrito aqui (o Agent SDK só fala com modelos Claude).

Chaves no ambiente (ou no .env): OPENAI_API_KEY para openai; GEMINI_API_KEY (ou GOOGLE_API_KEY) para gemini.
"""

import base64
import json

from fireredia.agente import ferramentas

TELAS_GUARDADAS = 2  # só as últimas telas vão de novo ao modelo; as antigas viram texto (contexto e custo)
OMITIDA = "[tela antiga omitida]"


def _esquema(t):
    return t.input_schema or {"type": "object", "properties": {}}


def _inteiros(v):
    """O Gemini devolve número inteiro como float (12.0); as ferramentas usam x/y/nível como índice."""
    if isinstance(v, float) and v.is_integer():
        return int(v)
    if isinstance(v, dict):
        return {k: _inteiros(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_inteiros(x) for x in v]
    return v


async def _executar(nome, args):
    """(texto, [(mime, base64)]) do resultado da ferramenta, como o Agent SDK entregaria."""
    t = ferramentas.ULTIMAS.get(nome)
    if not t:
        return f"ferramenta {nome} não existe", []
    try:
        r = await t.handler(_inteiros(args))
    except Exception as exc:  # argumento inválido do modelo: ele precisa ver o erro para corrigir
        return f"{nome} falhou: {exc}", []
    textos = [c["text"] for c in r["content"] if c["type"] == "text"]
    imagens = [(c["mimeType"], c["data"]) for c in r["content"] if c["type"] == "image"]
    return ("ERRO: " if r.get("is_error") else "") + "\n".join(textos), imagens


async def episodio_openai(sistema, pedido, modelo, esforco, turnos, ao_pensar, ao_chamar):
    """Devolve (turnos usados, tokens de entrada, tokens de saída)."""
    from openai import AsyncOpenAI

    cliente = AsyncOpenAI()
    tools = [
        {"type": "function", "name": t.name, "description": t.description, "parameters": _esquema(t), "strict": False}
        for t in ferramentas.ULTIMAS.values()
    ]
    entrada, entra, sai = [{"role": "user", "content": pedido}], 0, 0
    for turno in range(1, turnos + 1):
        _podar_openai(entrada)
        r = await cliente.responses.create(
            model=modelo,
            instructions=sistema,
            input=entrada,
            tools=tools,
            **({"reasoning": {"effort": esforco}} if esforco else {}),
        )
        entra, sai = entra + r.usage.input_tokens, sai + r.usage.output_tokens
        entrada += r.output  # inclui o raciocínio e as chamadas: o modelo precisa delas no turno seguinte
        if r.output_text.strip():
            ao_pensar(r.output_text.strip())
        chamadas = [i for i in r.output if i.type == "function_call"]
        if not chamadas:
            return turno, entra, sai
        for c in chamadas:
            args = json.loads(c.arguments or "{}")
            ao_chamar(c.name, args)
            texto, imagens = await _executar(c.name, args)
            entrada.append(
                {
                    "type": "function_call_output",
                    "call_id": c.call_id,
                    "output": [{"type": "input_text", "text": texto}]
                    + [{"type": "input_image", "image_url": f"data:{m};base64,{b}"} for m, b in imagens],
                }
            )
    return turnos, entra, sai


def _podar_openai(entrada):
    saidas = [i for i in entrada if isinstance(i, dict) and i.get("type") == "function_call_output"]
    for i in saidas[:-TELAS_GUARDADAS]:
        if isinstance(i["output"], list):
            i["output"] = [
                p if p["type"] != "input_image" else {"type": "input_text", "text": OMITIDA} for p in i["output"]
            ]


async def episodio_gemini(sistema, pedido, modelo, esforco, turnos, ao_pensar, ao_chamar):
    """Devolve (turnos usados, tokens de entrada, tokens de saída)."""
    from google import genai
    from google.genai import types

    cliente = genai.Client()
    declaracoes = [
        types.FunctionDeclaration(name=t.name, description=t.description, parameters_json_schema=_esquema(t))
        for t in ferramentas.ULTIMAS.values()
    ]
    config = types.GenerateContentConfig(
        system_instruction=sistema,
        tools=[types.Tool(function_declarations=declaracoes)],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        **({"thinking_config": types.ThinkingConfig(thinking_level=esforco)} if esforco else {}),
    )
    conversa, entra, sai = [types.Content(role="user", parts=[types.Part.from_text(text=pedido)])], 0, 0
    for turno in range(1, turnos + 1):
        _podar_gemini(conversa)
        r = await cliente.aio.models.generate_content(model=modelo, contents=conversa, config=config)
        if r.usage_metadata:
            entra += r.usage_metadata.prompt_token_count or 0
            sai += r.usage_metadata.candidates_token_count or 0
        if not r.candidates or not r.candidates[0].content:
            return turno, entra, sai
        conteudo = r.candidates[0].content
        conversa.append(conteudo)  # devolve também as assinaturas de pensamento, que o Gemini exige
        texto = "".join(p.text for p in conteudo.parts or [] if p.text and not p.thought).strip()
        if texto:
            ao_pensar(texto)
        chamadas = r.function_calls or []
        if not chamadas:
            return turno, entra, sai
        partes = []
        for c in chamadas:
            args = dict(c.args or {})
            ao_chamar(c.name, args)
            texto, imagens = await _executar(c.name, args)
            partes.append(
                types.Part(
                    function_response=types.FunctionResponse(
                        id=c.id,
                        name=c.name,
                        response={"output": texto},
                        parts=[
                            types.FunctionResponsePart(
                                inline_data=types.FunctionResponseBlob(mime_type=m, data=base64.b64decode(b))
                            )
                            for m, b in imagens
                        ]
                        or None,
                    )
                )
            )
        conversa.append(types.Content(role="user", parts=partes))
    return turnos, entra, sai


def _podar_gemini(conversa):
    respostas = [p.function_response for c in conversa for p in c.parts or [] if p.function_response]
    for fr in respostas[:-TELAS_GUARDADAS]:
        if fr.parts:
            fr.parts = None
            fr.response = {**(fr.response or {}), "tela": OMITIDA}


EPISODIOS = {"openai": episodio_openai, "gemini": episodio_gemini}
