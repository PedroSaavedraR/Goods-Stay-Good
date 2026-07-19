from pathlib import Path

from world_state.world_state import AirQuality

OUTPUT = Path(__file__).parent / "problem.pddl"


def generate(world):

    facts = []

    # Current air quality
    if world.air_quality == AirQuality.BAD:
        facts.append("(bad_air)")


    # Fan reason
    if world.fan_needed_by_air:
        facts.append("(fan_needed_by_air)")


    problem = f"""
(define (problem smart-truck)

    (:domain smart-truck)

    (:init
        {' '.join(facts)}
    )

    (:goal
        (and
            (not (bad_air))
            (not (fan_needed_by_air))
        )
    )
)
"""

    OUTPUT.write_text(problem)
