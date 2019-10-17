
import ply.yacc as yacc
from graphviz import Digraph
from datetime import datetime
from lexico import Lexer
import sys
import ply.lex as lex

class Tree:
    def __init__(self, type_node='', child=[], value='', lineno=''):
        self.type = type_node
        self.child = child
        self.value = value
        self.lineno= lineno

    def __str__(self):
        return self.type

class Syntactic:
    def __init__(self):
        lexer = Lexer()

        #Definição das precedencias
        
        self.tokens = lexer.tokens
        self.precedence = (
            ('left', 'IGUAL', 'MAIOR_IGUAL', 'MAIOR', 'MENOR_IGUAL', 'MENOR'),
            ('left', 'ADICAO', 'SUBTRACAO'),
            ('left', 'MULTIPLICACAO', 'DIVISAO'),
        )
        arq = open(sys.argv[1], 'r', encoding='utf-8')
        data = arq.read()
        parser = yacc.yacc(debug=False, module=self, optimize=False)
        self.ps = parser.parse(data)

    
    ###### Declaração das regras ######
    
    def p_programa(self, p):
        '''programa : lista_declaracoes'''

        p[0] = Tree('programa', [p[1]])

    def p_lista_declaracoes(self, p):
        '''lista_declaracoes : lista_declaracoes declaracao
        | declaracao'''

        if len(p) == 3:
            p[0] = Tree('lista_declaracoes', [p[1], p[2]])
        else:
            p[0] = Tree('lista_declaracoes', [p[1]])

    def p_declaracao(self, p):
        '''declaracao : declaracao_variaveis
        | inicializacao_variaveis
        | declaracao_funcao'''

        p[0] = Tree('declaracao', [p[1]], '', p.lineno(1))

    def p_declaracao_variaveis(self, p):
        '''declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'''

        p[0] = Tree('declaracao_variaveis', [p[1], p[3]])


    def p_inicializacao_variaveis(self, p):
        '''inicializacao_variaveis : atribuicao'''

        p[0] = Tree('inicializacao_variaveis', [p[1]])

    def p_lista_variaveis(self, p):
        '''lista_variaveis : lista_variaveis VIRGULA var
        | var'''

        if len(p) == 4:
            p[0] = Tree('lista_variaveis', [p[1], p[3]])
        else:
            p[0] = Tree('lista_variaveis', [p[1]])

    def p_var(self, p):
        '''var : ID
        | ID indice'''


        if len(p) == 2:
            #h = Tree('ID', [p[1]], p[1], p.lineno(1))
            h = Tree('ID', [], p[1], p.lineno(1))
            p[0] = Tree('var', [h], p[1], p.lineno(1))
            
        elif len(p) == 2:
            p[0] = Tree('var', [p[2]], p[1], p.lineno(1))

    def p_indice(self, p):
        '''indice : indice ABRE_COLCHETES expressao FECHA_COLCHETES
        | ABRE_COLCHETES expressao FECHA_COLCHETES'''

        if len(p) == 5:
            p[0] = Tree('indice', [p[1], p[3]])
        else:
            p[0] = Tree('indice', [p[2]])

    def p_tipo(self, p):
        '''tipo : INTEIRO
        | FLUTUANTE'''

        p[0] = Tree('tipo', [], p[1])

    def p_declaracao_funcao(self, p):
        '''declaracao_funcao : tipo cabecalho
        | cabecalho'''

        if len(p) == 3:
            p[0] = Tree('declaracao_funcao', [p[1], p[2]], '', p.lineno(2))
        else:
            p[0] = Tree('declaracao_funcao', [p[1]], '', p.lineno(1))

    def p_cabecalho(self, p):
        '''cabecalho : ID ABRE_PARENTESES lista_parametros FECHA_PARENTESES corpo FIM'''

        p[0] = Tree('cabecalho', [p[3], p[5], Tree(type_node=p[6])], p[1])

    def p_lista_parametros(self, p):
        '''lista_parametros : lista_parametros VIRGULA parametro
        | parametro
        | vazio '''

        if len(p) == 4:
            p[0] = Tree('lista_parametros', [p[1], p[3]])
        else: 
            p[0] = Tree('lista_parametros', [p[1]])

    def p_parametro(self, p):
        '''parametro : tipo DOIS_PONTOS ID
        |  parametro ABRE_COLCHETES FECHA_COLCHETES'''

        if p[2] == ':':
            p[0] = Tree('parametro', [p[1]], p[3])
        else:
            p[0] = Tree('parametro', [p[1]])

    def p_corpo(self, p):
        '''corpo : corpo acao
        | vazio'''

        if len(p) == 3:
            p[0] = Tree('corpo', [p[1], p[2]])
        else:
            p[0] = Tree('corpo', [p[1]])

    def p_acao(self, p):
        '''acao : expressao
        | declaracao_variaveis
        | se
        | repita
        | leia
        | escreva
        | retorna'''

        p[0] = Tree('acao', [p[1]])

    def p_se(self, p):
        '''se : SE expressao ENTAO corpo FIM
        | SE expressao ENTAO corpo SENAO corpo FIM'''

        if len(p) == 6:
            p[0] = Tree('se', [p[2], p[4], Tree(type_node=p[5])])
        else:
            p[0] = Tree('se', [p[2], p[4], p[6], Tree(type_node=p[7])])

    def p_repita(self, p):
        '''repita : REPITA corpo ATE expressao'''

        p[0] = Tree('repita', [p[2], p[4], Tree(type_node=p[3])])

    def p_leia(self, p):
        '''leia : LEIA ABRE_PARENTESES var FECHA_PARENTESES'''

        p[0] = Tree('leia', [p[3]],'' ,p.lineno(1))
    
    def p_escreva(self, p):
        '''escreva : ESCREVA ABRE_PARENTESES expressao FECHA_PARENTESES '''

        p[0] = Tree('escreva', [p[3]],'' ,p.lineno(1))
    
    def p_retorna(self, p):
        '''retorna : RETORNA ABRE_PARENTESES expressao FECHA_PARENTESES '''

        p[0] = Tree('retorna', [p[3]],'' ,p.lineno(1))
    
    def p_atribuicao(self, p):
        '''atribuicao : var ATRIBUICAO expressao'''

        p[0] = Tree('atribuicao', [p[1], p[3]], '', p.lineno(2))

    def p_expressao(self, p):
        '''expressao : expressao_logica
        | atribuicao'''

        p[0] = Tree('expressao', [p[1]])

    def p_operador_relacional(self, p):
        '''operador_relacional : MENOR
        | MAIOR
        | IGUAL
        | DIFERENTE
        | MENOR_IGUAL
        | MAIOR_IGUAL'''

        p[0] = Tree('operador_relacional', [], str(p[1]), p.lineno(1))

    def p_operador_soma(self, p):
        '''operador_soma : ADICAO
        | SUBTRACAO'''

        p[0] = Tree('operador_soma', [], str(p[1]), p.lineno(1))
    
    def p_operador_logico(self, p):
        '''operador_logico : E_LOGICO
        | OU_LOGICO
        | NEGACAO'''

        p[0] = Tree('operador_logico', [], str(p[1]))

    def p_operador_multiplicacao(self, p):
        '''operador_multiplicacao : MULTIPLICACAO
        | DIVISAO'''

        p[0] = Tree('operador_multiplicacao', [], str(p[1]))
        
    def p_fator(self, p):
        '''fator : ABRE_PARENTESES expressao FECHA_PARENTESES
        | var
        | chamada_funcao
        | numero_int
        | numero_float'''

        if len(p) == 2:
            p[0] = Tree('fator', [p[1]])
        else:
            p[0] = Tree('fator', [p[2]])
        
    def p_numero_int(self, p):
        '''numero_int : INTEIRO'''

        p[0] = Tree('numero_int', [], p[1])
    
    def p_numero_float(self, p):
        '''numero_float : FLUTUANTE'''

        p[0] = Tree('numero_float', [], float(p[1]), p.lineno(1))
    
    def p_chamada_funcao(self, p):
        '''chamada_funcao : ID ABRE_PARENTESES lista_argumentos FECHA_PARENTESES'''

        p[0] = Tree('chamada_funcao', [p[3]], p[1])
    
    def p_lista_argumentos(self, p):
        '''lista_argumentos : lista_argumentos VIRGULA expressao
        | expressao
        | vazio'''

        if len(p) == 2:
            p[0] = Tree('lista_argumentos', [p[1]])
        else:
            p[0] = Tree('lista_argumentos', [p[1], p[3]])

    def p_expressao_logica(self, p):
        '''expressao_logica : expressao_simples
        | expressao_logica operador_logico expressao_simples'''

        if len(p) == 2:
            p[0] = Tree('expressao_logica', [p[1]])
        else:
            p[0] = Tree('expressao_logica', [p[1], p[2], p[3]])

    def p_expressao_simples(self,p):
        '''expressao_simples : expressao_aditiva
        | expressao_simples operador_relacional expressao_aditiva'''

        if len(p) == 2:
            p[0] = Tree('expressao_simples', [p[1]])
        else:
            p[0] = Tree('expressao_simples', [p[1], p[2], p[3]])

    def p_expressao_aditiva(self, p):
        '''expressao_aditiva : expressao_multiplicativa
        | expressao_aditiva operador_soma expressao_multiplicativa'''

        if len(p) == 2:
            p[0] = Tree('expressao_aditiva', [p[1]])
        else:
            p[0] = Tree('expressao_aditiva', [p[1], p[2], p[3]])

    def p_expressao_multiplicativa(self, p):
        '''expressao_multiplicativa : expressao_unaria
        | expressao_multiplicativa operador_multiplicacao expressao_unaria'''

        if len(p) == 2:
            p[0] = Tree('expressao_multiplicativa', [p[1]])
        else:
            p[0] = Tree('expressao_multiplicativa', [p[1], p[2], p[3]])                    

    def p_expressao_unaria(self, p):
        '''expressao_unaria : fator
        | operador_soma fator'''

        if len(p) == 2:
            p[0] = Tree('expressao_unaria', [p[1]])
        else:
            p[0] = Tree('expressao_unaria', [p[1], p[2]])

    def p_vazio(self, p):
        '''vazio : '''

        p[0] = Tree('vazio')
        pass

    def p_error(self, p):
        if p:
            print("Erro Sintatico na linha %d" %(p.lineno))
        else:
            print("Erro!")
    
    def p_leia_error(self, p):
        '''leia : LEIA ABRE_PARENTESES error FECHA_PARENTESES'''

        print("Erro na operação de leitura (Argumento Inválido)")
        exit(1)

    def p_escreva_error(self, p):
        '''escreva : ESCREVA ABRE_PARENTESES error FECHA_PARENTESES '''

        print("Erro na operação de escrita (Argumento Inválido)")
        exit(1)

    def p_retorna_error(self, p):
        '''retorna : RETORNA ABRE_PARENTESES error FECHA_PARENTESES'''

        print("Erro de retorno (Argumento Inválido)")
        exit(1)

    def p_declaracao_variaveis_error(self, p):
        '''declaracao_variaveis : error DOIS_PONTOS lista_variaveis'''

        print("Erro na declaração de variáveis")
        exit(1)
        
    def p_atribuicao_error(self, p):
        '''atribuicao : var ATRIBUICAO error
        | error ATRIBUICAO expressao'''

        print("Erro na atribuição")
        exit(1)
    
    def p_lista_declaracoes_error(self, p):
        '''lista_declaracoes : error error
        | error'''
        print("Erro na lista de declarações")
        exit(1)

    def p_indice_error(self, p):
        '''indice : indice ABRE_COLCHETES error FECHA_COLCHETES
        | ABRE_COLCHETES error FECHA_COLCHETES'''
        print("Erro de índice")
        exit(1)
    
    def p_acao_error(self, p):
        '''acao : error'''
        print("Erro de ação")
        exit(1)


    def p_cabecalho_error(self, p):
        '''cabecalho : ID ABRE_PARENTESES lista_parametros FECHA_PARENTESES error FIM'''

        print("Erro no cabeçalho da função")
        exit(1)

    def p_repita_error(self, p):
        '''repita : REPITA error ATE error'''
        print("Erro no laço 'REPITA'")
        exit(1)

    def p_declaracao_error(self, p):
        '''declaracao : error'''
        print("Erro de declaração")
        exit(1)
    
    def p_inicializacao_variaveis_error(self, p):
        '''inicializacao_variaveis : error'''
        print("Erro na inicialização de variável")
        exit(1)
    
    def p_lista_variaveis_error(self, p):
        '''lista_variaveis : error VIRGULA error
        | error'''
        print("Erro na lista de variáveis")
        exit(1)

    def p_declaracao_funcao_error(self, p):
        '''declaracao_funcao : error error
        | error'''
        print("Erro na declaração de função")
        exit(1)
    
    def p_lista_parametros_error(self, p):
        '''lista_parametros : error VIRGULA error
        | error '''
        print("Erro na lista de parametros")
        exit(1)
    
    def p_corpo_error(self, p):
        '''corpo : error error
        | error'''
        print("Erro no corpo da função")
        exit(1)
    
    def p_se_error(self, p):
        '''se : SE error ENTAO error FIM
        | SE error ENTAO error SENAO error FIM'''
        print("Erro de condicional 'SE'")
        exit(1)

    def p_expressao_error(self, p):
        '''expressao : error'''
        print("Erro de expressão")
        exit(1)

    def p_expressao_simples_error(self,p):
        '''expressao_simples : error
        | error error error'''
        print("Erro na expressão")
        exit(1)

def print_tree(node, dot, i="0", pai=None):
    if node != None:
        filho = str(node) + str(i)
        dot.node(filho, str(node))
        if pai: dot.edge(pai, filho)
        j = "0"
        if not isinstance(node, Tree): return
        for son in node.child:
            j+="1"
            print_tree(son, dot, i+j, filho) 


if __name__ == '__main__':
    now = datetime.now()
    if len(sys.argv) > 1:
        
        syn = Syntactic()
        dot = Digraph(comment='TREE')
        print_tree(syn.ps, dot)
        
        dot.render('Arvore_'+str(sys.argv[1]), view=True)
    else:
        print("Erro de arquivo")
