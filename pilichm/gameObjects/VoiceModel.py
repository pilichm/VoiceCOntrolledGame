import openfst_python as fst
import re

from pilichm.gameObjects.Direction import *
from pilichm.gameObjects.Constants import PATH_TO_GRAMMAR, RECORDING_FILENAME, RESOURCES_DIR, PATH_TO_MODEL_CONF_FILE

wordlist = ['prawo', 'lewo', 'dół', 'góra']


def add_arc(sf, st, word, wsyms, g):
    wid = wsyms.find(word)
    g.add_arc(sf, fst.Arc(wid, wid, None, st))
    return g


def change_model_frequency():
    with open(f'{PATH_TO_MODEL_CONF_FILE}', 'a') as f:
        f.write('\n--sample-frequency=48000')


def create_info_about_recording():
    with open(f'{PATH_TO_GRAMMAR}wav.scp', 'w+') as f:
        f.write(f'{RECORDING_FILENAME} {RESOURCES_DIR}recordings/{RECORDING_FILENAME}')

    with open(f'{PATH_TO_GRAMMAR}spk2utt', 'w+') as f:
        f.write(f'{RECORDING_FILENAME} {RECORDING_FILENAME}')


def get_direction_from_prediction(prediction):
    for line in prediction:
        line = line.lower()
        if line.find(Direction.UP.value) != -1:
            return Direction.UP
        elif line.find(Direction.DOWN.value) != -1:
            return Direction.DOWN
        elif line.find(Direction.LEFT.value) != -1:
            return Direction.LEFT
        elif line.find(Direction.RIGHT.value) != -1:
            return Direction.RIGHT

    return Direction.UNKNOWN


def check_cost(prediction):
    pattern = re.compile("\d{1,6}\.\d{1,6} over")

    for line in prediction:
        result = pattern.search(line)
        if result:
            result = result.group(0)
            result = result.split(' ')[0]
            return float(result)

    return 0


class VoiceModel:
    def __init__(self, psyms, wsyms, l):
        self.word_list = wordlist
        self.l = l
        self.grammar = None
        self.create_grammar(psyms, wsyms)

    def create_grammar(self, psyms, wsyms):
        self.l.set_input_symbols(psyms)
        self.l.set_output_symbols(wsyms)

        self.grammar = fst.Fst()
        self.grammar.set_input_symbols(wsyms)
        self.grammar.set_output_symbols(wsyms)

        s0 = self.grammar.add_state()
        s1 = self.grammar.add_state()
        s2 = self.grammar.add_state()

        self.grammar = add_arc(s0, s1, 'Prawo', wsyms, self.grammar)
        self.grammar = add_arc(s0, s1, 'Lewo', wsyms, self.grammar)
        # self.grammar = add_arc(s0, s2, 'W', wsyms, self.grammar)
        self.grammar = add_arc(s0, s1, 'górę', wsyms, self.grammar)
        self.grammar = add_arc(s0, s1, 'dół', wsyms, self.grammar)

        self.grammar.set_start(s0)
        self.grammar.set_final(s1)
        self.grammar = fst.determinize(self.grammar.rmepsilon()).minimize()
