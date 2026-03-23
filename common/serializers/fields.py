from rest_framework import serializers


class CaseInsensitiveChoiceField(serializers.ChoiceField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            normalized_choices = {
                str(choice_value).strip().lower(): choice_value for choice_value in self.choices.keys()
            }
            normalized_value = normalized_choices.get(data.strip().lower())
            if normalized_value is not None:
                data = normalized_value
        return super().to_internal_value(data)
