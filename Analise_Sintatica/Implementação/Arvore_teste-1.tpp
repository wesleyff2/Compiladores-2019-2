// TREE
digraph {
	programa0 [label=programa]
	lista_declaracoes001 [label=lista_declaracoes]
	programa0 -> lista_declaracoes001
	declaracao00101 [label=declaracao]
	lista_declaracoes001 -> declaracao00101
	declaracao_funcao0010101 [label=declaracao_funcao]
	declaracao00101 -> declaracao_funcao0010101
	tipo001010101 [label=tipo]
	declaracao_funcao0010101 -> tipo001010101
	cabecalho0010101011 [label=cabecalho]
	declaracao_funcao0010101 -> cabecalho0010101011
	lista_parametros001010101101 [label=lista_parametros]
	cabecalho0010101011 -> lista_parametros001010101101
	vazio00101010110101 [label=vazio]
	lista_parametros001010101101 -> vazio00101010110101
	corpo0010101011011 [label=corpo]
	cabecalho0010101011 -> corpo0010101011011
	vazio001010101101101 [label=vazio]
	corpo0010101011011 -> vazio001010101101101
	fim00101010110111 [label=fim]
	cabecalho0010101011 -> fim00101010110111
}
