import openfst_python as fst
from pydub import AudioSegment
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


def get_trim_index(sound, silence_threshold=-50.0, chunk_size=10):
    trim_ms = 0

    assert chunk_size > 0
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


def get_audio_without_initial_silence(silence_threshold=-50.0, chunk_size=10):
    sound = AudioSegment.from_file("/content/VoiceCOntrolledGame/pilichm/data/recordings/Nagranie.wav", format="wav")
    start_trim = get_trim_index(sound)
    end_trim = get_trim_index(sound.reverse())
    duration = len(sound)
    trimmed_sound = sound[start_trim:duration - end_trim]
    trimmed_sound.export("/content/VoiceCOntrolledGame/pilichm/data/recordings/Nagranie.wav", format="wav")


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
        s3 = self.grammar.add_state()
        s4 = self.grammar.add_state()

        self.grammar = add_arc(s0, s1, 'prawo', wsyms, self.grammar)
        self.grammar = add_arc(s0, s2, 'lewo', wsyms, self.grammar)
        self.grammar = add_arc(s0, s3, 'góra', wsyms, self.grammar)
        self.grammar = add_arc(s1, s4, 'dół', wsyms, self.grammar)

        s5 = self.grammar.add_state()
        s6 = self.grammar.add_state()
        s7 = self.grammar.add_state()
        s8 = self.grammar.add_state()

        self.grammar = add_arc(s1, s5, 'prawo', wsyms, self.grammar)
        self.grammar = add_arc(s2, s6, 'lewo', wsyms, self.grammar)
        self.grammar = add_arc(s3, s7, 'góra', wsyms, self.grammar)
        self.grammar = add_arc(s4, s8, 'dół', wsyms, self.grammar)

        s9 = self.grammar.add_state()

        self.grammar = add_arc(s5, s9, 'prawo', wsyms, self.grammar)
        self.grammar = add_arc(s6, s9, 'lewo', wsyms, self.grammar)
        self.grammar = add_arc(s7, s9, 'góra', wsyms, self.grammar)
        self.grammar = add_arc(s8, s9, 'dół', wsyms, self.grammar)

        self.grammar.set_start(s0)
        self.grammar.set_final(s9)

        self.grammar = fst.determinize(self.grammar.rmepsilon())
