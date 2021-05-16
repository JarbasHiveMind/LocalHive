from ovos_utils.messagebus import FakeBus as _FakeBus


class FakeBus(_FakeBus):
    def __init__(self, *args, **kwargs):
        self.skill_id = None
        super().__init__(*args, **kwargs)

    def bind(self, skill):
        if isinstance(skill, str):
            self.skill_id = skill
        else:
            self.skill_id = skill.skill_id

    def emit(self, message):
        if self.skill_id is not None:
            message.context["skill_id"] = self.skill_id
            message.context["source"] = message.context.get("source") or \
                                        self.skill_id
        super().emit(message)
