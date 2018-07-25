from mechanics.events import Trigger
from mechanics.combat.AttackEvent import AttackEvent
from mechanics.events import DamageEvent
import my_context


def damage_to_attackers(source, protected_unit, damage, interrupt=False):

    def callback_deal_damage(_, attack_event):
        DamageEvent(damage, target=attack_event.source, source=source)


    trig = Trigger(AttackEvent,
                   conditions={"target":protected_unit},
                   source=source,
                   event_callbacks=[callback_deal_damage],
                   is_interrupt=interrupt)

    return trig