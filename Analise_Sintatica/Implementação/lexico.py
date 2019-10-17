# -*- coding: UTF-8 -*-
import ply.lex as lex
from ply.lex import TOKEN
import ply.yacc as yacc


class Lexer:
    def __init__(self):
        self.lexer = lex.lex(debug=False, module=self, optimize=False)

    # Dictionary of reserved words
    reserved = {
        'inteiro': 'INTEIRO',
        'flutuante': 'FLUTUANTE',
        'se': 'SE',
        'então': 'ENTAO',
        'senão': 'SENAO',
        'repita': 'REPITA',
        'até': 'ATE',
        'fim': 'FIM',
        'retorna': 'RETORNA',
        'escreva': 'ESCREVA',
        'leia': 'LEIA',
        'cientifico': 'CIENTIFICO'
    }

    # List of token names
    tokens = ['ADICAO',
              'SUBTRACAO',
              'MULTIPLICACAO',
              'DIVISAO',
              'ATRIBUICAO',
              'IGUAL',
              'MAIOR',
              'MENOR',
              'DIFERENTE',
              'MENOR_IGUAL',
              'MAIOR_IGUAL',
              'VIRGULA',
              'DOIS_PONTOS',
              'E_LOGICO',
              'OU_LOGICO',
              'NEGACAO',
              'ABRE_PARENTESES',
              'FECHA_PARENTESES',
              'ABRE_CHAVES',
              'FECHA_CHAVES',
              'ABRE_COLCHETES',
              'FECHA_COLCHETES',
              'ID',
              'COMENTARIO',
              'NOVA_LINHA'] + \
        list(reserved.values())

    # Regular expressions rulers
    t_ADICAO = r'\+'
    t_SUBTRACAO = r'-'
    t_MULTIPLICACAO = r'\*'
    t_DIVISAO = r'/'
    t_ATRIBUICAO = r':='
    t_IGUAL = r'='
    t_MAIOR = r'>'
    t_MENOR = r'<'
    t_DIFERENTE = r'<>'
    t_MENOR_IGUAL = r'<='
    t_MAIOR_IGUAL = r'>='
    t_VIRGULA = r','
    t_DOIS_PONTOS = r':'
    t_E_LOGICO = r'&&'
    t_OU_LOGICO = r'\|\|'
    t_NEGACAO = r'\!'
    t_ABRE_PARENTESES = r'\('
    t_FECHA_PARENTESES = r'\)'
    t_ABRE_COLCHETES = r'\['
    t_FECHA_COLCHETES = r'\]'

    def t_ID(self, t):
        r'[A-Za-z_][\w_]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_FLUTUANTE(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_INTEIRO(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

        # Only one line comments
    def t_COMENTARIO(self, t):
        r'\{[^}]*[^{]*\}'
        for x in range(1, len(t.value)):
            if t.value[x] == "\n":
                t.lexer.lineno += 1

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

        # Contains ignore characters as spaces and tabs
    t_ignore = ' \t'

        # Error handling rule
    def t_error(self, t):
        if((t.value[0]!= '{') and (t.value[0]!= '}')):
            print("Caractere não reconhecido '%s'" % t.value[0])
        else:
            if (t.value[0] == '{'):
                    print("ERROR: Comentário sem fechamento. } esperado.")
            elif (t.value[0] == '}'):
	                print("ERROR: Comentário sem abertura. { esperado.")
                    
            # return None
        t.lexer.skip(1)



if __name__ == '__main__':
    import sys
    code = open(sys.argv[1], encoding='utf8')
    lexer = Lexer()

    lex.input(code.read())
    while True:
        tok = lex.token()
        if not tok:
            break
        if tok.type == 'ABRECHAVE':
            print('Comentario inacializado e não terminado')

        print(tok.lineno, ':', tok.type, ':', tok.value)
