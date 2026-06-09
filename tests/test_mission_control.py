import unittest

from mission_control import (
    SCENARIOS,
    assess_mission,
    build_user_prompt,
    run,
)


class MissionControlTests(unittest.TestCase):
    def test_normal_scenario_has_no_risk_alert(self):
        result = assess_mission(SCENARIOS["normal"])
        self.assertEqual(result.level, "NORMAL")
        self.assertIn("faixa segura", result.alerts[0])

    def test_critical_scenario_triggers_emergency_actions(self):
        result = assess_mission(SCENARIOS["critical"])
        self.assertEqual(result.level, "CRITICO")
        self.assertGreaterEqual(len(result.alerts), 4)
        self.assertTrue(any("economia" in action for action in result.automatic_actions))
        self.assertTrue(any("oxigenio" in action for action in result.automatic_actions))

    def test_prompt_contains_mission_context_and_telemetry(self):
        data = SCENARIOS["attention"]
        prompt = build_user_prompt(data, assess_mission(data))
        self.assertIn("telemetria", prompt)
        self.assertIn("temperature_c", prompt)
        self.assertIn("avaliacao_deterministica", prompt)

    def test_ai_response_is_displayed(self):
        def fake_ai(data, assessment):
            del data, assessment
            return "Resposta de IA validada."

        output = run("critical", ai_client=fake_ai)
        self.assertIn("LLAMA VIA OLLAMA", output)
        self.assertIn("Resposta de IA validada.", output)


if __name__ == "__main__":
    unittest.main()
