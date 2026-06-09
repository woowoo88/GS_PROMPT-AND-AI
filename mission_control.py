"""Mission Control AI: monitoramento e analise de uma missao espacial."""

from __future__ import annotations

import argparse
import json
import random
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Callable


SYSTEM_PROMPT = """
Voce e a IA de apoio do Mission Control de uma missao espacial experimental.
Analise apenas os dados fornecidos. Responda em portugues, de forma objetiva,
com: (1) nivel de risco, (2) principais problemas, (3) ate tres acoes imediatas.
Priorize a seguranca da tripulacao, a preservacao de energia, o controle termico
e a recuperacao da comunicacao. Nao invente medicoes ausentes.
""".strip()


@dataclass(frozen=True)
class MissionData:
    temperature_c: float
    energy_percent: float
    signal_percent: float
    oxygen_percent: float
    module_status: str
    timestamp: str


@dataclass(frozen=True)
class MissionAssessment:
    level: str
    alerts: list[str]
    automatic_actions: list[str]


SCENARIOS = {
    "normal": MissionData(
        temperature_c=23.5,
        energy_percent=87.0,
        signal_percent=96.0,
        oxygen_percent=98.0,
        module_status="operacional",
        timestamp="SIMULACAO",
    ),
    "attention": MissionData(
        temperature_c=36.8,
        energy_percent=42.0,
        signal_percent=48.0,
        oxygen_percent=93.0,
        module_status="degradado",
        timestamp="SIMULACAO",
    ),
    "critical": MissionData(
        temperature_c=51.7,
        energy_percent=14.0,
        signal_percent=19.0,
        oxygen_percent=86.0,
        module_status="falha parcial",
        timestamp="SIMULACAO",
    ),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def simulate_data(seed: int | None = None) -> MissionData:
    """Gera telemetria aleatoria, incluindo ocasionalmente valores criticos."""
    rng = random.Random(seed)
    return MissionData(
        temperature_c=round(rng.uniform(18, 55), 1),
        energy_percent=round(rng.uniform(8, 100), 1),
        signal_percent=round(rng.uniform(10, 100), 1),
        oxygen_percent=round(rng.uniform(82, 100), 1),
        module_status=rng.choice(["operacional", "operacional", "degradado"]),
        timestamp=now_iso(),
    )


def get_scenario(name: str) -> MissionData:
    if name == "random":
        return simulate_data()
    data = SCENARIOS[name]
    return MissionData(**{**asdict(data), "timestamp": now_iso()})


def assess_mission(data: MissionData) -> MissionAssessment:
    alerts: list[str] = []
    actions: list[str] = []
    critical = False

    if data.temperature_c >= 45:
        critical = True
        alerts.append("Temperatura critica no modulo")
        actions.append("Ativar resfriamento de emergencia")
    elif data.temperature_c >= 35:
        alerts.append("Temperatura acima da faixa ideal")
        actions.append("Aumentar ventilacao do modulo")

    if data.energy_percent < 20:
        critical = True
        alerts.append("Reserva de energia critica")
        actions.append("Ativar modo de economia e desligar cargas nao essenciais")
    elif data.energy_percent < 40:
        alerts.append("Nivel de energia baixo")
        actions.append("Priorizar recarga pelos paineis solares")

    if data.signal_percent < 25:
        critical = True
        alerts.append("Comunicacao em risco de interrupcao")
        actions.append("Alternar para antena redundante")
    elif data.signal_percent < 50:
        alerts.append("Sinal de comunicacao instavel")
        actions.append("Reorientar antena principal")

    if data.oxygen_percent < 90:
        critical = True
        alerts.append("Oxigenio abaixo do limite seguro")
        actions.append("Isolar modulo e ativar reserva de oxigenio")
    elif data.oxygen_percent < 94:
        alerts.append("Oxigenio requer monitoramento")

    if data.module_status != "operacional":
        alerts.append(f"Modulo com status: {data.module_status}")
        actions.append("Executar diagnostico do modulo")

    if critical:
        level = "CRITICO"
    elif alerts:
        level = "ATENCAO"
    else:
        level = "NORMAL"
        alerts.append("Todos os parametros estao dentro da faixa segura")
        actions.append("Manter monitoramento nominal")

    return MissionAssessment(level, alerts, list(dict.fromkeys(actions)))


def build_user_prompt(
    data: MissionData, assessment: MissionAssessment
) -> str:
    payload = {
        "telemetria": asdict(data),
        "avaliacao_deterministica": asdict(assessment),
    }
    return (
        "Analise a telemetria e valide ou complemente as acoes automaticas:\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )


def query_ollama(
    data: MissionData,
    assessment: MissionAssessment,
    model: str = "llama3.2:1b",
    base_url: str = "http://localhost:11434",
    timeout: int = 120,
) -> str:
    """Consulta a API local do Ollama sem exigir bibliotecas adicionais."""
    body = json.dumps(
        {
            "model": model,
            "stream": False,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_user_prompt(data, assessment),
                },
            ],
            "options": {"temperature": 0.2},
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(
            "Ollama indisponivel. Inicie 'ollama serve' e baixe "
            "'ollama pull llama3.2:1b'."
        ) from exc

    try:
        return result["message"]["content"].strip()
    except (KeyError, TypeError) as exc:
        raise RuntimeError("Resposta inesperada recebida do Ollama.") from exc


def local_summary(data: MissionData, assessment: MissionAssessment) -> str:
    """Resumo de contingencia; nao se apresenta como resposta de IA."""
    del data
    if assessment.level == "NORMAL":
        return "Operacao nominal. Continue o monitoramento dos subsistemas."
    return (
        f"Nivel {assessment.level}. Prioridade: "
        + "; ".join(assessment.automatic_actions[:3])
        + "."
    )


def format_dashboard(
    data: MissionData,
    assessment: MissionAssessment,
    analysis: str,
    analysis_source: str,
) -> str:
    alert_lines = "\n".join(f"  - {item}" for item in assessment.alerts)
    action_lines = "\n".join(
        f"  - {item}" for item in assessment.automatic_actions
    )
    return f"""
============================================================
                  MISSION CONTROL AI
============================================================
Horario UTC   : {data.timestamp}
Nivel         : {assessment.level}
------------------------------------------------------------
Temperatura   : {data.temperature_c:>5.1f} C
Energia       : {data.energy_percent:>5.1f} %
Comunicacao   : {data.signal_percent:>5.1f} %
Oxigenio      : {data.oxygen_percent:>5.1f} %
Modulo        : {data.module_status}
------------------------------------------------------------
ALERTAS
{alert_lines}
------------------------------------------------------------
ACOES AUTOMATICAS
{action_lines}
------------------------------------------------------------
ANALISE ({analysis_source})
{analysis}
============================================================
""".strip()


def run(
    scenario: str,
    use_ai: bool = True,
    ai_client: Callable[[MissionData, MissionAssessment], str] = query_ollama,
) -> str:
    data = get_scenario(scenario)
    assessment = assess_mission(data)
    if use_ai:
        try:
            analysis = ai_client(data, assessment)
            source = "LLAMA VIA OLLAMA"
        except RuntimeError as exc:
            analysis = f"{local_summary(data, assessment)}\nAviso: {exc}"
            source = "CONTINGENCIA LOCAL - IA INDISPONIVEL"
    else:
        analysis = local_summary(data, assessment)
        source = "REGRAS LOCAIS - MODO DEMONSTRACAO"
    return format_dashboard(data, assessment, analysis, source)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mission Control AI")
    parser.add_argument(
        "--scenario",
        choices=[*SCENARIOS, "random"],
        default="random",
        help="Cenario de telemetria a executar.",
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Executa apenas as regras locais, sem chamar o Ollama.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(run(args.scenario, use_ai=not args.no_ai))
