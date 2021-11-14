import openfst_python as fst

wordlist = ['W', 'Prawo', 'Lewo', 'dół', 'górę']


def add_arc(sf, st, word, wsyms, g):
    wid = wsyms.find(word)
    g.add_arc(sf, fst.Arc(wid, wid, None, st))
    return g


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
        self.grammar = add_arc(s0, s2, 'W', wsyms, self.grammar)
        self.grammar = add_arc(s2, s1, 'górę', wsyms, self.grammar)
        self.grammar = add_arc(s2, s1, 'dół', wsyms, self.grammar)

        self.grammar.set_start(s0)
        self.grammar.set_final(s1)
        self.grammar = fst.determinize(self.grammar.rmepsilon()).minimize()
