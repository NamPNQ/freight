from __future__ import absolute_import

from itertools import chain

from freight.exceptions import ApiError

from . import manager


def parse_checks_config(value):
    result = []
    for data in value:
        try:
            instance = manager.get(data['type'])
        except KeyError:
            raise ApiError(
                message='Invalid check: {}'.format(data['type']),
                name='invalid_check',
            )

        config = data.get('config', {})
        all_options = chain(instance.get_default_options().items(),
                            instance.get_options().items())
        for option, option_values in all_options:
            value = config.get(option)
            if option_values.get('required') and not value:
                raise ApiError(
                    message='Missing required option "{}" for check: {}'.format(option, data['type']),
                    name='invalid_check',
                )
        result.append({
            'type': data['type'],
            'config': config,
        })
    return result
