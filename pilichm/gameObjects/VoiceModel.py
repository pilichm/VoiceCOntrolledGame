import openfst_python as fst
from Constants import FILE_RECORDINGS_TRANSCRIPTION


def get_words():
    word_dict = []
    with open(FILE_RECORDINGS_TRANSCRIPTION) as f:
        for line in f:
            for word in line.split():
                word_dict.append(word.strip())

    return word_dict


def add_arc(sf, st, word, wsyms, g):
    wid = wsyms.find(word)
    g.add_arc(sf, fst.Arc(wid, wid, None, st))
    return g


class VoiceModel:
    def __init__(self):
        self.word_list = get_words()
        self.l = None
        self.grammar = None

    def create_grammar(self, psyms, wsyms, l):
        self.l = l
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
        self.grammar = add_arc(s0, s2, 'W', wsyms, self.grammar)
        self.grammar = add_arc(s2, s1, 'górę', self.grammar)
        self.grammar = add_arc(s2, s1, 'dół', self.grammar)

        self.grammar.set_start(s0)
        self.grammar.set_final(s1)
        self.grammar = fst.determinize(self.grammar.rmepsilon()).minimize()
