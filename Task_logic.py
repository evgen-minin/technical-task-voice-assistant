import datetime

if __name__ == '__main__':
    import libneuro

    nn = libneuro.NeuroNetLibrary()  # Создание экземпляра класса NeuroNetLibrary из модуля libneuro.
    nlu = libneuro.NeuroNluLibrary()  # Создание экземпляра класса NeuroNluLibrary из модуля libneuro.
    nv = libneuro.NeuroVoiceLibrary()  # Создание экземпляра класса NeuroVoiceLibrary из модуля libneuro.

    InvalidCallStateError = libneuro.InvalidCallStateError
    check_call_state = libneuro.check_call_state

"""Тайминги для спикера по юнитам"""

hello_unit_timing = {'no_input_timeout': 2700,
                     'recognition_timeout': 6000,
                     'speech_complete_timeout': 700,
                     'asr_complete_timeout': 700,
                     'interruption_no_input_timeout': 50}

payment_unit_timing = {'no_input_timeout': 4500,
                       'recognition_timeout': 90000,
                       'speech_complete_timeout': 1150,
                       'asr_complete_timeout': 1150,
                       'interruption_no_input_timeout': 800}
tv_unit_timing = {'no_input_timeout': 4000,
                  'recognition_timeout': 100000,
                  'speech_complete_timeout': 1300,
                  'asr_complete_timeout': 1300,
                  'start_timeout': 1000,
                  'interruption_no_input_timeout': 2000}
internet_unit_timing = {'no_input_timeout': 4000,
                        'recognition_timeout': 100000,
                        'speech_complete_timeout': 1300,
                        'asr_complete_timeout': 1300,
                        'start_timeout': 1000,
                        'interruption_no_input_timeout': 2000}
internet_green_unit_timing = {'no_input_timeout': 4000,
                              'recognition_timeout': 100000,
                              'speech_complete_timeout': 1300,
                              'asr_complete_timeout': 1300,
                              'start_timeout': 1000,
                              'interruption_no_input_timeout': 2000}
more_question_unit_timing = {'no_input_timeout': 4000,
                             'recognition_timeout': 100000,
                             'speech_complete_timeout': 1300,
                             'asr_complete_timeout': 1300,
                             'start_timeout': 1000,
                             'interruption_no_input_timeout': 2000}
goodbye_unit_timing = {'no_input_timeout': 4000,
                       'recognition_timeout': 100000,
                       'speech_complete_timeout': 1300,
                       'asr_complete_timeout': 1300,
                       'start_timeout': 1000,
                       'interruption_no_input_timeout': 2000}

"""Паттерны распознавания"""
# hello_unit
hello_unit_entity_list = [
    "payment_problem",
    "internet_problem",
    "tv_problem",
    "repeat",
    "robot",
    "operator",
]
hello_unit_entity_interruption_list = [
    "payment_problem",
    "internet_problem",
    "tv_problem",
    "repeat",
    "robot",
    "operator",
]
# payment_unit
payment_unit_entity_list = [
    "pay_site",
    "offices",
    "repeat",
    "promise_pay",
    "operator",
    "confirm",
]
payment_unit_entity_interruption_list = [
    "pay_site",
    "offices",
    "repeat",
    "promise_pay",
    "operator",
    "confirm",
]
# tv_unit
tv_unit_entity_list = [
    "repeat",
    "robot",
    "confirm",
    "operator",
]
tv_unit_entity_interruption_list = [
    "repeat",
    "robot",
    "confirm",
    "operator",
]
# internet_unit
internet_unit_entity_list = [
    "robot",
    "repeat",
    "operator",
    "confirm",
]
internet_unit_entity_interruption_list = [
    "robot",
    "repeat",
    "operator",
    "confirm",
]
# internet_green_unit
internet_green_unit_entity_list = [
    "confirm",
    "operator",
    "repeat",
    "robot",
]
internet_green_unit_entity_interruption_list = [
    "confirm",
    "operator",
    "repeat",
    "robot",
]
# more_question_unit
more_question_unit_entity_list = [
    "payment_problem",
    "internet_problem",
    "tv_problem",
    "robot",
    "no_question",
    "operator",
    "confirm",
]
more_question_unit_entity_interruption_list = [
    "payment_problem",
    "internet_problem",
    "tv_problem",
    "robot",
    "no_question",
    "operator",
    "confirm",
]


def main():
    nn.call('+7' + nn.dialog['msisdn'], entry_point='main_online_container',
            on_success_call='after_call_succes',
            on_failed_call='after_call_fail',
            )


def main_online_container():
    """Настройки проекта"""
    try:
        nn.env('msisdn', nn.dialog['msisdn'])
        nn.env('start_time', nn.env('call_start_time'))
        now = datetime.datetime.now() + datetime.timedelta(hours=3)
        nn.env('start_time_str', str(now))
        nn.env('duration', nv.get_call_duration())
        main_online()
    except InvalidCallStateError:
        nn.log("Звонок завершен, пропускается выполнение функций")
    finally:
        call_uuid = nn.env('call_uuid')
        nn.env('call_record',
               f'https://panel-v2.smartdialogs.ru/downloads?'
               f'call_uuid={call_uuid}')
        nn.env('duration', nv.get_call_duration())
        nn.env('call_transcript', nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT))


def main_online():
    nn.env('flag', 'nadya_ozvuchker')
    nn.log('Новый звонок, начало логики main_online')
    nv.background('office')
    return hello_unit()


# hello_unit.
@check_call_state(nv)
def hello_unit(*prompts):
    nn.log('unit', 'hello_unit')
    """Функция распознавания речи"""
    nv.set_default('listen', hello_unit_timing)
    with nv.listen((
            hello_unit_entity_interruption_list,
            None, None, 'AND'),
            drop_ni_utterance=True,
            entities=hello_unit_entity_list
    ) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
                nv.say(prompt)
    return hello_logic(r)


@check_call_state(nv)
def hello_logic(r):
    nn.log("hello_logic")
    if nn.counter('hello_logic', '+') >= 100:
        nn.log('Recursive usage')
        return
    if not r:
        nn.log("condition", "NULL")
        if nn.counter('hello_null_counter', '+') <= 1:
            return hello_unit('hello_null_prompt')
        return goodbye_null_prompt()

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return hello_unit('hello_default_prompt')

    if r.has_entity('payment_problem'):
        if r.entity('payment_problem') == "true":
            nn.log('condition', 'payment_problem=true')
            return payment_unit('payment_main_prompt')

    if r.has_entity('internet_problem'):
        if r.entity('internet_problem') == "true":
            nn.log('condition', 'internet_problem=true')
            return internet_unit('internet_main_prompt')

    if r.has_entity('tv_problem'):
        if r.entity('tv_problem') == "true":
            nn.log('condition', 'tv_problem=true')
            return tv_unit('tv_main_prompt')

    if r.has_entity('repeat'):
        if r.entity('repeat') == "true":
            nn.log('condition', 'repeat=true')
            return hello_unit('hello_repeat_prompt')

    if r.has_entity('robot'):
        if r.entity('robot') == "true":
            nn.log('condition', 'robot=true')
            return hello_unit('hello_robot_prompt')

    if r.has_entity('operator'):
        if r.entity('operator') == "true":
            nn.log('condition', 'operator=true')
            return goodbye_operator_demand_prompt()


# payment_unit
@check_call_state(nv)
def payment_unit(*prompts):
    nn.log('unit', 'payment_unit')
    """Функция распознавания речи"""
    nv.set_default('listen', payment_unit_timing)
    with nv.listen((
            payment_unit_entity_interruption_list,
            None, None, 'AND'),
            drop_ni_utterance=True,
            entities=payment_unit_entity_list
    ) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
                nv.say(prompt)
    return payment_logic(r)


@check_call_state(nv)
def payment_logic(r):
    nn.log("payment_logic")
    if nn.counter('payment_logic', '+') >= 100:
        nn.log('Recursive usage')
        return
    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return payment_unit('payment_default_prompt')

    if not r:
        nn.log("condition", "NULL")
        if nn.counter('payment_null_counter', '+') <= 1:
            return payment_unit('payment_null_prompt')
        return goodbye_null_prompt()

    if r.has_entity('pay_site'):
        if r.entity('pay_site') == "true":
            nn.log('condition', 'pay_site=true')
            return payment_unit('payment_site_prompt')

    if r.has_entity('offices'):
        if r.entity('offices') == "true":
            nn.log('condition', 'offices=true')
            return payment_unit('payment_offices_prompt')

    if r.has_entity('repeat'):
        if r.entity('repeat') == "true":
            nn.log('condition', 'repeat=true')
            return payment_unit('payment_repeat_prompt')

    if r.has_entity('promise_pay'):
        if r.entity('promise_pay') == "true":
            nn.log('condition', 'promise_pay=true')
            return payment_unit('payment_promise_pay_prompt')

    if r.has_entity('operator'):
        if r.entity('operator') == "true":
            nn.log('condition', 'operator=true')
            return goodbye_operator_demand_prompt()

    if r.has_entity('confirm'):
        if r.entity('confirm') == "true":
            nn.log('condition', 'confirm=true')
            return more_question_unit('more_question_main_prompt')
        if r.entity('confirm') == "false":
            nn.log('condition', 'confirm=true')
            return goodbye_main_prompt()


# tv_unit
@check_call_state(nv)
def tv_unit(*prompts):
    nn.log('unit', 'tv_unit')
    """Функция распознавания речи"""
    nv.set_default('listen', tv_unit_timing)
    with nv.listen((
            tv_unit_entity_interruption_list,
            None, None, 'AND'),
            drop_ni_utterance=True,
            entities=tv_unit_entity_list
    ) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
                nv.say(prompt)
    return tv_logic(r)


@check_call_state(nv)
def tv_logic(r):
    nn.log("tv_logic")
    if nn.counter('tv_logic', '+') >= 100:
        nn.log('Recursive usage')
        return

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return tv_unit('tv_default_prompt')

    if not r:
        nn.log("condition", "NULL")
        if nn.counter('tv_null_counter', '+') <= 1:
            return tv_unit('tv_null_prompt')

    if r.has_entity('repeat'):
        if r.entity('repeat') == "true":
            nn.log('condition', 'repeat=true')
            return tv_unit('tv_repeat_prompt')

    if r.has_entity('robot'):
        if r.entity('robot') == "true":
            nn.log('condition', 'robot=true')
            return tv_unit('tv_robot_prompt')

    if r.has_entity('confirm'):
        if r.entity('confirm') == "true":
            nn.log('condition', 'confirm=true')
            return more_question_unit('more_question_main_prompt')
        if r.entity('confirm') == "false":
            nn.log('condition', 'confirm=true')
            return goodbye_main_prompt()

    if r.has_entity('operator'):
        if r.entity('operator') == "true":
            nn.log('condition', 'operator=true')
            return goodbye_operator_demand_prompt()


# internet_unit
@check_call_state(nv)
def internet_unit(*prompts):
    nn.log('unit', 'internet_unit')
    """Функция распознавания речи"""
    nv.set_default('listen', internet_unit_timing)
    with nv.listen((
            internet_unit_entity_interruption_list,
            None, None, 'AND'),
            drop_ni_utterance=True,
            entities=internet_unit_entity_list
    ) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
                nv.say(prompt)
    return internet_logic(r)


@check_call_state(nv)
def internet_logic(r):
    nn.log("internet_logic")
    if nn.counter('internet_logic', '+') >= 100:
        nn.log('Recursive usage')
        return

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return internet_unit('internet_default_prompt')

    if not r:
        nn.log("condition", "NULL")
        if nn.counter('internet_null_counter', '+') <= 1:
            return internet_unit('internet_null_prompt')
        return goodbye_null_prompt()

    if r.has_entity('robot'):
        if r.entity('robot') == "true":
            nn.log('condition', 'robot=true')
            return internet_unit('internet_robot_prompt')

    if r.has_entity('repeat'):
        if r.entity('repeat') == "true":
            nn.log('condition', 'repeat=true')
            return internet_unit('internet_repeat_prompt')

    if r.has_entity('operator'):
        if r.entity('operator') == "true":
            nn.log('condition', 'operator=true')
            return goodbye_operator_demand_prompt()

    if r.has_entity('confirm'):
        if r.entity('confirm') == "true":
            nn.log('condition', 'confirm=true')
            return goodbye_operator_prompt()
        if r.entity('confirm') == "false":
            nn.log('condition', 'confirm=true')
            return internet_unit('internet_green_main_prompt')


# internet_green_unit
@check_call_state(nv)
def internet_green_unit(*prompts):
    nn.log('unit', 'internet_green_unit')
    """Функция распознавания речи"""
    nv.set_default('listen', internet_green_unit_timing)
    with nv.listen((
            internet_green_unit_entity_interruption_list,
            None, None, 'AND'),
            drop_ni_utterance=True,
            entities=internet_green_unit_entity_list
    ) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
                nv.say(prompt)
    return tv_logic(r)


@check_call_state(nv)
def internet_green_logic(r):
    nn.log("internet_green_logic")
    if nn.counter('internet_green_logic', '+') >= 100:
        nn.log('Recursive usage')
        return

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return internet_green_unit('internet_green_default_prompt')

    if not r:
        nn.log("condition", "NULL")
        if nn.counter('internet_green_null_counter', '+') <= 1:
            return internet_green_unit('internet_green_null_prompt')
        return goodbye_null_prompt()

    if r.has_entity('confirm'):
        if r.entity('confirm') == "true":
            nn.log('condition', 'confirm=true')
            return more_question_unit('more_question_main_prompt')
        if r.entity('confirm') == "false":
            nn.log('condition', 'confirm=true')
            return goodbye_internet_green_prompt()

    if r.has_entity('operator'):
        if r.entity('operator') == "true":
            nn.log('condition', 'operator=true')
            return goodbye_operator_demand_prompt()

    if r.has_entity('repeat'):
        if r.entity('repeat') == "true":
            nn.log('condition', 'repeat=true')
            return internet_unit('internet_green_repeat_prompt')

    if r.has_entity('robot'):
        if r.entity('robot') == "true":
            nn.log('condition', 'robot=true')
            return internet_green_unit('internet_green_robot_prompt')


# more_question_unit
@check_call_state(nv)
def more_question_unit(*prompts):
    nn.log('unit', 'more_question_unit')
    """Функция распознавания речи"""
    nv.set_default('listen', more_question_unit_timing)
    with nv.listen((
            more_question_unit_entity_interruption_list,
            None, None, 'AND'),
            drop_ni_utterance=True,
            entities=more_question_unit_entity_list
    ) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
                nv.say(prompt)
    return more_question_logic(r)


@check_call_state(nv)
def more_question_logic(r):
    nn.log("more_question_logic")
    if nn.counter('more_question_logic', '+') >= 100:
        nn.log('Recursive usage')
        return

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return more_question_unit('more_question_default_prompt')

    if not r:
        nn.log("condition", "NULL")
        if nn.counter('more_question_null_counter', '+') <= 1:
            return more_question_unit('more_question_default_prompt')
        return goodbye_null_prompt()

    if r.has_entity('payment_problem'):
        if r.entity('payment_problem') == "true":
            nn.log('condition', 'payment_problem=true')
            return payment_unit('payment_main_prompt')

    if r.has_entity('internet_problem'):
        if r.entity('internet_problem') == "true":
            nn.log('condition', 'internet_problem=true')
            return internet_unit('internet_main_prompt')

    if r.has_entity('tv_problem'):
        if r.entity('tv_problem') == "true":
            nn.log('condition', 'tv_problem=true')
            return tv_unit('tv_main_prompt')

    if r.has_entity('robot'):
        if r.entity('robot') == "true":
            nn.log('condition', 'robot=true')
            return more_question_unit('more_question_robot_prompt')

    if r.has_entity('no_question'):
        if r.entity('no_question') == "true":
            nn.log('condition', 'no_question=true')
            return goodbye_main_prompt()

    if r.has_entity('operator'):
        if r.entity('operator') == "true":
            nn.log('condition', 'operator=true')
            return goodbye_operator_demand_prompt()

    if r.has_entity('confirm'):
        if r.entity('confirm') == "true":
            nn.log('condition', 'confirm=true')
            return more_question_unit('more_question_confirm_prompt')


def goodbye_null_prompt():
    nn.log('unit', 'goodbye_null')
    nv.say('goodbye_null_prompt')
    nn.env("set_output")
    nv.hangup()
    return

def goodbye_operator_demand_prompt():
    nn.log('unit', 'goodbye_operator_demand')
    nv.say('goodbye_operator_demand_prompt')
    nn.env("set_output")
    nv.hangup()
    return


def goodbye_main_prompt():
    nn.log('unit', 'goodbye_main')
    nv.say('goodbye_main_prompt')
    nn.env("set_output")
    nv.hangup()
    return


def goodbye_operator_prompt():
    nn.log('unit', 'goodbye_operator')
    nv.say('goodbye_operator_prompt')
    nn.env("set_output")
    nv.hangup()
    return


def goodbye_internet_green_prompt():
    nn.log('unit', 'goodbye_internet_green')
    nv.say('goodbye_internet_green_prompt')
    nn.env("set_output")
    nv.hangup()
    return
